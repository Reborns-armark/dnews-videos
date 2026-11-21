"""Visuals for the Hera / DART episode (vertical coordinate system, CX=540, CY=960)."""
import math, random
from common4 import *
from engine import pil_to_surface
from space2 import pin, CX, CY, STARPAL, v_comment
from space3 import probe, eyes
from space import planet

ROCK = "#9C8C7A"
ROCK2 = "#7A6C5E"
EARTH = "#3FA9F5"


def rock(ctx, x, y, r, seed=1, col=ROCK, ridge=False, boulders=0, rot=0.0):
    rnd = random.Random(seed)
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ctx.new_path()
    n = 18
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n
        rr = r * (0.86 + 0.14 * rnd.random())
        pts.append((rr * math.cos(a), rr * math.sin(a)))
    ctx.move_to(*pts[0])
    for k in range(1, n + 1):
        x0, y0 = pts[k - 1]; x1, y1 = pts[k % n]
        ctx.curve_to(x0 + (x1 - x0) * 0.33, y0 + (y1 - y0) * 0.33, x0 + (x1 - x0) * 0.66, y0 + (y1 - y0) * 0.66, x1, y1)
    ctx.close_path()
    fill_stroke(ctx, col, lw=max(4, r * 0.04))
    for k in range(int(3 + r / 40)):
        cx_, cy_ = rnd.uniform(-0.55, 0.55) * r, rnd.uniform(-0.55, 0.55) * r
        cr = rnd.uniform(0.06, 0.15) * r
        ctx.new_path(); ctx.arc(cx_, cy_, cr, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(ROCK2)); ctx.fill()
    for k in range(boulders):
        bx, by = rnd.uniform(-0.6, 0.6) * r, rnd.uniform(-0.6, 0.6) * r
        if bx * bx + by * by < (0.7 * r) ** 2:
            ctx.new_path(); ctx.arc(bx, by, rnd.uniform(0.04, 0.08) * r, 0, 2 * math.pi)
            ctx.set_source_rgba(*hexc("#5E5247")); ctx.fill()
    if ridge:
        ctx.move_to(-r * 0.95, 0); ctx.curve_to(-r * 0.4, -r * 0.08, r * 0.4, -r * 0.08, r * 0.95, 0)
        ctx.set_source_rgba(*hexc("#C9B79F")); ctx.set_line_width(r * 0.06); ctx.stroke()
    ctx.restore()


def hera(ctx, x, y, s, gt, mag=False):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(0.06 * math.sin(gt * 2))
    for side in (-1, 1):
        rrect(ctx, side * 70 - (110 if side < 0 else 0), -36, 110, 72, 8); fill_stroke(ctx, "#3D5BFF", lw=6)
        for k in range(3):
            ctx.move_to(side * 70 - (110 if side < 0 else 0) + 27 * (k + 1), -36); ctx.rel_line_to(0, 72)
        ctx.set_source_rgba(1, 1, 1, 0.5); ctx.set_line_width(3); ctx.stroke()
    rrect(ctx, -70, -70, 140, 140, 18); fill_stroke(ctx, "#F2C14E", lw=8)
    circle(ctx, 0, -10, 30, "#FFFFFF", lw=6); circle(ctx, 0, -10, 14, "#1B1B3A", lw=0)
    draw_sprite(ctx, text_sprite("ESA", 30, color="#1B1B3A", stroke="#FFFFFF", stroke_w=3, shadow=False, path=FONTS["dela"]), 0, 45, 1, 1)
    if mag:
        ctx.save(); ctx.translate(95, 60); ctx.rotate(-0.6)
        circle(ctx, 0, 0, 46, "#BFE9FF", lw=8)
        rrect(ctx, -10, 44, 20, 70, 8); fill_stroke(ctx, "#8A5A2B", lw=6)
        ctx.restore()
    ctx.restore()


def dart(ctx, x, y, s, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    for side in (-1, 1):
        rrect(ctx, -12, side * 50 - (90 if side < 0 else 0), 24, 90, 6); fill_stroke(ctx, "#3D5BFF", lw=5)
    rrect(ctx, -50, -40, 100, 80, 12); fill_stroke(ctx, "#E8E8F0", lw=7)
    draw_sprite(ctx, text_sprite("DART", 26, color="#1B1B3A", stroke="#FFFFFF", stroke_w=3, shadow=False, path=FONTS["dela"]), 0, 0, 1, 1)
    ctx.restore()


def space_bg(ctx, gt):
    rnd = random.Random(9)
    for k in range(40):
        star(ctx, rnd.uniform(40, 1040), rnd.uniform(420, 1500), rnd.uniform(4, 9) * (0.6 + 0.4 * math.sin(gt * 3 + k)), "#FFFFFF", 0.8)


def label(ctx, t, x, y, size=80, color="#FFFFFF", hi="#FFE14D", s=1.0, rot=0.0, font="dela"):
    draw_sprite(ctx, text_sprite(t, size, color=color, hi=hi, path=FONTS[font]), x, y, s, 1, rot)


def pair(ctx, gt, cx=CX, cy=CY, s=1.0, orbit=True, ridge=True, boulders=8):
    rock(ctx, cx, cy, 230 * s, seed=3, ridge=ridge, boulders=boulders, rot=gt * 0.25)
    a = gt * 0.9
    if orbit:
        ctx.save(); ctx.translate(cx, cy); ctx.scale(1, 0.35)
        ctx.new_path(); ctx.arc(0, 0, 380 * s, 0, 2 * math.pi); ctx.restore()
        ctx.set_source_rgba(1, 1, 1, 0.35); ctx.set_line_width(5); ctx.set_dash([14, 12]); ctx.stroke(); ctx.set_dash([])
    mx, my = cx + 380 * s * math.cos(a), cy + 133 * s * math.sin(a)
    rock(ctx, mx, my, 60 * s, seed=7, col="#B3A28E")
    return mx, my


# ---------------------------------------------------------------- scenes
def v_hook_crash(ctx, lt, d, gt):
    space_bg(ctx, gt)
    p = clamp(lt / max(0.9, d * 0.5))
    rock(ctx, CX + 120, CY + 60, 150 * pin(lt), seed=7, col="#B3A28E")
    if p < 1:
        dart(ctx, CX - 420 + 520 * p, CY - 380 + 420 * p, 1.2, 0.7)
    else:
        burst(ctx, CX + 60, CY + 20, 300 + 60 * math.sin(lt * 20), gt, "#FFE14D")
        sparkles(ctx, CX + 60, CY + 20, lt, 0.0, "#FFB34D", 22, 520)
        label(ctx, "ドカーン!", CX, CY - 380, 130, color="#FF3D7F", s=pin(lt - d * 0.5), rot=-0.1)


def v_detective(ctx, lt, d, gt):
    space_bg(ctx, gt)
    pair(ctx, gt, CX + 140, CY + 170, 0.6)
    hera(ctx, CX - 230, CY - 230 + 20 * math.sin(gt * 2), 1.3 * pin(lt), gt, mag=True)
    label(ctx, "現場検証!", CX + 120, CY - 420, 110, s=pin(lt, 0.2), rot=0.06)


def v_pair(ctx, lt, d, gt):
    space_bg(ctx, gt)
    mx, my = pair(ctx, gt, CX, CY + 40, 1.0 * pin(lt))
    label(ctx, "ディディモス", CX, CY + 330, 64, s=pin(lt, 0.2), font="mochiy")
    draw_sprite(ctx, text_sprite("ディモルフォス", 44, path=FONTS["mochiy"]), mx, my - 90, pin(lt, 0.35), 1)


def tower(ctx, x, base, h):
    w = h * 0.32
    ctx.move_to(x - w / 2, base); ctx.line_to(x - w * 0.08, base - h); ctx.line_to(x + w * 0.08, base - h); ctx.line_to(x + w / 2, base); ctx.close_path()
    fill_stroke(ctx, "#FF5A3C", lw=6)
    for k in range(1, 5):
        yy = base - h * k / 5
        ww = w * (1 - k / 5) / 2 + w * 0.08
        ctx.move_to(x - ww, yy); ctx.line_to(x + ww, yy)
    ctx.set_source_rgba(1, 1, 1, 0.9); ctx.set_line_width(6); ctx.stroke()


def v_sizes(ctx, lt, d, gt):
    base = CY + 420
    ctx.rectangle(40, base, 1000, 14); ctx.set_source_rgba(1, 1, 1, 0.7); ctx.fill()
    k = 0.92  # px per metre
    rock(ctx, 330, base - 780 * k / 2, 780 * k / 2 * pin(lt), seed=3, ridge=True)
    tower(ctx, 760, base, 333 * k * pin(lt, 0.15))
    rock(ctx, 930, base - 151 * k / 2, 151 * k / 2 * pin(lt, 0.3), seed=7, col="#B3A28E")
    draw_sprite(ctx, text_sprite("780m", 60, path=FONTS["dela"]), 330, base - 780 * k - 40, pin(lt, 0.2), 1)
    draw_sprite(ctx, text_sprite("東京タワー 333m", 40, path=FONTS["mochiy"]), 760, base - 333 * k - 40, pin(lt, 0.3), 1)
    draw_sprite(ctx, text_sprite("151m", 44, path=FONTS["dela"]), 930, base - 151 * k - 40, pin(lt, 0.4), 1)


def v_dart_fly(ctx, lt, d, gt):
    space_bg(ctx, gt)
    for k in range(7):
        y = CY - 300 + k * 90; off = (gt * 1400 + k * 230) % 1300
        ctx.move_to(1100 - off, y); ctx.line_to(1100 - off + 260, y); ctx.set_source_rgba(1, 1, 1, 0.45); ctx.set_line_width(8); ctx.stroke()
    dart(ctx, CX, CY, 1.6 * pin(lt), -0.05)
    label(ctx, "秒速6.1km", CX, CY - 360, 120, s=pin(lt, 0.2), rot=0.05)


def v_impact(ctx, lt, d, gt):
    space_bg(ctx, gt)
    rock(ctx, CX, CY, 170, seed=7, col="#B3A28E")
    p = ease_out_cubic(clamp(lt / max(d * 0.8, 0.6)))
    rnd = random.Random(5)
    for k in range(60):
        a = rnd.uniform(-2.6, -0.5); r = 170 + p * rnd.uniform(150, 520)
        circle(ctx, CX + r * math.cos(a), CY + r * math.sin(a), rnd.uniform(5, 14) * (1 - 0.5 * p), "#D9C9B3", lw=0)
    label(ctx, "ちりが1万km!", CX, CY + 360, 100, s=pin(lt, 0.3), rot=-0.05)


def clockface(ctx, x, y, r, frac, gt):
    circle(ctx, x, y, r, "#FFFFFF", lw=10)
    for k in range(12):
        a = k * math.pi / 6
        ctx.move_to(x + 0.82 * r * math.cos(a), y + 0.82 * r * math.sin(a)); ctx.line_to(x + 0.95 * r * math.cos(a), y + 0.95 * r * math.sin(a))
    ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(6); ctx.stroke()
    a = -math.pi / 2 + 2 * math.pi * frac
    ctx.move_to(x, y); ctx.line_to(x + 0.7 * r * math.cos(a), y + 0.7 * r * math.sin(a)); ctx.set_line_width(14); ctx.stroke()
    a = -math.pi / 2 + gt * 3
    ctx.move_to(x, y); ctx.line_to(x + 0.85 * r * math.cos(a), y + 0.85 * r * math.sin(a)); ctx.set_source_rgba(*hexc("#FF3D7F")); ctx.set_line_width(7); ctx.stroke()


def v_orbit_change(ctx, lt, d, gt):
    space_bg(ctx, gt)
    rock(ctx, CX, CY + 40, 130, seed=3, ridge=True)
    ctx.new_path(); ctx.arc(CX, CY + 40, 360, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.35); ctx.set_line_width(6); ctx.set_dash([16, 12]); ctx.stroke()
    p = ease_in_out(clamp(lt / max(d * 0.7, 0.6)))
    rr = 360 - 50 * p
    ctx.new_path(); ctx.arc(CX, CY + 40, rr, 0, 2 * math.pi); ctx.set_source_rgba(*hexc("#FFE14D")); ctx.set_line_width(8); ctx.set_dash([]); ctx.stroke()
    a = gt * 1.4
    rock(ctx, CX + rr * math.cos(a), CY + 40 + rr * math.sin(a), 40, seed=7, col="#B3A28E")
    label(ctx, "33分短く!", CX, CY - 420, 120, color="#FFE14D", s=pin(lt, 0.3))


def v_clock(ctx, lt, d, gt):
    clockface(ctx, CX - 210, CY, 170 * pin(lt), 11.92 / 12, gt)
    clockface(ctx, CX + 210, CY, 170 * pin(lt, 0.15), 11.37 / 12, gt)
    label(ctx, "11時間55分", CX - 210, CY + 240, 54, font="mochiy", s=pin(lt, 0.1))
    label(ctx, "11時間22分", CX + 210, CY + 240, 54, color="#FFE14D", font="mochiy", s=pin(lt, 0.25))
    label(ctx, "→", CX, CY, 120, s=pin(lt, 0.2))


def v_predict(ctx, lt, d, gt):
    base = CY + 330
    for i, (lab, h, col) in enumerate([("予想", 280, "#7FD3FF"), ("実際", 520, "#FF3D7F")]):
        x = CX - 200 + i * 400
        hh = h * ease_out_cubic(clamp((lt - 0.15 * i) / 0.6))
        rrect(ctx, x - 100, base - hh, 200, hh, 20); fill_stroke(ctx, col, lw=8)
        label(ctx, lab, x, base + 70, 70, font="mochiy")
    label(ctx, "予想以上!", CX, CY - 380, 120, color="#FFE14D", s=pin(lt, 0.6), rot=-0.06)


def v_why(ctx, lt, d, gt):
    space_bg(ctx, gt)
    rock(ctx, CX, CY + 40, 220 * pin(lt), seed=7, col="#B3A28E")
    for i, (x, y, sz) in enumerate([(CX - 320, CY - 300, 170), (CX + 300, CY - 260, 220), (CX + 10, CY - 420, 140)]):
        draw_sprite(ctx, text_sprite("?", sz, color="#FFE14D", path=FONTS["dela"]), x, y, pin(lt, 0.1 + i * 0.12), 1, 0.3 * math.sin(gt * 4 + i))


def rocket(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -45, -260, 90, 400, 40); fill_stroke(ctx, "#FFFFFF", lw=8)
    ctx.move_to(-45, -220); ctx.curve_to(-45, -330, 45, -330, 45, -220); fill_stroke(ctx, "#1B1B3A", lw=6)
    for side in (-1, 1):
        ctx.move_to(side * 45, 60); ctx.line_to(side * 95, 150); ctx.line_to(side * 45, 140); ctx.close_path(); fill_stroke(ctx, "#1B1B3A", lw=6)
    ctx.restore()


def v_launch(ctx, lt, d, gt):
    p = ease_in_out(clamp(lt / max(d, 0.8)))
    y = CY + 300 - 600 * p
    for k in range(8):
        circle(ctx, CX + 30 * math.sin(gt * 9 + k), y + 230 + k * 50, 50 - k * 4, ["#FFE14D", "#FF8A3D"][k % 2], lw=0)
    rocket(ctx, CX, y, 1.0)
    label(ctx, "2024年10月", CX - 230, CY - 420, 80, s=pin(lt, 0.2), rot=-0.06)


def v_mars(ctx, lt, d, gt):
    space_bg(ctx, gt)
    planet(ctx, CX - 150, CY + 120, 230 * pin(lt), "#E2633A")
    p = clamp(lt / max(d, 0.8))
    hera(ctx, CX + 300 - 80 * p, CY - 260 + 120 * p, 0.8, gt)
    label(ctx, "火星をスイング!", CX, CY - 430, 90, s=pin(lt, 0.2))


def v_early(ctx, lt, d, gt):
    for i, (m, col) in enumerate([("11月", "#FFE14D"), ("12月", "#FFFFFF")]):
        x = CX - 210 + i * 420
        rrect(ctx, x - 160, CY - 180, 320, 360, 30); fill_stroke(ctx, col, lw=8)
        rrect(ctx, x - 160, CY - 180, 320, 90, 30); fill_stroke(ctx, "#FF3D7F", lw=8)
        label(ctx, m, x, CY + 40, 110, color="#1B1B3A", hi="#FF3D7F", s=pin(lt, 0.1 * i))
    label(ctx, "1か月早く到着!", CX, CY - 380, 100, s=pin(lt, 0.3), rot=0.05)


def v_far(ctx, lt, d, gt):
    space_bg(ctx, gt)
    planet(ctx, 180, CY + 120, 110 * pin(lt), EARTH)
    hera(ctx, 900, CY - 120, 0.75 * pin(lt, 0.15), gt)
    p = (lt % 1.4) / 1.4
    for k in range(3):
        q = (p + k / 3) % 1
        circle(ctx, 280 + 520 * q, CY + 80 - 180 * q, 16, "#FFE14D", lw=0)
    label(ctx, "1億9650万km", CX, CY + 360, 96, s=pin(lt, 0.3))


def v_car(ctx, lt, d, gt):
    hera(ctx, CX - 200, CY - 60, 1.2 * pin(lt), gt)
    ctx.save(); ctx.translate(CX + 250, CY + 120); s = pin(lt, 0.2); ctx.scale(s, s)
    rrect(ctx, -170, -60, 340, 110, 40); fill_stroke(ctx, "#FF8FB1", lw=8)
    rrect(ctx, -100, -130, 200, 80, 30); fill_stroke(ctx, "#BFE9FF", lw=8)
    for wx in (-100, 100):
        circle(ctx, wx, 55, 42, "#1B1B3A", lw=0); circle(ctx, wx, 55, 18, "#CCCCCC", lw=0)
    ctx.restore()
    label(ctx, "小さな車くらい", CX, CY - 380, 96, s=pin(lt, 0.3))


def v_rect_orbit(ctx, lt, d, gt):
    space_bg(ctx, gt)
    pair(ctx, gt, CX, CY + 20, 0.45, orbit=False)
    L = 760
    ctx.rectangle(CX - L / 2, CY + 20 - L / 2, L, L); ctx.set_source_rgba(*hexc("#FFE14D")); ctx.set_line_width(8); ctx.set_dash([20, 14]); ctx.stroke(); ctx.set_dash([])
    per = (gt * 0.18) % 1
    side, f = int(per * 4), (per * 4) % 1
    corners = [(CX - L / 2, CY + 20 - L / 2), (CX + L / 2, CY + 20 - L / 2), (CX + L / 2, CY + 20 + L / 2), (CX - L / 2, CY + 20 + L / 2)]
    (x0, y0), (x1, y1) = corners[side], corners[(side + 1) % 4]
    x, y = x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
    hera(ctx, x, y, 0.45, gt)
    if f < 0.08:
        burst(ctx, x, y, 90, gt, "#FF8A3D")
    label(ctx, "長方形の軌道!?", CX, CY - 440, 96, s=pin(lt, 0.2))


def v_gravity(ctx, lt, d, gt):
    rock(ctx, CX, CY + 220, 200 * pin(lt), seed=7, col="#B3A28E")
    y = CY - 60 - 80 * math.sin(gt * 0.8)
    piko(ctx, CX, y, gt, 0.8, "wow")
    label(ctx, "重力は地球の20万分の1", CX, CY - 420, 72, s=pin(lt, 0.2))


def v_snail(ctx, lt, d, gt):
    x = 200 + 680 * clamp(lt / max(d, 1.0)) * 0.3
    ctx.save(); ctx.translate(x, CY + 160); s = pin(lt); ctx.scale(s, s)
    rrect(ctx, -140, 40, 300, 70, 35); fill_stroke(ctx, "#B6F07A", lw=8)
    circle(ctx, 0, 0, 95, "#FFB36B", lw=8)
    ctx.new_path(); ctx.arc(0, 0, 50, 0, 2 * math.pi); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(6); ctx.stroke()
    for ex in (140, 170):
        ctx.move_to(ex - 20, 50); ctx.line_to(ex, -30); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(6); ctx.stroke()
        circle(ctx, ex, -30, 10, "#1B1B3A", lw=0)
    ctx.restore()
    label(ctx, "秒速12cm", CX, CY - 360, 130, s=pin(lt, 0.2), rot=-0.05)


def v_photo(ctx, lt, d, gt):
    rrect(ctx, CX - 430, CY - 330, 860, 660, 30); fill_stroke(ctx, "#1B1B3A", lw=12)
    ctx.save(); rrect(ctx, CX - 410, CY - 310, 820, 620, 20); ctx.clip()
    ctx.rectangle(0, 0, 1080, 1920); ctx.set_source_rgba(0.05, 0.05, 0.1, 1); ctx.fill()
    rock(ctx, CX, CY + 20, 280, seed=3, ridge=True, boulders=26)
    ctx.restore()
    for (x, y) in [(CX - 430, CY - 330), (CX + 430, CY - 330), (CX - 430, CY + 330), (CX + 430, CY + 330)]:
        circle(ctx, x, y, 18, "#FF3D7F", lw=0)
    label(ctx, "わぁ!", CX, CY - 420, 140, color="#FFE14D", s=pin(lt, 0.25), rot=-0.08)


def v_boulders(ctx, lt, d, gt):
    rock(ctx, CX, CY + 40, 330 * pin(lt), seed=3, ridge=True, boulders=40)
    rnd = random.Random(11)
    for k in range(5):
        x, y = CX + rnd.uniform(-200, 200), CY + 40 + rnd.uniform(-180, 180)
        ctx.new_path(); ctx.arc(x, y, 44 + 8 * math.sin(gt * 6 + k), 0, 2 * math.pi)
        ctx.set_source_rgba(*hexc("#FFE14D")); ctx.set_line_width(7); ctx.stroke()
    label(ctx, "大きな岩がゴロゴロ", CX, CY - 400, 84, s=pin(lt, 0.3))


def v_ridge(ctx, lt, d, gt):
    space_bg(ctx, gt)
    rock(ctx, CX, CY + 20, 300 * pin(lt), seed=3, ridge=True, rot=gt * 1.2)
    label(ctx, "2.2時間で1回転", CX, CY - 400, 96, s=pin(lt, 0.2))


def v_transfer(ctx, lt, d, gt):
    space_bg(ctx, gt)
    rock(ctx, CX - 180, CY + 60, 230, seed=3, ridge=True)
    rock(ctx, CX + 330, CY - 220, 70, seed=7, col="#B3A28E")
    for k in range(6):
        q = ((lt * 0.6) + k / 6) % 1
        x = CX + 300 - 420 * q; y = CY - 200 + 230 * q - math.sin(q * math.pi) * 120
        circle(ctx, x, y, 14, "#D9C9B3", lw=4)
    label(ctx, "お引っ越し!?", CX, CY + 380, 100, color="#FFE14D", s=pin(lt, 0.3), rot=0.05)


def v_thermal(ctx, lt, d, gt):
    ctx.save(); ctx.translate(CX, CY + 40)
    for k, col in enumerate(["#3B1F86", "#7B5CFF", "#FF3D7F", "#FF8A3D", "#FFE14D"]):
        r = 300 - k * 55
        ctx.new_path(); ctx.arc(10 * math.sin(gt + k), 0, r * pin(lt, k * 0.05), 0, 2 * math.pi); ctx.set_source_rgba(*hexc(col)); ctx.fill()
    ctx.restore()
    rrect(ctx, CX - 170, CY - 470, 340, 110, 30); fill_stroke(ctx, "#FFFFFF", lw=8)
    label(ctx, "JAXA", CX, CY - 415, 80, color="#1B1B3A", hi="#FF3D7F", s=pin(lt, 0.2))
    label(ctx, "温度カメラ", CX, CY + 400, 96, s=pin(lt, 0.3))


def v_ryugu(ctx, lt, d, gt):
    space_bg(ctx, gt)
    ctx.save(); ctx.translate(CX - 80, CY + 80); s = pin(lt); ctx.scale(s, s)
    ctx.move_to(0, -260); ctx.line_to(250, 0); ctx.line_to(0, 260); ctx.line_to(-250, 0); ctx.close_path(); fill_stroke(ctx, "#5E5247", lw=10)
    rnd = random.Random(4)
    for k in range(30):
        circle(ctx, rnd.uniform(-150, 150), rnd.uniform(-150, 150), rnd.uniform(6, 14), "#3E352D", lw=0)
    ctx.restore()
    hera(ctx, CX + 300, CY - 300, 0.6, gt)
    label(ctx, "リュウグウ", CX - 80, CY + 420, 84, s=pin(lt, 0.2), font="mochiy")
    label(ctx, "スカスカ!?", CX + 220, CY - 470, 96, color="#FFE14D", s=pin(lt, 0.35))


def v_cubesats(ctx, lt, d, gt):
    space_bg(ctx, gt)
    hera(ctx, CX - 260, CY - 260, 0.8, gt)
    p = ease_out_cubic(clamp(lt / max(d * 0.8, 0.6)))
    for k, (dx, dy, name) in enumerate([(380, 260, "ユベンタス"), (180, 520, "ミラニ")]):
        x, y = CX - 260 + dx * p, CY - 260 + dy * p
        rrect(ctx, x - 50, y - 35, 100, 70, 10); fill_stroke(ctx, ["#7FD3FF", "#B6F07A"][k], lw=6)
        draw_sprite(ctx, text_sprite(name, 40, path=FONTS["mochiy"]), x, y + 80, p, 1)
    label(ctx, "くつ箱サイズの子機!", CX, CY + 440, 84, s=pin(lt, 0.3))


def v_landing(ctx, lt, d, gt):
    space_bg(ctx, gt)
    rock(ctx, CX, CY + 520, 420, seed=7, col="#B3A28E")
    p = ease_in_out(clamp(lt / max(d * 0.9, 0.8)))
    hera(ctx, CX, CY - 320 + 380 * p, 0.9, gt)
    label(ctx, "最後は着陸!?", CX, CY - 450, 100, s=pin(lt, 0.2))


def v_calendar(ctx, lt, d, gt):
    rrect(ctx, CX - 260, CY - 260, 520, 520, 40); fill_stroke(ctx, "#FFFFFF", lw=10)
    rrect(ctx, CX - 260, CY - 260, 520, 140, 40); fill_stroke(ctx, "#FF3D7F", lw=10)
    label(ctx, "11月", CX, CY - 190, 80, s=pin(lt))
    label(ctx, "25", CX, CY + 70, 240, color="#FF3D7F", hi="#FF3D7F", s=pin(lt, 0.15) * (1 + 0.05 * math.sin(gt * 6)))
    label(ctx, "くわしい写真が公開!", CX, CY + 400, 80, s=pin(lt, 0.3))


def v_shield(ctx, lt, d, gt):
    space_bg(ctx, gt)
    planet(ctx, CX - 200, CY + 220, 200 * pin(lt), EARTH)
    ctx.new_path(); ctx.arc(CX - 200, CY + 220, 290, -1.4, 0.6); ctx.set_source_rgba(0.5, 0.9, 1, 0.6 + 0.3 * math.sin(gt * 5)); ctx.set_line_width(18); ctx.stroke()
    p = clamp(lt / max(d * 0.8, 0.8))
    ax, ay = CX + 420 - 300 * min(p, 0.55), CY - 420 + 300 * min(p, 0.55)
    if p > 0.55:
        q = (p - 0.55) / 0.45
        ax, ay = ax + 300 * q, ay - 60 * q
    rock(ctx, ax, ay, 70, seed=5, col="#B3A28E")
    if 0.5 < p < 0.62:
        burst(ctx, ax, ay, 120, gt, "#FFE14D")
    label(ctx, "地球を守る!", CX + 120, CY - 470, 110, color="#FFE14D", s=pin(lt, 0.2))


def v_safe(ctx, lt, d, gt):
    planet(ctx, CX - 260, CY + 120, 170 * pin(lt), EARTH)
    pair(ctx, gt, CX + 260, CY - 160, 0.35, orbit=False)
    circle(ctx, CX + 260, CY + 260, 110 * pin(lt, 0.2), "#3CE07A", lw=10)
    ctx.move_to(CX + 205, CY + 260); ctx.line_to(CX + 245, CY + 305); ctx.line_to(CX + 320, CY + 210)
    ctx.set_source_rgba(1, 1, 1, 1); ctx.set_line_width(22); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    label(ctx, "地球にはぶつからない", CX, CY - 430, 76, s=pin(lt, 0.3))


def v_team(ctx, lt, d, gt):
    for k, (col, name) in enumerate([("#3D5BFF", "NASA"), ("#F2C14E", "ESA"), ("#FF3D7F", "JAXA")]):
        x = CX - 330 + k * 330
        circle(ctx, x, CY, 140 * pin(lt, k * 0.12), col, lw=10)
        label(ctx, name, x, CY, 64, s=pin(lt, 0.1 + k * 0.12))
    label(ctx, "チームで地球を守る", CX, CY - 380, 84, s=pin(lt, 0.4))


def v_question(ctx, lt, d, gt):
    piko(ctx, CX, CY + 160, gt, 1.2 * pin(lt), "smile")
    for i, (x, y, sz) in enumerate([(CX - 300, CY - 260, 170), (CX + 300, CY - 200, 220)]):
        draw_sprite(ctx, text_sprite("?", sz, color="#FFE14D", path=FONTS["dela"]), x, y, pin(lt, 0.1 + i * 0.15), 1, 0.3 * math.sin(gt * 4 + i))


def v_longvideo(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY); ctx.scale(s, s)
    rrect(ctx, -440, -260, 880, 500, 40); fill_stroke(ctx, "#1B1B3A", lw=12)
    rrect(ctx, -410, -230, 820, 440, 26); fill_stroke(ctx, "#FF3D7F", lw=0)
    ctx.move_to(-60, -100); ctx.line_to(100, -10); ctx.line_to(-60, 80); ctx.close_path(); fill_stroke(ctx, "#FFFFFF", lw=8)
    ctx.restore()
    label(ctx, "8分のくわしい版!", CX, CY - 400, 96, color="#FFE14D", s=pin(lt, 0.2), rot=-0.05)
    piko(ctx, CX + 360, CY + 330, gt, 0.6, "wow")


# ---------------------------------------------------------------- real photos (credit always under the photo)
_PHOTO = {}
PHOTO_LAYOUT = {"cy": None, "scale": 1.0}  # Shorts override: photo higher and smaller so captions never cover it
PHOTO_DIR = __import__("os").path.join(__import__("os").path.dirname(__file__), "photos")


def _img(name):
    if name not in _PHOTO:
        from PIL import Image
        im = Image.open(f"{PHOTO_DIR}/{name}.png").convert("RGBA")
        _PHOTO[name] = (pil_to_surface(im), im.size)
    return _PHOTO[name]


def photo_scene(name, credit, title=None, box=(940, 760), zoom=0.06, crop=None):
    """Returns a vis function: framed photo with slow Ken Burns zoom, credit line right under it."""
    def vis(ctx, lt, d, gt):
        surf, (iw, ih) = _img(name)
        sc = PHOTO_LAYOUT["scale"]
        bw, bh = box[0] * sc, box[1] * sc
        cx, cy = CX, (PHOTO_LAYOUT["cy"] if PHOTO_LAYOUT["cy"] is not None else CY - 20)
        s0 = pin(lt)
        ctx.save(); ctx.translate(cx, cy); ctx.scale(s0, s0)
        rrect(ctx, -bw / 2 - 14, -bh / 2 - 14, bw + 28, bh + 28, 24); fill_stroke(ctx, "#FFFFFF", lw=8)
        ctx.save(); rrect(ctx, -bw / 2, -bh / 2, bw, bh, 14); ctx.clip()
        ctx.rectangle(-bw / 2, -bh / 2, bw, bh); ctx.set_source_rgb(0, 0, 0); ctx.fill()
        sx, sy, sw, sh = crop if crop else (0, 0, iw, ih)
        k = max(bw / sw, bh / sh) * (1 + zoom * clamp(lt / max(d, 1)))
        ctx.scale(k, k); ctx.translate(-(sx + sw / 2), -(sy + sh / 2))
        ctx.set_source_surface(surf, 0, 0); ctx.paint()
        ctx.restore()
        ctx.restore()
        # credit directly under the photo
        cr = text_sprite("出典:" + credit, 44 if sc >= 1 else 38, color="#FFFFFF", hi="#FFE14D", stroke="#1B1B3A", stroke_w=5, shadow=False, path=FONTS["mochiy"])
        draw_sprite(ctx, cr, cx, cy + bh / 2 + (48 if sc >= 1 else 40), min(1.0, (bw + 20) / max(1, cr.get_width())) * s0, 1)
        if title:
            draw_sprite(ctx, text_sprite(title, 70 if sc >= 1 else 58, color="#FFE14D", path=FONTS["dela"]), cx, cy - bh / 2 - (70 if sc >= 1 else 52), pin(lt, 0.15), 1, -0.04)
    return vis


ESA = "ESA"
NASA = "NASA/Johns Hopkins APL"
P_first = photo_scene("first_view", ESA, "ヘラが撮った本物!")
P_didy = photo_scene("didymos_28km", ESA, "28.5kmから撮影", crop=(260, 260, 500, 500))
P_didy_wide = photo_scene("didymos_28km", ESA, crop=(160, 160, 700, 700))
P_tiri = photo_scene("tiri", "ESA(温度カメラはJAXA製)", "温度で見ると…", box=(940, 600), crop=(180, 0, 400, 353))
P_hsh = photo_scene("hyperscout", ESA, "25色で分析!", box=(980, 560))
P_sagrada = photo_scene("sagrada", ESA, "サグラダ・ファミリアと比べると", box=(980, 660))
P_brian = photo_scene("brian3d", "ESA/Brian May・Claudia Manzoni", "3D写真!", box=(900, 800))
P_dart_both = photo_scene("dart_both", NASA, "ダートが撮った2つの小惑星")
P_dart_dimo = photo_scene("dart_dimorphos", NASA, "ぶつかる直前のディモルフォス", crop=(150, 150, 724, 724))
P_dart_final = photo_scene("dart_final", NASA, "最後の1枚", crop=(0, 0, 762, 380), box=(980, 500))
P_plume = photo_scene("licia_plume", "ASI/NASA", "ちりが噴き出した!", box=(980, 520))
P_hubble = photo_scene("hubble_ejecta", "NASA, ESA, STScI", "しっぽが伸びた!", box=(980, 330))
P_square = photo_scene("square_orbit", ESA, "本当に長方形!", box=(980, 360))
P_cubesats = photo_scene("cubesats", ESA, "子機の切り離し", box=(960, 680))


def v_dino(ctx, lt, d, gt):
    ctx.rectangle(0, CY + 260, 1080, 400); ctx.set_source_rgba(*hexc("#7A5A3A")); ctx.fill()
    ctx.save(); ctx.translate(CX - 180, CY + 260); s = pin(lt); ctx.scale(s, s)
    ctx.move_to(-200, 0); ctx.curve_to(-180, -160, -40, -200, 40, -160); ctx.curve_to(80, -260, 120, -340, 190, -330)
    ctx.curve_to(250, -330, 250, -280, 200, -270); ctx.curve_to(150, -260, 130, -200, 120, -130); ctx.curve_to(160, -60, 120, 0, 60, 0)
    ctx.close_path(); fill_stroke(ctx, "#5BBF5B", lw=8)
    circle(ctx, 210, -310, 9, "#1B1B3A", lw=0)
    ctx.restore()
    p = clamp(lt / max(d * 0.8, 0.8))
    x, y = CX + 420 - 300 * p, CY - 460 + 520 * p
    for k in range(6):
        circle(ctx, x + 30 * (k + 1), y - 40 * (k + 1), 40 - 6 * k, ["#FFE14D", "#FF8A3D"][k % 2], lw=0)
    rock(ctx, x, y, 70, seed=2, col="#8A7A6A")
    label(ctx, "6600万年前", CX + 160, CY + 420, 84, s=pin(lt, 0.2))


def v_fireball(ctx, lt, d, gt):
    ctx.rectangle(0, CY + 280, 1080, 400); ctx.set_source_rgba(*hexc("#DDE8F0")); ctx.fill()
    for k in range(5):
        rrect(ctx, 80 + k * 190, CY + 120, 150, 160, 10); fill_stroke(ctx, "#8FA3B8", lw=6)
    p = clamp(lt / max(d * 0.7, 0.8))
    x, y = 950 - 700 * p, CY - 460 + 360 * p
    ctx.move_to(1080, CY - 560); ctx.line_to(x, y); ctx.set_source_rgba(1, 0.9, 0.6, 0.8); ctx.set_line_width(30); ctx.stroke()
    burst(ctx, x, y, 90 + 20 * math.sin(gt * 20), gt, "#FFE14D")
    label(ctx, "2013年 ロシア", CX, CY - 440, 90, s=pin(lt, 0.2))


def v_billiard(ctx, lt, d, gt):
    p = clamp(lt / max(d * 0.5, 0.6))
    x1 = 160 + 340 * p
    circle(ctx, x1, CY, 70, "#FFFFFF", lw=8)
    q = clamp((lt - d * 0.5) / max(d * 0.5, 0.6))
    circle(ctx, 640 + 120 * q, CY - 60 * q, 120, "#B3A28E", lw=8)
    if 0.95 < p and q < 0.25:
        burst(ctx, 570, CY, 80, gt, "#FFE14D")
    label(ctx, "ビリヤードのように", CX, CY - 380, 90, s=pin(lt, 0.2))


def v_recoil(ctx, lt, d, gt):
    space_bg(ctx, gt)
    rock(ctx, CX + 100, CY + 40, 170, seed=7, col="#B3A28E")
    rnd = random.Random(8)
    for k in range(40):
        a = rnd.uniform(2.4, 3.9); r = 180 + ((lt * 260 + k * 37) % 420)
        circle(ctx, CX + 100 + r * math.cos(a), CY + 40 + r * math.sin(a), 9, "#D9C9B3", lw=0)
    ctx.move_to(CX + 300, CY + 40); ctx.line_to(CX + 470, CY + 40); ctx.set_source_rgba(*hexc("#FFE14D")); ctx.set_line_width(26); ctx.stroke()
    ctx.move_to(CX + 470, CY - 10); ctx.line_to(CX + 530, CY + 40); ctx.line_to(CX + 470, CY + 90); ctx.close_path(); ctx.fill()
    label(ctx, "ちりの反動で押された!?", CX, CY - 420, 84, s=pin(lt, 0.2))


def v_names(ctx, lt, d, gt):
    for i, (gr, ja, col) in enumerate([("Didymos", "ふたご", "#7FD3FF"), ("Dimorphos", "ふたつの形", "#FF8FB1")]):
        y = CY - 180 + i * 360
        rrect(ctx, 120, y - 130, 840, 260, 40); fill_stroke(ctx, col, lw=8)
        label(ctx, gr, CX, y - 50, 80, color="#FFFFFF", hi="#FFE14D", s=pin(lt, 0.15 * i))
        label(ctx, "= " + ja, CX, y + 60, 80, s=pin(lt, 0.1 + 0.15 * i))
    label(ctx, "ギリシャ語!", CX, CY - 470, 90, color="#FFE14D", s=pin(lt, 0.4))


def v_hera_goddess(ctx, lt, d, gt):
    ctx.save(); ctx.translate(CX, CY + 60); s = pin(lt); ctx.scale(s, s)
    ctx.move_to(-160, -150); ctx.line_to(-110, -260); ctx.line_to(-50, -170); ctx.line_to(0, -290); ctx.line_to(50, -170); ctx.line_to(110, -260); ctx.line_to(160, -150); ctx.close_path()
    fill_stroke(ctx, "#FFD23F", lw=8)
    ctx.restore()
    piko(ctx, CX, CY + 160, gt, 1.0 * pin(lt), "smile")
    label(ctx, "ギリシャ神話の女神", CX, CY - 430, 84, s=pin(lt, 0.2))
