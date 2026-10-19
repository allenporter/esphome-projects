#!/usr/bin/env python3
"""Render 8 Re-Balanced 800x480 E-Ink Panel Concepts under Rubric v4 (Balanced Household Dashboard)."""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = str(Path(__file__).resolve().parents[2] / "config" / "fonts")
BOLD_PATH = f"{FONT_DIR}/GothamRnd-Bold.ttf"
BOOK_PATH = f"{FONT_DIR}/GothamRnd-Book.ttf"
BLACK_PATH = f"{FONT_DIR}/Montserrat-Black.ttf"
MDI_PATH = f"{FONT_DIR}/materialdesignicons-webfont.ttf"

OUT_DIR = "."


def f_bold(size):
    return ImageFont.truetype(BOLD_PATH, size)


def f_book(size):
    return ImageFont.truetype(BOOK_PATH, size)


def f_black(size):
    return ImageFont.truetype(BLACK_PATH, size)


def f_mdi(size):
    return ImageFont.truetype(MDI_PATH, size)


MDI = {
    "sunny": "\U000F0599",
    "partly_cloudy": "\U000F0595",
    "cloudy": "\U000F0590",
    "rainy": "\U000F0597",
    "car": "\U000F010B",
    "waves": "\U000F078D",
    "water_percent": "\U000F058E",
}

# 3 Indoor + 3 Outdoor zones
ZONES = [
    ("Dining", "DINING", 79, 47, "IN"),
    ("Loft", "LOFT", 78, 40, "IN"),
    ("Crawlspace", "CRAWL", 80, 31, "IN"),
    ("Cabana", "CABANA", 73, 68, "OUT"),
    ("Driveway", "DRIVE", 84, 52, "OUT"),
    ("Backyard", "YARD", 87, 43, "OUT"),
]

HOURLY = [
    ("NOW", "sunny", 84),
    ("1 PM", "sunny", 84),
    ("2 PM", "sunny", 83),
    ("3 PM", "partly_cloudy", 81),
    ("4 PM", "partly_cloudy", 79),
]

FORECAST_SUMMARY = (
    "Sunny with highs in the 70s-80s through Tue. Rain expected Wed, "
    "followed by cooler, partly cloudy conditions Thu-Fri."
)


def dt(draw, x, y, text, font, fill=0, anchor="la"):
    draw.text((x, y), text, font=font, fill=fill, anchor=anchor)


def wrap_lines(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = f"{cur} {w}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, font, max_w, line_h, fill=0, max_lines=4):
    for i, line in enumerate(wrap_lines(draw, text, font, max_w)[:max_lines]):
        draw.text((x, y + i * line_h), line, font=font, fill=fill, anchor="la")


# ==============================================================================
# BAL-01: "R-P1 Balanced v2" (Exact R-P1 Proportions + 6-Zone Temp & RH Pill Table in Sidebar)
# ==============================================================================
def render_bal_01():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Left Solid Black Sidebar (x=0..256)
    d.rectangle((0, 0, 256, 480), fill=0)
    dt(d, 22, 16, "SUNDAY", f_black(24), fill=255)
    dt(d, 22, 44, "OCTOBER 18", f_book(16), fill=255)
    d.line((22, 68, 234, 68), fill=255, width=1)

    dt(d, 20, 74, "84°", f_black(72), fill=255)
    dt(d, 200, 114, MDI["sunny"], f_mdi(64), fill=255, anchor="mm")
    dt(d, 22, 160, "SUNNY • 21% RH", f_bold(16), fill=255)
    dt(d, 22, 184, "AQI 21 GOOD • UV 5.6", f_book(13), fill=255)
    d.line((22, 208, 234, 208), fill=255, width=1)

    # 6-Zone Climate Table in Sidebar (Grouped 3 Indoor + Divider + 3 Outdoor)
    dt(d, 22, 218, "CLIMATE ZONES", f_bold(12), fill=255)
    dt(d, 234, 218, "TEMP / RH", f_book(11), fill=255, anchor="ra")
    sy = 240
    for idx, (name, _, tp, rh, _) in enumerate(ZONES):
        if idx == 3:
            d.line((22, sy - 4, 234, sy - 4), fill=255, width=1)
            sy += 4
        dt(d, 22, sy + 2, name, f_book(14), fill=255)
        dt(d, 174, sy + 1, f"{tp}°", f_bold(16), fill=255, anchor="ra")
        # Crisp white pill for Humidity
        d.rounded_rectangle((182, sy, 234, sy + 22), radius=5, fill=255)
        dt(d, 208, sy + 11, f"{rh}%", f_black(13), fill=0, anchor="mm")
        sy += 38

    # Right Top (x=280..776, y=16..158): 5 Full-Size Graphical Hourly Columns
    dt(d, 280, 16, "HOURLY FORECAST", f_black(16), fill=0)
    dt(d, 776, 18, "Updated 2:40 PM", f_book(13), fill=0, anchor="ra")
    d.line((280, 40, 776, 40), fill=0, width=2)

    col_w = 496 // 5
    for i, (ts, ic, tp) in enumerate(HOURLY):
        cx = 280 + i * col_w + col_w // 2
        if i > 0:
            d.line((280 + i * col_w, 48, 280 + i * col_w, 148), fill=0, width=1)
        dt(d, cx, 48, ts, f_bold(14), fill=0, anchor="ma")
        dt(d, cx, 92, MDI[ic], f_mdi(36), fill=0, anchor="mm")
        dt(d, cx, 122, f"{tp}°F", f_black(18), fill=0, anchor="ma")

    d.line((280, 158, 776, 158), fill=0, width=2)

    # Right Middle (x=280..776, y=170..268): 5-Day Forecast Summary
    dt(d, 280, 170, "5-DAY OUTLOOK", f_black(16), fill=0)
    draw_wrapped(d, 280, 196, FORECAST_SUMMARY, f_book(16), 496, 23, fill=0, max_lines=3)
    d.line((280, 272, 776, 272), fill=0, width=2)

    # Right Bottom (x=280..776, y=288..464): 3 Full-Size R-P1 Rounded Gauge Cards
    # Card 1: Commute
    d.rounded_rectangle((280, 288, 436, 464), radius=10, outline=0, width=2)
    dt(d, 294, 302, "COMMUTE", f_bold(13), fill=0)
    dt(d, 294, 326, "9 min", f_black(24), fill=0)
    dt(d, 294, 356, "Work (Rose Ave)", f_book(13), fill=0)
    d.line((294, 380, 422, 380), fill=0, width=1)
    dt(d, 294, 390, "17 min", f_black(24), fill=0)
    dt(d, 294, 420, "WISH (Centinela)", f_book(13), fill=0)

    # Card 2: Model 3 & Softener Salt
    d.rounded_rectangle((450, 288, 606, 464), radius=10, outline=0, width=2)
    dt(d, 464, 302, "MODEL 3", f_bold(13), fill=0)
    dt(d, 464, 326, "79%", f_black(26), fill=0)
    dt(d, 592, 334, "202 mi", f_bold(14), fill=0, anchor="ra")
    d.rectangle((464, 362, 592, 374), outline=0, width=2)
    d.rectangle((466, 364, 466 + int(124 * 0.79), 372), fill=0)
    dt(d, 464, 392, "SOFTENER", f_bold(12), fill=0)
    dt(d, 592, 392, "63%", f_bold(14), fill=0, anchor="ra")
    d.rectangle((464, 416, 592, 428), outline=0, width=2)
    d.rectangle((466, 418, 466 + int(124 * 0.63), 426), fill=0)

    # Card 3: Santa Monica Tides
    d.rounded_rectangle((620, 288, 776, 464), radius=10, outline=0, width=2)
    dt(d, 634, 302, "SANTA MONICA", f_bold(13), fill=0)
    dt(d, 634, 326, "3:29 PM", f_black(22), fill=0)
    dt(d, 634, 354, "High Tide", f_book(13), fill=0)
    # Mini sine wave inside card
    wpts = []
    for px in range(634, 762, 4):
        t = (px - 634) / 128.0
        py = 398 - int(12 * math.sin((t - 0.05) * 1.8 * math.pi))
        wpts.append((px, py))
    d.line(wpts, fill=0, width=2)
    dt(d, 634, 426, "Low: 11:38 PM", f_bold(13), fill=0)

    img.save(f"{OUT_DIR}/bal_01.png")


# ==============================================================================
# BAL-02: "R-P1 + 4-Tier Right Deck" (Sidebar has Weather + Tide Wave + Salt; Right has 6-Zone Ribbon)
# ==============================================================================
def render_bal_02():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Left Solid Black Sidebar (x=0..256): Weather + Santa Monica Tide Wave + Softener Salt
    d.rectangle((0, 0, 256, 480), fill=0)
    dt(d, 22, 16, "SUNDAY", f_black(24), fill=255)
    dt(d, 22, 44, "OCTOBER 18", f_book(16), fill=255)
    d.line((22, 68, 234, 68), fill=255, width=1)

    dt(d, 20, 76, "84°", f_black(72), fill=255)
    dt(d, 200, 116, MDI["sunny"], f_mdi(64), fill=255, anchor="mm")
    dt(d, 22, 164, "SUNNY • 21% OUT RH", f_bold(15), fill=255)
    dt(d, 22, 188, "AQI 21 GOOD • UV 5.6 • 6 mph", f_book(13), fill=255)
    d.line((22, 214, 234, 214), fill=255, width=1)

    # 5-Day Outlook in Sidebar
    dt(d, 22, 226, "5-DAY OUTLOOK", f_bold(13), fill=255)
    draw_wrapped(d, 22, 248, FORECAST_SUMMARY, f_book(14), 212, 19, fill=255, max_lines=5)
    d.line((22, 352, 234, 352), fill=255, width=1)

    # Santa Monica Tide Curve in Sidebar
    dt(d, 22, 364, "SANTA MONICA TIDES", f_bold(13), fill=255)
    wpts = []
    for px in range(24, 232, 4):
        t = (px - 24) / 208.0
        py = 414 - int(14 * math.sin((t - 0.08) * 1.8 * math.pi))
        wpts.append((px, py))
    d.line(wpts, fill=255, width=2)
    hx, hy = wpts[16]
    d.ellipse((hx - 4, hy - 4, hx + 4, hy + 4), fill=255)
    dt(d, 22, 444, "HI 3:29 PM  •  LO 11:38 PM", f_bold(13), fill=255)

    # Right Tier 1 (y=14..136): 5 Hourly Graphical Columns
    dt(d, 280, 14, "HOURLY FORECAST", f_black(15), fill=0)
    dt(d, 776, 16, "Updated 2:40 PM", f_book(12), fill=0, anchor="ra")
    d.line((280, 36, 776, 36), fill=0, width=2)
    col_w = 496 // 5
    for i, (ts, ic, tp) in enumerate(HOURLY):
        cx = 280 + i * col_w + col_w // 2
        if i > 0:
            d.line((280 + i * col_w, 42, 280 + i * col_w, 128), fill=0, width=1)
        dt(d, cx, 42, ts, f_bold(13), fill=0, anchor="ma")
        dt(d, cx, 80, MDI[ic], f_mdi(32), fill=0, anchor="mm")
        dt(d, cx, 106, f"{tp}°F", f_black(17), fill=0, anchor="ma")
    d.line((280, 136, 776, 136), fill=0, width=2)

    # Right Tier 2 (y=148..296): 6-Zone Co-Equal Temp & Humidity Strip (3 Indoor + 3 Outdoor)
    dt(d, 280, 148, "CLIMATE ZONES (TEMP + RH%)", f_black(15), fill=0)
    dt(d, 776, 150, "INDOOR (3)  |  OUTDOOR (3)", f_book(12), fill=0, anchor="ra")

    zw = 496 // 6  # 82px per zone
    for i, (_, caps, tp, rh, kind) in enumerate(ZONES):
        zx = 280 + i * zw
        cx = zx + zw // 2
        d.rounded_rectangle((zx + 3, 174, zx + zw - 3, 288), radius=8, outline=0, width=2)
        if kind == "IN":
            d.rounded_rectangle((zx + 3, 174, zx + zw - 3, 198), radius=8, fill=0)
            d.rectangle((zx + 3, 188, zx + zw - 3, 198), fill=0)
            dt(d, cx, 180, caps, f_bold(11), fill=255, anchor="ma")
        else:
            d.line((zx + 3, 198, zx + zw - 3, 198), fill=0, width=1)
            dt(d, cx, 180, caps, f_bold(11), fill=0, anchor="ma")

        dt(d, cx, 206, f"{tp}°", f_black(22), fill=0, anchor="ma")
        dt(d, cx, 238, f"{rh}%", f_bold(16), fill=0, anchor="ma")
        # Mini RH bar with 40-60% ticks
        bx, by, bw = zx + 10, 266, zw - 20
        d.rectangle((bx, by, bx + bw, by + 10), outline=0, width=1)
        d.rectangle((bx + 1, by + 1, bx + 1 + int((bw - 2) * (rh / 100.0)), by + 9), fill=0)

    d.line((280, 302, 776, 302), fill=0, width=2)

    # Right Tier 3 (y=316..464): 3 Large Rounded Telemetry Cards (Work, WISH, Model 3 + Salt)
    cards = [
        ("TO WORK", "9 MIN", "via Rose Ave"),
        ("TO WISH", "17 MIN", "via S Centinela"),
        ("MODEL 3 & SALT", "79%", "202 mi • Salt 63%"),
    ]
    for i, (ct, cv, cs) in enumerate(cards):
        bx = 280 + i * 170
        d.rounded_rectangle((bx, 316, bx + 156, 464), radius=10, outline=0, width=2)
        dt(d, bx + 14, 332, ct, f_bold(13), fill=0)
        dt(d, bx + 14, 364, cv, f_black(26), fill=0)
        dt(d, bx + 14, 416, cs, f_book(13), fill=0)

    img.save(f"{OUT_DIR}/bal_02.png")


# ==============================================================================
# BAL-03: "Dieter Rams / Braun Balanced 4-Quadrant Grid"
# ==============================================================================
def render_bal_03():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Top Masthead (y=0..46)
    dt(d, 24, 16, "SUNDAY, OCTOBER 18", f_black(22), fill=0)
    dt(d, 776, 18, "AQI 21 GOOD  •  UV 5.6  •  WIND 6 MPH", f_bold(14), fill=0, anchor="ra")
    d.line((24, 46, 776, 46), fill=0, width=3)

    # Center Crosshair Dividers (x=392, y=262)
    d.line((392, 46, 392, 468), fill=0, width=2)
    d.line((24, 262, 776, 262), fill=0, width=2)

    # Q1 (Top-Left, x=24..376, y=56..252): Current Weather + 5-Day Summary
    dt(d, 24, 58, "84°F", f_black(60), fill=0)
    dt(d, 236, 92, MDI["sunny"], f_mdi(60), fill=0, anchor="mm")
    dt(d, 24, 130, "Sunny  •  21% Outside RH", f_bold(16), fill=0)
    d.line((24, 158, 372, 158), fill=0, width=1)
    draw_wrapped(d, 24, 168, FORECAST_SUMMARY, f_book(15), 348, 21, fill=0, max_lines=4)

    # Q2 (Top-Right, x=412..776, y=56..252): 5 Hourly Columns + Santa Monica Tides Strip
    dt(d, 412, 58, "HOURLY FORECAST", f_bold(14), fill=0)
    cw = 364 // 5
    for i, (ts, ic, tp) in enumerate(HOURLY):
        cx = 412 + i * cw + cw // 2
        if i > 0:
            d.line((412 + i * cw, 82, 412 + i * cw, 174), fill=0, width=1)
        dt(d, cx, 82, ts, f_book(13), fill=0, anchor="ma")
        dt(d, cx, 120, MDI[ic], f_mdi(32), fill=0, anchor="mm")
        dt(d, cx, 148, f"{tp}°F", f_black(17), fill=0, anchor="ma")

    d.line((412, 186, 776, 186), fill=0, width=1)
    dt(d, 412, 198, "SANTA MONICA TIDES", f_bold(13), fill=0)
    dt(d, 412, 222, "High: 3:29 PM", f_black(17), fill=0)
    dt(d, 610, 224, "Low: 11:38 PM", f_bold(16), fill=0)

    # Q3 (Bottom-Left, x=24..376, y=274..468): 6-Zone Climate Matrix (3x2 Co-Equal Temp + RH)
    dt(d, 24, 274, "CLIMATE ZONES (INDOOR / OUTDOOR)", f_bold(14), fill=0)
    zw, zh = 116, 82
    for idx, (_, caps, tp, rh, kind) in enumerate(ZONES):
        col = idx % 3
        row = idx // 3
        zx = 24 + col * zw
        zy = 300 + row * zh
        if col > 0:
            d.line((zx, zy + 4, zx, zy + zh - 6), fill=0, width=1)
        if row > 0:
            d.line((24, zy, 372, zy), fill=0, width=1)
        dt(d, zx + 8, zy + 6, f"{caps} ({kind})", f_bold(11) if kind == "IN" else f_book(11), fill=0)
        dt(d, zx + 8, zy + 24, f"{tp}°", f_black(22), fill=0)
        dt(d, zx + 64, zy + 28, f"{rh}%", f_bold(16), fill=0)
        # Mini comfort bar
        bx, by, bw = zx + 8, zy + 58, zw - 18
        d.rectangle((bx, by, bx + bw, by + 8), outline=0, width=1)
        d.rectangle((bx + 1, by + 1, bx + 1 + int((bw - 2) * (rh / 100.0)), by + 7), fill=0)

    # Q4 (Bottom-Right, x=412..776, y=274..468): Commute + Model 3 + Softener Salt
    dt(d, 412, 274, "COMMUTE & HOUSEHOLD SYSTEMS", f_bold(14), fill=0)
    dt(d, 412, 304, "To Work (Rose Ave)", f_book(15), fill=0)
    dt(d, 776, 298, "9 MIN", f_black(22), fill=0, anchor="ra")
    dt(d, 412, 336, "To WISH (Centinela)", f_book(15), fill=0)
    dt(d, 776, 330, "17 MIN", f_black(22), fill=0, anchor="ra")
    d.line((412, 366, 776, 366), fill=0, width=1)

    dt(d, 412, 378, "Tesla Model 3", f_bold(15), fill=0)
    dt(d, 776, 378, "79% • 202 mi", f_bold(15), fill=0, anchor="ra")
    d.rectangle((412, 402, 776, 414), outline=0, width=2)
    d.rectangle((414, 404, 414 + int(360 * 0.79), 412), fill=0)

    dt(d, 412, 426, "Softener Salt", f_bold(15), fill=0)
    dt(d, 776, 426, "63%", f_bold(15), fill=0, anchor="ra")
    d.rectangle((412, 450, 776, 462), outline=0, width=2)
    d.rectangle((414, 452, 414 + int(360 * 0.63), 460), fill=0)

    img.save(f"{OUT_DIR}/bal_03.png")


# ==============================================================================
# BAL-04: "Swiss Asymmetric Top-Banner + 3 Equal Columns"
# ==============================================================================
def render_bal_04():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Full-width Top Black Weather & Hourly Banner (y=0..146)
    d.rectangle((0, 0, 800, 146), fill=0)
    dt(d, 24, 16, "SUNDAY, OCT 18", f_black(20), fill=255)
    dt(d, 24, 44, "84°F", f_black(62), fill=255)
    dt(d, 218, 76, MDI["sunny"], f_mdi(56), fill=255, anchor="mm")
    dt(d, 24, 116, "SUNNY • 21% RH • AQI 21 • UV 5.6", f_bold(13), fill=255)

    d.line((296, 16, 296, 130), fill=255, width=1)
    cw = 480 // 5
    for i, (ts, ic, tp) in enumerate(HOURLY):
        cx = 304 + i * cw + cw // 2
        if i > 0:
            d.line((304 + i * cw, 22, 304 + i * cw, 126), fill=255, width=1)
        dt(d, cx, 22, ts, f_bold(13), fill=255, anchor="ma")
        dt(d, cx, 68, MDI[ic], f_mdi(34), fill=255, anchor="mm")
        dt(d, cx, 102, f"{tp}°F", f_black(18), fill=255, anchor="ma")

    # Middle Strip (y=156..212): Full-width 5-Day Forecast Summary
    dt(d, 24, 160, "5-DAY OUTLOOK", f_black(14), fill=0)
    draw_wrapped(d, 176, 158, FORECAST_SUMMARY, f_book(15), 600, 21, fill=0, max_lines=2)
    d.line((24, 210, 776, 210), fill=0, width=2)

    # Bottom 3 Equal Rounded Cards (y=222..466)
    # Card 1 (x=24..262): Commute & Santa Monica Tides
    d.rounded_rectangle((24, 222, 262, 466), radius=10, outline=0, width=2)
    dt(d, 40, 236, "COMMUTE & TIDES", f_black(14), fill=0)
    dt(d, 40, 266, "Work (Rose Ave)", f_book(14), fill=0)
    dt(d, 246, 262, "9m", f_black(22), fill=0, anchor="ra")
    dt(d, 40, 300, "WISH (Centinela)", f_book(14), fill=0)
    dt(d, 246, 296, "17m", f_black(22), fill=0, anchor="ra")
    d.line((40, 332, 246, 332), fill=0, width=1)
    dt(d, 40, 344, "SANTA MONICA TIDES", f_bold(12), fill=0)
    wpts = []
    for px in range(40, 246, 4):
        t = (px - 40) / 206.0
        py = 394 - int(14 * math.sin((t - 0.08) * 1.8 * math.pi))
        wpts.append((px, py))
    d.line(wpts, fill=0, width=2)
    dt(d, 40, 432, "HI 3:29P  •  LO 11:38P", f_bold(14), fill=0)

    # Card 2 (x=278..516): Tesla Model 3 & Softener Salt
    d.rounded_rectangle((278, 222, 516, 466), radius=10, outline=0, width=2)
    dt(d, 294, 236, "MODEL 3 & SYSTEMS", f_black(14), fill=0)
    dt(d, 294, 268, "79%", f_black(36), fill=0)
    dt(d, 500, 280, "202 MI RANGE", f_bold(14), fill=0, anchor="ra")
    d.rectangle((294, 318, 500, 336), outline=0, width=2)
    d.rectangle((296, 320, 296 + int(202 * 0.79), 334), fill=0)
    d.line((294, 356, 500, 356), fill=0, width=1)
    dt(d, 294, 370, "SOFTENER SALT", f_bold(13), fill=0)
    dt(d, 294, 394, "63%", f_black(26), fill=0)
    d.rectangle((294, 430, 500, 446), outline=0, width=2)
    d.rectangle((296, 432, 296 + int(202 * 0.63), 444), fill=0)

    # Card 3 (x=532..776): 6-Zone Temp & Humidity Table
    d.rounded_rectangle((532, 222, 776, 466), radius=10, outline=0, width=2)
    dt(d, 548, 236, "CLIMATE (TEMP / RH)", f_black(14), fill=0)
    sy = 266
    for idx, (name, _, tp, rh, kind) in enumerate(ZONES):
        if idx == 3:
            d.line((548, sy - 3, 760, sy - 3), fill=0, width=1)
            sy += 3
        dt(d, 548, sy + 2, name, f_bold(14) if kind == "IN" else f_book(14), fill=0)
        dt(d, 696, sy + 1, f"{tp}°F", f_bold(15), fill=0, anchor="ra")
        d.rounded_rectangle((706, sy, 760, sy + 22), radius=5, fill=0 if kind == "IN" else 255, outline=0, width=1)
        dt(d, 733, sy + 11, f"{rh}%", f_bold(13), fill=255 if kind == "IN" else 0, anchor="mm")
        sy += 32

    img.save(f"{OUT_DIR}/bal_04.png")


# ==============================================================================
# BAL-05: "Vignelli Transit & Climate Board (Balanced Horizontal Bands)"
# ==============================================================================
def render_bal_05():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Top Header Bar
    dt(d, 24, 14, "SUNDAY, OCTOBER 18", f_black(22), fill=0)
    dt(d, 776, 16, "AQI 21 GOOD  •  UV 5.6  •  WIND 6 MPH", f_bold(14), fill=0, anchor="ra")
    d.line((24, 44, 776, 44), fill=0, width=3)

    # Upper Band (y=52..204): Weather Hero (Left) + 5 Hourly Columns (Right) + 5-Day Summary Strip
    dt(d, 24, 54, "84°F", f_black(56), fill=0)
    dt(d, 216, 84, MDI["sunny"], f_mdi(56), fill=0, anchor="mm")
    dt(d, 24, 120, "Sunny • 21% Outside RH", f_bold(15), fill=0)

    d.line((272, 54, 272, 144), fill=0, width=2)
    cw = 500 // 5
    for i, (ts, ic, tp) in enumerate(HOURLY):
        cx = 276 + i * cw + cw // 2
        if i > 0:
            d.line((276 + i * cw, 58, 276 + i * cw, 140), fill=0, width=1)
        dt(d, cx, 58, ts, f_bold(13), fill=0, anchor="ma")
        dt(d, cx, 94, MDI[ic], f_mdi(30), fill=0, anchor="mm")
        dt(d, cx, 120, f"{tp}°F", f_black(17), fill=0, anchor="ma")

    d.line((24, 150, 776, 150), fill=0, width=1)
    draw_wrapped(d, 24, 158, FORECAST_SUMMARY, f_book(15), 752, 20, fill=0, max_lines=2)

    # Middle Band (y=208..324): Full-Bleed Black Ribbon with 6 Co-Equal Temp + RH Cards
    d.rectangle((0, 208, 800, 324), fill=0)
    zw = 752 // 6
    for i, (_, caps, tp, rh, kind) in enumerate(ZONES):
        zx = 24 + i * zw
        d.rounded_rectangle((zx + 4, 218, zx + zw - 4, 314), radius=8, fill=255)
        cx = zx + zw // 2
        dt(d, cx, 226, f"{caps} • {kind}", f_bold(11), fill=0, anchor="ma")
        dt(d, cx, 246, f"{tp}°F", f_black(22), fill=0, anchor="ma")
        d.rounded_rectangle((cx - 34, 278, cx + 34, 304), radius=5, fill=0)
        dt(d, cx, 291, f"{rh}% RH", f_bold(13), fill=255, anchor="mm")

    # Bottom Band (y=336..468): 4 Vignelli Subway-Badge Telemetry Columns
    items = [
        ("W", "WORK", "9 MIN", "via Rose Ave"),
        ("S", "WISH", "17 MIN", "via S Centinela"),
        ("3", "MODEL 3", "79%", "202 mi • Salt 63%"),
        ("T", "HIGH TIDE", "3:29P", "Low Tide 11:38 PM"),
    ]
    iw = 752 // 4
    for i, (badge, title, big, sub) in enumerate(items):
        ix = 24 + i * iw
        if i > 0:
            d.line((ix - 10, 342, ix - 10, 464), fill=0, width=2)
        d.ellipse((ix, 344, ix + 34, 378), fill=0)
        dt(d, ix + 17, 361, badge, f_black(17), fill=255, anchor="mm")
        dt(d, ix + 44, 352, title, f_bold(15), fill=0)
        dt(d, ix, 390, big, f_black(28), fill=0)
        dt(d, ix, 434, sub, f_book(14), fill=0)

    img.save(f"{OUT_DIR}/bal_05.png")


# ==============================================================================
# BAL-06: "Marine / Santa Monica Coastal Dashboard (Balanced)"
# ==============================================================================
def render_bal_06():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Left Solid Black Sidebar (x=0..256): Weather + Tide Curve + Softener
    d.rectangle((0, 0, 256, 480), fill=0)
    dt(d, 22, 16, "SUNDAY", f_black(24), fill=255)
    dt(d, 22, 44, "OCTOBER 18", f_book(16), fill=255)
    d.line((22, 68, 234, 68), fill=255, width=1)

    dt(d, 20, 76, "84°", f_black(72), fill=255)
    dt(d, 200, 116, MDI["sunny"], f_mdi(64), fill=255, anchor="mm")
    dt(d, 22, 162, "SUNNY • 21% OUT RH", f_bold(15), fill=255)
    dt(d, 22, 186, "AQI 21 GOOD • UV 5.6", f_book(13), fill=255)
    d.line((22, 212, 234, 212), fill=255, width=1)

    # Santa Monica Sine Tide Wave in Sidebar
    dt(d, 22, 224, "SANTA MONICA TIDES", f_bold(13), fill=255)
    wpts = []
    for px in range(24, 232, 4):
        t = (px - 24) / 208.0
        py = 278 - int(16 * math.sin((t - 0.08) * 1.8 * math.pi))
        wpts.append((px, py))
    d.line(wpts, fill=255, width=3)
    hx, hy = wpts[16]
    lx, ly = wpts[44]
    d.ellipse((hx - 5, hy - 5, hx + 5, hy + 5), fill=255)
    d.ellipse((lx - 4, ly - 4, lx + 4, ly + 4), fill=0, outline=255, width=2)
    dt(d, 22, 310, "HI 3:29 PM", f_bold(14), fill=255)
    dt(d, 234, 310, "LO 11:38 PM", f_book(13), fill=255, anchor="ra")
    d.line((22, 338, 234, 338), fill=255, width=1)

    # Commute & EV in lower sidebar
    dt(d, 22, 350, "WORK (ROSE AVE)", f_book(13), fill=255)
    dt(d, 234, 348, "9 MIN", f_black(17), fill=255, anchor="ra")
    dt(d, 22, 380, "WISH (CENTINELA)", f_book(13), fill=255)
    dt(d, 234, 378, "17 MIN", f_black(17), fill=255, anchor="ra")
    dt(d, 22, 412, "MODEL 3 (202 MI)", f_book(13), fill=255)
    dt(d, 234, 410, "79%", f_black(17), fill=255, anchor="ra")
    dt(d, 22, 442, "SOFTENER SALT", f_book(13), fill=255)
    dt(d, 234, 440, "63%", f_bold(16), fill=255, anchor="ra")

    # Right Top (y=16..150): 5 Hourly Columns
    dt(d, 280, 16, "HOURLY FORECAST", f_black(16), fill=0)
    dt(d, 776, 18, "Wind 6 mph • UV 5.6", f_book(13), fill=0, anchor="ra")
    d.line((280, 40, 776, 40), fill=0, width=2)
    col_w = 496 // 5
    for i, (ts, ic, tp) in enumerate(HOURLY):
        cx = 280 + i * col_w + col_w // 2
        if i > 0:
            d.line((280 + i * col_w, 48, 280 + i * col_w, 140), fill=0, width=1)
        dt(d, cx, 48, ts, f_bold(14), fill=0, anchor="ma")
        dt(d, cx, 88, MDI[ic], f_mdi(34), fill=0, anchor="mm")
        dt(d, cx, 118, f"{tp}°F", f_black(18), fill=0, anchor="ma")
    d.line((280, 150, 776, 150), fill=0, width=2)

    # Right Middle (y=162..246): 5-Day Forecast Summary
    dt(d, 280, 162, "5-DAY OUTLOOK", f_black(15), fill=0)
    draw_wrapped(d, 280, 186, FORECAST_SUMMARY, f_book(15), 496, 21, fill=0, max_lines=3)
    d.line((280, 254, 776, 254), fill=0, width=2)

    # Right Bottom (y=266..466): 3x2 Co-Equal Temp + Braun Arc Cards
    cw, ch = 165, 100
    for idx, (_, caps, tp, rh, kind) in enumerate(ZONES):
        col = idx % 3
        row = idx // 3
        x0 = 280 + col * cw
        y0 = 266 + row * ch
        if col > 0:
            d.line((x0, y0 + 6, x0, y0 + ch - 6), fill=0, width=1)
        if row > 0:
            d.line((280, y0, 776, y0), fill=0, width=1)
        dt(d, x0 + 12, y0 + 10, f"{caps} ({kind})", f_bold(12) if kind == "IN" else f_book(12), fill=0)
        dt(d, x0 + 12, y0 + 32, f"{tp}°F", f_black(24), fill=0)
        dt(d, x0 + 12, y0 + 66, f"{rh}% RH", f_bold(15), fill=0)
        # Compact circular dial on the right side of each cell
        dcx, dcy, dr = x0 + 126, y0 + 52, 26
        d.arc((dcx - dr, dcy - dr, dcx + dr, dcy + dr), start=135, end=405, fill=0, width=2)
        ang = 135 + int(270 * (rh / 100.0))
        d.arc((dcx - dr, dcy - dr, dcx + dr, dcy + dr), start=135, end=ang, fill=0, width=6)

    img.save(f"{OUT_DIR}/bal_06.png")


# ==============================================================================
# BAL-07: "Tufte High-Craft 3-Column Editorial Dashboard"
# ==============================================================================
def render_bal_07():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Top Masthead
    dt(d, 24, 16, "SUNDAY, OCTOBER 18", f_black(22), fill=0)
    dt(d, 776, 18, "WOODGREEN HOUSEHOLD TELEMETRY  •  UPDATED 2:40 PM", f_book(13), fill=0, anchor="ra")
    d.line((24, 46, 776, 46), fill=0, width=2)

    # Col 1 (x=24..260): Weather + Hourly Sparkline + 5-Day Summary
    dt(d, 24, 58, "84°F", f_black(54), fill=0)
    dt(d, 218, 86, MDI["sunny"], f_mdi(54), fill=0, anchor="mm")
    dt(d, 24, 120, "Sunny • 21% RH • Wind 6 mph", f_bold(14), fill=0)
    dt(d, 24, 142, "AQI 21 Good  •  UV Index 5.6", f_book(13), fill=0)
    d.line((24, 168, 256, 168), fill=0, width=1)

    dt(d, 24, 178, "HOURLY TRAJECTORY", f_bold(13), fill=0)
    pts = [("Now", 84), ("1p", 84), ("2p", 83), ("3p", 81), ("4p", 79)]
    xs = [38 + i * 50 for i in range(len(pts))]
    ys = [int(242 - ((t - 78) / 7.0) * 30) for _, t in pts]
    for i in range(len(pts) - 1):
        d.line((xs[i], ys[i], xs[i + 1], ys[i + 1]), fill=0, width=2)
    for i, (lbl, t) in enumerate(pts):
        d.ellipse((xs[i] - 3, ys[i] - 3, xs[i] + 3, ys[i] + 3), fill=0)
        dt(d, xs[i], ys[i] - 14, f"{t}°", f_bold(12), fill=0, anchor="mm")
        dt(d, xs[i], 256, lbl, f_book(12), fill=0, anchor="mm")

    d.line((24, 280, 256, 280), fill=0, width=1)
    dt(d, 24, 292, "5-DAY OUTLOOK", f_bold(13), fill=0)
    draw_wrapped(d, 24, 314, FORECAST_SUMMARY, f_book(14), 232, 20, fill=0, max_lines=6)

    d.line((272, 58, 272, 464), fill=0, width=1)

    # Col 2 (x=288..524): 6-Zone Temp & Humidity Table with Tufte Dot-Scale
    dt(d, 288, 58, "PROPERTY CLIMATE (6 ZONES)", f_bold(14), fill=0)
    dt(d, 288, 80, "Zone", f_book(12), fill=0)
    dt(d, 404, 80, "Temp", f_book(12), fill=0, anchor="ra")
    dt(d, 520, 80, "RH (40-60%)", f_book(12), fill=0, anchor="ra")
    d.line((288, 98, 520, 98), fill=0, width=1)

    sy = 112
    for idx, (name, _, tp, rh, kind) in enumerate(ZONES):
        if idx == 3:
            d.line((288, sy - 6, 520, sy - 6), fill=0, width=1)
            sy += 6
        short_name = "Crawl" if name == "Crawlspace" else name
        dt(d, 288, sy, short_name, f_bold(15) if kind == "IN" else f_book(15), fill=0)
        dt(d, 404, sy, f"{tp}°F", f_black(16), fill=0, anchor="ra")
        dt(d, 458, sy, f"{rh}%", f_bold(15), fill=0, anchor="ra")
        # Mini Tufte dot scale (x=468..520)
        d.line((468, sy + 9, 520, sy + 9), fill=0, width=1)
        # 40% & 60% ticks
        d.line((468 + int(52 * 0.4), sy + 5, 468 + int(52 * 0.4), sy + 13), fill=0, width=1)
        d.line((468 + int(52 * 0.6), sy + 5, 468 + int(52 * 0.6), sy + 13), fill=0, width=1)
        px = 468 + int(52 * (rh / 100.0))
        d.ellipse((px - 4, sy + 5, px + 4, sy + 13), fill=0)
        sy += 54

    d.line((536, 58, 536, 464), fill=0, width=1)

    # Col 3 (x=552..776): Commute, Model 3, Softener, Santa Monica Tides
    dt(d, 552, 58, "COMMUTE & LOGISTICS", f_bold(14), fill=0)
    dt(d, 552, 88, "Work (Rose Ave)", f_book(15), fill=0)
    dt(d, 776, 82, "9 min", f_black(22), fill=0, anchor="ra")
    dt(d, 552, 124, "WISH (Centinela)", f_book(15), fill=0)
    dt(d, 776, 118, "17 min", f_black(22), fill=0, anchor="ra")
    d.line((552, 156, 776, 156), fill=0, width=1)

    dt(d, 552, 170, "TESLA MODEL 3", f_bold(14), fill=0)
    dt(d, 552, 194, "79%  •  202 mi", f_black(20), fill=0)
    d.rectangle((552, 224, 776, 236), outline=0, width=2)
    d.rectangle((554, 226, 554 + int(220 * 0.79), 234), fill=0)

    dt(d, 552, 254, "SOFTENER SALT", f_bold(14), fill=0)
    dt(d, 776, 254, "63%", f_black(18), fill=0, anchor="ra")
    d.rectangle((552, 280, 776, 292), outline=0, width=2)
    d.rectangle((554, 282, 554 + int(220 * 0.63), 290), fill=0)
    d.line((552, 312, 776, 312), fill=0, width=1)

    dt(d, 552, 326, "SANTA MONICA TIDES", f_bold(14), fill=0)
    wpts = []
    for px in range(552, 776, 4):
        t = (px - 552) / 224.0
        py = 384 - int(18 * math.sin((t - 0.08) * 1.8 * math.pi))
        wpts.append((px, py))
    d.line(wpts, fill=0, width=2)
    hx, hy = wpts[18]
    d.ellipse((hx - 4, hy - 4, hx + 4, hy + 4), fill=0)
    dt(d, 552, 420, "High Tide: 3:29 PM", f_bold(15), fill=0)
    dt(d, 552, 444, "Low Tide: 11:38 PM", f_book(14), fill=0)

    img.save(f"{OUT_DIR}/bal_07.png")


# ==============================================================================
# BAL-08: "Teenage Engineering Modular Bento (5 Balanced Bento Tiles)"
# ==============================================================================
def render_bal_08():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Top Technical Bar
    d.rectangle((0, 0, 800, 40), fill=0)
    dt(d, 20, 11, "WOODGREEN PANEL // SUN OCT 18", f_black(16), fill=255)
    dt(d, 780, 12, "AQI 21 GOOD • UV 5.6 • WIND 6 MPH", f_bold(13), fill=255, anchor="ra")

    # Bento 1 (Top-Left, x=16..272, y=52..268, Solid Black): Weather Hero + 5-Day Summary
    d.rounded_rectangle((16, 52, 272, 268), radius=10, fill=0)
    dt(d, 34, 64, "84°F", f_black(58), fill=255)
    dt(d, 224, 96, MDI["sunny"], f_mdi(54), fill=255, anchor="mm")
    dt(d, 34, 130, "SUNNY • 21% OUT RH", f_bold(14), fill=255)
    d.line((34, 154, 254, 154), fill=255, width=1)
    draw_wrapped(d, 34, 164, FORECAST_SUMMARY, f_book(13), 220, 18, fill=255, max_lines=5)

    # Bento 2 (Bottom-Left, x=16..272, y=280..466): Commute & Santa Monica Tides
    d.rounded_rectangle((16, 280, 272, 466), radius=10, outline=0, width=2)
    dt(d, 34, 294, "COMMUTE & TIDES", f_black(14), fill=0)
    dt(d, 34, 322, "TO WORK", f_book(13), fill=0)
    dt(d, 254, 318, "9 MIN", f_black(20), fill=0, anchor="ra")
    dt(d, 34, 352, "TO WISH", f_book(13), fill=0)
    dt(d, 254, 348, "17 MIN", f_black(20), fill=0, anchor="ra")
    d.line((34, 380, 254, 380), fill=0, width=1)
    dt(d, 34, 392, "HIGH TIDE", f_book(13), fill=0)
    dt(d, 254, 390, "3:29 PM", f_bold(16), fill=0, anchor="ra")
    dt(d, 34, 422, "LOW TIDE", f_book(13), fill=0)
    dt(d, 254, 422, "11:38 PM", f_book(15), fill=0, anchor="ra")

    # Bento 3 (Top-Right, x=284..784, y=52..178): 5 Hourly Columns
    d.rounded_rectangle((284, 52, 784, 178), radius=10, outline=0, width=2)
    cw = 500 // 5
    for i, (ts, ic, tp) in enumerate(HOURLY):
        cx = 284 + i * cw + cw // 2
        if i > 0:
            d.line((284 + i * cw, 64, 284 + i * cw, 166), fill=0, width=1)
        dt(d, cx, 64, ts, f_bold(13), fill=0, anchor="ma")
        dt(d, cx, 106, MDI[ic], f_mdi(32), fill=0, anchor="mm")
        dt(d, cx, 138, f"{tp}°F", f_black(18), fill=0, anchor="ma")

    # Bento 4 (Mid-Right, x=284..784, y=190..352): 6-Zone Temp & Segmented Humidity Grid
    d.rounded_rectangle((284, 190, 784, 352), radius=10, outline=0, width=2)
    zw, zh = 500 // 3, 81
    for idx, (_, caps, tp, rh, kind) in enumerate(ZONES):
        col = idx % 3
        row = idx // 3
        zx = 284 + col * zw
        zy = 190 + row * zh
        if col > 0:
            d.line((zx, zy + 8, zx, zy + zh - 8), fill=0, width=1)
        if row > 0:
            d.line((294, zy, 774, zy), fill=0, width=1)
        dt(d, zx + 14, zy + 10, f"{caps} • {kind}", f_bold(12) if kind == "IN" else f_book(12), fill=0)
        dt(d, zx + 14, zy + 30, f"{tp}°F", f_black(20), fill=0)
        dt(d, zx + zw - 14, zy + 32, f"{rh}%", f_bold(16), fill=0, anchor="ra")
        # 5-segment mini bar
        active = round((rh / 100.0) * 5)
        for s in range(5):
            sx = zx + 14 + s * 26
            if s < active:
                d.rectangle((sx, zy + 58, sx + 22, zy + 68), fill=0)
            else:
                d.rectangle((sx, zy + 58, sx + 22, zy + 68), outline=0, width=1)

    # Bento 5 (Bottom-Right, x=284..784, y=364..466): Model 3 & Softener Salt Module
    d.rounded_rectangle((284, 364, 784, 466), radius=10, outline=0, width=2)
    dt(d, 302, 378, "TESLA MODEL 3", f_black(14), fill=0)
    dt(d, 302, 404, "79%", f_black(28), fill=0)
    dt(d, 410, 412, "202 MI", f_bold(15), fill=0)
    d.rectangle((302, 440, 516, 452), outline=0, width=2)
    d.rectangle((304, 442, 304 + int(210 * 0.79), 450), fill=0)

    d.line((536, 376, 536, 454), fill=0, width=1)
    dt(d, 554, 378, "SOFTENER SALT", f_black(14), fill=0)
    dt(d, 554, 404, "63%", f_black(28), fill=0)
    d.rectangle((554, 440, 766, 452), outline=0, width=2)
    d.rectangle((556, 442, 556 + int(208 * 0.63), 450), fill=0)

    img.save(f"{OUT_DIR}/bal_08.png")


if __name__ == "__main__":
    render_bal_01()
    render_bal_02()
    render_bal_03()
    render_bal_04()
    render_bal_05()
    render_bal_06()
    render_bal_07()
    render_bal_08()
    print("Rendered all 8 Balanced Dashboard Concepts (bal_01 .. bal_08)!")
