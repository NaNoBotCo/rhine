(function(){var th=document.documentElement.lang==='th';
if(th){window.RHINE_L={circle:"วงกลม",cross:"บวก",waves:"คลื่น",square:"สี่เหลี่ยม",star:"ดาว",
intro:{"clairvoyance": "เซิร์ฟเวอร์สับไพ่ 25 ใบ สัญลักษณ์ละ 5 ใบ แล้วคว่ำไว้ ทายทีละใบก่อนเปิด นี่คือการทดสอบตาทิพย์พื้นฐานของไรน์ช่วงต้นทศวรรษ 1930 กดปุ่ม 1–5 ก็ได้", "precognition": "ทายก่อน แล้วเซิร์ฟเวอร์จึงสุ่มไพ่เป้าหมาย ตอนที่ทาย ยังไม่มีไพ่ให้แอบดู ห้องแล็บของไรน์ประกาศผลเรื่องรู้ล่วงหน้าในปี 1938", "dice": "เลือกหน้าที่อยากให้ออก แล้วเซิร์ฟเวอร์ทอยลูกเต๋าหนึ่งลูก 24 ครั้ง โอกาส 1 ใน 6 ก็คือถูก 4 ครั้ง ไรน์เริ่มทดสอบลูกเต๋าในปี 1934"},
card:function(n,t,test){return (test==="dice"?"ทอยที่ ":"ใบที่ ")+n+" จาก "+t},
done:"จบรอบ",dealing:"กำลังสับ…",counted:"เซิร์ฟเวอร์ถือไพ่เป้าหมายไว้ รอบนี้นับรวมในสถิติ",
offline:"ติดต่อเซิร์ฟเวอร์ไม่ได้ รอบนี้เล่นในเบราว์เซอร์และไม่นับรวม",err:"มีปัญหา:",
hits:function(h,n){return "ถูก "+h+" จาก "+n},
chance:function(h,n,e,pct,z){return "ถ้าเดาล้วน ๆ จะถูกเฉลี่ย "+e+" ครั้ง คะแนน "+h+" หรือสูงกว่า เกิดจากโชคได้ราว "+pct+"% ของรอบ (z = "+z+") ห้องแล็บของไรน์มองหาคะแนนที่เกิน 2 ไปไกล ๆ ในหลาย ๆ รอบ"},
bellAlt:"โอกาสที่โชคล้วน ๆ ให้แต่ละคะแนน พร้อมคะแนนของคุณ",
bellCap:function(n,t){return "แท่ง: โอกาสที่เดาล้วน ๆ จะได้แต่ละคะแนนใน "+n+(t==="dice"?" ทอย":" คำทาย")+" แท่งสีน้ำเงินคือของคุณ"},
youTitle:"คำทายบอกอะไรเกี่ยวกับคุณ",repLabel:"ทายซ้ำตัวเดิมติดกัน",
rep:function(r){return r+" ครั้ง ถ้าสุ่มจริงจะซ้ำราว 5 ครั้งใน 25 คนส่วนใหญ่ซ้ำน้อยกว่านั้น เพราะรู้สึกว่าซ้ำแล้วไม่สุ่ม"},
useLabel:"สัญลักษณ์ที่คุณทาย",use:function(s,c){return "ทายบ่อยสุด: "+s+" "+c+" ครั้ง ในสำรับมีอย่างละ 5 ใบ"},
halfLabel:"ครึ่งแรก ครึ่งหลัง",half:function(a,b){return "ถูก "+a+" ครั้งในใบที่ 1–12 และ "+b+" ครั้งในใบที่ 14–25 ห้องแล็บของไรน์รายงานว่าคะแนนตกลงเมื่อรอบยืดออกไป"},
notCounted:"เล่นในเบราว์เซอร์ ไม่นับรวม",countedDone:"นับแล้ว สถิติรวมด้านล่างรวมรอบนี้ด้วย",
rowName:{all:"ทุกคน",clairvoyance:"ไพ่",precognition:"ทายก่อนสับ",dice:"ลูกเต๋า",human:"คน",robot:"หุ่นยนต์",sheep:"ตอบว่ามี",goat:"ตอบว่าไม่มี",unsure:"ไม่แน่ใจ"},
cols:["รอบ","คำทาย","ถูก","อัตราถูก","โอกาส","z"],
posAlt:"อัตราทายถูกตามลำดับในรอบ 25 ใบ เทียบเส้นโอกาส 20%",
mine:function(t,h,e){return "รอบของคุณบนเครื่องนี้: ถูก "+h+" จาก "+t+" คำทาย เดาล้วน ๆ ได้ "+e},
sending:"กำลังส่ง…",entered:function(n,w){return "รับแล้ว ในชื่อ <b>"+n+"</b> ออกผล "+w},
open:function(w,c,n,r){return "ออกผลครั้งถัดไป: "+w+" (เวลาของคุณ) จาก drand รอบ "+r+" ปิดรับ "+c+" ส่งมาแล้ว "+n+" คำทาย"},
entries:function(n){return n+" คำทาย"},noneYet:"ยังไม่มีผล",
boardCols:["ชื่อ","ประเภท","ครั้ง","ถูก","z"],boardEmpty:"ว่างอยู่จนกว่าจะออกผลครั้งแรกที่มีคนส่ง"};}else{window.RHINE_L={circle:"circle",cross:"cross",waves:"waves",square:"square",star:"star",
intro:{"clairvoyance": "The server shuffles a closed deck of 25, five of each symbol, and keeps it hidden. Call each card before it turns. This is Rhine's basic clairvoyance test from the early 1930s. Keys 1\u20135 work too.", "precognition": "Call a symbol. Only then does the server draw the target. Nothing exists to peek at when you call. Rhine's lab announced precognition results in 1938.", "dice": "Pick the face you want. The server throws one die. 24 throws; chance is 1 in 6, so 4 hits. Rhine started dice tests in 1934."},
card:function(n,t,test){return (test==="dice"?"Throw ":"Card ")+n+" of "+t},
done:"Run done",dealing:"Shuffling…",counted:"The server holds the targets. This run counts toward the tallies.",
offline:"Server not reached: this run plays in your browser and does not count.",err:"Something went wrong:",
hits:function(h,n){return h+" of "+n},
chance:function(h,n,e,pct,z){return "Chance alone gives "+e+" on average. A score of "+h+" or better turns up in about "+pct+"% of runs by luck (z = "+z+"). Rhine's lab looked for scores well past 2 on that scale, across many runs."},
bellAlt:"How often luck gives each score, with yours marked",
bellCap:function(n,t){return "Bars: how often luck alone gives each score in "+n+(t==="dice"?" throws.":" calls.")+" Yours is blue."},
youTitle:"What your calls say about you",repLabel:"Same symbol twice in a row",
rep:function(r){return r+" times. A random caller does it about 5 times in 25; most people do it less, because repeats don't feel random."},
useLabel:"Symbols you called",use:function(s,c){return "Most called: "+s+", "+c+" times. The deck holds 5 of each."},
halfLabel:"First half, second half",half:function(a,b){return a+" hits in cards 1–12, "+b+" in 14–25. Rhine's lab reported scores dropping as a run wore on."},
notCounted:"Played in your browser; not counted.",countedDone:"Counted. The pooled tallies below include this run.",
rowName:{all:"Everyone",clairvoyance:"Cards",precognition:"Before the shuffle",dice:"Dice",human:"People",robot:"Robots",sheep:"Say yes to ESP",goat:"Say no",unsure:"Not sure"},
cols:["Runs","Calls","Hits","Hit rate","Chance","z"],
posAlt:"Hit rate at each place in the run of 25, against the 20% chance line",
mine:function(t,h,e){return "Your runs on this device: "+h+" hits in "+t+" calls; chance gives "+e+"."},
sending:"Sending…",entered:function(n,w){return "In, as <b>"+n+"</b>. Drawn "+w+"."},
open:function(w,c,n,r){return "Next draw: "+w+" (your time), from drand round "+r+". Entries close "+c+". "+n+" in so far."},
entries:function(n){return n+" forecast"+(n===1?"":"s")},noneYet:"No draws yet.",
boardCols:["Name","Kind","Draws","Hits","z"],boardEmpty:"Empty until the first draw with entries."};}})();
/* The lab: three of Rhine's tests played against rhine-lab.nanobotco.workers.dev,
   which deals and checks every card; the pooled tallies; the daily forecast.
   If the server cannot be reached the tests run here in the browser and the
   run is marked as not counted. Strings come from window.RHINE_L. */
(function () {
  var API = "https://rhine-lab.nanobotco.workers.dev";
  var L = window.RHINE_L || {};
  var SYM = ["circle", "cross", "waves", "square", "star"];
  var TESTS = {
    clairvoyance: { trials: 25, faces: 5, p: 0.2 },
    precognition: { trials: 25, faces: 5, p: 0.2 },
    dice: { trials: 24, faces: 6, p: 1 / 6 }
  };
  var LOC = document.documentElement.lang === "th" ? "th-TH" : undefined;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var store = {
    get: function (k) { try { return localStorage.getItem("rhine." + k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem("rhine." + k, v); } catch (e) {} }
  };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function post(path, body) {
    return fetch(API + path, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().then(function (j) { if (!r.ok) throw j; return j; }); });
  }
  function get(path) { return fetch(API + path).then(function (r) { return r.json(); }); }

  function svg(s, k) {
    var d;
    if (s === "circle") d = '<circle cx="32" cy="32" r="20"/>';
    else if (s === "cross") d = '<path d="M32 10v44M10 32h44"/>';
    else if (s === "waves") d = '<path d="M8 20q6-7 12 0t12 0 12 0 12 0M8 32q6-7 12 0t12 0 12 0 12 0M8 44q6-7 12 0t12 0 12 0 12 0"/>';
    else if (s === "square") d = '<rect x="13" y="13" width="38" height="38"/>';
    else d = '<path d="M32 8l6.5 16.2 17.4 1-13.4 11.1 4.4 16.9L32 44l-14.9 9.2 4.4-16.9L8.1 25.2l17.4-1z"/>';
    return '<svg viewBox="0 0 64 64" width="' + k + '" height="' + k + '" aria-hidden="true" class="sym">' + d + "</svg>";
  }
  var PIPS = { 1: [[32, 32]], 2: [[18, 18], [46, 46]], 3: [[18, 18], [32, 32], [46, 46]],
    4: [[18, 18], [46, 18], [18, 46], [46, 46]], 5: [[18, 18], [46, 18], [32, 32], [18, 46], [46, 46]],
    6: [[18, 16], [46, 16], [18, 32], [46, 32], [18, 48], [46, 48]] };
  function die(n, k) {
    return '<svg viewBox="0 0 64 64" width="' + k + '" height="' + k + '" aria-hidden="true" class="die"><rect x="5" y="5" width="54" height="54" rx="10"/>' +
      PIPS[n].map(function (p) { return '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="5.5"/>'; }).join("") + "</svg>";
  }
  function show(test, v, k) { return test === "dice" ? die(+v, k) : svg(v, k); }
  function label(test, v) { return test === "dice" ? String(v) : (L[v] || v); }

  function binom(n, k, p) {
    var c = 1, i;
    for (i = 0; i < k; i++) c = c * (n - i) / (i + 1);
    return c * Math.pow(p, k) * Math.pow(1 - p, n - k);
  }
  function bell(n, p, hits) {
    var top = Math.min(n, Math.ceil(n * p * 3) + 1), W = 520, H = 170, bw = W / (top + 1), max = 0, i, bars = "";
    for (i = 0; i <= top; i++) max = Math.max(max, binom(n, i, p));
    for (i = 0; i <= top; i++) {
      var h = binom(n, i, p) / max * (H - 34);
      bars += '<rect x="' + (i * bw + 2).toFixed(1) + '" y="' + (H - 20 - h).toFixed(1) + '" width="' + (bw - 4).toFixed(1) +
        '" height="' + h.toFixed(1) + '" class="' + (i === hits ? "you" : "bar") + '"/>' +
        '<text x="' + (i * bw + bw / 2).toFixed(1) + '" y="' + (H - 5) + '" class="ax">' + i + "</text>";
    }
    return '<svg viewBox="0 0 ' + W + " " + H + '" class="bell" role="img" aria-label="' + esc(L.bellAlt || "") + '">' + bars + "</svg>";
  }

  /* ------------------------------------------------------------ who's playing */
  var who = { player: store.get("player") || "human", belief: store.get("belief") || "", name: store.get("name") || "" };
  function pick(group, key) {
    var g = $(group); if (!g) return;
    g.querySelectorAll("button").forEach(function (b) {
      b.setAttribute("aria-pressed", b.dataset.v === who[key] ? "true" : "false");
      b.addEventListener("click", function () {
        who[key] = b.dataset.v; store.set(key, b.dataset.v);
        g.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        if (key === "player") $("#robot-door").hidden = who.player !== "robot";
      });
    });
  }
  pick("#who-player", "player"); pick("#who-belief", "belief");
  if ($("#robot-door")) $("#robot-door").hidden = who.player !== "robot";
  var nameIn = $("#who-name");
  if (nameIn) { nameIn.value = who.name; nameIn.addEventListener("change", function () { who.name = nameIn.value.trim().slice(0, 32); store.set("name", who.name); }); }

  /* ------------------------------------------------------------ the tests */
  var box = $("#tests");
  if (box) (function () {
    var test = "clairvoyance", run = null;
    var face = $(".face", box), count = $(".count", box), tally = $(".tally", box), out = $(".out", box),
      btns = $(".calls", box), status = $(".status", box), intro = $(".intro", box);

    box.querySelectorAll(".tabs button").forEach(function (b) {
      b.addEventListener("click", function () {
        test = b.dataset.test;
        box.querySelectorAll(".tabs button").forEach(function (x) { x.setAttribute("aria-selected", x === b ? "true" : "false"); });
        start();
      });
    });
    $(".again", box).addEventListener("click", start);
    document.addEventListener("keydown", function (e) {
      if (!run || run.n >= run.trials || run.busy || e.metaKey || e.ctrlKey || /INPUT|TEXTAREA|SELECT/.test(e.target.tagName)) return;
      var k = "123456".indexOf(e.key);
      if (k >= 0 && k < TESTS[test].faces) call(k);
    });

    function buttons() {
      btns.innerHTML = "";
      var n = TESTS[test].faces, i;
      btns.style.gridTemplateColumns = "repeat(" + n + ",1fr)";
      for (i = 0; i < n; i++) (function (i) {
        var v = test === "dice" ? i + 1 : SYM[i], b = document.createElement("button");
        b.type = "button"; b.className = "call";
        b.setAttribute("aria-label", label(test, v));
        b.innerHTML = show(test, v, 40) + (test === "dice" ? "" : "<span>" + esc(label(test, v)) + "</span>");
        b.addEventListener("click", function () { call(i); });
        btns.appendChild(b);
      })(i);
    }

    function start() {
      var T = TESTS[test];
      run = { test: test, trials: T.trials, n: 0, hits: 0, calls: [], targets: [], id: null, local: false, busy: false };
      intro.innerHTML = (L.intro && L.intro[test]) || "";
      face.innerHTML = test === "dice" ? '<div class="back dice">?</div>' : '<div class="back">?</div>';
      tally.innerHTML = ""; out.hidden = true; out.innerHTML = ""; btns.hidden = false; buttons();
      count.textContent = L.card(1, T.trials, test);
      status.textContent = "";
    }

    /* the session opens on the first call, so a visit without play leaves no run behind */
    function open(mine) {
      status.textContent = L.dealing || "";
      return post("/session", { test: test, player: who.player, belief: who.belief || "unsure", name: who.name || undefined })
        .then(function (j) { if (mine !== run) return; run.id = j.id; status.textContent = L.counted || ""; })
        .catch(function () { if (mine !== run) return; run.local = true; run.deck = localDeck(test); status.textContent = L.offline || ""; });
    }

    function localDeck(t) {
      var a = [], i, j, x, r = new Uint32Array(25);
      (window.crypto || window.msCrypto).getRandomValues(r);
      if (t !== "clairvoyance") return null;
      for (i = 0; i < 25; i++) a.push(i % 5);
      for (i = 24; i > 0; i--) { j = r[i] % (i + 1); x = a[i]; a[i] = a[j]; a[j] = x; }
      return a;
    }
    function localDraw(n) { var b = new Uint8Array(1), lim = 256 - 256 % n; for (;;) { crypto.getRandomValues(b); if (b[0] < lim) return b[0] % n; } }

    function call(i) {
      if (!run || run.busy || run.n >= run.trials) return;
      if (!run.id && !run.local) {
        var first = run; run.busy = true; btns.classList.add("busy");
        open(first).then(function () { if (first !== run) return; run.busy = false; btns.classList.remove("busy"); call(i); });
        return;
      }
      var mine = run, v = test === "dice" ? i + 1 : SYM[i];
      run.busy = true; btns.classList.add("busy");
      var p = run.local
        ? Promise.resolve((function () {
          var t = run.deck ? run.deck[run.n] : localDraw(TESTS[test].faces);
          return { target: test === "dice" ? t + 1 : SYM[t], hit: t === i };
        })())
        : post("/session/" + run.id + "/call", { call: v });
      p.then(function (j) {
        if (mine !== run) return;
        run.busy = false; btns.classList.remove("busy");
        run.calls.push(v); run.targets.push(j.target); run.n++; if (j.hit) run.hits++;
        face.innerHTML = '<div class="front ' + (j.hit ? "hit" : "miss") + '">' + show(test, j.target, test === "dice" ? 88 : 96) + "</div>";
        var dot = document.createElement("i");
        dot.className = j.hit ? "h" : "m";
        dot.title = label(test, v) + " → " + label(test, j.target);
        tally.appendChild(dot);
        if (run.n < run.trials) count.textContent = L.card(run.n + 1, run.trials, test);
        else finish();
      }).catch(function (e) {
        if (mine !== run) return;
        run.busy = false; btns.classList.remove("busy");
        status.textContent = (L.err || "") + " " + ((e && e.error) || "");
      });
    }

    function finish() {
      var T = TESTS[test], n = run.trials, hits = run.hits, i, tail = 0;
      btns.hidden = true;
      count.textContent = L.done || "";
      for (i = hits; i <= n; i++) tail += binom(n, i, T.p);
      var zz = (hits - n * T.p) / Math.sqrt(n * T.p * (1 - T.p));
      var html = '<p class="big">' + L.hits(hits, n) + "</p><p>" +
        L.chance(hits, n, +(n * T.p).toFixed(1), (tail * 100).toFixed(tail < 0.01 ? 2 : 0), zz.toFixed(1)) + "</p>" +
        bell(n, T.p, hits) + '<p class="cap">' + esc(L.bellCap(n, test)) + "</p>";
      if (test !== "dice") {
        var reps = 0, used = {};
        for (i = 0; i < n; i++) { if (i && run.calls[i] === run.calls[i - 1]) reps++; used[run.calls[i]] = (used[run.calls[i]] || 0) + 1; }
        var most = SYM.reduce(function (a, s) { return (used[s] || 0) > (used[a] || 0) ? s : a; }, SYM[0]);
        html += "<h3>" + esc(L.youTitle) + '</h3><dl class="you-dl"><dt>' + esc(L.repLabel) + "</dt><dd>" + L.rep(reps) + "</dd>" +
          "<dt>" + esc(L.useLabel) + "</dt><dd>" + SYM.map(function (s) { return '<span class="u">' + svg(s, 20) + (used[s] || 0) + "</span>"; }).join(" ") +
          "<br>" + L.use(L[most] || most, used[most] || 0) + "</dd>";
        var h1 = 0, h2 = 0;
        for (i = 0; i < n; i++) { if (run.calls[i] === run.targets[i]) { if (i < 12) h1++; else if (i > 12) h2++; } }
        html += "<dt>" + esc(L.halfLabel) + "</dt><dd>" + L.half(h1, h2) + "</dd></dl>";
      }
      html += '<p class="small">' + (run.local ? L.notCounted : L.countedDone) + "</p>";
      out.innerHTML = html; out.hidden = false;
      var mine = JSON.parse(store.get("mine") || "{}");
      mine[test] = mine[test] || { runs: 0, trials: 0, hits: 0 };
      mine[test].runs++; mine[test].trials += n; mine[test].hits += hits;
      store.set("mine", JSON.stringify(mine));
      loadStats();
    }

    start();
  })();

  /* ------------------------------------------------------------ pooled tallies */
  function zc(zv) { return Math.abs(zv) >= 2 ? "z hot" : "z"; }
  function loadStats() {
    var el = $("#pool"); if (!el) return;
    get("/stats").then(function (s) {
      function row(k, o) {
        if (!o) return "";
        var rate = o.trials ? (o.hits / o.trials * 100).toFixed(1) + "%" : "–";
        var exp = o.trials ? (o.expected / o.trials * 100).toFixed(1) + "%" : "–";
        return "<tr><th>" + esc(L.rowName[k] || k) + "</th><td>" + o.runs + "</td><td>" + o.trials + "</td><td>" + o.hits + "</td><td>" + rate +
          "</td><td>" + exp + '</td><td class="' + zc(o.z) + '">' + (o.trials ? o.z.toFixed(2) : "–") + "</td></tr>";
      }
      var head = "<tr><th></th><th>" + L.cols.join("</th><th>") + "</th></tr>";
      var body = row("all", s.all) +
        '<tr class="sep"><td colspan="7"></td></tr>' + ["clairvoyance", "precognition", "dice"].map(function (k) { return row(k, s.by_test[k]); }).join("") +
        '<tr class="sep"><td colspan="7"></td></tr>' + ["human", "robot"].map(function (k) { return row(k, s.by_player[k]); }).join("") +
        '<tr class="sep"><td colspan="7"></td></tr>' + ["sheep", "goat", "unsure"].map(function (k) { return row(k, s.by_belief[k]); }).join("");
      $("table", el).innerHTML = "<thead>" + head + "</thead><tbody>" + body + "</tbody>";
      /* hits by position in the run: Rhine's decline effect */
      var pos = {}, i;
      (s.positions || []).forEach(function (p) {
        if (p.test === "dice") return;
        pos[p.pos] = pos[p.pos] || { t: 0, h: 0 }; pos[p.pos].t += p.trials; pos[p.pos].h += p.hits;
      });
      var W = 520, H = 160, bw = W / 25, bars = "", y20 = H - 20 - 0.2 / 0.4 * (H - 34);
      for (i = 1; i <= 25; i++) {
        var q = pos[i], r = q && q.t ? q.h / q.t : 0, h = Math.min(r, 0.4) / 0.4 * (H - 34);
        bars += '<rect x="' + ((i - 1) * bw + 2).toFixed(1) + '" y="' + (H - 20 - h).toFixed(1) + '" width="' + (bw - 4).toFixed(1) + '" height="' + h.toFixed(1) + '" class="bar"><title>' +
          i + ": " + (q ? q.h + "/" + q.t : "0") + "</title></rect>" + (i === 1 || i % 5 === 0 ? '<text x="' + ((i - 1) * bw + bw / 2).toFixed(1) + '" y="' + (H - 5) + '" class="ax">' + i + "</text>" : "");
      }
      bars += '<line x1="0" x2="' + W + '" y1="' + y20.toFixed(1) + '" y2="' + y20.toFixed(1) + '" class="chance"/><text x="' + (W - 4) + '" y="' + (y20 - 5).toFixed(1) + '" class="ax end">20%</text>';
      $(".pos", el).innerHTML = '<svg viewBox="0 0 ' + W + " " + H + '" class="bell" role="img" aria-label="' + esc(L.posAlt) + '">' + bars + "</svg>";
      var mine = JSON.parse(store.get("mine") || "{}"), t = 0, h = 0, e = 0;
      Object.keys(mine).forEach(function (k) { t += mine[k].trials; h += mine[k].hits; e += mine[k].trials * TESTS[k].p; });
      $(".mine", el).innerHTML = t ? L.mine(t, h, e.toFixed(1)) : "";
    }).catch(function () { $(".pos", el).textContent = L.offline || ""; });
  }
  loadStats();

  /* ------------------------------------------------------------ the forecast */
  var fc = $("#fc");
  if (fc) (function () {
    var slots = [], grid = $(".slots", fc), pad = $(".pad", fc), msg = $(".msg", fc);
    function draw() {
      var i, h = "";
      for (i = 0; i < 25; i++) h += '<button type="button" class="slot' + (i === slots.length ? " next" : "") + '" data-i="' + i + '" aria-label="' + (i + 1) + '">' +
        (slots[i] ? svg(slots[i], 26) : "<span>" + (i + 1) + "</span>") + "</button>";
      grid.innerHTML = h;
      grid.querySelectorAll(".slot").forEach(function (b) {
        b.addEventListener("click", function () { var k = +b.dataset.i; if (k < slots.length) { slots = slots.slice(0, k); draw(); } });
      });
      $(".send", fc).disabled = slots.length !== 25;
    }
    SYM.forEach(function (s) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "call"; b.setAttribute("aria-label", L[s] || s);
      b.innerHTML = svg(s, 32) + "<span>" + esc(L[s] || s) + "</span>";
      b.addEventListener("click", function () { if (slots.length < 25) { slots.push(s); draw(); } });
      pad.appendChild(b);
    });
    $(".clear", fc).addEventListener("click", function () { slots = []; draw(); });
    $(".send", fc).addEventListener("click", function () {
      msg.textContent = L.sending || "";
      post("/forecast", { name: who.name || undefined, player: who.player, belief: who.belief || "unsure", calls: slots })
        .then(function (j) {
          msg.innerHTML = L.entered(esc(j.name), new Date(j.draws).toLocaleString(LOC));
          if (!who.name) { who.name = j.name; store.set("name", j.name); if (nameIn) nameIn.value = j.name; }
          slots = []; draw(); loadForecast();
        })
        .catch(function (e) { msg.textContent = (e && e.error) || L.err; });
    });
    draw();

    function loadForecast() {
      get("/forecast").then(function (f) {
        var o = f.open, when = new Date(o.draws), close = new Date(o.closes);
        $(".open", fc).innerHTML = L.open(when.toLocaleString(LOC), close.toLocaleString(LOC), o.entries, o.round);
        $(".recent", fc).innerHTML = (f.recent || []).map(function (r) {
          return '<li><a href="' + API + "/forecast/" + r.day + '">' + r.day + "</a> " + r.target.map(function (s) { return svg(s, 14); }).join("") +
            ' <span class="small">' + L.entries(r.entries) + "</span></li>";
        }).join("") || "<li>" + esc(L.noneYet) + "</li>";
        var b = f.leaderboard || [];
        $(".board", fc).classList.toggle("empty", !b.length);
        $(".board", fc).innerHTML = b.length ? "<thead><tr><th>" + L.boardCols.join("</th><th>") + "</th></tr></thead><tbody>" +
          b.map(function (r) {
            return "<tr><th>" + esc(r.name) + "</th><td>" + esc(L.rowName[r.player] || r.player) + "</td><td>" + r.draws + "</td><td>" + r.hits + "/" + r.trials +
              '</td><td class="' + zc(r.z) + '">' + r.z.toFixed(2) + "</td></tr>";
          }).join("") + "</tbody>" : "<tbody><tr><td>" + esc(L.boardEmpty) + "</td></tr></tbody>";
      }).catch(function () { $(".open", fc).textContent = L.offline || ""; });
    }
    loadForecast();
  })();
})();
