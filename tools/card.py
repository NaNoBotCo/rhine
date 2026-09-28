#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""card.py — the 1200×630 share card: five Zener cards fanned under the title."""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
W, H = 1200, 630
PAPER = (244, 239, 226)
CARD = (255, 250, 240)
INK = (27, 28, 34)
BLUE = (18, 58, 140)
MUTE = (93, 90, 82)
COND = "/System/Library/Fonts/Avenir Next Condensed.ttc"
BODY = "/System/Library/Fonts/Avenir Next.ttc"


def font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.load_default()


def symbol(d, s, cx, cy, r, w):
    if s == 0:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=w)
    elif s == 1:
        d.line([cx, cy - r * 1.1, cx, cy + r * 1.1], fill=BLUE, width=w)
        d.line([cx - r * 1.1, cy, cx + r * 1.1, cy], fill=BLUE, width=w)
    elif s == 2:
        for k in (-1, 0, 1):
            pts = [(cx - r * 1.2 + i * r * 2.4 / 40, cy + k * r * 0.62 + math.sin(i / 40 * 4 * math.pi) * r * 0.24)
                   for i in range(41)]
            d.line(pts, fill=BLUE, width=w, joint="curve")
    elif s == 3:
        d.rectangle([cx - r * .9, cy - r * .9, cx + r * .9, cy + r * .9], outline=BLUE, width=w)
    else:
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rr = r * 1.15 if i % 2 == 0 else r * 0.47
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        d.polygon(pts, outline=BLUE, width=w)


def build():
    S = 2
    img = Image.new("RGBA", (W * S, H * S), PAPER + (255,))
    for i, s in enumerate(range(5)):
        cw, ch = 168 * S, 236 * S
        c = Image.new("RGBA", (cw + 40, ch + 40), (0, 0, 0, 0))
        d = ImageDraw.Draw(c)
        d.rounded_rectangle([20, 20, 20 + cw, 20 + ch], radius=22 * S, fill=CARD + (255,), outline=INK, width=4 * S)
        symbol(d, s, 20 + cw / 2, 20 + ch / 2, 50 * S, 8 * S)
        c = c.rotate(-24 + i * 12, resample=Image.BICUBIC, expand=True)
        x = int((566 + i * 126) * S - c.width / 2 + 60 * S)
        y = int(330 * S - c.height / 2 + abs(i - 2) * 26 * S + 10 * S)
        img.alpha_composite(c, (x, y))
    img = img.resize((W, H), Image.LANCZOS).convert("RGB")
    d = ImageDraw.Draw(img)
    d.text((64, 70), "DUKE · DURHAM, NORTH CAROLINA", font=font(COND, 30, 2), fill=BLUE)
    d.text((60, 118), "THE RHINE", font=font(COND, 112, 2), fill=INK)
    d.text((60, 232), "DECK", font=font(COND, 112, 2), fill=BLUE)
    d.text((66, 392), "Guess 25 cards.", font=font(BODY, 34), fill=INK)
    d.text((66, 436), "See what your guesses", font=font(BODY, 34), fill=INK)
    d.text((66, 480), "say about you.", font=font(BODY, 34), fill=INK)
    d.text((66, H - 56), "nanobotco.github.io/rhine", font=font(BODY, 26), fill=MUTE)
    out = ROOT / "docs" / "card.jpg"
    img.save(out, format="JPEG", quality=88, optimize=True)
    print(f"card → {out}")


if __name__ == "__main__":
    build()
