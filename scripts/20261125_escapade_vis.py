"""Visuals for the ESCAPADE (NASA twin Mars probes) Earth-flyby / farewell-photo episode. Vertical stage, CX=540, CY=760."""
import math, random
import cairo
from common4 import *
from space2 import pin, CX, CY
from space import planet
from hera_vis import label, photo_scene, PHOTO_LAYOUT, v_question, v_longvideo, space_bg

OPTS = {"short": False}
EARTH = "#3FA9F5"
MARS = "#E2633A"
BLUE = "#3D7BFF"
GOLD = "#FDB515"
INK = "#1B1B3A"


def lbl(ctx, t, x, y, size=80, s=1.0, rot=0.0, font="dela", color="#FFFFFF"):
    if OPTS["short"] and font == "mochiy" and size < 70:
        return
    label(ctx, t, x, y, size, color=color, s=s, rot=rot, font=font)


def P(name, credit, title=None, box=(940, 700), **kw):
    return photo_scene(name, credit, title, box=box, **kw)


def bigtext(text, sub=None, color="#FFE14D", size=220):
    def vis(ctx, lt, d, gt):
        space_bg(ctx, gt)
        draw_sprite(ctx, text_sprite(text, size, color=color, hi="#FF3D7F", path=FONTS["dela"]), CX, CY - 60, pin(lt), 1, -0.04)
        if sub:
            draw_sprite(ctx, text_sprite(sub, 78, color="#FFFFFF", hi="#FFE14D", path=FONTS["mochiy"]), CX, CY + 160, pin(lt, 0.2), 1)
    return vis


# ---------------------------------------------------------------- props
def earth(ctx, x, y, r, gt=0.0):
    if r < 3:
        return
    planet(ctx, x, y, r, EARTH)
    ctx.save(); ctx.new_path(); ctx.arc(x, y, r * 0.97, 0, 2 * math.pi); ctx.clip()
    for (dx, dy, rr) in [(-0.35, -0.1, 0.32), (0.25, 0.3, 0.28), (0.3, -0.45, 0.2)]:
        circle(ctx, x + dx * r, y + dy * r, rr * r, "#4FC36A", lw=0)
    for k in range(3):
        yy = y - r * 0.5 + k * r * 0.45
        ctx.move_to(x - r + ((gt * 30 + k * 90) % (2 * r)), yy); ctx.rel_line_to(r * 0.6, 0)
        ctx.set_source_rgba(1, 1, 1, 0.75); ctx.set_line_width(max(4, r * 0.08)); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.restore()


def mars(ctx, x, y, r, air=0.0):
    if r < 3:
        return
    if air > 0:
        circle(ctx, x, y, r * (1.12 + 0.1 * air), "#9FD8FF", lw=0)
    planet(ctx, x, y, r, MARS)
    circle(ctx, x - r * 0.1, y - r * 0.82, r * 0.18, "#FFFFFF", lw=0)


def sun(ctx, x, y, r, gt):
    for k in range(12):
        a = k / 12 * 2 * math.pi + gt * 0.3
        ctx.move_to(x + r * 1.1 * math.cos(a), y + r * 1.1 * math.sin(a)); ctx.line_to(x + r * 1.45 * math.cos(a), y + r * 1.45 * math.sin(a))
        ctx.set_source_rgba(*hexc("#FFB84D")); ctx.set_line_width(max(6, r * 0.12)); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    circle(ctx, x, y, r, "#FFD23F", lw=max(5, r * 0.06))


def twin(ctx, x, y, s, gt, col=BLUE, rot=0.0, flame=False, face=True):
    """Cute ESCAPADE-like probe: boxy body, two square solar panels, color band."""
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot + 0.06 * math.sin(gt * 2.5)); ctx.scale(s, s)
    if flame:
        for k in range(5):
            circle(ctx, -150 - k * 38 + 6 * math.sin(gt * 30 + k), 0, 34 - k * 5, ["#FFE14D", "#FF8A3D"][k % 2], lw=0)
    for sx in (-1, 1):
        ctx.move_to(sx * 60, 0); ctx.line_to(sx * 110, 0); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(10); ctx.stroke()
        rrect(ctx, sx * 110 - (130 if sx < 0 else 0), -65, 130, 130, 10); fill_stroke(ctx, "#2E3F8F", lw=6)
        for g in (1, 2):
            ctx.move_to(sx * 110 + (-130 if sx < 0 else 0) + g * 43, -65); ctx.rel_line_to(0, 130)
            ctx.set_source_rgba(0.7, 0.8, 1, 0.6); ctx.set_line_width(3); ctx.stroke()
    rrect(ctx, -70, -80, 140, 160, 18); fill_stroke(ctx, "#D8DEE8", lw=7)
    rrect(ctx, -70, 30, 140, 30, 4); fill_stroke(ctx, col, lw=5)
    if face:
        circle(ctx, -25, -25, 13, INK, lw=0); circle(ctx, 25, -25, 13, INK, lw=0)
        circle(ctx, -21, -29, 4, "#FFFFFF", lw=0); circle(ctx, 29, -29, 4, "#FFFFFF", lw=0)
        ctx.new_path(); ctx.arc(0, -5, 14, 0.3, 2.8); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(5); ctx.stroke()
    circle(ctx, 0, -100, 16, "#FFFFFF", lw=5)
    ctx.restore()


def arrow(ctx, x0, y0, x1, y1, col="#FFE14D", w=14):
    ctx.move_to(x0, y0); ctx.line_to(x1, y1); ctx.set_source_rgba(*hexc(col)); ctx.set_line_width(w); ctx.stroke()
    a = math.atan2(y1 - y0, x1 - x0)
    ctx.move_to(x1 + 30 * math.cos(a), y1 + 30 * math.sin(a))
    ctx.line_to(x1 + 30 * math.cos(a + 2.3), y1 + 30 * math.sin(a + 2.3)); ctx.line_to(x1 + 30 * math.cos(a - 2.3), y1 + 30 * math.sin(a - 2.3))
    ctx.close_path(); ctx.fill()


def particles(ctx, x0, y0, x1, y1, gt, n=14, col="#FFE14D", stop=None, seed=3):
    rnd = random.Random(seed)
    for k in range(n):
        f = (gt * 0.6 + k / n) % 1
        if stop is not None and f > stop:
            continue
        off = rnd.uniform(-160, 160)
        x = x0 + (x1 - x0) * f; y = y0 + (y1 - y0) * f + off
        circle(ctx, x, y, 9, col, lw=0)


# ---------------------------------------------------------------- scenes
def v_hook(ctx, lt, d, gt):
    space_bg(ctx, gt)
    earth(ctx, CX - 170, CY + 150, 230 * pin(lt), gt)
    twin(ctx, CX + 260, CY - 120, 0.85 * pin(lt, 0.15), gt, GOLD, rot=-0.2)
    if 0.5 < (lt % 2.0) < 0.75:
        circle(ctx, CX + 260, CY - 220, 90, "#FFFFFF", lw=0)
    lbl(ctx, "パチリ!", CX + 250, CY - 400, 110, s=pin(lt, 0.3), rot=0.06)


def v_twins(ctx, lt, d, gt):
    space_bg(ctx, gt)
    twin(ctx, CX - 230, CY + 60, 0.9 * pin(lt), gt, BLUE)
    twin(ctx, CX + 230, CY + 60, 0.9 * pin(lt, 0.15), gt + 1, GOLD)
    lbl(ctx, "ブルー", CX - 230, CY + 300, 80, s=pin(lt, 0.25), color="#7FB0FF")
    lbl(ctx, "ゴールド", CX + 230, CY + 300, 80, s=pin(lt, 0.35), color=GOLD)
    lbl(ctx, "ふたごの探査機", CX, CY - 400, 100, s=pin(lt, 0.1))


def v_name(ctx, lt, d, gt):
    space_bg(ctx, gt)
    lbl(ctx, "ESCAPADE", CX, CY - 150, 110, s=pin(lt))
    lbl(ctx, "エスカペード", CX, CY + 20, 100, s=pin(lt, 0.2), color="#FFE14D")
    lbl(ctx, "=大冒険!", CX, CY + 200, 110, s=pin(lt, 0.4))


def v_colors(ctx, lt, d, gt):
    for i, (c, n) in enumerate([(BLUE, "青"), (GOLD, "金")]):
        x = CX - 220 + i * 440
        circle(ctx, x, CY + 20, 170 * pin(lt, 0.15 * i), c, lw=10)
        lbl(ctx, n, x, CY + 20, 140, s=pin(lt, 0.2 + 0.15 * i))
    lbl(ctx, "大学のカラー!", CX, CY - 400, 100, s=pin(lt, 0.1))


def v_cost(ctx, lt, d, gt):
    h1 = 560 * ease_out_cubic(clamp(lt / 0.8)); h2 = 56 * ease_out_cubic(clamp((lt - 0.4) / 0.6))
    rrect(ctx, CX - 330, CY + 380 - max(h1, 1), 220, max(h1, 1), 10); fill_stroke(ctx, "#8FA3B8", lw=6)
    rrect(ctx, CX + 110, CY + 380 - max(h2, 1), 220, max(h2, 1), 10); fill_stroke(ctx, GOLD, lw=6)
    lbl(ctx, "ふつうの火星探査機", CX - 220, CY + 450, 50, font="mochiy", s=pin(lt, 0.1))
    lbl(ctx, "エスカペード", CX + 220, CY + 450, 56, font="mochiy", s=pin(lt, 0.2))
    lbl(ctx, "約10分の1!", CX + 220, CY + 160, 90, s=pin(lt, 0.8), color="#FFE14D")
    lbl(ctx, "お値段くらべ", CX, CY - 420, 100, s=pin(lt, 0.1))


def rocket(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -55, -300, 110, 460, 46); fill_stroke(ctx, "#FFFFFF", lw=8)
    ctx.move_to(-55, -250); ctx.curve_to(-55, -380, 55, -380, 55, -250); fill_stroke(ctx, "#3D5BFF", lw=6)
    for side in (-1, 1):
        ctx.move_to(side * 55, 80); ctx.line_to(side * 110, 170); ctx.line_to(side * 55, 160); ctx.close_path(); fill_stroke(ctx, INK, lw=6)
    ctx.restore()


def v_launch(ctx, lt, d, gt):
    p = ease_in_out(clamp(lt / max(d, 0.8)))
    y = CY + 280 - 520 * p
    for k in range(8):
        circle(ctx, CX + 30 * math.sin(gt * 9 + k), y + 230 + k * 50, 50 - k * 4, ["#FFE14D", "#FF8A3D"][k % 2], lw=0)
    rocket(ctx, CX, y, 0.95)
    lbl(ctx, "2025年11月13日", CX, CY - 430, 84, s=pin(lt, 0.2))


def v_landing(ctx, lt, d, gt):
    ctx.rectangle(0, CY + 330, 1080, 300); ctx.set_source_rgba(*hexc("#2F6FB5")); ctx.fill()
    rrect(ctx, CX - 260, CY + 300, 520, 50, 10); fill_stroke(ctx, "#8FA3B8", lw=6)
    p = ease_out_cubic(clamp(lt / max(d * 0.7, 0.8)))
    y = CY - 300 + 410 * p
    for k in range(4):
        circle(ctx, CX + 10 * math.sin(gt * 20 + k), y + 210 + k * 36, 30 - k * 5, "#FFB84D", lw=0)
    rocket(ctx, CX, y - 40, 0.6)
    lbl(ctx, "1段目がもどってきた!", CX, CY - 430, 86, s=pin(lt, 0.2))


def v_window(ctx, lt, d, gt):
    space_bg(ctx, gt)
    sun(ctx, CX, CY + 60, 70, gt)
    for r, c, sp, fn in ((200, EARTH, 1.0, earth), (330, MARS, 0.53, None)):
        ctx.new_path(); ctx.arc(CX, CY + 60, r, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.3); ctx.set_line_width(4); ctx.stroke()
        a = gt * 0.8 * sp
        if fn:
            earth(ctx, CX + r * math.cos(a), CY + 60 + r * math.sin(a), 40, gt)
        else:
            mars(ctx, CX + r * math.cos(a), CY + 60 + r * math.sin(a), 34)
    lbl(ctx, "チャンスは約2年2か月に1回", CX, CY - 420, 70, s=pin(lt, 0.1))


def v_l2(ctx, lt, d, gt):
    space_bg(ctx, gt)
    sun(ctx, 120, CY + 60, 60, gt)
    earth(ctx, CX - 40, CY + 60, 60, gt)
    lx = CX + 330
    ctx.save(); ctx.translate(lx, CY + 60); ctx.scale(1.0, 1.6)
    ctx.new_path(); ctx.arc(0, 0, 90, 0, 2 * math.pi); ctx.restore()
    ctx.set_source_rgba(1, 0.88, 0.3, 0.8); ctx.set_line_width(6); ctx.set_dash([16, 12]); ctx.stroke(); ctx.set_dash([])
    a = gt * 1.2
    twin(ctx, lx + 90 * math.cos(a), CY + 60 + 144 * math.sin(a), 0.32, gt, BLUE, face=False)
    twin(ctx, lx + 90 * math.cos(a + 0.5), CY + 60 + 144 * math.sin(a + 0.5), 0.32, gt, GOLD, face=False)
    arrow(ctx, CX + 40, CY + 330, lx - 60, CY + 330, "#FFFFFF", 8)
    lbl(ctx, "約150万km", CX + 150, CY + 420, 80, s=pin(lt, 0.3))
    lbl(ctx, "地球のうしろで待機", CX, CY - 420, 90, s=pin(lt, 0.1))


v_year = bigtext("約1年", "宇宙で まちぼうけ!?", size=260)


def v_tail(ctx, lt, d, gt):
    space_bg(ctx, gt)
    particles(ctx, 0, CY + 60, 1080, CY + 60, gt, n=18, col="#FFE14D")
    earth(ctx, CX - 180, CY + 60, 90 * pin(lt), gt)
    ctx.move_to(CX - 120, CY - 40); ctx.curve_to(CX + 100, CY - 60, CX + 300, CY - 10, 1080, CY + 20)
    ctx.line_to(1080, CY + 100); ctx.curve_to(CX + 300, CY + 130, CX + 100, CY + 180, CX - 120, CY + 160); ctx.close_path()
    ctx.set_source_rgba(0.6, 0.8, 1.0, 0.3); ctx.fill()
    twin(ctx, CX + 300, CY + 60, 0.3, gt, GOLD, face=False)
    lbl(ctx, "地球の“しっぽ”も調べた", CX, CY - 420, 80, s=pin(lt, 0.1))


def v_flyby(ctx, lt, d, gt):
    space_bg(ctx, gt)
    earth(ctx, CX, CY + 160, 220 * pin(lt), gt)
    p = clamp(lt / max(d, 1.0))
    a = math.pi * 1.05 - p * math.pi * 0.95
    x, y = CX + 340 * math.cos(a), CY + 160 - 340 * math.sin(a) * 0.9
    ctx.new_path(); ctx.arc(CX, CY + 160, 340, math.pi * 1.0, math.pi * 2.0); ctx.set_source_rgba(1, 1, 1, 0.0); ctx.stroke()
    twin(ctx, x, y, 0.42, gt, GOLD, rot=-a + math.pi / 2 + math.pi, flame=0.3 < p < 0.75)
    lbl(ctx, "地球の横をすりぬけ!", CX, CY - 430, 90, s=pin(lt, 0.1))


def v_burn(ctx, lt, d, gt):
    space_bg(ctx, gt)
    twin(ctx, CX + 80, CY + 60, 1.1 * pin(lt), gt, BLUE, flame=True)
    lbl(ctx, "9分間 エンジン噴射!", CX, CY - 420, 90, s=pin(lt, 0.1))


v_speed = bigtext("+時速1600km", "以上 スピードアップ!", size=115)


def v_skate(ctx, lt, d, gt):
    ctx.move_to(60, CY - 240); ctx.curve_to(400, CY + 380, 680, CY + 380, 1020, CY - 240)
    ctx.set_source_rgba(1, 1, 1, 0.9); ctx.set_line_width(14); ctx.stroke()
    p = (lt * 0.5) % 1
    t = p
    x = 60 + 960 * t; y = CY - 240 + 620 * 4 * t * (1 - t) * 0.82
    piko(ctx, x, y - 120, gt, 0.45, "wow")
    if 0.4 < t < 0.6:
        lbl(ctx, "ここでこぐ!", x, y + 80, 70, color="#FFE14D")
    lbl(ctx, "いちばん速いところで加速", CX, CY - 430, 76, s=pin(lt, 0.1))


def v_first(ctx, lt, d, gt):
    space_bg(ctx, gt)
    lbl(ctx, "NASAで", CX, CY - 200, 100, s=pin(lt))
    lbl(ctx, "はじめての作戦!", CX, CY, 120, s=pin(lt, 0.2), color="#FFE14D")
    twin(ctx, CX, CY + 320, 0.6 * pin(lt, 0.3), gt, GOLD)


def v_anytime(ctx, lt, d, gt):
    for i in range(12):
        x = CX - 375 + (i % 4) * 250; y = CY - 180 + (i // 4) * 200
        rrect(ctx, x - 90, y - 70, 180, 140, 18); fill_stroke(ctx, "#FFFFFF", lw=6)
        lbl(ctx, f"{i + 1}月", x, y - 20, 46, color=INK, s=pin(lt, 0.03 * i))
        if lt > 0.4 + 0.05 * i:
            lbl(ctx, "OK", x, y + 35, 46, color="#3FAF5A")
    lbl(ctx, "いつでも出発できる!?", CX, CY - 430, 90, s=pin(lt, 0.1))


def v_far_cam(ctx, lt, d, gt):
    space_bg(ctx, gt)
    earth(ctx, 200, CY + 80, 90, gt)
    twin(ctx, 880, CY - 40, 0.4, gt, GOLD)
    arrow(ctx, 320, CY + 330, 780, CY + 330, "#FFFFFF", 8)
    arrow(ctx, 780, CY + 330, 320, CY + 330, "#FFFFFF", 8)
    lbl(ctx, "約6万2000km", CX, CY + 430, 86, s=pin(lt, 0.2), color="#FFE14D")
    lbl(ctx, "はなれて撮った", CX, CY - 420, 100, s=pin(lt, 0.1))


def v_earth5(ctx, lt, d, gt):
    space_bg(ctx, gt)
    for i in range(5):
        earth(ctx, 140 + i * 200, CY + 40, 95 * pin(lt, 0.1 * i), gt)
    lbl(ctx, "地球 約5こ分!", CX, CY + 300, 100, s=pin(lt, 0.6), color="#FFE14D")
    lbl(ctx, "6万2000kmって?", CX, CY - 400, 96, s=pin(lt, 0.1))


def v_thermo(ctx, lt, d, gt):
    rrect(ctx, CX - 50, CY - 300, 100, 520, 50); fill_stroke(ctx, "#FFFFFF", lw=8)
    h = 400 * (0.5 + 0.4 * math.sin(gt * 2))
    rrect(ctx, CX - 28, CY + 200 - h, 56, h, 28); ctx.set_source_rgba(*hexc("#FF4D4D")); ctx.fill()
    circle(ctx, CX, CY + 240, 90, "#FF4D4D", lw=8)
    lbl(ctx, "あったかい=明るい", CX, CY - 420, 90, s=pin(lt, 0.1))


def v_satcam(ctx, lt, d, gt):
    space_bg(ctx, gt)
    earth(ctx, CX, CY + 620, 520, gt)
    ctx.save(); ctx.translate(CX - 300, CY - 60); ctx.scale(pin(lt), pin(lt))
    rrect(ctx, -50, -40, 100, 80, 10); fill_stroke(ctx, "#D8DEE8", lw=6)
    for sx in (-1, 1):
        rrect(ctx, sx * 60 - (120 if sx < 0 else 0), -25, 120, 50, 6); fill_stroke(ctx, "#2E3F8F", lw=5)
    ctx.restore()
    twin(ctx, CX + 280, CY - 230, 0.45, gt, BLUE)
    if (lt % 1.5) < 0.2:
        circle(ctx, CX - 300, CY - 60, 70, "#FFFFFF", lw=0)
    lbl(ctx, "人工衛星が探査機を撮影!", CX, CY - 430, 80, s=pin(lt, 0.1))


def v_ground(ctx, lt, d, gt):
    space_bg(ctx, gt)
    for i in range(9):
        h = 120 + (i * 53) % 160
        rrect(ctx, 40 + i * 115, CY + 420 - h, 100, h + 40, 6); fill_stroke(ctx, "#2A2F55", lw=4)
    p = clamp(lt / max(d, 1.0))
    for k, (c, dy) in enumerate(((BLUE, 0), (GOLD, 120))):
        ctx.move_to(100, CY - 200 + dy); ctx.line_to(100 + 880 * p, CY - 200 + dy + 200 * p)
        ctx.set_source_rgba(*hexc(c)); ctx.set_line_width(10); ctx.stroke()
    lbl(ctx, "地上からも見えた!", CX, CY - 430, 96, s=pin(lt, 0.1))


def v_route(ctx, lt, d, gt):
    space_bg(ctx, gt)
    sun(ctx, CX, CY + 60, 60, gt)
    ctx.new_path(); ctx.arc(CX, CY + 60, 200, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.3); ctx.set_line_width(4); ctx.stroke()
    ctx.new_path(); ctx.arc(CX, CY + 60, 360, 0, 2 * math.pi); ctx.stroke()
    earth(ctx, CX + 200, CY + 60, 36, gt)
    mars(ctx, CX - 360, CY + 60, 32)
    p = clamp(lt / max(d, 1.0))
    a = p * math.pi
    r = 200 + 160 * (1 - math.cos(a)) / 2
    twin(ctx, CX + r * math.cos(-a), CY + 60 + r * math.sin(-a), 0.22, gt, GOLD, face=False)
    lbl(ctx, "2027年9月 火星へ", CX, CY - 430, 96, s=pin(lt, 0.1))


def v_arrive(ctx, lt, d, gt):
    space_bg(ctx, gt)
    mars(ctx, CX, CY + 120, 230 * pin(lt))
    ctx.save(); ctx.translate(CX, CY + 120); ctx.scale(1, 0.45)
    ctx.new_path(); ctx.arc(0, 0, 400, 0, 2 * math.pi); ctx.restore()
    ctx.set_source_rgba(1, 1, 1, 0.5); ctx.set_line_width(5); ctx.set_dash([14, 12]); ctx.stroke(); ctx.set_dash([])
    a = gt * 0.7
    twin(ctx, CX + 400 * math.cos(a), CY + 120 + 180 * math.sin(a), 0.3, gt, BLUE, face=False)
    twin(ctx, CX + 400 * math.cos(a + 2.4), CY + 120 + 180 * math.sin(a + 2.4), 0.3, gt, GOLD, face=False)
    lbl(ctx, "火星をぐるぐる", CX, CY - 430, 100, s=pin(lt, 0.1))


def v_two_orbits(ctx, lt, d, gt):
    space_bg(ctx, gt)
    mars(ctx, CX, CY + 80, 150 * pin(lt))
    for k, (rx, ry, c, sp) in enumerate(((300, 170, BLUE, 1.0), (440, 250, GOLD, 0.65))):
        ctx.save(); ctx.translate(CX + (rx - 150) * 0.5, CY + 80); ctx.scale(1, ry / rx)
        ctx.new_path(); ctx.arc(0, 0, rx, 0, 2 * math.pi); ctx.restore()
        ctx.set_source_rgba(*hexc(c)); ctx.set_line_width(5); ctx.stroke()
        a = gt * sp * 1.2 + k
        twin(ctx, CX + (rx - 150) * 0.5 + rx * math.cos(a), CY + 80 + ry * math.sin(a), 0.22, gt, c, face=False)
    lbl(ctx, "ちがう場所で同時に測る", CX, CY - 430, 84, s=pin(lt, 0.1))


def v_weather(ctx, lt, d, gt):
    for i, (x, c) in enumerate(((CX - 250, BLUE), (CX + 250, GOLD))):
        rrect(ctx, x - 40, CY - 40, 80, 300, 10); fill_stroke(ctx, "#D8DEE8", lw=6)
        circle(ctx, x, CY - 90, 70 * pin(lt, 0.15 * i), c, lw=6)
    ctx.new_path(); ctx.arc(CX, CY - 260, 90, math.pi, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.9); ctx.fill()
    for k in range(5):
        circle(ctx, CX - 80 + k * 40, CY - 120 + ((gt * 200 + k * 50) % 160), 10, "#7FD3FF", lw=0)
    lbl(ctx, "観測所が2つ!", CX, CY - 430, 100, s=pin(lt, 0.1))


def v_oldmars(ctx, lt, d, gt):
    space_bg(ctx, gt)
    mars(ctx, CX, CY + 80, 260 * pin(lt), air=1.0)
    ctx.save(); ctx.new_path(); ctx.arc(CX, CY + 80, 255, 0, 2 * math.pi); ctx.clip()
    for (dx, dy, rr) in [(-120, 40, 90), (90, 120, 70), (60, -90, 50)]:
        circle(ctx, CX + dx, CY + 80 + dy, rr * pin(lt, 0.3), "#3F8FE0", lw=0)
    ctx.restore()
    lbl(ctx, "むかしの火星は水の星?", CX, CY - 430, 84, s=pin(lt, 0.1))


def v_thinair(ctx, lt, d, gt):
    space_bg(ctx, gt)
    earth(ctx, CX - 230, CY + 80, 150 * pin(lt), gt)
    circle(ctx, CX - 230, CY + 80, 190 * pin(lt), "#9FD8FF", lw=0)
    earth(ctx, CX - 230, CY + 80, 150 * pin(lt), gt)
    mars(ctx, CX + 250, CY + 80, 100 * pin(lt, 0.2))
    lbl(ctx, "地球", CX - 230, CY + 330, 70, s=pin(lt, 0.2))
    lbl(ctx, "火星", CX + 250, CY + 330, 70, s=pin(lt, 0.3))
    lbl(ctx, "火星の空気はうすい", CX, CY - 430, 90, s=pin(lt, 0.1))


def v_wind(ctx, lt, d, gt):
    space_bg(ctx, gt)
    sun(ctx, 60, CY + 60, 130, gt)
    particles(ctx, 200, CY + 60, 1080, CY + 60, gt, n=22, col="#FFE14D")
    lbl(ctx, "太陽風", CX, CY - 200, 130, s=pin(lt, 0.1), color="#FFE14D")
    lbl(ctx, "太陽からの つぶの風", CX, CY - 430, 84, s=pin(lt, 0.1))


def v_shield(ctx, lt, d, gt):
    space_bg(ctx, gt)
    earth(ctx, CX + 160, CY + 80, 140 * pin(lt), gt)
    ctx.new_path(); ctx.arc(CX + 160, CY + 80, 250, math.pi * 0.55, math.pi * 1.45)
    ctx.set_source_rgba(0.5, 0.9, 1, 0.6 + 0.3 * math.sin(gt * 5)); ctx.set_line_width(18); ctx.stroke()
    rnd = random.Random(4)
    for k in range(14):
        f = (gt * 0.6 + k / 14) % 1
        yy = CY + 80 + rnd.uniform(-260, 260)
        x = 40 + (CX + 160 - 250 - 40) * min(f * 1.4, 1)
        if f * 1.4 > 1:
            yy += (yy - CY - 80) * (f * 1.4 - 1) * 2
            x -= 0
        circle(ctx, x, yy, 9, "#FFE14D", lw=0)
    lbl(ctx, "地球は 磁石のバリアで守られる", CX, CY - 430, 70, s=pin(lt, 0.1))


def v_strip(ctx, lt, d, gt):
    space_bg(ctx, gt)
    particles(ctx, 0, CY + 60, CX - 120, CY + 60, gt, n=12, col="#FFE14D")
    mars(ctx, CX, CY + 60, 160 * pin(lt), air=0.4)
    rnd = random.Random(7)
    for k in range(14):
        f = (gt * 0.5 + k / 14) % 1
        a = rnd.uniform(-0.7, 0.7)
        circle(ctx, CX + (190 + 500 * f) * math.cos(a), CY + 60 + (190 + 500 * f) * math.sin(a), 11 * (1 - f * 0.5), "#9FD8FF", lw=0)
    lbl(ctx, "空気がはぎとられる!?", CX, CY - 430, 90, s=pin(lt, 0.1))


def v_patch(ctx, lt, d, gt):
    space_bg(ctx, gt)
    mars(ctx, CX, CY + 80, 260 * pin(lt))
    for i, (dx, dy) in enumerate([(-100, 120), (40, 170), (130, 90), (-20, 60)]):
        r = 60 + 15 * math.sin(gt * 3 + i)
        ctx.new_path(); ctx.arc(CX + dx, CY + 80 + dy, r, 0, 2 * math.pi)
        ctx.set_source_rgba(0.5, 0.9, 1, 0.55); ctx.set_line_width(8); ctx.stroke()
    lbl(ctx, "あちこちに小さな磁石", CX, CY - 430, 84, s=pin(lt, 0.1))


def v_aurora(ctx, lt, d, gt):
    space_bg(ctx, gt)
    mars(ctx, CX, CY + 120, 250 * pin(lt))
    for k in range(4):
        ctx.new_path(); ctx.arc(CX, CY + 120, 275 + k * 18, math.pi * 1.1, math.pi * 1.9)
        ctx.set_source_rgba(0.3, 1, 0.5, 0.55 - 0.12 * k + 0.15 * math.sin(gt * 4 + k)); ctx.set_line_width(14); ctx.stroke()
    lbl(ctx, "火星にもオーロラ!", CX, CY - 430, 100, s=pin(lt, 0.1))


def v_bluesunset(ctx, lt, d, gt):
    ctx.rectangle(0, CY - 360, 1080, 760); ctx.set_source_rgba(*hexc("#C98A5A")); ctx.fill()
    circle(ctx, CX, CY + 220, 240 * pin(lt), "#9FC7E8", lw=0)
    circle(ctx, CX, CY + 220, 60, "#FFFFFF", lw=0)
    ctx.move_to(0, CY + 260)
    for i in range(10):
        ctx.line_to(i * 120, CY + 220 + (i % 3) * 30)
    ctx.line_to(1080, CY + 260); ctx.line_to(1080, CY + 400); ctx.line_to(0, CY + 400); ctx.close_path()
    ctx.set_source_rgba(*hexc("#6B3A22")); ctx.fill()
    lbl(ctx, "夕やけが青い!?", CX, CY - 430, 100, s=pin(lt, 0.1))


def v_pale(ctx, lt, d, gt):
    space_bg(ctx, gt)
    for k in range(3):
        ctx.move_to(CX - 400 + k * 300, CY - 300); ctx.line_to(CX - 200 + k * 300, CY + 400)
        ctx.set_source_rgba(1, 0.85, 0.6, 0.15); ctx.set_line_width(60); ctx.stroke()
    circle(ctx, CX + 80, CY + 60, 10 + 3 * math.sin(gt * 4), "#7FD3FF", lw=0)
    ctx.new_path(); ctx.arc(CX + 80, CY + 60, 50, 0, 2 * math.pi); ctx.set_source_rgba(1, 0.9, 0.3, 0.9); ctx.set_line_width(5); ctx.stroke()
    lbl(ctx, "1990年 ボイジャー1号", CX, CY - 430, 84, s=pin(lt, 0.1))
    lbl(ctx, "小さな青い点", CX, CY + 300, 90, s=pin(lt, 0.3), color="#FFE14D")


def v_human(ctx, lt, d, gt):
    ctx.rectangle(0, CY + 200, 1080, 300); ctx.set_source_rgba(*hexc("#C9673E")); ctx.fill()
    ctx.new_path(); ctx.arc(CX + 200, CY + 200, 170, math.pi, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.9); ctx.fill()
    piko(ctx, CX - 220, CY + 90, gt, 0.7 * pin(lt), "smile")
    twin(ctx, CX + 300, CY - 300, 0.35, gt, GOLD, face=False)
    lbl(ctx, "宇宙の天気予報で守る", CX, CY - 430, 86, s=pin(lt, 0.1))


def v_team(ctx, lt, d, gt):
    names = [("UCバークレー", "#3D7BFF"), ("ロケットラボ", "#FF3D7F"), ("NASA", "#1E3A8A"), ("ブルーオリジン", "#5BC0EB")]
    for k, (n, c) in enumerate(names):
        x = CX - 240 + (k % 2) * 480; y = CY - 120 + (k // 2) * 320
        circle(ctx, x, y, 140 * pin(lt, 0.1 * k), c, lw=8)
        lbl(ctx, n, x, y, 50 if len(n) > 4 else 64, s=pin(lt, 0.15 + 0.1 * k))
    lbl(ctx, "チームで作った", CX, CY - 430, 100, s=pin(lt, 0.1))


def v_size(ctx, lt, d, gt):
    twin(ctx, CX - 80, CY + 60, 1.2 * pin(lt), gt, BLUE)
    piko(ctx, CX + 340, CY + 200, gt, 0.55 * pin(lt, 0.2), "wow")
    lbl(ctx, "1台 約535kg", CX, CY - 430, 100, s=pin(lt, 0.1))


def v_comment(ctx, lt, d, gt):
    earth(ctx, CX + 220, CY + 160, 170 * pin(lt), gt)
    piko(ctx, CX - 260, CY + 100, gt, 0.75 * pin(lt, 0.2), "wow")
    lbl(ctx, "宇宙から撮りたいのは?", CX, CY - 430, 84, s=pin(lt, 0.1))


def v_hello(ctx, lt, d, gt):
    piko(ctx, CX - 220, CY + 200, gt, 1.0 * pin(lt), "smile")
    twin(ctx, CX + 240, CY + 80, 0.5 * pin(lt, 0.2), gt, GOLD)
    lbl(ctx, "またね!", CX, CY - 400, 120, s=pin(lt, 0.2))


def v_caution(ctx, lt, d, gt):
    twin(ctx, CX, CY + 200, 0.8 * pin(lt), gt, GOLD)
    draw_sprite(ctx, text_sprite("!", 220, color="#FFE14D", path=FONTS["dela"]), CX + 320, CY - 120, pin(lt, 0.2), 1)
    lbl(ctx, "まだ旅のとちゅう", CX, CY - 430, 100, s=pin(lt, 0.1))
