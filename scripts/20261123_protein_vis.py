"""Visuals for the 'protein from CO2 (WashU, One Earth 2026)' episode (vertical stage, CX=540, CY=760)."""
import math, random
from common4 import *
from space2 import pin, CX, CY
from space import sun
from hera_vis import label, photo_scene, PHOTO_LAYOUT, v_question, v_longvideo

FUNGUS = "#FF8A2B"
FUNGUS2 = "#FFC15A"
COPPER = "#C8743A"
GOLD = "#F2C14E"
SKY = "#8FD3FF"
GRASS = "#7DBF5A"
OPTS = {"short": False}


def lbl(ctx, t, x, y, size=80, s=1.0, rot=0.0, font="dela", color="#FFFFFF"):
    if OPTS["short"] and font == "mochiy" and size < 70:
        return
    label(ctx, t, x, y, size, color=color, s=s, rot=rot, font=font)


def P(name, credit, title=None, box=(940, 700), **kw):
    return photo_scene(name, credit, title, box=box, **kw)


# ---------------------------------------------------------------- props
def co2(ctx, x, y, s, gt=0.0, k=0, face=True):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y + 10 * math.sin(gt * 2.4 + k)); ctx.scale(s, s)
    ctx.move_to(-110, 0); ctx.line_to(110, 0); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(18); ctx.stroke()
    circle(ctx, -110, 0, 52, "#FF5A5A", lw=7)
    circle(ctx, 110, 0, 52, "#FF5A5A", lw=7)
    circle(ctx, 0, 0, 66, "#5B6B8A", lw=7)
    if face:
        for sx in (-1, 1):
            circle(ctx, sx * 20, -12, 9, "#FFFFFF", lw=0)
        ctx.new_path(); ctx.arc(0, 10, 18, 0.3, math.pi - 0.3); ctx.set_source_rgba(1, 1, 1); ctx.set_line_width(5); ctx.stroke()
    draw_sprite(ctx, text_sprite("CO2", 40, color="#FFFFFF", path=FONTS["dela"]), 0, 92, 1, 1)
    ctx.restore()


def fungus(ctx, x, y, s, gt=0.0, mood="smile", n=9):
    """Fluffy orange mold ball with a face."""
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rnd = random.Random(7)
    for k in range(n):
        a = k / n * 6.283 + 0.2 * math.sin(gt * 2 + k)
        r = 110 + 12 * math.sin(gt * 3 + k * 1.7)
        circle(ctx, r * math.cos(a), r * math.sin(a) * 0.85, 70 + rnd.random() * 20, FUNGUS2, lw=6)
    circle(ctx, 0, 0, 150, FUNGUS, lw=8)
    for sx in (-1, 1):
        circle(ctx, sx * 50, -20, 24, "#FFFFFF", lw=5)
        circle(ctx, sx * 50 + 4, -16, 11, "#1B1B3A", lw=0)
    if mood == "wow":
        circle(ctx, 0, 50, 22, "#1B1B3A", lw=0)
    else:
        ctx.new_path(); ctx.arc(0, 30, 40, 0.3, math.pi - 0.3); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(9); ctx.stroke()
    ctx.restore()


def cow(ctx, x, y, s, gt=0.0):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for lx in (-110, -50, 50, 110):
        rrect(ctx, lx - 16, 40, 32, 110, 10); fill_stroke(ctx, "#FFFFFF", lw=6)
    rrect(ctx, -170, -80, 340, 170, 70); fill_stroke(ctx, "#FFFFFF", lw=8)
    circle(ctx, -60, -20, 40, "#1B1B3A", lw=0); circle(ctx, 70, 30, 32, "#1B1B3A", lw=0)
    ctx.save(); ctx.translate(-190, -90 + 6 * math.sin(gt * 3))
    rrect(ctx, -70, -60, 130, 120, 50); fill_stroke(ctx, "#FFFFFF", lw=7)
    rrect(ctx, -80, 10, 110, 60, 28); fill_stroke(ctx, "#FFB3C7", lw=6)
    circle(ctx, -35, -15, 10, "#1B1B3A", lw=0); circle(ctx, 15, -15, 10, "#1B1B3A", lw=0)
    ctx.move_to(-60, -55); ctx.line_to(-80, -95); ctx.move_to(40, -55); ctx.line_to(60, -95)
    ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(10); ctx.stroke()
    ctx.restore(); ctx.restore()


def soybean(ctx, x, y, s, gt=0.0):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(0.15 * math.sin(gt * 2))
    ctx.move_to(0, 120); ctx.line_to(0, -40); ctx.set_source_rgba(*hexc("#3E8E3E")); ctx.set_line_width(14); ctx.stroke()
    for sx in (-1, 1):
        ctx.save(); ctx.translate(sx * 60, -60); ctx.rotate(sx * 0.5); ctx.scale(1, 0.55)
        circle(ctx, 0, 0, 70, GRASS, lw=6); ctx.restore()
    for k in range(3):
        circle(ctx, -40 + k * 40, 30, 26, "#E8D58A", lw=6)
    ctx.restore()


def factory(ctx, x, y, s, gt=0.0, smoke=True):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -220, -60, 440, 200, 10); fill_stroke(ctx, "#A9B4C2", lw=8)
    for k in range(3):
        rrect(ctx, -180 + k * 130, 0, 80, 70, 8); fill_stroke(ctx, "#FFE14D", lw=6)
    rrect(ctx, 120, -260, 70, 210, 8); fill_stroke(ctx, "#8A94A6", lw=8)
    if smoke:
        for k in range(4):
            q = (gt * 0.5 + k / 4) % 1
            circle(ctx, 155 + 40 * q, -290 - 220 * q, 40 + 50 * q, "#D0D5DD", lw=5)
    ctx.restore()


def solar(ctx, x, y, s, gt=0.0):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-200, -60); ctx.line_to(200, -60); ctx.line_to(240, 80); ctx.line_to(-240, 80); ctx.close_path()
    fill_stroke(ctx, "#2E4A9E", lw=8)
    for k in range(1, 4):
        ctx.move_to(-200 + k * 100, -60); ctx.line_to(-240 + k * 120, 80)
    ctx.move_to(-220, 10); ctx.line_to(220, 10)
    ctx.set_source_rgba(*hexc("#8FD3FF")); ctx.set_line_width(5); ctx.stroke()
    rrect(ctx, -16, 80, 32, 90, 6); fill_stroke(ctx, "#8A94A6", lw=6)
    ctx.restore()


def bolt(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(10, -80); ctx.line_to(-40, 10); ctx.line_to(0, 10); ctx.line_to(-15, 80); ctx.line_to(45, -15); ctx.line_to(5, -15); ctx.close_path()
    fill_stroke(ctx, "#FFE14D", lw=6); ctx.restore()


def tank(ctx, x, y, s, gt=0.0, fill="#8FD3FF", level=0.7, label_t=None, content=None):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -150, -200, 300, 400, 40); fill_stroke(ctx, "#FFFFFF", lw=8)
    h = 380 * level
    ctx.save(); rrect(ctx, -140, -190, 280, 380, 34); ctx.clip()
    ctx.rectangle(-150, 190 - h, 300, h); ctx.set_source_rgba(*hexc(fill, 0.85)); ctx.fill()
    for k in range(5):
        q = (gt * 0.6 + k / 5) % 1
        circle(ctx, -90 + k * 45, 180 - 360 * q * level, 10, "#FFFFFF", lw=0)
    ctx.restore()
    if content == "fungus":
        for k in range(6):
            circle(ctx, -80 + (k % 3) * 80, 100 - (k // 3) * 90, 34 + 4 * math.sin(gt * 3 + k), FUNGUS, lw=5)
    ctx.restore()
    if label_t:
        lbl(ctx, label_t, x, y + 260 * s, 58, s=s, font="mochiy")


def electrode(ctx, x, y, s, gt=0.0):
    """Copper plate with gold dots = tandem catalyst."""
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -170, -230, 340, 460, 24); fill_stroke(ctx, COPPER, lw=8)
    rnd = random.Random(3)
    for k in range(14):
        px, py = rnd.uniform(-130, 130), rnd.uniform(-190, 190)
        circle(ctx, px, py, 16 + 4 * math.sin(gt * 4 + k), GOLD, lw=4)
    ctx.restore()


def powder(ctx, x, y, s, gt=0.0):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 40, 200, 0, math.pi); ctx.close_path(); fill_stroke(ctx, "#FFFFFF", lw=8)
    ctx.new_path(); ctx.arc(0, 40, 170, math.pi, 2 * math.pi); ctx.close_path(); ctx.scale(1, 1); fill_stroke(ctx, FUNGUS2, lw=6)
    rrect(ctx, -60, -170, 120, 60, 20); fill_stroke(ctx, "#A9B4C2", lw=6)
    ctx.move_to(0, -110); ctx.line_to(0, -50); ctx.set_source_rgba(*hexc("#A9B4C2")); ctx.set_line_width(16); ctx.stroke()
    ctx.restore()


def scientist(ctx, x, y, s, gt=0.0, mood="smile"):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -110, -40, 220, 260, 60); fill_stroke(ctx, "#FFFFFF", lw=8)
    circle(ctx, 0, -130, 90, "#FFD9B0", lw=8)
    ctx.new_path(); ctx.arc(0, -150, 92, math.pi, 2 * math.pi); ctx.close_path(); fill_stroke(ctx, "#3A2A1A", lw=6)
    for sx in (-1, 1):
        circle(ctx, sx * 34, -125, 24, "#FFFFFF", lw=5); circle(ctx, sx * 34, -125, 8, "#1B1B3A", lw=0)
    if mood == "wow":
        circle(ctx, 0, -80, 14, "#1B1B3A", lw=0)
    else:
        ctx.new_path(); ctx.arc(0, -95, 24, 0.3, math.pi - 0.3); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


def bar(ctx, x, y, w, h, col, s=1.0):
    hh = h * s
    rrect(ctx, x - w / 2, y - hh, w, max(4, hh), 16); fill_stroke(ctx, col, lw=6)


def bars(ctx, lt, items, title=None, unit="", logscale=False, ymax=None, base=None):
    """items: list of (name, value, color, text)."""
    short = OPTS["short"]
    base = (CY + 180 if short else CY + 380) if base is None else base
    hmax = 400 if short else 650
    n = len(items)
    vals = [math.log10(max(1, v)) if logscale else v for (_, v, _, _) in items]
    ymax = ymax or max(vals)
    for i, ((name, v, col, txt), vv) in enumerate(zip(items, vals)):
        x = CX + (i - (n - 1) / 2) * 300
        g = ease_out_cubic(clamp((lt - 0.15 * i) / 0.7))
        h = max(14, hmax * vv / ymax)
        bar(ctx, x, base, 200, h, col, g)
        label(ctx, txt, x, base - h * g - 60, 62, s=pin(lt, 0.3 + 0.15 * i))
        label(ctx, name, x, base + 70, 60, s=pin(lt, 0.1 * i), font="mochiy")
    if title:
        lbl(ctx, title, CX, CY - (400 if short else 470), 92, s=pin(lt, 0.05))


def bigtext(text, sub=None, color="#FFE14D", size=220):
    def vis(ctx, lt, d, gt):
        draw_sprite(ctx, text_sprite(text, size, color=color, hi="#FF3D7F", path=FONTS["dela"]), CX, CY - 60, pin(lt), 1, -0.04)
        if sub:
            draw_sprite(ctx, text_sprite(sub, 78, color="#FFFFFF", hi="#FFE14D", path=FONTS["mochiy"]), CX, CY + 160, pin(lt, 0.2), 1)
    return vis


def arrow(ctx, x0, y0, x1, y1, p=1.0, col="#FFFFFF"):
    xe, ye = x0 + (x1 - x0) * p, y0 + (y1 - y0) * p
    ctx.move_to(x0, y0); ctx.line_to(xe, ye); ctx.set_source_rgba(*hexc(col)); ctx.set_line_width(18); ctx.stroke()
    if p > 0.95:
        a = math.atan2(y1 - y0, x1 - x0)
        ctx.move_to(x1, y1); ctx.line_to(x1 - 50 * math.cos(a - 0.5), y1 - 50 * math.sin(a - 0.5))
        ctx.move_to(x1, y1); ctx.line_to(x1 - 50 * math.cos(a + 0.5), y1 - 50 * math.sin(a + 0.5)); ctx.stroke()


# ---------------------------------------------------------------- scenes
def v_hook(ctx, lt, d, gt):
    co2(ctx, CX - 250, CY - 160, 0.9 * pin(lt), gt)
    arrow(ctx, CX - 100, CY - 40, CX + 80, CY + 120, ease_out_cubic(clamp((lt - 0.3) / 0.5)))
    fungus(ctx, CX + 200, CY + 260, 0.95 * pin(lt, 0.4), gt, "wow")
    lbl(ctx, "空気から…ごはん!?", CX, CY - 420, 90, s=pin(lt, 0.1))


v_7days = bigtext("7日", "空気から{たんぱく質}!", size=360)
v_7days_big = bigtext("7日", None, size=420)


def v_air(ctx, lt, d, gt):
    for k in range(5):
        co2(ctx, CX - 330 + (k % 3) * 330, CY - 200 + (k // 3) * 380, 0.7 * pin(lt, 0.08 * k), gt, k)
    lbl(ctx, "二酸化炭素", CX, CY - 450, 100, s=pin(lt, 0.1))


def v_protein(ctx, lt, d, gt):
    for i, (txt, col) in enumerate([("お肉", "#FF7A7A"), ("魚", "#8FD3FF"), ("大豆", "#E8D58A"), ("卵", "#FFF2B3")]):
        x = CX - 240 + (i % 2) * 480; y = CY - 140 + (i // 2) * 380
        circle(ctx, x, y, 140 * pin(lt, 0.1 * i), col, lw=8)
        label(ctx, txt, x, y, 76, s=pin(lt, 0.1 * i + 0.1))
    lbl(ctx, "たんぱく質", CX, CY - 450, 104, s=pin(lt, 0.05))


def v_body(ctx, lt, d, gt):
    piko(ctx, CX, CY + 160, gt, 1.2 * pin(lt), "smile")
    for i, t in enumerate(["筋肉", "皮ふ", "かみの毛"]):
        a = -2.4 + i * 1.2
        label(ctx, t, CX + 360 * math.cos(a), CY + 80 + 360 * math.sin(a), 70, s=pin(lt, 0.2 + 0.15 * i))
    lbl(ctx, "体をつくる材料", CX, CY - 460, 92, s=pin(lt, 0.1))


def v_world(ctx, lt, d, gt):
    s = pin(lt)
    circle(ctx, CX, CY + 60, 330 * s, "#4FA3FF", lw=10)
    for (a, b, r) in [(-120, -80, 110), (90, 60, 130), (-40, 160, 80)]:
        circle(ctx, CX + a * s, CY + 60 + b * s, r * s, GRASS, lw=6)
    for k in range(12):
        a = k / 12 * 6.283 + gt * 0.4
        circle(ctx, CX + 420 * math.cos(a), CY + 60 + 420 * math.sin(a), 22 * pin(lt, 0.3), "#FFE14D", lw=4)
    lbl(ctx, "人がどんどんふえる", CX, CY - 440, 88, s=pin(lt, 0.1))


def v_fao(ctx, lt, d, gt):
    bars(ctx, lt, [("2012年", 100, "#A9B4C2", "100"), ("2050年", 150, "#FF8A2B", "約150")], title="食べ物が1.5倍必要!?")


def v_cow_land(ctx, lt, d, gt):
    ctx.rectangle(60, CY + 160, 960, 300); ctx.set_source_rgba(*hexc(GRASS)); ctx.fill()
    cow(ctx, CX - 220, CY + 160, 0.8 * pin(lt), gt)
    cow(ctx, CX + 260, CY + 200, 0.65 * pin(lt, 0.15), gt + 1)
    lbl(ctx, "広い土地と水と時間", CX, CY - 400, 88, s=pin(lt, 0.2))


def v_soy(ctx, lt, d, gt):
    for k in range(5):
        soybean(ctx, CX - 400 + k * 200, CY + 160, 0.9 * pin(lt, 0.06 * k), gt + k)
    lbl(ctx, "大豆も畑が必要", CX, CY - 400, 92, s=pin(lt, 0.2))


def v_idea(ctx, lt, d, gt):
    scientist(ctx, CX - 180, CY + 220, 1.0 * pin(lt), gt)
    s = pin(lt, 0.3)
    circle(ctx, CX + 240, CY - 220, 120 * s, "#FFE14D", lw=8)
    rrect(ctx, CX + 200, CY - 110, 80, 60, 10); fill_stroke(ctx, "#A9B4C2", lw=6)
    lbl(ctx, "ひらめいた!", CX, CY - 450, 100, s=pin(lt, 0.4))


def v_washu(ctx, lt, d, gt):
    scientist(ctx, CX - 220, CY + 200, 0.9 * pin(lt), gt)
    scientist(ctx, CX + 220, CY + 200, 0.9 * pin(lt, 0.15), gt, "wow")
    lbl(ctx, "アメリカの大学", CX, CY - 400, 96, s=pin(lt, 0.1))
    label(ctx, "ワシントン大学", CX, CY - 260, 70, s=pin(lt, 0.25), font="mochiy")


def v_paper(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY); ctx.rotate(-0.05); ctx.scale(s, s)
    rrect(ctx, -300, -380, 600, 760, 20); fill_stroke(ctx, "#FFFFFF", lw=10)
    for k in range(9):
        ctx.move_to(-230, -200 + k * 60); ctx.line_to(230 - 80 * (k % 3 == 2), -200 + k * 60)
        ctx.set_source_rgba(*hexc("#A9B4C2")); ctx.set_line_width(14); ctx.stroke()
    ctx.restore()
    label(ctx, "One Earth", CX, CY - 290, 80, s=s, color="#FF3D7F")
    lbl(ctx, "11月20日 発表", CX, CY + 470, 80, s=pin(lt, 0.3))


def v_two_steps(ctx, lt, d, gt):
    electrode(ctx, CX - 260, CY + 40, 0.75 * pin(lt), gt)
    arrow(ctx, CX - 100, CY + 40, CX + 70, CY + 40, ease_out_cubic(clamp((lt - 0.4) / 0.5)))
    tank(ctx, CX + 260, CY + 40, 0.7 * pin(lt, 0.5), gt, "#FFE7B3", 0.7, content="fungus")
    label(ctx, "1 電気", CX - 260, CY - 300, 76, s=pin(lt, 0.2))
    label(ctx, "2 カビ", CX + 260, CY - 300, 76, s=pin(lt, 0.6))
    lbl(ctx, "2つのステップ", CX, CY - 460, 96, s=pin(lt, 0.05))


def v_catalyst(ctx, lt, d, gt):
    electrode(ctx, CX, CY + 60, 1.0 * pin(lt), gt)
    for k in range(3):
        co2(ctx, CX - 300 + k * 300, CY - 330, 0.45 * pin(lt, 0.1 * k + 0.2), gt, k, face=False)
    label(ctx, "銅", CX - 240, CY + 360, 80, s=pin(lt, 0.3), color=COPPER)
    label(ctx, "金", CX + 240, CY + 360, 80, s=pin(lt, 0.4), color=GOLD)
    lbl(ctx, "銅と金の板", CX, CY - 470, 96, s=pin(lt, 0.05))


def v_ethanol(ctx, lt, d, gt):
    co2(ctx, CX - 300, CY - 150, 0.6 * pin(lt), gt)
    bolt(ctx, CX - 300, CY + 70, 0.9 * pin(lt, 0.2))
    arrow(ctx, CX - 130, CY - 40, CX + 50, CY - 40, ease_out_cubic(clamp((lt - 0.3) / 0.4)))
    for i, (t, col) in enumerate([("エタノール", "#8FD3FF"), ("酢酸", "#FFE14D")]):
        y = CY - 220 + i * 330
        rrect(ctx, CX + 80, y - 90, 390, 180, 40); fill_stroke(ctx, col, lw=8)
        label(ctx, t, CX + 275, y, 64, s=pin(lt, 0.5 + 0.15 * i))
    lbl(ctx, "電気で変身!", CX, CY - 460, 96, s=pin(lt, 0.1))


def v_vinegar(ctx, lt, d, gt):
    s = pin(lt)
    rrect(ctx, CX - 110, CY - 240, 220, 520, 50); fill_stroke(ctx, "#E9F6FF", lw=8)
    rrect(ctx, CX - 50, CY - 330, 100, 100, 16); fill_stroke(ctx, "#FF3D7F", lw=6)
    label(ctx, "お酢", CX, CY + 40, 80, s=s)
    lbl(ctx, "酢酸=お酢のすっぱさ", CX, CY - 460, 80, s=pin(lt, 0.2))


def v_picky(ctx, lt, d, gt):
    fungus(ctx, CX, CY + 120, 0.95 * pin(lt), gt, "smile" if (lt % 2.4) < 1.6 else "wow")
    for i, (t, col, ok) in enumerate([("エタノール", "#8FD3FF", True), ("酢酸", "#FFE14D", True), ("ギ酸", "#A9B4C2", False)]):
        x = CX - 330 + i * 330; y = CY - 300
        rrect(ctx, x - 140, y - 60, 280, 120, 30); fill_stroke(ctx, col, lw=6)
        label(ctx, t, x, y, 50, s=pin(lt, 0.2 + 0.1 * i))
        label(ctx, "OK" if ok else "NG", x, y - 130, 90, s=pin(lt, 0.5 + 0.1 * i), color="#4CC85A" if ok else "#FF3D7F")
    lbl(ctx, "好ききらいがある", CX, CY + 450, 84, s=pin(lt, 0.3))


def v_design(ctx, lt, d, gt):
    electrode(ctx, CX - 230, CY + 80, 0.6 * pin(lt), gt)
    fungus(ctx, CX + 230, CY + 80, 0.75 * pin(lt, 0.2), gt)
    q = clamp((lt - 0.5) / 0.5)
    if q > 0:
        circle(ctx, CX, CY - 230, 90 * q, "#FF3D7F", lw=8)
        label(ctx, "♥", CX, CY - 230, 100, s=q)
    lbl(ctx, "カビに合わせて設計", CX, CY - 460, 86, s=pin(lt, 0.05))


def v_tank(ctx, lt, d, gt):
    tank(ctx, CX, CY + 40, 1.1 * pin(lt), gt, "#FFE7B3", 0.25 + 0.5 * clamp(lt / max(1, d)), content="fungus")
    lbl(ctx, "カビがぐんぐん育つ", CX, CY - 440, 88, s=pin(lt, 0.2))


def v_fungus(ctx, lt, d, gt):
    fungus(ctx, CX, CY + 60, 1.4 * pin(lt), gt)
    lbl(ctx, "オレンジ色のカビ", CX, CY - 400, 92, s=pin(lt, 0.2))


def v_fungus_name(ctx, lt, d, gt):
    fungus(ctx, CX, CY + 160, 1.1 * pin(lt), gt)
    lbl(ctx, "アカパンカビの なかま", CX, CY - 400, 80, s=pin(lt, 0.2))
    label(ctx, "ニューロスポラ・インターメディア", CX, CY - 270, 52, s=pin(lt, 0.3), font="mochiy")


def v_sheet(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY); ctx.rotate(-0.08); ctx.scale(s, s)
    ctx.move_to(-330, -160); ctx.curve_to(-100, -220, 100, -120, 330, -180); ctx.line_to(320, 180); ctx.curve_to(100, 120, -100, 220, -330, 160); ctx.close_path()
    fill_stroke(ctx, FUNGUS2, lw=10)
    rnd = random.Random(5)
    for k in range(30):
        circle(ctx, rnd.uniform(-280, 280), rnd.uniform(-130, 130), rnd.uniform(6, 14), FUNGUS, lw=0)
    ctx.restore()
    lbl(ctx, "パリパリのシート", CX, CY - 400, 92, s=pin(lt, 0.2))
    label(ctx, "こおらせて かわかす", CX, CY + 350, 66, s=pin(lt, 0.4), font="mochiy")


def v_powder(ctx, lt, d, gt):
    powder(ctx, CX, CY + 120, 1.2 * pin(lt), gt)
    lbl(ctx, "こなにする!", CX, CY - 400, 100, s=pin(lt, 0.2))


def v_flow(ctx, lt, d, gt):
    steps = [("CO2", "#5B6B8A"), ("電気", "#FFE14D"), ("カビ", FUNGUS), ("こな", FUNGUS2)]
    for i, (t, col) in enumerate(steps):
        y = CY - 330 + i * 250
        s = pin(lt, 0.25 * i)
        rrect(ctx, CX - 230, y - 80, 460, 160, 50); fill_stroke(ctx, col, lw=8)
        label(ctx, t, CX, y, 80, s=s)
        if i < 3:
            arrow(ctx, CX, y + 90, CX, y + 160, ease_out_cubic(clamp((lt - 0.25 * i - 0.2) / 0.3)), col="#FFFFFF")


def v_leaf(ctx, lt, d, gt):
    s = pin(lt)
    sun(ctx, CX + 280, CY - 330, 110 * s, gt)
    ctx.save(); ctx.translate(CX - 60, CY + 120); ctx.rotate(-0.5); ctx.scale(s, s * 0.6)
    circle(ctx, 0, 0, 260, GRASS, lw=10); ctx.restore()
    co2(ctx, CX - 330, CY - 260, 0.45 * pin(lt, 0.2), gt, face=False)
    lbl(ctx, "植物の光合成", CX, CY - 470, 92, s=pin(lt, 0.1))


def v_artificial(ctx, lt, d, gt):
    solar(ctx, CX - 220, CY - 120, 0.8 * pin(lt), gt)
    sun(ctx, CX - 380, CY - 380, 70 * pin(lt), gt)
    bolt(ctx, CX, CY - 60, 0.8 * pin(lt, 0.3))
    tank(ctx, CX + 250, CY + 200, 0.6 * pin(lt, 0.4), gt, "#FFE7B3", 0.7, content="fungus")
    lbl(ctx, "人工の光合成", CX, CY - 480, 96, s=pin(lt, 0.1))


def v_factory(ctx, lt, d, gt):
    factory(ctx, CX, CY + 200, 1.3 * pin(lt), gt)
    lbl(ctx, "工場のけむりのCO2も", CX, CY - 440, 82, s=pin(lt, 0.2))


def v_protein_pct(ctx, lt, d, gt):
    bars(ctx, lt, [("牛肉", 20.4, "#FF7A7A", "20.4%"), ("大豆", 36, "#E8D58A", "36%"), ("カビ", 48.5, FUNGUS, "48.5%")], title="たんぱく質の多さ")


def v_days(ctx, lt, d, gt):
    bars(ctx, lt, [("牛", 645, "#FF7A7A", "645日"), ("大豆", 122, "#E8D58A", "122日"), ("カビ", 7, FUNGUS, "7日")], title="できるまでの日数")


def v_calendar(ctx, lt, d, gt):
    s = pin(lt)
    rrect(ctx, CX - 330, CY - 260, 660, 620, 40); fill_stroke(ctx, "#FFFFFF", lw=10)
    rrect(ctx, CX - 330, CY - 260, 660, 130, 40); fill_stroke(ctx, "#FF3D7F", lw=10)
    q = int(7 * clamp(lt / 1.4))
    for k in range(7):
        x = CX - 255 + (k % 4) * 170; y = CY - 30 + (k // 4) * 200
        label(ctx, str(k + 1), x, y, 70, s=s, color="#1B1B3A" if k >= q else "#FF3D7F")
    lbl(ctx, "たった1週間!", CX, CY - 450, 100, s=pin(lt, 0.2))


def v_water(ctx, lt, d, gt):
    bars(ctx, lt, [("牛", 75600, "#FF7A7A", "75600L"), ("大豆", 5970, "#E8D58A", "5970L"), ("カビ", 794, FUNGUS, "794L")],
         title="使う水(たんぱく質1kg)", logscale=True)


def v_bath(ctx, lt, d, gt):
    for i, (t, n, col) in enumerate([("牛", "約378杯", "#FF7A7A"), ("カビ", "約4杯", FUNGUS)]):
        y = CY - 170 + i * 380
        rrect(ctx, CX - 420, y - 110, 520, 220, 60); fill_stroke(ctx, "#8FD3FF", lw=8)
        label(ctx, t, CX - 160, y, 80, s=pin(lt, 0.2 * i))
        label(ctx, n, CX + 290, y, 76, s=pin(lt, 0.2 * i + 0.2), color=col)
    lbl(ctx, "お風呂で何杯分?", CX, CY - 460, 92, s=pin(lt, 0.05))


def v_land(ctx, lt, d, gt):
    s = pin(lt)
    n = int(1 + 22 * clamp((lt - 0.2) / 1.2))
    for k in range(22):
        x = CX - 330 + (k % 6) * 130; y = CY - 250 + (k // 6) * 130
        rrect(ctx, x - 55, y - 55, 110, 110, 12); fill_stroke(ctx, GRASS if k < n else "#5B6B8A", lw=5)
    label(ctx, "カビ", CX + 330, CY + 270, 60, s=s)
    rrect(ctx, CX + 290, CY + 160, 80, 60, 8); fill_stroke(ctx, FUNGUS, lw=5)
    lbl(ctx, "大豆の22倍!", CX, CY - 450, 100, s=pin(lt, 0.2))


v_513 = bigtext("513倍", "牛よりも{同じ土地で}多くとれる", size=250)


def v_sun_eff(ctx, lt, d, gt):
    bars(ctx, lt, [("大豆", 0.48, "#E8D58A", "1"), ("カビ", 4.35, FUNGUS, "約9")], title="日光をむだなく使う")


def v_nutrients(ctx, lt, d, gt):
    fungus(ctx, CX, CY + 200, 0.8 * pin(lt), gt)
    for i, t in enumerate(["ベータカロテン", "ビタミンB", "よいあぶら"]):
        a = -2.6 + i * 1.1
        rrect(ctx, CX + 360 * math.cos(a) - 200, CY - 60 + 300 * math.sin(a) - 55, 400, 110, 50); fill_stroke(ctx, "#FFFFFF", lw=6)
        label(ctx, t, CX + 360 * math.cos(a), CY - 60 + 300 * math.sin(a), 52, s=pin(lt, 0.2 + 0.15 * i), color="#FF8A2B")
    lbl(ctx, "栄養もいろいろ", CX, CY - 470, 92, s=pin(lt, 0.05))


def v_carrot(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX - 150, CY + 60); ctx.rotate(0.4); ctx.scale(s, s)
    ctx.move_to(-70, -200); ctx.line_to(70, -200); ctx.line_to(0, 240); ctx.close_path(); fill_stroke(ctx, "#FF8A2B", lw=8)
    ctx.move_to(0, -200); ctx.line_to(-40, -300); ctx.move_to(0, -200); ctx.line_to(40, -300)
    ctx.set_source_rgba(*hexc("#3E8E3E")); ctx.set_line_width(18); ctx.stroke(); ctx.restore()
    fungus(ctx, CX + 230, CY + 120, 0.7 * pin(lt, 0.2), gt)
    lbl(ctx, "にんじんと同じ色のもと", CX, CY - 440, 78, s=pin(lt, 0.3))


def v_indonesia(ctx, lt, d, gt):
    s = pin(lt)
    for (x, y, r) in [(-250, 0, 120), (-60, 60, 90), (120, 30, 140), (300, 90, 80)]:
        ctx.save(); ctx.translate(CX + x * s, CY + y * s); ctx.scale(1, 0.45); circle(ctx, 0, 0, r * s, GRASS, lw=8); ctx.restore()
    lbl(ctx, "インドネシア", CX, CY - 330, 104, s=pin(lt, 0.2))
    label(ctx, "オンチョム", CX, CY + 300, 90, s=pin(lt, 0.4), color=FUNGUS)


def v_nobel(ctx, lt, d, gt):
    s = pin(lt)
    circle(ctx, CX, CY + 40, 230 * s, GOLD, lw=10)
    circle(ctx, CX, CY + 40, 170 * s, "#FFE14D", lw=6)
    label(ctx, "1958", CX, CY + 40, 90, s=s, color="#FF3D7F")
    lbl(ctx, "ノーベル賞!", CX, CY - 400, 110, s=pin(lt, 0.2))
    label(ctx, "アカパンカビの研究", CX, CY + 360, 66, s=pin(lt, 0.3), font="mochiy")


def v_gene(ctx, lt, d, gt):
    s = pin(lt)
    for k in range(14):
        y = CY - 360 + k * 55
        dx = 130 * math.sin(k * 0.6 + gt * 1.5)
        circle(ctx, CX - dx, y, 22 * s, "#FF3D7F", lw=5); circle(ctx, CX + dx, y, 22 * s, "#4FA3FF", lw=5)
    lbl(ctx, "遺伝子のしくみ", CX, CY - 470, 96, s=pin(lt, 0.1))


def v_space(ctx, lt, d, gt):
    s = pin(lt)
    rnd = random.Random(2)
    for k in range(40):
        circle(ctx, rnd.uniform(40, 1040), rnd.uniform(200, 1400), rnd.uniform(3, 7), "#FFFFFF", lw=0)
    circle(ctx, CX, CY + 80, 150 * s, "#FFFFFF", lw=10)
    rrect(ctx, CX - 90, CY + 30, 180, 100, 40); fill_stroke(ctx, "#1B1B3A", lw=6)
    rrect(ctx, CX - 130, CY + 200, 260, 220, 60); fill_stroke(ctx, "#FFFFFF", lw=8)
    lbl(ctx, "宇宙ステーションでも?", CX, CY - 400, 84, s=pin(lt, 0.2))


def v_nasa60(ctx, lt, d, gt):
    draw_sprite(ctx, text_sprite("1960年代", 170, color="#FFE14D", hi="#FF3D7F", path=FONTS["dela"]), CX, CY - 60, pin(lt), 1, -0.04)
    lbl(ctx, "宇宙で食べ物を作る研究", CX, CY + 180, 76, s=pin(lt, 0.2))


def v_quorn(ctx, lt, d, gt):
    s = pin(lt)
    rrect(ctx, CX - 330, CY - 120, 660, 360, 60); fill_stroke(ctx, "#F2E2C2", lw=10)
    for k in range(3):
        rrect(ctx, CX - 260 + k * 180, CY - 50, 150, 220, 40); fill_stroke(ctx, "#D9B27A", lw=6)
    lbl(ctx, "カビのお肉の代わり", CX, CY - 400, 82, s=pin(lt, 0.2))
    label(ctx, "イギリス 1985年〜", CX, CY + 360, 70, s=pin(lt, 0.3), font="mochiy")


def v_check(ctx, lt, d, gt):
    for i, t in enumerate(["安全?", "消化できる?", "おいしい?"]):
        y = CY - 220 + i * 230
        rrect(ctx, CX - 360, y - 80, 720, 160, 50); fill_stroke(ctx, "#FFFFFF", lw=8)
        label(ctx, t, CX, y, 76, s=pin(lt, 0.2 * i), color="#1B1B3A")
    lbl(ctx, "まだチェック中", CX, CY - 470, 96, s=pin(lt, 0.05))


def v_gold(ctx, lt, d, gt):
    s = pin(lt)
    for k in range(3):
        ctx.save(); ctx.translate(CX - 200 + k * 200, CY + 80 - k * 40); ctx.scale(s, s)
        ctx.move_to(-120, 60); ctx.line_to(120, 60); ctx.line_to(80, -40); ctx.line_to(-80, -40); ctx.close_path(); fill_stroke(ctx, GOLD, lw=8)
        ctx.restore()
    lbl(ctx, "金は高い!", CX, CY - 400, 110, s=pin(lt, 0.2))


def v_lab_small(ctx, lt, d, gt):
    tank(ctx, CX - 200, CY + 120, 0.5 * pin(lt), gt, "#FFE7B3", 0.6, content="fungus")
    factory(ctx, CX + 230, CY + 220, 0.8 * pin(lt, 0.3), gt, smoke=False)
    arrow(ctx, CX - 90, CY + 40, CX + 70, CY + 40, ease_out_cubic(clamp((lt - 0.5) / 0.5)))
    lbl(ctx, "まだ実験室サイズ", CX, CY - 400, 92, s=pin(lt, 0.1))


def v_future_food(ctx, lt, d, gt):
    s = pin(lt)
    circle(ctx, CX, CY + 120, 300 * s, "#FFFFFF", lw=10)
    circle(ctx, CX, CY + 120, 230 * s, "#F7F7F7", lw=4)
    for k, col in enumerate([FUNGUS2, "#FF7A7A", GRASS]):
        a = k * 2.1 + 0.4
        circle(ctx, CX + 110 * math.cos(a) * s, CY + 120 + 110 * math.sin(a) * s, 80 * s, col, lw=6)
    lbl(ctx, "未来のごはん", CX, CY - 400, 104, s=pin(lt, 0.2))


def v_moon_base(ctx, lt, d, gt):
    s = pin(lt)
    ctx.rectangle(40, CY + 250, 1000, 300); ctx.set_source_rgba(*hexc("#A9B4C2")); ctx.fill()
    ctx.new_path(); ctx.arc(CX, CY + 250, 230 * s, math.pi, 2 * math.pi); ctx.close_path(); fill_stroke(ctx, "#FFFFFF", lw=10)
    tank(ctx, CX, CY + 160, 0.35 * s, gt, "#FFE7B3", 0.6, content="fungus")
    circle(ctx, CX + 330, CY - 300, 110 * s, "#4FA3FF", lw=8)
    lbl(ctx, "月や火星でも?", CX, CY - 470, 96, s=pin(lt, 0.2))


def v_win(ctx, lt, d, gt):
    co2(ctx, CX - 230, CY - 120, 0.65 * pin(lt), gt)
    arrow(ctx, CX - 80, CY + 20, CX + 80, CY + 20, ease_out_cubic(clamp((lt - 0.3) / 0.4)))
    powder(ctx, CX + 240, CY + 80, 0.6 * pin(lt, 0.4), gt)
    lbl(ctx, "へらして、食べ物に!", CX, CY - 440, 86, s=pin(lt, 0.2))


def v_comment(ctx, lt, d, gt):
    fungus(ctx, CX, CY + 160, 0.9 * pin(lt), gt, "wow")
    lbl(ctx, "何を作る?", CX, CY - 380, 110, s=pin(lt, 0.2))


def v_hello(ctx, lt, d, gt):
    fungus(ctx, CX - 180, CY + 200, 0.7 * pin(lt), gt)
    piko(ctx, CX + 200, CY + 220, gt, 0.9 * pin(lt, 0.15), "smile")
    lbl(ctx, "またね!", CX, CY - 400, 120, s=pin(lt, 0.2))


def v_secret(ctx, lt, d, gt):
    fungus(ctx, CX, CY + 160, 0.8 * pin(lt), gt, "wow")
    for i, (x, y, sz) in enumerate([(CX - 300, CY - 260, 170), (CX + 300, CY - 200, 220)]):
        draw_sprite(ctx, text_sprite("?", sz, color="#FFE14D", path=FONTS["dela"]), x, y, pin(lt, 0.1 + i * 0.15), 1, 0.3 * math.sin(gt * 4 + i))
