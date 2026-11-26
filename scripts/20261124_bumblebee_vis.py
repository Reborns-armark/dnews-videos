"""Visuals for the 'bumblebee intelligence' episode (Science Perspective, Chittka & Heinze, 2026-11-19). Vertical stage, CX=540, CY=760."""
import math, random
from common4 import *
from space2 import pin, CX, CY
from hera_vis import label, photo_scene, PHOTO_LAYOUT, v_question, v_longvideo

OPTS = {"short": False}
INK = "#1B1B3A"
YEL = "#FFC83D"
BLK = "#2A2438"


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


# ---------------------------------------------------------------- characters / props
def bee(ctx, x, y, s, gt, k=0.0, mood="smile", flip=False, wings=True, rot=0.0, hat=None):
    """Cute fluffy bumblebee facing right (flip=True faces left)."""
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(-s if flip else s, s)
    # wings (fast flutter)
    if wings:
        fl = 0.35 * math.sin(gt * 40 + k)
        for dx, a in ((-30, -0.5 + fl), (20, -0.2 - fl)):
            ctx.save(); ctx.translate(dx, -70); ctx.rotate(a); ctx.scale(0.55, 1.0)
            ctx.new_path(); ctx.arc(0, -70, 70, 0, 2 * math.pi); ctx.set_source_rgba(0.85, 0.95, 1.0, 0.75); ctx.fill_preserve()
            ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(6); ctx.stroke(); ctx.restore()
    # legs
    for lx in (-60, -10, 40):
        ctx.move_to(lx, 60); ctx.line_to(lx - 10, 105); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(9); ctx.stroke()
    # body (fuzzy oval with stripes)
    ctx.save(); ctx.scale(1.25, 1.0)
    ctx.new_path(); ctx.arc(0, 0, 90, 0, 2 * math.pi); fill_stroke(ctx, YEL, lw=8)
    ctx.restore()
    ctx.save(); ctx.scale(1.25, 1.0); ctx.new_path(); ctx.arc(0, 0, 86, 0, 2 * math.pi); ctx.clip()
    for bx in (-70, -20):
        ctx.rectangle(bx, -100, 26, 200); ctx.set_source_rgba(*hexc(BLK)); ctx.fill()
    ctx.rectangle(-110, -100, 30, 200); ctx.set_source_rgba(*hexc("#FFFFFF")); ctx.fill()
    ctx.restore()
    # fuzz dots
    for i in range(14):
        a = i / 14 * 2 * math.pi
        circle(ctx, 112 * math.cos(a), 90 * math.sin(a), 7, YEL, lw=0)
    # head
    circle(ctx, 120, -10, 58, BLK, lw=8)
    circle(ctx, 140, -22, 14, "#FFFFFF", lw=0); circle(ctx, 144, -24, 7, INK, lw=0)
    if mood == "smile":
        ctx.new_path(); ctx.arc(138, 8, 18, 0.2, 2.6); ctx.set_source_rgba(1, 1, 1, 1); ctx.set_line_width(5); ctx.stroke()
    elif mood == "wow":
        circle(ctx, 142, 16, 10, "#FFFFFF", lw=0)
    circle(ctx, 112, 16, 9, "#FF8FB1", lw=0)
    # antennae
    for ax, ay in ((120, -110), (160, -95)):
        ctx.move_to(118, -55); ctx.curve_to(120, -80, ax - 10, ay + 10, ax, ay); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(7); ctx.stroke()
        circle(ctx, ax, ay, 9, BLK, lw=0)
    if hat == "crown":
        ctx.move_to(90, -60); ctx.line_to(95, -110); ctx.line_to(115, -80); ctx.line_to(125, -120); ctx.line_to(135, -80)
        ctx.line_to(155, -110); ctx.line_to(155, -60); ctx.close_path(); fill_stroke(ctx, "#FFD23F", lw=5)
    ctx.restore()


def ball(ctx, x, y, r, col="#FF6FA8", rot=0.0):
    circle(ctx, x, y, r, col, lw=8)
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ctx.move_to(-r, 0); ctx.line_to(r, 0); ctx.set_source_rgba(1, 1, 1, 0.6); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()
    circle(ctx, x - r * 0.35, y - r * 0.35, r * 0.18, "#FFFFFF", lw=0)


def flower(ctx, x, y, r, col="#5BC0EB", ctr="#FFE14D", up=False):
    for i in range(6):
        a = i / 6 * 2 * math.pi
        circle(ctx, x + r * math.cos(a), y + r * math.sin(a), r * 0.62, col, lw=5)
    circle(ctx, x, y, r * 0.6, ctr, lw=5)


def drop(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(0, -40); ctx.curve_to(30, -5, 30, 30, 0, 30); ctx.curve_to(-30, 30, -30, -5, 0, -40); ctx.close_path()
    fill_stroke(ctx, "#FFB84D", lw=5); ctx.restore()


def brain(ctx, x, y, s, col="#FF9EC4"):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for (bx, by, r) in [(-60, -20, 70), (0, -50, 75), (60, -20, 70), (-30, 30, 65), (40, 30, 65)]:
        circle(ctx, bx, by, r, col, lw=7)
    for i in range(5):
        ctx.new_path(); ctx.arc(-70 + i * 35, -10 + (i % 2) * 20, 22, 0.3, 2.6); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


def arena(ctx, lt, top=CY - 260, bot=CY + 330):
    """Low clear box seen from the side."""
    rrect(ctx, 90, top, 900, bot - top, 20); ctx.set_source_rgba(0.85, 0.95, 1.0, 0.28); ctx.fill_preserve()
    ctx.set_source_rgba(1, 1, 1, 0.9); ctx.set_line_width(10); ctx.stroke()


# ---------------------------------------------------------------- scenes
def v_hook(ctx, lt, d, gt):
    ball(ctx, CX - 150, CY + 250, 140)
    bee(ctx, CX + 180, CY + 200, 1.15 * pin(lt), gt, mood="wow", flip=True)
    lbl(ctx, "ハチがボールを!?", CX, CY - 380, 130, s=pin(lt, 0.15), rot=-0.05)


v_sesame = bigtext("ゴマつぶ", "くらいの脳", size=220)
v_million = bigtext("100万", "より少ない神経細胞", size=260)
v_million_big = bigtext("100万", None, size=330)


def v_bee(ctx, lt, d, gt):
    bee(ctx, CX, CY + 60, 1.5 * pin(lt), gt, k=0.3)
    flower(ctx, CX - 300, CY + 420, 70 * pin(lt, 0.2), "#FF8FB1")
    flower(ctx, CX + 320, CY + 430, 60 * pin(lt, 0.3), "#B07BE0")
    lbl(ctx, "マルハナバチ", CX, CY - 400, 110, s=pin(lt, 0.1))


def v_fluffy(ctx, lt, d, gt):
    bee(ctx, CX, CY + 60, 1.7 * pin(lt), gt)
    for i in range(6):
        a = gt * 0.8 + i
        draw_sprite(ctx, text_sprite("♥", 70, color="#FF8FB1", path=FONTS["dela"]), CX + 380 * math.cos(a), CY + 60 + 260 * math.sin(a), pin(lt, 0.1 * i), 1)
    lbl(ctx, "モフモフ!", CX, CY - 400, 120, s=pin(lt, 0.1))


def v_buzz(ctx, lt, d, gt):
    flower(ctx, CX, CY + 100, 120 * pin(lt), "#FFFFFF", "#FFD23F")
    j = 8 * math.sin(gt * 60)
    bee(ctx, CX + j, CY - 30, 0.9 * pin(lt, 0.15), gt)
    for i in range(3):
        r = 220 + i * 70 + (gt * 120) % 70
        ctx.new_path(); ctx.arc(CX, CY - 30, r, -0.6, 0.6); ctx.set_source_rgba(1, 1, 1, 0.8); ctx.set_line_width(8); ctx.stroke()
        ctx.new_path(); ctx.arc(CX, CY - 30, r, math.pi - 0.6, math.pi + 0.6); ctx.stroke()
    rnd = random.Random(int(gt * 10))
    for i in range(12):
        circle(ctx, CX + rnd.uniform(-160, 160), CY + 120 + rnd.uniform(0, 200), 9, "#FFE14D", lw=0)
    lbl(ctx, "ブルブルで花粉を落とす", CX, CY - 420, 82, s=pin(lt, 0.1))


def v_tomato(ctx, lt, d, gt):
    # greenhouse
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 120); ctx.scale(s, s)
    ctx.move_to(-440, 300); ctx.line_to(-440, -60); ctx.curve_to(-440, -340, 440, -340, 440, -60); ctx.line_to(440, 300); ctx.close_path()
    ctx.set_source_rgba(0.85, 0.97, 1.0, 0.35); ctx.fill_preserve(); ctx.set_source_rgba(1, 1, 1, 0.95); ctx.set_line_width(10); ctx.stroke()
    for i in range(5):
        x = -320 + i * 160
        ctx.move_to(x, 300); ctx.line_to(x, -40); ctx.set_source_rgba(*hexc("#3FAF5A")); ctx.set_line_width(12); ctx.stroke()
        circle(ctx, x + 30, 60 + (i % 2) * 70, 38, "#FF4D4D", lw=5)
        circle(ctx, x - 30, 170 - (i % 2) * 50, 32, "#FF4D4D", lw=5)
    ctx.restore()
    bee(ctx, CX + 200 * math.sin(gt), CY - 120, 0.45 * pin(lt, 0.2), gt)
    lbl(ctx, "トマトのハウスで大活やく", CX, CY - 430, 80, s=pin(lt, 0.1))


def v_noFly(ctx, lt, d, gt):
    lbl(ctx, "計算では…", CX, CY - 420, 100, s=pin(lt, 0.1))
    draw_sprite(ctx, text_sprite("羽が小さい÷体が重い", 70, color="#FFFFFF", path=FONTS["mochiy"]), CX, CY - 200, pin(lt, 0.2), 1)
    draw_sprite(ctx, text_sprite("=とべない!?", 120, color="#FF3D7F", hi="#FFE14D", path=FONTS["dela"]), CX, CY - 40, pin(lt, 0.4), 1, -0.05)
    bee(ctx, CX, CY + 300, 0.8 * pin(lt, 0.5), gt, mood="wow")


def v_canFly(ctx, lt, d, gt):
    y = CY + 60 + 60 * math.sin(gt * 2)
    bee(ctx, CX + 120 * math.sin(gt * 1.3), y, 1.1 * pin(lt), gt, k=1)
    for i in range(4):
        ctx.new_path(); ctx.arc(CX - 300 + i * 40, CY + 380, 50 + i * 20, math.pi, 1.8 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.7); ctx.set_line_width(6); ctx.stroke()
    lbl(ctx, "1秒に約200回はばたく", CX, CY - 420, 84, s=pin(lt, 0.1))


def v_science(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX + 140, CY + 40); ctx.scale(s, s); ctx.rotate(0.05)
    rrect(ctx, -230, -310, 460, 620, 18); fill_stroke(ctx, "#FFFFFF", lw=10)
    rrect(ctx, -230, -310, 460, 130, 18); fill_stroke(ctx, "#C8102E", lw=10)
    ctx.restore()
    draw_sprite(ctx, text_sprite("Science", 80, color="#FFFFFF", stroke="#C8102E", path=FONTS["dela"]), CX + 140, CY - 205, s, 1, 0.05)
    for i in range(5):
        rrect(ctx, CX - 40, CY - 80 + i * 70, 360 - (i % 2) * 90, 20, 10); ctx.set_source_rgba(*hexc("#B8C0D0")); ctx.fill()
    bee(ctx, CX - 260, CY + 300, 0.7 * pin(lt, 0.25), gt)
    lbl(ctx, "11月19日 サイエンス誌", CX, CY - 440, 80, s=pin(lt, 0.1))


def v_brain_cmp(ctx, lt, d, gt):
    brain(ctx, CX - 210, CY + 60, 1.9 * pin(lt))
    lbl(ctx, "人間", CX - 210, CY + 320, 80, s=pin(lt, 0.2))
    lbl(ctx, "約860億", CX - 210, CY + 430, 74, s=pin(lt, 0.3), color="#FFE14D")
    brain(ctx, CX + 300, CY + 140, 0.25 * pin(lt, 0.4))
    lbl(ctx, "ハチ", CX + 300, CY + 320, 80, s=pin(lt, 0.45))
    lbl(ctx, "100万より少ない", CX + 300, CY + 430, 60, s=pin(lt, 0.55), color="#FFE14D")
    lbl(ctx, "神経細胞の数", CX, CY - 420, 100, s=pin(lt, 0.1))


def v_sesame_scene(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 40); ctx.scale(s, s)
    ctx.save(); ctx.scale(1.0, 0.6); circle(ctx, 0, 0, 150, "#F3E3C3", lw=8); ctx.restore()
    ctx.restore()
    brain(ctx, CX, CY + 40, 0.9 * pin(lt, 0.3))
    draw_sprite(ctx, text_sprite("ゴマ1つぶ", 70, path=FONTS["mochiy"]), CX, CY + 260, pin(lt, 0.2), 1)
    lbl(ctx, "ハチの脳はこのくらい", CX, CY - 400, 86, s=pin(lt, 0.1))


def v_high_flower(ctx, lt, d, gt):
    arena(ctx, lt)
    flower(ctx, CX + 120, CY - 220, 56 * pin(lt), "#5BC0EB")
    drop(ctx, CX + 120, CY - 140, 0.8 * pin(lt, 0.2))
    bee(ctx, CX - 200, CY + 250, 0.55 * pin(lt, 0.2), gt, wings=False)
    ball(ctx, CX - 360, CY + 260, 70)
    lbl(ctx, "天井の花にミツ", CX, CY - 430, 100, s=pin(lt, 0.1))


def v_no_fly_box(ctx, lt, d, gt):
    arena(ctx, lt)
    flower(ctx, CX + 120, CY - 220, 56, "#5BC0EB")
    bee(ctx, CX + 40, CY + 140 + 30 * math.sin(gt * 6), 0.55 * pin(lt), gt, mood="wow")
    draw_sprite(ctx, text_sprite("ひくくて飛べない!", 72, color="#FF3D7F", hi="#FFE14D", path=FONTS["mochiy"]), CX, CY - 40, pin(lt, 0.3), 1)
    lbl(ctx, "箱がひくい", CX, CY - 430, 100, s=pin(lt, 0.1))


def v_push(ctx, lt, d, gt):
    arena(ctx, lt)
    flower(ctx, CX + 120, CY - 220, 56, "#5BC0EB")
    drop(ctx, CX + 120, CY - 140, 0.8)
    p = ease_out_cubic(clamp(lt / max(1.0, d * 0.7)))
    bx = CX - 360 + 480 * p
    ball(ctx, bx, CY + 260, 70, rot=p * 6)
    bee(ctx, bx - 150, CY + 250, 0.55 * pin(lt), gt, wings=False)
    lbl(ctx, "ゴロゴロ…", CX, CY - 430, 110, s=pin(lt, 0.1))


def v_climb(ctx, lt, d, gt):
    arena(ctx, lt)
    flower(ctx, CX + 120, CY - 220, 56, "#5BC0EB")
    drop(ctx, CX + 120, CY - 140, 0.8)
    ball(ctx, CX + 120, CY + 260, 70)
    p = ease_out_cubic(clamp(lt / 0.8))
    bee(ctx, CX + 70, CY + 200 - 110 * p, 0.5 * pin(lt), gt, wings=False, rot=-0.5 * p, mood="smile")
    lbl(ctx, "ふみ台にして…ゴクッ!", CX, CY - 430, 90, s=pin(lt, 0.1))


def v_unseen(ctx, lt, d, gt):
    arena(ctx, lt)
    rrect(ctx, CX - 40, CY - 260, 30, 590, 6); ctx.set_source_rgba(*hexc("#7A8A99")); ctx.fill()
    flower(ctx, CX + 260, CY - 220, 50, "#5BC0EB")
    ball(ctx, CX - 200, CY + 260, 70)
    bee(ctx, CX - 340, CY + 250, 0.5 * pin(lt), gt, wings=False)
    draw_sprite(ctx, text_sprite("?", 140, color="#FFE14D", path=FONTS["dela"]), CX + 230, CY + 40, pin(lt, 0.3), 1)
    lbl(ctx, "見えない場所へも運ぶ", CX, CY - 430, 84, s=pin(lt, 0.1))


def v_chimp(ctx, lt, d, gt):
    # simple box + banana scene
    s = pin(lt)
    rrect(ctx, CX - 330, CY + 120, 260, 220, 10); fill_stroke(ctx, "#C99A5B", lw=8)
    ctx.save(); ctx.translate(CX + 220, CY - 230); ctx.scale(s, s); ctx.rotate(0.3)
    ctx.new_path(); ctx.arc(0, 0, 90, 0.2, 2.6); ctx.set_source_rgba(*hexc("#FFE14D")); ctx.set_line_width(40); ctx.stroke()
    ctx.restore()
    bee(ctx, CX + 200, CY + 260, 0.6 * pin(lt, 0.2), gt)
    lbl(ctx, "道具の知恵", CX, CY - 430, 110, s=pin(lt, 0.1))


def v_play(ctx, lt, d, gt):
    for i, (x, c) in enumerate([(CX - 300, "#FF6FA8"), (CX + 40, "#FFE14D"), (CX + 320, "#5BC0EB")]):
        ball(ctx, x + 20 * math.sin(gt * 2 + i), CY + 300, 70, c, rot=gt * 2 + i)
    bee(ctx, CX - 120 + 180 * math.sin(gt * 1.1), CY + 160 + 40 * math.sin(gt * 3), 0.6 * pin(lt), gt)
    draw_sprite(ctx, text_sprite("ごほうび なし", 70, color="#FFFFFF", hi="#FFE14D", path=FONTS["mochiy"]), CX, CY - 120, pin(lt, 0.3), 1)
    lbl(ctx, "ボールで遊ぶ!?", CX, CY - 430, 110, s=pin(lt, 0.1))


def v_young(ctx, lt, d, gt):
    bee(ctx, CX - 220, CY + 160, 0.55 * pin(lt), gt)
    ball(ctx, CX - 60, CY + 300, 60, rot=gt * 3)
    bee(ctx, CX + 260, CY + 120, 0.9 * pin(lt, 0.2), gt, k=1)
    lbl(ctx, "わかいハチほどよく遊ぶ", CX, CY - 430, 80, s=pin(lt, 0.1))


def v_goal(ctx, lt, d, gt):
    circle(ctx, CX, CY + 120, 300, "#7CC36A", lw=8)
    circle(ctx, CX, CY + 120, 60, "#1B1B3A", lw=6)
    p = ease_out_cubic(clamp(lt / max(1.0, d * 0.6)))
    bx = CX - 220 + 220 * p
    ball(ctx, bx, CY + 120, 45, "#FFE14D", rot=p * 5)
    bee(ctx, bx - 110, CY + 100, 0.4 * pin(lt), gt, wings=False)
    lbl(ctx, "ハチのサッカー!?", CX, CY - 430, 110, s=pin(lt, 0.1))


def v_watch(ctx, lt, d, gt):
    bee(ctx, CX - 260, CY + 200, 0.6 * pin(lt), gt, k=0.5)
    draw_sprite(ctx, text_sprite("じーっ", 70, color="#FFFFFF", path=FONTS["mochiy"]), CX - 260, CY - 20, pin(lt, 0.2), 1)
    ball(ctx, CX + 200, CY + 250, 55, "#FFE14D", rot=gt)
    bee(ctx, CX + 80, CY + 230, 0.45 * pin(lt, 0.15), gt, wings=False)
    lbl(ctx, "見て まねして 上達", CX, CY - 430, 90, s=pin(lt, 0.1))


def puzzlebox(ctx, x, y, s, gt, step=0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -260, -180, 520, 360, 30); fill_stroke(ctx, "#FFFFFF", lw=10)
    circle(ctx, 0, 0, 90, "#FFB84D" if step >= 2 else "#DDE3EA", lw=8)
    if step >= 2:
        drop(ctx, 0, 0, 1.2)
    rrect(ctx, -230 + (90 if step >= 1 else 0), -40, 70, 80, 14); fill_stroke(ctx, "#4FA3E0", lw=7)
    rrect(ctx, 160 - (90 if step >= 2 else 0), -40, 70, 80, 14); fill_stroke(ctx, "#FF3D7F", lw=7)
    ctx.restore()


def v_puzzle(ctx, lt, d, gt):
    st = 0 if lt < 0.8 else (1 if lt < 1.6 else 2)
    puzzlebox(ctx, CX, CY + 80, 1.3 * pin(lt), gt, st)
    lbl(ctx, "青→赤の 2ステップ", CX, CY - 420, 92, s=pin(lt, 0.1))


def v_alone(ctx, lt, d, gt):
    puzzlebox(ctx, CX, CY + 160, 0.9 * pin(lt), gt, 0)
    bee(ctx, CX - 120, CY - 130, 0.5 * pin(lt, 0.2), gt, mood="wow")
    draw_sprite(ctx, text_sprite("ひとりでは×", 90, color="#FF3D7F", hi="#FFE14D", path=FONTS["dela"]), CX, CY + 470, pin(lt, 0.3), 1)
    lbl(ctx, "ひとりではとけない", CX, CY - 430, 92, s=pin(lt, 0.1))


def v_teach(ctx, lt, d, gt):
    puzzlebox(ctx, CX, CY + 180, 0.85 * pin(lt), gt, 2 if lt > 1.0 else 1)
    bee(ctx, CX - 260, CY - 120, 0.45 * pin(lt, 0.1), gt, hat="crown")
    bee(ctx, CX + 250, CY - 120, 0.45 * pin(lt, 0.2), gt, flip=True)
    draw_sprite(ctx, text_sprite("先生バチ", 56, path=FONTS["mochiy"]), CX - 260, CY - 260, pin(lt, 0.2), 1)
    lbl(ctx, "先生を見て できた!", CX, CY - 440, 92, s=pin(lt, 0.1))


def v_treat(ctx, lt, d, gt):
    bee(ctx, CX - 120, CY + 200, 0.95 * pin(lt), gt, mood="smile")
    drop(ctx, CX + 260, CY - 20, 2.0 * pin(lt, 0.3))
    for i in range(6):
        a = i / 6 * 2 * math.pi + gt
        draw_sprite(ctx, text_sprite("✦", 50, color="#FFE14D", path=FONTS["dela"]), CX + 260 + 130 * math.cos(a), CY - 20 + 130 * math.sin(a), pin(lt, 0.4), 1)
    lbl(ctx, "思いがけないごほうび", CX, CY - 430, 86, s=pin(lt, 0.1))


def v_ambig(ctx, lt, d, gt):
    flower(ctx, CX - 300, CY + 100, 70 * pin(lt), "#4FA3E0")
    flower(ctx, CX, CY + 100, 70 * pin(lt, 0.15), "#8F8FE0")
    flower(ctx, CX + 300, CY + 100, 70 * pin(lt, 0.3), "#3FAF5A")
    lbl(ctx, "あたり", CX - 300, CY + 260, 60, s=pin(lt, 0.2), font="mochiy")
    lbl(ctx, "どっち?", CX, CY + 260, 60, s=pin(lt, 0.3), font="mochiy", color="#FFE14D")
    lbl(ctx, "はずれ", CX + 300, CY + 260, 60, s=pin(lt, 0.4), font="mochiy")
    bee(ctx, CX - 20, CY - 140, 0.45 * pin(lt, 0.3), gt)
    lbl(ctx, "あいまいな花", CX, CY - 430, 100, s=pin(lt, 0.1))


def v_optimist(ctx, lt, d, gt):
    bee(ctx, CX, CY + 120, 1.2 * pin(lt), gt, mood="smile")
    draw_sprite(ctx, text_sprite("たぶん あたり!", 80, color="#FFFFFF", hi="#FFE14D", path=FONTS["mochiy"]), CX, CY - 180, pin(lt, 0.25), 1, -0.04)
    lbl(ctx, "前向きな気分?", CX, CY - 430, 110, s=pin(lt, 0.1))


def v_kenyon(ctx, lt, d, gt):
    brain(ctx, CX, CY + 80, 2.2 * pin(lt), "#FFC8DD")
    for sx in (-1, 1):
        ctx.save(); ctx.translate(CX + sx * 90, CY + 20)
        s = pin(lt, 0.3)
        ctx.scale(s, s)
        ctx.new_path(); ctx.arc(0, -40, 60, math.pi, 2 * math.pi); ctx.close_path(); fill_stroke(ctx, "#FFB84D", lw=6)
        rrect(ctx, -14, -40, 28, 120, 10); fill_stroke(ctx, "#FFB84D", lw=6)
        ctx.restore()
    lbl(ctx, "キノコ体", CX, CY + 380, 80, s=pin(lt, 0.3), color="#FFE14D")
    lbl(ctx, "記憶と学習のセンター", CX, CY - 420, 84, s=pin(lt, 0.1))


def v_fly50(ctx, lt, d, gt):
    lbl(ctx, "ショウジョウバエ", CX - 230, CY - 200, 56, s=pin(lt, 0.1), font="mochiy")
    lbl(ctx, "マルハナバチ", CX + 230, CY - 200, 56, s=pin(lt, 0.2), font="mochiy")
    h1 = 30; h2 = 520 * ease_out_cubic(clamp((lt - 0.3) / 0.8))
    rrect(ctx, CX - 300, CY + 380 - h1, 140, h1, 8); fill_stroke(ctx, "#8FA3B8", lw=6)
    rrect(ctx, CX + 160, CY + 380 - max(h2, 1), 140, max(h2, 1), 8); fill_stroke(ctx, "#FFB84D", lw=6)
    lbl(ctx, "約50倍!", CX + 230, CY - 100, 90, s=pin(lt, 0.9), color="#FFE14D")
    lbl(ctx, "キノコ体の細胞", CX, CY - 430, 100, s=pin(lt, 0.1))


def v_oldcircuit(ctx, lt, d, gt):
    for i in range(3):
        for j in range(4):
            circle(ctx, CX - 300 + j * 200, CY - 100 + i * 180, 40 * pin(lt, 0.05 * (i + j)), "#5BC0EB", lw=6)
    for i in range(3):
        for j in range(3):
            ctx.move_to(CX - 300 + j * 200, CY - 100 + i * 180); ctx.line_to(CX - 100 + j * 200, CY - 100 + i * 180)
            ctx.set_source_rgba(1, 1, 1, 0.8); ctx.set_line_width(6); ctx.stroke()
    lbl(ctx, "昔からの回路を", CX, CY - 430, 96, s=pin(lt, 0.1))
    lbl(ctx, "大きくしただけ?", CX, CY + 450, 90, s=pin(lt, 0.4), color="#FFE14D")


def crow(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.save(); ctx.scale(1.3, 1.0); circle(ctx, 0, 0, 100, "#2A2438", lw=8); ctx.restore()
    circle(ctx, 110, -80, 60, "#2A2438", lw=8)
    ctx.move_to(160, -90); ctx.line_to(240, -70); ctx.line_to(160, -55); ctx.close_path(); fill_stroke(ctx, "#5A5A6A", lw=6)
    circle(ctx, 125, -95, 12, "#FFFFFF", lw=0)
    ctx.restore()


def v_convergent(ctx, lt, d, gt):
    crow(ctx, CX - 250, CY + 100, 0.9 * pin(lt))
    piko(ctx, CX + 20, CY + 140, gt, 0.5 * pin(lt, 0.15), "smile")
    bee(ctx, CX + 300, CY + 120, 0.55 * pin(lt, 0.3), gt)
    lbl(ctx, "ちがう脳で 同じかしこさ", CX, CY - 430, 80, s=pin(lt, 0.1))


def v_drone(ctx, lt, d, gt):
    s = pin(lt)
    y = CY + 40 + 30 * math.sin(gt * 2)
    ctx.save(); ctx.translate(CX, y); ctx.scale(s, s)
    rrect(ctx, -120, -50, 240, 100, 30); fill_stroke(ctx, "#DDE3EA", lw=8)
    for dx in (-200, 200):
        ctx.move_to(dx * 0.6, 0); ctx.line_to(dx, -40); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(10); ctx.stroke()
        ctx.save(); ctx.translate(dx, -50); ctx.scale(1, 0.2); circle(ctx, 0, 0, 90, "#B8E1FF", lw=6); ctx.restore()
    circle(ctx, 60, 0, 22, "#4FD1A5", lw=5)
    ctx.restore()
    bee(ctx, CX - 330, CY + 340, 0.5 * pin(lt, 0.2), gt)
    lbl(ctx, "小さくて かしこいロボ", CX, CY - 430, 84, s=pin(lt, 0.1))


def v_protect(ctx, lt, d, gt):
    for i in range(7):
        flower(ctx, 120 + i * 140, CY + 380 - (i % 2) * 60, 46 * pin(lt, 0.05 * i), ["#FF8FB1", "#B07BE0", "#5BC0EB", "#FFE14D"][i % 4], "#FFB84D")
    bee(ctx, CX - 150, CY - 20, 0.6 * pin(lt, 0.2), gt)
    bee(ctx, CX + 200, CY + 60, 0.5 * pin(lt, 0.3), gt, k=2, flip=True)
    lbl(ctx, "ハチを大切に", CX, CY - 430, 110, s=pin(lt, 0.1))


def v_comment(ctx, lt, d, gt):
    bee(ctx, CX + 120, CY + 200, 0.9 * pin(lt), gt)
    piko(ctx, CX - 300, CY - 60, gt, 0.6 * pin(lt, 0.2), "wow")
    lbl(ctx, "ハチに教えたいことは?", CX, CY - 440, 84, s=pin(lt, 0.1))


def v_hello(ctx, lt, d, gt):
    piko(ctx, CX - 220, CY + 200, gt, 1.0 * pin(lt), "smile")
    bee(ctx, CX + 240, CY + 120, 0.6 * pin(lt, 0.2), gt)
    lbl(ctx, "またね!", CX, CY - 400, 120, s=pin(lt, 0.2))


def v_caution(ctx, lt, d, gt):
    bee(ctx, CX, CY + 200, 0.9 * pin(lt), gt)
    draw_sprite(ctx, text_sprite("!", 220, color="#FFE14D", path=FONTS["dela"]), CX + 320, CY - 120, pin(lt, 0.2), 1)
    lbl(ctx, "ただし", CX, CY - 430, 120, s=pin(lt, 0.1))
