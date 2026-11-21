"""Visuals for the 'star swallowed its companion' (AT 2025abao / Bao, Andromeda) episode.
Vertical coordinate system shared with hera_vis (CX=540, CY from space2)."""
import math, random
from common4 import *
from space2 import pin, CX, CY, v_comment
from space import planet, sun as sun_icon, telescope
from hera_vis import label, space_bg, photo_scene, PHOTO_LAYOUT, v_question, rocket

RED = "#FF6B4A"
GIANT = "#FF7A45"
SMALL = "#FFF3B0"
EARTH = "#3FA9F5"


def glow(ctx, x, y, r, col, a=1.0):
    if r < 1:
        return
    c = hexc(col)
    g = cairo.RadialGradient(x, y, r * 0.2, x, y, r * 1.8)
    g.add_color_stop_rgba(0, c[0], c[1], c[2], 0.55 * a)
    g.add_color_stop_rgba(1, c[0], c[1], c[2], 0)
    ctx.new_path(); ctx.arc(x, y, r * 1.8, 0, 2 * math.pi); ctx.set_source(g); ctx.fill()
    circle(ctx, x, y, r, col, lw=max(4, r * 0.04))
    ctx.new_path(); ctx.arc(x - r * 0.3, y - r * 0.35, r * 0.22, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.35 * a); ctx.fill()


def face(ctx, x, y, r, mood="smile", gt=0.0):
    """Tiny cartoon face on a star."""
    e = r * 0.12
    for sx in (-1, 1):
        circle(ctx, x + sx * r * 0.3, y - r * 0.1, e, "#1B1B3A", lw=0)
    if mood == "open":
        ctx.new_path(); ctx.arc(x, y + r * 0.28, r * 0.28 * (0.8 + 0.2 * math.sin(gt * 9)), 0, 2 * math.pi)
        ctx.set_source_rgba(*hexc("#7A1F2B")); ctx.fill()
    elif mood == "scared":
        ctx.new_path(); ctx.arc(x, y + r * 0.3, r * 0.14, 0, 2 * math.pi); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.fill()
    else:
        ctx.new_path(); ctx.arc(x, y + r * 0.12, r * 0.28, 0.2, math.pi - 0.2)
        ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(max(3, r * 0.07)); ctx.stroke()


# ---------------------------------------------------------------- scenes
def v_hook_eat(ctx, lt, d, gt):
    space_bg(ctx, gt)
    gx, gy = CX - 60, CY + 40
    glow(ctx, gx, gy, 250 * pin(lt), GIANT)
    p = clamp(lt / max(1.2, d * 0.75))
    if p < 1:
        a = gt * 2.5
        rr = 430 * (1 - p) + 120 * p
        x, y = gx + rr * math.cos(a), gy + rr * 0.5 * math.sin(a)
        glow(ctx, x, y, 46, SMALL)
        face(ctx, x, y, 46, "scared")
        face(ctx, gx, gy, 250 * pin(lt), "open", gt)
    else:
        face(ctx, gx, gy, 250, "smile")
        burst(ctx, gx, gy - 300, 110, gt, "#FFE14D")
        label(ctx, "パクッ!", CX + 200, CY - 400, 130, color="#FF3D7F", s=pin(lt - d * 0.75), rot=-0.1)


def v_binary(ctx, lt, d, gt, small_r=44):
    space_bg(ctx, gt)
    a = gt * 1.3
    bx, by = CX + 40 * math.cos(a + math.pi), CY + 10 * math.sin(a + math.pi)
    sx, sy = CX + 380 * math.cos(a), CY + 120 * math.sin(a)
    ctx.save(); ctx.translate(CX, CY); ctx.scale(1, 0.32)
    ctx.new_path(); ctx.arc(0, 0, 380, 0, 2 * math.pi); ctx.restore()
    ctx.set_source_rgba(1, 1, 1, 0.35); ctx.set_line_width(5); ctx.set_dash([14, 12]); ctx.stroke(); ctx.set_dash([])
    order = [(by, lambda: (glow(ctx, bx, by, 200 * pin(lt), GIANT), face(ctx, bx, by, 200 * pin(lt)))),
             (sy, lambda: (glow(ctx, sx, sy, small_r, SMALL), face(ctx, sx, sy, small_r)))]
    for _, f in sorted(order, key=lambda o: o[0]):
        f()
    draw_sprite(ctx, text_sprite("大バオ", 64, path=FONTS["mochiy"]), bx, by + 270, pin(lt, 0.2), 1)
    draw_sprite(ctx, text_sprite("小バオ", 48, path=FONTS["mochiy"]), sx, sy - 90, pin(lt, 0.35), 1)


def v_names(ctx, lt, d, gt):
    rrect(ctx, 90, CY - 150, 900, 200, 40); fill_stroke(ctx, "#FFFFFF", lw=8)
    label(ctx, "AT 2025ab{ao}", CX, CY - 50, 96, color="#1B1B3A", hi="#FF3D7F", s=pin(lt))
    ctx.move_to(CX + 300, CY + 70); ctx.line_to(CX + 300, CY + 200)
    ctx.set_source_rgba(*hexc("#FFE14D")); ctx.set_line_width(14); ctx.stroke()
    label(ctx, "「バオ」", CX + 200, CY + 290, 120, color="#FFE14D", s=pin(lt, 0.3), rot=-0.05)


def v_sun_vs(ctx, lt, d, gt):
    # the giant's edge fills the screen, the Sun is a dot
    R = 2600
    ctx.new_path(); ctx.arc(CX + R - 380, CY + 40, R * pin(lt), 0, 2 * math.pi)
    ctx.set_source_rgba(*hexc(GIANT)); ctx.fill()
    ctx.new_path(); ctx.arc(CX + R - 380, CY + 40, R * pin(lt), 0, 2 * math.pi)
    ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(10); ctx.stroke()
    sun_icon(ctx, 120, CY + 40, 14 * pin(lt, 0.4), gt)
    ctx.move_to(120, CY - 20); ctx.line_to(120, CY - 120); ctx.set_source_rgba(1, 1, 1, 1); ctx.set_line_width(8); ctx.stroke()
    label(ctx, "太陽", 120, CY - 170, 60, font="mochiy", s=pin(lt, 0.45))
    label(ctx, "直径350倍!", CX + 140, CY - 380, 120, color="#FFE14D", s=pin(lt, 0.6), rot=-0.05)


def v_orbits(ctx, lt, d, gt, swallow=True, R_au=1.63, text="火星の軌道まで\nすっぽり!"):
    space_bg(ctx, gt)
    cx, cy = CX, CY + 40
    unit = 250  # px per AU
    if swallow:
        R = R_au * unit * ease_out_cubic(clamp((lt - 0.6) / max(0.8, d * 0.6)))
        if R > 2:
            ctx.new_path(); ctx.arc(cx, cy, R, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(GIANT, 0.85)); ctx.fill()
    for au, col, rr, name in [(0.39, "#B9B0A3", 12, "水星"), (0.72, "#F2C14E", 18, "金星"), (1.0, EARTH, 20, "地球"), (1.52, "#E2633A", 16, "火星")]:
        ctx.new_path(); ctx.arc(cx, cy, au * unit, 0, 2 * math.pi)
        ctx.set_source_rgba(1, 1, 1, 0.5); ctx.set_line_width(4); ctx.set_dash([10, 10]); ctx.stroke(); ctx.set_dash([])
        a = gt * (0.6 / au) + au * 5
        circle(ctx, cx + au * unit * math.cos(a), cy + au * unit * math.sin(a), rr, col, lw=4)
        draw_sprite(ctx, text_sprite(name, 34, path=FONTS["mochiy"]), cx + au * unit * math.cos(a), cy + au * unit * math.sin(a) - 40, 1, 1)
    sun_icon(ctx, cx, cy, 16, gt)
    if swallow:
        label(ctx, text, CX, CY - 470, 84, color="#FFE14D", s=pin(lt, 0.9))


def v_bright(ctx, lt, d, gt):
    sun_icon(ctx, 170, CY + 60, 40 * pin(lt), gt)
    label(ctx, "太陽", 170, CY + 170, 54, font="mochiy", s=pin(lt, 0.1))
    rnd = random.Random(3)
    n = int(60 * clamp(lt / max(0.8, d * 0.6)))
    for k in range(n):
        x, y = 360 + (k % 10) * 66, CY - 240 + (k // 10) * 66
        circle(ctx, x, y, 22, "#FFC93C", lw=3)
    label(ctx, "1万8000倍の明るさ", CX, CY - 420, 84, color="#FFE14D", s=pin(lt, 0.3))


def v_scale(ctx, lt, d, gt, left="大バオ", right="太陽", lw_=7, rw=1, lcol=GIANT, rcol="#FFC93C", title="重さは太陽の7倍"):
    base = CY + 260
    tilt = -0.28 * ease_out_back(clamp(lt / 0.8))
    ctx.save(); ctx.translate(CX, base)
    rrect(ctx, -20, 0, 40, 240, 10); fill_stroke(ctx, "#C9C9D6", lw=6)
    ctx.rotate(tilt)
    rrect(ctx, -400, -18, 800, 36, 18); fill_stroke(ctx, "#FFFFFF", lw=6)
    glow(ctx, -330, -110, 90, lcol)
    glow(ctx, 330, -60, 40, rcol)
    ctx.restore()
    draw_sprite(ctx, text_sprite(left, 54, path=FONTS["mochiy"]), CX - 320, base + 140, pin(lt, 0.2), 1)
    draw_sprite(ctx, text_sprite(right, 54, path=FONTS["mochiy"]), CX + 320, base + 20, pin(lt, 0.3), 1)
    label(ctx, title, CX, CY - 420, 90, color="#FFE14D", s=pin(lt, 0.3))


def v_small(ctx, lt, d, gt):
    space_bg(ctx, gt)
    glow(ctx, CX - 200, CY + 20, 120 * pin(lt), "#FFC93C"); face(ctx, CX - 200, CY + 20, 120 * pin(lt))
    glow(ctx, CX + 220, CY + 50, 100 * pin(lt, 0.2), SMALL); face(ctx, CX + 220, CY + 50, 100 * pin(lt, 0.2))
    draw_sprite(ctx, text_sprite("太陽", 56, path=FONTS["mochiy"]), CX - 200, CY + 220, pin(lt, 0.1), 1)
    draw_sprite(ctx, text_sprite("小バオ", 56, path=FONTS["mochiy"]), CX + 220, CY + 220, pin(lt, 0.3), 1)
    label(ctx, "太陽より少し小さい", CX, CY - 400, 84, s=pin(lt, 0.4))


def v_spiral(ctx, lt, d, gt):
    space_bg(ctx, gt)
    gx, gy = CX, CY + 40
    # giant with puffy envelope
    ctx.new_path(); ctx.arc(gx, gy, 380, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(GIANT, 0.35)); ctx.fill()
    glow(ctx, gx, gy, 170, GIANT)
    p = (lt / max(d, 1.5))
    ctx.new_path()
    for k in range(200):
        q = k / 199
        rr = 400 * (1 - 0.75 * q); a = q * 4 * 2 * math.pi
        ctx.line_to(gx + rr * math.cos(a), gy + rr * 0.8 * math.sin(a))
    ctx.set_source_rgba(1, 1, 1, 0.5); ctx.set_line_width(5); ctx.set_dash([12, 10]); ctx.stroke(); ctx.set_dash([])
    q = clamp(p)
    rr = 400 * (1 - 0.75 * q); a = q * 4 * 2 * math.pi
    glow(ctx, gx + rr * math.cos(a), gy + rr * 0.8 * math.sin(a), 34, SMALL)
    label(ctx, "ぐるぐる落ちていく", CX, CY - 450, 84, color="#FFE14D", s=pin(lt, 0.2))


def v_brake(ctx, lt, d, gt):
    ctx.rectangle(0, CY - 200, 1080, 440); ctx.set_source_rgba(*hexc(GIANT, 0.55)); ctx.fill()
    rnd = random.Random(2)
    for k in range(40):
        x = (rnd.uniform(0, 1080) - gt * 500 * rnd.uniform(0.6, 1.2)) % 1080
        y = CY - 180 + rnd.uniform(0, 400)
        ctx.move_to(x, y); ctx.line_to(x + 80, y); ctx.set_source_rgba(1, 1, 1, 0.5); ctx.set_line_width(6); ctx.stroke()
    x = CX + 30 * math.sin(gt * 7)
    glow(ctx, x, CY + 20, 70, SMALL); face(ctx, x, CY + 20, 70, "scared")
    label(ctx, "ガスの中でブレーキ!", CX, CY - 400, 84, color="#FFE14D", s=pin(lt, 0.2))
    label(ctx, "ズズズ…", CX, CY + 360, 90, s=pin(lt, 0.4), rot=0.05)


def v_week(ctx, lt, d, gt):
    base = CY + 260
    ctx.move_to(100, base); ctx.line_to(1000, base); ctx.set_source_rgba(1, 1, 1, 0.9); ctx.set_line_width(8); ctx.stroke()
    for k in range(7):
        x = 160 + k * 125
        on = lt > 0.25 + k * 0.18
        rrect(ctx, x - 50, base + 30, 100, 100, 16); fill_stroke(ctx, "#FFE14D" if on else "#FFFFFF", lw=6)
        draw_sprite(ctx, text_sprite(f"{k + 1}日", 40, color="#1B1B3A", stroke="#FFFFFF", stroke_w=2, shadow=False, path=FONTS["mochiy"]), x, base + 80, 1, 1)
    p = clamp((lt - 0.25) / 1.3)
    ctx.move_to(160, base - 20)
    for k in range(60):
        q = k / 59 * p
        ctx.line_to(160 + q * 750, base - 20 - 520 * (q ** 3))
    ctx.set_source_rgba(*hexc("#FF3D7F")); ctx.set_line_width(14); ctx.stroke()
    if p >= 1:
        burst(ctx, 910, base - 540, 80, gt, "#FFE14D")
    label(ctx, "たった1週間でピーク!", CX, CY - 440, 84, color="#FFE14D", s=pin(lt, 0.2))


def v_bomb(ctx, lt, d, gt):
    glow(ctx, CX, CY + 40, 260, GIANT)
    p = clamp(lt / max(0.8, d * 0.5))
    if p < 1:
        ctx.save(); ctx.translate(CX, CY + 40); s = 0.6 + 0.4 * p; ctx.scale(s, s)
        circle(ctx, 0, 0, 80, "#1B1B3A", stroke="#FFFFFF", lw=6)
        ctx.move_to(40, -60); ctx.curve_to(70, -120, 110, -110, 120, -150); ctx.set_source_rgba(1, 1, 1, 1); ctx.set_line_width(8); ctx.stroke()
        sparkles(ctx, 120, -150, lt, 0, "#FFE14D", 8, 60)
        ctx.restore()
    else:
        burst(ctx, CX, CY + 40, 420 + 40 * math.sin(lt * 20), gt, "#FFE14D", n=18)
        sparkles(ctx, CX, CY + 40, lt, d * 0.5, "#FFB34D", 24, 600)
        label(ctx, "星の中で爆弾!?", CX, CY - 420, 100, color="#FF3D7F", s=pin(lt - d * 0.5), rot=-0.06)


def v_lightbeam(ctx, lt, d, gt, years="250万年"):
    space_bg(ctx, gt)
    ctx.save(); ctx.translate(880, CY - 260); ctx.rotate(-0.5); ctx.scale(1, 0.4)
    g = cairo.RadialGradient(0, 0, 10, 0, 0, 200)
    g.add_color_stop_rgba(0, 1, 0.95, 0.85, 1); g.add_color_stop_rgba(0.4, 0.75, 0.7, 1, 0.7); g.add_color_stop_rgba(1, 0.4, 0.3, 0.9, 0)
    ctx.new_path(); ctx.arc(0, 0, 200 * pin(lt), 0, 2 * math.pi); ctx.set_source(g); ctx.fill(); ctx.restore()
    planet(ctx, 170, CY + 300, 100 * pin(lt, 0.1), EARTH)
    for k in range(5):
        q = ((lt * 0.35) + k / 5) % 1
        x = 880 - (880 - 170) * q; y = CY - 260 + (CY + 300 - (CY - 260)) * q
        circle(ctx, x, y, 14, "#FFE14D", lw=0)
    label(ctx, "アンドロメダ銀河", 760, CY - 470, 60, font="mochiy", s=pin(lt, 0.2))
    label(ctx, f"光で{years}!", CX, CY + 470, 100, color="#FFE14D", s=pin(lt, 0.4), rot=-0.04)


def v_timemachine(ctx, lt, d, gt):
    ctx.save(); ctx.translate(CX, CY + 20); s = pin(lt); ctx.scale(s, s)
    ctx.move_to(-170, -260); ctx.line_to(170, -260); ctx.line_to(20, 0); ctx.line_to(170, 260); ctx.line_to(-170, 260); ctx.line_to(-20, 0); ctx.close_path()
    fill_stroke(ctx, "#BFE9FF", lw=10)
    f = (lt / max(d, 1)) % 1
    ctx.move_to(-120 * (1 - f), -230 + 230 * f); ctx.line_to(120 * (1 - f), -230 + 230 * f); ctx.line_to(0, -10); ctx.close_path()
    ctx.set_source_rgba(*hexc("#F2C14E")); ctx.fill()
    ctx.move_to(-150 * f, 240); ctx.line_to(150 * f, 240); ctx.line_to(0, 240 - 160 * f); ctx.close_path(); ctx.fill()
    ctx.restore()
    label(ctx, "250万年前の\nできごと!", CX, CY - 440, 90, color="#FFE14D", s=pin(lt, 0.3))


def v_sky(ctx, lt, d, gt, show_m31=True):
    rnd = random.Random(21)
    for k in range(60):
        star(ctx, rnd.uniform(20, 1060), rnd.uniform(380, 1100), rnd.uniform(3, 8) * (0.6 + 0.4 * math.sin(gt * 3 + k)), "#FFFFFF", 0.9)
    if show_m31:
        ctx.save(); ctx.translate(700, CY - 160); ctx.rotate(-0.5); ctx.scale(1, 0.38)
        g = cairo.RadialGradient(0, 0, 4, 0, 0, 140)
        g.add_color_stop_rgba(0, 1, 1, 0.9, 0.95); g.add_color_stop_rgba(1, 0.7, 0.7, 1, 0)
        ctx.new_path(); ctx.arc(0, 0, 140 * pin(lt, 0.3), 0, 2 * math.pi); ctx.set_source(g); ctx.fill(); ctx.restore()
        ctx.new_path(); ctx.arc(700, CY - 160, 120 + 6 * math.sin(gt * 5), 0, 2 * math.pi)
        ctx.set_source_rgba(*hexc("#FFE14D")); ctx.set_line_width(6); ctx.stroke()
    ctx.move_to(0, CY + 420); ctx.line_to(240, CY + 260); ctx.line_to(420, CY + 380); ctx.line_to(640, CY + 220); ctx.line_to(1080, CY + 420)
    ctx.line_to(1080, CY + 600); ctx.line_to(0, CY + 600); ctx.close_path(); fill_stroke(ctx, "#2A2350", lw=6)
    piko(ctx, 260, CY + 300, gt, 0.6, "wow", look=0.6)
    label(ctx, "秋の夜空で見える!", CX, CY - 470, 84, color="#FFE14D", s=pin(lt, 0.2))


def v_far_eye(ctx, lt, d, gt):
    ctx.save(); ctx.translate(CX, CY + 20); s = pin(lt); ctx.scale(s, s)
    ctx.move_to(-300, 0); ctx.curve_to(-150, -190, 150, -190, 300, 0); ctx.curve_to(150, 190, -150, 190, -300, 0); ctx.close_path()
    fill_stroke(ctx, "#FFFFFF", lw=10)
    circle(ctx, 30 * math.sin(gt), 0, 110, "#3FA9F5", lw=8); circle(ctx, 30 * math.sin(gt), 0, 50, "#1B1B3A", lw=0)
    ctx.restore()
    label(ctx, "肉眼で見える\nいちばん遠いもの級!", CX, CY - 430, 80, color="#FFE14D", s=pin(lt, 0.3))


def jwst(ctx, x, y, s, gt):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    # sunshield
    ctx.move_to(-300, 140); ctx.line_to(0, 60); ctx.line_to(300, 140); ctx.line_to(0, 220); ctx.close_path(); fill_stroke(ctx, "#C9A0FF", lw=6)
    # hexagon mirror (18 segments)
    hr = 34
    pts = [(0, 0)]
    for ring in (1, 2):
        for k in range(6 * ring):
            side, f = divmod(k, ring)
            a0 = math.pi / 6 + side * math.pi / 3; a1 = a0 + math.pi / 3
            px = ring * (math.cos(a0) * (1 - f / ring) + math.cos(a1) * f / ring)
            py = ring * (math.sin(a0) * (1 - f / ring) + math.sin(a1) * f / ring)
            pts.append((px, py))
    for (px, py) in pts[1:]:
        cx_, cy_ = px * hr * 1.75, py * hr * 1.75 - 40
        ctx.new_path()
        for k in range(6):
            a = k * math.pi / 3
            ctx.line_to(cx_ + hr * math.cos(a), cy_ + hr * math.sin(a))
        ctx.close_path(); fill_stroke(ctx, "#F2C14E", lw=4)
    ctx.move_to(0, -40); ctx.line_to(0, -230); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(8); ctx.stroke()
    circle(ctx, 0, -230, 16, "#FFFFFF", lw=5)
    ctx.restore()


def v_webb(ctx, lt, d, gt):
    space_bg(ctx, gt)
    jwst(ctx, CX, CY + 40 + 14 * math.sin(gt * 2), 1.15 * pin(lt), gt)
    label(ctx, "ウェッブ宇宙望遠鏡", CX, CY - 430, 80, color="#FFE14D", s=pin(lt, 0.2))


def v_mirror(ctx, lt, d, gt):
    jwst(ctx, CX, CY + 60, 1.4 * pin(lt), gt)
    label(ctx, "鏡は6.5m・金ぴか!", CX, CY - 430, 84, color="#FFE14D", s=pin(lt, 0.3))


def v_xmas(ctx, lt, d, gt):
    rrect(ctx, CX - 300, CY - 280, 380, 420, 40); fill_stroke(ctx, "#FFFFFF", lw=10)
    rrect(ctx, CX - 300, CY - 280, 380, 120, 40); fill_stroke(ctx, "#2BB673", lw=10)
    label(ctx, "12月", CX - 110, CY - 220, 70, s=pin(lt))
    label(ctx, "24", CX - 110, CY + 10, 200, color="#FF3D7F", hi="#FF3D7F", s=pin(lt, 0.15))
    # tree
    ctx.save(); ctx.translate(CX + 270, CY + 140); s = pin(lt, 0.25); ctx.scale(s, s)
    for k, w in enumerate([200, 160, 110]):
        ctx.move_to(-w, -k * 110); ctx.line_to(0, -k * 110 - 170); ctx.line_to(w, -k * 110); ctx.close_path(); fill_stroke(ctx, "#2BB673", lw=6)
    star(ctx, 0, -400, 50, "#FFE14D")
    rrect(ctx, -30, 0, 60, 70, 8); fill_stroke(ctx, "#8A5A2B", lw=6)
    ctx.restore()
    label(ctx, "クリスマスイブ!", CX, CY + 380, 100, color="#FFE14D", s=pin(lt, 0.4), rot=-0.05)


def v_47days(ctx, lt, d, gt):
    n = int(47 * clamp(lt / max(0.8, d * 0.6)))
    for k in range(47):
        x, y = 140 + (k % 8) * 115, CY - 300 + (k // 8) * 100
        rrect(ctx, x - 44, y - 38, 88, 76, 14); fill_stroke(ctx, "#FFE14D" if k < n else "#FFFFFF", lw=5)
    label(ctx, f"{max(1, n)}日", CX, CY + 400, 130, color="#FF3D7F", s=pin(lt, 0.1))
    label(ctx, "ピークから47日後!", CX, CY - 450, 84, color="#FFE14D", s=pin(lt, 0.3))


def v_relay(ctx, lt, d, gt):
    names = ["NEOWISE", "WINTER", "SPHEREx", "ZTF", "スウィフト", "ジェミニ", "ウェッブ"]
    for k, n in enumerate(names):
        x = 160 + (k % 4) * 255 + (127 if k >= 4 else 0)
        y = CY - 180 + (k // 4) * 330
        s = pin(lt, 0.12 * k)
        ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
        circle(ctx, 0, 0, 90, ["#7FD3FF", "#B6F07A", "#FF8FB1", "#FFE14D", "#C9A0FF", "#FFB36B", "#F2C14E"][k], lw=7)
        ctx.rotate(-0.6); rrect(ctx, -22, -60, 44, 100, 12); fill_stroke(ctx, "#FFFFFF", lw=5); ctx.rotate(0.6)
        ctx.restore()
        draw_sprite(ctx, text_sprite(n, 36, path=FONTS["mochiy"]), x, y + 120, s, 1)
    label(ctx, "望遠鏡リレー!", CX, CY - 460, 100, color="#FFE14D", s=pin(lt, 0.2))


def v_timeline(ctx, lt, d, gt, upto=5):
    ev = [("2018", "明るくなりはじめ"), ("2023", "様子が変!"), ("2024", "ちりが出る"), ("2025.10", "大爆発!"), ("2025.12", "ウェッブ")]
    x0, x1 = 120, 960
    ctx.move_to(x0, CY + 40); ctx.line_to(x1, CY + 40); ctx.set_source_rgba(1, 1, 1, 0.9); ctx.set_line_width(10); ctx.stroke()
    for k, (yy, t) in enumerate(ev[:upto]):
        x = x0 + (x1 - x0) * k / 4
        s = pin(lt, 0.15 * k)
        circle(ctx, x, CY + 40, 26 * s, "#FF3D7F" if k == 3 else "#FFE14D", lw=6)
        draw_sprite(ctx, text_sprite(yy, 44, path=FONTS["dela"]), x, CY - 40 - (60 if k % 2 else 0), s, 1)
        draw_sprite(ctx, text_sprite(t, 34, path=FONTS["mochiy"]), x, CY + 130 + (60 if k % 2 else 0), s, 1)
    label(ctx, "何年もかけて変化", CX, CY - 430, 84, color="#FFE14D", s=pin(lt, 0.2))


def v_dust(ctx, lt, d, gt):
    space_bg(ctx, gt)
    glow(ctx, CX, CY + 40, 140, GIANT)
    rnd = random.Random(4)
    for k in range(70):
        a = rnd.uniform(0, 2 * math.pi); r = 170 + ((lt * 120 + k * 23) % 330)
        circle(ctx, CX + r * math.cos(a), CY + 40 + r * 0.8 * math.sin(a), rnd.uniform(5, 11), "#C9A27E", lw=0)
    label(ctx, "ちりのカーテン", CX, CY - 420, 90, color="#FFE14D", s=pin(lt, 0.2))


def v_earths(ctx, lt, d, gt):
    n = int(220 * clamp(lt / max(0.8, d * 0.7)))
    rnd = random.Random(6)
    for k in range(n):
        planet(ctx, rnd.uniform(80, 1000), rnd.uniform(CY - 300, CY + 330), 16, EARTH)
    label(ctx, "地球 3万〜7万個分!", CX, CY - 440, 84, color="#FFE14D", s=pin(lt, 0.2))
    label(ctx, "ふき飛んだガス", CX, CY + 430, 76, s=pin(lt, 0.4))


def v_one_star(ctx, lt, d, gt):
    space_bg(ctx, gt)
    glow(ctx, CX, CY + 40, 230 * pin(lt), "#FFB36B")
    face(ctx, CX, CY + 40, 230 * pin(lt))
    sparkles(ctx, CX, CY + 40, lt, 0.1, "#FFE14D", 14, 420)
    label(ctx, "1つの星に!?", CX, CY - 420, 110, color="#FFE14D", s=pin(lt, 0.3))


def v_rejuv(ctx, lt, d, gt):
    space_bg(ctx, gt)
    glow(ctx, CX - 60, CY + 60, 200 * pin(lt), "#FFB36B")
    face(ctx, CX - 60, CY + 60, 200 * pin(lt))
    ctx.save(); ctx.translate(CX + 200, CY - 180); ctx.rotate(0.3)
    for k in range(3):
        draw_sprite(ctx, text_sprite("キラ", 54, color="#FFE14D", path=FONTS["dela"]), k * 70, k * 60, pin(lt, 0.2 + 0.1 * k), 1)
    ctx.restore()
    label(ctx, "若返った!?", CX, CY + 400, 110, color="#FF3D7F", s=pin(lt, 0.3), rot=-0.05)


def v_pairs(ctx, lt, d, gt):
    space_bg(ctx, gt)
    rnd = random.Random(8)
    for k in range(9):
        x, y = 180 + (k % 3) * 360, CY - 260 + (k // 3) * 280
        a = gt * rnd.uniform(1, 2.5) + k
        s = pin(lt, 0.06 * k)
        glow(ctx, x - 40 * math.cos(a), y - 14 * math.sin(a), 36 * s, rnd.choice(["#FFC93C", "#FFB36B", "#9FD8FF"]))
        glow(ctx, x + 60 * math.cos(a), y + 20 * math.sin(a), 20 * s, rnd.choice([SMALL, "#FF8FB1", "#BFE9FF"]))
    label(ctx, "ペアの星がいっぱい", CX, CY - 470, 84, color="#FFE14D", s=pin(lt, 0.2))


def v_fate(ctx, lt, d, gt):
    items = [("中性子星", "#BFE9FF"), ("ブラックホール", "#1B1B3A"), ("超新星", "#FFE14D")]
    for k, (n, col) in enumerate(items):
        x = 200 + k * 340; s = pin(lt, 0.15 * k)
        if col == "#1B1B3A":
            ctx.new_path(); ctx.arc(x, CY, 120 * s, 0, 2 * math.pi); ctx.set_source_rgba(1, 0.6, 0.2, 0.8); ctx.set_line_width(18); ctx.stroke()
            circle(ctx, x, CY, 100 * s, col, stroke="#FFB36B", lw=4)
        elif k == 2:
            burst(ctx, x, CY, 120 * s + 10 * math.sin(gt * 10), gt, col)
        else:
            glow(ctx, x, CY, 70 * s, col)
        draw_sprite(ctx, text_sprite(n, 44, path=FONTS["mochiy"]), x, CY + 200, s, 1)
    label(ctx, "ペアの星の行く末", CX, CY - 430, 84, color="#FFE14D", s=pin(lt, 0.3))


def v_sun_future(ctx, lt, d, gt):
    space_bg(ctx, gt)
    p = ease_in_out(clamp(lt / max(1.0, d * 0.8)))
    r = 60 + 330 * p
    col = "#FFC93C" if p < 0.4 else GIANT
    glow(ctx, CX - 260, CY + 40, r, col)
    face(ctx, CX - 260, CY + 40, r, "smile")
    planet(ctx, CX + 330, CY + 40, 40, EARTH)
    label(ctx, "50億年後の太陽", CX, CY - 440, 90, color="#FFE14D", s=pin(lt, 0.2))


def v_safe_sun(ctx, lt, d, gt):
    sun_icon(ctx, CX - 220, CY + 20, 120 * pin(lt), gt)
    circle(ctx, CX + 240, CY + 20, 130 * pin(lt, 0.2), "#3CE07A", lw=10)
    ctx.move_to(CX + 180, CY + 20); ctx.line_to(CX + 225, CY + 70); ctx.line_to(CX + 305, CY - 40)
    ctx.set_source_rgba(1, 1, 1, 1); ctx.set_line_width(24); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    label(ctx, "太陽はひとりっ子", CX, CY - 420, 90, color="#FFE14D", s=pin(lt, 0.3))
    label(ctx, "食べられる心配なし!", CX, CY + 360, 84, s=pin(lt, 0.45))


def v_rush(ctx, lt, d, gt):
    space_bg(ctx, gt)
    telescope(ctx, CX, CY + 360, gt, 1.2 * pin(lt))
    rnd = random.Random(12)
    for k in range(8):
        x, y = rnd.uniform(120, 960), rnd.uniform(CY - 380, CY + 40)
        s = pin(lt, 0.2 + 0.1 * k)
        burst(ctx, x, y, 40 * s, gt, "#FFE14D", n=10)
        draw_sprite(ctx, text_sprite("!", 60, color="#FF3D7F", path=FONTS["dela"]), x, y, s, 1)
    label(ctx, "発見ラッシュが来る!", CX, CY - 470, 84, color="#FFE14D", s=pin(lt, 0.2))


def v_long_short(ctx, lt, d, gt):
    """Shorts ending: points down to the link."""
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY); ctx.scale(s, s)
    rrect(ctx, -400, -240, 800, 460, 40); fill_stroke(ctx, "#1B1B3A", lw=12)
    rrect(ctx, -370, -210, 740, 400, 26); fill_stroke(ctx, "#FF3D7F", lw=0)
    ctx.move_to(-60, -90); ctx.line_to(100, -10); ctx.line_to(-60, 70); ctx.close_path(); fill_stroke(ctx, "#FFFFFF", lw=8)
    ctx.restore()
    label(ctx, "特別編で\nぜんぶ解説!", CX, CY - 430, 90, color="#FFE14D", s=pin(lt, 0.2), rot=-0.05)
    yy = CY + 330 + 30 * abs(math.sin(gt * 5))
    label(ctx, "↓", CX, yy, 150, color="#FFE14D", s=pin(lt, 0.4))


# ---------------------------------------------------------------- real images (credit always right under the image)
C_MAIN = "NASA, ESA, CSA, STScI, V. Karambelkar・K. De(Columbia)/DSS, R. Gendler"
C_ART = "NASA, ESA, CSA, STScI, Leah Hustak (STScI) 想像図"
C_PANEL = "NASA, ESA, CSA, STScI, V. Karambelkar・K. De (Columbia)"
C_M31 = "NASA, ESA, B. Williams (University of Washington)"
C_V838 = "NASA, ESA, H.E. Bond (STScI)"
P_main = photo_scene("bao_main", C_MAIN, "本物の観測画像!", box=(980, 660))
P_and = photo_scene("bao_andromeda", C_MAIN, "□の中にバオ", box=(940, 760), crop=(850, 250, 780, 630))
P_and_wide = photo_scene("bao_andromeda", C_MAIN, "アンドロメダ銀河のはし", box=(940, 760))
P_quiet = photo_scene("p_quiet", C_PANEL, "1 ふだん", box=(640, 640))
P_pre = photo_scene("p_pre", C_PANEL, "2 明るくなってきた", box=(640, 640))
P_erupt = photo_scene("p_erupt", C_PANEL, "3 大爆発!", box=(640, 640))
P_post = photo_scene("p_post", C_PANEL, "4 ウェッブが見た今", box=(640, 640))
P_art1 = photo_scene("art1", C_ART, "1 ちりにつつまれた2つの星", box=(980, 551))
P_art2 = photo_scene("art2", C_ART, "2 小さい星がのみこまれる", box=(980, 551))
P_art3 = photo_scene("art3", C_ART, "3 ドカーン!", box=(980, 551))
P_art4 = photo_scene("art4", C_ART, "4 南北にちりが広がる", box=(980, 551))
P_art_all = photo_scene("art_all", C_ART, "4コマで見ると…", box=(980, 551))
P_m31 = photo_scene("m31_hubble", C_M31, "ハッブルのアンドロメダ", box=(980, 520), crop=(500, 0, 1400, 561))
P_m31_wide = photo_scene("m31_hubble", C_M31, "2億個以上の星が写った!", box=(980, 300))
P_v838 = photo_scene("v838", C_V838, "V838いっかくじゅう座", box=(760, 830))
P_v838_seq = photo_scene("v838_seq", C_V838, "光のこだま", box=(980, 563))


def v_orbits_sun(ctx, lt, d, gt):
    v_orbits(ctx, lt, d, gt, R_au=0.85, text="水星・金星は\nのみこまれるかも")
