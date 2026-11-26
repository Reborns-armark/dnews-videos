"""Visuals for the 'record hummingbird migration tracked by passers-by phones' episode
(Rhodes et al., Ecology and Evolution 2026, doi:10.1002/ecy3.74624; Science news 2026-11-23). Vertical stage, CX=540, CY=760."""
import math, random
import cairo
from common4 import *
from space2 import pin, CX, CY
from hera_vis import label, photo_scene, PHOTO_LAYOUT, v_question, v_longvideo

OPTS = {"short": False}
INK = "#1B1B3A"
RUF = "#E8743B"     # rufous orange
GRN = "#3FAF5A"
SKY = "#5BC0EB"
YEL = "#FFE14D"
PINK = "#FF3D7F"


def lbl(ctx, t, x, y, size=80, s=1.0, rot=0.0, font="dela", color="#FFFFFF"):
    if OPTS["short"] and font == "mochiy" and size < 70:
        return
    label(ctx, t, x, y, size, color=color, s=s, rot=rot, font=font)


def P(name, credit, title=None, box=(940, 700), **kw):
    return photo_scene(name, credit, title, box=box, **kw)


def bigtext(text, sub=None, color=YEL, size=220, title=None):
    def vis(ctx, lt, d, gt):
        if title:
            lbl(ctx, title, CX, CY - 400, 96, s=pin(lt))
        draw_sprite(ctx, text_sprite(text, size, color=color, hi=PINK, path=FONTS["dela"]), CX, CY - 40, pin(lt, 0.1), 1, -0.04)
        if sub:
            draw_sprite(ctx, text_sprite(sub, 78, color="#FFFFFF", hi=YEL, path=FONTS["mochiy"]), CX, CY + 180, pin(lt, 0.3), 1)
    return vis


# ---------------------------------------------------------------- props
def hb(ctx, x, y, s, gt, col=RUF, flip=False, mood="smile", tag=False, rot=0.0, blur=True):
    """Cute hummingbird facing right (flip=True faces left), hovering wings."""
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y + 8 * math.sin(gt * 6)); ctx.rotate(rot)
    ctx.scale(-s if flip else s, s)
    # wings (fast flap)
    a = math.sin(gt * 60)
    for k, alpha in ((0, 1.0), (1, 0.35) if blur else (0, 0)):
        if alpha == 0:
            continue
        ang = -0.9 + 0.9 * (a if k == 0 else -a)
        ctx.save(); ctx.translate(-10, -40); ctx.rotate(ang)
        ctx.move_to(0, 0); ctx.curve_to(-60, -40, -150, -150, -110, -190); ctx.curve_to(-60, -150, -20, -60, 0, 0); ctx.close_path()
        ctx.set_source_rgba(0.85, 0.95, 1.0, 0.9 * alpha); ctx.fill_preserve()
        ctx.set_source_rgba(0.1, 0.1, 0.23, alpha); ctx.set_line_width(6); ctx.stroke()
        ctx.restore()
    # tail
    ctx.move_to(-70, 20); ctx.line_to(-170, 70); ctx.line_to(-150, 20); ctx.line_to(-175, -5); ctx.close_path(); fill_stroke(ctx, col, lw=6)
    # body
    ctx.save(); ctx.scale(1.25, 0.85); ctx.new_path(); ctx.arc(0, 10, 75, 0, 2 * math.pi); ctx.restore(); fill_stroke(ctx, col, lw=7)
    ctx.save(); ctx.scale(1.0, 0.6); ctx.new_path(); ctx.arc(10, 70, 55, 0, 2 * math.pi); ctx.restore(); fill_stroke(ctx, "#FFF3E6", lw=0)
    # head
    circle(ctx, 70, -45, 50, GRN, lw=7)
    circle(ctx, 70, -10, 26, "#FF5A3D", lw=0)  # throat (gorget)
    # beak
    ctx.move_to(112, -55); ctx.line_to(230, -62); ctx.line_to(114, -38); ctx.close_path(); fill_stroke(ctx, INK, lw=4)
    # eye
    if mood == "wow":
        circle(ctx, 85, -55, 13, "#FFFFFF", lw=4); circle(ctx, 87, -55, 7, INK, lw=0)
    else:
        circle(ctx, 85, -55, 10, INK, lw=0); circle(ctx, 88, -59, 3.5, "#FFFFFF", lw=0)
    circle(ctx, 55, -25, 10, "#FF9EC4", lw=0)
    if tag:
        rrect(ctx, -30, -50, 34, 22, 4); fill_stroke(ctx, "#2E3F8F", lw=4)
        ctx.move_to(-13, -28); ctx.line_to(-110, 50); ctx.set_source_rgba(0.1, 0.1, 0.2, 1); ctx.set_line_width(3); ctx.stroke()
    ctx.restore()


def flower(ctx, x, y, s, col="#FF3D5A", gt=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(0, 0); ctx.line_to(0, 380); ctx.set_source_rgba(*hexc("#2E8B57")); ctx.set_line_width(12); ctx.stroke()
    for i in range(5):
        a = -1.2 + i * 0.6 + 0.05 * math.sin(gt * 2 + i)
        ctx.save(); ctx.rotate(a); rrect(ctx, -14, -110, 28, 110, 14); fill_stroke(ctx, col, lw=5); ctx.restore()
    circle(ctx, 0, 0, 22, YEL, lw=5)
    ctx.restore()


def phone(ctx, x, y, s, gt, waves=True, screen="#9FE3FF", rot=0.0):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -80, -150, 160, 300, 26); fill_stroke(ctx, "#2A2438", lw=8)
    rrect(ctx, -64, -124, 128, 236, 12); fill_stroke(ctx, screen, lw=0)
    circle(ctx, 0, 130, 9, "#FFFFFF", lw=0)
    # pin on screen
    ctx.move_to(0, 30); ctx.curve_to(-50, -20, -40, -80, 0, -80); ctx.curve_to(40, -80, 50, -20, 0, 30); ctx.close_path(); fill_stroke(ctx, PINK, lw=5)
    circle(ctx, 0, -45, 14, "#FFFFFF", lw=0)
    ctx.restore()
    if waves:
        for k in range(3):
            f = (gt * 0.8 + k / 3) % 1
            ctx.new_path(); ctx.arc(x, y - 40 * s, (60 + 260 * f) * s, -2.6, -0.5)
            ctx.set_source_rgba(1, 0.88, 0.3, 1 - f); ctx.set_line_width(10 * s + 2); ctx.stroke()


def tag(ctx, x, y, s, gt=0.0, shine=True):
    """The BluMorpho-like solar tag: small panel + antenna."""
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(0, 60); ctx.line_to(0, 330); ctx.set_source_rgba(0.1, 0.1, 0.2, 1); ctx.set_line_width(8); ctx.stroke()
    rrect(ctx, -70, -110, 140, 180, 12); fill_stroke(ctx, "#2E3F8F", lw=7)
    for g in (-1, 1):
        ctx.move_to(g * 23, -105); ctx.rel_line_to(0, 170); ctx.set_source_rgba(0.7, 0.8, 1, 0.7); ctx.set_line_width(4); ctx.stroke()
    rrect(ctx, -30, 70, 60, 30, 6); fill_stroke(ctx, "#C9CED8", lw=5)
    if shine and 0.2 < (gt % 1.6) < 0.45:
        circle(ctx, 40, -80, 18, "#FFFFFF", lw=0)
    ctx.restore()


def coin(ctx, x, y, r, txt="1"):
    if r < 8:
        return
    circle(ctx, x, y, r, "#E6E8EE", lw=6)
    circle(ctx, x, y, r * 0.82, "#F4F5F8", lw=2)
    draw_sprite(ctx, text_sprite(txt, int(r * 0.9), color="#8A90A0", stroke="#FFFFFF", stroke_w=2, shadow=False, path=FONTS["dela"]), x, y, 1, 1)


def rice(ctx, x, y, s, rot=0.3):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s * 0.55)
    ctx.new_path(); ctx.arc(0, 0, 40, 0, 2 * math.pi); ctx.restore()
    fill_stroke(ctx, "#FFFDF5", lw=5)


def walker(ctx, x, y, s, gt, col="#5B8CFF", ph=True):
    """Simple person holding a phone."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    sw = 20 * math.sin(gt * 5)
    for d in (-1, 1):
        ctx.move_to(0, 60); ctx.line_to(d * (20 + sw * d), 170); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(16); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    rrect(ctx, -40, -40, 80, 110, 30); fill_stroke(ctx, col, lw=6)
    circle(ctx, 0, -80, 40, "#FFD9B8", lw=6)
    ctx.move_to(30, -10); ctx.line_to(70, -30); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(14); ctx.stroke()
    if ph:
        rrect(ctx, 62, -70, 30, 50, 6); fill_stroke(ctx, "#2A2438", lw=4)
    ctx.restore()


def cloud(ctx, x, y, s, col="#FFFFFF"):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for (bx, by, r) in [(-70, 10, 55), (0, -20, 75), (70, 10, 55)]:
        circle(ctx, bx, by, r, col, lw=0)
    rrect(ctx, -125, 10, 250, 60, 30); ctx.set_source_rgba(*hexc(col)); ctx.fill()
    ctx.restore()


def sun(ctx, x, y, r, gt):
    for k in range(10):
        a = k / 10 * 2 * math.pi + gt * 0.4
        ctx.move_to(x + r * 1.15 * math.cos(a), y + r * 1.15 * math.sin(a)); ctx.line_to(x + r * 1.5 * math.cos(a), y + r * 1.5 * math.sin(a))
        ctx.set_source_rgba(*hexc("#FFB84D")); ctx.set_line_width(max(6, r * 0.12)); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    circle(ctx, x, y, r, "#FFD23F", lw=max(5, r * 0.06))


def arrow(ctx, x0, y0, x1, y1, col=YEL, w=14):
    ctx.move_to(x0, y0); ctx.line_to(x1, y1); ctx.set_source_rgba(*hexc(col)); ctx.set_line_width(w); ctx.stroke()
    a = math.atan2(y1 - y0, x1 - x0)
    ctx.move_to(x1 + 30 * math.cos(a), y1 + 30 * math.sin(a))
    ctx.line_to(x1 + 30 * math.cos(a + 2.3), y1 + 30 * math.sin(a + 2.3)); ctx.line_to(x1 + 30 * math.cos(a - 2.3), y1 + 30 * math.sin(a - 2.3))
    ctx.close_path(); ctx.fill()


# stylised route (not to scale): Alabama -> Texas -> northern Mexico -> California -> Oregon -> Canada -> Juneau (Alaska)
ROUTE = [(860, 1060, "アラバマ"), (640, 1110, "テキサス"), (430, 1170, "メキシコ"), (250, 1010, "カリフォルニア"),
         (210, 830, None), (215, 680, "カナダ"), (170, 520, "アラスカ")]


def route_path(ctx, p, col=PINK, w=14, labels=True, lt=9.0):
    pts = [(x, y) for x, y, _ in ROUTE]
    segs = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    tot = sum(segs); goal = tot * clamp(p); acc = 0.0
    ctx.move_to(*pts[0]); hx, hy = pts[0]
    for i, sl in enumerate(segs):
        if acc + sl <= goal:
            ctx.line_to(*pts[i + 1]); hx, hy = pts[i + 1]; acc += sl
        else:
            f = (goal - acc) / sl
            hx = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f; hy = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f
            ctx.line_to(hx, hy); break
    ctx.set_source_rgba(*hexc(col)); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()
    if labels:
        for k, (x, y, n) in enumerate(ROUTE):
            if n and (k == 0 or k == len(ROUTE) - 1 or p > 0.95):
                circle(ctx, x, y, 16, "#FFFFFF", lw=5)
                lbl(ctx, n, x + (90 if x < 400 else -20), y + 60, 46, font="mochiy", s=pin(lt, 0.2), color="#FFFFFF")
    return hx, hy


def land(ctx):
    """Very rough North America blob behind the route."""
    ctx.move_to(120, 470); ctx.curve_to(300, 380, 700, 420, 960, 520); ctx.line_to(980, 1000); ctx.curve_to(900, 1080, 820, 1120, 700, 1080)
    ctx.curve_to(600, 1180, 520, 1260, 420, 1250); ctx.curve_to(300, 1150, 230, 1060, 190, 900); ctx.curve_to(170, 700, 140, 600, 120, 470)
    ctx.close_path(); ctx.set_source_rgba(0.55, 0.8, 0.55, 0.55); ctx.fill_preserve(); ctx.set_source_rgba(1, 1, 1, 0.8); ctx.set_line_width(6); ctx.stroke()


# ---------------------------------------------------------------- scenes
def v_hook(ctx, lt, d, gt):
    phone(ctx, CX - 250, CY + 230, 1.0 * pin(lt), gt)
    hb(ctx, CX + 200, CY - 60, 0.95 * pin(lt, 0.15), gt, tag=True, mood="wow", flip=True)
    if 0.3 < (gt % 1.0) < 0.6:
        lbl(ctx, "ピッ!", CX + 280, CY - 300, 90, s=1, color=YEL, rot=0.1)
    if not OPTS["short"]:
        lbl(ctx, "スマホが鳥を追跡!?", CX, CY - 420, 96, s=pin(lt, 0.25), rot=-0.04)


def v_hb(ctx, lt, d, gt):
    flower(ctx, CX - 260, CY + 40, 1.0 * pin(lt), gt=gt)
    hb(ctx, CX + 150, CY - 20, 1.25 * pin(lt, 0.15), gt, flip=True)
    lbl(ctx, "ハチドリ", CX, CY - 420, 120, s=pin(lt, 0.1))


def v_ruf(ctx, lt, d, gt):
    hb(ctx, CX, CY, 1.5 * pin(lt), gt)
    lbl(ctx, "アカフトオハチドリ", CX, CY - 420, 92, s=pin(lt, 0.1))
    lbl(ctx, "オレンジ色が目印", CX, CY + 330, 76, s=pin(lt, 0.3), color=YEL)


def v_wings(ctx, lt, d, gt):
    hb(ctx, CX, CY + 40, 1.4 * pin(lt), gt * 1.6)
    for k in range(4):
        ctx.new_path(); ctx.arc(CX - 30, CY - 120, 160 + k * 40, -2.4, -1.2)
        ctx.set_source_rgba(1, 1, 1, 0.5 - k * 0.1); ctx.set_line_width(8); ctx.stroke()
    lbl(ctx, "ブブブブ…", CX + 250, CY - 250, 80, s=pin(lt, 0.2), color=YEL, rot=0.1)
    lbl(ctx, "目にもとまらぬ羽ばたき", CX, CY - 430, 80, s=pin(lt, 0.1))


def v_back(ctx, lt, d, gt):
    off = 120 * math.sin(gt * 1.5)
    hb(ctx, CX + 80 - off, CY + 20, 1.2 * pin(lt), gt)
    arrow(ctx, CX + 60, CY + 280, CX - 280, CY + 280, YEL, 16)
    lbl(ctx, "うしろにも飛べる!", CX, CY - 420, 104, s=pin(lt, 0.1))


def v_america(ctx, lt, d, gt):
    land(ctx)
    hb(ctx, CX + 50, CY + 40, 0.7 * pin(lt, 0.2), gt)
    lbl(ctx, "アメリカ大陸だけ!", CX, CY - 430, 100, s=pin(lt, 0.1))
    lbl(ctx, "日本の野生には いない", CX, CY + 450, 66, s=pin(lt, 0.4), color=YEL)


def moth(ctx, x, y, s, gt):
    ctx.save(); ctx.translate(x, y + 6 * math.sin(gt * 6)); ctx.scale(s, s)
    a = math.sin(gt * 50)
    for sx in (-1, 1):
        ctx.save(); ctx.rotate(sx * (0.3 + 0.3 * a))
        ctx.move_to(0, 0); ctx.curve_to(sx * 80, -120, sx * 190, -60, sx * 170, 10); ctx.curve_to(sx * 120, 40, sx * 40, 20, 0, 0)
        fill_stroke(ctx, "#8C6B4F", lw=5); ctx.restore()
    ctx.save(); ctx.scale(0.6, 1.3); ctx.new_path(); ctx.arc(0, 30, 45, 0, 2 * math.pi); ctx.restore(); fill_stroke(ctx, "#A9876A", lw=6)
    for k in range(3):
        ctx.move_to(-25, 40 + k * 22); ctx.line_to(25, 40 + k * 22); ctx.set_source_rgba(1, 0.6, 0.2, 1); ctx.set_line_width(6); ctx.stroke()
    circle(ctx, -14, -35, 9, INK, lw=0); circle(ctx, 14, -35, 9, INK, lw=0)
    ctx.move_to(0, -40); ctx.curve_to(10, -90, 40, -110, 60, -140); ctx.set_source_rgba(0.1, 0.1, 0.2, 1); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


def v_moth(ctx, lt, d, gt):
    flower(ctx, CX + 230, CY - 20, 0.9 * pin(lt), "#B36BFF", gt)
    moth(ctx, CX - 120, CY + 60, 1.4 * pin(lt, 0.15), gt)
    lbl(ctx, "ホウジャク", CX, CY - 420, 120, s=pin(lt, 0.1))
    lbl(ctx, "じつはガのなかま", CX, CY + 400, 76, s=pin(lt, 0.4), color=YEL)


def v_coins(ctx, lt, d, gt):
    hb(ctx, CX - 230, CY - 20, 0.8 * pin(lt), gt)
    lbl(ctx, "=", CX - 20, CY, 140, s=pin(lt, 0.2))
    for k in range(4):
        coin(ctx, CX + 200 + (k % 2) * 150, CY - 90 + (k // 2) * 160, 66 * pin(lt, 0.3 + 0.1 * k), "1")
    lbl(ctx, "体重 約3.7g", CX, CY - 420, 110, s=pin(lt, 0.1))
    lbl(ctx, "1円玉 4枚くらい!", CX, CY + 330, 86, s=pin(lt, 0.7), color=YEL)


def v_rice(ctx, lt, d, gt):
    tag(ctx, CX - 220, CY - 60, 0.9 * pin(lt), gt)
    for k in range(3):
        rice(ctx, CX + 150 + k * 100, CY + 20 + (k % 2) * 30, 1.1 * pin(lt, 0.3 + 0.12 * k), 0.3 + k * 0.4)
    lbl(ctx, "≒", CX - 20, CY, 120, s=pin(lt, 0.2))
    lbl(ctx, "0.06g", CX, CY - 420, 150, s=pin(lt, 0.1), color=YEL)
    lbl(ctx, "お米2〜3つぶ分", CX, CY + 330, 86, s=pin(lt, 0.6))


def v_tagbird(ctx, lt, d, gt):
    hb(ctx, CX, CY + 20, 1.5 * pin(lt), gt, tag=True)
    lbl(ctx, "せなかに発信機", CX, CY - 420, 104, s=pin(lt, 0.1))


def v_old_new(ctx, lt, d, gt):
    vals = [("むかしの発信機", "0.28g", 6.9, "#8FA3B8"), ("今回", "0.06g", 1.6, YEL)]
    for i, (n, g, pct, c) in enumerate(vals):
        x = CX - 220 + i * 440
        h = 70 * pct * ease_out_cubic(clamp((lt - 0.2 * i) / 0.7))
        rrect(ctx, x - 100, CY + 330 - max(h, 1), 200, max(h, 1), 12); fill_stroke(ctx, c, lw=6)
        lbl(ctx, n, x, CY + 400, 54, font="mochiy", s=pin(lt, 0.1))
        lbl(ctx, g, x, CY + 330 - h - 60, 80, s=pin(lt, 0.5 + 0.2 * i), color="#FFFFFF")
        lbl(ctx, f"体重の約{pct}%", x, CY + 330 - h - 150, 52, font="mochiy", s=pin(lt, 0.6 + 0.2 * i), color=c)
    lbl(ctx, "重さくらべ", CX, CY - 430, 104, s=pin(lt, 0.1))


def v_rule(ctx, lt, d, gt):
    rrect(ctx, CX - 400, CY - 40, 800, 90, 45); fill_stroke(ctx, "#FFFFFF", lw=8)
    w = 800 * 0.3 * ease_out_cubic(clamp(lt / 0.8))
    rrect(ctx, CX - 400, CY - 40, max(w, 1), 90, 45); fill_stroke(ctx, GRN, lw=0)
    lbl(ctx, "3%", CX - 400 + 240, CY + 130, 90, s=pin(lt, 0.6), color=YEL)
    lbl(ctx, "体重の3%まで", CX, CY - 400, 110, s=pin(lt, 0.1))
    lbl(ctx, "鳥の負担をへらすルール", CX, CY + 330, 66, s=pin(lt, 0.4))


def v_glue(ctx, lt, d, gt):
    ctx.save(); ctx.translate(CX - 180, CY + 40); ctx.rotate(-0.5); ctx.scale(pin(lt), pin(lt))
    rrect(ctx, -60, -200, 120, 300, 30); fill_stroke(ctx, "#FFFFFF", lw=8)
    rrect(ctx, -30, -270, 60, 80, 10); fill_stroke(ctx, PINK, lw=6)
    ctx.restore()
    s = pin(lt, 0.3)
    ctx.save(); ctx.translate(CX + 230, CY - 20); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 120, 0.2, math.pi - 0.2); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(12); ctx.stroke()
    for k in range(9):
        a = 0.35 + k * 0.3
        ctx.move_to(120 * math.cos(a), 120 * math.sin(a)); ctx.line_to(175 * math.cos(a), 175 * math.sin(a)); ctx.set_line_width(7); ctx.stroke()
    ctx.restore()
    lbl(ctx, "まつげ用ののり!?", CX, CY - 420, 110, s=pin(lt, 0.1))


def v_nape(ctx, lt, d, gt):
    hb(ctx, CX, CY + 40, 1.4 * pin(lt), gt)
    ctx.move_to(CX + 30, CY - 160); ctx.line_to(CX + 30, CY + 60); ctx.set_source_rgba(1, 0.24, 0.5, 1); ctx.set_line_width(10); ctx.set_dash([18, 12]); ctx.stroke(); ctx.set_dash([])
    lbl(ctx, "首のうしろはダメ", CX, CY - 420, 104, s=pin(lt, 0.1))
    lbl(ctx, "羽が引っぱられちゃう", CX, CY + 340, 70, s=pin(lt, 0.4), color=YEL)


def v_solar(ctx, lt, d, gt):
    sun(ctx, CX + 270, CY - 230, 90 * pin(lt), gt)
    tag(ctx, CX - 120, CY + 10, 1.2 * pin(lt, 0.15), gt)
    for k in range(3):
        f = (gt * 0.9 + k / 3) % 1
        x = CX + 200 - 280 * f; y = CY - 170 + 150 * f
        circle(ctx, x, y, 12, YEL, lw=0)
    lbl(ctx, "電池なし!", CX, CY - 430, 120, s=pin(lt, 0.1))
    lbl(ctx, "太陽の光で動く", CX, CY + 380, 80, s=pin(lt, 0.4), color=YEL)


def v_beep(ctx, lt, d, gt):
    tag(ctx, CX, CY - 20, 1.1 * pin(lt), gt, shine=False)
    for k in range(3):
        f = ((gt / 3.0) * 3 + k / 3) % 1
        ctx.new_path(); ctx.arc(CX, CY - 60, 120 + 300 * f, 0, 2 * math.pi)
        ctx.set_source_rgba(1, 0.88, 0.3, 1 - f); ctx.set_line_width(10); ctx.stroke()
    lbl(ctx, "3秒に1回 ピッ!", CX, CY - 430, 110, s=pin(lt, 0.1))


def v_catch(ctx, lt, d, gt):
    hb(ctx, CX + 230, CY - 150, 0.7 * pin(lt), gt, tag=True, flip=True)
    walker(ctx, CX - 250, CY + 150, 1.3 * pin(lt, 0.15), gt)
    for k in range(3):
        f = (gt * 0.8 + k / 3) % 1
        ctx.new_path(); ctx.arc(CX + 230, CY - 150, 60 + 400 * f, 2.0, 3.4)
        ctx.set_source_rgba(1, 0.88, 0.3, 1 - f); ctx.set_line_width(9); ctx.stroke()
    lbl(ctx, "近くのスマホがキャッチ", CX, CY - 430, 88, s=pin(lt, 0.1))
    lbl(ctx, "約200mまで", CX, CY + 420, 80, s=pin(lt, 0.4), color=YEL)


def v_upload(ctx, lt, d, gt):
    phone(ctx, CX - 250, CY + 200, 0.9 * pin(lt), gt, waves=False)
    cloud(ctx, CX + 200, CY - 150, 1.2 * pin(lt, 0.2))
    for k in range(4):
        f = (gt * 0.7 + k / 4) % 1
        circle(ctx, CX - 200 + 380 * f, CY + 90 - 230 * f, 12, YEL, lw=0)
    lbl(ctx, "いつ・どこで", CX + 200, CY - 140, 50, font="mochiy", s=pin(lt, 0.4), color=INK)
    lbl(ctx, "場所を記録!", CX, CY - 430, 110, s=pin(lt, 0.1))


def v_dayonly(ctx, lt, d, gt):
    sun(ctx, CX - 220, CY - 30, 120 * pin(lt), gt)
    ctx.new_path(); ctx.arc(CX + 230, CY - 30, 120 * pin(lt, 0.2), 0, 2 * math.pi); ctx.set_source_rgba(0.3, 0.33, 0.55, 1); ctx.fill()
    circle(ctx, CX + 270, CY - 60, 100 * pin(lt, 0.2), "#FFF3B0", lw=0)
    lbl(ctx, "○", CX - 220, CY + 230, 120, s=pin(lt, 0.4), color=YEL)
    lbl(ctx, "×", CX + 230, CY + 230, 120, s=pin(lt, 0.5), color=PINK)
    lbl(ctx, "発信は昼だけ", CX, CY - 430, 110, s=pin(lt, 0.1))


def v_town(ctx, lt, d, gt):
    for k in range(4):
        x = CX - 380 + k * 110; h = 160 + 60 * (k % 2)
        rrect(ctx, x, CY + 200 - h * pin(lt, 0.05 * k), 90, h * pin(lt, 0.05 * k), 8); fill_stroke(ctx, "#C9D3E6", lw=5)
    for k in range(3):
        x = CX + 160 + k * 120
        ctx.move_to(x, CY + 20); ctx.line_to(x - 60, CY + 200); ctx.line_to(x + 60, CY + 200); ctx.close_path(); fill_stroke(ctx, "#2E8B57", lw=5)
    for k in range(6):
        phone(ctx, CX - 360 + (k % 3) * 140, CY - 80 + (k // 3) * 0, 0.25 * pin(lt, 0.3), gt + k, waves=False)
    lbl(ctx, "町はたくさん", CX - 230, CY + 300, 60, font="mochiy", s=pin(lt, 0.4), color=YEL)
    lbl(ctx, "森は少なめ", CX + 270, CY + 300, 60, font="mochiy", s=pin(lt, 0.5))
    lbl(ctx, "見つかりやすさ", CX, CY - 430, 104, s=pin(lt, 0.1))


def v_eleven(ctx, lt, d, gt):
    for k in range(11):
        x = CX - 400 + (k % 6) * 160; y = CY - 120 + (k // 6) * 230
        hb(ctx, x + (80 if k >= 6 else 0), y, 0.38 * pin(lt, 0.04 * k), gt + k, col=RUF if k < 4 else GRN, flip=k % 2 == 1)
    lbl(ctx, "11羽に発信機", CX, CY - 430, 110, s=pin(lt, 0.1))
    lbl(ctx, "2025年春 アラバマとフロリダ", CX, CY + 380, 62, font="mochiy", s=pin(lt, 0.4), color=YEL)


def v_route(ctx, lt, d, gt):
    land(ctx)
    hx, hy = route_path(ctx, clamp(lt / max(1.2, d * 0.8)), lt=lt)
    hb(ctx, hx, hy - 40, 0.35, gt, tag=True, flip=hy < 1000 and hx < 300)
    lbl(ctx, "38日の大旅行", CX, CY - 430, 100, s=pin(lt, 0.1))


def v_route_full(ctx, lt, d, gt):
    land(ctx)
    route_path(ctx, 1.0, lt=lt)
    x, y, _ = ROUTE[-1]
    hb(ctx, x + 40, y - 70, 0.35 * pin(lt, 0.3), gt, tag=True)
    lbl(ctx, "約6526km!", CX + 120, CY - 30, 120, s=pin(lt, 0.4), color=YEL, rot=-0.05)


v_km = bigtext("6526km", "ハチドリの最長記録", size=200)
v_38 = bigtext("38日", "で 約6526km", size=280)


def v_japan(ctx, lt, d, gt):
    # two stylised Japan archipelago bars stacked to compare lengths
    for i in range(2):
        y = CY - 80 + i * 170; w = 330 * pin(lt, 0.2 * i)
        ctx.save(); ctx.translate(CX - 330 + i * 330, y); ctx.rotate(-0.35)
        rrect(ctx, 0, -35, w, 70, 35); fill_stroke(ctx, GRN, lw=6); ctx.restore()
    lbl(ctx, "日本列島 2つ分より長い!", CX, CY + 300, 76, s=pin(lt, 0.6), color=YEL)
    lbl(ctx, "6526kmって?", CX, CY - 430, 104, s=pin(lt, 0.1))


def v_perday(ctx, lt, d, gt):
    hb(ctx, CX - 260 + 520 * clamp(lt / max(d, 1)), CY + 60, 0.7, gt, tag=True)
    ctx.move_to(CX - 420, CY + 230); ctx.line_to(CX + 420, CY + 230); ctx.set_source_rgba(1, 1, 1, 0.8); ctx.set_line_width(8); ctx.set_dash([20, 14]); ctx.stroke(); ctx.set_dash([])
    lbl(ctx, "1日 平均 約170km", CX, CY - 430, 100, s=pin(lt, 0.1), color=YEL)
    lbl(ctx, "東京→静岡くらいを毎日!", CX, CY + 340, 70, s=pin(lt, 0.4))


def v_body(ctx, lt, d, gt):
    hb(ctx, CX, CY - 20, 0.8 * pin(lt), gt)
    ctx.move_to(CX - 200, CY + 160); ctx.line_to(CX + 230, CY + 160); ctx.set_source_rgba(*hexc(YEL)); ctx.set_line_width(8); ctx.stroke()
    lbl(ctx, "体長 約8cm", CX, CY + 230, 70, font="mochiy", s=pin(lt, 0.3))
    lbl(ctx, "体の約8000万倍!", CX, CY - 430, 104, s=pin(lt, 0.5), color=YEL)


def v_straight(ctx, lt, d, gt):
    land(ctx)
    route_path(ctx, 1.0, col="#FF9EC4", w=10, labels=False)
    p = clamp(lt / 0.8)
    x0, y0, _ = ROUTE[0]; x1, y1, _ = ROUTE[-1]
    ctx.move_to(x0, y0); ctx.line_to(x0 + (x1 - x0) * p, y0 + (y1 - y0) * p)
    ctx.set_source_rgba(*hexc(YEL)); ctx.set_line_width(10); ctx.set_dash([24, 14]); ctx.stroke(); ctx.set_dash([])
    lbl(ctx, "まっすぐなら 約4730km", CX, CY - 430, 84, s=pin(lt, 0.1), color=YEL)


def v_why_west(ctx, lt, d, gt):
    land(ctx)
    route_path(ctx, 1.0, labels=False)
    for k, (x, y) in enumerate([(430, 1170), (250, 1010), (215, 680)]):
        flower(ctx, x + 40, y - 30, 0.25 * pin(lt, 0.2 + 0.1 * k), "#FF3D5A", gt)
    lbl(ctx, "西へ ぐるっと遠回り", CX, CY - 430, 92, s=pin(lt, 0.1))


def v_band(ctx, lt, d, gt):
    ctx.save(); ctx.translate(CX - 230, CY + 30); ctx.scale(pin(lt), pin(lt))
    ctx.move_to(0, -150); ctx.line_to(0, 150); ctx.set_source_rgba(*hexc("#F2A65A")); ctx.set_line_width(22); ctx.stroke()
    rrect(ctx, -34, -30, 68, 60, 12); fill_stroke(ctx, "#C9CED8", lw=6)
    ctx.restore()
    for k, (x, y) in enumerate([(CX + 120, CY + 200), (CX + 380, CY - 180)]):
        circle(ctx, x, y, 26 * pin(lt, 0.3 + 0.2 * k), PINK, lw=6)
    ctx.move_to(CX + 120, CY + 200); ctx.line_to(CX + 380, CY - 180); ctx.set_source_rgba(1, 1, 1, 0.8); ctx.set_line_width(6); ctx.set_dash([16, 12]); ctx.stroke(); ctx.set_dash([])
    lbl(ctx, "? ? ?", CX + 250, CY, 70, s=pin(lt, 0.6), color=YEL)
    lbl(ctx, "足輪だと2点だけ", CX, CY - 430, 104, s=pin(lt, 0.1))


def v_dots(ctx, lt, d, gt):
    land(ctx)
    pts = [(x, y) for x, y, _ in ROUTE]
    n = int(60 * clamp(lt / max(1.0, d * 0.7)))
    rnd = random.Random(5)
    for k in range(n):
        i = rnd.randrange(len(pts) - 1); f = rnd.random()
        x = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f + rnd.uniform(-14, 14)
        y = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f + rnd.uniform(-14, 14)
        circle(ctx, x, y, 11, PINK, lw=3)
    lbl(ctx, "点がいっぱい=道がわかる", CX, CY - 430, 80, s=pin(lt, 0.1))


v_23000 = bigtext("2万3000回", "以上 スマホなどがキャッチ", size=170)


def v_wiggle(ctx, lt, d, gt):
    p = clamp(lt / max(1.0, d * 0.8))
    ctx.move_to(CX - 380, CY + 300)
    for k in range(1, int(60 * p) + 1):
        t = k / 60
        ctx.line_to(CX - 380 + 760 * t, CY + 300 - 520 * t + 160 * math.sin(t * 14))
    ctx.set_source_rgba(*hexc("#F2A65A")); ctx.set_line_width(12); ctx.stroke()
    lbl(ctx, "くねくね旅も!", CX, CY - 430, 110, s=pin(lt, 0.1))


def v_alaska(ctx, lt, d, gt):
    # sea, glacier mountains, a boat with phones
    rrect(ctx, 60, CY + 120, 960, 300, 20); ctx.set_source_rgba(0.2, 0.5, 0.85, 0.8); ctx.fill()
    for k in range(3):
        x = 220 + k * 300
        ctx.move_to(x - 170, CY + 120); ctx.line_to(x, CY - 180 * pin(lt, 0.1 * k)); ctx.line_to(x + 170, CY + 120); ctx.close_path(); fill_stroke(ctx, "#E8F4FF", lw=6)
    bx = CX - 300 + 600 * ((gt * 0.05) % 1)
    ctx.move_to(bx - 130, CY + 200); ctx.line_to(bx + 130, CY + 200); ctx.line_to(bx + 90, CY + 270); ctx.line_to(bx - 90, CY + 270); ctx.close_path(); fill_stroke(ctx, "#FFFFFF", lw=6)
    phone(ctx, bx, CY + 140, 0.25, gt, waves=True)
    hb(ctx, CX + 260, CY - 300, 0.45 * pin(lt, 0.3), gt, tag=True, flip=True)
    lbl(ctx, "船や山の人のスマホも", CX, CY - 440, 84, s=pin(lt, 0.1))


def v_gulf(ctx, lt, d, gt):
    rrect(ctx, 60, CY - 250, 960, 600, 30); ctx.set_source_rgba(0.2, 0.5, 0.85, 0.7); ctx.fill()
    ctx.new_path(); ctx.arc(CX, CY + 600, 640, math.pi * 1.15, math.pi * 1.85); ctx.set_source_rgba(0.55, 0.8, 0.55, 0.9); ctx.set_line_width(60); ctx.stroke()
    p = clamp(lt / max(1.0, d * 0.7))
    x = CX - 380 + 760 * p
    ctx.move_to(CX - 380, CY + 40); ctx.line_to(x, CY + 40); ctx.set_source_rgba(*hexc(YEL)); ctx.set_line_width(10); ctx.set_dash([20, 12]); ctx.stroke(); ctx.set_dash([])
    hb(ctx, x, CY, 0.45, gt, tag=True)
    lbl(ctx, "海をまっすぐ横断!?", CX, CY - 430, 100, s=pin(lt, 0.1))


def v_alaska_km(ctx, lt, d, gt):
    land(ctx)
    p = clamp(lt / max(1.0, d * 0.7))
    x0, y0 = 220, 480; x1, y1 = 470, 1200
    ctx.move_to(x0, y0); ctx.line_to(x0 + (x1 - x0) * p, y0 + (y1 - y0) * p); ctx.set_source_rgba(*hexc(YEL)); ctx.set_line_width(12); ctx.stroke()
    circle(ctx, x0, y0, 18, "#FFFFFF", lw=5); circle(ctx, x1, y1, 18 * pin(lt, 0.6), PINK, lw=5)
    lbl(ctx, "アラスカ", x0 + 120, y0 + 50, 50, font="mochiy", s=pin(lt, 0.2))
    lbl(ctx, "メキシコ", x1 + 170, y1 - 20, 50, font="mochiy", s=pin(lt, 0.7))
    lbl(ctx, "少なくとも約5821km", CX + 60, CY - 120, 70, s=pin(lt, 0.6), color=YEL)
    lbl(ctx, "アラスカから南へ", CX, CY - 430, 104, s=pin(lt, 0.1))


def v_decline(ctx, lt, d, gt):
    ctx.move_to(CX - 380, CY + 320); ctx.line_to(CX - 380, CY - 260); ctx.move_to(CX - 380, CY + 320); ctx.line_to(CX + 400, CY + 320)
    ctx.set_source_rgba(1, 1, 1, 0.9); ctx.set_line_width(8); ctx.stroke()
    p = clamp(lt / 0.9)
    ctx.move_to(CX - 360, CY - 200)
    ctx.line_to(CX - 360 + 740 * p, CY - 200 + 330 * p); ctx.set_source_rgba(*hexc(PINK)); ctx.set_line_width(14); ctx.stroke()
    lbl(ctx, "約6割へった", CX + 160, CY + 220, 80, s=pin(lt, 0.8), color=YEL)
    lbl(ctx, "1990年代から", CX, CY - 430, 104, s=pin(lt, 0.1))


def v_feeder(ctx, lt, d, gt):
    ctx.save(); ctx.translate(CX - 160, CY - 40); ctx.scale(pin(lt), pin(lt))
    ctx.move_to(0, -300); ctx.line_to(0, -200); ctx.set_source_rgba(0.1, 0.1, 0.2, 1); ctx.set_line_width(6); ctx.stroke()
    rrect(ctx, -70, -200, 140, 260, 40); fill_stroke(ctx, "#FFD9E0", lw=7)
    rrect(ctx, -130, 60, 260, 70, 30); fill_stroke(ctx, "#FF3D5A", lw=7)
    for k in range(3):
        circle(ctx, -80 + k * 80, 60, 16, YEL, lw=4)
    ctx.restore()
    hb(ctx, CX + 230, CY + 30, 0.8 * pin(lt, 0.2), gt, flip=True)
    lbl(ctx, "庭のえさ台", CX, CY - 430, 110, s=pin(lt, 0.1))


def v_rest(ctx, lt, d, gt):
    land(ctx)
    route_path(ctx, 1.0, labels=False)
    for k, (x, y, _) in enumerate(ROUTE[1:-1]):
        flower(ctx, x + 30, y - 20, 0.22 * pin(lt, 0.15 * k), ["#FF3D5A", "#B36BFF", "#FFB84D"][k % 3], gt)
    lbl(ctx, "休む場所を守る", CX, CY - 430, 104, s=pin(lt, 0.1))


def v_yourphone(ctx, lt, d, gt):
    phone(ctx, CX - 150, CY + 120, 1.2 * pin(lt), gt)
    hb(ctx, CX + 250, CY - 150, 0.6 * pin(lt, 0.2), gt, tag=True, flip=True)
    lbl(ctx, "あなたのスマホも!?", CX, CY - 430, 104, s=pin(lt, 0.1), color=YEL)


def v_other_birds(ctx, lt, d, gt):
    hb(ctx, CX - 230, CY + 20, 0.6 * pin(lt), gt, col="#8C6B4F")
    hb(ctx, CX + 230, CY - 60, 0.45 * pin(lt, 0.15), gt + 1, col="#5B8CFF", flip=True)
    tag(ctx, CX, CY + 240, 0.4 * pin(lt, 0.3), gt)
    lbl(ctx, "ほかの小鳥にも?", CX, CY - 430, 104, s=pin(lt, 0.1))


def v_comment(ctx, lt, d, gt):
    hb(ctx, CX + 200, CY + 120, 0.8 * pin(lt), gt, flip=True)
    piko(ctx, CX - 280, CY + 60, gt, 0.7 * pin(lt, 0.2), "wow")
    lbl(ctx, "追いかけたい生き物は?", CX, CY - 430, 84, s=pin(lt, 0.1))


def v_hello(ctx, lt, d, gt):
    piko(ctx, CX - 220, CY + 200, gt, 1.0 * pin(lt), "smile")
    hb(ctx, CX + 240, CY + 60, 0.6 * pin(lt, 0.2), gt, flip=True)
    lbl(ctx, "またね!", CX, CY - 400, 120, s=pin(lt, 0.2))


def v_caution(ctx, lt, d, gt):
    hb(ctx, CX - 60, CY + 120, 0.9 * pin(lt), gt, tag=True)
    draw_sprite(ctx, text_sprite("!", 220, color=YEL, path=FONTS["dela"]), CX + 330, CY - 120, pin(lt, 0.2), 1)
    lbl(ctx, "ただし", CX, CY - 430, 120, s=pin(lt, 0.1))
