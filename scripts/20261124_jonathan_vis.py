"""Visuals for the 'Jonathan, the 194-year-old tortoise' episode (Science Advances 2026). Vertical stage, CX=540, CY=760."""
import math, random
from common4 import *
from space2 import pin, CX, CY
from hera_vis import label, photo_scene, PHOTO_LAYOUT, v_question, v_longvideo

OPTS = {"short": False}
INK = "#1B1B3A"
SHELL = "#8C6B3E"
SHELL2 = "#B08850"
SKIN = "#9C9A7A"


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


# ---------------------------------------------------------------- characters
def tortoise(ctx, x, y, s, gt, k=0, walk=False, hat=None, mood="smile", young=False):
    """Cute giant tortoise facing right. hat: None | 'party' | 'crown'."""
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    step = math.sin(gt * 3 + k) if walk else 0.0
    # legs
    for i, lx in enumerate((-150, -60, 70, 150)):
        dy = 12 * step * (1 if i % 2 else -1)
        rrect(ctx, lx - 38, 40 + dy, 76, 110, 30); fill_stroke(ctx, SKIN, lw=8)
    # neck + head
    nod = 6 * math.sin(gt * 1.5 + k)
    ctx.move_to(170, -10); ctx.curve_to(240, -40, 250, -120, 290, -150 + nod); ctx.line_to(330, -120 + nod); ctx.curve_to(300, -60, 280, 10, 200, 50)
    ctx.close_path(); fill_stroke(ctx, SKIN, lw=8)
    ctx.save(); ctx.translate(320, -165 + nod); ctx.scale(1.25, 1.0); circle(ctx, 0, 0, 62, SKIN, lw=8); ctx.restore()
    circle(ctx, 345, -185 + nod, 15, INK, lw=0); circle(ctx, 350, -191 + nod, 5, "#FFFFFF", lw=0)
    if mood == "smile":
        ctx.new_path(); ctx.arc(355, -150 + nod, 24, 0.2, 1.4); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(6); ctx.stroke()
    else:
        circle(ctx, 360, -140 + nod, 12, INK, lw=0)
    # shell
    ctx.save(); ctx.scale(1.0, 0.82)
    ctx.new_path(); ctx.arc(0, 40, 230, math.pi, 2 * math.pi); ctx.close_path(); fill_stroke(ctx, SHELL2 if young else SHELL, lw=10)
    ctx.restore()
    rrect(ctx, -250, 20, 500, 46, 23); fill_stroke(ctx, "#6E5230", lw=8)
    for (px, py, r) in [(-120, -60, 55), (0, -110, 60), (120, -60, 55), (-60, -20, 40), (60, -20, 40)]:
        circle(ctx, px, py, r, "#A47E48" if not young else "#C9A060", lw=6)
    if hat == "party":
        ctx.move_to(270, -215 + nod); ctx.line_to(320, -330 + nod); ctx.line_to(370, -215 + nod); ctx.close_path(); fill_stroke(ctx, "#FF3D7F", lw=6)
        circle(ctx, 320, -335 + nod, 16, "#FFE14D", lw=4)
    elif hat == "crown":
        ctx.move_to(270, -215 + nod); ctx.line_to(280, -290 + nod); ctx.line_to(305, -245 + nod); ctx.line_to(320, -300 + nod)
        ctx.line_to(335, -245 + nod); ctx.line_to(360, -290 + nod); ctx.line_to(370, -215 + nod); ctx.close_path(); fill_stroke(ctx, "#FFD23F", lw=6)
    ctx.restore()


def dna(ctx, x, y, s, gt, n=9, tags=0, tagcol="#FF3D7F", messy=0.0):
    """Vertical DNA ladder. tags: number of little 'switch' markers. messy: 0..1 how scattered they are."""
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rnd = random.Random(7)
    for i in range(n * 4):
        t = i / (n * 4 - 1)
        yy = -380 + 760 * t
        a = t * 6 * math.pi + gt * 1.2
        x1, x2 = 120 * math.sin(a), -120 * math.sin(a)
        if i % 4 == 0:
            ctx.move_to(x1, yy); ctx.line_to(x2, yy); ctx.set_source_rgba(*hexc("#FFFFFF")); ctx.set_line_width(8); ctx.stroke()
        circle(ctx, x1, yy, 14, "#4FA3E0", lw=0); circle(ctx, x2, yy, 14, "#FFB84D", lw=0)
    for j in range(tags):
        t = (j + 0.5) / tags
        yy = -380 + 760 * t + messy * rnd.uniform(-60, 60)
        xx = 170 + messy * rnd.uniform(-80, 120)
        rrect(ctx, xx - 30, yy - 22, 60, 44, 10); fill_stroke(ctx, tagcol if rnd.random() > messy * 0.5 else "#B07BE0", lw=5)
    ctx.restore()


def island(ctx, x, y, s, gt, label_t=None):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-260, 40); ctx.curve_to(-220, -120, -60, -200, 40, -170); ctx.curve_to(160, -150, 260, -60, 270, 40); ctx.close_path()
    fill_stroke(ctx, "#6FBF5A", lw=10)
    ctx.move_to(-60, -150); ctx.line_to(20, -250); ctx.line_to(90, -150); ctx.close_path(); fill_stroke(ctx, "#5A8F4A", lw=8)
    ctx.restore()


def sea(ctx, gt, top=CY + 180):
    ctx.rectangle(-100, top, 1300, 1200); ctx.set_source_rgba(*hexc("#3D8FD6")); ctx.fill()
    for i in range(8):
        x = (i * 170 + gt * 40) % 1200 - 60
        ctx.new_path(); ctx.arc(x, top + 60 + (i % 2) * 70, 40, math.pi, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.7); ctx.set_line_width(6); ctx.stroke()


def mansion(ctx, x, y, s):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -380, -200, 760, 340, 6); fill_stroke(ctx, "#F4F1E6", lw=10)
    ctx.move_to(-420, -200); ctx.line_to(0, -330); ctx.line_to(420, -200); ctx.close_path(); fill_stroke(ctx, "#7A8A99", lw=10)
    for r in range(2):
        for i in range(6):
            rrect(ctx, -330 + i * 115, -160 + r * 150, 70, 100, 4); fill_stroke(ctx, "#9ED8F5", lw=5)
    ctx.restore()
    ctx.rectangle(-100, y + 140 * s, 1300, 700); ctx.set_source_rgba(*hexc("#7CC36A")); ctx.fill()


# ---------------------------------------------------------------- scenes
def v_hook(ctx, lt, d, gt):
    tortoise(ctx, CX - 60, CY + 200, 1.15 * pin(lt), gt, hat="party")
    lbl(ctx, "194才!?", CX, CY - 380, 170, s=pin(lt, 0.15), rot=-0.05)


v_194 = bigtext("194才", "世界一長生きの陸の動物", size=230)
v_194_big = bigtext("194才", None, size=360)


def v_jonathan(ctx, lt, d, gt):
    mansion(ctx, CX, CY - 80, 0.75 * pin(lt))
    tortoise(ctx, CX - 40, CY + 360, 0.85 * pin(lt, 0.2), gt, walk=True)
    lbl(ctx, "ジョナサン", CX, CY - 440, 110, s=pin(lt, 0.1))


def v_secret(ctx, lt, d, gt):
    dna(ctx, CX + 230, CY + 60, 0.75 * pin(lt), gt, tags=6)
    tortoise(ctx, CX - 200, CY + 280, 0.6 * pin(lt, 0.2), gt)
    draw_sprite(ctx, text_sprite("?", 200, color="#FFE14D", path=FONTS["dela"]), CX - 180, CY - 140, pin(lt, 0.3), 1, 0.2 * math.sin(gt * 3))
    lbl(ctx, "長生きのひみつ", CX, CY - 440, 96, s=pin(lt, 0.1))


def v_timeline(ctx, lt, d, gt):
    y = CY + 40
    p = ease_out_cubic(clamp(lt / 0.8))
    ctx.move_to(120, y); ctx.line_to(120 + 840 * p, y); ctx.set_source_rgba(1, 1, 1, 1); ctx.set_line_width(16); ctx.stroke()
    for i, (t, xx, sub) in enumerate([("1832年", 140, "生まれる"), ("1882年", 360, "島へ"), ("2026年", 940, "いま")]):
        circle(ctx, xx, y, 28 * pin(lt, 0.2 + 0.25 * i), "#FF3D7F", lw=6)
        lbl(ctx, t, xx, y - 100, 56, s=pin(lt, 0.2 + 0.25 * i))
        lbl(ctx, sub, xx, y + 100, 54, s=pin(lt, 0.3 + 0.25 * i), font="mochiy")
    tortoise(ctx, 120 + 820 * p, y + 330, 0.4 * pin(lt), gt, walk=True)
    lbl(ctx, "194年の旅", CX, CY - 400, 100, s=pin(lt, 0.1))


def v_map(ctx, lt, d, gt):
    sea(ctx, gt, top=-100)
    s = pin(lt)
    # Africa blob
    ctx.save(); ctx.translate(CX, CY); ctx.scale(s, s)
    ctx.move_to(-120, -420); ctx.curve_to(120, -460, 260, -360, 300, -200); ctx.curve_to(360, -60, 240, 80, 160, 300)
    ctx.curve_to(100, 420, 0, 430, -30, 300); ctx.curve_to(-80, 120, -260, 60, -300, -120); ctx.curve_to(-320, -300, -240, -400, -120, -420)
    ctx.close_path(); fill_stroke(ctx, "#E9C46A", lw=8)
    ctx.restore()
    # Seychelles (right) and St Helena (left)
    sx, sy = CX + 420, CY - 120
    hx, hy = CX - 400, CY + 160
    circle(ctx, sx, sy, 22 * pin(lt, 0.2), "#FF3D7F", lw=5)
    circle(ctx, hx, hy, 22 * pin(lt, 0.3), "#FFE14D", lw=5)
    lbl(ctx, "セーシェル", sx - 60, sy - 80, 54, s=pin(lt, 0.25))
    lbl(ctx, "セントヘレナ島", hx + 110, hy + 80, 54, s=pin(lt, 0.35))
    q = clamp((lt - 0.5) / 1.2)
    if q > 0:
        ctx.move_to(sx, sy); ctx.curve_to(sx, sy + 700, hx + 300, hy + 400, hx + (sx - hx) * 0 , hy)
        ctx.set_source_rgba(1, 1, 1, 0.9); ctx.set_line_width(8); ctx.set_dash([20, 14]); ctx.stroke(); ctx.set_dash([])
    lbl(ctx, "はるばる船で", CX, CY - 460, 92, s=pin(lt, 0.1))


def v_island(ctx, lt, d, gt):
    sea(ctx, gt, top=CY + 60)
    island(ctx, CX, CY + 80, 1.3 * pin(lt), gt)
    tortoise(ctx, CX + 20, CY - 40, 0.28 * pin(lt, 0.3), gt)
    lbl(ctx, "大西洋のまん中の島", CX, CY - 430, 84, s=pin(lt, 0.1))


def v_far(ctx, lt, d, gt):
    sea(ctx, gt, top=CY + 120)
    island(ctx, CX, CY + 140, 0.6 * pin(lt), gt)
    for i, (t, x) in enumerate([("←2000km→", CX)]):
        lbl(ctx, "アフリカまで約2000km", CX, CY - 200, 70, s=pin(lt, 0.2))
    lbl(ctx, "ものすごく遠い島", CX, CY - 430, 90, s=pin(lt, 0.1))


def v_gift(ctx, lt, d, gt):
    tortoise(ctx, CX - 80, CY + 240, 0.95 * pin(lt), gt)
    s = pin(lt, 0.3)
    ctx.save(); ctx.translate(CX + 300, CY - 120); ctx.scale(s, s); ctx.rotate(0.1)
    rrect(ctx, -110, -90, 220, 180, 14); fill_stroke(ctx, "#FF3D7F", lw=8)
    ctx.rectangle(-18, -90, 36, 180); ctx.set_source_rgba(*hexc("#FFE14D")); ctx.fill()
    ctx.restore()
    lbl(ctx, "おくりもの", CX, CY - 440, 110, s=pin(lt, 0.1))


def v_governor(ctx, lt, d, gt):
    mansion(ctx, CX, CY + 20, 0.9 * pin(lt))
    lbl(ctx, "島の知事の家", CX, CY - 430, 100, s=pin(lt, 0.1))
    lbl(ctx, "プランテーション・ハウス", CX, CY + 400, 64, s=pin(lt, 0.3), font="mochiy")


def v_grownup(ctx, lt, d, gt):
    tortoise(ctx, CX - 40, CY + 160, 1.1 * pin(lt), gt)
    lbl(ctx, "すでにおとな!", CX, CY - 420, 110, s=pin(lt, 0.15))
    lbl(ctx, "少なくとも50才", CX, CY + 430, 72, s=pin(lt, 0.3), font="mochiy")


def v_edo(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 120); ctx.scale(s, s)
    ctx.move_to(-360, -60); ctx.line_to(0, -260); ctx.line_to(360, -60); ctx.close_path(); fill_stroke(ctx, "#4A4A6A", lw=10)
    rrect(ctx, -300, -70, 600, 330, 6); fill_stroke(ctx, "#F4EEDD", lw=10)
    for i in range(3):
        rrect(ctx, -260 + i * 180, -30, 160, 250, 4); fill_stroke(ctx, "#FFFFFF", lw=6)
    ctx.restore()
    lbl(ctx, "日本は江戸時代", CX, CY - 430, 100, s=pin(lt, 0.1))


def v_camera(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 40); ctx.scale(s, s)
    rrect(ctx, -260, -170, 520, 340, 20); fill_stroke(ctx, "#6B4A2B", lw=10)
    circle(ctx, 0, 0, 120, "#333344", lw=10); circle(ctx, 0, 0, 70, "#7FB3E8", lw=6)
    ctx.move_to(-200, 170); ctx.line_to(-260, 420); ctx.move_to(200, 170); ctx.line_to(260, 420); ctx.move_to(0, 170); ctx.line_to(0, 440)
    ctx.set_source_rgba(*hexc("#6B4A2B")); ctx.set_line_width(14); ctx.stroke()
    ctx.restore()
    lbl(ctx, "写真より先輩!", CX, CY - 430, 104, s=pin(lt, 0.15))


def v_famous(ctx, lt, d, gt):
    for i, (t, col) in enumerate([("ダーウィン", "#5BC0EB"), ("ヴィクトリア女王", "#C3423F")]):
        x = CX - 230 + i * 460
        circle(ctx, x, CY - 60, 120 * pin(lt, 0.15 * i), "#F7D2B0", lw=8)
        rrect(ctx, x - 130, CY + 60, 260, 260, 60); fill_stroke(ctx, col, lw=8)
        lbl(ctx, t, x, CY + 400, 56, s=pin(lt, 0.2 + 0.15 * i))
    lbl(ctx, "同じ時代を生きた", CX, CY - 430, 96, s=pin(lt, 0.1))


def v_coin(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 20); ctx.scale(s * abs(math.cos(gt * 1.2)) + 0.05, s)
    circle(ctx, 0, 0, 280, "#D9A441", lw=14); circle(ctx, 0, 0, 230, "#E8BC5A", lw=6)
    ctx.restore()
    tortoise(ctx, CX - 30, CY + 70, 0.5 * s * (abs(math.cos(gt * 1.2)) > 0.3), gt)
    lbl(ctx, "5ペンス玉", CX, CY - 430, 110, s=pin(lt, 0.1))


def v_aldabra(ctx, lt, d, gt):
    for i in range(4):
        tortoise(ctx, CX - 260 + (i % 2) * 460, CY - 80 + (i // 2) * 420, 0.5 * pin(lt, 0.1 * i), gt, k=i, walk=True)
    lbl(ctx, "アルダブラゾウガメ", CX, CY - 450, 86, s=pin(lt, 0.1))


def v_weight(ctx, lt, d, gt):
    tortoise(ctx, CX - 160, CY + 120, 0.8 * pin(lt), gt)
    for i in range(4):
        x = CX + 220 + (i % 2) * 120; y = CY + 260 - (i // 2) * 200
        circle(ctx, x, y - 90, 40 * pin(lt, 0.2 + 0.1 * i), "#F7D2B0", lw=5)
        rrect(ctx, x - 45, y - 50, 90, 120, 30); fill_stroke(ctx, "#5BC0EB", lw=5)
    lbl(ctx, "最大300kgほど", CX, CY - 430, 100, s=pin(lt, 0.1))


def v_slow(ctx, lt, d, gt):
    tortoise(ctx, CX - 300 + 80 * clamp(lt / max(d, 1)), CY + 200, 0.8 * pin(lt), gt, walk=True)
    lbl(ctx, "のんびり", CX, CY - 400, 130, s=pin(lt, 0.1))


def v_gene_switch(ctx, lt, d, gt):
    dna(ctx, CX - 180, CY + 60, 0.85 * pin(lt), gt, tags=6)
    for i in range(3):
        y = CY - 200 + i * 220
        on = (i + int(gt)) % 2 == 0
        rrect(ctx, CX + 160, y - 50, 220, 100, 50); fill_stroke(ctx, "#4FD1A5" if on else "#888899", lw=6)
        circle(ctx, CX + (330 if on else 210), y, 40, "#FFFFFF", lw=5)
    lbl(ctx, "遺伝子のスイッチ", CX, CY - 450, 96, s=pin(lt, 0.1))


def v_sticky(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 40); ctx.scale(s, s); ctx.rotate(-0.04)
    rrect(ctx, -300, -380, 600, 760, 20); fill_stroke(ctx, "#FFFFFF", lw=10)
    for i in range(9):
        ctx.move_to(-230, -300 + i * 75); ctx.line_to(230 - 50 * (i % 3), -300 + i * 75)
        ctx.set_source_rgba(*hexc("#B9C2D0")); ctx.set_line_width(14); ctx.stroke()
    for i, (yy, col) in enumerate([(-260, "#FF3D7F"), (-40, "#FFD23F"), (190, "#4FD1A5")]):
        rrect(ctx, 220, yy, 120, 80, 8); fill_stroke(ctx, col, lw=5)
    ctx.restore()
    lbl(ctx, "体の設計図に「ふせん」", CX, CY - 450, 80, s=pin(lt, 0.1))


def v_messy(ctx, lt, d, gt):
    dna(ctx, CX - 230, CY + 60, 0.7 * pin(lt), gt, tags=7, messy=0.0)
    dna(ctx, CX + 200, CY + 60, 0.7 * pin(lt, 0.15), gt, tags=7, messy=1.0)
    lbl(ctx, "わかい", CX - 230, CY + 420, 70, s=pin(lt, 0.2))
    lbl(ctx, "年をとると…", CX + 200, CY + 420, 70, s=pin(lt, 0.3))
    lbl(ctx, "ふせんがバラバラに", CX, CY - 450, 86, s=pin(lt, 0.1))


def v_compare5(ctx, lt, d, gt):
    tortoise(ctx, CX, CY - 180, 0.55 * pin(lt), gt, hat="crown")
    lbl(ctx, "ジョナサン", CX, CY - 420, 74, s=pin(lt, 0.1))
    for i in range(4):
        x = CX - 360 + i * 240
        tortoise(ctx, x, CY + 300, (0.22 + 0.05 * i) * pin(lt, 0.2 + 0.1 * i), gt, k=i, young=(i < 2))
    lbl(ctx, "ほかの4ひき", CX, CY + 470, 70, s=pin(lt, 0.4))


def v_cheek(ctx, lt, d, gt):
    tortoise(ctx, CX - 160, CY + 220, 0.9 * pin(lt), gt, mood="open")
    s = pin(lt, 0.3)
    ctx.save(); ctx.translate(CX + 280, CY - 100); ctx.scale(s, s); ctx.rotate(-0.6)
    rrect(ctx, -12, -160, 24, 320, 12); fill_stroke(ctx, "#FFFFFF", lw=5)
    circle(ctx, 0, -160, 30, "#F4F4F4", lw=5)
    ctx.restore()
    lbl(ctx, "ほっぺの内側を", CX, CY - 450, 96, s=pin(lt, 0.1))
    lbl(ctx, "こすりとる", CX, CY - 320, 80, s=pin(lt, 0.2), font="mochiy")


def v_food_trick(ctx, lt, d, gt):
    tortoise(ctx, CX - 160, CY + 220, 0.9 * pin(lt), gt, mood="open")
    for i, col in enumerate(["#FF7A3D", "#9BC53D", "#FFD23F"]):
        circle(ctx, CX + 260 + 40 * math.sin(gt * 3 + i), CY - 120 + i * 100, 50 * pin(lt, 0.2 + 0.1 * i), col, lw=6)
    lbl(ctx, "ごはんで「あーん」", CX, CY - 450, 92, s=pin(lt, 0.1))


def v_287(ctx, lt, d, gt):
    draw_sprite(ctx, text_sprite("287", 300, color="#FFE14D", hi="#FF3D7F", path=FONTS["dela"]), CX, CY - 80, pin(lt), 1, -0.04)
    draw_sprite(ctx, text_sprite("ジョナサンだけの遺伝子のちがい", 64, color="#FFFFFF", path=FONTS["mochiy"]), CX, CY + 160, pin(lt, 0.2), 1)


def v_repair(ctx, lt, d, gt):
    dna(ctx, CX - 160, CY + 60, 0.8 * pin(lt), gt, tags=0)
    s = pin(lt, 0.25)
    ctx.save(); ctx.translate(CX + 250, CY - 20); ctx.scale(s, s); ctx.rotate(0.4 * math.sin(gt * 3))
    rrect(ctx, -30, -40, 60, 260, 20); fill_stroke(ctx, "#C9CED6", lw=8)
    ctx.move_to(-80, -60); ctx.line_to(-80, -170); ctx.line_to(-30, -120); ctx.line_to(30, -120); ctx.line_to(80, -170); ctx.line_to(80, -60); ctx.close_path()
    fill_stroke(ctx, "#C9CED6", lw=8)
    ctx.restore()
    lbl(ctx, "DNAの修理", CX, CY - 450, 110, s=pin(lt, 0.1))


def v_energy(ctx, lt, d, gt):
    for i in range(5):
        a = gt * 1.5 + i * 1.256
        x, y = CX + 260 * math.cos(a), CY + 40 + 260 * math.sin(a)
        ctx.save(); ctx.translate(x, y); ctx.scale(pin(lt, 0.1 * i), pin(lt, 0.1 * i))
        ctx.move_to(-20, -60); ctx.line_to(30, -10); ctx.line_to(0, -10); ctx.line_to(20, 60); ctx.line_to(-30, 0); ctx.line_to(0, 0); ctx.close_path()
        fill_stroke(ctx, "#FFE14D", lw=5); ctx.restore()
    tortoise(ctx, CX - 30, CY + 100, 0.5 * pin(lt), gt)
    lbl(ctx, "エネルギーづくり", CX, CY - 450, 96, s=pin(lt, 0.1))


def v_stable(ctx, lt, d, gt):
    dna(ctx, CX, CY + 60, 0.85 * pin(lt), gt, tags=7)
    lbl(ctx, "ずっと安定!", CX, CY - 450, 120, s=pin(lt, 0.15))
    lbl(ctx, "約200年", CX + 300, CY + 380, 80, s=pin(lt, 0.3), rot=0.1)


def v_272(ctx, lt, d, gt):
    draw_sprite(ctx, text_sprite("272か所", 230, color="#FFE14D", hi="#FF3D7F", path=FONTS["dela"]), CX, CY - 80, pin(lt), 1, -0.04)
    draw_sprite(ctx, text_sprite("わかいカメと同じまま!", 70, color="#FFFFFF", path=FONTS["mochiy"]), CX, CY + 160, pin(lt, 0.2), 1)


def v_friends(ctx, lt, d, gt):
    items = [("クラゲ", "#B07BE0"), ("ハダカデバネズミ", "#F7A8B8"), ("ホッキョククジラ", "#5BC0EB")]
    for i, (t, col) in enumerate(items):
        y = CY - 220 + i * 260
        circle(ctx, CX - 300, y, 90 * pin(lt, 0.15 * i), col, lw=8)
        lbl(ctx, t, CX + 90, y, 66, s=pin(lt, 0.15 * i + 0.1))
    lbl(ctx, "長生き動物のなかま", CX, CY - 470, 86, s=pin(lt, 0.1))


def v_caution(ctx, lt, d, gt):
    tortoise(ctx, CX, CY + 220, 0.75 * pin(lt), gt)
    lbl(ctx, "でも注意!", CX, CY - 440, 120, s=pin(lt, 0.1), color="#FFE14D")
    lbl(ctx, "調べたのは5ひきだけ", CX, CY - 260, 74, s=pin(lt, 0.25))


def v_human(ctx, lt, d, gt):
    circle(ctx, CX - 220, CY - 40, 110 * pin(lt), "#F7D2B0", lw=8)
    rrect(ctx, CX - 340, CY + 70, 240, 280, 60); fill_stroke(ctx, "#5BC0EB", lw=8)
    tortoise(ctx, CX + 220, CY + 220, 0.5 * pin(lt, 0.2), gt)
    lbl(ctx, "人間にも役立つ?", CX, CY - 440, 100, s=pin(lt, 0.1))
    lbl(ctx, "研究はこれから", CX, CY + 450, 70, s=pin(lt, 0.3), font="mochiy")


def v_tea(ctx, lt, d, gt):
    tortoise(ctx, CX - 130, CY + 230, 0.85 * pin(lt), gt)
    for i, col in enumerate(["#9BC53D", "#FF7A3D", "#FF3D7F", "#FFD23F"]):
        circle(ctx, CX + 260 + (i % 2) * 110, CY - 60 + (i // 2) * 120, 50 * pin(lt, 0.15 + 0.08 * i), col, lw=6)
    lbl(ctx, "ごはんは草や葉っぱ", CX, CY - 450, 84, s=pin(lt, 0.1))


def v_party(ctx, lt, d, gt):
    tortoise(ctx, CX - 60, CY + 220, 1.0 * pin(lt), gt, hat="party")
    rnd = random.Random(3)
    for i in range(30):
        x = rnd.uniform(60, 1020); y = (rnd.uniform(0, 1500) + gt * 260) % 1500 - 100
        rrect(ctx, x, y, 22, 36, 4); fill_stroke(ctx, ["#FF3D7F", "#FFE14D", "#4FD1A5", "#5BC0EB"][i % 4], lw=0)
    lbl(ctx, "200才まであと6年!", CX, CY - 450, 88, s=pin(lt, 0.1))


def v_future(ctx, lt, d, gt):
    for i, t in enumerate(["カメ", "→", "しくみ", "→", "人間?"]):
        lbl(ctx, t, CX - 400 + i * 200, CY, 70 if i % 2 == 0 else 80, s=pin(lt, 0.12 * i))
    lbl(ctx, "長生きのしくみ研究", CX, CY - 430, 92, s=pin(lt, 0.1))


def v_comment(ctx, lt, d, gt):
    tortoise(ctx, CX, CY + 230, 0.85 * pin(lt), gt)
    piko(ctx, CX - 300, CY - 60, gt, 0.6 * pin(lt, 0.2), "wow")
    lbl(ctx, "200才になったら?", CX, CY - 440, 96, s=pin(lt, 0.1))


def v_hello(ctx, lt, d, gt):
    piko(ctx, CX - 220, CY + 200, gt, 1.0 * pin(lt), "smile")
    tortoise(ctx, CX + 220, CY + 260, 0.5 * pin(lt, 0.2), gt)
    lbl(ctx, "またね!", CX, CY - 400, 120, s=pin(lt, 0.2))
