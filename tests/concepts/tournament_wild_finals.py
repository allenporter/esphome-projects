#!/usr/bin/env python3
"""Wild & Balanced Tournament Finals: 6 Cross-Bred Championship Concepts (wf_01 .. wf_06)."""

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
    px = img.load()
    for y in range(max(0, y0), min(480, y1)):
        for x in range(max(0, x0), min(800, x1)):
            if step == 2:
                if (x + y) % 2 == 0:
                    px[x, y] = 0
            elif step == 4:
                if (x % 2 == 0) and (y % 2 == 0):
                    px[x, y] = 0


# ==============================================================================
# WF-01: "Architectural Property Cutaway × Meteogram Sky"
# ==============================================================================
def render_wf_01():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Outer Blueprint Frame + Top Black Title Bar
    d.rectangle((10, 10, 790, 470), outline=0, width=2)
    d.rectangle((14, 14, 786, 50), fill=0)
    dt(d, 26, 21, "WOODGREEN ARCHITECTURAL TELEMETRY // SECTION VIEW", f_mono(17), fill=255)
    dt(d, 774, 21, "SUN OCT 18 • AQI 21 • UV 5.6", f_mono(15), fill=255, anchor="ra")

    # Sky Zone (y=56..148): Current Weather + 5-Day Summary (Left) | Smooth Hourly Curve (Right)
    dt(d, 28, 56, "84°F", f_bebas(64), fill=0)
    dt(d, 144, 82, MDI["sunny"], f_mdi(46), fill=0, anchor="mm")
    dt(d, 180, 60, "SUNNY • 21% OUT RH • 6 MPH", f_mono(14), fill=0)
    draw_wrapped(d, 180, 82, FORECAST_SUMMARY, f_book(13), 296, 17, fill=0, max_lines=3)

    # Smooth Hourly Trajectory Curve in the Right Sky (x=504..760)
    hx_pts = [516 + i * 58 for i in range(5)]
    hy_pts = [int(114 - (tp - 78) * 3.5) for _, _, tp in HOURLY]
    for i in range(4):
        d.line((hx_pts[i], hy_pts[i], hx_pts[i + 1], hy_pts[i + 1]), fill=0, width=2)
    for i, (ts, ic, tp) in enumerate(HOURLY):
        hx, hy = hx_pts[i], hy_pts[i]
        d.ellipse((hx - 3, hy - 3, hx + 3, hy + 3), fill=0)
        dt(d, hx, 64, ts, f_mono(11), fill=0, anchor="ma")
        dt(d, hx, 84, MDI[ic], f_mdi(20), fill=0, anchor="mm")
        dt(d, hx, hy + 10, f"{tp}°", f_bold(13), fill=0, anchor="ma")

    d.line((14, 146, 786, 146), fill=0, width=1)

    # Architectural Cross-Section (y=152..386)
    d.line((22, 334, 778, 334), fill=0, width=3)  # Ground line
    fill_dither(img, 22, 335, 778, 386, step=4)  # Earth hatching

    # Left Wing: Driveway + Carport with Tesla Model 3
    d.rectangle((36, 158, 214, 198), fill=255, outline=0, width=2)
    dt(d, 125, 164, "DRIVEWAY (OUT)", f_mono(12), fill=0, anchor="ma")
    dt(d, 125, 179, "84°F • 52% RH", f_bold(13), fill=0, anchor="ma")

    d.line((28, 222, 228, 204), fill=0, width=3)  # Carport roof
    d.line((36, 222, 36, 334), fill=0, width=2)
    d.rounded_rectangle((48, 232, 214, 324), radius=8, fill=0)
    dt(d, 60, 242, "TESLA MODEL 3", f_mono(13), fill=255)
    dt(d, 200, 240, "79%", f_bebas(28), fill=255, anchor="ra")
    dt(d, 60, 268, "Range: 202 mi", f_book(13), fill=255)
    d.rectangle((60, 294, 200, 308), outline=255, width=1)
    d.rectangle((62, 296, 62 + int(136 * 0.79), 306), fill=255)

    # Center Main House: Pitched Roof + 2F Loft + 1F Dining + B1 Crawlspace
    d.polygon([(224, 204), (380, 152), (536, 204)], outline=0, width=3)
    d.rectangle((234, 204, 526, 334), fill=255, outline=0, width=3)
    d.line((234, 268, 526, 268), fill=0, width=2)

    # 2F Loft
    dt(d, 250, 214, "2F // LOFT", f_mono(14), fill=0)
    dt(d, 510, 212, "78°F • 40% RH", f_black(16), fill=0, anchor="ra")
    d.rectangle((250, 242, 510, 254), outline=0, width=1)
    d.rectangle((252, 244, 252 + int(256 * 0.40), 252), fill=0)

    # 1F Dining + Water Softener
    dt(d, 250, 276, "1F // DINING", f_mono(14), fill=0)
    dt(d, 510, 274, "79°F • 47% RH", f_black(16), fill=0, anchor="ra")
    d.rectangle((250, 304, 412, 316), outline=0, width=1)
    d.rectangle((252, 306, 252 + int(158 * 0.47), 314), fill=0)
    dt(d, 510, 304, "Salt: 63%", f_mono(13), fill=0, anchor="ra")

    # B1 Crawlspace (Below ground)
    d.rectangle((234, 334, 526, 386), fill=255, outline=0, width=2)
    dt(d, 250, 350, "B1 // CRAWL", f_mono(14), fill=0)
    dt(d, 510, 348, "80°F • 31% RH", f_black(16), fill=0, anchor="ra")

    # Right Wing: Backyard Callout + Cabana Pavilion
    d.rectangle((548, 158, 766, 206), fill=255, outline=0, width=2)
    dt(d, 562, 166, "BACKYARD (OUT)", f_mono(13), fill=0)
    dt(d, 752, 166, "87°F", f_black(17), fill=0, anchor="ra")
    dt(d, 562, 184, "Humidity: 43% RH", f_bold(13), fill=0)

    d.polygon([(546, 242), (657, 214), (768, 242)], outline=0, width=3)
    d.rectangle((556, 242, 758, 334), fill=255, outline=0, width=2)
    dt(d, 657, 252, "CABANA PAVILION", f_mono(13), fill=0, anchor="ma")
    dt(d, 657, 274, "73°F • 68% RH", f_black(17), fill=0, anchor="ma")
    d.rectangle((576, 306, 738, 318), outline=0, width=1)
    d.rectangle((578, 308, 578 + int(158 * 0.68), 316), fill=0)

    # Bottom Black Blueprint Footer (y=394..462)
    d.rectangle((22, 394, 778, 462), fill=0)
    dt(d, 38, 406, "WORK (ROSE AVE)", f_mono(14), fill=255)
    dt(d, 260, 400, "9 MIN", f_bebas(28), fill=255, anchor="ra")
    dt(d, 38, 434, "WISH (CENTINELA)", f_mono(14), fill=255)
    dt(d, 260, 428, "17 MIN", f_bebas(28), fill=255, anchor="ra")

    d.line((284, 402, 284, 454), fill=255, width=1)
    dt(d, 304, 406, "SANTA MONICA TIDES", f_mono(14), fill=255)
    dt(d, 304, 432, "HI 3:29 PM  •  LO 11:38 PM", f_bold(15), fill=255)
    wpts = []
    for px in range(560, 760, 4):
        t = (px - 560) / 200.0
        py = 428 - int(15 * math.sin((t - 0.08) * 1.8 * math.pi))
        wpts.append((px, py))
    d.line(wpts, fill=255, width=2)
    hx, hy = wpts[16]
    d.ellipse((hx - 4, hy - 4, hx + 4, hy + 4), fill=255)

    img.save(f"{OUT_DIR}/wf_01.png")


# ==============================================================================
# WF-02: "Solari Split-Flap × JR Express Departure Board"
# ==============================================================================
def draw_flap_string(d, x, y, text, cw=24, ch=36, font=None):
    if font is None:
        font = f_bebas(30)
    for i, ch_str in enumerate(text):
        fx = x + i * (cw + 3)
        d.rounded_rectangle((fx, y, fx + cw, y + ch), radius=3, fill=0)
        dt(d, fx + cw // 2, y + ch // 2, ch_str, font, fill=255, anchor="mm")
        d.line((fx, y + ch // 2, fx + cw, y + ch // 2), fill=255, width=1)


def render_wf_02():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    d.rectangle((10, 10, 790, 470), outline=0, width=3)
    d.rectangle((10, 10, 790, 56), fill=0)
    d.rounded_rectangle((22, 18, 76, 48), radius=5, fill=255)
    dt(d, 49, 33, "WG-01", f_bebas(22), fill=0, anchor="mm")
    dt(d, 90, 18, "WOODGREEN // SPLIT-FLAP TELEMETRY", f_bebas(28), fill=255)
    dt(d, 774, 22, "SUN 18 OCT • AQI 21 • UV 5.6", f_mono(15), fill=255, anchor="ra")

    # Top Section (y=66..190): Weather Flap + 5-Day Summary (Left) | 5 Hourly Flaps (Right)
    draw_flap_string(d, 26, 68, "84F SUNNY", cw=26, ch=42, font=f_bebas(34))
    dt(d, 26, 118, "OUTSIDE: 21% RH  •  WIND: 6 MPH", f_mono(14), fill=0)
    draw_wrapped(d, 26, 140, FORECAST_SUMMARY, f_book(13), 360, 17, fill=0, max_lines=3)

    d.line((404, 64, 404, 190), fill=0, width=2)
    dt(d, 420, 66, "HOURLY FORECAST FLAPS", f_mono(13), fill=0)
    for i, (ts, ic, tp) in enumerate(HOURLY):
        cx = 420 + i * 72 + 28
        dt(d, cx, 86, ts, f_mono(12), fill=0, anchor="ma")
        dt(d, cx, 118, MDI[ic], f_mdi(26), fill=0, anchor="mm")
        draw_flap_string(d, cx - 26, 140, f"{tp}", cw=24, ch=36, font=f_bebas(28))

    d.line((10, 196, 790, 196), fill=0, width=2)

    # Middle Section (y=204..346): 6-Car Split-Flap Climate Consist!
    dt(d, 26, 204, "6-ZONE CLIMATE CONSIST // INDOOR (1-3) & PERIMETER (4-6)", f_mono(13), fill=0)
    zw = 122
    for i, (_, caps, tp, rh, kind) in enumerate(ZONES):
        zx = 26 + i * zw
        d.rounded_rectangle((zx, 226, zx + zw - 8, 336), radius=6, outline=0, width=2)
        d.rectangle((zx, 226, zx + zw - 8, 248), fill=0 if kind == "IN" else 255, outline=0, width=2)
        dt(d, zx + (zw - 8) // 2, 237, f"{caps} • {kind}", f_mono(12), fill=255 if kind == "IN" else 0, anchor="mm")
        # 2-digit Flap for Temp on left + Bold RH% on right
        draw_flap_string(d, zx + 8, 258, f"{tp}", cw=20, ch=32, font=f_bebas(24))
        dt(d, zx + 104, 274, f"{rh}%", f_bebas(26), fill=0, anchor="rm")
        # Mini comfort bar
        d.rectangle((zx + 10, 306, zx + zw - 18, 318), outline=0, width=1)
        d.rectangle((zx + 12, 308, zx + 12 + int((zw - 32) * (rh / 100.0)), 316), fill=0)

    d.line((10, 348, 790, 348), fill=0, width=2)

    # Bottom Section (y=358..460): 4 Split-Flap Departure Modules
    mods = [
        ("WORK (ROSE AVE)", "09 MIN"),
        ("WISH (CENTINELA)", "17 MIN"),
        ("MODEL 3 (202 MI)", "79 PCT"),
        ("HI TIDE (LO 11:38)", "03:29P"),
    ]
    mw = 756 // 4
    for i, (lbl, fval) in enumerate(mods):
        mx = 24 + i * mw
        if i > 0:
            d.line((mx - 8, 356, mx - 8, 424), fill=0, width=1)
        dt(d, mx, 358, lbl, f_mono(13), fill=0)
        draw_flap_string(d, mx, 380, fval, cw=24, ch=36, font=f_bebas(28))

    d.line((24, 428, 776, 428), fill=0, width=1)
    dt(d, 24, 436, "SOFTENER SALT LEVEL: 63% [OK]  •  SANTA MONICA PIER STATION", f_mono(13), fill=0)

    img.save(f"{OUT_DIR}/wf_02.png")


# ==============================================================================
# WF-03: "R-P1 Split-Contrast × Yr.no Halftone Meteogram"
# ==============================================================================
def render_wf_03():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Left Solid Black Sidebar (x=0..256): Date, Weather Hero, 6-Zone Temp + White RH% Pill Table
    d.rectangle((0, 0, 256, 480), fill=0)
    dt(d, 22, 16, "SUNDAY", f_black(24), fill=255)
    dt(d, 22, 44, "OCTOBER 18", f_book(16), fill=255)
    d.line((22, 68, 234, 68), fill=255, width=1)

    dt(d, 20, 74, "84°", f_black(72), fill=255)
    dt(d, 200, 114, MDI["sunny"], f_mdi(64), fill=255, anchor="mm")
    dt(d, 22, 160, "SUNNY • 21% RH", f_bold(16), fill=255)
    dt(d, 22, 184, "AQI 21 GOOD • UV 5.6", f_book(13), fill=255)
    d.line((22, 208, 234, 208), fill=255, width=1)

    dt(d, 22, 218, "CLIMATE ZONES", f_bold(12), fill=255)
    dt(d, 234, 218, "TEMP / RH", f_book(11), fill=255, anchor="ra")
    sy = 240
    for idx, (name, _, tp, rh, _) in enumerate(ZONES):
        if idx == 3:
            d.line((22, sy - 4, 234, sy - 4), fill=255, width=1)
            sy += 4
        dt(d, 22, sy + 2, name, f_book(14), fill=255)
        dt(d, 174, sy + 1, f"{tp}°", f_bold(16), fill=255, anchor="ra")
        d.rounded_rectangle((182, sy, 234, sy + 22), radius=5, fill=255)
        dt(d, 208, sy + 11, f"{rh}%", f_black(13), fill=0, anchor="mm")
        sy += 38

    # Right Top (x=280..776, y=16..204): Sweeping Yr.no Halftone Meteogram Curve!
    dt(d, 280, 16, "HOURLY METEOGRAM & OUTLOOK", f_black(16), fill=0)
    dt(d, 776, 18, "Wind 6 mph • Updated 2:40p", f_spacemono(11), fill=0, anchor="ra")
    d.line((280, 40, 776, 40), fill=0, width=2)

    anchor_x = [316, 422, 528, 634, 740]
    anchor_t = [84, 84, 83, 81, 79]
    anchor_y = [int(136 - (t - 77) * 7) for t in anchor_t]

    curve_pts = []
    px_access = img.load()
    for x in range(296, 760):
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
        for y in range(cy + 2, 164):
            if (x % 3 == 0) and (y % 3 == 0):
                px_access[x, y] = 0

    d.line(curve_pts, fill=0, width=3)
    for i, (ts, ic, tp) in enumerate(HOURLY):
        nx, ny = anchor_x[i], anchor_y[i]
        d.ellipse((nx - 5, ny - 5, nx + 5, ny + 5), fill=255, outline=0, width=3)
        dt(d, nx, ny - 24, MDI[ic], f_mdi(24), fill=0, anchor="mm")
        dt(d, nx + 24, ny - 14, f"{tp}°", f_black(14), fill=0, anchor="mm")
        dt(d, nx, 174, ts, f_spacemono(11, bold=True), fill=0, anchor="mm")

    d.line((280, 196, 776, 196), fill=0, width=2)

    # Right Middle (y=206..272): 5-Day Forecast Summary
    draw_wrapped(d, 280, 208, FORECAST_SUMMARY, f_book(15), 496, 21, fill=0, max_lines=3)
    d.line((280, 276, 776, 276), fill=0, width=2)

    # Right Bottom (y=290..464): 3 R-P1 Rounded Gauge Cards
    # Card 1: Commute
    d.rounded_rectangle((280, 290, 436, 464), radius=10, outline=0, width=2)
    dt(d, 294, 304, "COMMUTE", f_bold(13), fill=0)
    dt(d, 294, 328, "9 min", f_black(24), fill=0)
    dt(d, 294, 358, "Work (Rose Ave)", f_book(13), fill=0)
    d.line((294, 382, 422, 382), fill=0, width=1)
    dt(d, 294, 392, "17 min", f_black(24), fill=0)
    dt(d, 294, 422, "WISH (Centinela)", f_book(13), fill=0)

    # Card 2: Model 3 & Softener
    d.rounded_rectangle((450, 290, 606, 464), radius=10, outline=0, width=2)
    dt(d, 464, 304, "MODEL 3", f_bold(13), fill=0)
    dt(d, 464, 328, "79%", f_black(26), fill=0)
    dt(d, 592, 336, "202 mi", f_bold(14), fill=0, anchor="ra")
    d.rectangle((464, 364, 592, 376), outline=0, width=2)
    d.rectangle((466, 366, 466 + int(124 * 0.79), 374), fill=0)
    dt(d, 464, 394, "SOFTENER", f_bold(12), fill=0)
    dt(d, 592, 394, "63%", f_bold(14), fill=0, anchor="ra")
    d.rectangle((464, 418, 592, 430), outline=0, width=2)
    d.rectangle((466, 420, 466 + int(124 * 0.63), 428), fill=0)

    # Card 3: Santa Monica Tides
    d.rounded_rectangle((620, 290, 776, 464), radius=10, outline=0, width=2)
    dt(d, 634, 304, "SANTA MONICA", f_bold(13), fill=0)
    dt(d, 634, 328, "3:29 PM", f_black(22), fill=0)
    dt(d, 634, 356, "High Tide", f_book(13), fill=0)
    wpts = []
    for px in range(634, 762, 4):
        t = (px - 634) / 128.0
        py = 400 - int(12 * math.sin((t - 0.05) * 1.8 * math.pi))
        wpts.append((px, py))
    d.line(wpts, fill=0, width=2)
    dt(d, 634, 428, "Low: 11:38 PM", f_bold(13), fill=0)

    img.save(f"{OUT_DIR}/wf_03.png")


# ==============================================================================
# WF-04: "The Woodgreen Editorial Broadsheet & Almanac" (DM Serif + Bebas Neue)
# ==============================================================================
def render_wf_04():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Double editorial border
    d.rectangle((10, 10, 790, 470), outline=0, width=2)

    # Halftone sun behind giant serif temperature
    px = img.load()
    cx_sun, cy_sun, r_sun = 156, 138, 82
    for y in range(cy_sun - r_sun, cy_sun + r_sun):
        for x in range(cx_sun - r_sun, cx_sun + r_sun):
            if (x - cx_sun) ** 2 + (y - cy_sun) ** 2 <= r_sun ** 2:
                if (x + y) % 2 == 0:
                    px[x, y] = 0

    dt(d, 28, 20, "SUNDAY, OCTOBER 18", f_bebas(24), fill=0)
    dt(d, 24, 48, "84°", f_serif(116), fill=0)
    d.rounded_rectangle((28, 194, 260, 226), radius=6, fill=0)
    dt(d, 144, 210, "SUNNY  •  21% RH  •  AQI 21", f_bold(13), fill=255, anchor="mm")

    # Top-Right Editorial Briefing + 5 Hourly Columns
    dt(d, 296, 20, "FIVE-DAY WEATHER BRIEFING", f_bebas(22), fill=0)
    dt(d, 772, 22, "UV Index 5.6  •  Wind 6 mph", f_serif(15, italic=True), fill=0, anchor="ra")
    draw_wrapped(d, 296, 46, FORECAST_SUMMARY, f_serif(19, italic=True), 476, 24, fill=0, max_lines=3)

    d.line((296, 128, 772, 128), fill=0, width=2)
    cw = 476 // 5
    for i, (ts, ic, tp) in enumerate(HOURLY):
        cx = 296 + i * cw + cw // 2
        if i > 0:
            d.line((296 + i * cw, 136, 296 + i * cw, 222), fill=0, width=1)
        dt(d, cx, 134, ts, f_bebas(18), fill=0, anchor="ma")
        dt(d, cx, 170, MDI[ic], f_mdi(28), fill=0, anchor="mm")
        dt(d, cx, 194, f"{tp}°F", f_serif(20), fill=0, anchor="ma")

    d.line((24, 238, 776, 238), fill=0, width=3)

    # Middle Tier (y=248..354): 6-Zone Chamber & Garden Register with IN/OUT Pill Headers
    zw = 752 // 6
    for i, (_, caps, tp, rh, kind) in enumerate(ZONES):
        zx = 24 + i * zw
        if i > 0:
            d.line((zx, 252, zx, 348), fill=0, width=1)
        cx = zx + zw // 2
        if kind == "IN":
            d.rounded_rectangle((cx - 48, 250, cx + 48, 272), radius=4, fill=0)
            dt(d, cx, 261, f"{caps} • IN", f_bebas(16), fill=255, anchor="mm")
        else:
            d.rounded_rectangle((cx - 48, 250, cx + 48, 272), radius=4, outline=0, width=1)
            dt(d, cx, 261, f"{caps} • OUT", f_bebas(16), fill=0, anchor="mm")
        dt(d, cx, 278, f"{tp}°F", f_serif(28), fill=0, anchor="ma")
        dt(d, cx, 318, f"{rh}% RH", f_serif(16, italic=True), fill=0, anchor="ma")

    d.line((24, 358, 776, 358), fill=0, width=2)

    # Bottom Tier (y=368..458): 4 Bold Magazine Columns
    cols = [
        ("WORK COMMUTE", "9 min", "via Rose Ave"),
        ("WISH SCHOOL", "17 min", "via S Centinela"),
        ("TESLA MODEL 3", "79%", "202 mi • Salt 63%"),
        ("SANTA MONICA", "3:29 PM", "High Tide • Lo 11:38p"),
    ]
    bw = 752 // 4
    for i, (lbl, big, sub) in enumerate(cols):
        bx = 28 + i * bw
        if i > 0:
            d.line((bx - 10, 368, bx - 10, 456), fill=0, width=1)
        dt(d, bx, 368, lbl, f_bebas(18), fill=0)
        dt(d, bx, 390, big, f_serif(30), fill=0)
        dt(d, bx, 432, sub, f_serif(15, italic=True), fill=0)

    img.save(f"{OUT_DIR}/wf_04.png")


# ==============================================================================
# WF-05: "1984 Macintosh System 1 / HyperCard Desktop v2"
# ==============================================================================
def draw_mac_window(img, d, x0, y0, x1, y1, title):
    d.rectangle((x0 + 4, y0 + 4, x1 + 4, y1 + 4), fill=0)
    d.rectangle((x0, y0, x1, y1), fill=255, outline=0, width=2)
    d.rectangle((x0, y0, x1, y0 + 26), fill=255, outline=0, width=2)
    for py in range(y0 + 4, y0 + 23, 2):
        d.line((x0 + 6, py, x1 - 6, py), fill=0, width=1)
    d.rectangle((x0 + 10, y0 + 6, x0 + 24, y0 + 20), fill=255, outline=0, width=2)
    tw = len(title) * 9 + 20
    cx = (x0 + x1) // 2
    d.rectangle((cx - tw // 2, y0 + 3, cx + tw // 2, y0 + 23), fill=255)
    dt(d, cx, y0 + 13, title, f_silk(12, bold=True), fill=0, anchor="mm")


def render_wf_05():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    fill_dither(img, 0, 28, 800, 480, step=2)

    # Top Menu Bar
    d.rectangle((0, 0, 800, 28), fill=255, outline=0, width=2)
    dt(d, 16, 7, "WOODGREEN OS  File  Edit  View  Weather  Sensors", f_silk(12, bold=True), fill=0)
    dt(d, 784, 7, "Sun Oct 18  2:40 PM", f_silk(12, bold=True), fill=0, anchor="ra")

    # Window 1: Weather.stk
    draw_mac_window(img, d, 16, 40, 428, 278, "Weather.stk")
    dt(d, 34, 74, "84°F", f_vt(68), fill=0)
    dt(d, 184, 104, MDI["sunny"], f_mdi(52), fill=0, anchor="mm")
    dt(d, 228, 78, "SUNNY", f_silk(14, bold=True), fill=0)
    dt(d, 228, 98, "Out RH: 21% • UV 5.6", f_vt(18), fill=0)
    dt(d, 228, 116, "AQI 21 Good • 6 mph", f_vt(18), fill=0)

    d.line((30, 142, 414, 142), fill=0, width=1)
    for i, (ts, ic, tp) in enumerate(HOURLY):
        cx = 34 + i * 76 + 34
        dt(d, cx, 148, ts, f_silk(10), fill=0, anchor="ma")
        dt(d, cx, 176, MDI[ic], f_mdi(24), fill=0, anchor="mm")
        dt(d, cx, 194, f"{tp}°F", f_vt(20), fill=0, anchor="ma")

    d.line((30, 218, 414, 218), fill=0, width=1)
    draw_wrapped(d, 30, 224, FORECAST_SUMMARY, f_vt(17), 384, 16, fill=0, max_lines=3)

    # Window 2: HomeClimate.da (with 40-60% comfort ticks!)
    draw_mac_window(img, d, 446, 40, 780, 294, "HomeClimate.da")
    sy = 76
    for idx, (name, _, tp, rh, kind) in enumerate(ZONES):
        if idx == 3:
            d.line((462, sy - 3, 764, sy - 3), fill=0, width=1)
            sy += 4
        short = "Crawl" if name == "Crawlspace" else name
        dt(d, 462, sy, f"{short} ({kind})", f_silk(11, bold=(kind == "IN")), fill=0)
        dt(d, 636, sy - 2, f"{tp}°F", f_vt(22), fill=0, anchor="ra")
        bx, by, bw = 646, sy + 2, 68
        d.rectangle((bx, by, bx + bw, by + 14), outline=0, width=1)
        d.rectangle((bx + 1, by + 1, bx + 1 + int((bw - 2) * (rh / 100.0)), by + 13), fill=0)
        for pct in (40, 60):
            kx = bx + int(bw * (pct / 100.0))
            d.line((kx, by - 2, kx, by + 16), fill=0, width=1)
        dt(d, 766, sy - 2, f"{rh}%", f_vt(22), fill=0, anchor="ra")
        sy += 34

    # Window 3: Commute_Tides
    draw_mac_window(img, d, 16, 294, 428, 464, "Commute_Tides")
    dt(d, 32, 332, "Work (Rose Ave):", f_silk(11), fill=0)
    dt(d, 226, 328, "9 MIN", f_vt(26), fill=0, anchor="ra")
    dt(d, 32, 362, "WISH (Centinela):", f_silk(11), fill=0)
    dt(d, 226, 358, "17 MIN", f_vt(26), fill=0, anchor="ra")
    d.line((32, 390, 412, 390), fill=0, width=1)
    dt(d, 32, 402, "Santa Monica High Tide: 3:29 PM", f_vt(20), fill=0)
    dt(d, 32, 426, "Low Tide: 11:38 PM", f_vt(18), fill=0)
    wpts = []
    for px in range(250, 410, 4):
        t = (px - 250) / 160.0
        py = 362 - int(16 * math.sin((t - 0.08) * 1.8 * math.pi))
        wpts.append((px, py))
    d.line(wpts, fill=0, width=2)

    # Window 4: Systems.ctrl
    draw_mac_window(img, d, 446, 312, 780, 464, "Systems.ctrl")
    dt(d, 462, 348, "TESLA MODEL 3", f_silk(11, bold=True), fill=0)
    dt(d, 764, 344, "79% (202 mi)", f_vt(22), fill=0, anchor="ra")
    d.rectangle((462, 370, 764, 386), outline=0, width=2)
    fill_dither(img, 464, 372, 464 + int(298 * 0.79), 384, step=2)

    dt(d, 462, 398, "SOFTENER SALT", f_silk(11, bold=True), fill=0)
    dt(d, 764, 394, "63%", f_vt(22), fill=0, anchor="ra")
    d.rectangle((462, 420, 764, 436), outline=0, width=2)
    fill_dither(img, 464, 422, 464 + int(298 * 0.63), 434, step=2)

    img.save(f"{OUT_DIR}/wf_05.png")


# ==============================================================================
# WF-06: "Casio G-Shock × Teenage Engineering Field Chrono v2"
# ==============================================================================
def render_wf_06():
    img = Image.new("L", (800, 480), 255)
    d = ImageDraw.Draw(img)

    # Octagonal Watch Bezel
    d.rectangle((0, 0, 800, 480), fill=0)
    bezel = [(36, 12), (764, 12), (788, 36), (788, 444), (764, 468), (36, 468), (12, 444), (12, 36)]
    d.polygon(bezel, fill=255, outline=0)
    inner = [(44, 20), (756, 20), (780, 44), (780, 436), (756, 460), (44, 460), (20, 436), (20, 44)]
    d.polygon(inner, fill=255, outline=0, width=3)

    d.rectangle((48, 28, 752, 62), fill=0)
    dt(d, 60, 35, "FIELD CHRONO // WOODGREEN TELEMETRY", f_chakra(16, bold=True), fill=255)
    dt(d, 740, 35, "SUN 10-18  •  AQI 21  •  UV 5.6", f_chakra(15, bold=True), fill=255, anchor="ra")

    # Sub-Bezel 1 (Top-Left): Weather + 5 Hourly Icons
    d.rounded_rectangle((48, 72, 320, 268), radius=8, outline=0, width=3)
    dt(d, 62, 80, "84°F", f_chakra(56, bold=True), fill=0)
    dt(d, 272, 112, MDI["sunny"], f_mdi(52), fill=0, anchor="mm")
    dt(d, 62, 144, "SUNNY • 21% OUT RH", f_chakra(14, bold=True), fill=0)
    dt(d, 62, 164, "WIND 6 MPH • BARO STEADY", f_chakra(12, bold=False), fill=0)
    d.line((62, 186, 306, 186), fill=0, width=2)
    for i, (ts, ic, tp) in enumerate(HOURLY):
        cx = 64 + i * 48 + 20
        dt(d, cx, 194, ts[:3], f_chakra(11, bold=True), fill=0, anchor="ma")
        dt(d, cx, 222, MDI[ic], f_mdi(22), fill=0, anchor="mm")
        dt(d, cx, 240, f"{tp}°", f_chakra(14, bold=True), fill=0, anchor="ma")

    # Sub-Bezel 2 (Top-Right): 6-Zone Hygro-Thermo Matrix
    d.rounded_rectangle((334, 72, 752, 268), radius=8, outline=0, width=3)
    d.rectangle((334, 72, 752, 98), fill=0)
    dt(d, 348, 77, "6-ZONE HYGRO-THERMO MATRIX", f_chakra(14, bold=True), fill=255)
    dt(d, 738, 77, "INDOOR / OUTDOOR", f_chakra(12, bold=True), fill=255, anchor="ra")

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
        d.rectangle((zx + 10, zy + 62, zx + cw - 12, zy + 72), outline=0, width=1)
        d.rectangle((zx + 12, zy + 64, zx + 12 + int((cw - 26) * (rh / 100.0)), zy + 70), fill=0)

    # Sub-Bezel 3 (Bottom-Left): 5-Day Outlook + Santa Monica Tide Graph
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

    # Sub-Bezel 4 (Bottom-Right): Commute + Model 3 + Softener Salt
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

    img.save(f"{OUT_DIR}/wf_06.png")


if __name__ == "__main__":
    render_wf_01()
    render_wf_02()
    render_wf_03()
    render_wf_04()
    render_wf_05()
    render_wf_06()
    print("Rendered all 6 Wild & Balanced Finalists (wf_01 .. wf_06)!")
