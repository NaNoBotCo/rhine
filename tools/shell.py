#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""shell.py — head, top bar, footer and CSS shared by the English and Thai pages."""
from __future__ import annotations

import html
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fleet  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://nanobotco.github.io/rhine"
BASE = "/rhine/"
SELF = "rhine"
FLEET = fleet.load(ROOT / "data" / "fleet.json")
TODAY = date.today().isoformat()
E = html.escape
SIB = ("chemtrails", "indras-net", "chaos", "talking-board", "bots-crave", "split-screen")

CSS = """
:root{
 --paper:#f4efe2;--card:#fffaf0;--ink:#1b1c22;--mute:#5d5a52;--line:#d8cfb8;
 --blue:#123a8c;--hot:#b8321f;--hit:#1f7a4a;--miss:#b8321f;--gold:#9a6b12;
 --display:"Avenir Next Condensed","HelveticaNeue-CondensedBold","Arial Narrow Bold",Impact,system-ui,sans-serif;
 --body:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Thonburi","Sukhumvit Set",serif;
 --sans:"Avenir Next",Avenir,"Segoe UI",system-ui,"Thonburi",sans-serif;
 color-scheme:light dark}
@media (prefers-color-scheme:dark){:root{
 --paper:#12131a;--card:#1b1d27;--ink:#efe9dc;--mute:#a8a293;--line:#343748;
 --blue:#8fb2ff;--hot:#ff7a63;--hit:#6fd39a;--miss:#ff7a63;--gold:#e8bd62}}
*{box-sizing:border-box}
html{font-size:19px;background:var(--paper)}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);line-height:1.6}
a{color:var(--blue)}
.sr{position:absolute;left:-9999px}.sr:focus{left:1rem;top:1rem;z-index:9;background:var(--card);padding:.5rem}
header.top{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--paper) 92%,transparent);
 backdrop-filter:blur(6px);border-bottom:1px solid var(--line);transition:transform .25s}
header.top .in,main,footer .in{max-width:46rem;margin:0 auto;padding:0 16px}
header.top .in{display:flex;flex-wrap:wrap;align-items:center;gap:.3rem 1rem;padding-top:.5rem;padding-bottom:.5rem}
.brand{font-family:var(--display);font-weight:800;font-size:1.15rem;text-transform:uppercase;letter-spacing:.04em;
 color:var(--ink);text-decoration:none;display:flex;align-items:center;gap:.45rem}
.brand svg{width:22px;height:22px;stroke:var(--blue);fill:none;stroke-width:5}
header nav{display:flex;flex-wrap:wrap;gap:.2rem .9rem;font-family:var(--sans);font-size:.8rem}
header nav a{text-decoration:none;color:var(--mute)}header nav a:hover{color:var(--ink)}
body.nav-tight header nav{display:none}body.nav-away header.top{transform:translateY(-100%)}
h1{font-family:var(--display);font-weight:800;text-transform:uppercase;font-size:clamp(2.3rem,8vw,3.8rem);
 line-height:.95;letter-spacing:.01em;margin:2rem 0 .6rem}
h1 b{color:var(--blue)}
h2,[id]{scroll-margin-top:4rem}
h2{font-family:var(--display);font-weight:800;text-transform:uppercase;font-size:1.6rem;letter-spacing:.03em;
 margin:2.8rem 0 .5rem;border-top:3px solid var(--ink);padding-top:.6rem}
h3{font-family:var(--sans);font-size:1rem;margin:1.4rem 0 .3rem}
.lede{font-size:1.15rem;color:var(--ink);max-width:40rem}
.small,.cap{font-family:var(--sans);font-size:.8rem;color:var(--mute)}
sup a{text-decoration:none;font-family:var(--sans);font-size:.7em}
/* the deck */
#tests{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1rem;margin:1.4rem 0;
 box-shadow:0 1px 0 var(--line)}
#tests .row{display:flex;gap:1rem;align-items:center;flex-wrap:wrap}
.face{width:128px;height:176px;flex:none}
.face>div{width:100%;height:100%;border-radius:10px;display:grid;place-items:center;border:2px solid var(--ink)}
.back{background:repeating-linear-gradient(45deg,var(--blue) 0 6px,color-mix(in srgb,var(--blue) 70%,var(--card)) 6px 12px);
 color:var(--card);font-family:var(--display);font-size:3rem;font-weight:800}
.front{background:var(--card)}.front.hit{border-color:var(--hit);box-shadow:0 0 0 3px var(--hit)}
.front.miss{border-color:var(--miss)}
.sym{fill:none;stroke:currentColor;stroke-width:4;stroke-linejoin:round;stroke-linecap:round}
.front .sym{color:var(--ink)}
.count{font-family:var(--display);font-weight:800;text-transform:uppercase;letter-spacing:.05em;font-size:1.2rem}
.tally{display:flex;flex-wrap:wrap;gap:4px;margin:.4rem 0;max-width:15rem}
.tally i{width:12px;height:12px;border-radius:50%;border:1.5px solid var(--mute)}
.tally i.h{background:var(--hit);border-color:var(--hit)}
.calls{display:grid;grid-template-columns:repeat(5,1fr);gap:.4rem;margin-top:1rem}
.call{font-family:var(--sans);font-size:.72rem;background:var(--paper);color:var(--ink);border:1.5px solid var(--line);
 border-radius:10px;padding:.5rem .2rem .35rem;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:.15rem}
.call:hover,.call:focus-visible{border-color:var(--blue);outline:none}
.call .sym{color:var(--blue)}
.again{font-family:var(--sans);font-size:.8rem;background:none;border:1px solid var(--line);color:var(--mute);
 border-radius:99px;padding:.3rem .8rem;cursor:pointer}
.out .big{font-family:var(--display);font-weight:800;font-size:2.4rem;margin:.6rem 0 0;text-transform:uppercase}
.bell{width:100%;height:auto;display:block;margin:.6rem 0 .1rem}
.bell .bar{fill:color-mix(in srgb,var(--mute) 45%,transparent)}.bell .you{fill:var(--blue)}
.bell .ax{font:11px var(--sans);fill:var(--mute);text-anchor:middle}
.you-dl{display:grid;grid-template-columns:auto 1fr;gap:.3rem 1rem;font-family:var(--sans);font-size:.88rem}
.you-dl dt{font-weight:700}.you-dl dd{margin:0}
.u{display:inline-flex;align-items:center;gap:.15rem;margin-right:.5rem}.u .sym{color:var(--blue)}
/* timeline and lists */
.tl{list-style:none;padding:0;margin:1rem 0;border-left:3px solid var(--line)}
.tl li{position:relative;padding:.1rem 0 .8rem 1.1rem}
.tl li::before{content:"";position:absolute;left:-8px;top:.55rem;width:13px;height:13px;border-radius:50%;
 background:var(--paper);border:3px solid var(--blue)}
.tl b{font-family:var(--display);font-size:1.05rem;letter-spacing:.03em;margin-right:.35rem}
.ideas{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:.8rem;margin:1rem 0}
.idea{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:.8rem .95rem}
.idea h3{margin:.1rem 0 .3rem;font-family:var(--display);text-transform:uppercase;letter-spacing:.03em;font-size:1.05rem;color:var(--blue)}
.idea p{margin:0;font-size:.93rem}
.note{border-left:3px solid var(--gold);padding:.2rem 0 .2rem .9rem;color:var(--ink);font-size:.95rem}
figure{margin:1.4rem 0}figure img{width:100%;height:auto;border-radius:10px;border:1px solid var(--line);display:block}
figcaption{font-family:var(--sans);font-size:.75rem;color:var(--mute);margin-top:.3rem}
.src{font-family:var(--sans);font-size:.8rem;padding-left:1.4rem}.src li{margin:.35rem 0}
.lang{font-family:var(--sans);font-size:.8rem}
footer.bot{margin-top:3.5rem;border-top:3px solid var(--ink);padding:1rem 0 2.5rem;font-family:var(--sans);font-size:.8rem;color:var(--mute)}
footer .fleet,footer .support{margin:.5rem 0}
.die rect{fill:var(--card);stroke:var(--ink);stroke-width:3}.die circle{fill:var(--ink)}
.call .die rect{stroke:var(--blue)}.call .die circle{fill:var(--blue)}
.back.dice{border-radius:18px;width:112px;height:112px;margin:32px auto 0}
.calls.busy{opacity:.55;pointer-events:none}
.tabs{display:flex;flex-wrap:wrap;gap:.35rem;margin:0 0 .8rem}
.tabs button,.seg button{font-family:var(--sans);font-size:.82rem;background:var(--paper);color:var(--ink);border:1.5px solid var(--line);
 border-radius:99px;padding:.35rem .85rem;cursor:pointer}
.tabs button[aria-selected=true],.seg button[aria-pressed=true]{background:var(--blue);border-color:var(--blue);color:var(--card)}
.intro{font-size:.93rem;margin:.2rem 0 .8rem}
.status{font-family:var(--sans);font-size:.75rem;color:var(--mute);margin:.3rem 0 0}
.who{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:.8rem 1rem;margin:1.2rem 0;
 display:grid;gap:.55rem;font-family:var(--sans);font-size:.85rem}
.who .q{display:flex;flex-wrap:wrap;align-items:center;gap:.4rem .6rem}
.who .q>span:first-child{font-weight:700;min-width:9rem}
.seg{display:flex;flex-wrap:wrap;gap:.3rem}
.who input{font:inherit;padding:.35rem .6rem;border:1.5px solid var(--line);border-radius:8px;background:var(--paper);color:var(--ink);width:14rem;max-width:100%}
#robot-door{font-size:.85rem}
pre{font-family:ui-monospace,Menlo,monospace;font-size:.72rem;background:var(--card);border:1px solid var(--line);border-radius:10px;
 padding:.7rem .8rem;overflow-x:auto;line-height:1.45}
code{font-family:ui-monospace,Menlo,monospace;font-size:.85em}
.tbl{width:100%;overflow-x:auto}
table{border-collapse:collapse;font-family:var(--sans);font-size:.8rem;width:100%;min-width:30rem}
th,td{padding:.3rem .45rem;text-align:right;border-bottom:1px solid var(--line)}
th:first-child,tbody th{text-align:left}
table.empty{min-width:0}table.empty td{text-align:left;color:var(--mute)}
tr.sep td{border:0;padding:.2rem}
td.z.hot{color:var(--hot);font-weight:700}
.bell .chance{stroke:var(--hot);stroke-dasharray:4 3;stroke-width:1.5}.bell .ax.end{text-anchor:end;fill:var(--hot)}
.slots{display:grid;grid-template-columns:repeat(5,1fr);gap:.3rem;max-width:20rem;margin:.6rem 0}
.slot{aspect-ratio:1;border:1.5px dashed var(--line);border-radius:8px;background:var(--card);color:var(--mute);display:grid;place-items:center;
 font-family:var(--sans);font-size:.7rem;cursor:pointer;padding:0}
.slot .sym{color:var(--blue)}.slot.next{border-color:var(--blue);border-style:solid}
.pad{display:grid;grid-template-columns:repeat(5,1fr);gap:.4rem;max-width:26rem}
.btnrow{display:flex;gap:.5rem;margin:.7rem 0;flex-wrap:wrap}
.btnrow button{font-family:var(--sans);font-size:.85rem;border-radius:99px;padding:.45rem 1rem;cursor:pointer;border:1.5px solid var(--line);background:var(--paper);color:var(--ink)}
.btnrow .send{background:var(--blue);border-color:var(--blue);color:var(--card);font-weight:700}
.btnrow .send:disabled{opacity:.4;cursor:default}
.recent{list-style:none;padding:0;font-family:var(--sans);font-size:.8rem}.recent li{margin:.25rem 0}
.recent .sym{color:var(--blue);stroke-width:6;vertical-align:-2px}
.msg{font-family:var(--sans);font-size:.85rem;min-height:1.2em}
@media (max-width:30rem){.calls span{display:none}.face{width:104px;height:144px}.who .q>span:first-child{min-width:0;width:100%}}
"""

MARK = ('<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="22"/></svg>')

NAV_JS = """(function(){var h=document.querySelector("header.top");if(!h)return;var b=document.body,y=window.pageYOffset,up=0,dn=0,t=false;function tight(on){if(on===b.classList.contains("nav-tight"))return;var r=document.documentElement.style;r.overflowAnchor="none";h.style.marginBottom="";var a=h.offsetHeight;b.classList.toggle("nav-tight",on);if(on)h.style.marginBottom=Math.max(0,a-h.offsetHeight)+"px";h.offsetHeight;r.overflowAnchor=""}function f(){t=false;var n=window.pageYOffset,d=n-y;y=n;if(n<60){up=dn=0;b.classList.remove("nav-away");tight(false);return}tight(true);if(d>0){dn+=d;up=0;if(dn>14)b.classList.add("nav-away")}else if(d<0){up-=d;dn=0;if(up>90)b.classList.remove("nav-away")}}addEventListener("scroll",function(){if(!t){t=true;requestAnimationFrame(f)}},{passive:true});addEventListener("resize",function(){if(b.classList.contains("nav-tight")){b.classList.remove("nav-tight");tight(true)}},{passive:true});addEventListener("focusin",function(e){if(h.contains(e.target)){b.classList.remove("nav-away");tight(false)}});f()})();"""


def head(lang, title, desc, path, name, nav, alt_href, alt_label, card_alt):
    url = SITE_URL + "/" + path
    links = "".join(f'<a href="#{i}">{E(t)}</a>' for i, t in nav)
    return f"""<!doctype html><html lang="{lang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{SITE_URL}/"><link rel="alternate" hreflang="th" href="{SITE_URL}/th/">
<meta property="og:type" content="website"><meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/card.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(card_alt)}">
<meta property="og:site_name" content="{E(name)}"><meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE_URL}/card.jpg">
<meta name="theme-color" content="#f4efe2">
<link rel="icon" href="{BASE}icon.svg" type="image/svg+xml">
<style>{CSS}</style></head><body>
<a class="sr" href="#main">{"ข้ามไปที่เนื้อหา" if lang == "th" else "Skip to the content"}</a>
<header class="top"><div class="in">
<a class="brand" href="{BASE}{"th/" if lang == "th" else ""}">{MARK}{E(name)}</a>
<nav aria-label="{"สารบัญ" if lang == "th" else "Sections"}">{links}<a class="lang" href="{alt_href}" hreflang="{"en" if lang == "th" else "th"}">{E(alt_label)}</a></nav>
</div></header><main id="main">"""


def foot(lang, name, tag):
    th = lang == "th"
    row = fleet.row_html(SELF, label="เว็บพี่น้อง" if th else "More 'splainers", roster=FLEET, ids=SIB)
    more = fleet.row_html(SELF, label="จาก NaNoBotCo" if th else "Also from NaNoBotCo", roster=FLEET)
    support = fleet.support_html(roster=FLEET, self_id=SELF)
    maker = fleet.maker_html(roster=FLEET, lang=lang)
    lic = ("ข้อความ CC BY 4.0 · โค้ด MIT · รูปจาก Wikimedia Commons ตามสัญญาอนุญาตที่ระบุใต้ภาพ · สร้างเมื่อ "
           if th else "Text CC BY 4.0. Code MIT. Pictures from Wikimedia Commons under the licence given with each. Built ")
    return f"""</main><footer class="bot"><div class="in">
<p><b>{E(name)}</b> — {E(tag)}</p>
<p class="small">{lic}{TODAY}.</p>
{row}
{more}
{support}
{maker}
</div></footer><script defer src="{BASE}lab.js"></script><script>{NAV_JS}</script></body></html>"""
