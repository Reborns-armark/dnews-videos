"""Visuals for the Cassiopeia A (Webb dust / shell merger, ESA/Webb weic2624 2026-11-23) episode. Vertical stage, CX=540, CY=760."""
import math, random
import cairo
from common4 import *
from space2 import pin, CX, CY
from space import planet, telescope
from hera_vis import label, photo_scene, PHOTO_LAYOUT, v_question, v_longvideo, space_bg

OPTS = {"short": False}
INK = "#1B1B3A"
LAYERS = [("#FF5A3C", "鉄"), ("#B07CFF", "ケイ素"), ("#3FAF5A", "ネオン"), ("#3FA9F5", "酸素"), ("#9AA3B8", "炭素"),
          ("#FDB515", "ヘリウム"), ("#FFE7A0", "水素")]


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
            draw_sprite(ctx, text_sprite(sub, 78, color="#FFFFFF", hi="#FFE14D", path=FONTS["mochiy"]), CX, CY + 160, pin(lt, 0.2), 1)
    return vis


# ---------------------------------------------------------------- props
def onion(ctx, x, y, r, s=1.0, n=7, mix=0.0, gt=0.0, labels=False):
    """Cross-section of a massive star: layers from iron core to hydrogen envelope."""
    if s < 1e-3:
        return
    for k in range(n - 1, -1, -1):
        col, name = LAYERS[k]
        rr = r * s * (k + 1) / n
        ctx.new_path()
        steps = 90
        for i in range(steps + 1):
            a = i / steps * 2 * math.pi
            wob = 1 + (0.09 * mix * math.sin(a * 5 + gt * 3 + k) if k in (2, 3, 4) else 0)
            px, py = x + rr * wob * math.cos(a), y + rr * wob * math.sin(a)
            ctx.line_to(px, py) if i else ctx.move_to(px, py)
        ctx.close_path(); fill_stroke(ctx, col, lw=5)
    if labels and s > 0.5:
        for k in range(n):
            col, name = LAYERS[k]
            rr = r * s * (k + 0.5) / n
            draw_sprite(ctx, text_sprite(name, 34 if k else 38, color="#FFFFFF", stroke=INK, stroke_w=5, shadow=False, path=FONTS["mochiy"]),
                        x, y - rr if k else y, 1, 1)


def explode(ctx, x, y, lt, gt, r=300):
    burst(ctx, x, y, r + 40 * math.sin(lt * 18), gt, "#FFE14D", n=18)
    burst(ctx, x, y, r * 0.6, gt + 0.5, "#FF8A3D", n=12)
    sparkles(ctx, x, y, lt, 0.0, "#FFB34D", 26, 560)


def dustcloud(ctx, x, y, r, gt, seed=3, cols=("#FF7A5C", "#7CE08A", "#8FD3FF")):
    rnd = random.Random(seed)
    for k in range(70):
        a = rnd.uniform(0, 2 * math.pi); rr = r * math.sqrt(rnd.random())
        c = cols[k % len(cols)]
        ctx.new_path(); ctx.arc(x + rr * math.cos(a + gt * 0.05), y + rr * math.sin(a + gt * 0.05), rnd.uniform(6, 18), 0, 2 * math.pi)
        ctx.set_source_rgba(*hexc(c)[:3], 0.75); ctx.fill()


def webb(ctx, x, y, s, gt):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(0.05 * math.sin(gt))
    ctx.move_to(-260, 150); ctx.line_to(260, 150); ctx.line_to(200, 230); ctx.line_to(-200, 230); ctx.close_path()
    fill_stroke(ctx, "#B9A6E8", lw=6)
    for (hx, hy) in [(0, 0), (-70, -40), (70, -40), (-70, 40), (70, 40), (0, -80), (0, 80), (-140, 0), (140, 0)]:
        ctx.new_path()
        for i in range(7):
            a = math.pi / 6 + i * math.pi / 3
            ctx.line_to(hx + 44 * math.cos(a), hy - 40 + 44 * math.sin(a))
        ctx.close_path(); fill_stroke(ctx, "#F6C343", lw=4)
    ctx.restore()


def wstars(ctx, x, y, s, lt):
    pts = [(-320, -40), (-160, 80), (0, -20), (160, 90), (320, -60)]
    ctx.move_to(x + pts[0][0] * s, y + pts[0][1] * s)
    for p in pts[1:]:
        ctx.line_to(x + p[0] * s, y + p[1] * s)
    ctx.set_source_rgba(1, 1, 1, 0.5); ctx.set_line_width(6); ctx.stroke()
    for i, p in enumerate(pts):
        star(ctx, x + p[0] * s, y + p[1] * s, 34 * pin(lt, 0.08 * i), "#FFE14D")


# ---------------------------------------------------------------- scenes
def v_hook(ctx, lt, d, gt):
    space_bg(ctx, gt)
    if lt < 0.9:
        onion(ctx, CX, CY + 40, 300, pin(lt), mix=1.0, gt=gt)
    else:
        explode(ctx, CX, CY + 40, lt - 0.9, gt)
        dustcloud(ctx, CX, CY + 40, 320 * clamp((lt - 0.9) / 0.6), gt)
    lbl(ctx, "ドカーン!", CX, CY - 420, 130, s=pin(lt - 0.9), color="#FF3D7F", rot=-0.08)


def v_onion(ctx, lt, d, gt):
    space_bg(ctx, gt)
    onion(ctx, CX, CY + 60, 380, pin(lt), labels=True)
    lbl(ctx, "星の中は 層になっている", CX, CY - 420, 80, s=pin(lt, 0.2))


def v_tamanegi(ctx, lt, d, gt):
    space_bg(ctx, gt)
    onion(ctx, CX - 210, CY + 60, 200, pin(lt))
    # onion vegetable
    s = pin(lt, 0.2)
    ctx.save(); ctx.translate(CX + 230, CY + 60); ctx.scale(s, s)
    for k in range(4, 0, -1):
        ctx.save(); ctx.scale(1, 1.05); circle(ctx, 0, 0, 45 * k, ["#F7E3B5", "#EFC98A", "#E2AE62", "#C98B3E"][k - 1], lw=5); ctx.restore()
    ctx.move_to(0, -190); ctx.line_to(-14, -250); ctx.move_to(0, -190); ctx.line_to(16, -255)
    ctx.set_source_rgba(*hexc("#7A5A2A")); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()
    lbl(ctx, "=", CX + 10, CY + 60, 120, s=pin(lt, 0.3))
    lbl(ctx, "たまねぎみたい!", CX, CY - 420, 100, s=pin(lt, 0.3))


def v_merge(ctx, lt, d, gt):
    space_bg(ctx, gt)
    onion(ctx, CX, CY + 60, 360, pin(lt), mix=clamp(lt / 1.2) * 2.2, gt=gt * 2)
    for k in range(6):
        a = gt * 2 + k
        draw_sprite(ctx, text_sprite("ぐるぐる", 36, color="#FFFFFF", path=FONTS["mochiy"]), CX + 250 * math.cos(a), CY + 60 + 250 * math.sin(a), 0.8 * pin(lt, 0.3), 0.8)
    lbl(ctx, "層がまざった!?", CX, CY - 420, 100, s=pin(lt, 0.2))


def v_clock(ctx, lt, d, gt):
    space_bg(ctx, gt)
    s = pin(lt)
    circle(ctx, CX, CY + 60, 300 * s, "#FFFFFF", lw=12)
    for k in range(12):
        a = k / 12 * 2 * math.pi
        circle(ctx, CX + 250 * s * math.sin(a), CY + 60 - 250 * s * math.cos(a), 12 * s, INK, lw=0)
    for (L, sp, w) in [(200, 2.5, 18), (130, 0.4, 24)]:
        a = gt * sp
        ctx.move_to(CX, CY + 60); ctx.line_to(CX + L * s * math.sin(a), CY + 60 - L * s * math.cos(a))
        ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    lbl(ctx, "爆発の 数時間前!", CX, CY - 420, 100, s=pin(lt, 0.2), color="#FFE14D")


def v_light(ctx, lt, d, gt):
    space_bg(ctx, gt)
    explode(ctx, CX - 330, CY, lt, gt, r=110)
    planet(ctx, CX + 360, CY, 80 * pin(lt, 0.2), "#3FA9F5")
    for k in range(8):
        x = CX - 230 + ((gt * 160 + k * 70) % 520)
        circle(ctx, x, CY, 12, "#FFE14D", lw=0)
    lbl(ctx, "約1万1000光年", CX, CY - 300, 110, s=pin(lt, 0.2))
    lbl(ctx, "カシオペヤ座A", CX - 330, CY + 220, 54, s=pin(lt, 0.3), font="mochiy")
    lbl(ctx, "地球", CX + 360, CY + 160, 60, s=pin(lt, 0.3), font="mochiy")


def v_lightyear(ctx, lt, d, gt):
    space_bg(ctx, gt)
    lbl(ctx, "1光年", CX, CY - 380, 120, s=pin(lt))
    lbl(ctx, "=光が1年で進むきょり", CX, CY - 220, 74, s=pin(lt, 0.15), font="mochiy")
    lbl(ctx, "約9兆5000億km!", CX, CY + 0, 110, s=pin(lt, 0.3), color="#FFE14D")
    piko(ctx, CX, CY + 330, gt, 0.7 * pin(lt, 0.4), "wow")


def v_constellation(ctx, lt, d, gt):
    space_bg(ctx, gt)
    wstars(ctx, CX, CY - 20, 1.25, lt)
    circle(ctx, CX + 60, CY - 150, 26 * pin(lt, 0.5), "#FF3D7F", lw=5)
    lbl(ctx, "ここらへん", CX + 230, CY - 230, 54, s=pin(lt, 0.6), font="mochiy")
    lbl(ctx, "カシオペヤ座(Wの形)", CX, CY - 420, 86, s=pin(lt, 0.1))
    lbl(ctx, "日本では 一年中 北の空に", CX, CY + 260, 64, s=pin(lt, 0.4), font="mochiy")


def v_edo(ctx, lt, d, gt):
    space_bg(ctx, gt)
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 80); ctx.scale(s, s)
    ctx.move_to(-380, -60); ctx.line_to(0, -230); ctx.line_to(380, -60); ctx.close_path(); fill_stroke(ctx, "#4B4E6D", lw=8)
    rrect(ctx, -300, -60, 600, 280, 8); fill_stroke(ctx, "#F2E6C9", lw=8)
    for x in (-180, 0, 180):
        rrect(ctx, x - 60, 10, 120, 150, 4); fill_stroke(ctx, "#FFFFFF", lw=6)
        ctx.move_to(x, 10); ctx.line_to(x, 160); ctx.move_to(x - 60, 85); ctx.line_to(x + 60, 85)
        ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()
    star(ctx, CX + 330, CY - 330, 50 * (1 + 0.3 * math.sin(gt * 8)), "#FFE14D")
    lbl(ctx, "1680年ごろ 日本は江戸時代", CX, CY - 440, 74, s=pin(lt, 0.2))


def v_flamsteed(ctx, lt, d, gt):
    space_bg(ctx, gt)
    telescope(ctx, CX - 60, CY + 300, gt, 1.0 * pin(lt))
    star(ctx, CX + 250, CY - 230, 40 * pin(lt, 0.3), "#FFE14D")
    lbl(ctx, "?", CX + 340, CY - 330, 120, s=pin(lt, 0.4), color="#FF3D7F")
    lbl(ctx, "フラムスティード(1680年)", CX, CY - 440, 74, s=pin(lt, 0.1))


def v_size(ctx, lt, d, gt):
    space_bg(ctx, gt)
    dustcloud(ctx, CX, CY + 40, 340 * pin(lt), gt, seed=5)
    ctx.move_to(CX - 340, CY + 430); ctx.line_to(CX + 340, CY + 430)
    ctx.set_source_rgba(1, 1, 1, 0.9); ctx.set_line_width(10); ctx.stroke()
    lbl(ctx, "はば 約10光年", CX, CY - 420, 100, s=pin(lt, 0.2))


def v_clump(ctx, lt, d, gt):
    space_bg(ctx, gt)
    dustcloud(ctx, CX, CY + 40, 330 * pin(lt), gt, seed=8, cols=("#FF7A5C",))
    sun_r = 30
    circle(ctx, CX, CY + 40, sun_r * pin(lt, 0.3), "#FFD23F", lw=4)
    for k, r in enumerate((80, 140, 220, 300)):
        ctx.new_path(); ctx.arc(CX, CY + 40, r * pin(lt, 0.3), 0, 2 * math.pi)
        ctx.set_source_rgba(1, 1, 1, 0.6); ctx.set_line_width(4); ctx.stroke()
    lbl(ctx, "ちりのかたまり=太陽系サイズ!", CX, CY - 420, 74, s=pin(lt, 0.2))


def v_webb(ctx, lt, d, gt):
    space_bg(ctx, gt)
    webb(ctx, CX, CY + 80, 1.3 * pin(lt), gt)
    lbl(ctx, "ジェイムズ・ウェッブ宇宙望遠鏡", CX, CY - 420, 70, s=pin(lt, 0.2))


def v_infrared(ctx, lt, d, gt):
    space_bg(ctx, gt)
    cols = ["#7B3DFF", "#3D7BFF", "#3FAF5A", "#FFE14D", "#FF8A3D", "#FF3D3D"]
    for i, c in enumerate(cols):
        rrect(ctx, CX - 420 + i * 120, CY - 40, 110, 200, 10); fill_stroke(ctx, c, lw=5)
    rrect(ctx, CX + 300, CY - 40, 140, 200, 10); fill_stroke(ctx, "#3A2A4A", lw=5)
    lbl(ctx, "目に見える光", CX - 120, CY + 230, 56, s=pin(lt, 0.1), font="mochiy")
    lbl(ctx, "赤外線", CX + 370, CY + 230, 56, s=pin(lt, 0.2), font="mochiy", color="#FF8A3D")
    lbl(ctx, "ちりは赤外線で光る", CX, CY - 420, 90, s=pin(lt, 0.2))


def _vial(ctx, x, y, s, col, name, lt, k):
    s = s * pin(lt, 0.12 * k)
    if s < 1e-3:
        return
    circle(ctx, x, y, 150 * s, col, lw=8)
    draw_sprite(ctx, text_sprite(name, 50, color="#FFFFFF", stroke=INK, stroke_w=6, shadow=False, path=FONTS["dela"]), x, y, s, 1)


def v_three(ctx, lt, d, gt):
    space_bg(ctx, gt)
    _vial(ctx, CX - 280, CY + 20, 1.0, "#C9B8FF", "シリカ", lt, 0)
    _vial(ctx, CX + 280, CY + 20, 1.0, "#555B6E", "炭素", lt, 1)
    _vial(ctx, CX, CY + 330, 1.15, "#3FAF5A", "グリーン\nモンスター", lt, 2)
    lbl(ctx, "3か所のちりを しらべた", CX, CY - 420, 84, s=pin(lt, 0.1))


def v_glass(ctx, lt, d, gt):
    space_bg(ctx, gt)
    s = pin(lt)
    ctx.save(); ctx.translate(CX - 220, CY + 80); ctx.scale(s, s)
    ctx.move_to(-110, -200); ctx.line_to(110, -200); ctx.line_to(80, 200); ctx.line_to(-80, 200); ctx.close_path()
    ctx.set_source_rgba(0.75, 0.9, 1, 0.55); ctx.fill_preserve(); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()
    s2 = pin(lt, 0.2)
    ctx.save(); ctx.translate(CX + 230, CY + 260); ctx.scale(s2, s2)
    ctx.move_to(-230, 0); ctx.curve_to(-120, -260, 120, -260, 230, 0); ctx.close_path(); fill_stroke(ctx, "#F2D08A", lw=8)
    rnd = random.Random(2)
    for k in range(30):
        circle(ctx, rnd.uniform(-150, 150), rnd.uniform(-150, -20), 6, "#C9A25A", lw=0)
    ctx.restore()
    lbl(ctx, "ガラス", CX - 220, CY - 220, 70, s=pin(lt, 0.3))
    lbl(ctx, "砂", CX + 230, CY - 20, 70, s=pin(lt, 0.4))
    lbl(ctx, "シリカ=ガラスや砂の材料", CX, CY - 420, 80, s=pin(lt, 0.1), color="#FFE14D")


def v_pencil(ctx, lt, d, gt):
    space_bg(ctx, gt)
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 60); ctx.rotate(-0.5); ctx.scale(s, s)
    rrect(ctx, -330, -50, 520, 100, 8); fill_stroke(ctx, "#FFD23F", lw=8)
    ctx.move_to(190, -50); ctx.line_to(330, 0); ctx.line_to(190, 50); ctx.close_path(); fill_stroke(ctx, "#F2D08A", lw=8)
    ctx.move_to(285, -16); ctx.line_to(330, 0); ctx.line_to(285, 16); ctx.close_path(); fill_stroke(ctx, "#333344", lw=4)
    ctx.restore()
    lbl(ctx, "炭素=えんぴつのしんや すすのなかま", CX, CY - 420, 64, s=pin(lt, 0.1), color="#FFE14D")


def v_fenway(ctx, lt, d, gt):
    space_bg(ctx, gt)
    s = pin(lt)
    rrect(ctx, CX - 440, CY - 140, 880, 400 * s, 10); fill_stroke(ctx, "#2E7D4F", lw=10)
    for x in range(-380, 400, 150):
        rrect(ctx, CX + x, CY - 80, 110, 70, 6); fill_stroke(ctx, "#1F5A38", lw=4)
    p = (gt * 0.6) % 1
    circle(ctx, CX - 400 + 800 * p, CY - 260 - 200 * math.sin(p * math.pi), 28, "#FFFFFF", lw=5)
    lbl(ctx, "ボストンの野球場の 緑のかべ", CX, CY - 420, 74, s=pin(lt, 0.2))
    lbl(ctx, "グリーンモンスター", CX, CY + 360, 84, s=pin(lt, 0.3), color="#7CE08A")


def v_gem(ctx, lt, d, gt):
    space_bg(ctx, gt)
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 60); ctx.scale(s, s)
    ctx.move_to(-200, -80); ctx.line_to(-110, -200); ctx.line_to(110, -200); ctx.line_to(200, -80); ctx.line_to(0, 220); ctx.close_path()
    fill_stroke(ctx, "#9BD94A", lw=10)
    ctx.move_to(-200, -80); ctx.line_to(200, -80); ctx.move_to(-110, -200); ctx.line_to(0, 220); ctx.move_to(110, -200); ctx.line_to(0, 220)
    ctx.set_source_rgba(1, 1, 1, 0.6); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()
    sparkles(ctx, CX, CY + 60, lt, 0.2, "#FFFFFF", 10, 320)
    lbl(ctx, "マグネシウムをふくむ 石のつぶ", CX, CY - 420, 72, s=pin(lt, 0.1))
    lbl(ctx, "宝石ペリドットのなかまも", CX, CY + 380, 66, s=pin(lt, 0.3), font="mochiy", color="#FFE14D")


def v_before(ctx, lt, d, gt):
    space_bg(ctx, gt)
    onion(ctx, CX, CY + 60, 200, pin(lt))
    rnd = random.Random(4)
    for k in range(40):
        a = rnd.uniform(0, 2 * math.pi); rr = 240 + ((gt * 40 + rnd.uniform(0, 180)) % 180)
        circle(ctx, CX + rr * math.cos(a), CY + 60 + rr * math.sin(a), 9, "#7CE08A", lw=0)
    lbl(ctx, "爆発の前に はき出したガス", CX, CY - 420, 76, s=pin(lt, 0.2))


def v_xray(ctx, lt, d, gt):
    space_bg(ctx, gt)
    for i, (x, col, name) in enumerate([(CX - 230, "#F2C14E", "チャンドラ(NASA)"), (CX + 230, "#FF8A3D", "XRISM(JAXAなど)")]):
        s = pin(lt, 0.15 * i)
        ctx.save(); ctx.translate(x, CY + 40); ctx.scale(s, s)
        rrect(ctx, -60, -200, 120, 360, 20); fill_stroke(ctx, "#E8E8F0", lw=7)
        for sx in (-1, 1):
            rrect(ctx, sx * 70 - (150 if sx < 0 else 0), -60, 150, 90, 8); fill_stroke(ctx, "#2E3F8F", lw=5)
        circle(ctx, 0, -200, 40, col, lw=6)
        ctx.restore()
        lbl(ctx, name, x, CY + 300, 50, s=pin(lt, 0.3), font="mochiy")
    lbl(ctx, "X線の望遠鏡", CX, CY - 420, 100, s=pin(lt, 0.1))


def v_japan(ctx, lt, d, gt):
    space_bg(ctx, gt)
    circle(ctx, CX, CY - 40, 200 * pin(lt), "#FFFFFF", lw=8)
    circle(ctx, CX, CY - 40, 90 * pin(lt, 0.1), "#E83A3A", lw=0)
    lbl(ctx, "日本の研究者も活やく!", CX, CY - 420, 90, s=pin(lt, 0.2))
    lbl(ctx, "明治大学 佐藤寿紀さんのチーム", CX, CY + 280, 62, s=pin(lt, 0.3), font="mochiy", color="#FFE14D")


def v_push(ctx, lt, d, gt):
    space_bg(ctx, gt)
    p = clamp(lt / 1.6)
    circle(ctx, CX, CY + 60, 330, "#3FAF5A", lw=6)
    lbl(ctx, "ネオンの層", CX, CY - 190, 54, font="mochiy")
    for k in range(5):
        a = -1.2 + k * 0.6
        rr = 120 + 170 * p
        circle(ctx, CX + rr * math.cos(a) * 0.9, CY + 60 + rr * math.sin(a) * 0.9, 50, "#B07CFF", lw=5)
    circle(ctx, CX, CY + 60, 110, "#B07CFF", lw=6)
    lbl(ctx, "ケイ素", CX, CY + 60, 54, font="mochiy")
    lbl(ctx, "ケイ素が外へ ぐいっ!", CX, CY - 420, 90, s=pin(lt, 0.2), color="#FFE14D")


def v_lopsided(ctx, lt, d, gt):
    space_bg(ctx, gt)
    ctx.save(); ctx.translate(CX - 40, CY + 60); ctx.scale(1.15, 0.85); ctx.rotate(0.4)
    dustcloud(ctx, 0, 0, 300 * pin(lt), gt, seed=11)
    ctx.restore()
    p = (lt * 0.4) % 1
    circle(ctx, CX + 40 + 300 * p, CY + 100 + 120 * p, 26, "#FFFFFF", lw=6)
    lbl(ctx, "中性子星", CX + 260, CY + 330, 60, s=pin(lt, 0.3), font="mochiy")
    lbl(ctx, "形がかたより 星のしんは高速で", CX, CY - 420, 70, s=pin(lt, 0.1))


def v_ns(ctx, lt, d, gt):
    space_bg(ctx, gt)
    circle(ctx, CX, CY + 20, 120 * pin(lt), "#DDEBFF", lw=10)
    for k in range(10):
        a = k / 10 * 2 * math.pi + gt
        ctx.move_to(CX + 150 * math.cos(a), CY + 20 + 150 * math.sin(a)); ctx.line_to(CX + 210 * math.cos(a), CY + 20 + 210 * math.sin(a))
        ctx.set_source_rgba(0.7, 0.85, 1, 0.8); ctx.set_line_width(10); ctx.stroke()
    lbl(ctx, "中性子星", CX, CY - 420, 110, s=pin(lt, 0.1))
    lbl(ctx, "スプーン1ぱいで 約10億トン!?", CX, CY + 330, 70, s=pin(lt, 0.3), color="#FFE14D")


def v_stardust(ctx, lt, d, gt):
    space_bg(ctx, gt)
    dustcloud(ctx, CX - 250, CY - 80, 180 * pin(lt), gt)
    planet(ctx, CX + 220, CY + 40, 150 * pin(lt, 0.2), "#3FA9F5")
    piko(ctx, CX - 120, CY + 330, gt, 0.6 * pin(lt, 0.3), "wow")
    lbl(ctx, "わたしたちも 星くず!?", CX, CY - 420, 96, s=pin(lt, 0.2), color="#FFE14D")


def v_recipe(ctx, lt, d, gt):
    space_bg(ctx, gt)
    for i, (c, n) in enumerate([("#C9B8FF", "シリカ"), ("#555B6E", "炭素"), ("#3FAF5A", "石のつぶ")]):
        x = CX - 300 + i * 300
        circle(ctx, x, CY - 60, 100 * pin(lt, 0.1 * i), c, lw=6)
        lbl(ctx, n, x, CY - 60, 44, s=pin(lt, 0.1 * i), font="mochiy")
    lbl(ctx, "↓", CX, CY + 110, 120, s=pin(lt, 0.3))
    planet(ctx, CX, CY + 320, 110 * pin(lt, 0.4), "#3FA9F5")
    lbl(ctx, "惑星の材料に", CX, CY - 420, 100, s=pin(lt, 0.1))


def v_future(ctx, lt, d, gt):
    space_bg(ctx, gt)
    webb(ctx, CX - 260, CY + 160, 0.6 * pin(lt), gt)
    for i, (x, y) in enumerate([(CX + 150, CY - 150), (CX + 330, CY + 40), (CX + 160, CY + 260)]):
        dustcloud(ctx, x, y, 90 * pin(lt, 0.15 * i), gt, seed=20 + i)
    lbl(ctx, "ほかの星の さいごも?", CX, CY - 420, 96, s=pin(lt, 0.2))


def v_betel(ctx, lt, d, gt):
    space_bg(ctx, gt)
    circle(ctx, CX, CY + 40, 220 * pin(lt) * (1 + 0.04 * math.sin(gt * 2)), "#FF6A3D", lw=10)
    lbl(ctx, "ベテルギウス(オリオン座)", CX, CY - 420, 76, s=pin(lt, 0.1))
    lbl(ctx, "いつか 超新星に!?", CX, CY + 360, 90, s=pin(lt, 0.3), color="#FFE14D")


def v_comment(ctx, lt, d, gt):
    dustcloud(ctx, CX + 220, CY + 140, 170 * pin(lt), gt)
    piko(ctx, CX - 260, CY + 100, gt, 0.75 * pin(lt, 0.2), "wow")
    lbl(ctx, "星のこと 何を知りたい?", CX, CY - 430, 84, s=pin(lt, 0.1))


def v_hello(ctx, lt, d, gt):
    piko(ctx, CX - 220, CY + 200, gt, 1.0 * pin(lt), "smile")
    webb(ctx, CX + 260, CY + 60, 0.5 * pin(lt, 0.2), gt)
    lbl(ctx, "またね!", CX, CY - 400, 120, s=pin(lt, 0.2))


v_340 = bigtext("約340年前", "地球にとどいた光", size=170)
v_hours = bigtext("数時間前", "爆発する ほんの少し前", size=210)
v_youngest = bigtext("いちばん若い", "天の川銀河の 大きな星の爆発あと", size=170)
v_nov23 = bigtext("11月23日", "ESAとNASAが発表", size=200)
v_bigstar = bigtext("太陽の8倍以上", "重い星の さいご", size=150)
