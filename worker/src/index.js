// rhine-lab — the shared side of nanobotco.github.io/rhine.
//
// The server holds the targets, so a score here is a score the server dealt
// and checked, whether the caller is a person at the page or a robot with curl.
//
//   GET  /                      the API, described
//   POST /session               {test, player, belief, name?}  → {id, trials, chance}
//   POST /session/:id/call      {call}                         → {n, target, hit, hits, done}
//   GET  /session/:id
//   GET  /stats                 pooled tallies, and hits by position in the run
//   GET  /forecast              the open draw, recent draws, the leaderboard
//   GET  /forecast/:day         one draw, its entries and (once drawn) the target
//   POST /forecast              {name?, player, belief, calls:[25 symbols], day?}
//
// Tests: clairvoyance (a closed deck of 25, five of each symbol, shuffled at the
// start, secret until each card is called), precognition (each target drawn
// after its call arrives), dice (call a face 1–6, the server throws; 24 throws).
//
// Forecast: each day's target is 25 symbols from drand quicknet (a public
// randomness beacon run by the League of Entropy), the first round at or after
// 12:00 UTC. Entries close at 11:00 UTC. Anyone can recompute the target:
//   for i = 0, 1, 2 …: b = first byte of SHA-256(randomness_hex + ":" + i);
//   keep b % 5 when b < 250; stop at 25.

const SYM = ["circle", "cross", "waves", "square", "star"];
const TESTS = {
  clairvoyance: { trials: 25, faces: 5, chance: 0.2 },
  precognition: { trials: 25, faces: 5, chance: 0.2 },
  dice: { trials: 24, faces: 6, chance: 1 / 6 },
};
const PLAYERS = ["human", "robot"];
const BELIEFS = ["sheep", "goat", "unsure"];
const GENESIS = 1692803367, PERIOD = 3;
const CHAIN = "52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971";
const SITE = "https://nanobotco.github.io/rhine/";

const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET, POST, OPTIONS",
  "access-control-allow-headers": "content-type",
};
const json = (o, status = 200) =>
  new Response(JSON.stringify(o, null, 1), {
    status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...CORS },
  });
const bad = (msg, status = 400) => json({ error: msg, help: "GET / for the API" }, status);

function rnd(n) {
  // uniform 0..n-1 by rejection
  const lim = 256 - (256 % n), b = new Uint8Array(1);
  for (;;) { crypto.getRandomValues(b); if (b[0] < lim) return b[0] % n; }
}
function shuffledDeck() {
  const a = [];
  for (let i = 0; i < 25; i++) a.push(i % 5);
  for (let i = 24; i > 0; i--) { const j = rnd(i + 1); [a[i], a[j]] = [a[j], a[i]]; }
  return a.join("");
}
function hex(n) {
  const b = new Uint8Array(n); crypto.getRandomValues(b);
  return [...b].map((x) => x.toString(16).padStart(2, "0")).join("");
}
function symbol(v) {
  if (typeof v === "number" && v >= 0 && v < 5) return v | 0;
  const s = String(v ?? "").trim().toLowerCase();
  if (/^[0-4]$/.test(s)) return +s;
  const i = SYM.indexOf(s === "plus" ? "cross" : s === "wave" ? "waves" : s);
  return i >= 0 ? i : null;
}
function face(v) {
  const n = parseInt(String(v ?? "").trim(), 10);
  return n >= 1 && n <= 6 ? n - 1 : null;
}
function cleanName(s) {
  const t = String(s ?? "").normalize("NFC").replace(/[\u0000-\u001f<>&"'`\\]/g, "").trim().slice(0, 32);
  return t;
}
function z(hits, trials, p) {
  if (!trials) return 0;
  return +((hits - trials * p) / Math.sqrt(trials * p * (1 - p))).toFixed(2);
}
async function body(req) {
  const t = await req.text();
  if (t.length > 4000) throw new Error("body too large");
  try { return t ? JSON.parse(t) : {}; } catch { throw new Error("body is not JSON"); }
}

// ---------------------------------------------------------------- sessions

async function newSession(env, b) {
  const test = String(b.test || "").toLowerCase();
  const T = TESTS[test];
  if (!T) return bad("test must be one of: " + Object.keys(TESTS).join(", "));
  const player = PLAYERS.includes(b.player) ? b.player : "human";
  const belief = BELIEFS.includes(b.belief) ? b.belief : "unsure";
  const id = hex(12);
  const deck = test === "clairvoyance" ? shuffledDeck() : null;
  await env.DB.prepare(
    "INSERT INTO sessions (id, test, player, belief, name, created, deck) VALUES (?,?,?,?,?,?,?)"
  ).bind(id, test, player, belief, cleanName(b.name) || null, Date.now(), deck).run();
  await env.DB.prepare(
    "INSERT INTO tally (test, player, belief, runs) VALUES (?,?,?,1) ON CONFLICT DO UPDATE SET runs = runs + 1"
  ).bind(test, player, belief).run();
  return json({
    id, test, player, belief, trials: T.trials, chance: T.chance,
    call: test === "dice" ? "POST /session/" + id + "/call {\"call\": 1-6}" :
      "POST /session/" + id + "/call {\"call\": \"" + SYM.join("|") + "\"}",
  }, 201);
}

async function getSession(env, id) {
  return env.DB.prepare("SELECT * FROM sessions WHERE id = ?").bind(id).first();
}

function view(s) {
  const T = TESTS[s.test];
  const show = (c) => (s.test === "dice" ? +c + 1 : SYM[+c]);
  return {
    id: s.id, test: s.test, player: s.player, belief: s.belief, name: s.name,
    n: s.n, trials: T.trials, hits: s.hits, done: s.n >= T.trials,
    expected: +(T.trials * T.chance).toFixed(2), z: s.n >= T.trials ? z(s.hits, T.trials, T.chance) : undefined,
    calls: [...s.calls].map(show), targets: [...s.targets].map(show),
  };
}

async function call(env, id, b) {
  const s = await getSession(env, id);
  if (!s) return bad("no such session", 404);
  const T = TESTS[s.test];
  if (s.n >= T.trials) return json({ ...view(s), error: "run is complete; POST /session for another" }, 409);
  const c = s.test === "dice" ? face(b.call) : symbol(b.call);
  if (c === null) return bad(s.test === "dice" ? "call a face, 1 to 6" : "call one of: " + SYM.join(", "));
  // clairvoyance: the card was fixed at the shuffle. precognition and dice:
  // the target is drawn now, after the call is in.
  const t = s.test === "clairvoyance" ? +s.deck[s.n] : rnd(T.faces);
  const hit = c === t ? 1 : 0;
  const r = await env.DB.prepare(
    "UPDATE sessions SET calls = calls || ?, targets = targets || ?, n = n + 1, hits = hits + ? WHERE id = ? AND n = ?"
  ).bind(String(c), String(t), hit, id, s.n).run();
  if (!r.meta.changes) return bad("that card was already called; try again", 409);
  await env.DB.batch([
    env.DB.prepare("INSERT INTO tally (test, player, belief, trials, hits) VALUES (?,?,?,1,?) " +
      "ON CONFLICT DO UPDATE SET trials = trials + 1, hits = hits + excluded.hits").bind(s.test, s.player, s.belief, hit),
    env.DB.prepare("INSERT INTO pos (test, pos, trials, hits) VALUES (?,?,1,?) " +
      "ON CONFLICT DO UPDATE SET trials = trials + 1, hits = hits + excluded.hits").bind(s.test, s.n + 1, hit),
  ]);
  const n = s.n + 1, hits = s.hits + hit;
  const out = {
    n, call: s.test === "dice" ? c + 1 : SYM[c], target: s.test === "dice" ? t + 1 : SYM[t],
    hit: !!hit, hits, trials: T.trials, done: n >= T.trials,
  };
  if (out.done) Object.assign(out, { expected: +(T.trials * T.chance).toFixed(2), z: z(hits, T.trials, T.chance) });
  return json(out);
}

async function stats(env) {
  const [t, p] = await Promise.all([
    env.DB.prepare("SELECT * FROM tally").all(),
    env.DB.prepare("SELECT * FROM pos ORDER BY test, pos").all(),
  ]);
  const rows = t.results.map((r) => ({
    ...r, chance: TESTS[r.test]?.chance, rate: r.trials ? +(r.hits / r.trials).toFixed(4) : null,
    z: z(r.hits, r.trials, TESTS[r.test]?.chance || 0.2),
  }));
  const sum = (f) => {
    const out = {};
    for (const r of rows) {
      const k = f(r), c = TESTS[r.test].chance;
      out[k] ??= { trials: 0, hits: 0, expected: 0, runs: 0 };
      out[k].trials += r.trials; out[k].hits += r.hits; out[k].expected += r.trials * c; out[k].runs += r.runs;
    }
    for (const k in out) {
      const o = out[k], v = rows.filter((r) => f(r) === k).reduce((a, r) => a + r.trials * TESTS[r.test].chance * (1 - TESTS[r.test].chance), 0);
      o.expected = +o.expected.toFixed(1);
      o.z = v ? +((o.hits - o.expected) / Math.sqrt(v)).toFixed(2) : 0;
    }
    return out;
  };
  return json({
    by_test: sum((r) => r.test), by_player: sum((r) => r.player), by_belief: sum((r) => r.belief),
    all: sum(() => "all").all || { trials: 0, hits: 0, expected: 0, runs: 0, z: 0 },
    rows, positions: p.results,
    note: "z is (hits − expected) ÷ standard deviation under chance. Between −2 and 2 is what chance gives about 95 times in 100.",
  });
}

// ---------------------------------------------------------------- forecast

const DAY_MS = 86400000;
const drawTime = (day) => Date.parse(day + "T12:00:00Z");
const closeTime = (day) => drawTime(day) - 3600000;
const roundFor = (ms) => Math.ceil((ms / 1000 - GENESIS) / PERIOD) + 1;
const isoDay = (ms) => new Date(ms).toISOString().slice(0, 10);
function openDay(now = Date.now()) {
  const today = isoDay(now);
  return now < closeTime(today) ? today : isoDay(now + DAY_MS);
}

async function targetFrom(randomness) {
  const out = [];
  for (let i = 0; out.length < 25; i++) {
    const h = new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(randomness + ":" + i)));
    if (h[0] < 250) out.push(h[0] % 5);
  }
  return out.join("");
}

async function draw(env, day) {
  const got = await env.DB.prepare("SELECT * FROM draws WHERE day = ?").bind(day).first();
  if (got) return got;
  if (Date.now() < drawTime(day) + 5000) return null;
  const round = roundFor(drawTime(day));
  const r = await fetch(`https://api.drand.sh/${CHAIN}/public/${round}`);
  if (!r.ok) return null;
  const { randomness } = await r.json();
  if (!/^[0-9a-f]{64}$/.test(randomness || "")) return null;
  const target = await targetFrom(randomness);
  await env.DB.prepare("INSERT OR IGNORE INTO draws (day, round, randomness, target) VALUES (?,?,?,?)")
    .bind(day, round, randomness, target).run();
  return { day, round, randomness, target };
}

const score = (calls, target) => [...calls].reduce((a, c, i) => a + (c === target[i] ? 1 : 0), 0);

async function forecastDay(env, day) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(day)) return bad("day is YYYY-MM-DD");
  const d = await draw(env, day);
  const e = await env.DB.prepare("SELECT name, player, belief, calls, created FROM forecast WHERE day = ? ORDER BY created").bind(day).all();
  const entries = e.results.map((x) => ({
    name: x.name, player: x.player, belief: x.belief, at: new Date(x.created).toISOString(),
    calls: [...x.calls].map((c) => SYM[+c]),
    ...(d ? { hits: score(x.calls, d.target), z: z(score(x.calls, d.target), 25, 0.2) } : {}),
  }));
  if (d) entries.sort((a, b) => b.hits - a.hits);
  return json({
    day, closes: new Date(closeTime(day)).toISOString(), draws: new Date(drawTime(day)).toISOString(),
    drand: { chain: CHAIN, round: roundFor(drawTime(day)), url: `https://api.drand.sh/${CHAIN}/public/${roundFor(drawTime(day))}` },
    target: d ? [...d.target].map((c) => SYM[+c]) : null, randomness: d?.randomness || null, entries,
  });
}

async function forecastIndex(env) {
  const now = Date.now(), open = openDay(now);
  const past = [];
  for (let k = 0; k <= 7; k++) {
    const day = isoDay(now - k * DAY_MS);
    if (drawTime(day) < now) past.push(day);
  }
  await Promise.all(past.map((d) => draw(env, d)));
  const [cnt, rows, recent] = await Promise.all([
    env.DB.prepare("SELECT COUNT(*) AS n FROM forecast WHERE day = ?").bind(open).first(),
    env.DB.prepare("SELECT f.name, f.player, f.calls, d.target FROM forecast f JOIN draws d ON d.day = f.day").all(),
    env.DB.prepare("SELECT d.day, d.target, COUNT(f.name) AS entries FROM draws d LEFT JOIN forecast f ON f.day = d.day " +
      "GROUP BY d.day ORDER BY d.day DESC LIMIT 10").all(),
  ]);
  const by = {};
  for (const r of rows.results) {
    const k = r.name;
    by[k] ??= { name: r.name, player: r.player, draws: 0, hits: 0 };
    by[k].draws++; by[k].hits += score(r.calls, r.target);
  }
  const board = Object.values(by).map((b) => ({ ...b, trials: b.draws * 25, z: z(b.hits, b.draws * 25, 0.2) }))
    .sort((a, b) => b.z - a.z).slice(0, 50);
  return json({
    open: { day: open, closes: new Date(closeTime(open)).toISOString(), draws: new Date(drawTime(open)).toISOString(),
      round: roundFor(drawTime(open)), entries: cnt?.n || 0 },
    recent: recent.results.map((r) => ({ day: r.day, entries: r.entries, target: [...r.target].map((c) => SYM[+c]) })),
    leaderboard: board,
    rule: "target = 25 symbols from drand quicknet, first round at or after 12:00 UTC; entries close 11:00 UTC. " +
      "For i = 0,1,2…: b = SHA-256(randomness_hex + ':' + i)[0]; keep b % 5 when b < 250. Symbols 0–4: " + SYM.join(", "),
  });
}

async function enter(env, b) {
  const now = Date.now();
  const day = b.day && /^\d{4}-\d{2}-\d{2}$/.test(b.day) ? b.day : openDay(now);
  if (now >= closeTime(day)) return bad("entries for " + day + " closed at " + new Date(closeTime(day)).toISOString(), 409);
  if (drawTime(day) - now > 8 * DAY_MS) return bad("enter up to a week ahead");
  const raw = Array.isArray(b.calls) ? b.calls : typeof b.calls === "string" ? b.calls.split(/[\s,]+/).filter(Boolean) : [];
  const calls = raw.map(symbol);
  if (calls.length !== 25 || calls.some((c) => c === null)) return bad("calls: 25 symbols, each one of " + SYM.join(", "));
  const player = PLAYERS.includes(b.player) ? b.player : "human";
  const belief = BELIEFS.includes(b.belief) ? b.belief : "unsure";
  const name = cleanName(b.name) || (player === "robot" ? "robot-" : "anon-") + hex(2);
  try {
    await env.DB.prepare("INSERT INTO forecast (day, name, player, belief, calls, created) VALUES (?,?,?,?,?,?)")
      .bind(day, name, player, belief, calls.join(""), now).run();
  } catch {
    return bad(name + " already has a forecast for " + day, 409);
  }
  return json({ ok: true, day, name, closes: new Date(closeTime(day)).toISOString(),
    draws: new Date(drawTime(day)).toISOString(), round: roundFor(drawTime(day)), see: "/forecast/" + day }, 201);
}

// ---------------------------------------------------------------- routes

const HELP = {
  what: "The Rhine Deck lab: Duke-style ESP tests anyone can take, people or robots. The server deals and checks every card.",
  site: SITE,
  symbols: SYM,
  tests: {
    clairvoyance: "closed deck of 25, five of each symbol, shuffled when the session opens; call each card before it turns",
    precognition: "25 calls; each target is drawn after your call arrives",
    dice: "24 throws; call the face you want, 1–6, then the server throws",
  },
  start: "POST /session {\"test\":\"clairvoyance\",\"player\":\"robot\",\"belief\":\"sheep|goat|unsure\",\"name\":\"optional\"}",
  call: "POST /session/<id>/call {\"call\":\"star\"}",
  stats: "GET /stats",
  forecast: "POST /forecast {\"name\":\"...\",\"player\":\"robot\",\"calls\":[25 symbols]} before 11:00 UTC; drawn from drand at 12:00 UTC",
  leaderboard: "GET /forecast",
  belief: "sheep = thinks ESP can happen; goat = thinks it cannot (Gertrude Schmeidler's terms, 1940s)",
};

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const path = url.pathname.replace(/\/+$/, "") || "/";
    if (req.method === "OPTIONS") return new Response(null, { headers: CORS });
    try {
      if (req.method === "GET" && path === "/") return json(HELP);
      if (req.method === "GET" && path === "/stats") return await stats(env);
      if (req.method === "POST" && path === "/session") return await newSession(env, await body(req));
      let m = path.match(/^\/session\/([0-9a-f]{24})(\/call)?$/);
      if (m && req.method === "GET" && !m[2]) {
        const s = await getSession(env, m[1]);
        return s ? json(view(s)) : bad("no such session", 404);
      }
      if (m && req.method === "POST" && m[2]) return await call(env, m[1], await body(req));
      if (req.method === "GET" && path === "/forecast") return await forecastIndex(env);
      if (req.method === "POST" && path === "/forecast") return await enter(env, await body(req));
      m = path.match(/^\/forecast\/(\d{4}-\d{2}-\d{2})$/);
      if (m && req.method === "GET") return await forecastDay(env, m[1]);
      return bad("not found", 404);
    } catch (e) {
      return bad(String(e.message || e), 400);
    }
  },
};
