"""Visuals for the Enceladus ice-grain episode (Postberg, Sekine et al., Science Advances 2026, doi:10.1126/sciadv.aee7256;
ELSI/Institute of Science Tokyo release 2026-09-28; sorae 2026-11-24). Vertical stage, CX=540, CY=760."""
import math, random
import cairo
from common4 import *
from space2 import pin, CX, CY
from space import planet, telescope
from space3 import probe
from hera_vis import label, photo_scene, PHOTO_LAYOUT, v_question, v_longvideo, space_bg
from casa_vis import v_hello

OPTS = {"short": False}
INK = "#1B1B3A"
SALT = {"しお": "#FFFFFF", "炭酸": "#FFB84D", "リン": "#B07CFF", "カリウム": "#5BE08A"}
SALT_C = list(SALT.values())


def lbl(ctx, t, x, y, size=80, s=1.0, rot=0.0, font="dela", color="#FFFFFF"):
    if OPTS["short"] and font == "mochiy" and size < 56:
        return
    label(ctx, t, x, y, size, color=color, s=s, rot=rot, font=font)


def P(name, credit, title=None, box=(940, 700), **kw):
    return photo_scene(name, credit, title, box=box, **kw)


def bigtext(text, sub=None, color="#FFE14D", size=220):
    def vis(ctx, lt, d, gt):
        space_bg(ctx, gt)
        draw_sprite(ctx, text_sprite(text, size, color=color, hi="#FF3D7F", path=FONTS["dela"]), CX, CY - 60, pin(lt), 1, -0.04)
        if sub:
            draw_sprite(ctx, text_sprite(sub, 74, color="#FFFFFF", hi="#FFE14D", path=FONTS["mochiy"]), CX, CY + 160, pin(lt, 0.2), 1)
    return vis


# ---------------------------------------------------------------- props
def moon(ctx, x, y, r, gt, jets=True, glow=True, face=False):
    if r < 2:
        return
    if glow:
        g = cairo.RadialGradient(x, y, r * 0.8, x, y, r * 1.5)
        g.add_color_stop_rgba(0, 0.8, 0.95, 1, 0.35); g.add_color_stop_rgba(1, 0.8, 0.95, 1, 0)
        ctx.set_source(g); ctx.arc(x, y, r * 1.5, 0, 2 * math.pi); ctx.fill()
    circle(ctx, x, y, r, "#F4F9FF", lw=max(3, r * 0.03))
    ctx.save(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.clip()
    rnd = random.Random(5)
    for k in range(9):
        cx0, cy0 = x + rnd.uniform(-0.8, 0.8) * r, y + rnd.uniform(-0.8, 0.8) * r
        ctx.move_to(cx0, cy0)
        ctx.curve_to(cx0 + r * 0.3, cy0 + rnd.uniform(-0.2, 0.2) * r, cx0 + r * 0.4, cy0 + rnd.uniform(-0.3, 0.3) * r, cx0 + r * 0.7, cy0 + rnd.uniform(-0.2, 0.2) * r)
        ctx.set_source_rgba(0.62, 0.72, 0.85, 0.7); ctx.set_line_width(max(1.5, r * 0.02)); ctx.stroke()
    for k in range(4):  # tiger stripes near south pole
        yy = y + r * (0.62 + 0.07 * k)
        ctx.move_to(x - r * 0.45, yy); ctx.curve_to(x - r * 0.15, yy - r * 0.06, x + r * 0.15, yy + r * 0.06, x + r * 0.45, yy - r * 0.02)
        ctx.set_source_rgba(*hexc("#3FA9F5")[:3], 0.9); ctx.set_line_width(max(2, r * 0.035)); ctx.stroke()
    ctx.restore()
    if face:
        for sx in (-1, 1):
            circle(ctx, x + sx * r * 0.28, y - r * 0.08, r * 0.08, INK, lw=0)
        ctx.new_path(); ctx.arc(x, y + r * 0.12, r * 0.18, 0.2, math.pi - 0.2)
        ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(max(3, r * 0.03)); ctx.stroke()
    if jets:
        plume(ctx, x, y + r * 0.95, r, gt)


def plume(ctx, x, y, r, gt, down=True, n=5, colored=False):
    rnd = random.Random(11)
    for j in range(n):
        ang = math.pi / 2 + (j - (n - 1) / 2) * 0.22
        for k in range(16):
            ph = ((gt * 0.6 + k / 16 + j * 0.13) % 1.0)
            dist = r * (0.05 + 0.9 * ph)
            px = x + dist * math.cos(ang) + rnd.uniform(-8, 8)
            py = y + dist * math.sin(ang) * (1 if down else -1)
            a = 0.85 * (1 - ph)
            col = hexc(SALT_C[(j + k) % 4])[:3] if colored else (0.85, 0.95, 1.0)
            ctx.new_path(); ctx.arc(px, py, max(2, r * 0.025 * (1 + ph)), 0, 2 * math.pi)
            ctx.set_source_rgba(*col, a); ctx.fill()


def saturn(ctx, x, y, r, gt, ering=False):
    if r < 2:
        return
    if ering:
        ctx.save(); ctx.translate(x, y); ctx.scale(1, 0.28)
        g = cairo.RadialGradient(0, 0, r * 1.9, 0, 0, r * 3.2)
        g.add_color_stop_rgba(0, 0.7, 0.85, 1, 0.0); g.add_color_stop_rgba(0.45, 0.7, 0.85, 1, 0.35); g.add_color_stop_rgba(1, 0.7, 0.85, 1, 0)
        ctx.set_source(g); ctx.arc(0, 0, r * 3.2, 0, 2 * math.pi); ctx.fill(); ctx.restore()
    planet(ctx, x, y, r, "#E8C77E", ring="#C9A96B", t=gt)


def grain(ctx, x, y, r, col, s=1.0, ring=True):
    if s * r < 1:
        return
    circle(ctx, x, y, r * s, "#DDF3FF", lw=4 if ring else 0)
    circle(ctx, x, y, r * s * 0.55, col, lw=3)


def drop(ctx, x, y, r, mode="mix", t=1.0):
    """A frozen droplet: 'mix' = uniform, 'sep' = salts in separate patches."""
    circle(ctx, x, y, r, "#BFE8FF", lw=6)
    ctx.save(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.clip()
    if mode == "mix":
        rnd = random.Random(3)
        for k in range(60):
            ctx.new_path(); ctx.arc(x + rnd.uniform(-r, r), y + rnd.uniform(-r, r), r * 0.06, 0, 2 * math.pi)
            ctx.set_source_rgba(*hexc(SALT_C[k % 4])[:3], 0.9); ctx.fill()
    else:
        for k in range(4):
            a = k * math.pi / 2 + 0.6
            ctx.new_path(); ctx.arc(x + r * 0.5 * math.cos(a), y + r * 0.5 * math.sin(a), r * 0.38 * t, 0, 2 * math.pi)
            ctx.set_source_rgba(*hexc(SALT_C[k])[:3], 0.95); ctx.fill()
    ctx.restore()


def crust(ctx, gt, top=CY - 120, bot=CY + 260, crack=True):
    """Cross-section: space above, ice shell, ocean below, with a crack."""
    ctx.rectangle(0, top, 1080, bot - top); ctx.set_source_rgba(*hexc("#DDEFFF")); ctx.fill()
    ctx.rectangle(0, bot, 1080, 1920 - bot); ctx.set_source_rgba(*hexc("#1E6FD9")); ctx.fill()
    for k in range(6):
        yy = bot + 40 + k * 60
        ctx.move_to(0, yy)
        for x in range(0, 1081, 40):
            ctx.line_to(x, yy + 10 * math.sin(x / 60 + gt * 2 + k))
        ctx.set_source_rgba(1, 1, 1, 0.15); ctx.set_line_width(4); ctx.stroke()
    if crack:
        ctx.move_to(CX - 70, bot); ctx.line_to(CX - 30, (top + bot) / 2); ctx.line_to(CX - 18, top)
        ctx.line_to(CX + 18, top); ctx.line_to(CX + 30, (top + bot) / 2); ctx.line_to(CX + 70, bot); ctx.close_path()
        ctx.set_source_rgba(*hexc("#0B1530")); ctx.fill()


def bar_meter(ctx, x, y, w, frac, col):
    rrect(ctx, x, y, w, 50, 25); fill_stroke(ctx, "#FFFFFF", lw=5)
    if frac > 0.01:
        rrect(ctx, x + 6, y + 6, (w - 12) * frac, 38, 19); fill_stroke(ctx, col, lw=0)


# ---------------------------------------------------------------- scenes
def v_hook(ctx, lt, d, gt):
    space_bg(ctx, gt)
    moon(ctx, CX, CY - 200, 230 * pin(lt), gt, jets=False)
    s = pin(lt, 0.2)
    if s > 0.05:
        plume(ctx, CX, CY + 20, 330, gt, n=5, colored=True)
    names = list(SALT.keys())
    for k in range(4):
        x = CX - 360 + k * 240
        grain(ctx, x, CY + 470, 70, SALT_C[k], s=pin(lt, 0.4 + 0.12 * k))
        lbl(ctx, names[k], x, CY + 580, 48, s=pin(lt, 0.5 + 0.12 * k), font="mochiy")
    lbl(ctx, "1つぶずつ ちがう!?", CX, CY - 520, 96, s=pin(lt, 0.3), color="#FFE14D", rot=-0.04)


def v_moon(ctx, lt, d, gt):
    space_bg(ctx, gt)
    moon(ctx, CX, CY, 330 * pin(lt), gt, jets=True)
    lbl(ctx, "エンケラドス", CX, CY - 470, 110, s=pin(lt, 0.2))


def v_saturn_moon(ctx, lt, d, gt):
    space_bg(ctx, gt)
    saturn(ctx, CX - 120, CY, 220 * pin(lt), gt, ering=True)
    a = gt * 0.5
    mx, my = CX - 120 + 430 * math.cos(a), CY + 120 * math.sin(a)
    moon(ctx, mx, my, 42 * pin(lt, 0.3), gt, jets=False)
    lbl(ctx, "土星", CX - 120, CY - 330, 90, s=pin(lt, 0.2))
    lbl(ctx, "エンケラドス", mx, my - 90, 50, s=pin(lt, 0.4), font="mochiy", color="#FFE14D")


def v_moons270(ctx, lt, d, gt):
    space_bg(ctx, gt)
    saturn(ctx, CX, CY + 40, 170 * pin(lt), gt)
    rnd = random.Random(7)
    n = int(140 * clamp(lt / 1.5))
    for k in range(n):
        a = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(260, 470)
        circle(ctx, CX + rr * math.cos(a + gt * 0.1), CY + 40 + rr * 0.6 * math.sin(a + gt * 0.1), rnd.uniform(4, 10), "#DDE6F5", lw=0)
    lbl(ctx, "月は 270こ以上!", CX, CY - 460, 104, s=pin(lt, 0.3), color="#FFE14D")


def v_size(ctx, lt, d, gt):
    space_bg(ctx, gt)
    moon(ctx, CX, CY - 90, 250 * pin(lt), gt, jets=False)
    p = clamp((lt - 0.4) / 0.8)
    x0, x1 = CX - 250, CX - 250 + 500 * p
    ctx.move_to(x0, CY + 260); ctx.line_to(x1, CY + 260)
    ctx.set_source_rgba(*hexc("#FFE14D")); ctx.set_line_width(14); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    lbl(ctx, "直径 約500km", CX, CY + 360, 90, s=pin(lt, 0.6), color="#FFE14D")
    lbl(ctx, "東京〜新大阪(約515km)くらい", CX, CY + 480, 56, s=pin(lt, 0.9), font="mochiy")


def v_train(ctx, lt, d, gt):
    space_bg(ctx, gt)
    p = clamp(lt / max(d * 0.8, 0.5))
    ctx.move_to(CX - 400, CY + 120); ctx.line_to(CX + 400, CY + 120)
    ctx.set_source_rgba(1, 1, 1, 0.7); ctx.set_line_width(10); ctx.stroke()
    for sx, nm in ((-1, "東京"), (1, "新大阪")):
        circle(ctx, CX + sx * 400, CY + 120, 26, "#FF3D7F", lw=5)
        lbl(ctx, nm, CX + sx * 400, CY + 210, 60, s=pin(lt, 0.2), font="mochiy")
    x = CX - 400 + 800 * p
    ctx.save(); ctx.translate(x, CY + 60)
    rrect(ctx, -140, -40, 260, 80, 30); fill_stroke(ctx, "#FFFFFF", lw=6)
    ctx.move_to(120, -40); ctx.curve_to(200, -40, 200, 40, 120, 40); fill_stroke(ctx, "#FFFFFF", lw=6)
    ctx.rectangle(-140, 5, 300, 12); ctx.set_source_rgba(*hexc("#2E4BB8")); ctx.fill()
    ctx.restore()
    moon(ctx, CX, CY - 300, 150 * pin(lt, 0.3), gt, jets=False)
    lbl(ctx, "はしからはしまで これくらい", CX, CY + 380, 60, s=pin(lt, 0.4), font="mochiy")


def v_herschel(ctx, lt, d, gt):
    space_bg(ctx, gt)
    telescope(ctx, CX - 80, CY + 300, gt, 1.3 * pin(lt))
    moon(ctx, CX + 280, CY - 250, 60 * pin(lt, 0.4), gt, jets=False)
    lbl(ctx, "1789年 発見", CX, CY - 470, 110, s=pin(lt, 0.2), color="#FFE14D")
    lbl(ctx, "ウィリアム・ハーシェル", CX, CY + 480, 64, s=pin(lt, 0.5), font="mochiy")


def v_white(ctx, lt, d, gt):
    space_bg(ctx, gt)
    for k in range(10):
        a = k * math.pi / 5 + gt * 0.3
        ctx.move_to(CX + 290 * math.cos(a), CY + 290 * math.sin(a)); ctx.line_to(CX + 460 * math.cos(a), CY + 460 * math.sin(a))
        ctx.set_source_rgba(1, 1, 0.8, 0.6 * pin(lt, 0.3)); ctx.set_line_width(14); ctx.stroke()
    moon(ctx, CX, CY, 260 * pin(lt), gt, jets=False, face=True)
    lbl(ctx, "ピカピカの白!", CX, CY - 500, 110, s=pin(lt, 0.2), color="#FFE14D")


def v_cold(ctx, lt, d, gt):
    space_bg(ctx, gt)
    s = pin(lt)
    ctx.save(); ctx.translate(CX - 200, CY + 60); ctx.scale(s, s)
    rrect(ctx, -50, -330, 100, 520, 50); fill_stroke(ctx, "#FFFFFF", lw=8)
    circle(ctx, 0, 230, 90, "#3FA9F5", lw=8)
    rrect(ctx, -22, 20, 44, 200, 22); fill_stroke(ctx, "#3FA9F5", lw=0)
    ctx.restore()
    lbl(ctx, "マイナス", CX + 180, CY - 120, 80, s=pin(lt, 0.2))
    lbl(ctx, "約200℃", CX + 180, CY + 20, 120, s=pin(lt, 0.3), color="#8FD3FF")
    lbl(ctx, "カチコチ!", CX + 180, CY + 200, 80, s=pin(lt, 0.5), color="#FFE14D")


def v_inside(ctx, lt, d, gt):
    space_bg(ctx, gt)
    s = pin(lt)
    r = 330 * s
    if r > 2:
        circle(ctx, CX, CY, r, "#F4F9FF", lw=6)
        circle(ctx, CX, CY, r * 0.86, "#1E6FD9", lw=4)
        circle(ctx, CX, CY, r * 0.62, "#6B5B4B", lw=4)
    lbl(ctx, "氷", CX, CY - r * 0.93, 50, s=pin(lt, 0.3), font="mochiy", color="#1B1B3A")
    lbl(ctx, "海!", CX, CY - r * 0.74, 64, s=pin(lt, 0.4), color="#FFE14D")
    lbl(ctx, "岩", CX, CY, 64, s=pin(lt, 0.5))
    lbl(ctx, "氷の下に 海がある", CX, CY - 480, 90, s=pin(lt, 0.2))


def v_cassini(ctx, lt, d, gt):
    space_bg(ctx, gt)
    saturn(ctx, CX + 200, CY - 220, 200 * pin(lt), gt)
    p = clamp(lt / max(d, 1))
    probe(ctx, CX - 250 + 120 * p, CY + 250 - 80 * p, 1.6 * pin(lt, 0.2), gt)
    lbl(ctx, "カッシーニ", CX - 200, CY + 470, 100, s=pin(lt, 0.3), color="#FFE14D")


def v_years(ctx, lt, d, gt):
    space_bg(ctx, gt)
    rows = [("1997年", "打ち上げ"), ("2004年", "土星に到着"), ("2005年", "しぶきを発見!"), ("2017年", "ミッション終了")]
    for i, (a, b) in enumerate(rows):
        y = CY - 330 + i * 210
        s = pin(lt, 0.15 * i)
        lbl(ctx, a, CX - 230, y, 84, s=s, color="#FFE14D")
        lbl(ctx, b, CX + 190, y, 64, s=s, font="mochiy")
    lbl(ctx, "カッシーニの13年", CX, CY - 540, 90, s=pin(lt))


def v_stripes(ctx, lt, d, gt):
    space_bg(ctx, gt)
    moon(ctx, CX, CY - 60, 300 * pin(lt), gt, jets=False)
    ctx.new_path(); ctx.arc(CX, CY - 60 + 300 * 0.72, 170 + 12 * math.sin(gt * 5), 0, 2 * math.pi)
    ctx.set_source_rgba(*hexc("#FF3D7F")); ctx.set_line_width(10); ctx.stroke()
    lbl(ctx, "トラのしま!", CX, CY - 460, 110, s=pin(lt, 0.3), color="#FFB84D", rot=-0.05)
    lbl(ctx, "南極の4本のわれめ", CX, CY + 440, 64, s=pin(lt, 0.4), font="mochiy")


def v_tiger(ctx, lt, d, gt):
    space_bg(ctx, gt)
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY); ctx.scale(s, s)
    circle(ctx, 0, 0, 220, "#FFB84D", lw=8)
    for sx in (-1, 1):
        circle(ctx, sx * 160, -170, 60, "#FFB84D", lw=8)
        circle(ctx, sx * 75, -40, 26, INK, lw=0)
    for k in range(3):
        ctx.move_to(-60 + k * 60, -220); ctx.line_to(-50 + k * 60, -140)
        ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(16); ctx.stroke()
    circle(ctx, 0, 50, 34, "#FF6FA8", lw=5)
    ctx.restore()
    lbl(ctx, "タイガー・ストライプ", CX, CY - 460, 90, s=pin(lt, 0.2), color="#FFE14D")


def v_jets(ctx, lt, d, gt):
    space_bg(ctx, gt)
    crust(ctx, gt)
    for k in range(26):
        ph = ((gt * 0.5 + k / 26) % 1.0)
        y = CY + 260 - ph * 900
        x = CX + 14 * math.sin(k * 3.1) * (1 + (1 - ph) * 2) + (0 if y > CY - 120 else (k % 7 - 3) * 25 * (CY - 120 - y) / 400)
        circle(ctx, x, y, 9 if y > CY - 120 else 7, "#FFFFFF", lw=2)
    lbl(ctx, "宇宙", CX - 330, CY - 300, 70, s=pin(lt), font="mochiy")
    lbl(ctx, "氷", CX - 330, CY + 70, 70, s=pin(lt, 0.1), font="mochiy", color="#1B1B3A")
    lbl(ctx, "海", CX - 330, CY + 420, 80, s=pin(lt, 0.2))
    lbl(ctx, "海の水が ふき出す!", CX, CY - 540, 92, s=pin(lt, 0.3), color="#FFE14D")


def v_ering(ctx, lt, d, gt):
    space_bg(ctx, gt)
    saturn(ctx, CX, CY, 150 * pin(lt), gt, ering=True)
    a = gt * 0.5
    moon(ctx, CX + 420 * math.cos(a), CY + 118 * math.sin(a), 22 * pin(lt, 0.3), gt, jets=False)
    lbl(ctx, "E環", CX + 360, CY - 200, 90, s=pin(lt, 0.4), color="#8FD3FF")
    lbl(ctx, "しぶきで できた わ!", CX, CY - 460, 90, s=pin(lt, 0.2), color="#FFE14D")


def v_flythrough(ctx, lt, d, gt):
    space_bg(ctx, gt)
    moon(ctx, CX - 80, CY - 420, 260 * pin(lt), gt, jets=False)
    plume(ctx, CX - 80, CY - 170, 700, gt, n=7)
    p = clamp(lt / max(d * 0.9, 0.5))
    probe(ctx, CX + 420 - 900 * p, CY + 200, 1.1, gt)
    lbl(ctx, "しぶきの中を 通りぬけ!", CX, CY + 480, 80, s=pin(lt, 0.3), color="#FFE14D")


def v_snow(ctx, lt, d, gt):
    space_bg(ctx, gt)
    ctx.rectangle(0, CY + 260, 1080, 800); ctx.set_source_rgba(*hexc("#F4F9FF")); ctx.fill()
    rnd = random.Random(2)
    for k in range(70):
        x = rnd.uniform(0, 1080); y = (rnd.uniform(0, 1) * 1100 + gt * 90) % 1100 + CY - 820
        circle(ctx, x, y, rnd.uniform(5, 11), "#FFFFFF", lw=0)
    piko(ctx, CX, CY + 160, gt, 0.9 * pin(lt), "wow")
    lbl(ctx, "宇宙で 雪が ふる!?", CX, CY - 460, 100, s=pin(lt, 0.2), color="#FFE14D")


def v_cda(ctx, lt, d, gt):
    space_bg(ctx, gt)
    s = pin(lt)
    ctx.save(); ctx.translate(CX - 160, CY); ctx.scale(s, s)
    rrect(ctx, -170, -150, 340, 300, 30); fill_stroke(ctx, "#F2C14E", lw=8)
    circle(ctx, 0, 0, 110, "#2A2050", lw=8)
    ctx.restore()
    for k in range(6):
        ph = (gt * 0.7 + k / 6) % 1
        grain(ctx, CX + 450 - ph * 500, CY - 40 + 30 * math.sin(k * 2), 22, SALT_C[k % 4], ring=False)
    lbl(ctx, "ちりの分析器 CDA", CX, CY - 400, 90, s=pin(lt, 0.2), color="#FFE14D")
    lbl(ctx, "つぶ1つずつ 中身をしらべる", CX, CY + 320, 64, s=pin(lt, 0.4), font="mochiy")


def v_961(ctx, lt, d, gt):
    space_bg(ctx, gt)
    rnd = random.Random(9)
    n = int(160 * clamp(lt / 1.2))
    for k in range(n):
        x, y = rnd.uniform(80, 1000), rnd.uniform(CY - 330, CY + 450)
        circle(ctx, x, y, 12, SALT_C[k % 4], lw=2)
    rrect(ctx, CX - 330, CY - 120, 660, 240, 40); fill_stroke(ctx, "#1B1B3A", stroke="#FFE14D", lw=8)
    lbl(ctx, "961つぶ", CX, CY, 150, s=pin(lt, 0.4), color="#FFE14D")
    lbl(ctx, "塩の多い 氷のつぶ", CX, CY - 470, 84, s=pin(lt, 0.2))


def v_salts(ctx, lt, d, gt):
    space_bg(ctx, gt)
    names = ["食塩(塩化ナトリウム)", "炭酸ナトリウム", "リン酸塩", "塩化カリウム"]
    for k in range(4):
        y = CY - 280 + k * 210
        grain(ctx, CX - 330, y, 80, SALT_C[k], s=pin(lt, 0.15 * k))
        lbl(ctx, names[k], CX + 110, y, 58, s=pin(lt, 0.15 * k + 0.1), font="mochiy")
    lbl(ctx, "つぶごとに 塩がちがう!", CX, CY - 470, 88, s=pin(lt), color="#FFE14D")


def v_apart(ctx, lt, d, gt):
    space_bg(ctx, gt)
    sep = 120 + 120 * clamp(lt / 1.0)
    grain(ctx, CX - sep, CY, 150, SALT_C[0], s=pin(lt))
    grain(ctx, CX + sep, CY, 150, SALT_C[1], s=pin(lt, 0.1))
    lbl(ctx, "食塩", CX - sep, CY + 230, 64, s=pin(lt, 0.2), font="mochiy")
    lbl(ctx, "炭酸", CX + sep, CY + 230, 64, s=pin(lt, 0.2), font="mochiy")
    lbl(ctx, "いっしょに いない!", CX, CY - 400, 100, s=pin(lt, 0.4), color="#FF6FA8")


def v_same_ocean(ctx, lt, d, gt):
    space_bg(ctx, gt)
    crust(ctx, gt, top=CY + 100, bot=CY + 260, crack=False)
    drop(ctx, CX, CY + 450, 120, "mix")
    for k in range(4):
        ph = clamp(lt / 1.5)
        grain(ctx, CX - 330 + k * 220, CY - 200 - 60 * ph, 70, SALT_C[k], s=pin(lt, 0.4 + 0.1 * k))
    lbl(ctx, "同じ海の水なのに?", CX, CY - 480, 100, s=pin(lt, 0.2), color="#FFE14D")


def v_lab(ctx, lt, d, gt):
    space_bg(ctx, gt)
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 60); ctx.scale(s, s)
    rrect(ctx, -300, -300, 600, 600, 40); fill_stroke(ctx, "#E9F4FF", lw=10)
    rrect(ctx, -250, -250, 500, 500, 24); fill_stroke(ctx, "#B9DBF5", lw=6)
    ctx.restore()
    drop(ctx, CX, CY + 60, 120 * pin(lt, 0.3), "mix")
    lbl(ctx, "実験室で こおらせた", CX, CY - 400, 92, s=pin(lt, 0.2), color="#FFE14D")
    lbl(ctx, "しずく 約0.2mm", CX, CY + 470, 70, s=pin(lt, 0.4), font="mochiy")


def v_slowfast(ctx, lt, d, gt):
    space_bg(ctx, gt)
    t = clamp((lt - 0.3) / 1.2)
    drop(ctx, CX - 250, CY + 40, 170 * pin(lt), "sep", t=max(0.05, t))
    drop(ctx, CX + 250, CY + 40, 170 * pin(lt, 0.1), "mix")
    lbl(ctx, "ゆっくり", CX - 250, CY - 220, 80, s=pin(lt, 0.2), color="#5BE08A")
    lbl(ctx, "いそいで", CX + 250, CY - 220, 80, s=pin(lt, 0.2), color="#FF6FA8")
    lbl(ctx, "塩が分かれる", CX - 250, CY + 280, 54, s=pin(lt, 0.5), font="mochiy")
    lbl(ctx, "まざったまま", CX + 250, CY + 280, 54, s=pin(lt, 0.5), font="mochiy")


def v_juice(ctx, lt, d, gt):
    space_bg(ctx, gt)
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 40); ctx.scale(s, s)
    rrect(ctx, -230, -260, 460, 520, 30); fill_stroke(ctx, "#FFF4D6", lw=8)
    g = cairo.RadialGradient(0, 0, 20, 0, 0, 230)
    g.add_color_stop_rgba(0, 1.0, 0.55, 0.1, 1); g.add_color_stop_rgba(1, 1.0, 0.95, 0.8, 1)
    rrect(ctx, -220, -250, 440, 500, 26); ctx.set_source(g); ctx.fill()
    ctx.restore()
    lbl(ctx, "まん中が こい!", CX, CY + 40, 74, s=pin(lt, 0.4))
    lbl(ctx, "ジュースの氷", CX, CY - 400, 100, s=pin(lt, 0.2), color="#FFE14D")


def v_seaice(ctx, lt, d, gt):
    space_bg(ctx, gt)
    ctx.rectangle(0, CY + 120, 1080, 900); ctx.set_source_rgba(*hexc("#1E6FD9")); ctx.fill()
    s = pin(lt)
    for k in range(3):
        x = CX - 300 + k * 300
        ctx.save(); ctx.translate(x, CY + 90); ctx.scale(s, s)
        ctx.move_to(-120, 0); ctx.line_to(-90, -70); ctx.line_to(100, -80); ctx.line_to(130, 0); ctx.close_path()
        fill_stroke(ctx, "#F4F9FF", lw=6); ctx.restore()
    lbl(ctx, "海の氷は あまりしょっぱくない", CX, CY - 300, 66, s=pin(lt, 0.3), font="mochiy")
    lbl(ctx, "塩は 外へおし出される", CX, CY + 400, 74, s=pin(lt, 0.5), color="#FFE14D")


def v_journey(ctx, lt, d, gt):
    space_bg(ctx, gt)
    steps = ["① 海のしぶき", "② ゆっくりこおる", "③ かべにぶつかる", "④ バラバラ!"]
    for i, st in enumerate(steps):
        y = CY + 380 - i * 210
        s = pin(lt, 0.25 * i)
        if i == 0:
            drop(ctx, CX - 300, y, 70 * s, "mix")
        elif i == 1:
            drop(ctx, CX - 300, y, 70 * s, "sep")
        elif i == 2:
            drop(ctx, CX - 330, y, 70 * s, "sep"); ctx.rectangle(CX - 250, y - 90, 30, 180); fill_stroke(ctx, "#DDEFFF", lw=5)
        else:
            for k in range(4):
                grain(ctx, CX - 380 + k * 55, y + (k % 2) * 40 - 20, 26, SALT_C[k], s=s, ring=False)
        lbl(ctx, st, CX + 140, y, 64, s=s, font="mochiy")
    lbl(ctx, "氷のつぶの 旅", CX, CY - 480, 90, s=pin(lt), color="#FFE14D")


def v_crash(ctx, lt, d, gt):
    space_bg(ctx, gt)
    ctx.rectangle(CX + 220, CY - 400, 120, 800); fill_stroke(ctx, "#DDEFFF", lw=6)
    t = clamp(lt / 0.8)
    if t < 1:
        drop(ctx, CX - 300 + 420 * t, CY, 130, "sep")
    else:
        k2 = clamp((lt - 0.8) / 0.8)
        for k in range(4):
            a = math.pi * (0.6 + 0.27 * k)
            grain(ctx, CX + 120 + 260 * k2 * math.cos(a), CY + 260 * k2 * math.sin(a), 55, SALT_C[k], ring=False)
        lbl(ctx, "パリーン!", CX - 60, CY - 330, 110, s=pin(lt - 0.8), color="#FF6FA8", rot=-0.06)


def v_japan(ctx, lt, d, gt):
    space_bg(ctx, gt)
    rrect(ctx, CX - 360, CY - 260, 720, 420, 40); fill_stroke(ctx, "#2A2050", stroke="#FFFFFF", lw=8)
    lbl(ctx, "東京科学大学 ELSI", CX, CY - 150, 74, s=pin(lt), color="#FF6FA8")
    lbl(ctx, "関根康人さん", CX, CY - 20, 90, s=pin(lt, 0.2), color="#FFFFFF")
    lbl(ctx, "たちのチーム", CX, CY + 90, 56, s=pin(lt, 0.3), font="mochiy", color="#FFE14D")
    piko(ctx, CX, CY + 400, gt, 0.7 * pin(lt, 0.4), "wow")
    lbl(ctx, "日本のチームも 大活躍!", CX, CY - 440, 84, s=pin(lt, 0.1), color="#FFE14D")


def v_berlin(ctx, lt, d, gt):
    space_bg(ctx, gt)
    lbl(ctx, "ベルリン自由大学", CX, CY - 260, 90, s=pin(lt), color="#FFE14D")
    lbl(ctx, "フランク・ポストベルクさん", CX, CY - 120, 66, s=pin(lt, 0.2), font="mochiy")
    lbl(ctx, "+", CX, CY + 20, 110, s=pin(lt, 0.3))
    lbl(ctx, "東京科学大学", CX, CY + 160, 90, s=pin(lt, 0.4), color="#FF6FA8")
    lbl(ctx, "国をこえたチーム", CX, CY + 400, 70, s=pin(lt, 0.5), font="mochiy")


def v_sample(ctx, lt, d, gt):
    space_bg(ctx, gt)
    moon(ctx, CX, CY - 330, 180 * pin(lt), gt, jets=False)
    plume(ctx, CX, CY - 160, 520, gt, n=5, colored=True)
    rrect(ctx, CX - 360, CY + 350, 720, 200, 30); fill_stroke(ctx, "#2A2050", stroke="#FFFFFF", lw=8)
    lbl(ctx, "自然の 下ごしらえ!", CX, CY + 450, 80, s=pin(lt, 0.3), color="#FF3D7F")


def v_life(ctx, lt, d, gt):
    space_bg(ctx, gt)
    crust(ctx, gt, top=CY - 200, bot=CY + 40, crack=False)
    for k in range(5):
        x = CX - 300 + k * 150; y = CY + 300 + 40 * math.sin(gt * 2 + k)
        circle(ctx, x, y, 34 * pin(lt, 0.1 * k), "#5BE08A", lw=5)
    lbl(ctx, "?", CX + 380, CY + 260, 160, s=pin(lt, 0.5), color="#FFE14D")
    lbl(ctx, "生き物は いる?", CX, CY - 460, 104, s=pin(lt, 0.2), color="#FFE14D")


def v_phos(ctx, lt, d, gt):
    space_bg(ctx, gt)
    rrect(ctx, CX - 200, CY - 260, 400, 440, 40); fill_stroke(ctx, "#B07CFF", lw=10)
    lbl(ctx, "P", CX, CY - 60, 220, s=pin(lt))
    lbl(ctx, "リン", CX, CY + 110, 80, s=pin(lt, 0.2))
    lbl(ctx, "体の骨やDNAにも", CX, CY + 380, 70, s=pin(lt, 0.4), font="mochiy")
    lbl(ctx, "2023年に発見", CX, CY - 460, 96, s=pin(lt, 0.1), color="#FFE14D")


def v_future_probe(ctx, lt, d, gt):
    space_bg(ctx, gt)
    moon(ctx, CX, CY - 420, 230 * pin(lt), gt, jets=False)
    plume(ctx, CX, CY - 190, 700, gt, n=7, colored=True)
    p = clamp(lt / max(d * 0.9, 0.5))
    probe(ctx, CX - 420 + 840 * p, CY + 220, 1.2, gt)
    lbl(ctx, "つぶを1つずつ キャッチ!", CX, CY + 480, 80, s=pin(lt, 0.3), color="#FFE14D")


def v_protect(ctx, lt, d, gt):
    space_bg(ctx, gt)
    saturn(ctx, CX, CY + 300, 330 * pin(lt), gt)
    p = clamp(lt / max(d * 0.8, 0.5))
    probe(ctx, CX + 300 - 300 * p, CY - 380 + 520 * p, 1.0 * (1 - 0.5 * p), gt)
    lbl(ctx, "月をよごさないために", CX, CY - 560, 80, s=pin(lt, 0.2), color="#FFE14D")


def v_dot(ctx, lt, d, gt):
    space_bg(ctx, gt)
    circle(ctx, CX, CY, 14 * pin(lt), "#8FD3FF", lw=0)
    ctx.new_path(); ctx.arc(CX, CY, 70 + 10 * math.sin(gt * 4), 0, 2 * math.pi); ctx.set_source_rgba(*hexc("#FFE14D")); ctx.set_line_width(6); ctx.stroke()
    lbl(ctx, "これが 地球!", CX, CY - 250, 100, s=pin(lt, 0.3), color="#FFE14D")
    lbl(ctx, "土星から 約14億km", CX, CY + 250, 70, s=pin(lt, 0.5), font="mochiy")


def v_esa(ctx, lt, d, gt):
    space_bg(ctx, gt)
    moon(ctx, CX + 200, CY - 250, 160 * pin(lt), gt, jets=True)
    probe(ctx, CX - 250, CY + 220, 1.4 * pin(lt, 0.2), gt)
    lbl(ctx, "2040年代?", CX - 200, CY - 470, 100, s=pin(lt, 0.3), color="#FFE14D")
    lbl(ctx, "ヨーロッパの探査計画", CX, CY + 480, 70, s=pin(lt, 0.4), font="mochiy")


def v_hours(ctx, lt, d, gt):
    space_bg(ctx, gt)
    lbl(ctx, "10℃", CX, CY - 160, 200, s=pin(lt), color="#8FD3FF")
    lbl(ctx, "下がるのに 1分以上", CX, CY + 60, 84, s=pin(lt, 0.2))
    lbl(ctx, "=ゆっくり", CX, CY + 220, 90, s=pin(lt, 0.4), color="#5BE08A")


def v_comment(ctx, lt, d, gt):
    space_bg(ctx, gt)
    moon(ctx, CX, CY - 120, 200 * pin(lt), gt, jets=True, face=True)
    piko(ctx, CX - 300, CY + 330, gt, 0.6 * pin(lt, 0.2), "wow")
    lbl(ctx, "生き物は いると思う?", CX, CY - 460, 88, s=pin(lt, 0.2), color="#FFE14D")
    lbl(ctx, "コメントで 教えてね!", CX + 80, CY + 420, 74, s=pin(lt, 0.4))
