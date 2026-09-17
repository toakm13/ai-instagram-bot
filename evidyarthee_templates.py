from __future__ import annotations

from datetime import datetime
import os
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1080
ROOT = Path(__file__).resolve().parent

# Evidyarthee fixed brand system.
NAVY = "#0B2438"
GREEN = "#0E5A46"
GREEN_2 = "#174F42"
GOLD = "#D9A441"
SAFFRON = "#E27A32"
CREAM = "#F6F1E7"
WHITE = "#FFFFFF"
INK = "#16252B"
MUTED = "#607078"
LINE = "#D9D5CA"
PALE_GREEN = "#E8F1EC"
PALE_GOLD = "#F6E9C8"

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def f(size: int, bold: bool = False):
    p = FONT_B if bold else FONT_R
    return ImageFont.truetype(p, size) if Path(p).exists() else ImageFont.load_default()


def wrap(draw, text: str, font, width: int):
    words = str(text).split()
    lines, line = [], ""
    for word in words:
        candidate = (line + " " + word).strip()
        if draw.textbbox((0, 0), candidate, font=font)[2] <= width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def rr(draw, box, radius=22, fill=WHITE, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def logo(draw, x=48, y=32, scale=1.0, dark=True):
    """Simple vector-style Evidyarthee mark; deliberately larger than the old renderer."""
    ink = NAVY if dark else WHITE
    accent = GOLD
    # Book.
    draw.polygon([(x, y + 45*scale), (x + 38*scale, y + 28*scale), (x + 72*scale, y + 45*scale),
                  (x + 38*scale, y + 60*scale)], fill=ink)
    draw.line((x + 38*scale, y + 28*scale, x + 38*scale, y + 60*scale), fill=CREAM if dark else NAVY, width=max(1, int(2*scale)))
    # Growth stem/leaves.
    draw.line((x + 38*scale, y + 30*scale, x + 38*scale, y + 2*scale), fill=accent, width=max(2, int(4*scale)))
    draw.ellipse((x + 25*scale, y - 2*scale, x + 39*scale, y + 12*scale), fill=accent)
    draw.ellipse((x + 39*scale, y + 6*scale, x + 54*scale, y + 21*scale), fill=SAFFRON)
    draw.text((x + 88*scale, y + 3*scale), "Evidyarthee", font=f(int(44*scale), True), fill=ink)
    draw.text((x + 90*scale, y + 52*scale), "LEARN | INVEST | GROW", font=f(int(15*scale), True), fill=GOLD if dark else WHITE)


def watermark(img, opacity=42):
    """One medium, centered watermark — the fixed production rule."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    text = "Evidyarthee"
    ft = f(70, True)
    bbox = d.textbbox((0, 0), text, font=ft)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    cx, cy = W // 2, H // 2
    d.text((cx - tw // 2, cy - th // 2), text, font=ft, fill=(14, 90, 70, opacity))
    img.alpha_composite(layer)


def base(dark=False):
    bg = NAVY if dark else CREAM
    img = Image.new("RGBA", (W, H), bg)
    d = ImageDraw.Draw(img)
    # Fine editorial grid.
    for x in range(0, W, 90):
        d.line((x, 0, x, H), fill=(255, 255, 255, 10) if dark else (11, 36, 56, 8), width=1)
    for y in range(0, H, 90):
        d.line((0, y, W, y), fill=(255, 255, 255, 10) if dark else (11, 36, 56, 8), width=1)
    return img, d


def header(img, d, label, date=None, dark=False):
    # Strong but compact header; date sits on upper border as approved for News.
    fill = NAVY if not dark else GREEN_2
    rr(d, (30, 25, W - 30, 150), 26, fill=fill)
    logo(d, 55, 37, 0.78, dark=False)
    d.text((700, 48), label.upper(), font=f(25, True), fill=GOLD)
    if date:
        d.text((700, 88), date.upper(), font=f(19, True), fill=WHITE)


def footer(d, disclaimer=True):
    d.rectangle((0, 1010, W, H), fill=NAVY)
    d.text((45, 1030), "Evidyarthee", font=f(27, True), fill=GOLD)
    d.text((245, 1034), "LEARN | INVEST | GROW", font=f(18, True), fill=WHITE)
    if disclaimer:
        d.text((650, 1034), "Educational content • Not investment advice", font=f(14, True), fill=WHITE)


def card(d, box, title, body, fill=WHITE, accent=GREEN, body_size=24):
    rr(d, box, 20, fill=fill, outline=LINE, width=2)
    x1, y1, x2, y2 = box
    d.rectangle((x1, y1, x1 + 8, y2), fill=accent)
    d.text((x1 + 25, y1 + 18), title, font=f(21, True), fill=accent)
    y = y1 + 58
    for line in wrap(d, body, f(body_size), x2 - x1 - 55):
        d.text((x1 + 25, y), line, font=f(body_size), fill=INK)
        y += body_size + 9
        if y > y2 - 28:
            break


def extract_numbers(body):
    parts = [p.strip() for p in str(body).split(" • ") if p.strip()]
    return parts[:4]


def render_premarket(title, body, source, path):
    img, d = base(False)
    today = datetime.now().strftime("%d %B %Y")
    header(img, d, "PRE-MARKET", today)
    d.text((48, 185), "BEFORE THE MARKET OPENS", font=f(48, True), fill=NAVY)
    d.text((50, 245), "What matters today — without the noise.", font=f(23), fill=MUTED)

    # Main dashboard area.
    rr(d, (45, 295, 1035, 555), 28, fill=WHITE, outline=LINE, width=2)
    d.text((75, 325), "MARKET SNAPSHOT", font=f(23, True), fill=GREEN)
    nums = extract_numbers(body)
    x = 75
    if not nums:
        nums = ["Live market data unavailable — no figure stated"]
    for i, item in enumerate(nums[:3]):
        w = 300
        if i == 0 and len(nums) == 1:
            w = 850
        rr(d, (x, 375, x + w, 510), 18, fill=PALE_GREEN if i == 0 else CREAM)
        lines = wrap(d, item, f(24, True), w - 35)
        yy = 395
        for ln in lines[:3]:
            d.text((x + 18, yy), ln, font=f(24, True), fill=NAVY)
            yy += 32
        x += w + 22

    card(d, (45, 585, 520, 800), "01 | GLOBAL & DOMESTIC CUES",
         "Track verified overnight developments, rates, currencies, commodities and domestic policy signals. Focus on what changed — not predictions.", fill=WHITE, accent=SAFFRON, body_size=22)
    card(d, (545, 585, 1035, 800), "02 | WHAT TO WATCH",
         "Watch the opening reaction, sector participation and whether market moves are broad-based or concentrated.", fill=WHITE, accent=GREEN, body_size=22)

    rr(d, (45, 825, 1035, 970), 24, fill=PALE_GOLD, outline=GOLD, width=2)
    d.text((70, 850), "💡 EVIDYARTHEE LEARNING BITE", font=f(22, True), fill=NAVY)
    d.text((70, 892), "A market trigger is information; the price reaction is the market's response. They are not the same thing.", font=f(23, True), fill=INK)
    d.text((70, 928), "Learn the difference before drawing a conclusion.", font=f(20), fill=MUTED)
    footer(d)
    watermark(img)
    img.convert("RGB").save(path, "PNG", optimize=True)


def render_educational(title, body, source, path):
    img, d = base(False)
    today = datetime.now().strftime("%d %B %Y")
    header(img, d, "FINANCE 101", today)
    d.text((48, 185), title.upper(), font=f(47, True), fill=NAVY)
    d.text((50, 245), "One concept. One example. One takeaway.", font=f(23), fill=MUTED)

    # Hero formula area.
    rr(d, (45, 290, 1035, 455), 30, fill=GREEN, outline=GREEN)
    d.text((80, 325), "THE CONCEPT", font=f(20, True), fill=GOLD)
    lines = wrap(d, body, f(31, True), 890)
    yy = 370
    for ln in lines[:2]:
        d.text((80, yy), ln, font=f(31, True), fill=WHITE)
        yy += 44

    card(d, (45, 485, 520, 705), "HOW TO THINK ABOUT IT", 
         "Start with the definition, then test the concept using a simple numerical or real-world example.", fill=WHITE, accent=GREEN, body_size=23)
    card(d, (545, 485, 1035, 705), "WHAT IT DOESN'T TELL YOU",
         "No single ratio, indicator or headline gives a complete investment picture. Context matters.", fill=WHITE, accent=SAFFRON, body_size=23)

    rr(d, (45, 735, 1035, 895), 24, fill=PALE_GOLD, outline=GOLD, width=2)
    d.text((70, 760), "🧠 REMEMBER", font=f(22, True), fill=NAVY)
    d.text((70, 805), "Good financial education turns a headline into a question you can investigate.", font=f(26, True), fill=INK)

    rr(d, (45, 920, 1035, 970), 16, fill=PALE_GREEN)
    d.text((65, 934), "SOURCE / SERIES: " + str(source)[:85], font=f(15, True), fill=GREEN)
    footer(d)
    watermark(img)
    img.convert("RGB").save(path, "PNG", optimize=True)


def render_postmarket(title, body, source, path):
    img, d = base(True)
    header(img, d, "POST-MARKET", datetime.now().strftime("%d %B %Y"), dark=True)
    d.text((48, 185), "MARKET CLOSE", font=f(55, True), fill=WHITE)
    d.text((50, 248), "What happened • What mattered • What we learned", font=f(22), fill="#C7D7D2")

    rr(d, (45, 300, 1035, 525), 28, fill="#F8F5EC", outline=GOLD, width=2)
    d.text((75, 330), "INDEX SNAPSHOT", font=f(22, True), fill=GREEN)
    nums = extract_numbers(body) or ["Closing data unavailable — no figure stated"]
    x = 75
    for i, item in enumerate(nums[:3]):
        w = 300
        rr(d, (x, 380, x + w, 490), 18, fill=WHITE, outline=LINE, width=1)
        for j, ln in enumerate(wrap(d, item, f(23, True), w - 30)[:2]):
            d.text((x + 15, 395 + j * 30), ln, font=f(23, True), fill=NAVY)
        x += w + 22

    card(d, (45, 555, 350, 805), "BREADTH", "Was the move broad-based or driven by a small group of stocks?", fill="#F8F5EC", accent=GOLD, body_size=21)
    card(d, (370, 555, 675, 805), "SECTORS", "Which sectors led, lagged or diverged from the headline index?", fill="#F8F5EC", accent=SAFFRON, body_size=21)
    card(d, (695, 555, 1035, 805), "KEY NEWS", "Which verified development changed the day's context?", fill="#F8F5EC", accent=GREEN, body_size=21)

    rr(d, (45, 830, 1035, 965), 24, fill="#E8F1EC", outline=GREEN, width=2)
    d.text((70, 852), "💡 LEARNING BITE", font=f(22, True), fill=GREEN)
    d.text((70, 895), "A flat index can still hide strong sector rotation. Always look underneath the headline number.", font=f(24, True), fill=INK)
    d.text((70, 932), "THINK LIKE AN INVESTOR • CHECK THE EVIDENCE BEFORE THE STORY", font=f(17, True), fill=MUTED)
    footer(d)
    watermark(img)
    img.convert("RGB").save(path, "PNG", optimize=True)


def render_news(title, body, source, path):
    img, d = base(False)
    header(img, d, "MARKET NEWS", datetime.now().strftime("%d %B %Y"))
    d.text((48, 185), "MARKET NEWS HIGHLIGHTS", font=f(49, True), fill=NAVY)
    d.text((50, 245), "Verified facts • Context • Why it matters", font=f(23), fill=MUTED)

    # Editorial hero panel.
    rr(d, (45, 290, 1035, 475), 28, fill=WHITE, outline=LINE, width=2)
    d.text((75, 320), "TOP STORY", font=f(20, True), fill=SAFFRON)
    for i, ln in enumerate(wrap(d, title, f(38, True), 900)[:3]):
        d.text((75, 360 + i * 45), ln, font=f(38, True), fill=NAVY)

    card(d, (45, 505, 520, 690), "01 | ECONOMY & POLICY", "RBI, SEBI, government and major policy developments — stated from verified sources.", fill=WHITE, accent=GREEN, body_size=20)
    card(d, (545, 505, 1035, 690), "02 | CORPORATE", "Material company announcements, earnings, M&A, IPO and credit developments.", fill=WHITE, accent=SAFFRON, body_size=20)
    card(d, (45, 710, 520, 895), "03 | GLOBAL & SECTOR", "Important global markets, commodities, currencies and sector-specific developments.", fill=WHITE, accent=GOLD, body_size=20)
    card(d, (545, 710, 1035, 895), "04 | WHY IT MATTERS", "Explain the mechanism and affected areas without turning the news into a buy/sell call.", fill=WHITE, accent=GREEN, body_size=20)

    rr(d, (45, 915, 1035, 970), 16, fill=PALE_GOLD, outline=GOLD, width=1)
    d.text((65, 931), "NEXT WATCH: upcoming data / decision / event  •  SOURCE: " + str(source)[:55], font=f(15, True), fill=NAVY)
    footer(d)
    watermark(img)
    img.convert("RGB").save(path, "PNG", optimize=True)


def render_meme(title, body, path):
    img, d = base(False)
    header(img, d, "MEME", datetime.now().strftime("%d %B %Y"))
    rr(d, (45, 185, 1035, 935), 32, fill=WHITE, outline=LINE, width=2)
    # Comic/story layout, not a generic text card.
    d.text((75, 220), title.upper(), font=f(34, True), fill=GREEN)
    # Split story into panels.
    paras = [p.strip() for p in str(body).split("\n\n") if p.strip()]
    if len(paras) < 2:
        paras = str(body).split("\n")
    panel_y = 295
    for i, para in enumerate(paras[:3]):
        x1 = 75 if i % 2 == 0 else 555
        y1 = panel_y + (i // 2) * 245
        x2 = 515 if i % 2 == 0 else 1005
        y2 = y1 + 205
        rr(d, (x1, y1, x2, y2), 24, fill=CREAM if i % 2 == 0 else PALE_GREEN, outline=LINE, width=2)
        d.text((x1 + 20, y1 + 18), f"SCENE {i+1}", font=f(16, True), fill=SAFFRON)
        yy = y1 + 55
        for ln in wrap(d, para, f(25, True), x2 - x1 - 40)[:5]:
            d.text((x1 + 20, yy), ln, font=f(25, True), fill=INK)
            yy += 35
    rr(d, (75, 790, 1005, 900), 20, fill=PALE_GOLD, outline=GOLD, width=2)
    d.text((100, 815), "💡 THE FINANCE TAKEAWAY", font=f(20, True), fill=NAVY)
    d.text((100, 850), "Same market. Different mindset. Learn before you react.", font=f(23, True), fill=INK)
    footer(d)
    watermark(img)
    img.convert("RGB").save(path, "PNG", optimize=True)


def render_fixed(lane, title, body, source, path):
    lane = (lane or os.getenv("EVIDYARTHEE_LANE", "")).lower()
    if lane == "pre-market":
        render_premarket(title, body, source, path)
    elif lane == "educational":
        render_educational(title, body, source, path)
    elif lane == "post-market":
        render_postmarket(title, body, source, path)
    elif lane == "news":
        render_news(title, body, source, path)
    elif lane == "meme":
        render_meme(title, body, path)
    else:
        raise ValueError(f"Unsupported Evidyarthee lane: {lane}")


def render(title, body, source, path):
    render_fixed(os.getenv("EVIDYARTHEE_LANE", ""), title, body, source, path)
