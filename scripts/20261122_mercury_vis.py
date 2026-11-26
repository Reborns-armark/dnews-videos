"""Visuals for the BepiColombo / Mercury episode (vertical coordinate system, CX=540, CY=960)."""
import math, random
from common4 import *
from engine import pil_to_surface
from space2 import pin, CX, CY
from space import planet, sun
from hera_vis import space_bg, label, photo_scene, PHOTO_LAYOUT, v_question, v_longvideo, rocket
import hera_vis

MERC = "#A8A29A"
OPTS = {"short": False}
EARTH = "#3FA9F5"
VENUS = "#F2C46D"
PLUTO = "#C9A27E"


def mercury(ctx, x, y, r, gt=0.0, face=False):
    if r < 3:
        return
    planet(ctx, x, y, r, MERC)
    rnd = random.Random(4)
    ctx.save(); ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.clip()
    for k in range(9):
        a = rnd.uniform(0, 6.28); rr = rnd.uniform(0.1, 0.75) * r
        ctx.new_path(); ctx.arc(x + rr * math.cos(a + gt * 0.1), y + rr * math.sin(a + gt * 0.1), rnd.uniform(0.05, 0.12) * r, 0, 2 * math.pi)
        ctx.set_source_rgba(0.3, 0.28, 0.26, 0.35); ctx.fill()
    ctx.restore()
    if face:
        for sx in (-1, 1):
            circle(ctx, x + sx * r * 0.28, y - r * 0.08, r * 0.1, "#1B1B3A", lw=0)
        ctx.new_path(); ctx.arc(x, y + r * 0.12, r * 0.22, 0.2, math.pi - 0.2)
        ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(max(3, r * 0.05)); ctx.stroke()


def bepi(ctx, x, y, s, gt, mio=True, mpo=True, mtm=False, rot=0.0):
    """Stacked BepiColombo: MPO (silver box + solar wing), Mio (octagon) on top."""
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot + 0.05 * math.sin(gt * 2)); ctx.scale(s, s)
    if mtm:
        rrect(ctx, -70, 70, 140, 90, 10); fill_stroke(ctx, "#D9DCE6", lw=6)
        for sx in (-1, 1):
            ctx.save(); ctx.translate(sx * 70, 115)
            for k in range(2):
                rrect(ctx, (0 if sx > 0 else -260) + sx * 0 + (k * 130 if sx > 0 else -k * 130 + 130), -28, 120, 56, 6)
                fill_stroke(ctx, "#2E4BB8", lw=5)
            ctx.restore()
        # ion glow
        for k in range(4):
            ctx.new_path(); ctx.arc(0, 175 + k * 30, 22 - 4 * k, 0, 2 * math.pi)
            ctx.set_source_rgba(0.4, 0.7, 1.0, 0.7 - 0.15 * k); ctx.fill()
    if mpo:
        rrect(ctx, -70, -40, 140, 110, 12); fill_stroke(ctx, "#E8E8F0", lw=7)
        ctx.move_to(70, 10); ctx.line_to(130, 10); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(6); ctx.stroke()
        rrect(ctx, 130, -30, 230, 80, 6); fill_stroke(ctx, "#3D5BFF", lw=6)
        for k in range(4):
            ctx.move_to(130 + 46 * (k + 1), -30); ctx.rel_line_to(0, 80)
        ctx.set_source_rgba(1, 1, 1, 0.5); ctx.set_line_width(3); ctx.stroke()
        draw_sprite(ctx, text_sprite("MPO", 30, color="#1B1B3A", stroke="#FFFFFF", stroke_w=3, shadow=False, path=FONTS["dela"]), 0, 20, 1, 1)
    if mio:
        oy = -110 if mpo else 0
        ctx.save(); ctx.translate(0, oy); ctx.rotate(gt * (1.6 if not mpo else 0))
        ctx.new_path()
        for k in range(8):
            a = math.pi / 8 + k * math.pi / 4
            ctx.line_to(78 * math.cos(a), 78 * math.sin(a))
        ctx.close_path(); fill_stroke(ctx, "#FF8FB1", lw=7)
        ctx.restore()
        draw_sprite(ctx, text_sprite("みお", 32, color="#FFFFFF", stroke="#1B1B3A", stroke_w=5, shadow=False, path=FONTS["dela"]), 0, oy, 1, 1)
    ctx.restore()


def bigcard(text, sub=None, color="#FFE14D", bg=True, icon=None):
    """Generic: one big number/word, optional subline, optional little icon function."""
    def vis(ctx, lt, d, gt):
        if bg:
            space_bg(ctx, gt)
        if icon:
            icon(ctx, lt, gt)
        draw_sprite(ctx, text_sprite(text, 230, color=color, hi="#FF3D7F", path=FONTS["dela"]), CX, CY - 60, pin(lt), 1, -0.04)
        if sub:
            draw_sprite(ctx, text_sprite(sub, 78, color="#FFFFFF", hi="#FFE14D", path=FONTS["mochiy"]), CX, CY + 160, pin(lt, 0.2), 1)
    return vis


def v_hook_mercury(ctx, lt, d, gt):
    space_bg(ctx, gt)
    sun(ctx, CX - 330, CY - 380, 160 * pin(lt), gt)
    mercury(ctx, CX + 180, CY + 80, 230 * pin(lt, 0.1), gt, face=True)
    p = ease_in_out(clamp(lt / max(d * 0.8, 0.8)))
    bepi(ctx, CX + 380 - 120 * p, CY - 260 + 120 * p, 0.55 * pin(lt, 0.2), gt)
    label(ctx, "水星", CX + 180, CY + 380, 110, s=pin(lt, 0.25))


def v_eight_years(ctx, lt, d, gt):
    space_bg(ctx, gt)
    draw_sprite(ctx, text_sprite("{8}年", 420, color="#FFFFFF", hi="#FFE14D", path=FONTS["dela"]), CX, CY - 40, ease_out_back(clamp(lt / 0.35), 2.4), 1, -0.05)
    label(ctx, "お隣の水星まで", CX, CY - 380, 90, s=pin(lt, 0.15), font="mochiy")
    sparkles(ctx, CX, CY - 40, lt, 0.0, "#FFE14D", 18, 520)


def v_solar(ctx, lt, d, gt):
    space_bg(ctx, gt)
    sun(ctx, 130, CY, 120 * pin(lt), gt)
    for i, (r, col, nm, sp) in enumerate([(300, MERC, "水星", 4.1), (520, VENUS, "金星", 1.6), (760, EARTH, "地球", 1.0)]):
        ctx.new_path(); ctx.arc(130, CY, r, -1.0, 1.0); ctx.set_source_rgba(1, 1, 1, 0.3); ctx.set_line_width(4); ctx.set_dash([10, 10]); ctx.stroke(); ctx.set_dash([])
        a = 0.7 * math.sin(gt * 0.4 * sp + i)
        x, y = 130 + r * math.cos(a), CY + r * math.sin(a)
        planet(ctx, x, y, [34, 50, 54][i] * pin(lt, 0.1 * i), col)
        draw_sprite(ctx, text_sprite(nm, 52, path=FONTS["mochiy"]), x, y - 90, pin(lt, 0.1 * i + 0.1), 1)
    label(ctx, "太陽にいちばん近い!", CX, CY - 320, 84, s=pin(lt, 0.3))


def v_pluto(ctx, lt, d, gt):
    base = CY + 330
    ctx.rectangle(80, base, 920, 12); ctx.set_source_rgba(1, 1, 1, 0.8); ctx.fill()
    for i, (nm, h, col) in enumerate([("冥王星へ", 290, PLUTO), ("水星をまわる", 450, MERC)]):
        x = CX - 210 + i * 420
        hh = h * ease_out_cubic(clamp((lt - 0.2 * i) / 0.7))
        rrect(ctx, x - 110, base - hh, 220, hh, 20); fill_stroke(ctx, col, lw=8)
        draw_sprite(ctx, text_sprite(nm, 58, path=FONTS["mochiy"]), x, base - hh - 50, pin(lt, 0.2 * i), 1)
    label(ctx, "必要なエネルギー", CX, CY - 320, 90, s=pin(lt, 0.1))
    if lt > 0.9:
        burst(ctx, CX + 330, base - 500, 60, gt, "#FFE14D")


def v_slope(ctx, lt, d, gt):
    """Sun's gravity = a slope: the ball speeds up going down."""
    ctx.move_to(60, CY - 300); ctx.curve_to(420, CY - 280, 560, CY + 300, 1020, CY + 360)
    ctx.set_source_rgba(1, 1, 1, 0.9); ctx.set_line_width(14); ctx.stroke()
    sun(ctx, 960, CY + 470, 90, gt)
    p = (lt / max(d, 1.0)) ** 1.8
    t = clamp(p)
    # cubic bezier point
    P0, P1, P2, P3 = (60, CY - 300), (420, CY - 280), (560, CY + 300), (1020, CY + 360)
    bx = (1 - t) ** 3 * P0[0] + 3 * (1 - t) ** 2 * t * P1[0] + 3 * (1 - t) * t * t * P2[0] + t ** 3 * P3[0]
    by = (1 - t) ** 3 * P0[1] + 3 * (1 - t) ** 2 * t * P1[1] + 3 * (1 - t) * t * t * P2[1] + t ** 3 * P3[1]
    bepi(ctx, bx, by - 60, 0.4, gt, rot=0.4)
    for k in range(int(6 * t)):
        ctx.move_to(bx - 80 - k * 40, by - 80 - k * 18); ctx.rel_line_to(-50, -20)
        ctx.set_source_rgba(1, 0.9, 0.4, 0.7); ctx.set_line_width(6); ctx.stroke()
    label(ctx, "どんどん速くなる!", CX, CY - 320, 90, s=pin(lt, 0.2))


def v_brake(ctx, lt, d, gt):
    space_bg(ctx, gt)
    bepi(ctx, CX, CY, 0.9 * pin(lt), gt)
    for k in range(5):
        x = CX - 300 - k * 30 + 20 * math.sin(gt * 20 + k)
        ctx.move_to(x, CY - 150 + k * 70); ctx.rel_line_to(-120, 0)
        ctx.set_source_rgba(1, 1, 1, 0.5); ctx.set_line_width(8); ctx.stroke()
    label(ctx, "ブレーキが大変!", CX, CY - 320, 100, color="#FF3D7F", s=pin(lt, 0.2), rot=-0.05)


def v_flybys(ctx, lt, d, gt):
    space_bg(ctx, gt)
    items = [(EARTH, "地球", 1), (VENUS, "金星", 2), (MERC, "水星", 6)]
    for i, (col, nm, n) in enumerate(items):
        y = CY - 280 + i * 240
        planet(ctx, 220, y, 90 * pin(lt, 0.15 * i), col)
        draw_sprite(ctx, text_sprite(nm, 60, path=FONTS["mochiy"]), 220, y + 130, pin(lt, 0.15 * i), 1)
        for k in range(n):
            if lt > 0.3 + 0.15 * i + 0.08 * k:
                star(ctx, 400 + k * 105, y, 40, "#FFE14D")
    label(ctx, "合計{9}回!", CX, CY + 430, 120, s=pin(lt, 0.9))


def v_swingby(ctx, lt, d, gt):
    space_bg(ctx, gt)
    planet(ctx, CX, CY + 60, 170 * pin(lt), VENUS)
    p = clamp(lt / max(d * 0.9, 0.8))
    a = -2.6 + 3.4 * p
    r = 330
    x, y = CX + r * math.cos(a), CY + 60 + r * 0.8 * math.sin(a)
    ctx.new_path(); ctx.arc(CX, CY + 60, r, -2.6, a); ctx.set_source_rgba(1, 0.9, 0.4, 0.8); ctx.set_line_width(8); ctx.set_dash([18, 12]); ctx.stroke(); ctx.set_dash([])
    bepi(ctx, x, y, 0.35, gt)
    label(ctx, "惑星の重力でブレーキ", CX, CY - 320, 80, s=pin(lt, 0.2))


def v_route(ctx, lt, d, gt):
    space_bg(ctx, gt)
    sun(ctx, CX, CY, 70, gt)
    p = clamp(lt / max(d * 0.9, 1))
    ctx.new_path()
    for k in range(int(200 * p) + 1):
        u = k / 200 * 7 * math.pi
        r = 430 - 300 * (k / 200)
        ctx.line_to(CX + r * math.cos(u), CY + r * math.sin(u))
    ctx.set_source_rgba(1, 0.88, 0.3, 0.9); ctx.set_line_width(6); ctx.stroke()
    label(ctx, "約{100億}km!", CX, CY - 320, 110, s=pin(lt, 0.2))
    if not OPTS["short"]:
        label(ctx, "ぐるぐる約8年", CX, CY + 430, 80, s=pin(lt, 0.4), font="mochiy")


def v_launch(ctx, lt, d, gt):
    p = ease_in_out(clamp(lt / max(d, 0.8)))
    y = CY + 300 - 600 * p
    for k in range(8):
        circle(ctx, CX + 30 * math.sin(gt * 9 + k), y + 230 + k * 50, 50 - k * 4, ["#FFE14D", "#FF8A3D"][k % 2], lw=0)
    rocket(ctx, CX, y, 1.0)
    label(ctx, "2018年10月", CX - 230, CY - 320, 80, s=pin(lt, 0.2), rot=-0.06)


def v_ion(ctx, lt, d, gt):
    space_bg(ctx, gt)
    bepi(ctx, CX, CY - 80, 0.9 * pin(lt), gt, mtm=True)
    label(ctx, "電気のエンジン", CX, CY - 320, 96, s=pin(lt, 0.2))
    label(ctx, "青い光", CX + 260, CY + 420, 70, color="#7FD3FF", s=pin(lt, 0.4), font="mochiy")


def v_trouble(ctx, lt, d, gt):
    space_bg(ctx, gt)
    bepi(ctx, CX, CY, 0.8, gt, mtm=True)
    if int(gt * 4) % 2:
        draw_sprite(ctx, text_sprite("!", 260, color="#FF3D7F", path=FONTS["dela"]), CX + 300, CY - 260, 1, 1)
    label(ctx, "パワーが出ない…", CX, CY - 320, 96, s=pin(lt, 0.2))
    label(ctx, "到着が約1年おくれた", CX, CY + 430, 70, s=pin(lt, 0.4), font="mochiy")


def v_selfie(ctx, lt, d, gt):
    space_bg(ctx, gt)
    bepi(ctx, CX - 120, CY + 60, 0.8 * pin(lt), gt, mtm=True)
    rrect(ctx, CX + 200, CY - 260, 150, 110, 18); fill_stroke(ctx, "#1B1B3A", lw=6)
    circle(ctx, CX + 275, CY - 205, 34, "#7FD3FF", lw=6)
    if (gt * 2) % 1 < 0.15:
        ctx.rectangle(0, 0, 1080, 1920); ctx.set_source_rgba(1, 1, 1, 0.35); ctx.fill()
    label(ctx, "自撮りカメラ!", CX, CY - 320, 100, s=pin(lt, 0.2))


def v_temp(ctx, lt, d, gt):
    for i, (t, col, lab, fill) in enumerate([("400℃以上", "#FF3D7F", "昼", 0.95), ("-170℃", "#4FC3FF", "夜", 0.12)]):
        x = CX - 230 + i * 460
        rrect(ctx, x - 50, CY - 260, 100, 480, 50); fill_stroke(ctx, "#FFFFFF", lw=8)
        h = 440 * fill * ease_out_cubic(clamp((lt - 0.2 * i) / 0.7))
        rrect(ctx, x - 30, CY + 200 - h, 60, h, 30); ctx.set_source_rgba(*hexc(col)); ctx.fill()
        circle(ctx, x, CY + 260, 90, col, lw=8)
        draw_sprite(ctx, text_sprite(lab, 70, path=FONTS["dela"]), x, CY + 260, pin(lt, 0.1 * i), 1)
        draw_sprite(ctx, text_sprite(t, 74, color=col, stroke="#FFFFFF", path=FONTS["dela"]), x, CY - 330, pin(lt, 0.2 + 0.2 * i), 1)


def v_day(ctx, lt, d, gt):
    for i, (nm, n, col) in enumerate([("水星の1年", "88日", "#7FD3FF"), ("水星の1日", "176日", "#FF8FB1")]):
        y = CY - 250 + i * 460
        rrect(ctx, 120, y - 160, 840, 320, 40); fill_stroke(ctx, col, lw=8)
        label(ctx, nm, CX, y - 70, 70, color="#1B1B3A", hi="#FFFFFF", s=pin(lt, 0.2 * i), font="mochiy")
        label(ctx, n, CX, y + 60, 130, s=pin(lt, 0.1 + 0.25 * i))


def v_ice(ctx, lt, d, gt):
    sun(ctx, 140, CY - 520, 80, gt)
    ctx.move_to(0, CY + 120); ctx.line_to(260, CY + 120); ctx.curve_to(340, CY + 120, 340, CY + 420, 540, CY + 420)
    ctx.curve_to(740, CY + 420, 740, CY + 120, 820, CY + 120); ctx.line_to(1080, CY + 120); ctx.line_to(1080, CY + 700); ctx.line_to(0, CY + 700); ctx.close_path()
    fill_stroke(ctx, MERC, lw=8)
    ctx.move_to(140, CY - 520); ctx.line_to(300, CY + 120); ctx.line_to(1080, CY + 40); ctx.line_to(1080, CY - 700); ctx.close_path()
    ctx.set_source_rgba(1, 0.95, 0.6, 0.18); ctx.fill()
    s = pin(lt, 0.3)
    for k in range(5):
        rrect(ctx, 420 + k * 50 - 30 * s, CY + 360 - 30 * s, 50 * s, 50 * s, 8); fill_stroke(ctx, "#CFF3FF", lw=5)
    label(ctx, "ずっと日かげ", CX, CY + 230, 70, color="#FFFFFF", s=pin(lt, 0.2), font="mochiy")
    label(ctx, "氷がある!?", CX, CY - 380, 120, color="#7FD3FF", s=pin(lt, 0.4))


def v_core(ctx, lt, d, gt):
    r = 330 * pin(lt)
    circle(ctx, CX, CY, r, MERC, lw=10)
    circle(ctx, CX, CY, r * 0.85 * pin(lt, 0.3), "#E0703A", lw=8)
    circle(ctx, CX, CY, r * 0.5 * pin(lt, 0.4), "#FFB34D", lw=0)
    label(ctx, "鉄のしん", CX, CY, 100, s=pin(lt, 0.5))
    label(ctx, "ほとんど鉄!?", CX, CY - 320, 110, s=pin(lt, 0.3))


def v_magnet(ctx, lt, d, gt):
    space_bg(ctx, gt)
    mercury(ctx, CX, CY, 150 * pin(lt), gt)
    for k in range(1, 4):
        for sx in (-1, 1):
            ctx.save(); ctx.translate(CX, CY); ctx.scale(sx, 1)
            ctx.new_path(); ctx.move_to(0, -150)
            ctx.curve_to(140 * k + 60, -320 * k * 0.6 - 150, 140 * k + 60, 320 * k * 0.6 + 150, 0, 150)
            ctx.restore()
            ctx.set_source_rgba(0.5, 0.85, 1, 0.7 * pin(lt, 0.1 * k)); ctx.set_line_width(6); ctx.stroke()
    label(ctx, "磁石の力!", CX, CY - 320, 110, s=pin(lt, 0.2))


def v_shrink(ctx, lt, d, gt):
    k = 1 - 0.12 * ease_in_out(clamp(lt / max(d * 0.8, 0.8)))
    mercury(ctx, CX, CY, 300 * k * pin(lt), gt)
    for i in range(5):
        y = CY - 180 + i * 90
        ctx.move_to(CX - 200 * k, y); ctx.curve_to(CX - 60 * k, y - 30, CX + 60 * k, y + 30, CX + 200 * k, y)
        ctx.set_source_rgba(0.25, 0.22, 0.2, 0.6); ctx.set_line_width(7); ctx.stroke()
    label(ctx, "ちぢんでしわしわ!?", CX, CY - 320, 96, s=pin(lt, 0.2))


def v_dark(ctx, lt, d, gt):
    space_bg(ctx, gt)
    planet(ctx, CX - 230, CY, 190 * pin(lt), "#E6E6E6")
    planet(ctx, CX + 230, CY, 190 * pin(lt, 0.15), "#7A746D")
    label(ctx, "月", CX - 230, CY + 280, 80, s=pin(lt, 0.2))
    label(ctx, "水星", CX + 230, CY + 280, 80, s=pin(lt, 0.3))
    label(ctx, "水星はけっこう黒い", CX, CY - 320, 84, s=pin(lt, 0.4))


def v_colombo(ctx, lt, d, gt):
    ctx.save(); ctx.translate(CX - 160, CY + 120); s = pin(lt); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, -220, 110, 0, 2 * math.pi); fill_stroke(ctx, "#F5D3B3", lw=8)
    ctx.new_path(); ctx.arc(0, -250, 112, math.pi, 2 * math.pi); fill_stroke(ctx, "#6B6B6B", lw=8)
    rrect(ctx, -150, -100, 300, 330, 60); fill_stroke(ctx, "#3D5BFF", lw=8)
    for sx in (-1, 1):
        circle(ctx, sx * 40, -210, 14, "#1B1B3A", lw=0)
    ctx.restore()
    draw_sprite(ctx, text_sprite("イタリア", 64, path=FONTS["mochiy"]), CX + 260, CY - 120, pin(lt, 0.2), 1)
    draw_sprite(ctx, text_sprite("科学者", 64, path=FONTS["mochiy"]), CX + 260, CY - 20, pin(lt, 0.3), 1)
    label(ctx, "ベピ・コロンボさん", CX, CY - 320, 96, s=pin(lt, 0.2))


def v_mariner(ctx, lt, d, gt):
    space_bg(ctx, gt)
    mercury(ctx, CX, CY + 80, 150 * pin(lt), gt)
    for k in range(3):
        a = gt * 0.8 + k * 2.1
        ctx.new_path(); ctx.arc(CX, CY + 80, 300 + 30 * k, 0, 2 * math.pi)
        ctx.set_source_rgba(1, 1, 1, 0.2); ctx.set_line_width(4); ctx.stroke()
    a = gt * 1.2
    hera_vis.probe(ctx, CX + 300 * math.cos(a), CY + 80 + 300 * math.sin(a), 0.6, gt) if hasattr(hera_vis, "probe") else None
    label(ctx, "何度も会える道!", CX, CY - 320, 100, s=pin(lt, 0.2))


def v_capture(ctx, lt, d, gt):
    space_bg(ctx, gt)
    mercury(ctx, CX, CY + 240, 100 * pin(lt), gt)
    p = ease_in_out(clamp(lt / max(d * 0.9, 1)))
    ctx.save(); ctx.translate(CX, CY + 20); ctx.scale(0.55, 1.0)
    ctx.new_path(); ctx.arc(0, 0, 290, 0, 2 * math.pi); ctx.restore()
    ctx.set_source_rgba(1, 0.88, 0.3, 0.7 * pin(lt, 0.2)); ctx.set_line_width(7); ctx.set_dash([18, 12]); ctx.stroke(); ctx.set_dash([])
    a = math.pi / 2 + 2 * math.pi * p * 0.9
    bepi(ctx, CX + 160 * math.cos(a), CY + 20 + 290 * math.sin(a), 0.3, gt)
    label(ctx, "重力につかまえてもらう!", CX, CY - 330, 76, s=pin(lt, 0.2))
    if not OPTS["short"]:
        label(ctx, "いちばん遠いとき 約17万8000km", CX, CY + 430, 54, s=pin(lt, 0.4), font="mochiy")


def v_split(ctx, lt, d, gt):
    space_bg(ctx, gt)
    p = ease_in_out(clamp((lt - 0.3) / max(d * 0.7, 0.8)))
    bepi(ctx, CX - 160 * p, CY + 120 + 60 * p, 0.9 * pin(lt), gt, mio=False)
    bepi(ctx, CX + 200 * p, CY - 110 - 160 * p, 0.9 * pin(lt), gt, mpo=False)
    label(ctx, "ふたつに分かれる!", CX, CY - 320, 100, s=pin(lt, 0.2))


def v_mio(ctx, lt, d, gt):
    space_bg(ctx, gt)
    bepi(ctx, CX, CY, 2.2 * pin(lt), gt, mpo=False)
    label(ctx, "みお(澪)", CX, CY - 380, 110, s=pin(lt, 0.2))
    label(ctx, "JAXA", CX, CY + 330, 110, color="#FF3D7F", s=pin(lt, 0.35))


def v_twoorbits(ctx, lt, d, gt):
    space_bg(ctx, gt)
    mercury(ctx, CX, CY, 120 * pin(lt), gt)
    for (rx, ry, col, nm, sp, rot) in [(220, 170, "#E8E8F0", "MPO", 2.2, 0.0), (460, 260, "#FF8FB1", "みお", 0.7, 0.0)]:
        ctx.save(); ctx.translate(CX, CY - (ry - 140)); ctx.scale(rx / ry, 1)
        ctx.new_path(); ctx.arc(0, 0, ry, 0, 2 * math.pi); ctx.restore()
        ctx.set_source_rgba(*hexc(col, 0.8)); ctx.set_line_width(6); ctx.stroke()
        a = gt * sp
        x, y = CX + rx * math.cos(a), CY - (ry - 140) + ry * math.sin(a)
        circle(ctx, x, y, 26, col, lw=5)
        draw_sprite(ctx, text_sprite(nm, 44, path=FONTS["dela"]), x, y - 52, 1, 1)
    label(ctx, "2機で同時に!", CX, CY - 320, 100, s=pin(lt, 0.2))


def v_calendar2(month, day, sub=None):
    def vis(ctx, lt, d, gt):
        rrect(ctx, CX - 260, CY - 260, 520, 520, 40); fill_stroke(ctx, "#FFFFFF", lw=10)
        rrect(ctx, CX - 260, CY - 260, 520, 140, 40); fill_stroke(ctx, "#FF3D7F", lw=10)
        label(ctx, month, CX, CY - 190, 80, s=pin(lt))
        draw_sprite(ctx, text_sprite(day, 220, color="#1B1B3A", stroke="#FFFFFF", path=FONTS["dela"]), CX, CY + 60, pin(lt, 0.15), 1)
        if sub:
            label(ctx, sub, CX, CY + 400, 80, s=pin(lt, 0.3), font="mochiy")
    return vis


def v_team2(ctx, lt, d, gt):
    for k, (col, name) in enumerate([("#F2C14E", "ESA"), ("#FF3D7F", "JAXA")]):
        x = CX - 220 + k * 440
        circle(ctx, x, CY, 180 * pin(lt, k * 0.12), col, lw=10)
        label(ctx, name, x, CY, 96, color="#1B1B3A", hi="#FFFFFF", s=pin(lt, 0.1 + k * 0.12))
    label(ctx, "ヨーロッパ×日本", CX, CY - 320, 100, s=pin(lt, 0.3))


def v_tea(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 100); ctx.scale(s, s)
    for k, y in enumerate([200, 40, -120]):
        w = 420 - 90 * k
        ctx.save(); ctx.scale(1, 0.25); ctx.new_path(); ctx.arc(0, y * 4, w, 0, 2 * math.pi); ctx.restore()
        fill_stroke(ctx, "#FFFFFF", lw=6)
        for j in range(3 - k + 2):
            circle(ctx, -w * 0.6 + j * (w * 1.2 / max(1, 3 - k + 1)), y - 30, 34, ["#FF8FB1", "#FFE14D", "#A8A29A"][j % 3], lw=5)
    ctx.move_to(0, -360); ctx.line_to(0, 200); ctx.set_source_rgba(*hexc("#C9A227")); ctx.set_line_width(12); ctx.stroke()
    ctx.restore()
    label(ctx, "水星のアフタヌーンティー!?", CX, CY - 320, 76, s=pin(lt, 0.2))


def v_contest(ctx, lt, d, gt):
    items = ["人形劇", "詩", "歌", "ししゅう", "ねんど", "絵"]
    for i, t in enumerate(items):
        x = 230 + (i % 3) * 310; y = CY - 160 + (i // 3) * 300
        rrect(ctx, x - 130, y - 110, 260, 220, 30); fill_stroke(ctx, ["#7FD3FF", "#FF8FB1", "#FFE14D"][i % 3], lw=7)
        label(ctx, t, x, y, 64, color="#1B1B3A", hi="#FFFFFF", s=pin(lt, 0.08 * i), font="mochiy")
    label(ctx, "ようこそ水星へ!", CX, CY - 320, 100, s=pin(lt, 0.2))
    label(ctx, "60作品以上", CX, CY + 430, 90, s=pin(lt, 0.6))


def v_sunlight(ctx, lt, d, gt):
    sun(ctx, CX, CY + 20, 150 * pin(lt), gt)
    bepi(ctx, CX, CY + 300, 0.5, gt)
    label(ctx, "日ざしは地球の約10倍", CX, CY - 300, 76, s=pin(lt, 0.3))


def v_messenger(ctx, lt, d, gt):
    space_bg(ctx, gt)
    mercury(ctx, CX, CY + 230, 150 * pin(lt), gt)
    for i, (yr, nm) in enumerate([("1974年", "マリナー10号"), ("2011年", "メッセンジャー"), ("2026年", "ベピコロンボ")]):
        y = CY - 320 + i * 100
        label(ctx, f"{yr} {nm}", CX, y, 64, color="#FFFFFF" if i < 2 else "#FFE14D", s=pin(lt, 0.2 * i + 0.1), font="mochiy")


# ---------------------------------------------------------------- real photos (credit always under the photo)
MCAM = "ESA/BepiColombo/MTM"
ESA_ART = "ESA/ATG medialab"
P_north = photo_scene("northpole", MCAM, "本物の水星の北極!", box=(820, 820))
P_north_lab = photo_scene("northpole_lab", MCAM, "ずっと日かげのクレーター", box=(820, 820))
P_sunlit = photo_scene("sunlit", MCAM, "日の当たる北の平原", box=(820, 820))
P_lava = photo_scene("lava", MCAM, "明るい=若い場所", box=(820, 820))
P_selfie = photo_scene("lava", MCAM, "ベピコロンボが撮った!", box=(820, 820))
P_flyby6 = P_selfie
P_best6 = photo_scene("best6", MCAM, "旅のとちゅうの写真", box=(980, 326))
P_art = photo_scene("mtmsep", ESA_ART, "切りはなしのイメージ", box=(980, 551))
P_timeline = photo_scene("timeline", "ESA", "到着の予定表", box=(980, 551), crop=(560, 100, 700, 700))
P_timeline_late = photo_scene("timeline", "ESA", "このあとの予定", box=(980, 551), crop=(950, 100, 710, 700))
