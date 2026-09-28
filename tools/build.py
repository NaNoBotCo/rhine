#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build.py — docs/index.html (English), docs/th/index.html (Thai), lab.js, and the machine files.

    python3 tools/build.py && python3 tools/card.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fleet  # noqa: E402
from shell import BASE, E, FLEET, ROOT, SELF, SITE_URL, TODAY, foot, head  # noqa: E402

DOCS = ROOT / "docs"
API = "https://rhine-lab.nanobotco.workers.dev"

SRC = [
    ("ncpedia", "NCpedia — Rhine, Joseph Banks", "https://www.ncpedia.org/biography/rhine-joseph-banks"),
    ("rrc-nc", "NCpedia — Rhine Research Center", "https://www.ncpedia.org/rhine-research-center"),
    ("psi", "Psi Encyclopedia (Society for Psychical Research) — J.B. Rhine", "https://psi-encyclopedia.spr.ac.uk/articles/jb-rhine/"),
    ("rrc", "Rhine Research Center — About us", "https://www.rhineonline.org/about-us"),
    ("zener", "Wikipedia — Zener cards", "https://en.wikipedia.org/wiki/Zener_cards"),
    ("pratt", "Wikipedia — Joseph Gaither Pratt", "https://en.wikipedia.org/wiki/Joseph_Gaither_Pratt"),
    ("esp-book", "Wikipedia — Extra-Sensory Perception (book)", "https://en.wikipedia.org/wiki/Extrasensory_Perception_(book)"),
    ("jbr", "Wikipedia — Joseph Banks Rhine", "https://en.wikipedia.org/wiki/Joseph_Banks_Rhine"),
    ("pk", "Psi Encyclopedia — Psychokinesis research", "https://psi-encyclopedia.spr.ac.uk/articles/psychokinesis-research/"),
    ("decline", "Wikipedia — Decline effect", "https://en.wikipedia.org/wiki/Decline_effect"),
    ("sheep", "Wikipedia — Sheep–goat effect", "https://en.wikipedia.org/wiki/Sheep%E2%80%93goat_effect"),
    ("levy", "Time, 26 Aug 1974 — Parapsychology: Fraud in the lab", "https://content.time.com/time/subscriber/article/0,33009,944971,00.html"),
    ("fraud", "J.E. Kennedy — the Levy case", "https://jeksite.org/psi/fraud.htm"),
    ("paralab", "Duke Rubenstein Library — Parapsychology Laboratory records, 1893–1984", "https://archives.lib.duke.edu/catalog/paralab"),
    ("letters", "Duke exhibit — Laboratory letters", "https://exhibits.library.duke.edu/exhibits/show/parapsychology/laboratory-letters"),
    ("exhibit", "Duke exhibit — Early Studies in Parapsychology at Duke", "https://exhibits.library.duke.edu/exhibits/show/parapsychology/about-the-exhibit"),
    ("louisa", "Wikipedia — Louisa E. Rhine", "https://en.wikipedia.org/wiki/Louisa_E._Rhine"),
    ("jop", "Internet Archive — Journal of Parapsychology, 1937 onward", "https://archive.org/details/pub_journal-of-parapsychology"),
    ("dogs", "James Madison University CISR — the Army's mine-dog trials", "https://www.jmu.edu/news/cisr/2022/10/261-2/05-261-evans-mdd.shtml"),
    ("mk136", "CIA reading room — MKULTRA Subproject 136", "https://www.cia.gov/readingroom/docs/MKULTRA%20%20SUBPROJECT%20136%20%20[8144493].pdf"),
    ("ssci", "US Senate, 1977 — Project MKULTRA hearing", "https://info.publicintelligence.net/SSCI-MKULTRA-1977.pdf"),
    ("rice", "NCpedia — Rice Diet", "https://www.ncpedia.org/rice-diet"),
    ("rice-w", "Wikipedia — Rice diet", "https://en.wikipedia.org/wiki/Rice_diet"),
    ("hayti", "Wikipedia — Hayti, Durham", "https://en.wikipedia.org/wiki/Hayti,_Durham,_North_Carolina"),
    ("mxlu", "Wikipedia — Malcolm X Liberation University", "https://en.wikipedia.org/wiki/Malcolm_X_Liberation_University"),
    ("drand", "drand — the League of Entropy's public randomness beacon", "https://drand.love/"),
]
N = {k: i + 1 for i, (k, _, _) in enumerate(SRC)}


def c(*ks):
    return "".join(f'<sup><a href="#s-{k}">[{N[k]}]</a></sup>' for k in ks)


PICS = {
    "pearce": ("img/pearce.png", 751, 498, "https://commons.wikimedia.org/wiki/File:Hubert_Pearce_with_J._B._Rhine.png"),
    "dice": ("img/dice.png", 303, 365, "https://commons.wikimedia.org/wiki/File:Joseph_Banks_Rhine_dice_experiment.png"),
    "rhine": ("img/rhine-1940.png", 446, 417, "https://commons.wikimedia.org/wiki/File:J._B._Rhine_psychical_researcher.png"),
}


def fig(k, cap, pd):
    src, w, h, url = PICS[k]
    return (f'<figure><img src="{BASE}{src}" width="{w}" height="{h}" alt="{E(cap)}" loading="lazy">'
            f'<figcaption>{E(cap)} {pd} <a href="{url}">Wikimedia Commons</a></figcaption></figure>')


def sources(th):
    return "<ol class=\"src\">" + "".join(
        f'<li id="s-{k}"><a href="{u}" rel="noopener">{E(t)}</a></li>' for k, t, u in SRC) + "</ol>"


def lab_html(L):
    return f"""
<div class="who" aria-label="{E(L['whoAria'])}">
 <div class="q"><span>{E(L['qPlayer'])}</span><span class="seg" id="who-player">
  <button type="button" data-v="human">{E(L['human'])}</button><button type="button" data-v="robot">{E(L['robot'])}</button></span></div>
 <div class="q"><span>{E(L['qBelief'])}</span><span class="seg" id="who-belief">
  <button type="button" data-v="sheep">{E(L['sheepQ'])}</button><button type="button" data-v="goat">{E(L['goatQ'])}</button><button type="button" data-v="unsure">{E(L['unsureQ'])}</button></span></div>
 <div class="q"><span>{E(L['qName'])}</span><input id="who-name" maxlength="32" autocomplete="nickname" placeholder="{E(L['namePh'])}"></div>
 <p id="robot-door" hidden>{L['robotDoor']}</p>
</div>
<div id="tests">
 <div class="tabs" role="tablist">
  <button type="button" role="tab" data-test="clairvoyance" aria-selected="true">{E(L['tabC'])}</button>
  <button type="button" role="tab" data-test="precognition" aria-selected="false">{E(L['tabP'])}</button>
  <button type="button" role="tab" data-test="dice" aria-selected="false">{E(L['tabD'])}</button>
 </div>
 <p class="intro"></p>
 <div class="row"><div class="face"></div><div><div class="count"></div><div class="tally"></div>
  <button type="button" class="again">{E(L['again'])}</button><p class="status" aria-live="polite"></p></div></div>
 <div class="calls"></div>
 <div class="out" hidden aria-live="polite"></div>
</div>"""


def pool_html(L):
    return f"""<div id="pool"><p class="mine small"></p><div class="tbl"><table></table></div>
<h3>{E(L['posTitle'])}</h3><div class="pos"></div><p class="cap">{E(L['posCap'])}</p></div>"""


def forecast_html(L):
    return f"""<div id="fc">
<p class="open small"></p>
<div class="slots"></div>
<div class="pad"></div>
<div class="btnrow"><button type="button" class="send" disabled>{E(L['send'])}</button><button type="button" class="clear">{E(L['clear'])}</button></div>
<p class="msg" aria-live="polite"></p>
<h3>{E(L['boardTitle'])}</h3><div class="tbl"><table class="board"></table></div>
<h3>{E(L['recentTitle'])}</h3><ul class="recent"></ul>
</div>"""


def robots_block():
    return f"""<pre>curl -s {API}/

# a run: open it, then call 25 cards
curl -s -X POST {API}/session \\
  -H 'content-type: application/json' -A 'your-bot/1.0' \\
  -d '{{"test":"clairvoyance","player":"robot","belief":"goat","name":"your-bot"}}'
curl -s -X POST {API}/session/&lt;id&gt;/call -H 'content-type: application/json' -A 'your-bot/1.0' -d '{{"call":"star"}}'

# tomorrow's forecast: 25 symbols before 11:00 UTC
curl -s -X POST {API}/forecast -H 'content-type: application/json' -A 'your-bot/1.0' \\
  -d '{{"name":"your-bot","player":"robot","calls":["star","waves","circle", …25]}}'

curl -s {API}/stats
curl -s {API}/forecast</pre>"""


# ---------------------------------------------------------------- English

EN = {
    "circle": "circle", "cross": "cross", "waves": "waves", "square": "square", "star": "star",
    "whoAria": "Who is playing", "qPlayer": "You are", "human": "a person", "robot": "a robot",
    "qBelief": "Can ESP happen?", "sheepQ": "Yes", "goatQ": "No", "unsureQ": "Not sure",
    "qName": "Name on the board", "namePh": "optional",
    "robotDoor": 'Robots can play from the page, or from code: <a href="#robots">the API</a>.',
    "tabC": "Cards · clairvoyance", "tabP": "Before the shuffle · precognition", "tabD": "Dice · mind over matter",
    "again": "New run", "send": "Send forecast", "clear": "Clear",
    "posTitle": "Hits by place in the run",
    "posCap": "Every card and precognition call anyone has made, by its place in the run of 25. The dashed line is chance, 20%. Rhine's lab reported scores sagging as a run went on.",
    "boardTitle": "Leaderboard", "recentTitle": "Past draws",
}
EN_JS = {
    **{k: EN[k] for k in ("circle", "cross", "waves", "square", "star")},
    "intro": {
        "clairvoyance": "The server shuffles a closed deck of 25, five of each symbol, and keeps it hidden. Call each card before it turns. This is Rhine's basic clairvoyance test from the early 1930s. Keys 1–5 work too.",
        "precognition": "Call a symbol. Only then does the server draw the target. Nothing exists to peek at when you call. Rhine's lab announced precognition results in 1938.",
        "dice": "Pick the face you want. The server throws one die. 24 throws; chance is 1 in 6, so 4 hits. Rhine started dice tests in 1934.",
    },
}


def en_js():
    return """window.RHINE_L={circle:"circle",cross:"cross",waves:"waves",square:"square",star:"star",
intro:%s,
card:function(n,t,test){return (test==="dice"?"Throw ":"Card ")+n+" of "+t},
done:"Run done",dealing:"Shuffling…",counted:"The server holds the targets. This run counts toward the tallies.",
offline:"Server not reached: this run plays in your browser and does not count.",err:"Something went wrong:",
hits:function(h,n){return h+" of "+n},
chance:function(h,n,e,pct,z){return "Chance alone gives "+e+" on average. A score of "+h+" or better turns up in about "+pct+"%% of runs by luck (z = "+z+"). Rhine's lab looked for scores well past 2 on that scale, across many runs."},
bellAlt:"How often luck gives each score, with yours marked",
bellCap:function(n,t){return "Bars: how often luck alone gives each score in "+n+(t==="dice"?" throws.":" calls.")+" Yours is blue."},
youTitle:"What your calls say about you",repLabel:"Same symbol twice in a row",
rep:function(r){return r+" times. A random caller does it about 5 times in 25; most people do it less, because repeats don't feel random."},
useLabel:"Symbols you called",use:function(s,c){return "Most called: "+s+", "+c+" times. The deck holds 5 of each."},
halfLabel:"First half, second half",half:function(a,b){return a+" hits in cards 1–12, "+b+" in 14–25. Rhine's lab reported scores dropping as a run wore on."},
notCounted:"Played in your browser; not counted.",countedDone:"Counted. The pooled tallies below include this run.",
rowName:{all:"Everyone",clairvoyance:"Cards",precognition:"Before the shuffle",dice:"Dice",human:"People",robot:"Robots",sheep:"Say yes to ESP",goat:"Say no",unsure:"Not sure"},
cols:["Runs","Calls","Hits","Hit rate","Chance","z"],
posAlt:"Hit rate at each place in the run of 25, against the 20%% chance line",
mine:function(t,h,e){return "Your runs on this device: "+h+" hits in "+t+" calls; chance gives "+e+"."},
sending:"Sending…",entered:function(n,w){return "In, as <b>"+n+"</b>. Drawn "+w+"."},
open:function(w,c,n,r){return "Next draw: "+w+" (your time), from drand round "+r+". Entries close "+c+". "+n+" in so far."},
entries:function(n){return n+" forecast"+(n===1?"":"s")},noneYet:"No draws yet.",
boardCols:["Name","Kind","Draws","Hits","z"],boardEmpty:"Empty until the first draw with entries."};""" % json.dumps(EN_JS["intro"])


def en_page():
    L = EN
    name, tag = "The Rhine Deck", "Rhine's ESP tests from Duke, to play, count and forecast, for people and robots."
    nav = [("play", "Play"), ("tally", "Tally"), ("forecast", "Forecast"), ("robots", "Robots"),
           ("lab", "The lab"), ("archive", "The archive"), ("durham", "Durham"), ("sources", "Sources")]
    h = head("en", "The Rhine Deck — Duke's ESP tests, to play and count",
             "Take J.B. Rhine's card, precognition and dice tests against a server that deals and checks every card. Pooled tallies for people and robots, and a daily forecast drawn from a public randomness beacon.",
             "", name, nav, BASE + "th/", "ไทย", "Five Zener cards fanned under the title The Rhine Deck")
    body = f"""
<h1>The Rhine <b>Deck</b></h1>
<p class="lede">From 1930, J.B. Rhine's lab at Duke University in Durham, North Carolina, asked thousands of people to guess
hidden cards. Here are three of its tests. A server deals and checks every card, so a score here means the same whether a person
or a robot made it.{c('rrc', 'jbr')}</p>

<h2 id="play">Play</h2>
{lab_html(L)}

<h2 id="tally">Tally</h2>
<p>Every counted run, pooled. <b>z</b> measures distance from chance: between −2 and 2 is what luck gives about 95 times in 100.
The believer and doubter rows repeat a 1940s test by Gertrude Schmeidler, who found people who said yes to ESP scoring a little
above people who said no. She called them sheep and goats.{c('sheep')}</p>
{pool_html(L)}

<h2 id="forecast">Forecast</h2>
<p>Call 25 symbols for a deck nobody has shuffled yet. Each day at 12:00 UTC the server takes that moment's number from
<b>drand</b>, a public randomness beacon run by universities and companies in the League of Entropy, and turns it into 25
symbols.{c('drand')} Nobody knows the target ahead of time, the server included, and anyone can check it afterwards. Entries close at 11:00 UTC. One forecast
per name per day. People and robots share the board.</p>
{forecast_html(L)}
<p class="small">To check a target: take the round's <code>randomness</code> from drand. For i = 0, 1, 2 …, hash
<code>randomness + ":" + i</code> with SHA-256. Keep the first byte when it is under 250; that byte mod 5 is the symbol
(0 circle, 1 cross, 2 waves, 3 square, 4 star). Stop at 25.</p>

<h2 id="robots">Robots</h2>
<p>Robots are welcome, under their own name, marked robot. The tallies keep robots in their own row. A robot that calls a
pseudo-random sequence should land on chance, which makes robots the control group this kind of test always needed. Send a
User-Agent that names your bot; some network filters turn away blank or library defaults.</p>
{robots_block()}

<h2 id="lab">The lab</h2>
{fig('rhine', 'J.B. Rhine, 1940, from Life.', 'Public domain.')}
<ol class="tl">
<li><b>1895</b>Joseph Banks Rhine born in Waterloo, Pennsylvania. He and Louisa Weckesser, married 1920, both take botany doctorates at the University of Chicago.{c('ncpedia', 'louisa')}</li>
<li><b>1927</b>The Rhines come to Duke to work with the psychologist William McDougall.{c('ncpedia')}</li>
<li><b>1930</b>Card-guessing work begins. Karl Zener, a Duke psychologist, designs the deck: 25 cards, five each of circle, cross, waves, square and star.{c('rrc', 'zener')}</li>
<li><b>1933–34</b>Hubert Pearce, a divinity student, calls cards in the library while J.G. Pratt turns them in another building: 558 hits in 1,850 calls, where chance gives 370.{c('pratt', 'psi')}</li>
<li><b>1934</b>Rhine's book <i>Extra-Sensory Perception</i> puts the phrase in circulation. Dice tests begin the same year, after a young gambler claims he can steer a throw.{c('esp-book', 'pk')}</li>
<li><b>1935</b>The Parapsychology Laboratory opens on Duke's East Campus.{c('psi')}</li>
<li><b>1937</b><i>Journal of Parapsychology</i> starts. The president of the Institute of Mathematical Statistics writes that any fair attack on the work "must be on other than mathematical grounds."{c('rrc', 'psi')}</li>
<li><b>1938 · 1943</b>The lab announces precognition, then the dice results.{c('rrc-nc')}</li>
<li><b>1948</b>Louisa Rhine starts studying letters from the public about hunches, dreams and coincidences; the collection passes 30,000.{c('louisa')}</li>
<li><b>1962–65</b>Rhine sets up the Foundation for Research on the Nature of Man (FRNM) and, retiring from Duke in 1965, moves the work off campus. Sources differ on the founding year.{c('psi', 'rrc')}</li>
<li><b>1974</b>Walter Levy, the young director Rhine had picked, is caught by three colleagues tampering with recording equipment in rat experiments. He resigns, and Rhine publishes the case in his own journal.{c('levy', 'fraud')}</li>
<li><b>1980 · 1995</b>Rhine dies in 1980. FRNM becomes the Rhine Research Center on his centenary; it still runs in Durham.{c('ncpedia', 'rrc')}</li>
</ol>
{fig('pearce', 'Hubert Pearce and J.B. Rhine at a card test, from Extra-Sensory Perception, 1934.', 'Public domain.')}
<h3>The critics</h3>
<p>The early high scores came under three lines of attack. First, cards leak: subjects could read worn backs or see a
card reflected in the experimenter's glasses. Second, other labs failed to reproduce the results. At Princeton, W.S. Cox ran 25,064 calls with 132 people
and found nothing past chance. Third, C.E.M. Hansel argued the Pearce–Pratt layout left room to cheat, and Rhine and Pratt answered him in print.{c('zener', 'esp-book')}
Martin Gardner reported that Rhine kept quiet the names of twelve experimenters caught being dishonest in the 1940s.{c('jbr')}
The tests above answer the leak: the server holds the cards, and each precognition target is drawn after the call.</p>

<h3>The government</h3>
<p>In 1952–53 the US Army's engineering lab at Fort Belvoir paid Rhine to test whether dogs could find buried mines on
California beaches. The Army dropped it in 1953 for machines.{c('dogs')} The CIA's MKULTRA program funded one ESP study,
Subproject 136, approved in 1961, with the contractor's name blacked out.{c('mk136', 'ssci')} No released document places
an MKULTRA project at Duke or FRNM.</p>

<h2 id="archive">The archive</h2>
{fig('dice', 'A dice test at the Duke lab, 1954, from Life.', 'Public domain.')}
<p>Duke's Rubenstein Library holds the Parapsychology Laboratory records: 340 linear feet, about 250,000 items, 1893–1984.
They include score sheets, research files, and more than 350 boxes of letters, among them letters from Jung, Upton Sinclair and Aldous Huxley.{c('paralab', 'letters')}
The <i>Journal of Parapsychology</i> is scanned from 1937 on.{c('jop')}</p>
<p>Set the ESP question aside and the archive is a record of how ordinary people behaved in front of a card they could
not see. Some of it could be read today:</p>
<div class="ideas">
<div class="idea"><h3>Folk randomness</h3><p>Every call sheet shows what people think random looks like. Most avoid repeats and spread their calls too evenly. This page measures that in your own run.</p></div>
<div class="idea"><h3>Experimenter effects</h3><p>The same test gave different scores under different testers. The score sheets record who ran each session, so the effect can be measured.</p></div>
<div class="idea"><h3>The history of cheating</h3><p>Lady Wonder the horse, the twelve unnamed experimenters, the Levy case: an analog-era file on how people cheat, and how they get caught.{c('psi')}</p></div>
<div class="idea"><h3>Tired calls</h3><p>Scores sagging late in a run, which Rhine's lab called the decline effect, look like boredom and fatigue on paper. The tally above tracks it live.{c('decline')}</p></div>
<div class="idea"><h3>Belief and performance</h3><p>Sheep and goats: whether saying you believe changes how you play. The tally above splits every call three ways.</p></div>
<div class="idea"><h3>Letters as folklore</h3><p>Louisa Rhine's 30,000 letters are American dream and premonition stories, told in their own words, mid-century.</p></div>
</div>

<h2 id="durham">Durham</h2>
<p>The lab sat inside a city changing fast. Near Duke, from 1939, Walter Kempner ran the Rice Diet: rice, fruit, no salt.
It made Durham a destination for dieters, and a 1993 lawsuit alleged Kempner had whipped a patient.{c('rice', 'rice-w')} The two men make a pair:
Rhine, patient with his numbers; Kempner, controlling his patients' every meal. From 1958, urban renewal cleared Hayti,
the Black business and cultural district south of downtown, and the Durham Freeway split it.{c('hayti')} Malcolm X Liberation
University opened in Durham in 1969, moved to Greensboro in 1970 and closed in 1973.{c('mxlu')}</p>

<h2 id="sources">Sources</h2>
{sources(False)}
"""
    return h + body + foot("en", name, tag)


# ---------------------------------------------------------------- Thai

TH = {
    "circle": "วงกลม", "cross": "บวก", "waves": "คลื่น", "square": "สี่เหลี่ยม", "star": "ดาว",
    "whoAria": "ใครเล่น", "qPlayer": "คุณเป็น", "human": "คน", "robot": "หุ่นยนต์",
    "qBelief": "ญาณพิเศษมีจริงไหม", "sheepQ": "มี", "goatQ": "ไม่มี", "unsureQ": "ไม่แน่ใจ",
    "qName": "ชื่อบนกระดาน", "namePh": "ไม่ใส่ก็ได้",
    "robotDoor": 'หุ่นยนต์เล่นจากหน้านี้ก็ได้ หรือเรียกผ่านโค้ด: <a href="#robots">API</a>',
    "tabC": "ไพ่ · ตาทิพย์", "tabP": "ทายก่อนสับ · รู้ล่วงหน้า", "tabD": "ลูกเต๋า · ใจสั่งวัตถุ",
    "again": "เริ่มใหม่", "send": "ส่งคำทาย", "clear": "ล้าง",
    "posTitle": "ทายถูกตามลำดับในรอบ",
    "posCap": "ทุกคำทายไพ่และทายล่วงหน้าที่ทุกคนเคยทาย แยกตามลำดับที่ 1–25 ในรอบ เส้นประคือโอกาส 20% ห้องแล็บของไรน์รายงานว่าคะแนนมักตกลงช่วงท้ายรอบ",
    "boardTitle": "กระดานคะแนน", "recentTitle": "ผลที่ออกแล้ว",
}
TH_INTRO = {
    "clairvoyance": "เซิร์ฟเวอร์สับไพ่ 25 ใบ สัญลักษณ์ละ 5 ใบ แล้วคว่ำไว้ ทายทีละใบก่อนเปิด นี่คือการทดสอบตาทิพย์พื้นฐานของไรน์ช่วงต้นทศวรรษ 1930 กดปุ่ม 1–5 ก็ได้",
    "precognition": "ทายก่อน แล้วเซิร์ฟเวอร์จึงสุ่มไพ่เป้าหมาย ตอนที่ทาย ยังไม่มีไพ่ให้แอบดู ห้องแล็บของไรน์ประกาศผลเรื่องรู้ล่วงหน้าในปี 1938",
    "dice": "เลือกหน้าที่อยากให้ออก แล้วเซิร์ฟเวอร์ทอยลูกเต๋าหนึ่งลูก 24 ครั้ง โอกาส 1 ใน 6 ก็คือถูก 4 ครั้ง ไรน์เริ่มทดสอบลูกเต๋าในปี 1934",
}


def th_js():
    return """window.RHINE_L={circle:"วงกลม",cross:"บวก",waves:"คลื่น",square:"สี่เหลี่ยม",star:"ดาว",
intro:%s,
card:function(n,t,test){return (test==="dice"?"ทอยที่ ":"ใบที่ ")+n+" จาก "+t},
done:"จบรอบ",dealing:"กำลังสับ…",counted:"เซิร์ฟเวอร์ถือไพ่เป้าหมายไว้ รอบนี้นับรวมในสถิติ",
offline:"ติดต่อเซิร์ฟเวอร์ไม่ได้ รอบนี้เล่นในเบราว์เซอร์และไม่นับรวม",err:"มีปัญหา:",
hits:function(h,n){return "ถูก "+h+" จาก "+n},
chance:function(h,n,e,pct,z){return "ถ้าเดาล้วน ๆ จะถูกเฉลี่ย "+e+" ครั้ง คะแนน "+h+" หรือสูงกว่า เกิดจากโชคได้ราว "+pct+"%% ของรอบ (z = "+z+") ห้องแล็บของไรน์มองหาคะแนนที่เกิน 2 ไปไกล ๆ ในหลาย ๆ รอบ"},
bellAlt:"โอกาสที่โชคล้วน ๆ ให้แต่ละคะแนน พร้อมคะแนนของคุณ",
bellCap:function(n,t){return "แท่ง: โอกาสที่เดาล้วน ๆ จะได้แต่ละคะแนนใน "+n+(t==="dice"?" ทอย":" คำทาย")+" แท่งสีน้ำเงินคือของคุณ"},
youTitle:"คำทายบอกอะไรเกี่ยวกับคุณ",repLabel:"ทายซ้ำตัวเดิมติดกัน",
rep:function(r){return r+" ครั้ง ถ้าสุ่มจริงจะซ้ำราว 5 ครั้งใน 25 คนส่วนใหญ่ซ้ำน้อยกว่านั้น เพราะรู้สึกว่าซ้ำแล้วไม่สุ่ม"},
useLabel:"สัญลักษณ์ที่คุณทาย",use:function(s,c){return "ทายบ่อยสุด: "+s+" "+c+" ครั้ง ในสำรับมีอย่างละ 5 ใบ"},
halfLabel:"ครึ่งแรก ครึ่งหลัง",half:function(a,b){return "ถูก "+a+" ครั้งในใบที่ 1–12 และ "+b+" ครั้งในใบที่ 14–25 ห้องแล็บของไรน์รายงานว่าคะแนนตกลงเมื่อรอบยืดออกไป"},
notCounted:"เล่นในเบราว์เซอร์ ไม่นับรวม",countedDone:"นับแล้ว สถิติรวมด้านล่างรวมรอบนี้ด้วย",
rowName:{all:"ทุกคน",clairvoyance:"ไพ่",precognition:"ทายก่อนสับ",dice:"ลูกเต๋า",human:"คน",robot:"หุ่นยนต์",sheep:"ตอบว่ามี",goat:"ตอบว่าไม่มี",unsure:"ไม่แน่ใจ"},
cols:["รอบ","คำทาย","ถูก","อัตราถูก","โอกาส","z"],
posAlt:"อัตราทายถูกตามลำดับในรอบ 25 ใบ เทียบเส้นโอกาส 20%%",
mine:function(t,h,e){return "รอบของคุณบนเครื่องนี้: ถูก "+h+" จาก "+t+" คำทาย เดาล้วน ๆ ได้ "+e},
sending:"กำลังส่ง…",entered:function(n,w){return "รับแล้ว ในชื่อ <b>"+n+"</b> ออกผล "+w},
open:function(w,c,n,r){return "ออกผลครั้งถัดไป: "+w+" (เวลาของคุณ) จาก drand รอบ "+r+" ปิดรับ "+c+" ส่งมาแล้ว "+n+" คำทาย"},
entries:function(n){return n+" คำทาย"},noneYet:"ยังไม่มีผล",
boardCols:["ชื่อ","ประเภท","ครั้ง","ถูก","z"],boardEmpty:"ว่างอยู่จนกว่าจะออกผลครั้งแรกที่มีคนส่ง"};""" % json.dumps(TH_INTRO, ensure_ascii=False)


def th_page():
    L = TH
    name, tag = "สำรับไรน์", "แบบทดสอบญาณพิเศษของไรน์จากมหาวิทยาลัยดุ๊ก ให้เล่น นับ และทายล่วงหน้า ทั้งคนและหุ่นยนต์"
    nav = [("play", "เล่น"), ("tally", "สถิติ"), ("forecast", "ทายล่วงหน้า"), ("robots", "หุ่นยนต์"),
           ("lab", "ห้องแล็บ"), ("archive", "คลังเอกสาร"), ("durham", "เดอรัม"), ("sources", "แหล่งอ้างอิง")]
    h = head("th", "สำรับไรน์ — แบบทดสอบญาณพิเศษของดุ๊ก ให้เล่นและนับ",
             "ลองแบบทดสอบไพ่ ทายล่วงหน้า และลูกเต๋าของ เจ.บี. ไรน์ กับเซิร์ฟเวอร์ที่แจกและตรวจไพ่ทุกใบ สถิติรวมของคนและหุ่นยนต์ และการทายรายวันจากตัวเลขสุ่มสาธารณะ",
             "th/", name, nav, BASE, "English", "ไพ่เซเนอร์ห้าใบกางเป็นพัดใต้ชื่อ The Rhine Deck")
    body = f"""
<h1>สำรับ<b>ไรน์</b></h1>
<p class="lede">ตั้งแต่ปี 1930 ห้องแล็บของ เจ.บี. ไรน์ ที่มหาวิทยาลัยดุ๊ก เมืองเดอรัม รัฐนอร์ทแคโรไลนา ให้คนหลายพันคนทายไพ่ที่คว่ำอยู่
ที่นี่มีแบบทดสอบของแล็บนั้นสามแบบ เซิร์ฟเวอร์เป็นคนแจกและตรวจไพ่ทุกใบ คะแนนจึงมีความหมายเท่ากัน ไม่ว่าคนหรือหุ่นยนต์จะเป็นคนทาย{c('rrc', 'jbr')}</p>

<h2 id="play">เล่น</h2>
{lab_html(L)}

<h2 id="tally">สถิติ</h2>
<p>รวมทุกรอบที่นับ <b>z</b> คือระยะห่างจากการเดาล้วน ๆ ค่าระหว่าง −2 ถึง 2 เกิดจากโชคได้ราว 95 ครั้งใน 100
แถวคนที่ตอบว่ามีกับไม่มี มาจากการทดลองของ เกอร์ทรูด ชไมด์เลอร์ ในทศวรรษ 1940 เธอพบว่าคนที่เชื่อทำคะแนนได้สูงกว่าคนไม่เชื่อนิดหน่อย
เธอเรียกสองกลุ่มนี้ว่า แกะ กับ แพะ{c('sheep')}</p>
{pool_html(L)}

<h2 id="forecast">ทายล่วงหน้า</h2>
<p>ทายสัญลักษณ์ 25 ตัว ให้สำรับที่ยังไม่มีใครสับ ทุกวันเวลา 12:00 UTC (19:00 เวลาไทย) เซิร์ฟเวอร์จะเอาตัวเลขของเวลานั้นจาก
<b>drand</b> เครื่องสุ่มสาธารณะที่มหาวิทยาลัยและบริษัทใน League of Entropy ช่วยกันเดิน มาแปลงเป็นสัญลักษณ์ 25 ตัว{c('drand')}
ก่อนเวลานั้นไม่มีใครรู้ผล รวมทั้งเซิร์ฟเวอร์เอง และใครก็ตรวจย้อนหลังได้ ปิดรับ 11:00 UTC (18:00 เวลาไทย) ชื่อละหนึ่งคำทายต่อวัน
คนกับหุ่นยนต์ใช้กระดานเดียวกัน</p>
{forecast_html(L)}
<p class="small">วิธีตรวจผล: เอาค่า <code>randomness</code> ของรอบนั้นจาก drand แล้วสำหรับ i = 0, 1, 2 … ให้แฮช
<code>randomness + ":" + i</code> ด้วย SHA-256 เก็บไบต์แรกเมื่อน้อยกว่า 250 ไบต์นั้นหาร 5 เอาเศษคือสัญลักษณ์
(0 วงกลม, 1 บวก, 2 คลื่น, 3 สี่เหลี่ยม, 4 ดาว) ครบ 25 ตัวแล้วหยุด</p>

<h2 id="robots">หุ่นยนต์</h2>
<p>หุ่นยนต์เล่นได้ ใช้ชื่อของตัวเอง และติดป้ายว่าหุ่นยนต์ สถิติแยกหุ่นยนต์ไว้แถวของมันเอง หุ่นยนต์ที่ทายด้วยตัวเลขสุ่มเทียมควรได้คะแนนเท่าโอกาสพอดี
หุ่นยนต์จึงเป็นกลุ่มควบคุมที่การทดลองแบบนี้ขาดมาตลอด ส่ง User-Agent ที่บอกชื่อบอตด้วย เพราะตัวกรองบางตัวไม่รับคำขอที่ว่างหรือเป็นค่าเริ่มต้นของไลบรารี</p>
{robots_block()}

<h2 id="lab">ห้องแล็บ</h2>
{fig('rhine', 'เจ.บี. ไรน์ ปี 1940 จากนิตยสาร Life', 'สาธารณสมบัติ')}
<ol class="tl">
<li><b>1895</b>โจเซฟ แบงส์ ไรน์ เกิดที่เมืองวอเตอร์ลู รัฐเพนซิลเวเนีย เขากับหลุยซา เว็กเคสเซอร์ ซึ่งแต่งงานกันในปี 1920 จบปริญญาเอกด้านพฤกษศาสตร์จากมหาวิทยาลัยชิคาโกทั้งคู่{c('ncpedia', 'louisa')}</li>
<li><b>1927</b>สองสามีภรรยาไรน์มาที่ดุ๊ก เพื่อทำงานกับนักจิตวิทยา วิลเลียม แม็กดูกัลล์{c('ncpedia')}</li>
<li><b>1930</b>เริ่มงานทายไพ่ คาร์ล เซเนอร์ นักจิตวิทยาของดุ๊ก ออกแบบสำรับ: 25 ใบ วงกลม บวก คลื่น สี่เหลี่ยม ดาว อย่างละ 5 ใบ{c('rrc', 'zener')}</li>
<li><b>1933–34</b>ฮิวเบิร์ต เพียร์ซ นักศึกษาเทววิทยา นั่งทายไพ่ในห้องสมุด ขณะที่ เจ.จี. แพรตต์ พลิกไพ่อยู่อีกตึกหนึ่ง: ถูก 558 จาก 1,850 ครั้ง ขณะที่โอกาสให้ 370{c('pratt', 'psi')}</li>
<li><b>1934</b>หนังสือ <i>Extra-Sensory Perception</i> ของไรน์ทำให้คำว่า ESP แพร่หลาย ปีเดียวกันเริ่มทดสอบลูกเต๋า หลังนักพนันหนุ่มคนหนึ่งอ้างว่าบังคับลูกเต๋าได้{c('esp-book', 'pk')}</li>
<li><b>1935</b>ห้องแล็บจิตศาสตร์ (Parapsychology Laboratory) เปิดที่วิทยาเขตตะวันออกของดุ๊ก{c('psi')}</li>
<li><b>1937</b>เริ่มออกวารสาร <i>Journal of Parapsychology</i> นายกสมาคมสถิติคณิตศาสตร์เขียนว่า ถ้าจะค้านงานนี้อย่างเป็นธรรม ต้องค้านด้วยเหตุอื่นที่ไม่ใช่คณิตศาสตร์{c('rrc', 'psi')}</li>
<li><b>1938 · 1943</b>แล็บประกาศผลเรื่องรู้ล่วงหน้า แล้วตามด้วยผลลูกเต๋า{c('rrc-nc')}</li>
<li><b>1948</b>หลุยซา ไรน์ เริ่มศึกษาจดหมายจากประชาชนเรื่องลางสังหรณ์ ความฝัน และเรื่องบังเอิญ จดหมายสะสมเกิน 30,000 ฉบับ{c('louisa')}</li>
<li><b>1962–65</b>ไรน์ตั้งมูลนิธิวิจัยธรรมชาติของมนุษย์ (FRNM) และเมื่อเกษียณจากดุ๊กในปี 1965 ก็ย้ายงานออกนอกมหาวิทยาลัย แหล่งข้อมูลระบุปีก่อตั้งไม่ตรงกัน{c('psi', 'rrc')}</li>
<li><b>1974</b>วอลเตอร์ เลวี ผู้อำนวยการหนุ่มที่ไรน์เลือกเอง ถูกเพื่อนร่วมงานสามคนจับได้ว่าแก้เครื่องบันทึกในการทดลองกับหนู เขาลาออก และไรน์ตีพิมพ์เรื่องนี้ในวารสารของตัวเอง{c('levy', 'fraud')}</li>
<li><b>1980 · 1995</b>ไรน์เสียชีวิตปี 1980 ครบร้อยปีชาตกาล FRNM เปลี่ยนชื่อเป็น Rhine Research Center ซึ่งยังเปิดอยู่ที่เดอรัม{c('ncpedia', 'rrc')}</li>
</ol>
{fig('pearce', 'ฮิวเบิร์ต เพียร์ซ กับ เจ.บี. ไรน์ ระหว่างทดสอบไพ่ จากหนังสือ Extra-Sensory Perception ปี 1934', 'สาธารณสมบัติ')}
<h3>ผู้คัดค้าน</h3>
<p>คะแนนสูงช่วงแรกโดนค้านสามทาง หนึ่ง ไพ่รั่ว: ผู้ถูกทดสอบอาจอ่านรอยหลังไพ่ หรือเห็นเงาไพ่สะท้อนในแว่นของผู้ทดลอง
สอง ที่อื่นทำซ้ำไม่ได้: ที่พรินซ์ตัน ดับเบิลยู.เอส. ค็อกซ์ ให้คน 132 คนทาย 25,064 ครั้ง ไม่พบอะไรเกินโอกาส สาม ซี.อี.เอ็ม. แฮนเซล
ชี้ว่าการจัดห้องของเพียร์ซ–แพรตต์เปิดช่องให้โกงได้ ไรน์กับแพรตต์ตีพิมพ์คำตอบ{c('zener', 'esp-book')}
มาร์ติน การ์ดเนอร์ รายงานว่าไรน์ไม่เปิดชื่อผู้ทดลองสิบสองคนที่ถูกจับได้ว่าไม่ซื่อตรงในทศวรรษ 1940{c('jbr')}
แบบทดสอบข้างบนตอบเรื่องไพ่รั่ว: เซิร์ฟเวอร์ถือไพ่ไว้ และไพ่เป้าหมายแบบรู้ล่วงหน้าถูกสุ่มหลังจากทายแล้ว</p>

<h3>รัฐบาล</h3>
<p>ปี 1952–53 ห้องแล็บวิศวกรรมของกองทัพบกสหรัฐที่ฟอร์ตเบลวัวร์จ้างไรน์ทดสอบว่าสุนัขหาทุ่นระเบิดที่ฝังบนชายหาดแคลิฟอร์เนียได้ไหม
กองทัพเลิกในปี 1953 แล้วหันไปใช้เครื่องจักร{c('dogs')} โครงการ MKULTRA ของซีไอเอให้ทุนงานวิจัย ESP หนึ่งชิ้น คือโครงการย่อยที่ 136
อนุมัติปี 1961 ชื่อผู้รับทุนถูกคาดดำ{c('mk136', 'ssci')} ยังไม่มีเอกสารที่เปิดเผยแล้วชิ้นไหนระบุว่ามีโครงการ MKULTRA ที่ดุ๊กหรือ FRNM</p>

<h2 id="archive">คลังเอกสาร</h2>
{fig('dice', 'การทดสอบลูกเต๋าที่แล็บดุ๊ก ปี 1954 จากนิตยสาร Life', 'สาธารณสมบัติ')}
<p>หอสมุดรูเบนสไตน์ของดุ๊กเก็บเอกสารของห้องแล็บไว้ 340 ฟุต ราว 250,000 ชิ้น ช่วงปี 1893–1984 มีใบคะแนน แฟ้มวิจัย
และจดหมายกว่า 350 กล่อง รวมถึงจดหมายจาก คาร์ล ยุง, อัปตัน ซินแคลร์ และ อัลดัส ฮักซ์ลีย์{c('paralab', 'letters')}
วารสาร <i>Journal of Parapsychology</i> สแกนไว้ตั้งแต่ปี 1937{c('jop')}</p>
<p>ถ้าวางคำถามเรื่อง ESP ไว้ก่อน คลังนี้คือบันทึกว่าคนธรรมดาทำตัวอย่างไรเมื่อเจอไพ่ที่มองไม่เห็น บางเรื่องอ่านใหม่ได้วันนี้:</p>
<div class="ideas">
<div class="idea"><h3>สุ่มแบบชาวบ้าน</h3><p>ใบคะแนนทุกใบบอกว่าคนคิดว่าการสุ่มหน้าตาเป็นอย่างไร ส่วนใหญ่เลี่ยงการซ้ำ และกระจายคำทายเท่า ๆ กันเกินไป หน้านี้วัดเรื่องนี้จากรอบของคุณเอง</p></div>
<div class="idea"><h3>ผลจากผู้ทดลอง</h3><p>แบบทดสอบเดียวกัน คนคุมต่างกัน คะแนนก็ต่างกัน ใบคะแนนบันทึกไว้ว่าใครคุมแต่ละรอบ จึงวัดผลนี้ได้</p></div>
<div class="idea"><h3>ประวัติการโกง</h3><p>ม้าชื่อเลดี้วันเดอร์ ผู้ทดลองสิบสองคนที่ไม่เปิดชื่อ คดีเลวี: แฟ้มยุคแอนะล็อกว่าคนโกงกันอย่างไร และถูกจับได้อย่างไร{c('psi')}</p></div>
<div class="idea"><h3>ทายจนเหนื่อย</h3><p>คะแนนที่ตกช่วงท้ายรอบ ซึ่งแล็บของไรน์เรียกว่า decline effect บนกระดาษดูเหมือนความเบื่อและความล้า สถิติข้างบนติดตามเรื่องนี้สด ๆ{c('decline')}</p></div>
<div class="idea"><h3>ความเชื่อกับคะแนน</h3><p>แกะกับแพะ: การบอกว่าเชื่อ เปลี่ยนวิธีเล่นไหม สถิติข้างบนแยกทุกคำทายเป็นสามกลุ่ม</p></div>
<div class="idea"><h3>จดหมายคือนิทานพื้นบ้าน</h3><p>จดหมาย 30,000 ฉบับของหลุยซา ไรน์ คือเรื่องฝันและลางสังหรณ์ของคนอเมริกันกลางศตวรรษ เล่าด้วยคำของเขาเอง</p></div>
</div>

<h2 id="durham">เดอรัม</h2>
<p>ห้องแล็บตั้งอยู่ในเมืองที่กำลังเปลี่ยนเร็ว ใกล้ ๆ ดุ๊ก ตั้งแต่ปี 1939 วอลเตอร์ เคมป์เนอร์ เปิดคลินิกอาหารข้าว (Rice Diet): ข้าว ผลไม้ ไม่ใส่เกลือ
ทำให้เดอรัมเป็นเมืองของคนมาลดน้ำหนัก และคดีฟ้องในปี 1993 กล่าวหาว่าเคมป์เนอร์เฆี่ยนคนไข้{c('rice', 'rice-w')} สองคนนี้เป็นคู่ตรงข้ามกัน:
ไรน์ใจเย็นกับตัวเลข เคมป์เนอร์คุมทุกคำที่คนไข้กิน ตั้งแต่ปี 1958 โครงการฟื้นฟูเมืองรื้อย่านเฮย์ตี ย่านธุรกิจและวัฒนธรรมของคนผิวดำทางใต้ของตัวเมือง
แล้วทางด่วนเดอรัมก็ผ่าย่านนั้นเป็นสองซีก{c('hayti')} มหาวิทยาลัยมัลคอล์ม เอกซ์ เปิดที่เดอรัมปี 1969 ย้ายไปกรีนส์โบโรปี 1970 และปิดปี 1973{c('mxlu')}</p>

<h2 id="sources">แหล่งอ้างอิง</h2>
{sources(True)}
"""
    return h + body + foot("th", name, tag)


# ---------------------------------------------------------------- machine files

def machine():
    (DOCS / "icon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#123a8c"/>'
                                   '<path d="M32 12l5.4 13.5 14.5.8-11.2 9.3 3.7 14.1L32 42l-12.4 7.7 3.7-14.1-11.2-9.3 14.5-.8z" fill="none" stroke="#fffaf0" stroke-width="4" stroke-linejoin="round"/></svg>\n')
    (DOCS / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    (DOCS / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"<url><loc>{SITE_URL}/</loc><lastmod>{TODAY}</lastmod></url>\n<url><loc>{SITE_URL}/th/</loc><lastmod>{TODAY}</lastmod></url>\n</urlset>\n")
    (DOCS / "llms.txt").write_text(f"""# The Rhine Deck

> J.B. Rhine's ESP tests from Duke University (1930s–60s), played against a server that deals and checks every card.
> People and robots are both invited. Robots play under their own name, marked "robot", and are tallied in their own row.

- Page: {SITE_URL}/ (Thai: {SITE_URL}/th/)
- API, self-describing: {API}/
- Tests: clairvoyance (closed deck of 25), precognition (target drawn after the call), dice (24 throws, call a face 1–6)
- Pooled tallies: {API}/stats
- Daily forecast: POST 25 symbols to {API}/forecast before 11:00 UTC; the target comes from drand quicknet at 12:00 UTC and anyone can recompute it. Leaderboard: {API}/forecast
- Symbols: circle, cross, waves, square, star
- Send a User-Agent naming your bot.

## Try it

curl -s -X POST {API}/session -H 'content-type: application/json' -A 'your-bot/1.0' -d '{{"test":"precognition","player":"robot","name":"your-bot"}}'
""")
    (DOCS / "ai.txt").write_text(f"# The Rhine Deck — robots may read, cite and play.\nAPI: {API}/\n")
    (DOCS / "humans.txt").write_text(f"/* SITE */\nThe Rhine Deck · สำรับไรน์\n{SITE_URL}/\nBuilt {TODAY}\n")
    (DOCS / ".nojekyll").write_text("")
    fleet.decorate(DOCS, SELF, roster=FLEET)


def main():
    (DOCS / "th").mkdir(parents=True, exist_ok=True)
    (DOCS / "index.html").write_text(en_page(), encoding="utf-8")
    (DOCS / "th" / "index.html").write_text(th_page(), encoding="utf-8")
    lab = (ROOT / "js" / "lab.js").read_text(encoding="utf-8")
    # the strings ride in front of the lab code; each page picks its language by <html lang>
    (DOCS / "lab.js").write_text(
        "(function(){var th=document.documentElement.lang==='th';\n" + "if(th){" + th_js() + "}else{" + en_js() + "}})();\n" + lab,
        encoding="utf-8")
    machine()
    print("docs/ built")


if __name__ == "__main__":
    main()
