"""Visuals for the 'potatoes in simulated lunar soil' episode (vertical coordinate system, CX=540, CY=960)."""
import math, random
from common4 import *
from space2 import pin, CX, CY
from space import planet, sun
from hera_vis import space_bg, label, photo_scene, PHOTO_LAYOUT, v_question, v_longvideo, rocket
import hera_vis

MOON = "#B9B6AE"
MARE = "#6E6A66"
HIGH = "#D8D4CC"
EARTHSOIL = "#6B4A2B"
COMPOST = "#3B2A1C"
POTATO = "#C98B5A"
REDSKIN = "#C2554B"
LEAF = "#4CC85A"
OPTS = {"short": False}


# ---------------------------------------------------------------- characters / props
def moon(ctx, x, y, r, gt=0.0, face=False):
    if r < 3:
        return
    planet(ctx, x, y, r, MOON)
    rnd = random.Random(7)
    ctx.save(); ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.clip()
    for k in range(10):
        a = rnd.uniform(0, 6.28); rr = rnd.uniform(0.1, 0.8) * r
        ctx.new_path(); ctx.arc(x + rr * math.cos(a), y + rr * math.sin(a), rnd.uniform(0.05, 0.14) * r, 0, 2 * math.pi)
        ctx.set_source_rgba(0.35, 0.34, 0.33, 0.35); ctx.fill()
    ctx.restore()
    if face:
        for sx in (-1, 1):
            circle(ctx, x + sx * r * 0.28, y - r * 0.08, r * 0.09, "#1B1B3A", lw=0)
        ctx.new_path(); ctx.arc(x, y + r * 0.12, r * 0.22, 0.2, math.pi - 0.2)
        ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(max(3, r * 0.05)); ctx.stroke()


def potato(ctx, x, y, s, gt=0.0, face=True, col=POTATO, mood="smile", green=0.0, sprout=False):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.rotate(0.06 * math.sin(gt * 3)); ctx.scale(s, s)
    ctx.new_path()
    pts = [(1.0, 0.0), (0.8, 0.62), (0.15, 0.78), (-0.55, 0.7), (-1.0, 0.15), (-0.85, -0.5), (-0.2, -0.75), (0.55, -0.66)]
    for i in range(len(pts)):
        x0, y0 = pts[i]; x1, y1 = pts[(i + 1) % len(pts)]
        mx, my = (x0 + x1) / 2 * 150, (y0 + y1) / 2 * 150
        if i == 0:
            ctx.move_to(mx, my)
        else:
            ctx.curve_to(x0 * 150, y0 * 150, x0 * 150, y0 * 150, mx, my)
    x0, y0 = pts[0]; mx, my = (pts[-1][0] + x0) / 2 * 150, (pts[-1][1] + y0) / 2 * 150
    ctx.curve_to(x0 * 150, y0 * 150, x0 * 150, y0 * 150, (x0 + pts[1][0]) / 2 * 150, (y0 + pts[1][1]) / 2 * 150)
    ctx.close_path()
    fill_stroke(ctx, col, lw=8)
    if green > 0:
        ctx.save(); ctx.new_path(); ctx.arc(70, -40, 80, 0, 6.28); ctx.set_source_rgba(0.3, 0.75, 0.2, green); ctx.fill(); ctx.restore()
    for (ex, ey) in [(-90, 40), (100, 50), (40, -80), (-40, -70)]:
        circle(ctx, ex, ey, 7, "#8A5A35", lw=0)
    if sprout:
        ctx.move_to(-30, -100); ctx.curve_to(-40, -150, -10, -170, 0, -200)
        ctx.set_source_rgba(*hexc("#B57FD0")); ctx.set_line_width(12); ctx.stroke()
    if face:
        for sx in (-1, 1):
            circle(ctx, sx * 42, -10, 14, "#1B1B3A", lw=0)
            circle(ctx, sx * 38, -15, 5, "#FFFFFF", lw=0)
        if mood == "wow":
            circle(ctx, 0, 40, 18, "#1B1B3A", lw=0)
        else:
            ctx.new_path(); ctx.arc(0, 20, 30, 0.3, math.pi - 0.3)
            ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(7); ctx.stroke()
        for sx in (-1, 1):
            ctx.new_path(); ctx.arc(sx * 75, 22, 14, 0, 6.28); ctx.set_source_rgba(1, 0.45, 0.55, 0.5); ctx.fill()
    ctx.restore()


def plant(ctx, x, base, h, gt, leaves=4, col=LEAF):
    if h < 3:
        return
    sway = 0.04 * math.sin(gt * 2.5 + x)
    ctx.save(); ctx.translate(x, base); ctx.rotate(sway)
    ctx.move_to(0, 0); ctx.line_to(0, -h); ctx.set_source_rgba(*hexc("#2E8B3A")); ctx.set_line_width(max(4, h * 0.05)); ctx.stroke()
    n = max(1, int(leaves * min(1, h / 200)))
    for k in range(n):
        yy = -h * (0.35 + 0.6 * k / max(1, n))
        sd = 1 if k % 2 else -1
        ctx.save(); ctx.translate(0, yy); ctx.rotate(sd * 0.6); ctx.scale(1, 0.5)
        ctx.new_path(); ctx.arc(sd * h * 0.16, 0, h * 0.16, 0, 6.28); ctx.restore()
        fill_stroke(ctx, col, lw=4)
    ctx.restore()


def pot(ctx, x, base, w, h, soil, gt, ph=0.0, tubers=0, tag=None, tagcol="#FFFFFF", s=1.0):
    """Flower pot cut-away: soil colour, plant of height ph, tubers drawn under the soil."""
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, base); ctx.scale(s, s)
    ctx.move_to(-w / 2, -h); ctx.line_to(w / 2, -h); ctx.line_to(w * 0.38, 0); ctx.line_to(-w * 0.38, 0); ctx.close_path()
    fill_stroke(ctx, "#E07A4F", lw=7)
    ctx.move_to(-w / 2 + 12, -h + 30); ctx.line_to(w / 2 - 12, -h + 30); ctx.line_to(w * 0.38 - 10, -14); ctx.line_to(-w * 0.38 + 10, -14); ctx.close_path()
    ctx.set_source_rgba(*hexc(soil)); ctx.fill()
    rnd = random.Random(int(x))
    for k in range(tubers):
        potato(ctx, rnd.uniform(-w * 0.25, w * 0.25), -h * rnd.uniform(0.3, 0.6), 0.22 + 0.04 * (k % 2), gt, face=False, col=REDSKIN)
    rrect(ctx, -w / 2 - 10, -h - 30, w + 20, 40, 10); fill_stroke(ctx, "#E07A4F", lw=7)
    plant(ctx, 0, -h - 30, ph, gt)
    ctx.restore()
    if tag and not OPTS["short"]:
        label(ctx, tag, x, base + 60 * s, 56, color=tagcol, s=s, font="mochiy")


def worm(ctx, x, y, s, gt):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path()
    for k in range(40):
        t = k / 39
        ctx.line_to(-200 + 400 * t, 35 * math.sin(t * 9 + gt * 6))
    ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(64); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke_preserve()
    ctx.set_source_rgba(*hexc("#F28BA8")); ctx.set_line_width(50); ctx.stroke()
    hy = 35 * math.sin(9 + gt * 6)
    for sx in (-1, 1):
        circle(ctx, 200 + sx * 10, hy - 8, 6, "#1B1B3A", lw=0)
    ctx.new_path(); ctx.arc(200, hy + 6, 9, 0.2, math.pi - 0.2); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def ground(ctx, y, col):
    ctx.rectangle(0, y, 1080, 1920 - y); ctx.set_source_rgba(*hexc(col)); ctx.fill()
    ctx.move_to(0, y); ctx.line_to(1080, y); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(8); ctx.stroke()


def bigcard(text, sub=None, color="#FFE14D", bg=True):
    def vis(ctx, lt, d, gt):
        if bg:
            space_bg(ctx, gt)
        draw_sprite(ctx, text_sprite(text, 230, color=color, hi="#FF3D7F", path=FONTS["dela"]), CX, CY - 60, pin(lt), 1, -0.04)
        if sub:
            draw_sprite(ctx, text_sprite(sub, 78, color="#FFFFFF", hi="#FFE14D", path=FONTS["mochiy"]), CX, CY + 160, pin(lt, 0.2), 1)
    return vis


# ---------------------------------------------------------------- scenes
def v_hook(ctx, lt, d, gt):
    space_bg(ctx, gt)
    moon(ctx, CX, CY + 520, 520 * pin(lt), gt)
    pot(ctx, CX, CY + 120, 300, 220, MARE, gt, ph=230 * clamp((lt - 0.3) / 0.8), tubers=2, s=pin(lt, 0.15))
    potato(ctx, CX + 300, CY - 260, 0.9 * pin(lt, 0.3), gt, mood="wow")
    label(ctx, "月の砂で…", CX - 170, CY - 360, 96, s=pin(lt, 0.1))


def v_moon_potato(ctx, lt, d, gt):
    space_bg(ctx, gt)
    moon(ctx, CX - 180, CY - 120, 260 * pin(lt), gt, face=True)
    potato(ctx, CX + 230, CY + 160, 1.2 * pin(lt, 0.15), gt)
    label(ctx, "×", CX + 40, CY + 20, 120, s=pin(lt, 0.25))


def v_regolith(ctx, lt, d, gt):
    """Magnified moon sand: sharp glassy grains."""
    s = pin(lt)
    circle(ctx, CX, CY, 380 * s, "#2B2B3A", lw=14)
    rnd = random.Random(3)
    ctx.save(); ctx.new_path(); ctx.arc(CX, CY, 370 * s, 0, 6.28); ctx.clip()
    for k in range(34):
        x, y = CX + rnd.uniform(-360, 360), CY + rnd.uniform(-360, 360)
        r = rnd.uniform(25, 60) * s
        ctx.new_path()
        n = rnd.randint(3, 5)
        for j in range(n):
            a = j * 6.28 / n + rnd.uniform(-0.4, 0.4)
            ctx.line_to(x + r * math.cos(a), y + r * math.sin(a))
        ctx.close_path(); fill_stroke(ctx, rnd.choice([MOON, HIGH, MARE, "#9FB4C8"]), lw=4)
    ctx.restore()
    ctx.move_to(CX + 270, CY + 270); ctx.line_to(CX + 440, CY + 440); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(40); ctx.stroke()
    label(ctx, "トゲトゲ!", CX, CY - 470, 100, s=pin(lt, 0.3), rot=-0.05)


def v_no_n(ctx, lt, d, gt):
    rrect(ctx, CX - 300, CY - 300, 600, 600, 60); fill_stroke(ctx, "#7FD3FF", lw=10)
    draw_sprite(ctx, text_sprite("N", 380, color="#1B1B3A", stroke="#FFFFFF", path=FONTS["dela"]), CX, CY, pin(lt), 1)
    p = clamp((lt - 0.4) / 0.3)
    if p > 0:
        ctx.move_to(CX - 330, CY - 330); ctx.line_to(CX - 330 + 660 * p, CY - 330 + 660 * p)
        ctx.set_source_rgba(*hexc("#FF3D7F")); ctx.set_line_width(46); ctx.stroke()
    label(ctx, "ちっ素(栄養)なし", CX, CY - 420, 90, s=pin(lt, 0.2))


def v_metal(ctx, lt, d, gt):
    for i, (sym, col) in enumerate([("Cu", "#D9844A"), ("Zn", "#A9B4C2"), ("Al", "#D0D6DE")]):
        x = CX - 300 + i * 300
        circle(ctx, x, CY, 125 * pin(lt, 0.1 * i), col, lw=8)
        label(ctx, sym, x, CY, 110, color="#1B1B3A", hi="#FFFFFF", s=pin(lt, 0.1 * i + 0.1))
    label(ctx, "金属が多め", CX, CY - 330, 100, s=pin(lt, 0.3))
    if lt > 0.8:
        burst(ctx, CX - 300, CY - 170, 50, gt, "#FFE14D")


def v_copper(ctx, lt, d, gt):
    pot(ctx, CX - 180, CY + 330, 300, 230, MARE, gt, ph=70, s=pin(lt))
    circle(ctx, CX + 250, CY - 80, 150 * pin(lt, 0.2), "#D9844A", lw=10)
    label(ctx, "Cu", CX + 250, CY - 80, 130, color="#1B1B3A", hi="#FFFFFF", s=pin(lt, 0.25))
    label(ctx, "銅", CX + 250, CY + 120, 90, s=pin(lt, 0.35))
    label(ctx, "犯人は銅!?", CX, CY - 420, 100, s=pin(lt, 0.4), rot=-0.04)


def v_simulants(ctx, lt, d, gt):
    cols = [MARE, "#7C7772", "#8A8580", HIGH, "#E4E0D8"]
    for i, c in enumerate(cols):
        x = 160 + i * 190
        s = pin(lt, 0.08 * i)
        rrect(ctx, x - 75, CY - 140, 150, 300, 30); fill_stroke(ctx, "#FFFFFF", lw=7)
        rrect(ctx, x - 62, CY - 60 + 0, 124, 206 * s, 22); fill_stroke(ctx, c, lw=0)
        label(ctx, str(i + 1), x, CY - 210, 70, s=s)
    label(ctx, "暗い「海」", 250, CY + 260, 62, font="mochiy", s=pin(lt, 0.5))
    label(ctx, "明るい「高地」", 820, CY + 260, 62, font="mochiy", s=pin(lt, 0.6))
    label(ctx, "ニセの月の砂 5種類", CX, CY - 380, 84, s=pin(lt, 0.2))


def v_mare_high(ctx, lt, d, gt):
    space_bg(ctx, gt)
    moon(ctx, CX, CY, 330 * pin(lt), gt)
    for (x, y, r) in [(CX - 90, CY - 60, 90), (CX + 80, CY + 60, 70), (CX - 20, CY + 130, 50)]:
        ctx.new_path(); ctx.arc(x, y, r * pin(lt, 0.2), 0, 6.28); ctx.set_source_rgba(*hexc(MARE)); ctx.fill()
    label(ctx, "暗い所=「海」", CX, CY - 440, 80, s=pin(lt, 0.3), font="mochiy")
    label(ctx, "明るい所=「高地」", CX, CY + 440, 80, s=pin(lt, 0.45), font="mochiy")


def v_modoc(ctx, lt, d, gt):
    potato(ctx, CX, CY - 20, 1.7 * pin(lt), gt, col=REDSKIN)
    label(ctx, "モドック", CX, CY - 380, 110, s=pin(lt, 0.2))
    label(ctx, "皮は赤・中は白", CX, CY + 300, 80, s=pin(lt, 0.35), font="mochiy")


def v_greenhouse(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 200); ctx.scale(s, s)
    ctx.move_to(-400, 0); ctx.line_to(-400, -330); ctx.curve_to(-400, -560, 400, -560, 400, -330); ctx.line_to(400, 0); ctx.close_path()
    ctx.set_source_rgba(0.8, 0.95, 1, 0.35); ctx.fill_preserve(); ctx.set_source_rgba(*hexc("#FFFFFF")); ctx.set_line_width(10); ctx.stroke()
    for k in range(-2, 3):
        ctx.move_to(k * 160, 0); ctx.line_to(k * 160, -470 + abs(k) * 40); ctx.set_source_rgba(1, 1, 1, 0.6); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()
    for k in range(4):
        pot(ctx, CX - 270 + k * 180, CY + 190, 130, 100, [MARE, HIGH, EARTHSOIL, MARE][k], gt, ph=90 + 20 * k, s=s)
    sun(ctx, CX + 380, CY - 520, 90 * pin(lt, 0.2), gt)
    label(ctx, "昼22℃・夜18℃", CX, CY + 380, 80, s=pin(lt, 0.3))


def v_three_pots(ctx, lt, d, gt):
    g = clamp((lt - 0.3) / 1.2)
    for i, (tag, h, tb) in enumerate([("堆肥0%", 40, 0), ("5%", 150, 1), ("30%", 300, 4)]):
        x = CX - 330 + i * 330
        pot(ctx, x, CY + 300, 250, 200, [MARE, "#5E5249", "#4A3A2C"][i], gt, ph=h * g, tubers=tb if g > 0.6 else 0, tag=tag, s=pin(lt, 0.1 * i))
    label(ctx, "ミミズのふんの量で…", CX, CY - 400, 84, s=pin(lt, 0.2))


def v_zero(ctx, lt, d, gt):
    pot(ctx, CX, CY + 260, 380, 300, MARE, gt, ph=55, s=pin(lt), tag="月の砂だけ")
    label(ctx, "ほとんど育たない…", CX, CY - 330, 90, s=pin(lt, 0.3))


def v_compare(ctx, lt, d, gt):
    g = clamp((lt - 0.2) / 1.0)
    pot(ctx, CX - 240, CY + 260, 300, 240, "#4A3A2C", gt, ph=320 * g, tubers=4 if g > 0.5 else 0, tag="月の砂+堆肥", s=pin(lt))
    pot(ctx, CX + 240, CY + 260, 300, 240, EARTHSOIL, gt, ph=320 * g, tubers=4 if g > 0.5 else 0, tag="地球の畑の土", s=pin(lt, 0.1))
    label(ctx, "=", CX, CY - 40, 160, s=pin(lt, 0.4))
    label(ctx, "同じくらい!", CX, CY - 430, 110, s=pin(lt, 0.6), rot=-0.04)


def v_ratio(ctx, lt, d, gt):
    w = 840; x0 = CX - w / 2
    p = ease_out_cubic(clamp(lt / 0.8))
    rrect(ctx, x0, CY - 90, w * 0.7 * p, 180, 30); fill_stroke(ctx, MARE, lw=8)
    if p > 0.95:
        rrect(ctx, x0 + w * 0.7, CY - 90, w * 0.3 * pin(lt, 0.8), 180, 30); fill_stroke(ctx, COMPOST, lw=8)
    label(ctx, "月の砂 7", x0 + w * 0.35, CY, 80, s=pin(lt, 0.2))
    label(ctx, "3", x0 + w * 0.85, CY, 90, s=pin(lt, 0.9))
    worm(ctx, x0 + w * 0.85, CY + 220, 0.45 * pin(lt, 1.0), gt)
    label(ctx, "7:3でまぜる!", CX, CY - 330, 100, s=pin(lt, 0.3))


def v_worm(ctx, lt, d, gt):
    ground(ctx, CY + 200, EARTHSOIL)
    worm(ctx, CX, CY + 30, 1.3 * pin(lt), gt)
    for k in range(5):
        circle(ctx, CX - 300 + k * 150, CY + 330 + 30 * (k % 2), 30 * pin(lt, 0.2 + 0.05 * k), COMPOST, lw=4)
    label(ctx, "ミミズのふん=堆肥", CX, CY - 380, 90, s=pin(lt, 0.2))


def v_worm_eat(ctx, lt, d, gt):
    ground(ctx, CY + 200, EARTHSOIL)
    for k in range(4):
        x = CX - 330 + k * 120
        ctx.save(); ctx.translate(x, CY + 160); ctx.rotate(0.5 * k); ctx.scale(1, 0.5)
        ctx.new_path(); ctx.arc(0, 0, 70 * pin(lt, 0.06 * k), 0, 6.28); ctx.restore()
        fill_stroke(ctx, ["#E8A33D", "#C2554B", "#8BBF4A", "#E07A4F"][k], lw=5)
    worm(ctx, CX + 200, CY + 60, 0.9 * pin(lt, 0.2), gt)
    label(ctx, "落ち葉や野菜くず", CX, CY - 330, 84, s=pin(lt, 0.2), font="mochiy")
    label(ctx, "↓ 食べて ふんに!", CX, CY + 420, 84, s=pin(lt, 0.5), font="mochiy")


def v_sponge(ctx, lt, d, gt):
    """Compost grabs the metals so roots take up less."""
    circle(ctx, CX, CY, 240 * pin(lt), COMPOST, lw=10)
    label(ctx, "堆肥", CX, CY, 100, s=pin(lt, 0.1))
    for k in range(6):
        a = k * 1.047 + gt * 0.6
        q = clamp((lt - 0.3 - 0.08 * k) / 0.5)
        r = 470 - 210 * ease_in_out(q)
        circle(ctx, CX + r * math.cos(a), CY + r * math.sin(a), 46, "#D9844A", lw=5)
        draw_sprite(ctx, text_sprite("Cu", 40, color="#1B1B3A", stroke="#FFFFFF", stroke_w=3, shadow=False, path=FONTS["dela"]), CX + r * math.cos(a), CY + r * math.sin(a), 1, 1)
    label(ctx, "金属をつかまえる!", CX, CY - 440, 90, s=pin(lt, 0.3))


def v_slow(ctx, lt, d, gt):
    base = CY + 260
    for i, (nm, days, col) in enumerate([("ほかの砂", 8, MARE), ("高地の砂", 24, HIGH)]):
        y = CY - 180 + i * 330
        label(ctx, nm, 210, y, 66, font="mochiy", s=pin(lt, 0.1 * i))
        w = 560 * days / 24 * ease_out_cubic(clamp((lt - 0.2 * i) / 0.9))
        rrect(ctx, 380, y - 50, max(10, w), 100, 30); fill_stroke(ctx, col, lw=7)
        label(ctx, f"{'4〜8' if i == 0 else '24'}日", 380 + w + 110 if w < 460 else 380 + w - 110, y, 66, s=pin(lt, 0.4 + 0.2 * i))
    label(ctx, "芽が出るまで", CX, CY - 420, 90, s=pin(lt, 0.1))


def v_three_of_five(ctx, lt, d, gt):
    for i in range(5):
        x = 150 + i * 195
        has = i < 3
        pot(ctx, x, CY + 200, 150, 130, HIGH, gt, ph=110, tubers=2 if has else 0, s=pin(lt, 0.08 * i))
        label(ctx, "○" if has else "×", x, CY - 150, 90, color="#FFE14D" if has else "#FF3D7F", s=pin(lt, 0.5 + 0.08 * i))
    label(ctx, "イモができたのは 5株中3株", CX, CY - 400, 74, s=pin(lt, 0.2))


def v_toxin(ctx, lt, d, gt):
    potato(ctx, CX, CY, 1.6 * pin(lt), gt, green=0.75, sprout=True, mood="wow")
    label(ctx, "芽や緑の皮に注意!", CX, CY - 400, 90, s=pin(lt, 0.2))
    label(ctx, "ソラニンなど", CX, CY + 330, 80, s=pin(lt, 0.35), font="mochiy")


def v_safe(ctx, lt, d, gt):
    potato(ctx, CX - 180, CY + 40, 1.1 * pin(lt), gt, col=REDSKIN)
    circle(ctx, CX + 250, CY - 40, 160 * pin(lt, 0.2), "#4CC85A", lw=10)
    ctx.move_to(CX + 175, CY - 40); ctx.line_to(CX + 235, CY + 30); ctx.line_to(CX + 340, CY - 110)
    ctx.set_source_rgba(1, 1, 1, 1); ctx.set_line_width(28); ctx.stroke()
    label(ctx, "毒は増えなかった", CX, CY - 390, 90, s=pin(lt, 0.3))
    label(ctx, "栄養も地球なみ", CX, CY + 320, 80, s=pin(lt, 0.45), font="mochiy")


def v_not_tasted(ctx, lt, d, gt):
    potato(ctx, CX, CY + 60, 1.3 * pin(lt), gt, col=REDSKIN, mood="wow")
    for i, (x, y, sz) in enumerate([(CX - 330, CY - 260, 170), (CX + 330, CY - 220, 210)]):
        draw_sprite(ctx, text_sprite("?", sz, color="#FFE14D", path=FONTS["dela"]), x, y, pin(lt, 0.1 + i * 0.15), 1, 0.3 * math.sin(gt * 4 + i))
    label(ctx, "味は…まだ ひみつ!", CX, CY - 430, 86, s=pin(lt, 0.3))


def v_small(ctx, lt, d, gt):
    potato(ctx, CX - 260, CY + 80, 0.35 * pin(lt), gt, col=REDSKIN)
    potato(ctx, CX + 170, CY + 40, 1.5 * pin(lt, 0.2), gt, col=REDSKIN)
    label(ctx, "10g未満", CX - 260, CY + 250, 70, s=pin(lt, 0.3))
    label(ctx, "お店サイズ", CX + 170, CY + 300, 70, s=pin(lt, 0.4))
    label(ctx, "小さな鉢では…", CX, CY - 380, 90, s=pin(lt, 0.1))


def v_banana(ctx, lt, d, gt):
    potato(ctx, CX - 230, CY, 1.0 * pin(lt), gt)
    s = pin(lt, 0.2)
    ctx.save(); ctx.translate(CX + 250, CY); ctx.scale(s, s); ctx.rotate(-0.4)
    ctx.new_path(); ctx.arc(0, -120, 200, 0.6, 2.5); ctx.arc_negative(0, -150, 150, 2.4, 0.7); ctx.close_path()
    fill_stroke(ctx, "#FFD84D", lw=8); ctx.restore()
    label(ctx, ">", CX + 20, CY, 140, s=pin(lt, 0.4))
    label(ctx, "カリウム", CX, CY - 340, 100, s=pin(lt, 0.3))


def v_field(ctx, lt, d, gt):
    ground(ctx, CY + 100, "#8BBF4A")
    for r in range(3):
        for c in range(5):
            plant(ctx, 160 + c * 190, CY + 160 + r * 110, 90 * pin(lt, 0.04 * (r * 5 + c)), gt)
    label(ctx, "せまい畑でも", CX, CY - 340, 90, s=pin(lt, 0.2))
    label(ctx, "カロリーたっぷり!", CX, CY - 220, 90, s=pin(lt, 0.35))


def v_mars(ctx, lt, d, gt):
    space_bg(ctx, gt)
    planet(ctx, CX, CY + 80, 300 * pin(lt), "#D9603B")
    potato(ctx, CX + 240, CY - 250, 0.8 * pin(lt, 0.2), gt)
    label(ctx, "火星でジャガイモ", CX, CY - 470, 90, s=pin(lt, 0.3))


def v_food_ship(ctx, lt, d, gt):
    space_bg(ctx, gt)
    p = ease_in_out(clamp(lt / max(d * 0.9, 1)))
    planet(ctx, 160, CY + 360, 140, "#3FA9F5")
    moon(ctx, 930, CY - 320, 120 * pin(lt), gt)
    x, y = 200 + 620 * p, CY + 250 - 520 * p
    rocket(ctx, x, y, 0.8)
    for k in range(3):
        rrect(ctx, x - 160 - k * 70, y + 60 + k * 40, 60, 50, 8); fill_stroke(ctx, "#E8A33D", lw=4)
    label(ctx, "ずっと運ぶのは大変!", CX, CY - 520, 84, s=pin(lt, 0.2))


def v_artemis(ctx, lt, d, gt):
    space_bg(ctx, gt)
    moon(ctx, CX + 200, CY - 280, 240 * pin(lt), gt)
    p = ease_in_out(clamp(lt / max(d, 1)))
    rocket(ctx, CX - 260 + 220 * p, CY + 380 - 380 * p, 1.0)
    label(ctx, "アルテミス計画", CX, CY + 450, 100, s=pin(lt, 0.2))


def v_base(ctx, lt, d, gt):
    space_bg(ctx, gt)
    ground(ctx, CY + 220, MOON)
    planet(ctx, 880, CY - 380, 90, "#3FA9F5")
    s = pin(lt)
    ctx.save(); ctx.translate(CX - 60, CY + 220); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 300, math.pi, 0); ctx.close_path()
    ctx.set_source_rgba(0.8, 0.95, 1, 0.4); ctx.fill_preserve(); ctx.set_source_rgba(1, 1, 1, 1); ctx.set_line_width(10); ctx.stroke()
    ctx.restore()
    for k in range(4):
        plant(ctx, CX - 240 + k * 120, CY + 220, 130 * pin(lt, 0.2 + 0.08 * k), gt)
    label(ctx, "月の畑!?", CX, CY - 380, 110, s=pin(lt, 0.3))


def v_shuttle1995(ctx, lt, d, gt):
    space_bg(ctx, gt)
    planet(ctx, CX, CY + 560, 420, "#3FA9F5")
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY - 60); ctx.scale(s, s); ctx.rotate(-0.15)
    ctx.move_to(-260, 40); ctx.line_to(180, 40); ctx.curve_to(300, 40, 300, -40, 180, -40); ctx.line_to(-260, -40); ctx.close_path()
    fill_stroke(ctx, "#FFFFFF", lw=8)
    ctx.move_to(-200, 40); ctx.line_to(-60, 40); ctx.line_to(-200, 170); ctx.close_path(); fill_stroke(ctx, "#E8E8F0", lw=7)
    ctx.restore()
    potato(ctx, CX + 300, CY - 330, 0.55 * pin(lt, 0.3), gt)
    label(ctx, "1995年", CX, CY - 520, 110, s=pin(lt, 0.15))


def v_crops(ctx, lt, d, gt):
    items = [("トマト", "#E84B3C"), ("レタス", "#8BBF4A"), ("アルファルファ", "#B5D86B"), ("ひよこ豆", "#E8C27A")]
    for i, (nm, col) in enumerate(items):
        x = CX - 230 + (i % 2) * 460; y = CY - 120 + (i // 2) * 360
        circle(ctx, x, y, 120 * pin(lt, 0.1 * i), col, lw=8)
        label(ctx, nm, x, y + 170, 60, font="mochiy", s=pin(lt, 0.1 * i + 0.1))
    label(ctx, "次はどれ?", CX, CY - 420, 100, s=pin(lt, 0.4))


def v_city(ctx, lt, d, gt):
    ground(ctx, CY + 300, "#C9B48A")
    for k in range(5):
        h = [380, 520, 300, 460, 340][k] * pin(lt, 0.06 * k)
        rrect(ctx, 90 + k * 190, CY + 300 - h, 150, h, 10); fill_stroke(ctx, ["#7FD3FF", "#A9B4C2", "#FF8FB1", "#B5D86B", "#FFE14D"][k], lw=6)
        plant(ctx, 165 + k * 190, CY + 300 - h, 70 * pin(lt, 0.4 + 0.06 * k), gt)
    label(ctx, "都会や砂ばくでも", CX, CY - 420, 90, s=pin(lt, 0.2))


def v_clean(ctx, lt, d, gt):
    ground(ctx, CY + 200, "#8A7B6B")
    worm(ctx, CX - 150, CY + 330, 0.6 * pin(lt), gt)
    plant(ctx, CX + 200, CY + 200, 260 * pin(lt, 0.2), gt)
    sparkles(ctx, CX, CY + 100, lt, 0.2, "#FFE14D", 12, 360)
    label(ctx, "よごれた土を きれいに", CX, CY - 360, 84, s=pin(lt, 0.3))


def v_scale1g(ctx, lt, d, gt):
    s = pin(lt)
    rrect(ctx, CX - 300, CY + 120, 600, 120, 30); fill_stroke(ctx, "#E8E8F0", lw=8)
    rrect(ctx, CX - 180, CY + 145, 360, 70, 14); fill_stroke(ctx, "#1B1B3A", lw=0)
    draw_sprite(ctx, text_sprite("1.0 g", 60, color="#4FF0FF", stroke="#1B1B3A", path=FONTS["dela"]), CX, CY + 180, s, 1)
    ctx.new_path(); ctx.arc(CX, CY + 110, 60 * s, math.pi, 0); ctx.set_source_rgba(*hexc(MOON)); ctx.fill()
    plant(ctx, CX, CY + 60, 140 * pin(lt, 0.3), gt, leaves=6)
    label(ctx, "本物の月の砂", CX, CY - 300, 96, s=pin(lt, 0.2))


def v_calendar(month, day, sub=None):
    def vis(ctx, lt, d, gt):
        rrect(ctx, CX - 260, CY - 260, 520, 520, 40); fill_stroke(ctx, "#FFFFFF", lw=10)
        rrect(ctx, CX - 260, CY - 260, 520, 140, 40); fill_stroke(ctx, "#FF3D7F", lw=10)
        label(ctx, month, CX, CY - 190, 80, s=pin(lt))
        draw_sprite(ctx, text_sprite(day, 200, color="#1B1B3A", stroke="#FFFFFF", path=FONTS["dela"]), CX, CY + 60, pin(lt, 0.15), 1)
        if sub:
            label(ctx, sub, CX, CY + 400, 76, s=pin(lt, 0.3), font="mochiy")
    return vis


def v_team(ctx, lt, d, gt):
    for k, (col, name) in enumerate([("#E07A4F", "オレゴン州立大"), ("#3D5BFF", "NASA")]):
        x = CX - 230 + k * 460
        circle(ctx, x, CY, 190 * pin(lt, k * 0.12), col, lw=10)
        label(ctx, name, x, CY, 64 if k == 0 else 96, color="#FFFFFF", hi="#FFE14D", s=pin(lt, 0.1 + k * 0.12), font="mochiy" if k == 0 else "dela")
    label(ctx, "研究チーム", CX, CY - 340, 100, s=pin(lt, 0.3))


def v_menu(ctx, lt, d, gt):
    items = ["フライドポテト", "ポテトサラダ", "じゃがバター", "肉じゃが"]
    for i, t in enumerate(items):
        x = CX - 230 + (i % 2) * 460; y = CY - 120 + (i // 2) * 300
        rrect(ctx, x - 210, y - 110, 420, 220, 34); fill_stroke(ctx, ["#FFE14D", "#7FD3FF", "#FF8FB1", "#B5D86B"][i], lw=7)
        label(ctx, t, x, y, 54, color="#1B1B3A", hi="#FFFFFF", s=pin(lt, 0.08 * i), font="mochiy")
    label(ctx, "月で食べるなら?", CX, CY - 400, 96, s=pin(lt, 0.3))


def v_dish(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 120); ctx.scale(s, s)
    ctx.save(); ctx.scale(1, 0.35); ctx.new_path(); ctx.arc(0, 0, 360, 0, 6.28); ctx.restore(); fill_stroke(ctx, "#FFFFFF", lw=8)
    ctx.restore()
    for k in range(3):
        potato(ctx, CX - 160 + k * 160, CY + 60 - 20 * (k % 2), 0.55 * pin(lt, 0.1 * k + 0.1), gt, col=REDSKIN, face=k == 1)
    label(ctx, "月面レストラン", CX, CY - 380, 96, s=pin(lt, 0.3))


def v_darwin(ctx, lt, d, gt):
    rrect(ctx, CX - 230, CY - 300, 460, 600, 30); fill_stroke(ctx, "#8A5A35", lw=10)
    rrect(ctx, CX - 190, CY - 260, 380, 520, 20); fill_stroke(ctx, "#F2E6C9", lw=0)
    worm(ctx, CX, CY + 60, 0.7 * pin(lt, 0.2), gt)
    label(ctx, "1881", CX, CY - 150, 90, color="#1B1B3A", hi="#FF3D7F", s=pin(lt, 0.1))
    label(ctx, "ダーウィンの本", CX, CY - 420, 96, s=pin(lt, 0.2))


def v_life_cycle(ctx, lt, d, gt):
    steps = [("植える", 0), ("芽", 60), ("花", 200), ("イモ", 0)]
    for i, (nm, h) in enumerate(steps):
        x = 170 + i * 250
        s = pin(lt, 0.15 * i)
        pot(ctx, x, CY + 170, 160, 140, "#4A3A2C", gt, ph=h, tubers=3 if i == 3 else (1 if i == 0 else 0), s=s)
        if i == 2:
            circle(ctx, x, CY + 170 - 170 - 200, 22 * s, "#FFFFFF", lw=4)
        label(ctx, nm, x, CY + 280, 64, s=s, font="mochiy")
        if i < 3:
            label(ctx, "→", x + 125, CY + 60, 60, s=s)
    label(ctx, "一生をぜんぶ!", CX, CY - 380, 100, s=pin(lt, 0.6))


# ---------------------------------------------------------------- real photos (NASA, public domain; credit under the photo)
NASA = "NASA"
P_boot = photo_scene("bootprint", "NASA(アポロ11号)", "本物の月の砂!", box=(820, 820))
P_schmitt = photo_scene("schmitt", "NASA(アポロ17号)", "月の砂を集める宇宙飛行士", box=(820, 820))
P_bed = photo_scene("simulant_bed", "NASA/JPL-Caltech", "ニセの月の砂で実験中", box=(620, 900))
P_earthset = photo_scene("earthset", "NASA(アルテミス2)", "月の向こうに地球!", box=(980, 653))
P_window = photo_scene("window_moon", "NASA(アルテミス2)", "窓から見た月", box=(980, 653))
P_romaine = photo_scene("romaine", "NASA", "宇宙ステーションのレタス", box=(980, 653))
P_veggie = photo_scene("veggie_pink", "NASA", "宇宙の野菜工場ベジー", box=(660, 880))
P_veg03 = photo_scene("veg03d", "NASA", "宇宙で育つ野菜", box=(980, 652))
