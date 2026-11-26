"""Visuals for the 'wild life of homes' episode (NC State, Ecology 2026). Vertical stage, CX=540, CY=760."""
import math, random
from common4 import *
from space2 import pin, CX, CY
from hera_vis import label, photo_scene, PHOTO_LAYOUT, v_question, v_longvideo

OPTS = {"short": False}
WALL = "#F6E7C8"
ROOF = "#E0585B"
FLOOR = "#B98A5E"
INK = "#1B1B3A"


def lbl(ctx, t, x, y, size=80, s=1.0, rot=0.0, font="dela", color="#FFFFFF"):
    if OPTS["short"] and font == "mochiy" and size < 70:
        return
    label(ctx, t, x, y, size, color=color, s=s, rot=rot, font=font)


def P(name, credit, title=None, box=(940, 700), **kw):
    return photo_scene(name, credit, title, box=box, **kw)


def bigtext(text, sub=None, color="#FFE14D", size=220):
    def vis(ctx, lt, d, gt):
        draw_sprite(ctx, text_sprite(text, size, color=color, hi="#FF3D7F", path=FONTS["dela"]), CX, CY - 60, pin(lt), 1, -0.04)
        if sub:
            draw_sprite(ctx, text_sprite(sub, 78, color="#FFFFFF", hi="#FFE14D", path=FONTS["mochiy"]), CX, CY + 160, pin(lt, 0.2), 1)
    return vis


# ---------------------------------------------------------------- critters (cute, simple)
def _eyes(ctx, x, y, r, gt, k=0):
    for sx in (-1, 1):
        circle(ctx, x + sx * r * 1.1, y, r, "#FFFFFF", lw=3)
        circle(ctx, x + sx * r * 1.1 + r * 0.25 * math.sin(gt * 2 + k), y + r * 0.1, r * 0.5, INK, lw=0)


def ladybug(ctx, x, y, s, gt, k=0):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(0.08 * math.sin(gt * 3 + k))
    circle(ctx, 0, -95, 52, INK, lw=6)
    ctx.save(); ctx.scale(1, 0.92); circle(ctx, 0, 0, 110, "#F28C28", lw=8); ctx.restore()
    ctx.move_to(0, -100); ctx.line_to(0, 100); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(7); ctx.stroke()
    for (dx, dy) in [(-55, -30), (55, -30), (-60, 40), (60, 40), (-25, 70), (25, 70)]:
        circle(ctx, dx, dy, 15, INK, lw=0)
    _eyes(ctx, 0, -108, 13, gt, k)
    ctx.restore()


def stinkbug(ctx, x, y, s, gt, k=0):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(0.06 * math.sin(gt * 3 + k))
    ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(7)
    for sy in (-1, 1):
        for j in range(3):
            ctx.move_to(sy * 70, -20 + j * 50); ctx.line_to(sy * 140, 10 + j * 55); ctx.stroke()
    ctx.move_to(-40, -110); ctx.line_to(-90, -190); ctx.move_to(40, -110); ctx.line_to(90, -190); ctx.stroke()
    ctx.move_to(0, -120); ctx.line_to(110, -60); ctx.line_to(95, 90); ctx.line_to(0, 150); ctx.line_to(-95, 90); ctx.line_to(-110, -60); ctx.close_path()
    fill_stroke(ctx, "#8A7A63", lw=8)
    for i in range(5):
        circle(ctx, -60 + 30 * i, 40 + 12 * math.sin(i), 6, "#5A4E40", lw=0)
    _eyes(ctx, 0, -90, 13, gt, k)
    ctx.restore()


def centipede(ctx, x, y, s, gt, k=0):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.set_source_rgba(*hexc("#C9A77A")); ctx.set_line_width(6)
    for i in range(8):
        yy = -120 + i * 34
        w = 0.25 * math.sin(gt * 10 + i)
        for sx in (-1, 1):
            ctx.move_to(0, yy); ctx.curve_to(sx * 80, yy - 20, sx * 140, yy + 10 + 30 * w, sx * 190, yy + 60 + 30 * w); ctx.stroke()
    for i in range(8):
        rrect(ctx, -30, -130 + i * 34, 60, 32, 12); fill_stroke(ctx, "#E6CFA6", lw=5)
    ctx.move_to(-10, -140); ctx.curve_to(-60, -220, -120, -240, -160, -300)
    ctx.move_to(10, -140); ctx.curve_to(60, -220, 120, -240, 160, -300); ctx.stroke()
    _eyes(ctx, 0, -140, 11, gt, k)
    ctx.restore()


def spider(ctx, x, y, s, gt, k=0, col="#3A3A55", jump=False, long=False):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y - (abs(math.sin(gt * 3 + k)) * 40 if jump else 0)); ctx.scale(s, s)
    L = 2.0 if long else 1.0
    ctx.set_source_rgba(*hexc(col)); ctx.set_line_width(9 if not long else 6); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for sx in (-1, 1):
        for j in range(4):
            a = -0.9 + j * 0.55 + 0.08 * math.sin(gt * 5 + j + k)
            kx, ky = sx * 90 * L * math.cos(a), 90 * L * math.sin(a) - 40 * L
            ctx.move_to(0, 0); ctx.line_to(kx, ky); ctx.line_to(kx + sx * 60 * L, ky + 110 * L); ctx.stroke()
    circle(ctx, 0, 70, 80 if not long else 50, col, lw=6)
    circle(ctx, 0, -20, 62, col, lw=6)
    if jump:
        for sx in (-1, 1):
            circle(ctx, sx * 24, -40, 22, "#FFFFFF", lw=0); circle(ctx, sx * 24, -38, 13, INK, lw=0)
            circle(ctx, sx * 18, -46, 5, "#FFFFFF", lw=0)
        circle(ctx, 0, 60, 18, "#FFFFFF", lw=0)
    else:
        _eyes(ctx, 0, -30, 13, gt, k)
    ctx.restore()


def mothfly(ctx, x, y, s, gt, k=0):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y + 10 * math.sin(gt * 6 + k)); ctx.scale(s, s)
    for sx in (-1, 1):
        ctx.save(); ctx.rotate(sx * (0.5 + 0.1 * math.sin(gt * 20))); ctx.scale(1, 1.4)
        circle(ctx, sx * 70, -10, 70, "#BDA98B", lw=6)
        for i in range(4):
            circle(ctx, sx * (50 + 18 * i), -10 + (i % 2) * 20, 7, "#FFFFFF", lw=0)
        ctx.restore()
    circle(ctx, 0, 30, 45, "#8B7558", lw=6)
    _eyes(ctx, 0, -10, 11, gt, k)
    ctx.restore()


def cricket(ctx, x, y, s, gt, k=0):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y - abs(math.sin(gt * 2.5 + k)) * 60); ctx.scale(s, s)
    ctx.set_source_rgba(*hexc("#8C5A2B")); ctx.set_line_width(8)
    ctx.move_to(60, 30); ctx.line_to(170, -90); ctx.line_to(220, 80); ctx.stroke()
    ctx.move_to(-60, 30); ctx.line_to(-110, 100); ctx.stroke()
    ctx.set_line_width(4); ctx.move_to(-90, -30); ctx.curve_to(-200, -200, -60, -260, 40, -300); ctx.stroke()
    ctx.save(); ctx.scale(1.4, 0.8); circle(ctx, 0, 0, 90, "#C98A4B", lw=8); ctx.restore()
    for i in range(4):
        circle(ctx, -60 + 40 * i, -10 + 10 * math.sin(i * 2), 10, "#8C5A2B", lw=0)
    _eyes(ctx, -100, -20, 12, gt, k)
    ctx.restore()


def alligator(ctx, x, y, s, gt, mood="smile"):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-330, 20); ctx.curve_to(-250, -70, 150, -80, 260, -30); ctx.line_to(420, -10 - 30 * abs(math.sin(gt * 2)))
    ctx.line_to(430, 30); ctx.line_to(260, 50); ctx.curve_to(100, 90, -200, 90, -330, 20); ctx.close_path()
    fill_stroke(ctx, "#5E9B4A", lw=10)
    ctx.move_to(-330, 20); ctx.curve_to(-420, 0, -480, 40, -560, 30); ctx.line_to(-330, 50); ctx.close_path(); fill_stroke(ctx, "#5E9B4A", lw=8)
    for i in range(7):
        circle(ctx, -200 + 60 * i, -50, 14, "#3F7A33", lw=0)
    for sx in (-150, 120):
        rrect(ctx, sx - 25, 50, 50, 70, 16); fill_stroke(ctx, "#5E9B4A", lw=7)
    for i in range(5):
        ctx.move_to(300 + 25 * i, 20); ctx.line_to(312 + 25 * i, 0); ctx.line_to(324 + 25 * i, 20); ctx.close_path(); fill_stroke(ctx, "#FFFFFF", lw=3)
    circle(ctx, 240, -70, 30, "#FFFFFF", lw=5); circle(ctx, 248, -68, 15, INK, lw=0)
    ctx.restore()


CRIT = {"lady": ladybug, "stink": stinkbug, "centi": centipede, "spider": spider, "fly": mothfly, "cricket": cricket}


# ---------------------------------------------------------------- props
def house(ctx, x, y, s, gt, cut=True, crit=None):
    """Cross-section house. crit: list of (kind, rx, ry, scale)."""
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-420, -200); ctx.line_to(0, -470); ctx.line_to(420, -200); ctx.close_path(); fill_stroke(ctx, ROOF, lw=10)
    rrect(ctx, -380, -210, 760, 560, 10); fill_stroke(ctx, WALL, lw=10)
    if cut:
        ctx.move_to(-380, 70); ctx.line_to(380, 70); ctx.set_source_rgba(*hexc(FLOOR)); ctx.set_line_width(14); ctx.stroke()
        ctx.move_to(0, -210); ctx.line_to(0, 70); ctx.set_source_rgba(*hexc("#E2CFA8")); ctx.set_line_width(10); ctx.stroke()
        rrect(ctx, -330, -150, 120, 110, 8); fill_stroke(ctx, "#9ED8F5", lw=6)
        rrect(ctx, 220, 160, 110, 190, 8); fill_stroke(ctx, "#C98A4B", lw=6)
        rrect(ctx, -320, 200, 240, 90, 20); fill_stroke(ctx, "#7FB3E8", lw=6)
    ctx.restore()
    for i, (kind, rx, ry, sc) in enumerate(crit or []):
        CRIT[kind](ctx, x + rx * s, y + ry * s, sc * s, gt, i)


def magnifier(ctx, x, y, s, gt):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(0.1 * math.sin(gt * 2))
    ctx.move_to(90, 90); ctx.line_to(220, 220); ctx.set_source_rgba(*hexc("#8C5A2B")); ctx.set_line_width(40); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.new_path(); ctx.arc(0, 0, 130, 0, 6.29); ctx.set_source_rgba(0.75, 0.92, 1, 0.45); ctx.fill_preserve()
    ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(16); ctx.stroke()
    ctx.restore()


def phone(ctx, x, y, s, gt, inner=None):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -170, -300, 340, 600, 50); fill_stroke(ctx, INK, lw=8)
    rrect(ctx, -145, -255, 290, 500, 24); fill_stroke(ctx, "#DFF3FF", lw=0)
    circle(ctx, 0, 270, 14, "#555577", lw=0)
    ctx.restore()
    if inner:
        inner(ctx, x, y - 10 * s, s * 0.9, gt)


def people(ctx, x, y, s, gt, n=7):
    cols = ["#FF8A5B", "#5BC0EB", "#9BC53D", "#FDE74C", "#C3423F", "#B07BE0", "#4FD1A5"]
    for i in range(n):
        xx = x + (i - (n - 1) / 2) * 120 * s
        yy = y + (i % 2) * 40 * s - abs(math.sin(gt * 3 + i)) * 20 * s
        sp = pin(gt, 0) if False else 1
        circle(ctx, xx, yy - 90 * s, 42 * s, "#F7D2B0", lw=5)
        rrect(ctx, xx - 50 * s, yy - 45 * s, 100 * s, 130 * s, 40 * s); fill_stroke(ctx, cols[i % 7], lw=5)


def bars(ctx, lt, items, x0=150, y0=None, w=780, title=None):
    """items: list of (text, value 0..1, color)."""
    y0 = CY - 260 if y0 is None else y0
    for i, (t, v, col) in enumerate(items):
        y = y0 + i * 150
        p = ease_out_cubic(clamp((lt - 0.15 * i) / 0.6))
        rrect(ctx, x0, y, max(30, w * v * p), 90, 20); fill_stroke(ctx, col, lw=6)
        label(ctx, t, x0 + 20 + 160, y - 40, 54, s=pin(lt, 0.15 * i), font="mochiy")


def pie(ctx, lt, parts, cx=CX, cy=CY + 40, r=300):
    a0 = -math.pi / 2
    p = ease_out_cubic(clamp(lt / 0.8))
    for (t, v, col) in parts:
        a1 = a0 + 2 * math.pi * v * p
        ctx.move_to(cx, cy); ctx.arc(cx, cy, r, a0, a1); ctx.close_path(); fill_stroke(ctx, col, lw=8)
        am = (a0 + a1) / 2
        if v > 0.08 and p > 0.9:
            label(ctx, t, cx + r * 0.6 * math.cos(am), cy + r * 0.6 * math.sin(am), 54, font="mochiy")
        a0 = a1


def map_na(ctx, x, y, s, lt):
    """Very simplified North America (US + Canada) blob with dots."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-420, -220); ctx.curve_to(-200, -330, 200, -330, 420, -240); ctx.line_to(380, -60)
    ctx.line_to(330, 60); ctx.curve_to(300, 140, 220, 160, 160, 230); ctx.line_to(60, 180); ctx.line_to(-120, 200)
    ctx.curve_to(-260, 170, -360, 100, -400, -20); ctx.close_path(); fill_stroke(ctx, "#8BD17C", lw=10)
    ctx.move_to(-400, -90); ctx.curve_to(-100, -110, 150, -100, 360, -80)
    ctx.set_source_rgba(1, 1, 1, 0.9); ctx.set_line_width(6); ctx.set_dash([16, 10]); ctx.stroke(); ctx.set_dash([])
    rnd = random.Random(4)
    n = int(70 * clamp(lt / 1.2))
    for i in range(n):
        circle(ctx, rnd.uniform(-360, 330), rnd.uniform(-240, 170), 9, "#FF3D7F", lw=0)
    ctx.restore()


# ---------------------------------------------------------------- scenes
def v_hook(ctx, lt, d, gt):
    house(ctx, CX, CY + 160, 0.95 * pin(lt), gt, crit=[("lady", -190, -110, 0.45 * pin(lt, 0.3)), ("spider", 190, -140, 0.4 * pin(lt, 0.4)),
                                                       ("centi", 120, 220, 0.4 * pin(lt, 0.5)), ("fly", -230, 150, 0.45 * pin(lt, 0.6))])
    lbl(ctx, "あなたの家にも…", CX, CY - 420, 92, s=pin(lt, 0.1))


v_2100 = bigtext("約2100種", "家の中の生き物")


def v_house_full(ctx, lt, d, gt):
    kinds = ["lady", "stink", "centi", "spider", "fly", "cricket"]
    crit = []
    rnd = random.Random(2)
    for i in range(10):
        crit.append((kinds[i % 6], rnd.uniform(-300, 300), rnd.uniform(-160, 300), 0.28 * pin(lt, 0.1 + 0.06 * i)))
    house(ctx, CX, CY + 160, 0.95 * pin(lt), gt, crit=crit)
    lbl(ctx, "家の中は生き物だらけ!", CX, CY - 420, 82, s=pin(lt, 0.2))


def v_study(ctx, lt, d, gt):
    magnifier(ctx, CX - 60, CY - 20, 1.3 * pin(lt), gt)
    ladybug(ctx, CX - 60, CY - 20, 0.6 * pin(lt, 0.3), gt)
    lbl(ctx, "家の中の生き物しらべ", CX, CY - 400, 80, s=pin(lt, 0.2))


def v_ncstate(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 60); ctx.scale(s, s)
    rrect(ctx, -380, -160, 760, 360, 12); fill_stroke(ctx, "#C9443A", lw=10)
    for i in range(5):
        rrect(ctx, -320 + i * 135, -100, 90, 120, 6); fill_stroke(ctx, "#FCE8C8", lw=5)
    ctx.move_to(-420, -160); ctx.line_to(0, -330); ctx.line_to(420, -160); ctx.close_path(); fill_stroke(ctx, "#8E2F28", lw=10)
    rrect(ctx, -60, 60, 120, 140, 8); fill_stroke(ctx, "#6B3A20", lw=6)
    ctx.restore()
    lbl(ctx, "アメリカの大学", CX, CY - 420, 90, s=pin(lt, 0.2))
    lbl(ctx, "ノースカロライナ州立大学", CX, CY + 360, 64, s=pin(lt, 0.35), font="mochiy")


def v_phone_snap(ctx, lt, d, gt):
    def inner(c, x, y, s, g):
        spider(c, x, y + 20 * s, 0.7 * s, g, jump=True)
    phone(ctx, CX, CY + 40, 1.0 * pin(lt), gt, inner if lt > 0.2 else None)
    q = clamp((lt - 0.8) / 0.3)
    if 0 < q < 1:
        ctx.rectangle(0, 0, 1080, 1920); ctx.set_source_rgba(1, 1, 1, 0.6 * (1 - q)); ctx.fill()
    lbl(ctx, "パシャ!", CX + 300, CY - 330, 100, s=pin(lt, 0.8), rot=0.1)
    lbl(ctx, "写真をアプリに", CX, CY - 420, 86, s=pin(lt, 0.2))


def v_people(ctx, lt, d, gt):
    people(ctx, CX, CY + 160, 1.1 * pin(lt), gt)
    lbl(ctx, "約3000人", CX, CY - 300, 150, s=pin(lt, 0.2))
    lbl(ctx, "みんなで調べた", CX, CY - 140, 72, s=pin(lt, 0.35), font="mochiy")


v_24000 = bigtext("2万4千件", "の記録")


def v_map(ctx, lt, d, gt):
    map_na(ctx, CX, CY + 40, 1.05 * pin(lt), lt)
    lbl(ctx, "カナダ", CX - 40, CY - 180, 64, s=pin(lt, 0.3), font="mochiy")
    lbl(ctx, "アメリカ", CX, CY + 120, 64, s=pin(lt, 0.4), font="mochiy")
    lbl(ctx, "全部の州から", CX, CY - 420, 90, s=pin(lt, 0.2))


def v_years(ctx, lt, d, gt):
    y = CY + 40
    p = ease_out_cubic(clamp(lt / 0.7))
    ctx.move_to(170, y); ctx.line_to(170 + 740 * p, y); ctx.set_source_rgba(1, 1, 1, 1); ctx.set_line_width(18); ctx.stroke()
    for i, (t, xx) in enumerate([("1996年", 170), ("2024年", 910)]):
        circle(ctx, xx, y, 30 * pin(lt, 0.2 + 0.3 * i), "#FF3D7F", lw=6)
        lbl(ctx, t, xx, y + 110, 70, s=pin(lt, 0.2 + 0.3 * i))
    lbl(ctx, "約30年分の記録", CX, CY - 300, 92, s=pin(lt, 0.4))


def v_paper(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 40); ctx.scale(s, s); ctx.rotate(-0.05)
    rrect(ctx, -300, -380, 600, 760, 20); fill_stroke(ctx, "#FFFFFF", lw=10)
    draw_sprite(ctx, text_sprite("Ecology", 80, color="#2E7D32", stroke="#FFFFFF", stroke_w=2, shadow=False, path=FONTS["dela"]), 0, -270, 1, 1)
    for i in range(8):
        ctx.move_to(-220, -150 + i * 60); ctx.line_to(220 - 60 * (i % 3), -150 + i * 60)
        ctx.set_source_rgba(*hexc("#B9C2D0")); ctx.set_line_width(14); ctx.stroke()
    ctx.restore()
    lbl(ctx, "11月19日 発表", CX, CY - 430, 86, s=pin(lt, 0.25))


def v_rank(n, kind, name):
    def vis(ctx, lt, d, gt):
        s = pin(lt)
        ctx.save(); ctx.translate(CX, CY + 160); ctx.scale(s, s)
        rrect(ctx, -260, 120, 520, 260, 20); fill_stroke(ctx, {1: "#F5C542", 2: "#C9CED6", 3: "#D9925B"}.get(n, "#7FB3E8"), lw=10)
        ctx.restore()
        draw_sprite(ctx, text_sprite(f"{n}位", 120, color="#1B1B3A", stroke="#FFFFFF", stroke_w=6, shadow=False, path=FONTS["dela"]), CX, CY + 410, s, 1)
        CRIT[kind](ctx, CX, CY + 40, 0.95 * pin(lt, 0.15), gt)
        lbl(ctx, name, CX, CY - 400, 84, s=pin(lt, 0.25))
    return vis


def v_rank_list(ctx, lt, d, gt):
    rows = ["1 ナミテントウ", "2 クサギカメムシ", "3 ゲジ", "4 ヒメマルカツオブシムシ", "5 イエユウレイグモ", "6 ヒメグモのなかま", "7 ホシチョウバエ", "8 ワシグモのなかま"]
    for i, t in enumerate(rows):
        draw_sprite(ctx, text_sprite(t, 56, color="#FFFFFF", hi="#FFE14D", path=FONTS["mochiy"]), CX, CY - 330 + i * 105, pin(lt, 0.07 * i), 1)
    lbl(ctx, "家の中ランキング", CX, CY - 470, 86, s=pin(lt))


def v_pie(ctx, lt, d, gt):
    pie(ctx, lt, [("虫 約6割", 0.6, "#F2A541"), ("クモ 約3割", 0.3, "#7B5CFF"), ("その他", 0.1, "#4FD1A5")])
    lbl(ctx, "どんな生き物?", CX, CY - 400, 92, s=pin(lt, 0.2))


def v_spiders(ctx, lt, d, gt):
    for i, (x, y, sc, j, lg) in enumerate([(CX - 280, CY - 120, 0.6, False, True), (CX + 260, CY - 160, 0.55, True, False),
                                           (CX - 160, CY + 260, 0.55, False, False), (CX + 250, CY + 250, 0.5, True, False)]):
        spider(ctx, x, y, sc * pin(lt, 0.1 * i), gt, i, col=["#3A3A55", "#222233", "#6B4A3A", "#2E2E44"][i], jump=j, long=lg)
    lbl(ctx, "クモは何百種も!", CX, CY - 430, 92, s=pin(lt, 0.2))


def v_spider_eat(ctx, lt, d, gt):
    spider(ctx, CX - 180, CY + 120, 0.9 * pin(lt), gt, jump=True)
    for i in range(3):
        mothfly(ctx, CX + 220 + 60 * math.sin(gt * 2 + i), CY - 160 + i * 140, 0.45 * pin(lt, 0.2 + 0.1 * i), gt, i)
    lbl(ctx, "虫をつかまえる", CX, CY - 430, 90, s=pin(lt, 0.2))
    lbl(ctx, "ハンター!", CX, CY + 420, 100, s=pin(lt, 0.35))


def v_worker(ctx, lt, d, gt):
    spider(ctx, CX, CY + 80, 1.1 * pin(lt), gt, jump=True)
    s = pin(lt, 0.25)
    ctx.save(); ctx.translate(CX, CY - 110); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 120, math.pi, 0); fill_stroke(ctx, "#FFD23F", lw=8)
    rrect(ctx, -150, -10, 300, 30, 10); fill_stroke(ctx, "#FFD23F", lw=6)
    ctx.restore()
    lbl(ctx, "はたらく生き物", CX, CY - 430, 92, s=pin(lt, 0.2))


def v_asia(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 360, 0, 6.29); fill_stroke(ctx, "#4FA3E0", lw=10)
    ctx.move_to(-300, -120); ctx.curve_to(-180, -260, 60, -240, 120, -120); ctx.curve_to(60, 20, -160, 80, -260, 20); ctx.close_path(); fill_stroke(ctx, "#8BD17C", lw=8)
    ctx.move_to(200, -150); ctx.curve_to(240, -120, 230, -40, 190, 20); ctx.curve_to(170, -20, 180, -100, 200, -150); fill_stroke(ctx, "#8BD17C", lw=6)
    ctx.restore()
    circle(ctx, CX + 200 * s, CY - 70 * s, 22 * pin(lt, 0.3), "#FF3D7F", lw=5)
    lbl(ctx, "日本", CX + 290, CY - 170, 70, s=pin(lt, 0.4))
    ladybug(ctx, CX - 150, CY + 330, 0.55 * pin(lt, 0.5), gt)
    stinkbug(ctx, CX + 150, CY + 330, 0.55 * pin(lt, 0.6), gt)
    lbl(ctx, "ふるさとはアジア", CX, CY - 450, 90, s=pin(lt, 0.2))


def v_ship(ctx, lt, d, gt):
    s = pin(lt)
    x = CX - 200 + 300 * clamp(lt / max(d, 1))
    ctx.rectangle(-100, CY + 150, 1300, 600); ctx.set_source_rgba(*hexc("#4FA3E0")); ctx.fill()
    ctx.save(); ctx.translate(x, CY + 120 + 10 * math.sin(gt * 2)); ctx.scale(s, s)
    ctx.move_to(-330, 0); ctx.line_to(330, 0); ctx.line_to(260, 110); ctx.line_to(-260, 110); ctx.close_path(); fill_stroke(ctx, "#E0585B", lw=10)
    for i, col in enumerate(["#F5C542", "#7FB3E8", "#9BC53D"]):
        rrect(ctx, -240 + i * 165, -120, 150, 120, 6); fill_stroke(ctx, col, lw=6)
    ctx.restore()
    stinkbug(ctx, x + 50 * s, CY - 60, 0.35 * pin(lt, 0.3), gt)
    lbl(ctx, "荷物にまぎれて", CX, CY - 400, 90, s=pin(lt, 0.2))


def v_aphid(ctx, lt, d, gt):
    ctx.move_to(200, CY + 380); ctx.curve_to(400, CY + 100, 600, CY - 100, 900, CY - 300)
    ctx.set_source_rgba(*hexc("#4E9A3A")); ctx.set_line_width(30); ctx.stroke()
    for i in range(6):
        t = i / 6
        x, y = 260 + 600 * t, CY + 300 - 600 * t
        if lt < 0.6 + 0.12 * i:
            circle(ctx, x + 30, y, 22, "#B5E27A", lw=4)
    ladybug(ctx, 260 + 600 * clamp(lt / 1.6), CY + 220 - 600 * clamp(lt / 1.6), 0.5 * pin(lt), gt)
    lbl(ctx, "アブラムシを食べる!", CX, CY - 430, 84, s=pin(lt, 0.2))


def v_winter(ctx, lt, d, gt):
    house(ctx, CX, CY + 200, 0.85 * pin(lt), gt, crit=[("lady", -260 + 60 * (i % 5), -150 + 60 * (i // 5), 0.22 * pin(lt, 0.2 + 0.04 * i)) for i in range(10)])
    rnd = random.Random(1)
    for i in range(30):
        x = rnd.uniform(0, 1080); y = (rnd.uniform(0, 1900) + gt * 120) % 1900
        circle(ctx, x, y, 8, "#FFFFFF", lw=0)
    lbl(ctx, "冬は家の中へ", CX, CY - 440, 90, s=pin(lt, 0.2))


def v_cricket(ctx, lt, d, gt):
    cricket(ctx, CX, CY + 80, 1.1 * pin(lt), gt)
    lbl(ctx, "カマドウマのなかま", CX, CY - 420, 84, s=pin(lt, 0.2))


def v_paper_eat(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX + 160, CY + 60); ctx.scale(s, s); ctx.rotate(0.08)
    rrect(ctx, -170, -220, 340, 440, 10); fill_stroke(ctx, "#FFFFFF", lw=8)
    for i in range(5):
        ctx.move_to(-120, -150 + i * 70); ctx.line_to(120, -150 + i * 70); ctx.set_source_rgba(*hexc("#B9C2D0")); ctx.set_line_width(12); ctx.stroke()
    ctx.restore()
    cricket(ctx, CX - 230, CY + 260, 0.6 * pin(lt, 0.2), gt)
    for i in range(6):
        a = gt * 2 + i
        circle(ctx, CX - 120 + 40 * math.cos(a), CY + 120 + 40 * math.sin(a), 12, "#FF3D7F", lw=3)
    lbl(ctx, "紙を分解する微生物!?", CX, CY - 430, 80, s=pin(lt, 0.2))


def v_gator(ctx, lt, d, gt):
    alligator(ctx, CX + 60, CY + 120, 0.9 * pin(lt), gt)
    lbl(ctx, "ワニ!?", CX, CY - 380, 160, s=pin(lt, 0.2), rot=-0.06)


def v_garage(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 160); ctx.scale(s, s)
    ctx.move_to(-440, -260); ctx.line_to(0, -460); ctx.line_to(440, -260); ctx.close_path(); fill_stroke(ctx, "#8899AA", lw=10)
    rrect(ctx, -400, -270, 800, 560, 6); fill_stroke(ctx, "#DDE3EA", lw=10)
    up = 0.55 * clamp((lt - 0.3) / 0.6)
    rrect(ctx, -330, -180, 660, 470 * (1 - up), 4); fill_stroke(ctx, "#B8C4D0", lw=8)
    for i in range(int(6 * (1 - up))):
        ctx.move_to(-330, -180 + 78 * (i + 1)); ctx.line_to(330, -180 + 78 * (i + 1)); ctx.set_source_rgba(*hexc("#8899AA")); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()
    if lt > 0.5:
        alligator(ctx, CX + 30, CY + 380, 0.55 * pin(lt, 0.5), gt)
    lbl(ctx, "ガレージを開けたら…", CX, CY - 450, 80, s=pin(lt, 0.15))


def v_visitor(ctx, lt, d, gt):
    house(ctx, CX - 120, CY + 200, 0.7 * pin(lt), gt, cut=False)
    alligator(ctx, CX + 300, CY + 430, 0.35 * pin(lt, 0.2), gt)
    lbl(ctx, "まよいこんだ", CX, CY - 420, 90, s=pin(lt, 0.2))
    lbl(ctx, "お客さん", CX + 260, CY + 250, 70, s=pin(lt, 0.35), font="mochiy")


def v_jungle(ctx, lt, d, gt):
    for i in range(5):
        x = 140 + i * 200
        h = 500 + 80 * math.sin(i * 1.7)
        ctx.move_to(x, CY + 420); ctx.line_to(x, CY + 420 - h * pin(lt, 0.05 * i)); ctx.set_source_rgba(*hexc("#7A5A3A")); ctx.set_line_width(36); ctx.stroke()
        circle(ctx, x, CY + 420 - h * pin(lt, 0.05 * i), 130 * pin(lt, 0.05 * i), "#3E9A4A", lw=8)
    lbl(ctx, "ジャングル", CX - 220, CY - 430, 80, s=pin(lt, 0.2))
    s = pin(lt, 0.4)
    ctx.save(); ctx.translate(CX + 260, CY - 360); ctx.scale(s, s)
    circle(ctx, 0, 0, 110, "#1F3B73", lw=8)
    circle(ctx, -20, -10, 20, "#FFFFFF", lw=0); circle(ctx, 30, 20, 12, "#FFFFFF", lw=0)
    ctx.restore()
    lbl(ctx, "深海", CX + 260, CY - 180, 70, s=pin(lt, 0.45), font="mochiy")


def v_home_unknown(ctx, lt, d, gt):
    house(ctx, CX, CY + 200, 0.85 * pin(lt), gt)
    for i, (x, y, sz) in enumerate([(CX - 200, CY + 120, 150), (CX + 180, CY + 240, 190)]):
        draw_sprite(ctx, text_sprite("?", sz, color="#FFE14D", path=FONTS["dela"]), x, y, pin(lt, 0.2 + i * 0.15), 1, 0.3 * math.sin(gt * 4 + i))
    lbl(ctx, "家の中はナゾだらけ", CX, CY - 440, 84, s=pin(lt, 0.2))


def v_dont_know(ctx, lt, d, gt):
    piko(ctx, CX - 200, CY + 220, gt, 0.9 * pin(lt), "wow")
    centipede(ctx, CX + 230, CY + 60, 0.7 * pin(lt, 0.2), gt)
    draw_sprite(ctx, text_sprite("だれ?", 120, color="#FFE14D", path=FONTS["dela"]), CX - 200, CY - 120, pin(lt, 0.3), 1, -0.1)
    lbl(ctx, "名前、知ってる?", CX, CY - 440, 90, s=pin(lt, 0.1))


def v_once(ctx, lt, d, gt):
    pie(ctx, lt, [("1回だけ", 0.52, "#FF8A5B"), ("2回以上", 0.48, "#5BC0EB")], cy=CY + 60, r=280)
    lbl(ctx, "半分は1回きり!", CX, CY - 400, 90, s=pin(lt, 0.2))


def v_unknown_id(ctx, lt, d, gt):
    pie(ctx, lt, [("わからない", 0.44, "#B07BE0"), ("わかった", 0.56, "#9BC53D")], cy=CY + 60, r=280)
    lbl(ctx, "本当はもっといる!?", CX, CY - 400, 86, s=pin(lt, 0.2))


def v_japan_home(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 180); ctx.scale(s, s)
    ctx.move_to(-460, -180); ctx.line_to(0, -420); ctx.line_to(460, -180); ctx.close_path(); fill_stroke(ctx, "#4A4A6A", lw=10)
    rrect(ctx, -400, -190, 800, 470, 6); fill_stroke(ctx, "#F4EEDD", lw=10)
    for i in range(4):
        rrect(ctx, -360 + i * 180, -140, 160, 280, 4); fill_stroke(ctx, "#FFFFFF", lw=6)
        ctx.move_to(-280 + i * 180, -140); ctx.line_to(-280 + i * 180, 140); ctx.set_source_rgba(*hexc("#C9B48A")); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()
    spider(ctx, CX + 300, CY + 30, 0.3 * pin(lt, 0.3), gt, jump=True)
    lbl(ctx, "日本の家では?", CX, CY - 440, 90, s=pin(lt, 0.2))


def v_join(ctx, lt, d, gt):
    def inner(c, x, y, s, g):
        ladybug(c, x, y, 0.55 * s, g)
    phone(ctx, CX - 170, CY + 60, 0.9 * pin(lt), gt, inner)
    piko(ctx, CX + 250, CY + 200, gt, 0.8 * pin(lt, 0.2), "smile")
    lbl(ctx, "だれでも参加できる!", CX, CY - 440, 84, s=pin(lt, 0.2))


def v_future(ctx, lt, d, gt):
    years = ["今", "10年後", "30年後"]
    for i, t in enumerate(years):
        x = CX - 330 + i * 330
        house(ctx, x, CY + 200, 0.32 * pin(lt, 0.15 * i), gt, crit=[(["lady", "spider", "cricket"][i], 0, 120, 0.7 * pin(lt, 0.2 + 0.15 * i))])
        lbl(ctx, t, x, CY + 420, 60, s=pin(lt, 0.2 + 0.15 * i))
        if i < 2:
            lbl(ctx, "→", x + 165, CY + 150, 80, s=pin(lt, 0.3 + 0.15 * i))
    lbl(ctx, "変化がわかる!", CX, CY - 400, 92, s=pin(lt, 0.2))


def v_climate(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX - 230, CY - 40); ctx.scale(s, s)
    rrect(ctx, -40, -260, 80, 420, 40); fill_stroke(ctx, "#FFFFFF", lw=8)
    circle(ctx, 0, 190, 80, "#FF3D3D", lw=8)
    h = 200 + 100 * math.sin(gt * 1.5)
    rrect(ctx, -20, 150 - h, 40, h, 20); fill_stroke(ctx, "#FF3D3D", lw=0)
    ctx.restore()
    house(ctx, CX + 200, CY + 220, 0.5 * pin(lt, 0.2), gt, crit=[("fly", 0, 100, 0.6 * pin(lt, 0.4))])
    lbl(ctx, "外の気温と関係?", CX, CY - 430, 88, s=pin(lt, 0.2))


def v_roommates(ctx, lt, d, gt):
    house(ctx, CX, CY + 180, 0.9 * pin(lt), gt, crit=[("lady", -200, -100, 0.35), ("spider", 200, -120, 0.32), ("fly", -220, 170, 0.35), ("cricket", 160, 210, 0.3)])
    piko(ctx, CX, CY - 10, gt, 0.5 * pin(lt, 0.2), "smile")
    lbl(ctx, "小さな同居人", CX, CY - 440, 96, s=pin(lt, 0.2))


def v_comment(ctx, lt, d, gt):
    for i, k in enumerate(["lady", "spider", "centi"]):
        CRIT[k](ctx, CX - 320 + i * 320, CY + 120, 0.45 * pin(lt, 0.1 * i), gt, i)
    lbl(ctx, "どれ見たことある?", CX, CY - 400, 90, s=pin(lt, 0.2))


def v_hello(ctx, lt, d, gt):
    piko(ctx, CX - 120, CY + 200, gt, 1.0 * pin(lt), "smile")
    ladybug(ctx, CX + 260, CY + 120, 0.5 * pin(lt, 0.2), gt)
    lbl(ctx, "またね!", CX, CY - 400, 120, s=pin(lt, 0.2))
