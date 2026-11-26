"""Visuals for the 'Westminster Abbey Roman coffin' episode (vertical stage, CX=540, CY=760)."""
import math, random
from common4 import *
from space2 import pin, CX, CY
from space import sun
from hera_vis import label, photo_scene, PHOTO_LAYOUT, v_question, v_longvideo

STONE = "#D8CFBF"
STONE2 = "#B9AE9A"
WOOD = "#9A6A3E"
BONE = "#F4EEDD"
ROBE = "#4A3A6B"
TOGA = "#F2F0EA"
GRASS = "#7DBF5A"
SOIL = "#7A5A3A"
OPTS = {"short": False}


def lbl(ctx, t, x, y, size=80, s=1.0, rot=0.0, font="dela", color="#FFFFFF"):
    if OPTS["short"] and font == "mochiy" and size < 70:
        return
    label(ctx, t, x, y, size, color=color, s=s, rot=rot, font=font)


# ---------------------------------------------------------------- props
def coffin(ctx, x, y, s, gt=0.0, lid=0.0, cross=True, inscr=True, inside=None, lid_pieces=False, face=False):
    """Stone sarcophagus seen from the front-top. lid: 0 closed .. 1 lifted away. inside: None|'skel'|'wood'|'empty'."""
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    # box
    ctx.move_to(-330, -40); ctx.line_to(330, -40); ctx.line_to(300, 170); ctx.line_to(-300, 170); ctx.close_path()
    fill_stroke(ctx, STONE2, lw=9)
    # top opening
    ctx.move_to(-330, -40); ctx.line_to(330, -40); ctx.line_to(290, -120); ctx.line_to(-290, -120); ctx.close_path()
    fill_stroke(ctx, "#5E5546", lw=9)
    if inside == "skel":
        skeleton_lying(ctx, 0, -80, 0.62, gt)
    elif inside == "wood":
        ctx.move_to(-250, -52); ctx.line_to(250, -52); ctx.line_to(225, -108); ctx.line_to(-225, -108); ctx.close_path()
        ctx.set_source_rgba(1, 1, 1, 0.9); ctx.set_line_width(10); ctx.set_dash([18, 10]); ctx.stroke(); ctx.set_dash([])
        skeleton_lying(ctx, 0, -80, 0.55, gt)
    if inscr:
        rrect(ctx, -160, 10, 320, 110, 10); fill_stroke(ctx, STONE, lw=6)
        for k in range(3):
            ctx.move_to(-130, 38 + k * 28); ctx.line_to(130 - 30 * (k == 2), 38 + k * 28)
            ctx.set_source_rgba(*hexc("#6E6352")); ctx.set_line_width(7); ctx.stroke()
    if face:
        for sx in (-1, 1):
            circle(ctx, sx * 230, 60, 16, "#1B1B3A", lw=0)
    # lid
    if lid < 1:
        ly = -120 - 260 * ease_in_out(lid); lr = -0.35 * lid
        ctx.save(); ctx.translate(-260 * lid, ly); ctx.rotate(lr)
        if lid_pieces:
            for k in range(6):
                xx = -340 + k * 113
                ctx.save(); ctx.translate(0, 8 * math.sin(k * 2.1)); ctx.rotate(0.05 * math.sin(k * 3.3))
                ctx.move_to(xx, 0); ctx.line_to(xx + 108, 0); ctx.line_to(xx + 104, -80); ctx.line_to(xx + 6, -80); ctx.close_path()
                fill_stroke(ctx, STONE, lw=7); ctx.restore()
        else:
            ctx.move_to(-345, 0); ctx.line_to(345, 0); ctx.line_to(300, -90); ctx.line_to(-300, -90); ctx.close_path()
            fill_stroke(ctx, STONE, lw=9)
        if cross:
            ctx.move_to(-230, -45); ctx.line_to(230, -45); ctx.move_to(-120, -78); ctx.line_to(-120, -12)
            ctx.set_source_rgba(*hexc("#8C7F68")); ctx.set_line_width(16); ctx.stroke()
        ctx.restore()
    ctx.restore()


def skull(ctx, x, y, r, gt=0.0, mood="smile"):
    circle(ctx, x, y, r, BONE, lw=6)
    for sx in (-1, 1):
        circle(ctx, x + sx * r * 0.38, y - r * 0.05, r * 0.24, "#1B1B3A", lw=0)
        circle(ctx, x + sx * r * 0.33, y - r * 0.12, r * 0.08, "#FFFFFF", lw=0)
    if mood == "wow":
        circle(ctx, x, y + r * 0.45, r * 0.14, "#1B1B3A", lw=0)
    else:
        ctx.new_path(); ctx.arc(x, y + r * 0.3, r * 0.3, 0.3, math.pi - 0.3)
        ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(max(3, r * 0.08)); ctx.stroke()


def skeleton_lying(ctx, x, y, s, gt):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-250, 0); ctx.line_to(220, 0); ctx.set_source_rgba(*hexc(BONE)); ctx.set_line_width(22); ctx.stroke()
    for k in range(5):
        ctx.move_to(-170 + k * 40, -40); ctx.line_to(-170 + k * 40, 40); ctx.set_line_width(14); ctx.stroke()
    for sy in (-1, 1):
        ctx.move_to(-150, 0); ctx.line_to(-60, sy * 70); ctx.set_line_width(14); ctx.stroke()
        ctx.move_to(220, 0); ctx.line_to(330, sy * 40); ctx.stroke()
    ctx.restore()
    skull(ctx, x - 300 * s, y, 62 * s, gt)


def skeleton_stand(ctx, x, y, s, gt, mood="smile", h=1.0):
    """Cute standing skeleton, height scale h (for 'taller' comparisons)."""
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s * h)
    ctx.set_source_rgba(*hexc(BONE)); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(0, -260); ctx.line_to(0, -40); ctx.set_line_width(24); ctx.stroke()
    for k in range(4):
        ctx.move_to(-55, -230 + k * 40); ctx.line_to(55, -230 + k * 40); ctx.set_line_width(14); ctx.stroke()
    wave = 0.3 * math.sin(gt * 4)
    for sx in (-1, 1):
        ctx.move_to(0, -240); ctx.line_to(sx * 110, -130 + (sx > 0) * wave * -200); ctx.set_line_width(16); ctx.stroke()
        ctx.move_to(0, -40); ctx.line_to(sx * 60, 160); ctx.stroke()
    ctx.restore()
    skull(ctx, x, y - 330 * s * h, 70 * s, gt, mood)


def monk(ctx, x, y, s, gt, mood="smile", staff=False):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-130, 200); ctx.curve_to(-120, 0, -90, -120, 0, -120); ctx.curve_to(90, -120, 120, 0, 130, 200); ctx.close_path()
    fill_stroke(ctx, ROBE, lw=8)
    ctx.move_to(-60, 40); ctx.line_to(60, 40); ctx.set_source_rgba(*hexc("#E8C27A")); ctx.set_line_width(12); ctx.stroke()
    if staff:
        ctx.move_to(170, 220); ctx.line_to(170, -200); ctx.set_source_rgba(*hexc("#E8C27A")); ctx.set_line_width(14); ctx.stroke()
        ctx.new_path(); ctx.arc(140, -200, 32, -math.pi, 0.6); ctx.stroke()
    ctx.restore()
    hy = y - 190 * s
    circle(ctx, x, hy, 92 * s, "#F6D2B0", lw=7)
    ctx.new_path(); ctx.arc(x, hy - 10 * s, 96 * s, math.pi * 1.05, math.pi * 1.95); ctx.set_source_rgba(*hexc("#6B4A2B")); ctx.set_line_width(26 * s); ctx.stroke()
    for sx in (-1, 1):
        circle(ctx, x + sx * 32 * s, hy + 5 * s, 10 * s, "#1B1B3A", lw=0)
    if mood == "wow":
        circle(ctx, x, hy + 45 * s, 14 * s, "#1B1B3A", lw=0)
    else:
        ctx.new_path(); ctx.arc(x, hy + 30 * s, 26 * s, 0.3, math.pi - 0.3); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(6 * s); ctx.stroke()


def roman(ctx, x, y, s, gt, col=TOGA, beard=False, mood="smile", scale_h=1.0):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s * scale_h)
    ctx.move_to(-120, 200); ctx.curve_to(-110, 0, -80, -110, 0, -110); ctx.curve_to(80, -110, 110, 0, 120, 200); ctx.close_path()
    fill_stroke(ctx, col, lw=8)
    ctx.move_to(-90, -60); ctx.curve_to(0, 40, 40, 120, 110, 190); ctx.set_source_rgba(*hexc("#B0413E")); ctx.set_line_width(22); ctx.stroke()
    ctx.restore()
    hy = y - 180 * s * scale_h
    circle(ctx, x, hy, 85 * s, "#F6D2B0", lw=7)
    for k in range(7):
        a = math.pi * (1.1 + 0.8 * k / 6)
        circle(ctx, x + 90 * s * math.cos(a), hy + 90 * s * math.sin(a), 18 * s, "#4CA64C", lw=3)
    if beard:
        ctx.new_path(); ctx.arc(x, hy + 30 * s, 70 * s, 0.1, math.pi - 0.1); ctx.set_source_rgba(*hexc("#8A8A8A")); ctx.fill()
    for sx in (-1, 1):
        circle(ctx, x + sx * 30 * s, hy, 10 * s, "#1B1B3A", lw=0)
    if mood == "wow":
        circle(ctx, x, hy + 40 * s, 13 * s, "#1B1B3A", lw=0)
    else:
        ctx.new_path(); ctx.arc(x, hy + 24 * s, 24 * s, 0.3, math.pi - 0.3); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(6 * s); ctx.stroke()


def abbey(ctx, x, y, s, col="#E9DFC9"):
    """Two-tower gothic church, base at y."""
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for sx in (-1, 1):
        rrect(ctx, sx * 170 - 70, -520, 140, 520, 8); fill_stroke(ctx, col, lw=8)
        for k in range(4):
            ctx.move_to(sx * 170 - 70 + 15 + k * 37, -520); ctx.line_to(sx * 170 - 70 + 15 + k * 37, -560)
        ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(10); ctx.stroke()
        ctx.new_path(); ctx.arc(sx * 170, -330, 34, math.pi, 0); ctx.line_to(sx * 170 + 34, -250); ctx.line_to(sx * 170 - 34, -250); ctx.close_path()
        fill_stroke(ctx, "#4FA3E0", lw=5)
    rrect(ctx, -100, -380, 200, 380, 6); fill_stroke(ctx, col, lw=8)
    ctx.new_path(); ctx.arc(0, -280, 80, 0, 6.28); fill_stroke(ctx, "#FF8FB1", lw=6)
    ctx.move_to(-60, 0); ctx.line_to(-60, -110); ctx.curve_to(-60, -190, 60, -190, 60, -110); ctx.line_to(60, 0); ctx.close_path()
    fill_stroke(ctx, "#6B4A2B", lw=6)
    ctx.restore()


def ground(ctx, y, col=GRASS):
    ctx.rectangle(-200, y, 1480, 1600); ctx.set_source_rgba(*hexc(col)); ctx.fill()
    ctx.move_to(-200, y); ctx.line_to(1280, y); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(8); ctx.stroke()


def worker(ctx, x, y, s, gt, dig=True):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -70, -150, 140, 190, 30); fill_stroke(ctx, "#3D5BFF", lw=7)
    ctx.restore()
    circle(ctx, x, y - 200 * s, 62 * s, "#F6D2B0", lw=6)
    ctx.new_path(); ctx.arc(x, y - 215 * s, 66 * s, math.pi, 0); ctx.set_source_rgba(*hexc("#8A5A35")); ctx.fill()
    for sx in (-1, 1):
        circle(ctx, x + sx * 22 * s, y - 195 * s, 8 * s, "#1B1B3A", lw=0)
    if dig:
        a = 0.4 * math.sin(gt * 6)
        ctx.save(); ctx.translate(x + 80 * s, y - 80 * s); ctx.rotate(0.6 + a)
        ctx.move_to(0, 0); ctx.line_to(0, 220 * s); ctx.set_source_rgba(*hexc("#8A5A35")); ctx.set_line_width(14 * s); ctx.stroke()
        rrect(ctx, -30 * s, 210 * s, 60 * s, 70 * s, 10 * s); fill_stroke(ctx, "#A9B4C2", lw=5)
        ctx.restore()


def timeline(ctx, lt, marks, hl=None, y=None, title=None):
    """marks: list of (year, text, color). Horizontal timeline 300..2026."""
    y = CY if y is None else y
    x0, x1 = 190, 1000
    p = ease_out_cubic(clamp(lt / 0.6))
    ctx.move_to(x0, y); ctx.line_to(x0 + (x1 - x0) * p, y); ctx.set_source_rgba(*hexc("#FFFFFF")); ctx.set_line_width(16); ctx.stroke()
    for i, (yr, txt, col) in enumerate(marks):
        xx = x0 + (x1 - x0) * (yr - 200) / (2100 - 200)
        s = pin(lt, 0.25 + 0.15 * i)
        circle(ctx, xx, y, 26 * s * (1.3 if hl == i else 1), col, lw=6)
        up = -1 if i % 2 == 0 else 1
        label(ctx, str(yr) + "年", xx, y + up * 95, 58, s=s)
        label(ctx, txt, xx, y + up * 175, 50, s=s, font="mochiy")
    if title:
        label(ctx, title, CX, CY - 420, 86, s=pin(lt, 0.1))


def bigtext(text, sub=None, color="#FFE14D", size=220):
    def vis(ctx, lt, d, gt):
        draw_sprite(ctx, text_sprite(text, size, color=color, hi="#FF3D7F", path=FONTS["dela"]), CX, CY - 60, pin(lt), 1, -0.04)
        if sub:
            draw_sprite(ctx, text_sprite(sub, 78, color="#FFFFFF", hi="#FFE14D", path=FONTS["mochiy"]), CX, CY + 160, pin(lt, 0.2), 1)
    return vis


# ---------------------------------------------------------------- scenes
def v_hook(ctx, lt, d, gt):
    coffin(ctx, CX, CY + 160, 1.15 * pin(lt), gt, lid=0.35 * clamp((lt - 0.5) / 0.6), inside="skel")
    skull(ctx, CX + 320, CY - 260, 80 * pin(lt, 0.3), gt, mood="wow")
    lbl(ctx, "ローマの棺に…", CX - 120, CY - 380, 92, s=pin(lt, 0.1))


def v_wrong(ctx, lt, d, gt):
    coffin(ctx, CX, CY + 220, 1.0 * pin(lt), gt, lid=0.5, inside="skel")
    roman(ctx, CX - 290, CY - 200, 0.8 * pin(lt, 0.15), gt)
    label(ctx, "?", CX - 120, CY - 360, 140, s=pin(lt, 0.3))
    monk(ctx, CX + 290, CY - 180, 0.8 * pin(lt, 0.25), gt, mood="wow")
    label(ctx, "!", CX + 450, CY - 380, 140, s=pin(lt, 0.4))


def v_coffin(ctx, lt, d, gt):
    coffin(ctx, CX, CY + 120, 1.25 * pin(lt), gt)
    lbl(ctx, "石の棺", CX, CY - 330, 110, s=pin(lt, 0.2))


def v_coffin_cross(ctx, lt, d, gt):
    coffin(ctx, CX, CY + 160, 1.3 * pin(lt), gt)
    q = clamp((lt - 0.4) / 0.4)
    if q > 0:
        ctx.new_path(); ctx.arc(CX, CY + 0, 380 * q, 0, 6.28); ctx.set_source_rgba(*hexc("#FF3D7F")); ctx.set_line_width(12); ctx.stroke()
    lbl(ctx, "ふたに十字架", CX, CY - 360, 96, s=pin(lt, 0.3))


def v_inscription(ctx, lt, d, gt):
    s = pin(lt)
    rrect(ctx, CX - 420, CY - 220, 840, 440, 30); fill_stroke(ctx, STONE, lw=10)
    lines = ["MEMORIAE VALER", "AMANDINI VALERII", "SUPERVENTOR ET", "MARCELLUS PATRI FEC"]
    for i, t in enumerate(lines):
        draw_sprite(ctx, text_sprite(t, 54, color="#5E5546", stroke="#F2EADA", stroke_w=3, shadow=False, path=FONTS["dela"]),
                    CX, CY - 150 + i * 100, pin(lt, 0.1 + 0.1 * i), 1)
    lbl(ctx, "ラテン語の文字", CX, CY - 330, 90, s=pin(lt, 0.2))


def v_sons(ctx, lt, d, gt):
    roman(ctx, CX, CY - 100, 0.95 * pin(lt), gt, beard=True)
    roman(ctx, CX - 330, CY + 60, 0.7 * pin(lt, 0.15), gt, col="#E7E2D6")
    roman(ctx, CX + 330, CY + 60, 0.7 * pin(lt, 0.25), gt, col="#E7E2D6")
    label(ctx, "お父さん", CX, CY - 400, 80, s=pin(lt, 0.3), font="mochiy")
    label(ctx, "むすこ2人", CX, CY + 360, 80, s=pin(lt, 0.4), font="mochiy")


def v_amandinus(ctx, lt, d, gt):
    roman(ctx, CX, CY + 20, 1.2 * pin(lt), gt, beard=True)
    lbl(ctx, "ウァレリウス・アマンディヌス", CX, CY - 380, 64, s=pin(lt, 0.2))
    lbl(ctx, "お金持ちのローマ時代の人", CX, CY + 330, 64, s=pin(lt, 0.35), font="mochiy")


def v_londinium(ctx, lt, d, gt):
    ground(ctx, CY + 220, "#C9B48A")
    for k in range(5):
        h = [240, 320, 200, 280, 220][k] * pin(lt, 0.06 * k)
        x = 120 + k * 210
        rrect(ctx, x - 80, CY + 220 - h, 160, h, 6); fill_stroke(ctx, "#F2E6C9", lw=6)
        ctx.move_to(x - 95, CY + 220 - h); ctx.line_to(x, CY + 220 - h - 70 * pin(lt, 0.06 * k)); ctx.line_to(x + 95, CY + 220 - h); ctx.close_path()
        fill_stroke(ctx, "#C2554B", lw=6)
    ctx.rectangle(-200, CY + 330, 1480, 140); ctx.set_source_rgba(*hexc("#4FA3E0")); ctx.fill()
    lbl(ctx, "ローマ時代のロンドン", CX, CY - 380, 80, s=pin(lt, 0.2))
    lbl(ctx, "ロンディニウム", CX, CY - 270, 80, s=pin(lt, 0.3), font="mochiy")


def v_kofun(ctx, lt, d, gt):
    ground(ctx, CY + 200, GRASS)
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 200); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(110, 0, 240, math.pi, 0); fill_stroke(ctx, "#5DAA45", lw=8)
    ctx.move_to(-420, 0); ctx.line_to(-330, -150); ctx.line_to(-60, -150); ctx.line_to(-10, 0); ctx.close_path(); fill_stroke(ctx, "#5DAA45", lw=8)
    ctx.restore()
    lbl(ctx, "日本は古墳時代", CX, CY - 380, 96, s=pin(lt, 0.2))


def v_genji(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 60); ctx.scale(s, s)
    rrect(ctx, -320, -230, 640, 420, 20); fill_stroke(ctx, "#F2E6C9", lw=8)
    for k in range(7):
        ctx.move_to(240 - k * 80, -190); ctx.line_to(240 - k * 80, 150); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(6); ctx.set_dash([24, 16]); ctx.stroke(); ctx.set_dash([])
    ctx.restore()
    lbl(ctx, "源氏物語のころ", CX, CY - 380, 96, s=pin(lt, 0.2))
    lbl(ctx, "日本は平安時代", CX, CY + 370, 78, s=pin(lt, 0.35), font="mochiy")


def v_abbey(ctx, lt, d, gt):
    ground(ctx, CY + 380, GRASS)
    abbey(ctx, CX, CY + 380, 1.05 * pin(lt))
    lbl(ctx, "ウェストミンスター寺院", CX, CY - 420, 74, s=pin(lt, 0.2))


def v_crown(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY); ctx.scale(s, s)
    ctx.move_to(-260, 120); ctx.line_to(-260, -80); ctx.line_to(-130, 20); ctx.line_to(0, -150); ctx.line_to(130, 20); ctx.line_to(260, -80); ctx.line_to(260, 120); ctx.close_path()
    fill_stroke(ctx, "#FFD23F", lw=10)
    for k, c in enumerate(["#FF3D7F", "#4FA3E0", "#4CC85A"]):
        circle(ctx, -150 + k * 150, 70, 30, c, lw=6)
    ctx.restore()
    sparkles(ctx, CX, CY, lt, 0.2, "#FFE14D", 12, 380)
    lbl(ctx, "王さまの戴冠式", CX, CY - 380, 96, s=pin(lt, 0.2))


def v_newton(ctx, lt, d, gt):
    for i, (nm, col) in enumerate([("ニュートン", "#4FA3E0"), ("ダーウィン", "#4CC85A")]):
        x = CX - 230 + i * 460
        rrect(ctx, x - 170, CY - 200, 340, 420, 40); fill_stroke(ctx, "#F2E6C9", lw=8)
        lbl(ctx, nm, x, CY + 300, 66, s=pin(lt, 0.15 * i), font="mochiy")
        circle(ctx, x, CY - 40, 100 * pin(lt, 0.15 * i), col, lw=8)
        label(ctx, "ねむる", x, CY + 120, 56, s=pin(lt, 0.15 * i + 0.1), font="mochiy")
    # apple
    circle(ctx, CX - 230, CY - 40, 50 * pin(lt, 0.2), "#E84B3C", lw=5)
    lbl(ctx, "有名な科学者も!", CX, CY - 400, 96, s=pin(lt, 0.3))


def v_dig(ctx, lt, d, gt):
    ground(ctx, CY + 120, SOIL)
    ctx.rectangle(-200, CY + 120 - 400, 1480, 0);
    coffin(ctx, CX, CY + 380, 0.7 * pin(lt, 0.2), gt)
    worker(ctx, CX - 330, CY + 120, 1.0 * pin(lt), gt)
    worker(ctx, CX + 330, CY + 120, 1.0 * pin(lt, 0.1), gt)
    lbl(ctx, "工事中に…", CX, CY - 380, 100, s=pin(lt, 0.2))


def v_1820(ctx, lt, d, gt):
    q = clamp((lt - 0.4) / 0.2)
    coffin(ctx, CX, CY + 180, 1.1 * pin(lt), gt, lid_pieces=q > 0, cross=q <= 0)
    if q > 0 and lt < 1.4:
        burst(ctx, CX, CY + 60, 160, gt, "#FFE14D")
    lbl(ctx, "ふたが6つに!", CX, CY - 380, 100, s=pin(lt, 0.4), rot=-0.04)


def v_1869(ctx, lt, d, gt):
    ground(ctx, CY + 260, GRASS)
    abbey(ctx, CX + 260, CY + 260, 0.6 * pin(lt))
    coffin(ctx, CX - 200, CY + 300, 0.6 * pin(lt, 0.15), gt)
    worker(ctx, CX - 430, CY + 260, 0.8 * pin(lt, 0.2), gt, dig=False)
    lbl(ctx, "1869年 発見!", CX, CY - 380, 100, s=pin(lt, 0.3))


def v_young(ctx, lt, d, gt):
    skeleton_stand(ctx, CX, CY + 300, 0.95 * pin(lt), gt, h=0.97)
    lbl(ctx, "がっしりした若い男", CX, CY - 420, 78, s=pin(lt, 0.2))
    lbl(ctx, "30才まで?", CX, CY + 400, 80, s=pin(lt, 0.35), font="mochiy")


def v_missing(ctx, lt, d, gt):
    coffin(ctx, CX, CY + 180, 1.1 * pin(lt), gt)
    for i, (x, y, sz) in enumerate([(CX - 300, CY - 260, 170), (CX + 300, CY - 220, 210)]):
        draw_sprite(ctx, text_sprite("?", sz, color="#FFE14D", path=FONTS["dela"]), x, y, pin(lt, 0.1 + i * 0.15), 1, 0.3 * math.sin(gt * 4 + i))
    lbl(ctx, "骨はどこ?", CX, CY - 400, 100, s=pin(lt, 0.2))


def v_open2016(ctx, lt, d, gt):
    coffin(ctx, CX, CY + 220, 1.15 * pin(lt), gt, lid=clamp((lt - 0.3) / 0.9), inside="skel")
    if lt > 1.1:
        sparkles(ctx, CX, CY + 120, lt, 1.1, "#FFE14D", 12, 360)
    lbl(ctx, "2016年 ふたを開けたら…", CX, CY - 400, 76, s=pin(lt, 0.1))


def v_skeleton_found(ctx, lt, d, gt):
    skeleton_stand(ctx, CX, CY + 300, 1.0 * pin(lt), gt, mood="wow")
    lbl(ctx, "ほぼ全身の骨!", CX, CY - 430, 96, s=pin(lt, 0.25))


def v_bones_check(ctx, lt, d, gt):
    skeleton_stand(ctx, CX - 170, CY + 300, 0.85 * pin(lt), gt)
    s = pin(lt, 0.2)
    ctx.save(); ctx.translate(CX + 250, CY - 60); ctx.scale(s, s); ctx.rotate(-0.5 + 0.15 * math.sin(gt * 3))
    circle(ctx, 0, 0, 110, "#BFE8FF", lw=14)
    ctx.move_to(80, 80); ctx.line_to(200, 200); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(34); ctx.stroke()
    ctx.restore()
    lbl(ctx, "骨のプロが調べ直す", CX, CY - 430, 80, s=pin(lt, 0.3))


def v_age(ctx, lt, d, gt):
    for i, (txt, sub, col) in enumerate([("30才まで", "1800年代", "#A9B4C2"), ("35〜49才", "今回", "#FFE14D")]):
        y = CY - 170 + i * 320
        rrect(ctx, CX - 400, y - 110, 800, 220, 40); fill_stroke(ctx, {"#A9B4C2": "#5B6B8A", "#FFE14D": "#FF3D7F"}[col], lw=8)
        label(ctx, sub, CX - 230, y, 60, s=pin(lt, 0.2 * i), font="mochiy")
        label(ctx, txt, CX + 120, y, 92, s=pin(lt, 0.2 * i + 0.1))
    lbl(ctx, "年れいは?", CX, CY - 430, 96, s=pin(lt, 0.1))


def v_height(ctx, lt, d, gt):
    skeleton_stand(ctx, CX - 220, CY + 330, 0.85 * pin(lt), gt, h=0.97)
    skeleton_stand(ctx, CX + 220, CY + 330, 0.85 * pin(lt, 0.2), gt, h=1.0, mood="wow")
    label(ctx, "約170cm", CX - 220, CY + 430, 64, s=pin(lt, 0.3))
    label(ctx, "約175cm", CX + 220, CY + 430, 64, s=pin(lt, 0.4))
    lbl(ctx, "身長は?", CX, CY - 440, 96, s=pin(lt, 0.1))


def v_c14(ctx, lt, d, gt):
    s = pin(lt)
    circle(ctx, CX, CY, 260 * s, "#FFFFFF", lw=12)
    a = -math.pi / 2 + gt * 1.6
    ctx.move_to(CX, CY); ctx.line_to(CX + 200 * s * math.cos(a), CY + 200 * s * math.sin(a)); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(16); ctx.stroke()
    draw_sprite(ctx, text_sprite("C-14", 90, color="#FF3D7F", stroke="#FFFFFF", path=FONTS["dela"]), CX, CY + 110, s, 1)
    lbl(ctx, "炭素の時計", CX, CY - 390, 100, s=pin(lt, 0.2))


def v_c14_decay(ctx, lt, d, gt):
    n = 16
    q = clamp((lt - 0.3) / 1.4)
    rnd = random.Random(4)
    gone = set(rnd.sample(range(n), int(n / 2 * q)))
    for k in range(n):
        x = CX - 330 + (k % 4) * 220; y = CY - 260 + (k // 4) * 170
        col = "#A9B4C2" if k in gone else "#FF3D7F"
        circle(ctx, x, y, 56 * pin(lt, 0.02 * k), col, lw=6)
    lbl(ctx, "5730年で半分に", CX, CY + 450, 84, s=pin(lt, 0.3))


def v_result(ctx, lt, d, gt):
    draw_sprite(ctx, text_sprite("987〜1052年", 130, color="#FFE14D", hi="#FF3D7F", path=FONTS["dela"]), CX, CY - 40, pin(lt), 1, -0.04)
    lbl(ctx, "骨の人が生きた時代", CX, CY - 330, 80, s=pin(lt, 0.2), font="mochiy")
    lbl(ctx, "約1000年前!", CX, CY + 220, 96, s=pin(lt, 0.4))


def v_gap(ctx, lt, d, gt):
    timeline(ctx, lt, [(350, "棺が作られた", "#B9AE9A"), (1020, "骨の人", "#FFE14D")], title="約650年の差!")
    p = clamp((lt - 0.7) / 0.6)
    if p > 0:
        x0 = 190 + 810 * (350 - 200) / 1900; x1 = 190 + 810 * (1020 - 200) / 1900
        ctx.new_path(); ctx.move_to(x0, CY - 30); ctx.curve_to(x0, CY - 220 * p, x1, CY - 220 * p, x1, CY - 30)
        ctx.set_source_rgba(*hexc("#FF3D7F")); ctx.set_line_width(12); ctx.stroke()


def v_recycle(ctx, lt, d, gt):
    coffin(ctx, CX, CY + 180, 1.0 * pin(lt), gt)
    s = pin(lt, 0.2)
    for k in range(3):
        a = gt * 1.2 + k * 2.09
        x, y = CX + 360 * math.cos(a), CY + 100 + 360 * math.sin(a) * 0.6
        ctx.save(); ctx.translate(x, y); ctx.rotate(a + 1.6); ctx.scale(s, s)
        ctx.move_to(-40, -20); ctx.line_to(40, 0); ctx.line_to(-40, 20); ctx.close_path(); fill_stroke(ctx, "#4CC85A", lw=5)
        ctx.restore()
    lbl(ctx, "棺のリサイクル!?", CX, CY - 400, 96, s=pin(lt, 0.3))


def v_wood(ctx, lt, d, gt):
    coffin(ctx, CX, CY + 220, 1.2 * pin(lt), gt, lid=1.0, inside="wood")
    lbl(ctx, "木の棺のあと!", CX, CY - 380, 100, s=pin(lt, 0.3))
    lbl(ctx, "白い石灰でくっきり", CX, CY + 440, 70, s=pin(lt, 0.45), font="mochiy")


def v_wood_in(ctx, lt, d, gt):
    q = ease_in_out(clamp((lt - 0.2) / 0.9))
    coffin(ctx, CX, CY + 260, 1.1 * pin(lt), gt, lid=1.0, inside="empty")
    ctx.save(); ctx.translate(CX, CY - 300 + 520 * q)
    rrect(ctx, -220, -50, 440, 100, 18); fill_stroke(ctx, WOOD, lw=8)
    ctx.restore()
    lbl(ctx, "石の棺の中に木の棺", CX, CY - 430, 78, s=pin(lt, 0.1))


def v_monk(ctx, lt, d, gt):
    ground(ctx, CY + 380, GRASS)
    abbey(ctx, CX + 300, CY + 380, 0.5 * pin(lt, 0.1))
    monk(ctx, CX - 120, CY + 150, 1.15 * pin(lt), gt)
    lbl(ctx, "修道士", CX, CY - 420, 110, s=pin(lt, 0.2))


def v_abbot(ctx, lt, d, gt):
    monk(ctx, CX, CY + 120, 1.3 * pin(lt), gt, staff=True)
    lbl(ctx, "修道院長", CX, CY - 420, 110, s=pin(lt, 0.2))
    s = pin(lt, 0.3)
    star(ctx, CX - 330, CY - 260, 50 * s, "#FFE14D"); star(ctx, CX + 330, CY - 240, 40 * s, "#FFE14D")


def v_two(ctx, lt, d, gt):
    monk(ctx, CX - 240, CY + 140, 0.9 * pin(lt), gt, staff=True)
    monk(ctx, CX + 240, CY + 140, 0.9 * pin(lt, 0.15), gt, staff=True, mood="wow")
    lbl(ctx, "エルフウィグ", CX - 240, CY + 420, 60, s=pin(lt, 0.3), font="mochiy")
    lbl(ctx, "ウルノス", CX + 240, CY + 420, 60, s=pin(lt, 0.4), font="mochiy")
    lbl(ctx, "候補は2人!", CX, CY - 430, 100, s=pin(lt, 0.2))


def v_aelfwig(ctx, lt, d, gt):
    monk(ctx, CX, CY + 140, 1.2 * pin(lt), gt, staff=True)
    lbl(ctx, "エルフウィグ", CX, CY - 420, 96, s=pin(lt, 0.2))
    lbl(ctx, "1020年ごろ死去", CX, CY + 440, 70, s=pin(lt, 0.35), font="mochiy")


def v_wulnoth(ctx, lt, d, gt):
    monk(ctx, CX, CY + 140, 1.2 * pin(lt), gt, staff=True, mood="wow")
    lbl(ctx, "ウルノス", CX, CY - 420, 96, s=pin(lt, 0.2))
    lbl(ctx, "1049年に死去", CX, CY + 440, 70, s=pin(lt, 0.35), font="mochiy")


def v_age_fit(ctx, lt, d, gt):
    w = 820; x0 = CX - w / 2
    p = ease_out_cubic(clamp(lt / 0.9))
    rrect(ctx, x0, CY - 70, w * p, 140, 30); fill_stroke(ctx, "#7FD3FF", lw=8)
    label(ctx, "20代で院長に", x0 + 150, CY - 170, 56, s=pin(lt, 0.2), font="mochiy")
    label(ctx, "50才近くで死去", x0 + w - 170, CY + 170, 56, s=pin(lt, 0.5), font="mochiy")
    lbl(ctx, "どちらも合う!", CX, CY - 400, 96, s=pin(lt, 0.4))


def v_mystery(ctx, lt, d, gt):
    monk(ctx, CX, CY + 160, 1.2 * pin(lt), gt)
    for i, (x, y, sz) in enumerate([(CX - 330, CY - 240, 170), (CX + 330, CY - 200, 210)]):
        draw_sprite(ctx, text_sprite("?", sz, color="#FFE14D", path=FONTS["dela"]), x, y, pin(lt, 0.1 + i * 0.15), 1, 0.3 * math.sin(gt * 4 + i))
    lbl(ctx, "まだ決まりではない", CX, CY - 430, 80, s=pin(lt, 0.2))


def v_dna(ctx, lt, d, gt):
    for k in range(14):
        y = CY - 320 + k * 50
        a = gt * 2 + k * 0.5
        x1 = CX + 150 * math.sin(a); x2 = CX - 150 * math.sin(a)
        ctx.move_to(x1, y); ctx.line_to(x2, y); ctx.set_source_rgba(1, 1, 1, 0.8); ctx.set_line_width(8); ctx.stroke()
        circle(ctx, x1, y, 18 * pin(lt, 0.03 * k), "#FF3D7F", lw=4)
        circle(ctx, x2, y, 18 * pin(lt, 0.03 * k), "#4FF0FF", lw=4)
    lbl(ctx, "これからの研究に期待", CX, CY + 420, 76, s=pin(lt, 0.3))


def v_thorney(ctx, lt, d, gt):
    ctx.rectangle(-200, CY - 300, 1480, 800); ctx.set_source_rgba(*hexc("#4FA3E0")); ctx.fill()
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 80); ctx.scale(s, s)
    ctx.new_path(); ctx.save(); ctx.scale(1.4, 0.7); ctx.arc(0, 0, 260, 0, 6.28); ctx.restore(); fill_stroke(ctx, GRASS, lw=8)
    for k in range(9):
        x = -300 + k * 75; y = -40 + 60 * math.sin(k * 1.7)
        ctx.move_to(x - 30, y + 30); ctx.line_to(x, y - 30); ctx.line_to(x + 30, y + 30)
        ctx.set_source_rgba(*hexc("#2E6B2A")); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()
    lbl(ctx, "いばらの島", CX, CY - 420, 110, s=pin(lt, 0.2))
    lbl(ctx, "テムズ川の中の島", CX, CY + 440, 72, s=pin(lt, 0.35), font="mochiy")


def v_edward(ctx, lt, d, gt):
    ground(ctx, CY + 380, GRASS)
    abbey(ctx, CX, CY + 380, 0.9 * pin(lt), col="#F2E6C9")
    s = pin(lt, 0.3)
    ctx.save(); ctx.translate(CX + 300, CY - 280); ctx.scale(s, s)
    ctx.move_to(-90, 50); ctx.line_to(-90, -30); ctx.line_to(-45, 10); ctx.line_to(0, -60); ctx.line_to(45, 10); ctx.line_to(90, -30); ctx.line_to(90, 50); ctx.close_path()
    fill_stroke(ctx, "#FFD23F", lw=7)
    ctx.restore()
    lbl(ctx, "1065年 新しい教会", CX, CY - 430, 84, s=pin(lt, 0.2))


def v_sacristy(ctx, lt, d, gt):
    ground(ctx, CY + 380, GRASS)
    abbey(ctx, CX + 200, CY + 380, 0.75 * pin(lt))
    s = pin(lt, 0.25)
    rrect(ctx, CX - 470, CY + 140, 330 * s, 240 * s, 10); fill_stroke(ctx, "#FFE14D", lw=7)
    lbl(ctx, "ここに新しい建物", CX - 300, CY + 70, 52, s=s, font="mochiy")
    lbl(ctx, "発くつ調査", CX, CY - 430, 100, s=pin(lt, 0.2))


def v_museum(ctx, lt, d, gt):
    rrect(ctx, CX - 440, CY - 300, 880, 640, 30); fill_stroke(ctx, "#F2E6C9", lw=10)
    coffin(ctx, CX, CY + 200, 0.85 * pin(lt), gt)
    for k in range(3):
        circle(ctx, CX - 300 + k * 300, CY - 200, 30 * pin(lt, 0.1 * k), "#FFE14D", lw=5)
    lbl(ctx, "博物館で見られる!", CX, CY - 420, 90, s=pin(lt, 0.2))


def v_weather(ctx, lt, d, gt):
    ground(ctx, CY + 380, GRASS)
    abbey(ctx, CX, CY + 380, 0.8 * pin(lt))
    p = ease_in_out(clamp((lt - 0.3) / 0.9))
    worker(ctx, CX + 80, CY - 120 - 40 * (1 - p), 0.5 * pin(lt, 0.2), gt, dig=False)
    s = pin(lt, 0.4)
    ctx.save(); ctx.translate(CX + 200, CY - 200); ctx.scale(s, s)
    ctx.move_to(-50, 20); ctx.curve_to(-40, -50, 30, -60, 50, 0); ctx.line_to(20, 30); ctx.close_path(); fill_stroke(ctx, "#FFD23F", lw=6)
    ctx.restore()
    lbl(ctx, "屋根に風見鶏!", CX, CY - 430, 96, s=pin(lt, 0.3))


def v_compare_now(ctx, lt, d, gt):
    for i, (yr, txt) in enumerate([("1869年", "見た目で予想"), ("今", "炭素の時計+骨のプロ")]):
        y = CY - 170 + i * 330
        rrect(ctx, CX - 420, y - 120, 840, 240, 40); fill_stroke(ctx, ["#5B6B8A", "#3D5BFF"][i], lw=8)
        label(ctx, yr, CX - 280, y, 70, s=pin(lt, 0.2 * i))
        label(ctx, txt, CX + 110, y, 50, s=pin(lt, 0.2 * i + 0.1), font="mochiy")
    lbl(ctx, "科学の力!", CX, CY - 430, 100, s=pin(lt, 0.4))


def v_future_lab(ctx, lt, d, gt):
    skeleton_stand(ctx, CX - 200, CY + 300, 0.75 * pin(lt), gt)
    s = pin(lt, 0.2)
    rrect(ctx, CX + 60, CY - 250, 380, 300, 30); fill_stroke(ctx, "#1B1B3A", lw=8)
    for k in range(4):
        ctx.move_to(CX + 100, CY - 190 + k * 60); ctx.line_to(CX + 100 + 300 * s * (0.4 + 0.6 * abs(math.sin(gt * 2 + k))), CY - 190 + k * 60)
        ctx.set_source_rgba(*hexc("#4FF0FF")); ctx.set_line_width(16); ctx.stroke()
    lbl(ctx, "骨が語る ひみつ", CX, CY - 430, 90, s=pin(lt, 0.3))


def v_comment(ctx, lt, d, gt):
    monk(ctx, CX - 230, CY + 140, 0.85 * pin(lt), gt, staff=True)
    monk(ctx, CX + 230, CY + 140, 0.85 * pin(lt, 0.15), gt, staff=True, mood="wow")
    label(ctx, "A", CX - 230, CY - 230, 110, s=pin(lt, 0.3))
    label(ctx, "B", CX + 230, CY - 230, 110, s=pin(lt, 0.4))
    lbl(ctx, "どっちだと思う?", CX, CY - 430, 96, s=pin(lt, 0.2))


def v_hello(ctx, lt, d, gt):
    skeleton_stand(ctx, CX, CY + 320, 1.0 * pin(lt), gt)
    lbl(ctx, "またね!", CX, CY - 430, 120, s=pin(lt, 0.2))


# ---------------------------------------------------------------- real photos (credit under the photo)
def P(name, credit, title=None, box=(940, 700), **kw):
    return photo_scene(name, credit, title, box=box, **kw)
