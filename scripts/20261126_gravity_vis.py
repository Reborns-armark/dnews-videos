"""Visuals for the gravity-communication episode (Groszek, Woffinden, Harvey, White & Davis, 'Unblockable communication with gravity',
Science Advances 2026, doi:10.1126/sciadv.aee0802; University of Queensland). Vertical stage, CX=540, CY=760."""
import math, random
import cairo
from common4 import *
from space2 import pin, CX, CY
from hera_vis import label, photo_scene, PHOTO_LAYOUT, v_question, v_longvideo
from casa_vis import v_hello

OPTS = {"short": False}
INK = "#1B1B3A"
BRICK, BRICK2 = "#C8553D", "#A8432F"
STEEL, STEEL2 = "#8A93A6", "#5E667A"
YEL, PINK, BLUE, GREEN = "#FFE14D", "#FF3D7F", "#3DB2FF", "#2ECC71"


def lbl(ctx, t, x, y, size=80, s=1.0, rot=0.0, font="dela", color="#FFFFFF"):
    if OPTS["short"] and font == "mochiy" and size < 56:
        return
    label(ctx, t, x, y, size, color=color, s=s, rot=rot, font=font)


def P(name, credit, title=None, box=(940, 700), **kw):
    return photo_scene(name, credit, title, box=box, **kw)


def bigtext(text, sub=None, color=YEL, size=220):
    def vis(ctx, lt, d, gt):
        sp = text_sprite(text, size, color=color, hi=PINK, path=FONTS["dela"])
        draw_sprite(ctx, sp, CX, CY - 60, pin(lt) * min(1.0, 1000 / sp.get_width()), 1, -0.04)
        if sub:
            sp2 = text_sprite(sub, 74, color="#FFFFFF", hi=YEL, path=FONTS["mochiy"])
            draw_sprite(ctx, sp2, CX, CY + 160, pin(lt, 0.2) * min(1.0, 1000 / sp2.get_width()), 1)
    return vis


def line(ctx, x0, y0, x1, y1, col=INK, w=8):
    ctx.move_to(x0, y0); ctx.line_to(x1, y1); ctx.set_source_rgba(*hexc(col)); ctx.set_line_width(w); ctx.stroke()


def arrow(ctx, x0, y0, x1, y1, col=YEL, w=14, p=1.0):
    x1 = x0 + (x1 - x0) * p; y1 = y0 + (y1 - y0) * p
    if p <= 0.02:
        return
    a = math.atan2(y1 - y0, x1 - x0)
    line(ctx, x0, y0, x1 - 20 * math.cos(a), y1 - 20 * math.sin(a), col, w)
    ctx.move_to(x1, y1)
    for da in (2.6, -2.6):
        ctx.line_to(x1 + 46 * math.cos(a + da), y1 + 46 * math.sin(a + da))
    ctx.close_path(); fill_stroke(ctx, col, lw=4)


def cross(ctx, x, y, r=60, s=1.0):
    if s <= 0:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for a in (1, -1):
        ctx.move_to(-r, -r * a); ctx.line_to(r, r * a)
        ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(34); ctx.stroke()
        ctx.move_to(-r, -r * a); ctx.line_to(r, r * a)
        ctx.set_source_rgba(*hexc(PINK)); ctx.set_line_width(20); ctx.stroke()
    ctx.restore()


def ok(ctx, x, y, r=60, s=1.0):
    if s <= 0:
        return
    ctx.new_path(); ctx.arc(x, y, r * s, 0, 2 * math.pi)
    ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(34); ctx.stroke()
    ctx.new_path(); ctx.arc(x, y, r * s, 0, 2 * math.pi)
    ctx.set_source_rgba(*hexc(GREEN)); ctx.set_line_width(20); ctx.stroke()


# ---------------------------------------------------------------- props
def brick_wall(ctx, x, y, w, h, s=1.0):
    ctx.save(); ctx.translate(x + w / 2, y + h); ctx.scale(1, s); ctx.translate(-(x + w / 2), -(y + h))
    rrect(ctx, x, y, w, h, 6); fill_stroke(ctx, BRICK2, lw=7)
    bh = 46
    ctx.save(); rrect(ctx, x, y, w, h, 6); ctx.clip()
    for r in range(int(h / bh) + 1):
        off = 0 if r % 2 == 0 else 45
        for c in range(-1, int(w / 90) + 2):
            bx = x + c * 90 + off; by = y + r * bh
            rrect(ctx, bx + 3, by + 3, 84, bh - 6, 4)
            ctx.set_source_rgba(*hexc(BRICK if (r + c) % 3 else "#D9694F")); ctx.fill()
    ctx.restore()
    ctx.restore()


def counterweight(ctx, x, y, s=1.0, txt="1.8トン"):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -90, -130, 180, 260, 14); fill_stroke(ctx, STEEL2, lw=8)
    for k in range(5):
        line(ctx, -80, -100 + k * 50, 80, -100 + k * 50, "#46506A", 5)
    line(ctx, 0, -130, 0, -170, INK, 8)
    ctx.restore()
    if txt:
        lbl(ctx, txt, x, y, 50 * s, color=YEL)


def gravimeter(ctx, x, y, s=1.0, gt=0.0, val=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -130, -110, 260, 200, 26); fill_stroke(ctx, "#2E86DE", lw=8)
    rrect(ctx, -100, -85, 200, 100, 14); fill_stroke(ctx, "#E8FFF4", lw=6)
    ctx.move_to(-90, -20)
    for k in range(40):
        xx = -90 + k * 4.6
        yy = -35 - 30 * val * (1 if k > 20 else 0) + 4 * math.sin(gt * 9 + k)
        ctx.line_to(xx, yy)
    ctx.set_source_rgba(*hexc(GREEN)); ctx.set_line_width(6); ctx.stroke()
    for k in range(3):
        circle(ctx, -60 + k * 60, 55, 14, [YEL, PINK, "#FFFFFF"][k], lw=5)
    rrect(ctx, -150, 90, 300, 26, 10); fill_stroke(ctx, "#555B6E", lw=6)
    ctx.restore()


def shaft(ctx, x, top, bot, pos, gt, w=300):
    """Elevator shaft: car on the left half, counterweight on the right half. pos 0=cw down, 1=cw up."""
    rrect(ctx, x - w / 2, top, w, bot - top, 10); fill_stroke(ctx, "#3A3F55", lw=8)
    circle(ctx, x, top + 50, 42, "#C9CEDA", lw=7)
    cy_cw = bot - 160 - (bot - top - 380) * pos
    cy_car = top + 250 + (bot - top - 420) * pos
    line(ctx, x - 42, top + 50, x - 42, cy_car - 100, "#D9DEE8", 5)
    line(ctx, x + 42, top + 50, x + 42, cy_cw - 130, "#D9DEE8", 5)
    rrect(ctx, x - 140, cy_car - 100, 100, 190, 10); fill_stroke(ctx, "#F2C14E", lw=6)
    rrect(ctx, x - 125, cy_car - 70, 70, 120, 6); fill_stroke(ctx, "#FFF3C4", lw=4)
    counterweight(ctx, x + 70, cy_cw, 0.55, None)
    return cy_cw


def ripples(ctx, x, y, gt, col=YEL, n=4, rmax=320, a=0.8, ang=None):
    for k in range(n):
        ph = (gt * 0.6 + k / n) % 1
        r = 40 + rmax * ph
        ctx.new_path()
        if ang:
            ctx.arc(x, y, r, ang[0], ang[1])
        else:
            ctx.arc(x, y, r, 0, 2 * math.pi)
        ctx.set_source_rgba(*hexc(col)[:3], a * (1 - ph)); ctx.set_line_width(10); ctx.stroke()


def phone(ctx, x, y, s=1.0, rot=0.0, screen="#8FD3FF"):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -70, -130, 140, 260, 24); fill_stroke(ctx, "#2B2B3F", lw=7)
    rrect(ctx, -56, -108, 112, 206, 12); fill_stroke(ctx, screen, lw=0)
    circle(ctx, 0, 112, 9, "#55556A", lw=0)
    ctx.restore()


def wifi(ctx, x, y, gt, s=1.0, col=BLUE, a=1.0):
    for k in range(3):
        ctx.new_path(); ctx.arc(x, y, (40 + k * 45) * s, -math.pi * 0.75, -math.pi * 0.25)
        ctx.set_source_rgba(*hexc(col)[:3], a * (0.6 + 0.4 * math.sin(gt * 6 - k))); ctx.set_line_width(14 * s); ctx.stroke()
    circle(ctx, x, y, 12 * s, col, lw=0)


def apple(ctx, x, y, r=50):
    circle(ctx, x, y, r, "#E8413C", lw=7)
    line(ctx, x, y - r, x + 8, y - r - 30, "#6B4226", 8)
    ctx.save(); ctx.translate(x + 26, y - r - 18); ctx.rotate(-0.5)
    ctx.scale(1, 0.5); ctx.new_path(); ctx.arc(0, 0, 26, 0, 2 * math.pi); ctx.restore(); fill_stroke(ctx, GREEN, lw=5)


def earth(ctx, x, y, r):
    circle(ctx, x, y, r, "#2E86DE", lw=8)
    rnd = random.Random(3)
    ctx.save(); ctx.new_path(); ctx.arc(x, y, r - 6, 0, 2 * math.pi); ctx.clip()
    for k in range(6):
        cx_, cy_ = x + rnd.uniform(-0.7, 0.7) * r, y + rnd.uniform(-0.7, 0.7) * r
        ctx.new_path(); ctx.arc(cx_, cy_, r * rnd.uniform(0.18, 0.35), 0, 2 * math.pi); ctx.set_source_rgba(*hexc("#3BB273")); ctx.fill()
    ctx.restore()


def truck(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -230, -150, 300, 150, 12); fill_stroke(ctx, "#F2994A", lw=7)
    rrect(ctx, 70, -110, 130, 110, 16); fill_stroke(ctx, "#56CCF2", lw=7)
    rrect(ctx, 120, -95, 60, 45, 8); fill_stroke(ctx, "#E8FFFF", lw=5)
    for wx in (-170, -60, 140):
        circle(ctx, wx, 10, 38, "#2B2B3F", lw=6); circle(ctx, wx, 10, 14, "#BBBBCC", lw=0)
    ctx.restore()


def tank(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -260, -40, 520, 110, 55); fill_stroke(ctx, "#4E5B31", lw=8)
    for k in range(6):
        circle(ctx, -200 + k * 80, 15, 30, "#2B2B3F", lw=5)
    rrect(ctx, -200, -120, 330, 90, 20); fill_stroke(ctx, "#6B7A3E", lw=8)
    rrect(ctx, -110, -190, 190, 80, 30); fill_stroke(ctx, "#7D8C48", lw=8)
    rrect(ctx, 70, -170, 300, 30, 12); fill_stroke(ctx, "#6B7A3E", lw=7)
    ctx.restore()


# ---------------------------------------------------------------- scenes
def v_hook(ctx, lt, d, gt):
    pos = 0.5 + 0.5 * math.sin(gt * 1.6)
    shaft(ctx, 270, 330, 1290, pos, gt, w=320)
    brick_wall(ctx, 470, 420, 110, 870, pin(lt, 0.1))
    gravimeter(ctx, 820, 1130, 1.0 * pin(lt, 0.2), gt, pos)
    ripples(ctx, 340, 900, gt, YEL, 4, 560, 0.7, (-0.9, 0.9))
    lbl(ctx, "かべの向こうへ", CX, 260, 80, s=pin(lt, 0.15), color="#FFFFFF")
    sp = text_sprite("Gravity", 120, color=YEL, hi=PINK, path=FONTS["dela"])
    draw_sprite(ctx, sp, 800, 650 + 10 * math.sin(gt * 3), pin(lt, 0.4) * 0.8, 1, -0.06)
    lbl(ctx, "重力で メッセージ!?", 800, 820, 56, s=pin(lt, 0.5), color=PINK, font="mochiy")


def v_hook_q(ctx, lt, d, gt):
    """Shorts experiment-A cut 1: same picture as v_hook, but a home elevator + a big '?'."""
    v_hook(ctx, lt, d, gt)
    draw_sprite(ctx, text_sprite("?", 200, color=YEL, path=FONTS["dela"]), 800, 470, pin(lt, 0.3), 1, 0.25 * math.sin(gt * 4))


def v_elev(ctx, lt, d, gt):
    pos = 0.5 + 0.5 * math.sin(gt * 1.4)
    cy = shaft(ctx, CX - 120, 280, 1290, pos, gt, w=420)
    lbl(ctx, "おもり", CX + 260, cy - 40, 70, s=pin(lt, 0.2), color=YEL)
    arrow(ctx, CX + 170, cy, CX + 30, cy, YEL, 12, pin(lt, 0.3))
    lbl(ctx, "かご", CX + 260, 1120 - 700 * pos, 60, s=pin(lt, 0.3), color="#FFFFFF", font="mochiy")
    lbl(ctx, "かごと おもりは シーソーの関係", CX, 1360, 52, s=pin(lt, 0.5), font="mochiy")


def v_cw(ctx, lt, d, gt):
    counterweight(ctx, CX, CY, 2.2 * pin(lt), None)
    lbl(ctx, "約1.8トン", CX, CY, 120, s=pin(lt, 0.2), color=YEL)
    lbl(ctx, "エレベーターの おもり", CX, 330, 84, s=pin(lt, 0.1))
    lbl(ctx, "車 1〜2台分くらい", CX, 1180, 66, s=pin(lt, 0.4), font="mochiy")


def v_wall(ctx, lt, d, gt):
    brick_wall(ctx, CX - 60, 360, 120, 900, pin(lt))
    # radio waves bouncing back
    wifi(ctx, 220, 560, gt, 1.1)
    arrow(ctx, 230, 600, 440, 600, BLUE, 12, pin(lt, 0.2))
    cross(ctx, 760, 600, 60, pin(lt, 0.5))
    lbl(ctx, "電波・光・音", 260, 440, 54, s=pin(lt, 0.2), font="mochiy")
    # gravity passes
    arrow(ctx, 160, 1020, 920, 1020, YEL, 16, pin(lt, 0.7))
    ok(ctx, 820, 900, 60, pin(lt, 0.9))
    lbl(ctx, "重力", 250, 920, 80, s=pin(lt, 0.7), color=YEL)
    lbl(ctx, "れんがのかべ", CX, 300, 66, s=pin(lt, 0.1), color="#FFFFFF")


def v_meter(ctx, lt, d, gt):
    v = 1.0 if (gt % 4) > 2 else 0.0
    gravimeter(ctx, CX, CY - 40, 2.6 * pin(lt), gt, v)
    lbl(ctx, "重力計", CX, 320, 120, s=pin(lt, 0.1), color=YEL)
    lbl(ctx, "重力の ほんの少しの変化を はかる", CX, 1220, 52, s=pin(lt, 0.4), font="mochiy")


def v_room(ctx, lt, d, gt):
    pos = 1.0 if (gt % 6) > 3 else 0.0
    shaft(ctx, 250, 300, 1290, pos, gt, w=300)
    brick_wall(ctx, 430, 300, 90, 990, 1)
    rrect(ctx, 520, 300, 500, 990, 10); fill_stroke(ctx, "#E6F4FF", lw=8)
    for k in range(6):
        line(ctx, 540 + k * 80, 1150, 540 + k * 80, 1290, "#B9D8EE", 4)
    gravimeter(ctx, 770, 1160, 0.9 * pin(lt, 0.2), gt, pos)
    lbl(ctx, "となりの部屋", 770, 400, 70, s=pin(lt, 0.1), color=PINK)
    lbl(ctx, "約0.7m", 470, 1220, 60, s=pin(lt, 0.4), color=YEL)


def v_bits(ctx, lt, d, gt):
    lbl(ctx, "おもりの位置で 0と1", CX, 300, 76, s=pin(lt, 0.05), color="#FFFFFF")
    for k, (txt, up) in enumerate([("1", True), ("0", False)]):
        x = CX - 220 + k * 440
        rrect(ctx, x - 150, 420, 300, 660, 16); fill_stroke(ctx, "#3A3F55", lw=7)
        y = 560 if up else 940
        counterweight(ctx, x, y, 0.7 * pin(lt, 0.2 + 0.15 * k), None)
        lbl(ctx, "上" if up else "下", x, 1150, 76, s=pin(lt, 0.3 + 0.15 * k), color="#FFFFFF")
        lbl(ctx, txt, x + (0 if up else 0), 760 if up else 620, 200, s=pin(lt, 0.4 + 0.15 * k), color=YEL if up else BLUE)


def v_ascii(ctx, lt, d, gt):
    sp = text_sprite("G", 330, color=YEL, hi=PINK, path=FONTS["dela"])
    draw_sprite(ctx, sp, CX, 520, pin(lt), 1, -0.05)
    arrow(ctx, CX, 720, CX, 860, "#FFFFFF", 14, pin(lt, 0.3))
    bits = "1000111"
    for k, b in enumerate(bits):
        x = CX - 390 + k * 130
        rrect(ctx, x - 55, 920, 110, 150, 16); fill_stroke(ctx, YEL if b == "1" else "#8FD3FF", lw=7)
        lbl(ctx, b, x, 995, 100, s=pin(lt, 0.4 + 0.08 * k), color=INK)
    lbl(ctx, "文字は 0と1の 7けたで 表せる", CX, 1200, 54, s=pin(lt, 0.8), font="mochiy")


def v_word(ctx, lt, d, gt):
    w = "Gravity"
    for k, ch in enumerate(w):
        x = CX - 390 + k * 130
        sp = text_sprite(ch, 170, color=[YEL, PINK, BLUE, GREEN][k % 4], path=FONTS["dela"])
        draw_sprite(ctx, sp, x, CY - 80 + 18 * math.sin(gt * 4 + k), pin(lt, k * 0.1), 1, 0.1 * math.sin(gt * 3 + k))
    lbl(ctx, "送った言葉は「重力」!", CX, CY + 220, 80, s=pin(lt, 0.8), color="#FFFFFF")


def v_hour(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY - 40); ctx.scale(s, s)
    circle(ctx, 0, 0, 300, "#FFFFFF", lw=12)
    for k in range(12):
        a = k * math.pi / 6
        line(ctx, 260 * math.cos(a), 260 * math.sin(a), 285 * math.cos(a), 285 * math.sin(a), INK, 8)
    a = gt * 2.0 - math.pi / 2
    line(ctx, 0, 0, 230 * math.cos(a), 230 * math.sin(a), PINK, 12)
    line(ctx, 0, 0, 150 * math.cos(a / 12), 150 * math.sin(a / 12), INK, 16)
    circle(ctx, 0, 0, 20, INK, lw=0)
    ctx.restore()
    lbl(ctx, "1分で 1けた", CX, 300, 96, s=pin(lt, 0.2), color=YEL)
    lbl(ctx, "1つの言葉に 約1時間!", CX, 1210, 76, s=pin(lt, 0.5), color="#FFFFFF")


def v_apple(ctx, lt, d, gt):
    ctx.rectangle(0, 1180, 1080, 200); ctx.set_source_rgba(*hexc("#5DBB63")); ctx.fill()
    rrect(ctx, 210, 640, 70, 560, 20); fill_stroke(ctx, "#8B5A2B", lw=7)
    for (x, y, r) in [(250, 560, 190), (110, 650, 120), (390, 650, 130)]:
        circle(ctx, x, y, r, "#3BB273", lw=7)
    fall = clamp((lt - 0.3) / 0.8)
    apple(ctx, 400, 700 + 420 * fall * fall, 46)
    earth(ctx, 800, 1060, 120 * pin(lt, 0.2))
    lbl(ctx, "ものは みんな 引き合う", CX, 300, 80, s=pin(lt, 0.1), color=YEL)
    lbl(ctx, "万有引力", 790, 820, 76, s=pin(lt, 0.6), color="#FFFFFF")


def v_you(ctx, lt, d, gt):
    piko(ctx, CX - 220, CY + 120, gt, 1.0 * pin(lt), "wow")
    phone(ctx, CX + 260, CY + 100, 1.3 * pin(lt, 0.2), 0.1)
    p = 0.5 + 0.5 * math.sin(gt * 4)
    arrow(ctx, CX - 40, CY - 120, CX + 120, CY - 120, YEL, 10, 0.6 + 0.4 * p)
    arrow(ctx, CX + 140, CY - 40, CX - 20, CY - 40, YEL, 10, 0.6 + 0.4 * p)
    lbl(ctx, "あなたと スマホも", CX, 300, 84, s=pin(lt, 0.1))
    lbl(ctx, "ほんの少し 引き合っている!", CX, 1230, 64, s=pin(lt, 0.4), color=YEL)


def v_signals(ctx, lt, d, gt):
    rows = [("電波", BLUE, False), ("光", YEL, False), ("音", "#FFFFFF", False), ("重力", PINK, True)]
    lbl(ctx, "かべで 止められる?", CX, 290, 84, s=pin(lt, 0.05), color="#FFFFFF")
    for k, (nm, col, passes) in enumerate(rows):
        y = 470 + k * 210
        rrect(ctx, 100, y - 80, 880, 160, 30); fill_stroke(ctx, "#FFFFFF", lw=7)
        lbl(ctx, nm, 250, y, 70, s=pin(lt, 0.15 + k * 0.15), color=col if col != "#FFFFFF" else "#9AA3B5")
        brick_wall(ctx, 560, y - 70, 50, 140, 1)
        if passes:
            ok(ctx, 820, y, 50, pin(lt, 0.3 + k * 0.15))
        else:
            cross(ctx, 820, y, 42, pin(lt, 0.3 + k * 0.15))


def v_shield(ctx, lt, d, gt):
    items = [("鉄", STEEL), ("なまり", "#6C7A89"), ("水", BLUE), ("コンクリート", "#B0A99F")]
    lbl(ctx, "重力を さえぎる物は…", CX, 290, 80, s=pin(lt, 0.05), color="#FFFFFF")
    for k, (nm, col) in enumerate(items):
        x = 200 + k * 230
        rrect(ctx, x - 90, 520, 180, 520, 20); fill_stroke(ctx, col, lw=8)
        lbl(ctx, nm, x, 780, 50 if len(nm) > 3 else 64, s=pin(lt, 0.1 + 0.1 * k), color="#FFFFFF")
    arrow(ctx, 40, 900, 1040, 900, YEL, 18, clamp((lt - 0.4) / 0.8))
    lbl(ctx, "ない!ぜんぶ すりぬける", CX, 1200, 76, s=pin(lt, 1.0), color=YEL)


def v_faraday(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY); ctx.scale(s, s)
    rrect(ctx, -330, -300, 660, 600, 20); ctx.set_source_rgba(1, 1, 1, 0.12); ctx.fill()
    for k in range(12):
        x = -330 + k * 60
        line(ctx, x, -300, x, 300, "#C9CEDA", 7)
    for k in range(11):
        y = -300 + k * 60
        line(ctx, -330, y, 330, y, "#C9CEDA", 7)
    ctx.restore()
    phone(ctx, CX, CY, 1.2 * pin(lt, 0.2), 0, "#55556A")
    wifi(ctx, CX + 400, CY - 380, gt, 1.0, BLUE)
    cross(ctx, CX + 300, CY - 280, 40, pin(lt, 0.5))
    lbl(ctx, "金あみの へや", CX, 300, 84, s=pin(lt, 0.1), color=YEL)
    lbl(ctx, "電波は 入れない", CX, 1200, 70, s=pin(lt, 0.4), color="#FFFFFF")


def v_elevator_phone(ctx, lt, d, gt):
    rrect(ctx, CX - 280, 380, 560, 860, 20); fill_stroke(ctx, "#C9CEDA", lw=10)
    line(ctx, CX, 380, CX, 1240, "#8A93A6", 8)
    piko(ctx, CX, CY + 120, gt, 0.9 * pin(lt), "wow")
    phone(ctx, CX + 170, CY + 80, 0.6 * pin(lt, 0.2), 0.2, "#55556A")
    cross(ctx, CX + 170, CY - 60, 30, pin(lt, 0.4))
    lbl(ctx, "圏外…", CX + 170, 470, 66, s=pin(lt, 0.4), color=PINK)
    lbl(ctx, "エレベーターで スマホが…", CX, 300, 66, s=pin(lt, 0.1), color="#FFFFFF")


def v_stuck(ctx, lt, d, gt):
    pos = 1.0 if (gt % 4) > 2 else 0.0
    shaft(ctx, 300, 330, 1290, pos, gt, w=320)
    gravimeter(ctx, 790, 1120, 0.9, gt, pos)
    ripples(ctx, 360, 860, gt, YEL, 4, 480, 0.7, (-0.9, 0.9))
    lbl(ctx, "SOS!?", 790, 600, 140, s=pin(lt, 0.2), color=PINK, rot=-0.06)
    lbl(ctx, "論文に 書かれた ジョーク", CX, 260, 60, s=pin(lt, 0.1), color="#FFFFFF", font="mochiy")


def v_weigh(ctx, lt, d, gt):
    ctx.rectangle(0, 1080, 1080, 260); ctx.set_source_rgba(*hexc("#555B6E")); ctx.fill()
    for k in range(6):
        rrect(ctx, 40 + k * 190, 1190, 110, 18, 6); ctx.set_source_rgba(1, 1, 1, 0.9); ctx.fill()
    x = -200 + (lt * 260) % 1500
    truck(ctx, x, 1060, 1.0)
    gravimeter(ctx, 820, 900, 0.8 * pin(lt, 0.2), gt, 1.0 if abs(x - 820) < 300 else 0.0)
    lbl(ctx, "さわらずに 重さをはかる", CX, 300, 76, s=pin(lt, 0.1), color=YEL)
    lbl(ctx, "はじめの アイデア", CX, 430, 60, s=pin(lt, 0.3), color="#FFFFFF", font="mochiy")


def v_tide(ctx, lt, d, gt):
    earth(ctx, CX - 120, CY, 260 * pin(lt))
    ctx.save(); ctx.translate(CX - 120, CY); ctx.scale(1.0 + 0.08 * (0.5 + 0.5 * math.sin(gt * 2)), 1.0)
    ctx.new_path(); ctx.arc(0, 0, 300, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(YEL)[:3], 0.8); ctx.set_line_width(8); ctx.set_dash([20, 14]); ctx.stroke(); ctx.set_dash([])
    ctx.restore()
    circle(ctx, CX + 360, CY, 80 * pin(lt, 0.2), "#E0E0E8", lw=7)
    lbl(ctx, "月", CX + 360, CY + 150, 70, s=pin(lt, 0.3))
    lbl(ctx, "地面も 月に 引っぱられて", CX, 300, 70, s=pin(lt, 0.2), color="#FFFFFF")
    lbl(ctx, "1日2回 上下する!", CX, 1220, 80, s=pin(lt, 0.5), color=YEL)


def v_noise(ctx, lt, d, gt):
    gravimeter(ctx, CX, 640, 1.6 * pin(lt), gt, 0.0)
    ctx.move_to(100, 1050)
    for k in range(120):
        x = 100 + k * 7.3
        ctx.line_to(x, 1050 + 40 * math.sin(k * 0.7 + gt * 8) * (0.6 + 0.4 * math.sin(k * 0.13)))
    ctx.set_source_rgba(*hexc(PINK)); ctx.set_line_width(8); ctx.stroke()
    lbl(ctx, "ゆれ・人の動き・潮…", CX, 1230, 64, s=pin(lt, 0.3), color="#FFFFFF")
    lbl(ctx, "じゃまが いっぱい", CX, 300, 84, s=pin(lt, 0.1), color=YEL)


def v_steps(ctx, lt, d, gt):
    """Stylised version of the measured staircase signal (not the paper's real data)."""
    rrect(ctx, 80, 420, 920, 620, 24); fill_stroke(ctx, "#FFFFFF", lw=8)
    bits = "1000111"
    p = clamp(lt / max(1.0, d * 0.8))
    ctx.move_to(120, 900)
    n = len(bits)
    for k, b in enumerate(bits[: max(1, int(n * p) + 1)]):
        x0 = 120 + k * 120; y = 600 if b == "1" else 900
        ctx.line_to(x0, y); ctx.line_to(x0 + 120, y)
    ctx.set_source_rgba(*hexc(BLUE)); ctx.set_line_width(12); ctx.stroke()
    for k, b in enumerate(bits):
        lbl(ctx, b, 180 + k * 120, 990, 60, s=pin(lt, 0.1 * k), color=INK)
    lbl(ctx, "重力計の グラフ(イメージ)", CX, 330, 64, s=pin(lt, 0.1), color="#FFFFFF")
    lbl(ctx, "ぴったり 読めた!", CX, 1200, 84, s=pin(lt, 0.6), color=YEL)


def v_rates(ctx, lt, d, gt):
    lbl(ctx, "1分に 送れる けた数", CX, 300, 76, s=pin(lt, 0.05), color="#FFFFFF")
    rows = [("今回の実験", 1, PINK), ("ボイジャー1号へ", 960, BLUE)]
    for k, (nm, v, col) in enumerate(rows):
        y = 560 + k * 330
        lbl(ctx, nm, CX, y - 90, 60, s=pin(lt, 0.2 + 0.2 * k), color="#FFFFFF", font="mochiy")
        w = 40 + 820 * (math.log10(v + 1) / math.log10(961)) * clamp((lt - 0.3 - 0.2 * k) / 0.6)
        rrect(ctx, 120, y - 30, max(30, w), 90, 20); fill_stroke(ctx, col, lw=7)
        lbl(ctx, f"{v}", 120 + max(30, w) + 90, y + 15, 76, s=pin(lt, 0.5 + 0.2 * k), color=YEL)
    lbl(ctx, "(長さは 目もりを ちぢめています)", CX, 1230, 44, s=pin(lt, 0.8), font="mochiy")


def v_range(ctx, lt, d, gt):
    lbl(ctx, "とどく きょり(計算)", CX, 300, 80, s=pin(lt, 0.05), color="#FFFFFF")
    lbl(ctx, "いま 約0.7m", CX, 520, 90, s=pin(lt, 0.2), color=BLUE)
    arrow(ctx, CX, 620, CX, 860, YEL, 18, pin(lt, 0.4))
    lbl(ctx, "工夫すれば", CX, 940, 70, s=pin(lt, 0.6), color="#FFFFFF")
    lbl(ctx, "約500m!?", CX, 1060, 130, s=pin(lt, 0.65), color=YEL)
    lbl(ctx, "約700倍", CX, 1230, 80, s=pin(lt, 0.8), color=PINK)


def v_tank(ctx, lt, d, gt):
    tank(ctx, CX - 40, CY + 60, 1.4 * pin(lt))
    lbl(ctx, "おもりを 戦車くらいに", CX, 320, 76, s=pin(lt, 0.1), color="#FFFFFF")
    lbl(ctx, "7万5000kg", CX, 1180, 110, s=pin(lt, 0.4), color=YEL)


def v_atoms(ctx, lt, d, gt):
    rnd = random.Random(7)
    for k in range(40):
        a = rnd.uniform(0, 2 * math.pi); r = rnd.uniform(0, 260)
        x = CX + r * math.cos(a + gt * 0.5); y = CY + r * math.sin(a + gt * 0.5) * 0.7
        circle(ctx, x, y, 16 * pin(lt, k * 0.01), [BLUE, "#8FD3FF", YEL][k % 3], lw=4)
    lbl(ctx, "原子で はかる 未来の重力計", CX, 300, 66, s=pin(lt, 0.1), color="#FFFFFF")
    lbl(ctx, "もっと 小さく・敏感に", CX, 1220, 76, s=pin(lt, 0.4), color=YEL)


def v_bunker(ctx, lt, d, gt):
    ctx.rectangle(0, 600, 1080, 780); ctx.set_source_rgba(*hexc("#7A5A3A")); ctx.fill()
    ctx.rectangle(0, 560, 1080, 50); ctx.set_source_rgba(*hexc("#5DBB63")); ctx.fill()
    rrect(ctx, CX - 260, 900, 520, 300, 30); fill_stroke(ctx, "#8A93A6", lw=8)
    piko(ctx, CX, 1080, gt, 0.6 * pin(lt), "smile")
    gravimeter(ctx, CX + 300, 480, 0.7 * pin(lt, 0.2), gt, 1.0 if gt % 3 > 1.5 else 0)
    ripples(ctx, CX, 1000, gt, YEL, 4, 520, 0.6, (-math.pi, 0))
    lbl(ctx, "地下の 深い へやから", CX, 300, 72, s=pin(lt, 0.1), color="#FFFFFF")


def v_cav(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY); ctx.scale(s, s)
    rrect(ctx, -400, -330, 800, 640, 20); fill_stroke(ctx, "#F6EBD0", lw=8)
    line(ctx, 0, -320, 0, -40, INK, 5)
    a = 0.15 * math.sin(gt * 1.2)
    ctx.save(); ctx.translate(0, -40); ctx.rotate(a)
    line(ctx, -260, 0, 260, 0, INK, 10)
    circle(ctx, -260, 0, 26, "#B08D57", lw=6); circle(ctx, 260, 0, 26, "#B08D57", lw=6)
    ctx.restore()
    circle(ctx, -250, 110, 90, STEEL2, lw=8); circle(ctx, 250, -190, 90, STEEL2, lw=8)
    ctx.restore()
    lbl(ctx, "1798年 キャベンディッシュ", CX, 330, 70, s=pin(lt, 0.2), color=YEL)
    lbl(ctx, "なまりの玉の 引き合いを はかった", CX, 1210, 52, s=pin(lt, 0.4), font="mochiy")


def v_aus(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY); ctx.scale(s, s)
    pts = [(-330, -120), (-200, -230), (-40, -200), (60, -300), (160, -160), (250, -260), (360, -60), (330, 140), (180, 260), (0, 200), (-170, 230), (-330, 120)]
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.close_path(); fill_stroke(ctx, "#F2994A", lw=8)
    circle(ctx, 330, 40, 22, PINK, lw=6)
    ctx.restore()
    lbl(ctx, "オーストラリア", CX, 300, 90, s=pin(lt, 0.1), color="#FFFFFF")
    lbl(ctx, "クイーンズランド大学", CX, 1210, 76, s=pin(lt, 0.4), color=YEL)


def v_semaphore(ctx, lt, d, gt):
    lbl(ctx, "電気を 使わず 読めるかも", CX, 300, 70, s=pin(lt, 0.1), color="#FFFFFF")
    line(ctx, CX, 1250, CX, 700, INK, 18)
    circle(ctx, CX, 700, 70, "#FFD6B0", lw=8)
    a = 0.6 * math.sin(gt * 3)
    for sx in (-1, 1):
        ctx.save(); ctx.translate(CX, 860); ctx.rotate(sx * (1.0 + a * sx))
        line(ctx, 0, 0, 0, -280, INK, 14)
        rrect(ctx, -60, -380, 120, 110, 8); fill_stroke(ctx, [PINK, YEL][(sx + 1) // 2], lw=6)
        ctx.restore()
    lbl(ctx, "手旗信号に にている", CX, 1330, 64, s=pin(lt, 0.4), color=YEL)


def v_future(ctx, lt, d, gt):
    piko(ctx, CX, CY + 260, gt, 0.9 * pin(lt), "wow")
    for k, (t, x, y) in enumerate([("ひみつの通信", 280, 480), ("地下・洞くつ", 800, 560), ("海の中?", 300, 760), ("宇宙?", 790, 820)]):
        rrect(ctx, x - 190, y - 60, 380, 120, 40); fill_stroke(ctx, "#FFFFFF", lw=7)
        lbl(ctx, t, x, y, 50, s=pin(lt, 0.2 + 0.12 * k), color=INK, font="mochiy" if not OPTS["short"] else "dela")
    lbl(ctx, "重力通信の 使い道", CX, 300, 84, s=pin(lt, 0.05), color=YEL)


def v_comment(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY); ctx.scale(s, s); ctx.rotate(0.05 * math.sin(gt * 5))
    rrect(ctx, -300, -200, 600, 360, 60); fill_stroke(ctx, "#FFFFFF", lw=12)
    ctx.move_to(-120, 150); ctx.line_to(-200, 280); ctx.line_to(-20, 160); ctx.close_path(); fill_stroke(ctx, "#FFFFFF", lw=12)
    rrect(ctx, -300, -200, 600, 360, 60); ctx.set_source_rgba(1, 1, 1, 1); ctx.fill()
    for k in range(3):
        circle(ctx, -150 + k * 150, -20, 40 * pin(lt, 0.2 + k * 0.15), PINK, lw=6)
    ctx.restore()


v_18t = bigtext("1.8トン", "エレベーターの おもり", size=230)
v_1950 = bigtext("1950年代", "の 古いエレベーター", size=200)
v_07m = bigtext("約70cm", "かべを はさんだ きょり", size=220)
v_tiny = bigtext("約2億分の1", "地球の重力に くらべた 変化", size=150)
v_49 = bigtext("49けた", "Gravity の 7文字ぶん", size=220)
v_1bit = bigtext("1分に1けた", "のんびりな 通信", size=170)
v_noblock = bigtext("さえぎれない!", "重力の いちばんの とくちょう", size=150)
v_sciadv = bigtext("11月", "サイエンス・アドバンシズに 発表", size=230)
v_100y = bigtext("100年以上", "電信から スマホまで", size=190)
v_015 = bigtext("1分に15けた", "最新の重力計なら(計算)", size=140)
