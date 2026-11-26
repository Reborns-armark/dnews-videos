"""Visuals for the Mariana Trench deep explosive-volcanism episode (Stern et al., Frontiers in Earth Science 2026,
doi:10.3389/feart.2026.1929806). Vertical stage, CX=540, CY=760."""
import math, random
import cairo
from common4 import *
from space2 import pin, CX, CY
from hera_vis import label, photo_scene, PHOTO_LAYOUT, v_question, v_longvideo
from casa_vis import v_hello

OPTS = {"short": False}
INK = "#1B1B3A"
SEA1, SEA2, SEA3 = "#1E6FD9", "#0F3C8C", "#08173F"
LAVA, LAVA2 = "#FF6A2B", "#FFC23D"
ROCKC = "#5A5368"


def lbl(ctx, t, x, y, size=80, s=1.0, rot=0.0, font="dela", color="#FFFFFF"):
    if OPTS["short"] and font == "mochiy" and size < 56:
        return
    label(ctx, t, x, y, size, color=color, s=s, rot=rot, font=font)


def P(name, credit, title=None, box=(940, 700), **kw):
    return photo_scene(name, credit, title, box=box, **kw)


def sea_bg(ctx, gt, n=22):
    rnd = random.Random(5)
    for k in range(n):
        x = rnd.uniform(60, 1020); sp = rnd.uniform(40, 90); r = rnd.uniform(6, 14)
        y = 1340 - ((gt * sp + rnd.uniform(0, 1200)) % 1200)
        ctx.new_path(); ctx.arc(x + 10 * math.sin(gt * 2 + k), y, r, 0, 2 * math.pi)
        ctx.set_source_rgba(1, 1, 1, 0.35); ctx.set_line_width(3); ctx.stroke()


def bigtext(text, sub=None, color="#FFE14D", size=220):
    def vis(ctx, lt, d, gt):
        sea_bg(ctx, gt)
        sp = text_sprite(text, size, color=color, hi="#FF3D7F", path=FONTS["dela"])
        draw_sprite(ctx, sp, CX, CY - 60, pin(lt) * min(1.0, 1000 / sp.get_width()), 1, -0.04)
        if sub:
            sp2 = text_sprite(sub, 74, color="#FFFFFF", hi="#FFE14D", path=FONTS["mochiy"])
            draw_sprite(ctx, sp2, CX, CY + 160, pin(lt, 0.2) * min(1.0, 1000 / sp2.get_width()), 1)
    return vis


# ---------------------------------------------------------------- props
def water_box(ctx, x, y, w, h, top=SEA1, bot=SEA3, r=30):
    g = cairo.LinearGradient(0, y, 0, y + h)
    g.add_color_stop_rgb(0, *hexc(top)[:3]); g.add_color_stop_rgb(1, *hexc(bot)[:3])
    rrect(ctx, x, y, w, h, r); ctx.set_source(g); ctx.fill_preserve()
    ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(8); ctx.stroke()


def ship(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-150, -10); ctx.line_to(150, -10); ctx.line_to(110, 50); ctx.line_to(-120, 50); ctx.close_path(); fill_stroke(ctx, "#FFFFFF", lw=7)
    ctx.rectangle(-150, 10, 300, 14); ctx.set_source_rgba(*hexc("#2E4BB8")); ctx.fill()
    rrect(ctx, -60, -80, 110, 70, 10); fill_stroke(ctx, "#FFFFFF", lw=7)
    ctx.move_to(90, -10); ctx.line_to(90, -110); ctx.line_to(140, -60); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(7); ctx.stroke()
    ctx.restore()


def rov(ctx, x, y, s=1.0, gt=0.0, lights=True):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if lights:
        for sx in (-1, 1):
            ctx.move_to(sx * 50, 60); ctx.line_to(sx * 170 - 60, 330); ctx.line_to(sx * 170 + 60, 330); ctx.close_path()
            ctx.set_source_rgba(1, 1, 0.75, 0.18 + 0.05 * math.sin(gt * 6)); ctx.fill()
    rrect(ctx, -120, -70, 240, 130, 18); fill_stroke(ctx, "#FFD23D", lw=7)
    rrect(ctx, -120, -70, 240, 40, 14); fill_stroke(ctx, "#FFFFFF", lw=7)
    for sx in (-1, 1):
        circle(ctx, sx * 60, 35, 20, "#FFFFAA", lw=6)
    ctx.move_to(100, 40); ctx.line_to(160, 90); ctx.line_to(140, 130); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(10); ctx.stroke()
    ctx.move_to(0, -70); ctx.line_to(0, -130); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


def mountain(ctx, x, y, w, h, col="#8B6B4A", snow=True):
    ctx.move_to(x - w / 2, y); ctx.line_to(x - w * 0.1, y - h); ctx.line_to(x + w * 0.05, y - h * 0.92); ctx.line_to(x + w / 2, y); ctx.close_path()
    fill_stroke(ctx, col, lw=7)
    if snow:
        ctx.move_to(x - w * 0.18, y - h * 0.8); ctx.line_to(x - w * 0.1, y - h); ctx.line_to(x + w * 0.05, y - h * 0.92); ctx.line_to(x + w * 0.1, y - h * 0.78)
        ctx.close_path(); fill_stroke(ctx, "#FFFFFF", lw=5)


def cloud(ctx, x, y, r, col=(0.35, 0.32, 0.38), a=1.0, seed=1):
    rnd = random.Random(seed)
    for k in range(9):
        cx_, cy_ = x + rnd.uniform(-1, 1) * r, y + rnd.uniform(-0.6, 0.6) * r
        ctx.new_path(); ctx.arc(cx_, cy_, r * rnd.uniform(0.45, 0.75), 0, 2 * math.pi)
        ctx.set_source_rgba(col[0], col[1], col[2], a); ctx.fill()


def embers(ctx, x, y, gt, n=14, spread=200, seed=3):
    rnd = random.Random(seed)
    for k in range(n):
        ph = (gt * rnd.uniform(0.6, 1.2) + rnd.random()) % 1
        ex = x + rnd.uniform(-1, 1) * spread * ph; ey = y - 260 * ph + 200 * ph * ph
        circle(ctx, ex, ey, rnd.uniform(6, 13) * (1 - ph * 0.5), [LAVA, LAVA2][k % 2], lw=0)


def seafloor(ctx, y=1180, col=ROCKC):
    ctx.move_to(0, y); ctx.curve_to(300, y - 40, 700, y + 30, 1080, y - 20); ctx.line_to(1080, 1400); ctx.line_to(0, 1400); ctx.close_path()
    fill_stroke(ctx, col, lw=7)


def gauge(ctx, x, top, bot, frac, label_txt, col="#FFE14D"):
    ctx.move_to(x, top); ctx.line_to(x, bot); ctx.set_source_rgba(1, 1, 1, 0.7); ctx.set_line_width(10); ctx.stroke()
    for k in range(12):
        yy = top + (bot - top) * k / 11
        ctx.move_to(x - 20, yy); ctx.line_to(x + 20, yy); ctx.set_line_width(5); ctx.stroke()
    yy = top + (bot - top) * frac
    circle(ctx, x, yy, 26, col, lw=6)
    lbl(ctx, label_txt, x + 40 + 150, yy, 56, color=col)


# ---------------------------------------------------------------- scenes
def v_hook(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    seafloor(ctx, 1160)
    s = pin(lt)
    ctx.save(); ctx.translate(CX, 1170); ctx.scale(s, s)
    ctx.move_to(-260, 0); ctx.line_to(-70, -230); ctx.line_to(70, -230); ctx.line_to(260, 0); ctx.close_path(); fill_stroke(ctx, "#4A4358", lw=8)
    ctx.restore()
    p = clamp((lt - 0.2) / 0.6)
    if p > 0:
        cloud(ctx, CX, 1170 - 230 - 140 * p, 150 * p, a=0.9, seed=4)
        embers(ctx, CX, 1170 - 260, gt, 16, 230)
        burst(ctx, CX, 1170 - 260, 160 * p, lt, color=LAVA2, alpha=0.7)
    lbl(ctx, "深さ 6000m", CX, 330, 120, s=pin(lt, 0.1), color="#8FD3FF")
    lbl(ctx, "海の底で 火山が爆発!?", CX, 480, 84, s=pin(lt, 0.35), color="#FFE14D", rot=-0.04)


def v_trench(ctx, lt, d, gt):
    water_box(ctx, 80, 230, 920, 1080)
    p = clamp(lt / 0.8)
    ctx.move_to(80, 520); ctx.curve_to(300, 560, 400, 700, 520, 1200 * 1.0 if p > 0 else 520)
    ctx.line_to(600, 1230); ctx.curve_to(660, 900, 800, 640, 1000, 600); ctx.line_to(1000, 1310); ctx.line_to(80, 1310); ctx.close_path()
    fill_stroke(ctx, ROCKC, lw=7)
    lbl(ctx, "海面", 170, 280, 54, color="#FFFFFF", font="mochiy")
    lbl(ctx, "マリアナ海溝", CX, 380, 96, s=pin(lt, 0.1), color="#FFE14D")
    circle(ctx, 560, 1222, 22 * pin(lt, 0.4), "#FF3D7F", lw=6)
    lbl(ctx, "チャレンジャー海淵", 560, 1130, 56, s=pin(lt, 0.5), font="mochiy", color="#FFFFFF")


def v_everest(ctx, lt, d, gt):
    water_box(ctx, 90, 220, 900, 1100)
    base = 1300
    k = 1000 / 11000.0
    p = clamp((lt - 0.3) / 0.7)
    mountain(ctx, CX, base, 520, 8849 * k * p, col="#8B6B4A")
    ctx.move_to(120, base - 10935 * k * 0 + 0); ctx.set_source_rgba(1, 1, 1, 0)
    lbl(ctx, "約1万900m", CX + 260, 300, 74, s=pin(lt), color="#FFE14D")
    lbl(ctx, "エベレスト 8849m", CX - 140, base - 8849 * k * p - 50, 54, s=pin(lt, 0.8), font="mochiy")
    lbl(ctx, "すっぽり しずむ!", CX, 1240, 70, s=pin(lt, 1.0), color="#FFFFFF")


def v_ship(ctx, lt, d, gt):
    water_box(ctx, 80, 380, 920, 940)
    bob = 8 * math.sin(gt * 2)
    ship(ctx, CX, 360 + bob, 1.2 * pin(lt))
    y = 520 + 560 * clamp(lt / max(1.0, d * 0.7))
    ctx.move_to(CX, 400); ctx.line_to(CX, y - 60); ctx.set_source_rgba(1, 1, 1, 0.8); ctx.set_line_width(5); ctx.stroke()
    rov(ctx, CX, y, 0.9 * pin(lt, 0.2), gt)
    lbl(ctx, "調査船から ケーブルで", CX, 1250, 58, s=pin(lt, 0.3), font="mochiy")


def v_jason(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    rov(ctx, CX, CY, 2.0 * pin(lt), gt)
    lbl(ctx, "ジェイソン", CX, 300, 120, s=pin(lt, 0.2), color="#FFE14D")
    lbl(ctx, "無人の 海底ロボット", CX, 1230, 66, s=pin(lt, 0.4), font="mochiy")


def v_limit(ctx, lt, d, gt):
    water_box(ctx, 120, 230, 840, 1080)
    top, bot = 260, 1290
    yl = top + (bot - top) * 6500 / 11000
    ctx.rectangle(124, yl, 832, bot - yl + 16); ctx.set_source_rgba(0, 0, 0.05, 0.55); ctx.fill()
    ctx.move_to(124, yl); ctx.line_to(956, yl); ctx.set_source_rgba(*hexc("#FF3D7F")); ctx.set_line_width(8); ctx.set_dash([24, 16]); ctx.stroke(); ctx.set_dash([])
    rov(ctx, CX - 120, yl - 110, 0.7 * pin(lt), gt)
    lbl(ctx, "6500mまで", CX + 230, yl - 70, 70, s=pin(lt, 0.2), color="#FFE14D")
    lbl(ctx, "ここから先は 行けない", CX, yl + 120, 60, s=pin(lt, 0.5), font="mochiy")
    lbl(ctx, "いちばん深い所 約1万900m", CX, bot - 50, 50, s=pin(lt, 0.7), font="mochiy", color="#8FD3FF")


def v_pressure(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 260); ctx.scale(s, s)
    rrect(ctx, -70, -20, 140, 140, 20); fill_stroke(ctx, "#FFD6B0", lw=7)
    rrect(ctx, -46, -6, 92, 70, 22); fill_stroke(ctx, "#FFEFE3", lw=5)
    ctx.restore()
    p = clamp((lt - 0.3) / 0.6)
    for k in range(4):
        y = CY + 180 - 120 * (k + 1) * p
        rrect(ctx, CX - 170, y - 50, 340, 100, 20); fill_stroke(ctx, "#6D6A80", lw=7)
        lbl(ctx, "150kg", CX, y, 54, color="#FFFFFF")
    lbl(ctx, "指先ほど(1cm²)に 約600kg!", CX, 1240, 62, s=pin(lt, 0.8), color="#FFE14D")


def v_cup(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    for sx, sc, nm in ((-1, 1.0, "もと"), (1, 0.55, "深海から もどると")):
        x = CX + sx * 230
        ctx.save(); ctx.translate(x, CY + 100); s = sc * pin(lt, 0.2 if sx < 0 else 0.6); ctx.scale(s, s)
        ctx.move_to(-130, -200); ctx.line_to(130, -200); ctx.line_to(90, 200); ctx.line_to(-90, 200); ctx.close_path(); fill_stroke(ctx, "#FFFFFF", lw=9)
        ctx.restore()
        lbl(ctx, nm, x, CY + 420, 52, s=pin(lt, 0.4), font="mochiy")
    lbl(ctx, "カップが 小さくなる!?", CX, 330, 92, s=pin(lt, 0.3), color="#FFE14D")


def v_pyro_land(ctx, lt, d, gt):
    ctx.rectangle(80, 260, 920, 1050); ctx.set_source_rgba(*hexc("#9ED8FF")); ctx.fill()
    mountain(ctx, CX - 80, 1250, 900, 720, col="#7A6A5A", snow=False)
    p = clamp(lt / max(1.2, d * 0.8))
    cloud(ctx, CX - 120, 560, 120, a=0.95, seed=2)
    embers(ctx, CX - 120, 560, gt, 10, 120, 5)
    cloud(ctx, CX - 80 + 380 * p, 640 + 520 * p, 130, col=(0.45, 0.4, 0.42), a=0.95, seed=7)
    lbl(ctx, "火砕流", CX, 330, 120, s=pin(lt, 0.2), color="#FF3D7F")
    lbl(ctx, "熱い灰や石が いっきに流れる", CX, 1250, 56, s=pin(lt, 0.4), font="mochiy", color=INK)


def v_pyro_sea(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    seafloor(ctx, 1150)
    ctx.move_to(80, 700); ctx.line_to(80, 1160); ctx.line_to(1000, 1160); ctx.close_path(); fill_stroke(ctx, "#4A4358", lw=8)
    p = clamp(lt / max(1.2, d * 0.8))
    x = 160 + 520 * p; y = 760 + 360 * p
    ctx.new_path(); ctx.arc(x, y, 80, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(LAVA, 0.85)); ctx.fill()
    embers(ctx, x, y, gt, 8, 80, 9)
    lbl(ctx, "ゆっくり 少しだけ流れた", CX, 380, 74, s=pin(lt, 0.3), color="#FFE14D")


def v_steam(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    circle(ctx, CX - 260, CY + 200, 80 * pin(lt), "#3FA9F5", lw=7)
    lbl(ctx, "水", CX - 260, CY + 320, 64, s=pin(lt, 0.2))
    p = clamp((lt - 0.4) / 0.8)
    if p > 0:
        cloud(ctx, CX + 180, CY - 40, 260 * p, col=(0.95, 0.95, 1.0), a=0.85, seed=8)
    lbl(ctx, "水蒸気", CX + 180, CY + 320, 64, s=pin(lt, 0.6))
    lbl(ctx, "約1700倍に ふくらむ!", CX, 300, 86, s=pin(lt, 0.8), color="#FFE14D")


def v_cooker(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 120); ctx.scale(s, s)
    rrect(ctx, -260, -140, 520, 300, 40); fill_stroke(ctx, "#C9D3E0", lw=9)
    rrect(ctx, -290, -190, 580, 70, 30); fill_stroke(ctx, "#AEB9C8", lw=9)
    rrect(ctx, -30, -260, 60, 80, 20); fill_stroke(ctx, "#FF3D7F", lw=7)
    ctx.move_to(260, -60); ctx.line_to(400, -60); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(22); ctx.stroke()
    ctx.restore()
    lbl(ctx, "圧力なべ", CX, 300, 110, s=pin(lt, 0.2), color="#FFE14D")
    lbl(ctx, "おすと ふっとうしにくい", CX, 1240, 62, s=pin(lt, 0.5), font="mochiy")


def v_super(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    for k, (t, col) in enumerate((("液体", "#3FA9F5"), ("気体", "#FFFFFF"))):
        x = CX + (k * 2 - 1) * 250
        rrect(ctx, x - 210, 400, 420, 190, 50); fill_stroke(ctx, col, lw=8)
        lbl(ctx, t, x, 495, 96, color="#FFFFFF" if not k else "#8FD3FF")
    p = pin(lt, 0.5)
    ctx.save(); ctx.translate(CX, CY + 230); ctx.scale(p, p)
    circle(ctx, 0, 0, 180, "#B07CFF", lw=9)
    ctx.restore()
    lbl(ctx, "どっちでもない!", CX, CY + 230, 74, s=p, color="#FFFFFF")
    lbl(ctx, "超臨界", CX, 290, 110, s=pin(lt, 0.2), color="#FFE14D")


def v_3pct(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    p = pin(lt)
    ctx.save(); ctx.translate(CX - 200, CY + 120); ctx.scale(p, p)
    rrect(ctx, -170, -330, 340, 560, 30); fill_stroke(ctx, "#FFFFFF", lw=8)
    ctx.restore()
    lbl(ctx, "水蒸気", CX - 200, CY + 440, 60, s=p)
    q = pin(lt, 0.5)
    ctx.save(); ctx.translate(CX + 250, CY + 200); ctx.scale(q, q)
    rrect(ctx, -60, -60, 120, 110, 20); fill_stroke(ctx, "#B07CFF", lw=8)
    ctx.restore()
    lbl(ctx, "超臨界", CX + 250, CY + 440, 60, s=q)
    lbl(ctx, "たった 約3%!", CX + 200, CY - 260, 96, s=pin(lt, 0.8), color="#FFE14D")


def v_cracks(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    p = clamp(lt / max(1.0, d * 0.6))
    glow = 1 - p
    rrect(ctx, 140, 500, 800, 640, 20)
    ctx.set_source_rgba(0.35 + 0.6 * glow, 0.33 + 0.1 * glow, 0.4 - 0.2 * glow, 1); ctx.fill_preserve()
    ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(8); ctx.stroke()
    ctx.set_line_width(9)
    for i in range(1, 4):
        if p > i * 0.2:
            ctx.move_to(140 + 200 * i, 500); ctx.line_to(140 + 200 * i + 10, 1140); ctx.stroke()
    for j in range(1, 3):
        if p > 0.3 + j * 0.2:
            ctx.move_to(140, 500 + 213 * j); ctx.line_to(940, 500 + 213 * j - 8); ctx.stroke()
    lbl(ctx, "冷えて 四角く われた!", CX, 340, 86, s=pin(lt, 0.2), color="#FFE14D")
    lbl(ctx, "1まい 約1m", CX, 1240, 62, s=pin(lt, 0.6), font="mochiy")


def v_samples(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    rnd = random.Random(11)
    n = int(155 * clamp(lt / max(1.2, d * 0.7)))
    for k in range(n):
        x = 160 + (k % 13) * 63 + rnd.uniform(-6, 6); y = 520 + (k // 13) * 62
        ctx.save(); ctx.translate(x, y); ctx.rotate(rnd.uniform(0, 3))
        rrect(ctx, -24, -20, 48, 40, 12); fill_stroke(ctx, ["#6D6A80", "#8B7A6A", "#4A4358", "#9AA36B"][k % 4], lw=3)
        ctx.restore()
    lbl(ctx, f"{n}こ", CX, 360, 130, color="#FFE14D")
    lbl(ctx, "7回のもぐりで 集めた石", CX, 1300, 58, s=pin(lt, 0.3), font="mochiy")


def v_plates(ctx, lt, d, gt):
    water_box(ctx, 80, 260, 920, 300, top="#3FA9F5", bot=SEA2, r=20)
    off = (gt * 30) % 80
    ctx.save()
    ctx.move_to(1000, 560); ctx.line_to(560, 560); ctx.curve_to(420, 600, 330, 760, 260, 1150); ctx.line_to(400, 1180)
    ctx.curve_to(460, 860, 560, 700, 1000, 680); ctx.close_path(); fill_stroke(ctx, "#6FAF5A", lw=8)
    ctx.restore()
    ctx.move_to(80, 560); ctx.line_to(540, 560); ctx.curve_to(420, 640, 340, 760, 300, 900); ctx.line_to(80, 900); ctx.close_path(); fill_stroke(ctx, "#C98B5A", lw=8)
    for k in range(3):
        x = 960 - k * 140 - off
        ctx.move_to(x, 620); ctx.line_to(x - 60, 620); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(10); ctx.stroke()
        ctx.move_to(x - 80, 620); ctx.line_to(x - 50, 600); ctx.line_to(x - 50, 640); ctx.close_path(); ctx.fill()
    lbl(ctx, "太平洋の板", 800, 760, 58, s=pin(lt, 0.2), font="mochiy")
    lbl(ctx, "もぐりこむ!", 560, 1040, 80, s=pin(lt, 0.4), color="#FFE14D")
    lbl(ctx, "フィリピン海の板", 300, 1240, 50, s=pin(lt, 0.3), font="mochiy")


def v_nail(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 160); ctx.scale(s, s)
    rrect(ctx, -140, -300, 280, 600, 130); fill_stroke(ctx, "#FFD6B0", lw=9)
    rrect(ctx, -95, -260, 190, 220, 70); fill_stroke(ctx, "#FFEFE3", lw=6)
    ctx.restore()
    lbl(ctx, "1年に 約3cm", CX, 330, 110, s=pin(lt, 0.2), color="#FFE14D")
    lbl(ctx, "つめがのびる速さくらい", CX, 1270, 60, s=pin(lt, 0.5), font="mochiy")


def v_stretch(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    p = clamp(lt / max(1.0, d * 0.7))
    gap = 40 + 140 * p
    for sx in (-1, 1):
        x0 = CX + sx * gap / 2
        ctx.rectangle(min(x0, x0 + sx * 380), 520, 380, 220 - 80 * p); fill_stroke(ctx, "#C98B5A", lw=8)
        ctx.move_to(x0 + sx * 120, 460); ctx.line_to(x0 + sx * 260, 460); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(12); ctx.stroke()
    ctx.new_path(); ctx.arc(CX, 1000 - 300 * p, 110, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(LAVA, 0.9)); ctx.fill()
    lbl(ctx, "マグマ", CX, 1000 - 300 * p, 60, color="#FFFFFF")
    lbl(ctx, "引っぱられて うすくなる", CX, 320, 74, s=pin(lt, 0.2), color="#FFE14D")


def v_mantle(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 80); ctx.scale(s, s)
    circle(ctx, 0, 0, 400, "#3FA9F5", lw=8)
    ctx.move_to(0, 0); ctx.arc(0, 0, 395, -math.pi / 2, 0); ctx.close_path(); ctx.set_source_rgba(*hexc("#FF8A3D")); ctx.fill()
    ctx.move_to(0, 0); ctx.arc(0, 0, 210, -math.pi / 2, 0); ctx.close_path(); ctx.set_source_rgba(*hexc("#FFC23D")); ctx.fill()
    ctx.restore()
    lbl(ctx, "マントル", CX + 210, CY - 60, 66, s=pin(lt, 0.3), color=INK)
    lbl(ctx, "地球の中の岩が 海底に!", CX, 300, 82, s=pin(lt, 0.4), color="#FFE14D")


def v_peridot(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 60); ctx.scale(s, s); ctx.rotate(0.1 * math.sin(gt * 2))
    ctx.move_to(-200, -80); ctx.line_to(-110, -190); ctx.line_to(110, -190); ctx.line_to(200, -80); ctx.line_to(0, 220); ctx.close_path()
    fill_stroke(ctx, "#9BD54A", lw=9)
    ctx.move_to(-200, -80); ctx.line_to(200, -80); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()
    sparkles(ctx, CX, CY + 40, lt, 0.2, "#FFFFFF", 8, 300)
    lbl(ctx, "宝石ペリドットの なかま", CX, 330, 78, s=pin(lt, 0.3), color="#FFE14D")


def v_bonin(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    rnd = random.Random(4)
    for k in range(7):
        x = CX + rnd.uniform(-160, 160); y = 520 + k * 95
        ctx.save(); ctx.translate(x, y); s = pin(lt, 0.1 * k) * rnd.uniform(0.6, 1.2); ctx.scale(s, s)
        ctx.new_path(); ctx.arc(0, 0, 50, 0, 2 * math.pi); fill_stroke(ctx, "#6FC45A", lw=6)
        ctx.restore()
    lbl(ctx, "小笠原諸島", CX, 330, 110, s=pin(lt, 0.2), color="#FFE14D")
    lbl(ctx, "英語で ボニン諸島", CX, 1270, 64, s=pin(lt, 0.6), font="mochiy")


def v_japan(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY - 80); ctx.scale(s, s)
    rrect(ctx, -330, -220, 660, 440, 30); fill_stroke(ctx, "#FFFFFF", lw=9)
    circle(ctx, 0, 0, 130, "#E8364A", lw=0)
    ctx.restore()
    names = ["海上保安庁", "産業技術総合研究所", "高知大学", "名古屋大学・東海大学"]
    for k, nm in enumerate(names):
        lbl(ctx, nm, CX, CY + 250 + k * 85, 54, s=pin(lt, 0.3 + 0.12 * k), font="mochiy", color="#FFE14D")


def v_shinkai(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 40); ctx.scale(s, s); ctx.translate(0, 10 * math.sin(gt * 2))
    rrect(ctx, -330, -120, 600, 240, 120); fill_stroke(ctx, "#FFFFFF", lw=9)
    rrect(ctx, -330, -20, 600, 40, 10); ctx.set_source_rgba(*hexc("#FF8A3D")); ctx.fill()
    circle(ctx, -230, -10, 44, "#8FD3FF", lw=7)
    ctx.move_to(270, -60); ctx.line_to(360, -110); ctx.line_to(360, 110); ctx.line_to(270, 60); ctx.close_path(); fill_stroke(ctx, "#FF8A3D", lw=7)
    ctx.restore()
    lbl(ctx, "しんかい6500", CX, 330, 110, s=pin(lt, 0.2), color="#FFE14D")
    lbl(ctx, "日本の 有人潜水船", CX, 1230, 64, s=pin(lt, 0.5), font="mochiy")


def v_vent(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    seafloor(ctx, 1000, "#4A4358")
    for k, x in enumerate((260, 540, 820)):
        draw_sprite(ctx, text_sprite("?", 200, color="#FFE14D", path=FONTS["dela"]), x, 760, pin(lt, 0.15 * k), 1, 0.3 * math.sin(gt * 3 + k))
    lbl(ctx, "ふき出し口は どこ?", CX, 340, 96, s=pin(lt, 0.4), color="#FFFFFF")


def v_dive_deeper(ctx, lt, d, gt):
    water_box(ctx, 120, 230, 840, 1080)
    p = clamp(lt / max(1.0, d * 0.8))
    rov(ctx, CX, 380 + 760 * p, 0.8 * pin(lt), gt)
    lbl(ctx, "もっと深くへ!", CX, 300, 96, s=pin(lt, 0.2), color="#FFE14D")


def v_volcano_ring(ctx, lt, d, gt):
    sea_bg(ctx, gt)
    seafloor(ctx, 1100)
    for k, x in enumerate((220, 540, 860)):
        ctx.save(); ctx.translate(x, 1110); s = pin(lt, 0.15 * k); ctx.scale(s, s)
        ctx.move_to(-150, 0); ctx.line_to(-40, -220); ctx.line_to(40, -220); ctx.line_to(150, 0); ctx.close_path(); fill_stroke(ctx, "#4A4358", lw=7)
        ctx.restore()
        embers(ctx, x, 880, gt, 6, 60, k + 2)
    lbl(ctx, "海の底は 火山だらけ", CX, 380, 90, s=pin(lt, 0.4), color="#FFE14D")


def v_comment(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY); ctx.scale(s, s); ctx.rotate(0.05 * math.sin(gt * 5))
    rrect(ctx, -300, -200, 600, 360, 60); fill_stroke(ctx, "#FFFFFF", lw=12)
    ctx.move_to(-120, 150); ctx.line_to(-200, 280); ctx.line_to(-20, 160); ctx.close_path(); fill_stroke(ctx, "#FFFFFF", lw=12)
    rrect(ctx, -300, -200, 600, 360, 60); ctx.set_source_rgba(1, 1, 1, 1); ctx.fill()
    for k in range(3):
        circle(ctx, -150 + k * 150, -20, 40 * pin(lt, 0.2 + k * 0.15), "#FF3D7F", lw=6)
    ctx.restore()


v_6148 = bigtext("6148m", "火山の岩が見つかった深さ", size=230)
v_deepest = bigtext("海で いちばん深い", "爆発した火山の あと", size=140)
v_52 = bigtext("5200万年前", "板のもぐりこみが 始まった", size=170)
v_2024 = bigtext("2024年", "11月〜12月の 調査", size=230)
v_nov23 = bigtext("11月23日", "論文が 発表された", size=210)
v_300km = bigtext("約300km", "東京〜名古屋くらいを しらべた", size=210)
v_374 = bigtext("374℃・約220気圧", "これをこえると 水は超臨界", size=110)
v_surprise = bigtext("びっくり!", "海溝の近くの爆発は めずらしい", size=210)
