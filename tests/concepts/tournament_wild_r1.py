#!/usr/bin/env python3
"""Wild Tournament Round 1: 10 Radically Different Themes, Fonts & Visual Metaphors (800x480)."""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = str(Path(__file__).resolve().parents[2] / "config" / "fonts")
DL_FONT_DIR = FONT_DIR
OUT_DIR = "."


def f_bebas(size):
    return ImageFont.truetype(f"{DL_FONT_DIR}/BebasNeue-Regular.ttf", size)


def f_mono(size):
    return ImageFont.truetype(f"{DL_FONT_DIR}/ShareTechMono-Regular.ttf", size)


def f_spacemono(size, bold=False):
    p = "SpaceMono-Bold.ttf" if bold else "SpaceMono-Regular.ttf"
    return ImageFont.truetype(f"{DL_FONT_DIR}/{p}", size)


def f_serif(size, italic=False):
    p = "DMSerifDisplay-Italic.ttf" if italic else "DMSerifDisplay-Regular.ttf"
    return ImageFont.truetype(f"{DL_FONT_DIR}/{p}", size)


def f_vt(size):
    return ImageFont.truetype(f"{DL_FONT_DIR}/VT323-Regular.ttf", size)


def f_chakra(size, bold=True):
    p = "ChakraPetch-Bold.ttf" if bold else "ChakraPetch-Regular.ttf"
    return ImageFont.truetype(f"{DL_FONT_DIR}/{p}", size)


def f_silk(size, bold=False):
    p = "Silkscreen-Bold.ttf" if bold else "Silkscreen-Regular.ttf"
    return ImageFont.truetype(f"{DL_FONT_DIR}/{p}", size)


def f_bold(size):
    return ImageFont.truetype(f"{FONT_DIR}/GothamRnd-Bold.ttf", size)


def f_book(size):
    return ImageFont.truetype(f"{FONT_DIR}/GothamRnd-Book.ttf", size)


def f_black(size):
    return ImageFont.truetype(f"{FONT_DIR}/Montserrat-Black.ttf", size)


def f_mdi(size):
    return ImageFont.truetype(f"{FONT_DIR}/materialdesignicons-webfont.ttf", size)


MDI = {
    "sunny": "\U000F0599",
    "partly_cloudy": "\U000F0595",
    "cloudy": "\U000F0590",
    "rainy": "\U000F0597",
    "car": "\U000F010B",
    "waves": "\U000F078D",
    "water_percent": "\U000F058E",
    "home": "\U000F06A1",
}

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


def fill_dither(img, x0, y0, x1, y1, step=2):
    """Fill a rectangle with a classic 1-bit checkerboard/halftone dither pattern."""
    px = img.load()
    for y in range(max(0, y0), min(480, y1)):
        for x in range(max(0, x0), min(800, x1)):
            if step == 2:
                if (x + y) % 2 == 0:
                    px[x, y] = 0
            elif step == 3:
                if (x % 3 == 0) and (y % 3 == 0):
                    px[x, y] = 0
            elif step == 4:
                if (x % 2 == 0) and (y % 2 == 0):
                    px[x, y] = 0


# ==============================================================================
# W1-01: "Architectural House Cutaway / Property Schematic" (r/homeassistant #1 concept)
# ==============================================================================
def render_w1_01():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Top Architectural Blueprint Title Block
    d.rectangle((12, 12, 788, 468), outline=0, width=2)
    d.rectangle((16, 16, 784, 52), fill=0)
    dt(d, 28, 23, "WOODGREEN RESIDENCE // ARCHITECTURAL TELEMETRY", f_mono(18), fill=255)
    dt(d, 772, 23, "SUN OCT 18 • AQI 21 • UV 5.6", f_mono(16), fill=255, anchor="ra")

    # Sky / Weather Arc Zone (y=60..156)
    # Left: Current Weather + 5-Day Summary
    dt(d, 30, 62, "84°F", f_bebas(64), fill=0)
    dt(d, 148, 86, MDI["sunny"], f_mdi(48), fill=0, anchor="mm")
    dt(d, 184, 66, "SUNNY • 21% OUT RH • WIND 6 MPH", f_mono(14), fill=0)
    draw_wrapped(d, 184, 88, FORECAST_SUMMARY, f_book(13), 310, 17, fill=0, max_lines=3)

    # Right Sky: 5 Hourly Sun/Cloud positions along an arc
    for i, (ts, ic, tp) in enumerate(HOURLY):
        hx = 530 + i * 52
        hy = 98 - int(10 * math.sin(i * math.pi / 4.0))
        dt(d, hx, hy - 24, ts, f_mono(11), fill=0, anchor="mm")
        dt(d, hx, hy, MDI[ic], f_mdi(24), fill=0, anchor="mm")
        dt(d, hx, hy + 22, f"{tp}°", f_bold(13), fill=0, anchor="mm")

    d.line((16, 146, 784, 146), fill=0, width=1)

    # Central Cross-Section Schematic (y=154..382)
    # Ground line at y=332
    d.line((24, 332, 776, 332), fill=0, width=3)
    fill_dither(img, 24, 333, 776, 384, step=4)

    # 1. Left Wing: Driveway + Carport with Tesla Model 3 (x=32..224, y=220..332)
    d.line((32, 224, 224, 204), fill=0, width=3)  # Carport roof
    d.line((40, 224, 40, 332), fill=0, width=2)
    d.rectangle((48, 162, 214, 200), fill=255, outline=0, width=2)
    dt(d, 131, 168, "DRIVEWAY (OUT)", f_mono(12), fill=0, anchor="ma")
    dt(d, 131, 182, "84°F • 52% RH", f_bold(13), fill=0, anchor="ma")

    # Carport box for Model 3
    d.rounded_rectangle((50, 236, 212, 322), radius=8, fill=0)
    dt(d, 62, 246, "TESLA MODEL 3", f_mono(13), fill=255)
    dt(d, 198, 246, "79%", f_bebas(26), fill=255, anchor="ra")
    dt(d, 62, 272, "Range: 202 mi", f_book(13), fill=255)
    d.rectangle((62, 296, 198, 308), outline=255, width=1)
    d.rectangle((64, 298, 64 + int(132 * 0.79), 306), fill=255)

    # 2. Center House Structure: Pitched Roof + Loft (Top) + Dining (Main) + Crawlspace (Below Ground)
    # House walls x=236..524, y=200..332; Pitched roof peak at (380, 152)
    d.polygon([(226, 204), (380, 152), (534, 204)], outline=0, width=3)
    d.rectangle((236, 204, 524, 332), fill=255, outline=0, width=3)
    d.line((236, 266, 524, 266), fill=0, width=2)  # Floor divider between Loft and Dining

    # Upper Floor: LOFT
    dt(d, 252, 214, "2F // LOFT", f_mono(14), fill=0)
    dt(d, 508, 212, "78°F • 40% RH", f_black(16), fill=0, anchor="ra")
    d.rectangle((252, 242, 508, 254), outline=0, width=1)
    d.rectangle((254, 244, 254 + int(252 * 0.40), 252), fill=0)

    # Main Floor: DINING ROOM + Water Softener
    dt(d, 252, 276, "1F // DINING", f_mono(14), fill=0)
    dt(d, 508, 274, "79°F • 47% RH", f_black(16), fill=0, anchor="ra")
    d.rectangle((252, 304, 410, 316), outline=0, width=1)
    d.rectangle((254, 306, 254 + int(154 * 0.47), 314), fill=0)
    dt(d, 508, 304, "Salt: 63%", f_mono(13), fill=0, anchor="ra")

    # Foundation Below Ground: CRAWLSPACE (y=332..382)
    d.rectangle((236, 332, 524, 382), fill=255, outline=0, width=2)
    dt(d, 252, 348, "B1 // CRAWL", f_mono(14), fill=0)
    dt(d, 508, 346, "80°F • 31% RH", f_black(16), fill=0, anchor="ra")

    # 3. Right Wing: Backyard + Cabana Structure (x=544..768)
    # Backyard Open Air Callout
    d.rectangle((548, 162, 764, 212), fill=255, outline=0, width=2)
    dt(d, 562, 170, "BACKYARD (OUT)", f_mono(13), fill=0)
    dt(d, 750, 170, "87°F", f_black(18), fill=0, anchor="ra")
    dt(d, 562, 190, "Humidity: 43% RH", f_bold(13), fill=0)

    # Cabana Pavilion (x=556..760, y=236..332)
    d.polygon([(548, 244), (658, 218), (768, 244)], outline=0, width=3)
    d.rectangle((558, 244, 758, 332), fill=255, outline=0, width=2)
    dt(d, 658, 254, "CABANA PAVILION", f_mono(13), fill=0, anchor="ma")
    dt(d, 658, 276, "73°F • 68% RH", f_black(18), fill=0, anchor="ma")
    d.rectangle((578, 306, 738, 318), outline=0, width=1)
    d.rectangle((580, 308, 580 + int(156 * 0.68), 316), fill=0)

    # Bottom Blueprint Footer Bar (y=392..460): Commute Routes & Santa Monica Tide Wave
    d.rectangle((24, 392, 776, 458), fill=0)
    dt(d, 40, 404, "COMMUTE // ROSE AVE (WORK)", f_mono(13), fill=255)
    dt(d, 310, 400, "9 MIN", f_bebas(28), fill=255, anchor="ra")
    dt(d, 40, 430, "COMMUTE // CENTINELA (WISH)", f_mono(13), fill=255)
    dt(d, 310, 426, "17 MIN", f_bebas(28), fill=255, anchor="ra")

    d.line((336, 400, 336, 450), fill=255, width=1)
    dt(d, 356, 404, "SANTA MONICA TIDES", f_mono(13), fill=255)
    dt(d, 356, 428, "HI 3:29 PM  •  LO 11:38 PM", f_bold(15), fill=255)
    wpts = []
    for px in range(600, 760, 4):
        t = (px - 600) / 160.0
        py = 426 - int(14 * math.sin((t - 0.08) * 1.8 * math.pi))
        wpts.append((px, py))
    d.line(wpts, fill=255, width=2)

    img.save(f"{OUT_DIR}/w1_01.png")


# ==============================================================================
# W1-02: "Solari Split-Flap Airport / Grand Central Departure Board"
# ==============================================================================
def draw_flap_string(d, x, y, text, cw=24, ch=36, font=None):
    """Draw mechanical split-flap character tiles with center horizontal hinge line."""
    if font is None:
        font = f_bebas(30)
    for i, ch_str in enumerate(text):
        fx = x + i * (cw + 3)
        d.rounded_rectangle((fx, y, fx + cw, y + ch), radius=3, fill=0)
        dt(d, fx + cw // 2, y + ch // 2, ch_str, font, fill=255, anchor="mm")
        # Mechanical split-flap horizontal hinge line across the middle!
        d.line((fx, y + ch // 2, fx + cw, y + ch // 2), fill=255, width=1)


def render_w1_02():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Outer mechanical board frame
    d.rectangle((0, 0, 800, 480), fill=255)
    d.rectangle((10, 10, 790, 470), outline=0, width=3)

    # Top Station Header
    d.rectangle((10, 10, 790, 58), fill=0)
    dt(d, 28, 20, "WOODGREEN TERMINAL // DEPARTURES & TELEMETRY", f_bebas(30), fill=255)
    dt(d, 772, 22, "SUN 18 OCT • AQI 21 • UV 5.6", f_mono(16), fill=255, anchor="ra")

    # Row 1 (y=70..192): Weather Split-Flap Readout (Left) + 5 Hourly Flap Slots (Right)
    dt(d, 28, 70, "CURRENT WEATHER", f_mono(13), fill=0)
    draw_flap_string(d, 28, 90, "84F SUNNY", cw=26, ch=42, font=f_bebas(34))
    dt(d, 28, 142, "OUTSIDE HUMIDITY: 21% RH  •  WIND: 6 MPH", f_mono(13), fill=0)
    draw_wrapped(d, 28, 162, FORECAST_SUMMARY, f_book(13), 360, 16, fill=0, max_lines=2)

    d.line((404, 68, 404, 194), fill=0, width=2)
    dt(d, 420, 70, "HOURLY FORECAST FLAPS", f_mono(13), fill=0)
    for i, (ts, ic, tp) in enumerate(HOURLY):
        cx = 420 + i * 72 + 30
        dt(d, cx, 92, ts, f_mono(12), fill=0, anchor="ma")
        dt(d, cx, 124, MDI[ic], f_mdi(28), fill=0, anchor="mm")
        draw_flap_string(d, cx - 26, 146, f"{tp}", cw=24, ch=36, font=f_bebas(28))

    d.line((10, 200, 790, 200), fill=0, width=2)

    # Row 2 (y=210..336): 4 Departure / Status Rows in Authentic Split-Flap Style!
    dt(d, 28, 210, "DESTINATION / SYSTEM", f_mono(12), fill=0)
    dt(d, 250, 210, "STATUS / ROUTE", f_mono(12), fill=0)
    dt(d, 480, 210, "READOUT", f_mono(12), fill=0)

    board_rows = [
        ("WORK COMMUTE", "VIA ROSE AVE", "09 MIN"),
        ("WISH SCHOOL", "VIA CENTINELA", "17 MIN"),
        ("TESLA MODEL 3", "202 MI RANGE", "79 PCT"),
        ("SANTA MONICA", "LO TIDE 11:38P", "03:29P"),
    ]
    ry = 232
    for dest, via, flap_val in board_rows:
        dt(d, 28, ry + 8, dest, f_bebas(24), fill=0)
        dt(d, 210, ry + 11, via, f_mono(14), fill=0)
        draw_flap_string(d, 380, ry, flap_val, cw=24, ch=34, font=f_bebas(28))
        ry += 40

    # Right Side Column (x=568..776, y=210..390): Water Softener & Quick Summary
    d.line((564, 200, 564, 396), fill=0, width=2)
    dt(d, 580, 212, "SOFTENER SALT", f_mono(13), fill=0)
    draw_flap_string(d, 580, 234, "63 PCT", cw=26, ch=38, font=f_bebas(30))
    d.rectangle((580, 284, 772, 298), outline=0, width=2)
    d.rectangle((582, 286, 582 + int(188 * 0.63), 296), fill=0)
    dt(d, 580, 316, "INDOOR AVG: 39% RH", f_mono(14), fill=0)
    dt(d, 580, 340, "PERIMETER: 21-68% RH", f_mono(14), fill=0)
    dt(d, 580, 364, "ALL SENSORS ONLINE", f_mono(13), fill=0)

    d.line((10, 396, 790, 396), fill=0, width=2)

    # Bottom Row (y=404..462): 6-Zone Split-Flap Climate Strip across the bottom
    zw = 756 // 6
    for i, (_, caps, tp, rh, _) in enumerate(ZONES):
        zx = 22 + i * zw
        dt(d, zx, 404, caps, f_mono(12), fill=0)
        draw_flap_string(d, zx, 422, f"{tp}F{rh}%", cw=17, ch=32, font=f_bebas(24))

    img.save(f"{OUT_DIR}/w1_02.png")


# ==============================================================================
# W1-03: "1984 Apple Macintosh System 1 / HyperCard Desktop" (1-Bit Dither + Pixel Windows)
# ==============================================================================
def draw_mac_window(img, d, x0, y0, x1, y1, title):
    """Draw a classic 1984 Mac System 1 window with drop shadow, close box, and pinstriped title bar."""
    # Drop shadow
    d.rectangle((x0 + 4, y0 + 4, x1 + 4, y1 + 4), fill=0)
    # Window body
    d.rectangle((x0, y0, x1, y1), fill=255, outline=0, width=2)
    # Title bar
    d.rectangle((x0, y0, x1, y0 + 26), fill=255, outline=0, width=2)
    for py in range(y0 + 4, y0 + 23, 2):
        d.line((x0 + 6, py, x1 - 6, py), fill=0, width=1)
    # Close box
    d.rectangle((x0 + 10, y0 + 6, x0 + 24, y0 + 20), fill=255, outline=0, width=2)
    # Title pill
    tw = len(title) * 9 + 20
    cx = (x0 + x1) // 2
    d.rectangle((cx - tw // 2, y0 + 3, cx + tw // 2, y0 + 23), fill=255)
    dt(d, cx, y0 + 13, title, f_silk(12, bold=True), fill=0, anchor="mm")


def render_w1_03():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Classic 50% 1-bit checkerboard desktop pattern
    fill_dither(img, 0, 28, 800, 480, step=2)

    # Top Mac System 1 Menu Bar (y=0..28)
    d.rectangle((0, 0, 800, 28), fill=255, outline=0, width=2)
    dt(d, 16, 7, "WOODGREEN OS  File  Edit  View  Weather  Sensors", f_silk(12, bold=True), fill=0)
    dt(d, 784, 7, "Sun Oct 18  2:40 PM", f_silk(12, bold=True), fill=0, anchor="ra")

    # Window 1 (Top-Left, x=18..430, y=42..276): "Weather & Forecast"
    draw_mac_window(img, d, 18, 42, 430, 276, "Weather.stk")
    dt(d, 36, 76, "84°F", f_vt(68), fill=0)
    dt(d, 188, 106, MDI["sunny"], f_mdi(52), fill=0, anchor="mm")
    dt(d, 232, 80, "SUNNY", f_silk(14, bold=True), fill=0)
    dt(d, 232, 100, "Out RH: 21% • UV 5.6", f_vt(18), fill=0)
    dt(d, 232, 118, "AQI 21 Good • 6 mph", f_vt(18), fill=0)

    d.line((32, 144, 416, 144), fill=0, width=1)
    # 5 Hourly slots inside Mac window
    for i, (ts, ic, tp) in enumerate(HOURLY):
        cx = 36 + i * 76 + 34
        dt(d, cx, 150, ts, f_silk(10), fill=0, anchor="ma")
        dt(d, cx, 178, MDI[ic], f_mdi(24), fill=0, anchor="mm")
        dt(d, cx, 196, f"{tp}°F", f_vt(20), fill=0, anchor="ma")

    d.line((32, 220, 416, 220), fill=0, width=1)
    draw_wrapped(d, 32, 226, FORECAST_SUMMARY, f_vt(17), 384, 16, fill=0, max_lines=3)

    # Window 2 (Top-Right, x=450..780, y=42..294): "Climate Zones (Temp & RH)"
    draw_mac_window(img, d, 450, 42, 780, 294, "HomeClimate.da")
    sy = 78
    for idx, (name, _, tp, rh, kind) in enumerate(ZONES):
        if idx == 3:
            d.line((466, sy - 3, 764, sy - 3), fill=0, width=1)
            sy += 4
        dt(d, 466, sy, f"{name} ({kind})", f_silk(11, bold=(kind == "IN")), fill=0)
        dt(d, 646, sy - 2, f"{tp}°F", f_vt(22), fill=0, anchor="ra")
        # Retro dithered progress bar for RH
        d.rectangle((656, sy + 2, 720, sy + 16), outline=0, width=1)
        fill_w = int(62 * (rh / 100.0))
        d.rectangle((657, sy + 3, 657 + fill_w, sy + 15), fill=0)
        dt(d, 766, sy - 2, f"{rh}%", f_vt(22), fill=0, anchor="ra")
        sy += 34

    # Window 3 (Bottom-Left, x=18..430, y=294..462): "Commute & Tides"
    draw_mac_window(img, d, 18, 294, 430, 462, "Commute_Tides")
    dt(d, 34, 332, "Work (Rose Ave):", f_silk(11), fill=0)
    dt(d, 224, 328, "9 MIN", f_vt(26), fill=0, anchor="ra")
    dt(d, 34, 362, "WISH (Centinela):", f_silk(11), fill=0)
    dt(d, 224, 358, "17 MIN", f_vt(26), fill=0, anchor="ra")
    d.line((34, 390, 414, 390), fill=0, width=1)
    dt(d, 34, 402, "Santa Monica High Tide: 3:29 PM", f_vt(20), fill=0)
    dt(d, 34, 426, "Low Tide: 11:38 PM", f_vt(18), fill=0)
    # Mini wave on right of window 3
    wpts = []
    for px in range(250, 410, 4):
        t = (px - 250) / 160.0
        py = 362 - int(16 * math.sin((t - 0.08) * 1.8 * math.pi))
        wpts.append((px, py))
    d.line(wpts, fill=0, width=2)

    # Window 4 (Bottom-Right, x=450..780, y=312..462): "Model 3 & Softener"
    draw_mac_window(img, d, 450, 312, 780, 462, "Systems.ctrl")
    dt(d, 466, 348, "TESLA MODEL 3", f_silk(11, bold=True), fill=0)
    dt(d, 764, 344, "79% (202 mi)", f_vt(22), fill=0, anchor="ra")
    d.rectangle((466, 370, 764, 386), outline=0, width=2)
    fill_dither(img, 468, 372, 468 + int(294 * 0.79), 384, step=2)

    dt(d, 466, 398, "SOFTENER SALT", f_silk(11, bold=True), fill=0)
    dt(d, 764, 394, "63%", f_vt(22), fill=0, anchor="ra")
    d.rectangle((466, 420, 764, 436), outline=0, width=2)
    fill_dither(img, 468, 422, 468 + int(294 * 0.63), 434, step=2)

    img.save(f"{OUT_DIR}/w1_03.png")


# ==============================================================================
# W1-04: "Yr.no / Windy Full-Width Meteogram & Tide Wave" (Data-Viz Curve First)
# ==============================================================================
def render_w1_04():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Top Header + Current Weather Summary
    dt(d, 24, 16, "SUNDAY, OCT 18", f_black(22), fill=0)
    dt(d, 250, 16, "84°F SUNNY • 21% RH • AQI 21 • UV 5.6", f_spacemono(14, bold=True), fill=0)
    d.line((24, 46, 776, 46), fill=0, width=2)
    draw_wrapped(d, 24, 54, FORECAST_SUMMARY, f_book(14), 752, 18, fill=0, max_lines=2)

    # Centerpiece (y=98..276): Full-Width Sweeping Meteogram Curve (Temp + Tide Wave) with Halftone Fill!
    d.rectangle((24, 96, 776, 272), outline=0, width=2)
    dt(d, 36, 104, "HOURLY METEOGRAM & SANTA MONICA TIDE WAVE", f_spacemono(12, bold=True), fill=0)
    dt(d, 764, 104, "HI TIDE 3:29 PM • LO 11:38 PM", f_spacemono(11), fill=0, anchor="ra")

    # Smooth temperature curve across x=60..740
    # Temps: 84, 84, 83, 81, 79
    anchor_x = [80, 240, 400, 560, 720]
    anchor_t = [84, 84, 83, 81, 79]
    anchor_y = [int(218 - (t - 77) * 9) for t in anchor_t]

    # Interpolate curve and dither underneath it
    curve_pts = []
    px_access = img.load()
    for x in range(60, 741):
        # Piecewise cosine interpolation
        if x <= anchor_x[0]:
            cy = anchor_y[0]
        elif x >= anchor_x[-1]:
            cy = anchor_y[-1]
        else:
            for k in range(len(anchor_x) - 1):
                if anchor_x[k] <= x <= anchor_x[k + 1]:
                    mu = (x - anchor_x[k]) / float(anchor_x[k + 1] - anchor_x[k])
                    mu2 = (1 - math.cos(mu * math.pi)) / 2.0
                    cy = int(anchor_y[k] * (1 - mu2) + anchor_y[k + 1] * mu2)
                    break
        curve_pts.append((x, cy))
        # Halftone dot fill below temperature curve down to y=242
        for y in range(cy + 2, 242):
            if (x % 3 == 0) and (y % 3 == 0):
                px_access[x, y] = 0

    d.line(curve_pts, fill=0, width=3)

    # Secondary dashed curve for Santa Monica Tide
    for x in range(60, 740, 6):
        t = (x - 60) / 680.0
        ty = 216 - int(22 * math.sin((t - 0.12) * 1.7 * math.pi))
        d.line((x, ty, x + 3, ty), fill=0, width=2)

    # Plot hourly nodes, icons, and labels along the curve
    for i, (ts, ic, tp) in enumerate(HOURLY):
        nx, ny = anchor_x[i], anchor_y[i]
        d.ellipse((nx - 5, ny - 5, nx + 5, ny + 5), fill=255, outline=0, width=3)
        dt(d, nx, ny - 26, MDI[ic], f_mdi(26), fill=0, anchor="mm")
        dt(d, nx + 26, ny - 16, f"{tp}°", f_black(15), fill=0, anchor="mm")
        dt(d, nx, 250, ts, f_spacemono(12, bold=True), fill=0, anchor="mm")

    # Tier 3 (y=282..372): 6-Zone Climate Ribbon (Co-Equal Temp & RH)
    zw = 752 // 6
    for i, (_, caps, tp, rh, kind) in enumerate(ZONES):
        zx = 24 + i * zw
        d.rounded_rectangle((zx + 3, 282, zx + zw - 3, 370), radius=6, fill=0 if kind == "IN" else 255, outline=0, width=2)
        fg = 255 if kind == "IN" else 0
        cx = zx + zw // 2
        dt(d, cx, 290, f"{caps} ({kind})", f_spacemono(11, bold=True), fill=fg, anchor="ma")
        dt(d, cx, 310, f"{tp}°F", f_black(20), fill=fg, anchor="ma")
        dt(d, cx, 340, f"{rh}% RH", f_bold(14), fill=fg, anchor="ma")

    # Tier 4 (y=382..466): 3 Bottom Logistics Cards (Work, WISH, Model 3 + Salt)
    cards = [
        ("TO WORK (ROSE AVE)", "9 MIN", "Normal traffic"),
        ("TO WISH (CENTINELA)", "17 MIN", "Normal traffic"),
        ("MODEL 3 & SOFTENER", "79% / 63%", "202 mi range • Salt OK"),
    ]
    for i, (ct, cv, cs) in enumerate(cards):
        bx = 24 + i * 256
        d.rounded_rectangle((bx, 382, bx + 240, 466), radius=8, outline=0, width=2)
        dt(d, bx + 14, 392, ct, f_spacemono(11, bold=True), fill=0)
        dt(d, bx + 14, 412, cv, f_black(22), fill=0)
        dt(d, bx + 14, 442, cs, f_book(13), fill=0)

    img.save(f"{OUT_DIR}/w1_04.png")


# ==============================================================================
# W1-05: "The Old Farmer's Ink Almanac & Broadsheet" (DM Serif Display + Italic Prose)
# ==============================================================================
def render_w1_05():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Ornamental double frame
    d.rectangle((12, 12, 788, 468), outline=0, width=3)
    d.rectangle((18, 18, 782, 462), outline=0, width=1)

    # Broadsheet Masthead in DM Serif Display
    dt(d, 400, 26, "THE WOODGREEN ALMANACK", f_serif(32), fill=0, anchor="ma")
    d.line((32, 66, 768, 66), fill=0, width=2)
    dt(d, 36, 72, "Sunday, the 18th of October", f_serif(16, italic=True), fill=0)
    dt(d, 400, 72, "LAT. 34.00° N  •  SANTA MONICA BAY", f_book(12), fill=0, anchor="ma")
    dt(d, 764, 72, "AQI 21 Good  •  UV 5.6", f_serif(16, italic=True), fill=0, anchor="ra")
    d.line((32, 96, 768, 96), fill=0, width=1)

    # Left Column (x=34..294): Engraved Sun + Giant Serif Temperature + Narrative
    dt(d, 36, 102, "84°", f_serif(84), fill=0)
    dt(d, 232, 152, MDI["sunny"], f_mdi(64), fill=0, anchor="mm")
    dt(d, 36, 198, "Bright & Sunny • 21% Out RH", f_serif(16, italic=True), fill=0)
    d.line((36, 226, 286, 226), fill=0, width=1)
    almanac_prose = (
        "“Sunny skies with highs in the 70s and 80s through Tuesday. "
        "Rain arrives Wednesday, followed by cooler, partly cloudy days.”"
    )
    draw_wrapped(d, 36, 236, almanac_prose, f_serif(16, italic=True), 250, 22, fill=0, max_lines=5)

    # Hourly table at bottom of Col 1
    d.line((36, 356, 286, 356), fill=0, width=1)
    dt(d, 36, 364, "HOURLY PROGRESSION", f_bold(12), fill=0)
    for i, (ts, ic, tp) in enumerate(HOURLY):
        cx = 40 + i * 50 + 20
        dt(d, cx, 386, ts, f_book(11), fill=0, anchor="ma")
        dt(d, cx, 412, MDI[ic], f_mdi(22), fill=0, anchor="mm")
        dt(d, cx, 430, f"{tp}°", f_serif(16), fill=0, anchor="ma")

    d.line((304, 104, 304, 450), fill=0, width=1)

    # Center Column (x=320..540): Household & Garden Register (6 Zones)
    dt(d, 430, 106, "CHAMBER & GARDEN", f_serif(18), fill=0, anchor="ma")
    d.line((320, 134, 540, 134), fill=0, width=1)
    sy = 148
    for idx, (name, _, tp, rh, kind) in enumerate(ZONES):
        if idx == 3:
            d.line((320, sy - 4, 540, sy - 4), fill=0, width=1)
            dt(d, 430, sy + 2, "— Outdoor Grounds —", f_serif(14, italic=True), fill=0, anchor="ma")
            sy += 28
        dt(d, 320, sy, name, f_serif(18), fill=0)
        dt(d, 462, sy, f"{tp}°F", f_serif(18), fill=0, anchor="ra")
        dt(d, 540, sy + 2, f"{rh}% RH", f_serif(16, italic=True), fill=0, anchor="ra")
        sy += 44

    d.line((556, 104, 556, 450), fill=0, width=1)

    # Right Column (x=572..764): Coaching / Transit Times, Electric Carriage & Tides
    dt(d, 668, 106, "CARRIAGE & TIDES", f_serif(18), fill=0, anchor="ma")
    d.line((572, 134, 764, 134), fill=0, width=1)

    dt(d, 572, 148, "To Work (Rose)", f_serif(15, italic=True), fill=0)
    dt(d, 764, 142, "9 min", f_serif(22), fill=0, anchor="ra")
    dt(d, 572, 186, "To WISH (Cent.)", f_serif(15, italic=True), fill=0)
    dt(d, 764, 180, "17 min", f_serif(22), fill=0, anchor="ra")
    d.line((572, 218, 764, 218), fill=0, width=1)

    dt(d, 572, 230, "Model 3 Accumulator", f_serif(16), fill=0)
    dt(d, 572, 254, "79%  (202 Miles)", f_serif(22, italic=True), fill=0)
    dt(d, 572, 290, "Brine Cistern (Salt):", f_serif(15, italic=True), fill=0)
    dt(d, 764, 288, "63%", f_serif(20), fill=0, anchor="ra")
    d.line((572, 322, 764, 322), fill=0, width=1)

    dt(d, 572, 334, "Santa Monica High Water", f_serif(16), fill=0)
    dt(d, 572, 358, "3:29 PM", f_serif(28), fill=0)
    dt(d, 572, 396, "Low Water: 11:38 PM", f_serif(16, italic=True), fill=0)
    wpts = []
    for px in range(572, 764, 4):
        t = (px - 572) / 192.0
        py = 434 - int(10 * math.sin((t - 0.08) * 1.8 * math.pi))
        wpts.append((px, py))
    d.line(wpts, fill=0, width=2)

    img.save(f"{OUT_DIR}/w1_05.png")


# ==============================================================================
# W1-06: "UNIX Terminal / tmux + btop Hacker News Dashboard" (ShareTechMono + ASCII Gauges)
# ==============================================================================
def draw_tty_box(d, x0, y0, x1, y1, title):
    d.rectangle((x0, y0, x1, y1), outline=0, width=2)
    tw = len(title) * 10 + 16
    d.rectangle((x0 + 14, y0 - 8, x0 + 14 + tw, y0 + 10), fill=255)
    dt(d, x0 + 22, y0 - 8, title, f_mono(15), fill=0)


def ascii_bar(pct, width=10):
    filled = round((pct / 100.0) * width)
    return "[" + ("#" * filled) + ("." * (width - filled)) + "]"


def render_w1_06():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Top tmux status bar
    d.rectangle((0, 0, 800, 32), fill=0)
    dt(d, 12, 7, "[0] woodgreen@eink-panel:~ (tmux 3.4)  |  0:weather*  1:sensors  2:route", f_mono(15), fill=255)
    dt(d, 788, 7, "Sun Oct 18 14:40", f_mono(15), fill=255, anchor="ra")

    # Pane 0 (Top-Left, x=14..424, y=48..258): wttr.in / weather
    draw_tty_box(d, 14, 48, 424, 258, "wttr.in/Woodgreen")
    dt(d, 30, 64, "84°F", f_mono(52), fill=0)
    dt(d, 182, 92, MDI["sunny"], f_mdi(48), fill=0, anchor="mm")
    dt(d, 224, 66, "COND: SUNNY", f_mono(16), fill=0)
    dt(d, 224, 88, "RH  : 21% (OUT)", f_mono(15), fill=0)
    dt(d, 224, 108, "AQI : 21 [GOOD] UV:5.6", f_mono(15), fill=0)

    dt(d, 30, 136, "HR   NOW    1PM    2PM    3PM    4PM", f_mono(15), fill=0)
    dt(d, 30, 158, "TMP  84F    84F    83F    81F    79F", f_mono(15), fill=0)
    dt(d, 30, 184, "OUTLOOK:", f_mono(14), fill=0)
    draw_wrapped(d, 30, 204, FORECAST_SUMMARY, f_mono(13), 380, 16, fill=0, max_lines=3)

    # Pane 1 (Top-Right, x=440..786, y=48..296): sensors --humidity --temp
    draw_tty_box(d, 440, 48, 786, 296, "sensors --zones")
    dt(d, 456, 66, "ZONE       TEMP   HUMIDITY       RH", f_mono(14), fill=0)
    d.line((456, 86, 770, 86), fill=0, width=1)
    sy = 96
    for idx, (_, caps, tp, rh, kind) in enumerate(ZONES):
        if idx == 3:
            dt(d, 456, sy, "--- outdoor perimeter ------------", f_mono(13), fill=0)
            sy += 22
        bar = ascii_bar(rh, 8)
        line = f"{caps:<8}  {tp:>3}F   {bar}  {rh:>2}%"
        dt(d, 456, sy, line, f_mono(15), fill=0)
        sy += 28

    # Pane 2 (Bottom-Left, x=14..424, y=276..466): route & tides
    draw_tty_box(d, 14, 276, 424, 466, "route & tide-predict")
    dt(d, 30, 298, "$ route --eta", f_mono(14), fill=0)
    dt(d, 30, 320, "  -> WORK (Rose Ave)     :  9 MIN [OK]", f_mono(16), fill=0)
    dt(d, 30, 344, "  -> WISH (Centinela)    : 17 MIN [OK]", f_mono(16), fill=0)
    dt(d, 30, 378, "$ tide --station 'Santa Monica'", f_mono(14), fill=0)
    dt(d, 30, 402, "  HIGH TIDE : 03:29 PM", f_mono(16), fill=0)
    dt(d, 30, 426, "  LOW TIDE  : 11:38 PM", f_mono(16), fill=0)

    # Pane 3 (Bottom-Right, x=440..786, y=314..466): tesla-cli & salt
    draw_tty_box(d, 440, 314, 786, 466, "power & telemetry")
    dt(d, 456, 338, "MODEL_3_SOC : 79% (202 mi)", f_mono(16), fill=0)
    dt(d, 456, 362, f"  {ascii_bar(79, 20)}", f_mono(16), fill=0)
    dt(d, 456, 396, "SOFTENER_SLT: 63% [NOMINAL]", f_mono(16), fill=0)
    dt(d, 456, 420, f"  {ascii_bar(63, 20)}", f_mono(16), fill=0)

    img.save(f"{OUT_DIR}/w1_06.png")


# ==============================================================================
# W1-07: "Casio G-Shock / Braun Digital LCD Multi-Bezel Watch Face" (Chakra Petch)
# ==============================================================================
def render_w1_07():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Outer Black Watch Case with Octagonal Inner Bezel
    d.rectangle((0, 0, 800, 480), fill=0)
    bezel = [(36, 12), (764, 12), (788, 36), (788, 444), (764, 468), (36, 468), (12, 444), (12, 36)]
    d.polygon(bezel, fill=255, outline=0)
    inner = [(44, 20), (756, 20), (780, 44), (780, 436), (756, 460), (44, 460), (20, 436), (20, 44)]
    d.polygon(inner, fill=255, outline=0, width=3)

    # Top LCD Mode Header Bar
    d.rectangle((48, 28, 752, 62), fill=0)
    dt(d, 60, 35, "CASIO // WOODGREEN CHRONO-CLIMATE", f_chakra(16, bold=True), fill=255)
    dt(d, 740, 35, "SUN 10-18  •  ALM  SIG  24H", f_chakra(15, bold=True), fill=255, anchor="ra")

    # Upper Left LCD Sub-Bezel (x=48..320, y=72..268): Weather + Hourly Bar Graph
    d.rounded_rectangle((48, 72, 320, 268), radius=8, outline=0, width=3)
    dt(d, 62, 80, "84°F", f_chakra(56, bold=True), fill=0)
    dt(d, 272, 112, MDI["sunny"], f_mdi(52), fill=0, anchor="mm")
    dt(d, 62, 144, "SUNNY • 21% OUT RH", f_chakra(14, bold=True), fill=0)
    dt(d, 62, 164, "AQI 21 • UV 5.6 • 6 MPH", f_chakra(12, bold=False), fill=0)
    d.line((62, 186, 306, 186), fill=0, width=2)
    for i, (ts, ic, tp) in enumerate(HOURLY):
        cx = 64 + i * 48 + 20
        dt(d, cx, 194, ts[:3], f_chakra(11, bold=True), fill=0, anchor="ma")
        dt(d, cx, 222, MDI[ic], f_mdi(22), fill=0, anchor="mm")
        dt(d, cx, 240, f"{tp}°", f_chakra(14, bold=True), fill=0, anchor="ma")

    # Upper Right LCD Sub-Bezel (x=334..752, y=72..268): 6-Zone Multi-Sensor LCD Matrix
    d.rounded_rectangle((334, 72, 752, 268), radius=8, outline=0, width=3)
    d.rectangle((334, 72, 752, 98), fill=0)
    dt(d, 348, 77, "6-ZONE HYGRO-THERMO MATRIX", f_chakra(14, bold=True), fill=255)
    dt(d, 738, 77, "IN / OUT", f_chakra(13, bold=True), fill=255, anchor="ra")

    cw, ch = 418 // 3, 84
    for idx, (_, caps, tp, rh, kind) in enumerate(ZONES):
        col = idx % 3
        row = idx // 3
        zx = 334 + col * cw
        zy = 98 + row * ch
        if col > 0:
            d.line((zx, zy + 4, zx, zy + ch - 4), fill=0, width=1)
        if row > 0:
            d.line((340, zy, 746, zy), fill=0, width=2)
        dt(d, zx + 10, zy + 6, f"{caps} [{kind}]", f_chakra(11, bold=True), fill=0)
        dt(d, zx + 10, zy + 24, f"{tp}°", f_chakra(26, bold=True), fill=0)
        dt(d, zx + cw - 10, zy + 28, f"{rh}%", f_chakra(20, bold=True), fill=0, anchor="ra")
        # LCD segment ticks
        d.rectangle((zx + 10, zy + 62, zx + cw - 12, zy + 72), outline=0, width=1)
        d.rectangle((zx + 12, zy + 64, zx + 12 + int((cw - 26) * (rh / 100.0)), zy + 70), fill=0)

    # Bottom Left LCD Sub-Bezel (x=48..424, y=280..446): 5-Day Outlook + Tides
    d.rounded_rectangle((48, 280, 424, 446), radius=8, outline=0, width=3)
    dt(d, 62, 290, "5-DAY OUTLOOK & TIDE GRAPH", f_chakra(13, bold=True), fill=0)
    draw_wrapped(d, 62, 312, FORECAST_SUMMARY, f_chakra(13, bold=False), 348, 18, fill=0, max_lines=3)
    d.line((62, 376, 410, 376), fill=0, width=1)
    dt(d, 62, 388, "HI TIDE: 3:29 PM", f_chakra(15, bold=True), fill=0)
    dt(d, 62, 412, "LO TIDE: 11:38 PM", f_chakra(14, bold=False), fill=0)
    wpts = []
    for px in range(256, 406, 4):
        t = (px - 256) / 150.0
        py = 412 - int(14 * math.sin((t - 0.08) * 1.8 * math.pi))
        wpts.append((px, py))
    d.line(wpts, fill=0, width=2)

    # Bottom Right LCD Sub-Bezel (x=438..752, y=280..446): Commute, Model 3 & Salt
    d.rounded_rectangle((438, 280, 752, 446), radius=8, outline=0, width=3)
    dt(d, 452, 290, "WORK (ROSE)", f_chakra(13, bold=False), fill=0)
    dt(d, 600, 288, "09M", f_chakra(20, bold=True), fill=0, anchor="ra")
    dt(d, 616, 290, "WISH", f_chakra(13, bold=False), fill=0)
    dt(d, 738, 288, "17M", f_chakra(20, bold=True), fill=0, anchor="ra")
    d.line((452, 318, 738, 318), fill=0, width=2)

    dt(d, 452, 328, "MODEL 3: 79% (202 MI)", f_chakra(14, bold=True), fill=0)
    for b in range(10):
        bx = 452 + b * 28
        if b < 8:
            d.rectangle((bx, 352, bx + 22, 370), fill=0)
        else:
            d.rectangle((bx, 352, bx + 22, 370), outline=0, width=2)

    dt(d, 452, 384, "SOFTENER SALT: 63%", f_chakra(14, bold=True), fill=0)
    for b in range(10):
        bx = 452 + b * 28
        if b < 6:
            d.rectangle((bx, 408, bx + 22, 426), fill=0)
        else:
            d.rectangle((bx, 408, bx + 22, 426), outline=0, width=2)

    img.save(f"{OUT_DIR}/w1_07.png")


# ==============================================================================
# W1-08: "Star Trek LCARS / Sci-Fi Bridge Telemetry" (Sweeping L-Bars + BebasNeue)
# ==============================================================================
def render_w1_08():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Top LCARS Sweeping Elbow Frame (Black L-frame on Left + Top Bar)
    d.rounded_rectangle((12, 12, 788, 52), radius=20, fill=0)
    d.rounded_rectangle((12, 12, 168, 250), radius=28, fill=0)
    d.rounded_rectangle((108, 52, 796, 256), radius=24, fill=255)
    # White pill cutouts in the top LCARS bar
    d.rectangle((180, 12, 188, 52), fill=255)
    d.rectangle((568, 12, 576, 52), fill=255)
    dt(d, 200, 18, "LCARS // WOODGREEN OPS // SD 2026.10.18", f_bebas(26), fill=255)
    dt(d, 768, 18, "AQI 21 • UV 5.6", f_bebas(26), fill=255, anchor="ra")

    # Left L-Bar Numeric Codes
    dt(d, 26, 70, "01-840", f_bebas(22), fill=255)
    d.line((12, 102, 108, 102), fill=255, width=4)
    dt(d, 26, 114, "02-021", f_bebas(22), fill=255)
    d.line((12, 146, 108, 146), fill=255, width=4)
    dt(d, 26, 158, "03-790", f_bebas(22), fill=255)

    # Upper Bay (x=126..780, y=62..244): Atmospheric Telemetry (Weather + Hourly + 5-Day)
    dt(d, 130, 62, "84°F", f_bebas(72), fill=0)
    dt(d, 276, 98, MDI["sunny"], f_mdi(56), fill=0, anchor="mm")
    dt(d, 130, 136, "SUNNY // EXT HUMIDITY 21% RH", f_chakra(14, bold=True), fill=0)
    draw_wrapped(d, 130, 160, FORECAST_SUMMARY, f_book(14), 310, 19, fill=0, max_lines=4)

    d.line((456, 66, 456, 238), fill=0, width=2)
    dt(d, 472, 64, "CHRONO ATMOSPHERIC ARRAY", f_bebas(22), fill=0)
    for i, (ts, ic, tp) in enumerate(HOURLY):
        cx = 472 + i * 62 + 26
        d.rounded_rectangle((cx - 26, 94, cx + 26, 232), radius=12, outline=0, width=2)
        dt(d, cx, 104, ts, f_bebas(18), fill=0, anchor="ma")
        dt(d, cx, 152, MDI[ic], f_mdi(28), fill=0, anchor="mm")
        dt(d, cx, 192, f"{tp}°", f_bebas(26), fill=0, anchor="ma")

    # Lower LCARS Sweeping Elbow Frame (y=260..468)
    d.rounded_rectangle((12, 260, 788, 296), radius=18, fill=0)
    d.rounded_rectangle((12, 260, 168, 468), radius=28, fill=0)
    d.rounded_rectangle((108, 296, 796, 474), radius=24, fill=255)
    d.rectangle((180, 260, 188, 296), fill=255)
    d.rectangle((480, 260, 488, 296), fill=255)
    dt(d, 200, 265, "LIFE SUPPORT // 6-ZONE CLIMATE", f_bebas(24), fill=255)
    dt(d, 502, 265, "SHUTTLE & TIDAL TELEMETRY", f_bebas(24), fill=255)

    dt(d, 26, 316, "04-390", f_bebas(22), fill=255)
    d.line((12, 348, 108, 348), fill=255, width=4)
    dt(d, 26, 362, "05-202", f_bebas(22), fill=255)

    # Lower Left Bay (x=126..474, y=306..464): 6-Zone Pill Array
    sy = 308
    for idx, (_, caps, tp, rh, kind) in enumerate(ZONES):
        col = idx % 2
        row = idx // 2
        px = 126 + col * 174
        py = 308 + row * 52
        d.rounded_rectangle((px, py, px + 164, py + 44), radius=18, fill=0 if kind == "IN" else 255, outline=0, width=2)
        fg = 255 if kind == "IN" else 0
        dt(d, px + 16, py + 12, caps, f_bebas(20), fill=fg)
        dt(d, px + 150, py + 10, f"{tp}° / {rh}%", f_bebas(22), fill=fg, anchor="ra")

    # Lower Right Bay (x=496..780, y=308..464): Shuttle (Model 3, Commute) & Tides
    rows = [
        ("WORK SHUTTLE (ROSE)", "09 MIN"),
        ("WISH SHUTTLE (CENT)", "17 MIN"),
        ("MODEL 3 RESERVES", "79% / 202 MI"),
        ("SANTA MONICA TIDE", "HI 3:29P / LO 11:38P"),
        ("SOFTENER MATRIX", "63% NOMINAL"),
    ]
    ry = 308
    for lbl, val in rows:
        dt(d, 496, ry, lbl, f_chakra(13, bold=True), fill=0)
        dt(d, 776, ry - 2, val, f_bebas(22), fill=0, anchor="ra")
        ry += 31

    img.save(f"{OUT_DIR}/w1_08.png")


# ==============================================================================
# W1-09: "Japanese Shinkansen / JR East Station Information Board"
# ==============================================================================
def render_w1_09():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Top JR Station Banner
    d.rectangle((0, 0, 800, 54), fill=0)
    d.rounded_rectangle((16, 10, 74, 44), radius=6, fill=255)
    dt(d, 45, 27, "JR-WG", f_bebas(24), fill=0, anchor="mm")
    dt(d, 88, 12, "WOODGREEN CENTRAL // CLIMATE & TRANSIT", f_bebas(28), fill=255)
    dt(d, 780, 16, "SUN OCT 18 • 14:40", f_bold(15), fill=255, anchor="ra")

    # Track 1 (y=64..194): Weather + 5 Platform Hourly Boxes + 5-Day Summary
    dt(d, 20, 62, "84°F", f_bebas(68), fill=0)
    dt(d, 152, 94, MDI["sunny"], f_mdi(52), fill=0, anchor="mm")
    dt(d, 20, 130, "SUNNY • 21% RH", f_bold(14), fill=0)
    dt(d, 20, 150, "AQI 21 • UV 5.6 • 6 mph", f_book(13), fill=0)

    # 5 Platform Boxes for Hourly Forecast
    for i, (ts, ic, tp) in enumerate(HOURLY):
        bx = 212 + i * 68
        d.rectangle((bx, 66, bx + 62, 168), outline=0, width=2)
        d.rectangle((bx, 66, bx + 62, 88), fill=0)
        dt(d, bx + 31, 77, ts, f_bold(11), fill=255, anchor="mm")
        dt(d, bx + 31, 116, MDI[ic], f_mdi(28), fill=0, anchor="mm")
        dt(d, bx + 31, 144, f"{tp}°F", f_black(15), fill=0, anchor="ma")

    # Right Top: 5-Day Outlook Box
    d.rectangle((560, 66, 784, 168), outline=0, width=2)
    d.rectangle((560, 66, 784, 88), fill=0)
    dt(d, 570, 71, "5-DAY ADVISORY", f_bold(12), fill=255)
    draw_wrapped(d, 570, 94, FORECAST_SUMMARY, f_book(12), 204, 16, fill=0, max_lines=4)

    d.line((16, 180, 784, 180), fill=0, width=3)

    # Track 2 (y=190..316): "6-Car Shinkansen Train Consist" Representing the 6 Property Climate Zones!
    dt(d, 20, 190, "CLIMATE CONSIST // CARS 1–3 INDOOR  •  CARS 4–6 PERIMETER", f_bold(13), fill=0)
    # Nose cone on left + 6 connected train cars!
    zw = 118
    for i, (_, caps, tp, rh, kind) in enumerate(ZONES):
        cx0 = 44 + i * zw
        # Coupler between cars
        if i > 0:
            d.line((cx0 - 8, 258, cx0, 258), fill=0, width=6)
        d.rounded_rectangle((cx0, 214, cx0 + zw - 8, 304), radius=8, outline=0, width=3)
        d.rectangle((cx0, 214, cx0 + zw - 8, 238), fill=0 if kind == "IN" else 255, outline=0, width=2)
        dt(d, cx0 + (zw - 8) // 2, 226, f"CAR {i+1} • {caps}", f_bold(11), fill=255 if kind == "IN" else 0, anchor="mm")
        dt(d, cx0 + 12, 246, f"{tp}°F", f_bebas(28), fill=0)
        dt(d, cx0 + zw - 18, 248, f"{rh}%", f_black(17), fill=0, anchor="ra")
        # Wheel bogies underneath each car!
        d.ellipse((cx0 + 16, 304, cx0 + 28, 316), fill=0)
        d.ellipse((cx0 + zw - 34, 304, cx0 + zw - 22, 316), fill=0)

    # Rail track line underneath train
    d.line((16, 318, 784, 318), fill=0, width=3)

    # Track 3 (y=332..466): Route Diagrams for Commute + Model 3 + Santa Monica Tides
    # Left Box: Express Route Diagram
    d.rectangle((16, 332, 392, 464), outline=0, width=2)
    dt(d, 30, 342, "EXPRESS ROUTE TIMES", f_bold(13), fill=0)
    # Route 1: HOME ---> ROSE AVE
    d.ellipse((34, 372, 50, 388), fill=0)
    d.line((50, 380, 240, 380), fill=0, width=4)
    d.ellipse((240, 372, 256, 388), fill=255, outline=0, width=3)
    dt(d, 60, 362, "ROSE AVE (WORK)", f_bold(12), fill=0)
    dt(d, 376, 366, "9 MIN", f_bebas(28), fill=0, anchor="ra")

    # Route 2: HOME ---> CENTINELA
    d.ellipse((34, 422, 50, 438), fill=0)
    d.line((50, 430, 240, 430), fill=0, width=4)
    d.ellipse((240, 422, 256, 438), fill=255, outline=0, width=3)
    dt(d, 60, 412, "CENTINELA (WISH)", f_bold(12), fill=0)
    dt(d, 376, 416, "17 MIN", f_bebas(28), fill=0, anchor="ra")

    # Right Box: Rolling Stock (Model 3) + Coastal Tide Schedule
    d.rectangle((408, 332, 784, 464), outline=0, width=2)
    dt(d, 424, 342, "MODEL 3 BATTERY", f_bold(13), fill=0)
    dt(d, 768, 338, "79% • 202 MI", f_bebas(24), fill=0, anchor="ra")
    d.rectangle((424, 366, 768, 380), outline=0, width=2)
    d.rectangle((426, 368, 426 + int(340 * 0.79), 378), fill=0)

    dt(d, 424, 394, "SOFTENER SALT: 63%", f_bold(13), fill=0)
    dt(d, 768, 394, "HI TIDE 3:29 PM", f_bold(14), fill=0, anchor="ra")
    dt(d, 424, 424, "SANTA MONICA TIDES", f_book(13), fill=0)
    dt(d, 768, 424, "LO TIDE 11:38 PM", f_book(13), fill=0, anchor="ra")

    img.save(f"{OUT_DIR}/w1_09.png")


# ==============================================================================
# W1-10: "Editorial Magazine Poster / Giant Typography (DM Serif + Halftone Sun)"
# ==============================================================================
def render_w1_10():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Halftone dithered circle behind the giant temperature on the left
    px = img.load()
    cx_sun, cy_sun, r_sun = 160, 150, 96
    for y in range(cy_sun - r_sun, cy_sun + r_sun):
        for x in range(cx_sun - r_sun, cx_sun + r_sun):
            if (x - cx_sun) ** 2 + (y - cy_sun) ** 2 <= r_sun ** 2:
                if (x + y) % 2 == 0:
                    px[x, y] = 0

    # Giant DM Serif Display Hero Temperature
    dt(d, 28, 20, "SUNDAY, OCTOBER 18", f_bebas(26), fill=0)
    dt(d, 24, 52, "84°", f_serif(128), fill=0)
    d.rounded_rectangle((28, 210, 260, 244), radius=6, fill=0)
    dt(d, 144, 227, "SUNNY  •  21% RH  •  AQI 21", f_bold(13), fill=255, anchor="mm")

    # Editorial Narrative Forecast on Right Top (x=300..776, y=24..168)
    dt(d, 300, 20, "THE DAILY BRIEFING", f_bebas(24), fill=0)
    draw_wrapped(d, 300, 50, FORECAST_SUMMARY, f_serif(21, italic=True), 476, 28, fill=0, max_lines=3)

    # 5 Hourly Minimalist Columns (x=300..776, y=148..244)
    d.line((300, 144, 776, 144), fill=0, width=2)
    cw = 476 // 5
    for i, (ts, ic, tp) in enumerate(HOURLY):
        cx = 300 + i * cw + cw // 2
        dt(d, cx, 152, ts, f_bebas(18), fill=0, anchor="ma")
        dt(d, cx, 188, MDI[ic], f_mdi(28), fill=0, anchor="mm")
        dt(d, cx, 212, f"{tp}°F", f_serif(20), fill=0, anchor="ma")

    d.line((28, 258, 776, 258), fill=0, width=3)

    # Middle Strip (y=268..356): 6-Zone Editorial Ledger
    zw = 748 // 6
    for i, (_, caps, tp, rh, kind) in enumerate(ZONES):
        zx = 28 + i * zw
        if i > 0:
            d.line((zx, 272, zx, 352), fill=0, width=1)
        cx = zx + zw // 2
        dt(d, cx, 270, f"{caps} ({kind})", f_bebas(18), fill=0, anchor="ma")
        dt(d, cx, 294, f"{tp}°", f_serif(30), fill=0, anchor="ma")
        dt(d, cx, 332, f"{rh}% RH", f_serif(15, italic=True), fill=0, anchor="ma")

    d.line((28, 364, 776, 364), fill=0, width=2)

    # Bottom Strip (y=376..464): 4 Bold Magazine Callouts
    cols = [
        ("WORK COMMUTE", "9 min", "via Rose Ave"),
        ("WISH SCHOOL", "17 min", "via S Centinela"),
        ("TESLA MODEL 3", "79%", "202 mi • Salt 63%"),
        ("SANTA MONICA", "3:29 PM", "High Tide • Lo 11:38p"),
    ]
    bw = 748 // 4
    for i, (lbl, big, sub) in enumerate(cols):
        bx = 28 + i * bw
        if i > 0:
            d.line((bx - 10, 376, bx - 10, 460), fill=0, width=1)
        dt(d, bx, 374, lbl, f_bebas(18), fill=0)
        dt(d, bx, 396, big, f_serif(32), fill=0)
        dt(d, bx, 438, sub, f_serif(15, italic=True), fill=0)

    img.save(f"{OUT_DIR}/w1_10.png")


if __name__ == "__main__":
    render_w1_01()
    render_w1_02()
    render_w1_03()
    render_w1_04()
    render_w1_05()
    render_w1_06()
    render_w1_07()
    render_w1_08()
    render_w1_09()
    render_w1_10()
    print("Rendered all 10 Wild Round 1 Concepts (w1_01 .. w1_10)!")
