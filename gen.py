#!/usr/bin/env python3
"""THE WORLD IN ONE PICTURE - Wednesday 18 November 2026.

Deterministic PIL broadsheet generator. Renders at 2x (2048), LANCZOS
downscales to 1024x1024. All stories verified genuine 18 Nov 2026 events;
see ../dev/STORY-POOL.md for sources and exclusions.
"""
import math

from PIL import Image, ImageDraw, ImageFont

S = 2
W = H = 1024

PAPER = (247, 243, 234)
PAPER_DK = (238, 232, 218)
INK = (18, 30, 58)
NAVY = (24, 40, 66)
RED = (178, 34, 38)
RED_LT = (205, 70, 66)
GOLD = (212, 145, 45)
SEA = (38, 78, 120)
SKY_TOP = (28, 52, 96)
SKY_BOT = (232, 150, 92)
STEEL = (96, 112, 132)
GREY = (92, 98, 110)
WHITE = (255, 255, 255)
BLACK = (12, 14, 18)
CREAM = (250, 246, 238)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

_fc = {}


def font(size, bold=False):
    k = (round(size * 2) / 2.0, bold)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(BOLD if bold else REG, int(round(size * S)))
    return _fc[k]


def sc(v):
    return int(round(v * S))


def rect(d, x, y, w, h, **kw):
    if "width" in kw:
        kw["width"] = max(1, sc(kw["width"]))
    d.rectangle([sc(x), sc(y), sc(x + w), sc(y + h)], **kw)


def rrect(d, x, y, w, h, r, **kw):
    if "width" in kw:
        kw["width"] = max(1, sc(kw["width"]))
    d.rounded_rectangle([sc(x), sc(y), sc(x + w), sc(y + h)], radius=sc(r), **kw)


def ell(d, cx, cy, rx, ry, **kw):
    d.ellipse([sc(cx - rx), sc(cy - ry), sc(cx + rx), sc(cy + ry)], **kw)


def line(d, pts, **kw):
    if "width" in kw:
        kw["width"] = max(1, sc(kw["width"]))
    d.line([(sc(x), sc(y)) for x, y in pts], **kw)


def poly(d, pts, **kw):
    if "width" in kw:
        kw["width"] = max(1, sc(kw["width"]))
    d.polygon([(sc(x), sc(y)) for x, y in pts], **kw)


def arc(d, box, a0, a1, **kw):
    if "width" in kw:
        kw["width"] = max(1, sc(kw["width"]))
    d.arc([sc(v) for v in box], a0, a1, **kw)


def lerp(c1, c2, t):
    return tuple(int(round(a + (b - a) * t)) for a, b in zip(c1, c2))


def vgrad(img, x, y, w, h, top, bot):
    d = ImageDraw.Draw(img)
    rows = sc(h)
    for i in range(rows + 1):
        t = i / max(1, rows)
        d.line([(sc(x), sc(y) + i), (sc(x + w), sc(y) + i)], fill=lerp(top, bot, t))


def text(d, x, y, s, size, color=INK, bold=False, anchor="la"):
    d.text((sc(x), sc(y)), s, font=font(size, bold), fill=color, anchor=anchor)


def text_w(s, size, bold=False):
    return font(size, bold).getlength(s) / S


def wrap(d, x, y, s, size, maxw, color=INK, bold=False, lh=None):
    """Word-wrap text; returns y after last line."""
    lh = lh or size * 1.28
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(trial, size, bold) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for ln in lines:
        text(d, x, y, ln, size, color, bold)
        y += lh
    return y


def kicker(d, x, y, s, color=RED, size=15):
    text(d, x, y, s, size, color, bold=True)


def headline(d, x, y, s, size, maxw, color=INK, lh=None):
    return wrap(d, x, y, s, size, maxw, color, bold=True, lh=lh)


def rule(d, x, y, w, color=INK, width=2):
    line(d, [(x, y), (x + w, y)], fill=color, width=width)


# ---------------------------------------------------------------- skyline
def skyline(d, x, y, w, h, color):
    """Simple Shenzhen-style tower silhouettes inside (x,y,w,h)."""
    import random as _r
    rng = _r.Random(1811)
    cx = x
    while cx < x + w - 8:
        bw = rng.randint(16, 42)
        bh = h * rng.uniform(0.35, 1.0)
        rect(d, cx, y + h - bh, bw, bh, fill=color)
        # spire on some towers
        if rng.random() < 0.45:
            line(d, [(cx + bw / 2, y + h - bh), (cx + bw / 2, y + h - bh - 14)],
                 fill=color, width=3)
        # lit windows
        for _ in range(int(bw * bh / 260)):
            wx = cx + rng.uniform(3, bw - 5)
            wy = y + h - bh + rng.uniform(6, bh - 6)
            rect(d, wx, wy, 3, 4, fill=GOLD)
        cx += bw + rng.randint(4, 12)


# ---------------------------------------------------------------- flags
def flag_china(d, x, y, w, h):
    rect(d, x, y, w, h, fill=(222, 41, 16))
    # one big star + 4 small (simplified: 5 small gold stars)
    for sx, sy, r in [(x + w * 0.22, y + h * 0.28, 5), (x + w * 0.45, y + h * 0.18, 3),
                      (x + w * 0.58, y + h * 0.28, 3), (x + w * 0.58, y + h * 0.45, 3),
                      (x + w * 0.45, y + h * 0.55, 3)]:
        star(d, sx, sy, r, GOLD)


def flag_russia(d, x, y, w, h):
    rect(d, x, y, w, h / 3, fill=WHITE)
    rect(d, x, y + h / 3, w, h / 3, fill=(0, 57, 166))
    rect(d, x, y + 2 * h / 3, w, h / 3, fill=(213, 0, 0))


def flag_usa(d, x, y, w, h):
    for i in range(7):
        rect(d, x, y + i * h / 7, w, h / 7 + 1, fill=WHITE if i % 2 else (178, 34, 52))
    rect(d, x, y, w * 0.42, h * 0.55, fill=(24, 40, 96))
    for r in range(3):
        for c in range(4):
            ell(d, x + w * 0.06 + c * w * 0.095, y + h * 0.10 + r * h * 0.17, 1.6, 1.6,
                fill=WHITE)


def star(d, cx, cy, r, color):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    poly(d, pts, fill=color)


def flagpole(d, x, y, h, flag_fn, fw, fh):
    line(d, [(x, y), (x, y - h)], fill=(60, 60, 60), width=3)
    ell(d, x, y - h - 2, 3, 3, fill=GOLD)
    flag_fn(d, x + 2, y - h, fw, fh)


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W * S, H * S), PAPER)
    d = ImageDraw.Draw(img)

    # outer frame
    rect(d, 0, 0, W, H, outline=INK, width=4)
    rect(d, 8, 8, W - 16, H - 16, outline=INK, width=1)

    # ---------------- masthead ----------------
    text(d, W / 2, 26, "THE WORLD IN ONE PICTURE", 40, INK, bold=True, anchor="ma")
    rule(d, 60, 74, W - 120, color=RED, width=3)
    text(d, W / 2, 82, "WEDNESDAY  ·  18 NOVEMBER 2026", 21, RED, bold=True, anchor="ma")
    text(d, 60, 84, "ONE DAY — ONE IMAGE", 14, GREY, bold=True)
    text(d, W - 60, 84, "ALL STORIES VERIFIED", 14, GREY, bold=True, anchor="ra")

    # ---------------- hero: Shenzhen ----------------
    hx, hy, hw, hh = 24, 118, W - 48, 348
    vgrad(img, hx, hy, hw, hh, SKY_TOP, SKY_BOT)
    # sun low on horizon
    ell(d, hx + hw - 150, hy + hh - 78, 42, 42, fill=(250, 196, 110))
    # skyline across the bottom of the hero
    skyline(d, hx, hy + hh - 128, hw, 128, (16, 26, 52))
    # water / foreground band
    rect(d, hx, hy + hh - 34, hw, 34, fill=(14, 22, 46))
    # red carpet strip
    rect(d, hx, hy + hh - 34, hw, 6, fill=RED)
    # two leaders as silhouettes shaking hands, centre-right
    # figure A (left, dark suit)
    cx, cy = hx + 690, hy + hh - 34
    ell(d, cx, cy - 96, 13, 13, fill=BLACK)                    # head
    poly(d, [(cx - 15, cy), (cx - 12, cy - 84), (cx + 12, cy - 84),
             (cx + 15, cy)], fill=BLACK)                       # body
    line(d, [(cx + 10, cy - 70), (cx + 34, cy - 58)], fill=BLACK, width=7)  # arm
    # figure B (right, dark suit)
    cx2 = cx + 66
    ell(d, cx2, cy - 96, 13, 13, fill=BLACK)
    poly(d, [(cx2 - 15, cy), (cx2 - 12, cy - 84), (cx2 + 12, cy - 84),
             (cx2 + 15, cy)], fill=BLACK)
    line(d, [(cx2 - 10, cy - 70), (cx2 - 34, cy - 58)], fill=BLACK, width=7)
    # clasped hands
    ell(d, cx + 33, cy - 58, 7, 7, fill=BLACK)
    # flags flanking the pair
    flagpole(d, hx + 600, hy + hh - 40, 130, flag_china, 74, 48)
    flagpole(d, hx + 830, hy + hh - 40, 130, flag_russia, 74, 48)
    # small US flag arriving (right)
    flagpole(d, hx + 940, hy + hh - 40, 118, flag_usa, 56, 36)
    # APEC banner
    rrect(d, hx + hw / 2 - 150, hy + 16, 300, 34, 6, fill=(12, 20, 44))
    text(d, hx + hw / 2, hy + 23, "APEC  ·  SHENZHEN", 17, WHITE, bold=True, anchor="ma")
    # hero text block (top-left, on a translucent-style cream panel)
    rrect(d, hx + 18, hy + 52, 560, 190, 8, fill=CREAM)
    rect(d, hx + 18, hy + 52, 6, 190, fill=RED)
    kicker(d, hx + 40, hy + 64, "THE SUMMIT  ·  CHINA", size=16)
    y_end = headline(d, hx + 40, hy + 88, "XI AND PUTIN MEET IN SHENZHEN", 30, 520)
    wrap(d, hx + 40, y_end + 8, "Leaders hold bilateral talks on the eve of the first "
         "Trump–Xi–Putin trilateral. Trump arrives for APEC.", 16, 520, color=(40, 48, 66))
    # hero credit line
    text(d, hx + hw - 14, hy + hh - 12, "SHENZHEN, CHINA", 12, (200, 205, 220),
         bold=True, anchor="ra")

    # ---------------- row 1: three panels ----------------
    py, ph = 482, 232
    pw = (W - 48 - 2 * 14) / 3
    px = [24, 24 + pw + 14, 24 + 2 * (pw + 14)]

    # --- panel 1: Gulf ---
    x = px[0]
    rect(d, x, py, pw, ph, outline=INK, width=2, fill=(16, 28, 52))
    vgrad(img, x + 2, py + 2, pw - 4, 98, (20, 38, 74), (58, 96, 140))
    # sea
    rect(d, x + 2, py + 72, pw - 4, 28, fill=(18, 52, 88))
    # tanker
    tx, ty = x + 34, py + 56
    rect(d, tx, ty, 150, 26, fill=(40, 44, 52))
    rect(d, tx + 118, ty - 22, 26, 22, fill=(52, 56, 66))
    line(d, [(tx + 130, ty - 22), (tx + 130, ty - 44)], fill=(52, 56, 66), width=4)
    # smoke plume
    for i, (sx, sy, sr) in enumerate([(tx + 132, ty - 52, 10), (tx + 142, ty - 64, 13),
                                      (tx + 156, ty - 76, 16)]):
        ell(d, sx, sy, sr, sr * 0.8, fill=(120, 120, 120))
    # drones
    for dx, dy in [(x + pw - 70, py + 26), (x + pw - 110, py + 44)]:
        ell(d, dx, dy, 9, 4, fill=(220, 220, 220))
        line(d, [(dx - 12, dy), (dx + 12, dy)], fill=(220, 220, 220), width=2)
    kicker(d, x + 12, py + 108, "GULF ON EDGE", size=15)
    y_end = headline(d, x + 12, py + 130, "Iran fires drones at US base in Kuwait", 19, pw - 24, color=WHITE)
    wrap(d, x + 12, y_end + 4, "Bahrain intercepts more; ADNOC tanker hit in "
         "Hormuz — 1 missing, 11 hurt.", 13, pw - 24, color=(210, 216, 228))

    # --- panel 2: Kerch Bridge ---
    x = px[1]
    rect(d, x, py, pw, ph, outline=INK, width=2, fill=CREAM)
    vgrad(img, x + 2, py + 2, pw - 4, 98, (168, 196, 214), (214, 226, 232))
    # strait
    rect(d, x + 2, py + 64, pw - 4, 36, fill=(64, 110, 150))
    # bridge deck left + right, collapsed arch in the middle
    line(d, [(x + 8, py + 52), (x + 118, py + 52)], fill=(52, 58, 68), width=8)
    line(d, [(x + pw - 118, py + 52), (x + pw - 8, py + 52)], fill=(52, 58, 68), width=8)
    # fallen arch segment in the water (tilted)
    poly(d, [(x + 128, py + 70), (x + 178, py + 92), (x + 196, py + 82),
             (x + 150, py + 62)], fill=(52, 58, 68))
    # broken arch stubs
    arc(d, (x + 96, py + 14, x + 168, py + 78), 200, 340, fill=RED, width=6)
    arc(d, (x + pw - 168, py + 14, x + pw - 96, py + 78), 200, 340, fill=(52, 58, 68), width=6)
    # support pillars
    rect(d, x + 30, py + 52, 10, 48, fill=(52, 58, 68))
    rect(d, x + pw - 40, py + 52, 10, 48, fill=(52, 58, 68))
    # splash
    for sx, sy, sr in [(x + 160, py + 82, 8), (x + 178, py + 90, 6), (x + 146, py + 92, 5)]:
        ell(d, sx, sy, sr, sr * 0.6, fill=(230, 240, 246))
    kicker(d, x + 12, py + 108, "UKRAINE  ·  KERCH STRAIT", size=15)
    y_end = headline(d, x + 12, py + 130, "Bridge hit a third time in three days", 19, pw - 24)
    wrap(d, x + 12, y_end + 4, "Road span lies in the strait; rail stands, "
         "traffic halted again.", 13, pw - 24, color=(40, 48, 66))

    # --- panel 3: Voyager ---
    x = px[2]
    rect(d, x, py, pw, ph, outline=INK, width=2, fill=(8, 12, 30))
    # stars
    import random as _r
    rng = _r.Random(42)
    for _ in range(46):
        sx = x + rng.uniform(6, pw - 6)
        sy = py + rng.uniform(6, 96)
        sr = rng.uniform(1, 2.6)
        ell(d, sx, sy, sr, sr, fill=(255, 255, 255))
    # golden record disc
    gx, gy = x + pw - 62, py + 36
    ell(d, gx, gy, 26, 26, fill=GOLD)
    ell(d, gx, gy, 26, 26, outline=(120, 84, 20), width=2)
    ell(d, gx, gy, 8, 8, fill=(120, 84, 20))
    # probe body + dish + boom
    bx, by = x + 96, py + 62
    poly(d, [(bx, by - 12), (bx + 52, by - 6), (bx + 52, by + 10), (bx, by + 14)],
         fill=(190, 196, 204))
    # dish (parabola as polygon)
    poly(d, [(bx - 6, by - 26), (bx - 44, by - 40), (bx - 40, by - 6), (bx - 6, by - 2)],
         fill=(220, 226, 232))
    line(d, [(bx - 6, by - 14), (bx - 40, by - 22)], fill=(150, 156, 164), width=3)
    # boom + antenna
    line(d, [(bx + 52, by), (bx + 96, by - 18)], fill=(190, 196, 204), width=4)
    ell(d, bx + 96, by - 18, 4, 4, fill=GOLD)
    # signal waves
    for rr in (18, 30):
        arc(d, (bx + 96 - rr, by - 18 - rr, bx + 96 + rr, by - 18 + rr), -60, 60,
            fill=GOLD, width=3)
    kicker(d, x + 12, py + 108, "SPACE  ·  NASA", size=15)
    y_end = headline(d, x + 12, py + 130, "Voyager 1, one light-day from Earth", 19, pw - 24, color=WHITE)
    wrap(d, x + 12, y_end + 4, "First human-made object 16bn miles out — "
         "49 years after launch in 1977.", 13, pw - 24, color=(210, 216, 228))

    # ---------------- row 2: two panels ----------------
    qy, qh = 728, 150
    qw = (W - 48 - 14) / 2
    qx = [24, 24 + qw + 14]

    # --- COP31 ---
    x = qx[0]
    rect(d, x, qy, qw, qh, outline=INK, width=2, fill=CREAM)
    # sun + globe
    gx, gy = x + 56, qy + 52
    ell(d, gx, gy, 30, 30, fill=(232, 163, 61))
    ell(d, gx, gy, 30, 30, outline=(178, 120, 30), width=2)
    # globe meridians
    arc(d, (gx - 19, gy - 19, gx + 19, gy + 19), 90, 270, fill=(178, 120, 30), width=2)
    line(d, [(gx, gy - 30), (gx, gy + 30)], fill=(178, 120, 30), width=2)
    # thermometer
    tx2, ty2 = x + 104, qy + 26
    rect(d, tx2, ty2, 12, 48, fill=(230, 230, 230), outline=INK, width=2)
    rect(d, tx2 + 2, ty2 + 24, 8, 22, fill=RED)
    ell(d, tx2 + 6, ty2 + 54, 12, 12, fill=RED)
    # rising bars
    for i, bh in enumerate([16, 26, 38]):
        rect(d, x + 140 + i * 20, qy + 82 - bh, 13, bh, fill=SEA)
    tx = x + 196
    kicker(d, tx, qy + 12, "CLIMATE  ·  ANTALYA", size=15)
    y_end = headline(d, tx, qy + 34, "COP31 talks deadlocked", 21, qw - 208)
    wrap(d, tx, y_end + 4, "Ministers split on finance, fossil fuels and "
         "1.5°C.", 14.5, qw - 208, color=(40, 48, 66))

    # --- Australia sanctions ---
    x = qx[1]
    rect(d, x, qy, qw, qh, outline=INK, width=2, fill=CREAM)
    # stylised Australia map (simplified polygon)
    ax, ay = x + 22, qy + 26
    aus = [(0, 34), (14, 12), (52, 4), (96, 10), (128, 26), (150, 18), (168, 34),
           (150, 52), (158, 78), (128, 96), (96, 88), (58, 96), (26, 78), (8, 56)]
    poly(d, [(ax + px_, ay + py_) for px_, py_ in aus], fill=(46, 110, 72))
    # prohibition ring over the map = sanctions
    ell(d, ax + 128, ay + 66, 26, 26, outline=RED, width=6)
    line(d, [(ax + 110, ay + 48), (ax + 146, ay + 84)], fill=RED, width=6)
    tx = x + 196
    kicker(d, tx, qy + 12, "DIPLOMACY  ·  CANBERRA", size=15)
    y_end = headline(d, tx, qy + 34, "Australia sanctions West Bank settlers", 21, qw - 208)
    wrap(d, tx, y_end + 4, "Three people, four groups blacklisted over "
         "settlements.", 14.5, qw - 208, color=(40, 48, 66))

    # ---------------- IN BRIEF band ----------------
    by = 892
    rect(d, 24, by, W - 48, 102, fill=NAVY)
    text(d, 40, by + 10, "IN BRIEF", 17, GOLD, bold=True)
    rule(d, 40, by + 34, W - 80, color=(90, 110, 140), width=1)
    bw = (W - 48 - 32 - 2 * 24) / 3
    briefs = [
        ("CYCLONE AKVAN", "Severe storm bears down on India's Andhra coast; landfall due Friday."),
        ("WORD OF THE YEAR", "Cambridge picks “human” — the backlash to AI."),
        ("SIBERIA CRASH", "19 dead as a Russian An-12 transport goes down."),
    ]
    for i, (lead, body) in enumerate(briefs):
        bx = 40 + i * (bw + 24)
        text(d, bx, by + 42, lead, 14.5, GOLD, bold=True)
        wrap(d, bx, by + 62, body, 14.5, bw, color=WHITE)

    # footer line
    text(d, W / 2, 1000, "18 NOVEMBER 2026  ·  SHENZHEN  ·  GULF  ·  KERCH  ·  DEEP SPACE  ·  ANTALYA  ·  CANBERRA",
         12.5, GREY, bold=True, anchor="ma")

    img = img.resize((W, H), Image.LANCZOS)
    return img


if __name__ == "__main__":
    out = build()
    out.save("entry.png", optimize=True)
    print("saved entry.png", out.size)
