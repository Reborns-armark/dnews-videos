"""Visuals for the 'Riemann hypothesis proof claim with Claude (Alpöge, 2026-11-20)' episode (vertical stage, CX=540, CY=760)."""
import math, random
from common4 import *
from space2 import pin, CX, CY
from hera_vis import label, photo_scene, PHOTO_LAYOUT, v_question, v_longvideo

BLUE = "#4FA3FF"
PINK = "#FF3D7F"
YEL = "#FFE14D"
NAVY = "#1B1B3A"
GREEN = "#3FCF7A"
OPTS = {"short": False}
PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47}


def lbl(ctx, t, x, y, size=80, s=1.0, rot=0.0, font="dela", color="#FFFFFF"):
    label(ctx, t, x, y, size, color=color, s=s, rot=rot, font=font)


def txt(ctx, t, x, y, size=60, s=1.0, color="#FFFFFF", font="mochiy", rot=0.0):
    if color == NAVY:
        sp = text_sprite(t, size, color=NAVY, hi=PINK, stroke="#FFFFFF", stroke_w=3, shadow=False, path=FONTS[font])
    else:
        sp = text_sprite(t, size, color=color, hi=YEL, path=FONTS[font])
    draw_sprite(ctx, sp, x, y, s, 1, rot)


def P(name, credit, title=None, box=(940, 700), **kw):
    return photo_scene(name, credit, title, box=box, **kw)


def arrow(ctx, x0, y0, x1, y1, p=1.0, col="#FFFFFF"):
    xe, ye = x0 + (x1 - x0) * p, y0 + (y1 - y0) * p
    ctx.move_to(x0, y0); ctx.line_to(xe, ye); ctx.set_source_rgba(*hexc(col)); ctx.set_line_width(18); ctx.stroke()
    if p > 0.95:
        a = math.atan2(y1 - y0, x1 - x0)
        ctx.move_to(x1, y1); ctx.line_to(x1 - 50 * math.cos(a - 0.5), y1 - 50 * math.sin(a - 0.5))
        ctx.move_to(x1, y1); ctx.line_to(x1 - 50 * math.cos(a + 0.5), y1 - 50 * math.sin(a + 0.5)); ctx.stroke()


def bigtext(text, sub=None, color=YEL, size=220):
    def vis(ctx, lt, d, gt):
        draw_sprite(ctx, text_sprite(text, size, color=color, hi=PINK, path=FONTS["dela"]), CX, CY - 60, pin(lt), 1, -0.04)
        if sub:
            draw_sprite(ctx, text_sprite(sub, 78, color="#FFFFFF", hi=YEL, path=FONTS["mochiy"]), CX, CY + 160, pin(lt, 0.2), 1)
    return vis


# ---------------------------------------------------------------- props
def tile(ctx, x, y, n, s, hot):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -70, -70, 140, 140, 26); fill_stroke(ctx, YEL if hot else "#FFFFFF", lw=7)
    draw_sprite(ctx, text_sprite(str(n), 64, color=NAVY if hot else "#8A94A6", stroke="#FFFFFF", stroke_w=2, shadow=False, path=FONTS["dela"]), 0, 4, 1, 1)
    ctx.restore()


def laptop(ctx, x, y, s, gt=0.0, text="AI"):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -190, -230, 380, 250, 24); fill_stroke(ctx, "#2E3A5C", lw=8)
    rrect(ctx, -165, -205, 330, 200, 14); fill_stroke(ctx, "#8FD3FF", lw=5)
    ctx.move_to(-240, 20); ctx.line_to(240, 20); ctx.line_to(270, 70); ctx.line_to(-270, 70); ctx.close_path(); fill_stroke(ctx, "#A9B4C2", lw=7)
    for sx in (-1, 1):
        circle(ctx, sx * 55, -125, 22, "#FFFFFF", lw=5); circle(ctx, sx * 55 + 3 * math.sin(gt * 2), -122, 9, NAVY, lw=0)
    ctx.new_path(); ctx.arc(0, -80, 34, 0.3, math.pi - 0.3); ctx.set_source_rgba(*hexc(NAVY)); ctx.set_line_width(7); ctx.stroke()
    draw_sprite(ctx, text_sprite(text, 50, color="#FFFFFF", path=FONTS["dela"]), 0, -175, 1, 1)
    ctx.restore()


def person(ctx, x, y, s, gt=0.0, mood="smile", hair="#3A2A1A", coat="#FFFFFF"):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -110, -40, 220, 260, 60); fill_stroke(ctx, coat, lw=8)
    circle(ctx, 0, -130, 90, "#FFD9B0", lw=8)
    ctx.new_path(); ctx.arc(0, -150, 92, math.pi, 2 * math.pi); ctx.close_path(); fill_stroke(ctx, hair, lw=6)
    if mood == "sleep":
        for sx in (-1, 1):
            ctx.move_to(sx * 34 - 18, -125); ctx.line_to(sx * 34 + 18, -125)
        ctx.set_source_rgba(*hexc(NAVY)); ctx.set_line_width(7); ctx.stroke()
    else:
        for sx in (-1, 1):
            circle(ctx, sx * 34, -125, 24, "#FFFFFF", lw=5); circle(ctx, sx * 34, -125, 8, NAVY, lw=0)
    if mood == "wow":
        circle(ctx, 0, -80, 14, NAVY, lw=0)
    elif mood != "sleep":
        ctx.new_path(); ctx.arc(0, -95, 24, 0.3, math.pi - 0.3); ctx.set_source_rgba(*hexc(NAVY)); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


def paper(ctx, x, y, s, rot=0.0, title=None, lines=7):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -170, -230, 340, 460, 16); fill_stroke(ctx, "#FFF8E6", lw=7)
    for k in range(lines):
        ctx.move_to(-130, -140 + k * 50); ctx.line_to(130 - (k % 3) * 40, -140 + k * 50)
    ctx.set_source_rgba(*hexc("#B9B2A0")); ctx.set_line_width(10); ctx.stroke()
    if title:
        draw_sprite(ctx, text_sprite(title, 46, color=NAVY, stroke="#FFF8E6", stroke_w=2, shadow=False, path=FONTS["dela"]), 0, -190, 1, 1)
    ctx.restore()


def lock(ctx, x, y, s, gt=0.0, open_p=0.0):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, -90 - 60 * open_p, 100, math.pi, 2 * math.pi)
    ctx.set_source_rgba(*hexc("#A9B4C2")); ctx.set_line_width(36); ctx.stroke()
    rrect(ctx, -160, -100, 320, 260, 36); fill_stroke(ctx, YEL, lw=9)
    circle(ctx, 0, 10, 30, NAVY, lw=0); rrect(ctx, -12, 20, 24, 70, 10); ctx.set_source_rgba(*hexc(NAVY)); ctx.fill()
    ctx.restore()


def cicada(ctx, x, y, s, gt=0.0, num=None):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for sx in (-1, 1):
        ctx.save(); ctx.rotate(sx * (0.35 + 0.05 * math.sin(gt * 14)))
        ctx.scale(1, 1)
        ctx.new_path(); ctx.save(); ctx.translate(sx * 60, 60); ctx.scale(0.45, 1.0); ctx.arc(0, 0, 150, 0, 2 * math.pi); ctx.restore()
        ctx.set_source_rgba(0.85, 0.95, 1, 0.75); ctx.fill_preserve(); ctx.set_source_rgba(*hexc(NAVY)); ctx.set_line_width(6); ctx.stroke()
        ctx.restore()
    rrect(ctx, -60, -110, 120, 260, 55); fill_stroke(ctx, "#5A3B22", lw=8)
    circle(ctx, -55, -95, 26, "#E8323C", lw=6); circle(ctx, 55, -95, 26, "#E8323C", lw=6)
    if num:
        draw_sprite(ctx, text_sprite(num, 70, color=YEL, path=FONTS["dela"]), 0, 30, 1, 1)
    ctx.restore()


def bag(ctx, x, y, s, gt=0.0):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y + 8 * math.sin(gt * 3)); ctx.scale(s, s)
    circle(ctx, 0, 40, 190, "#D9B56A", lw=9)
    rrect(ctx, -70, -190, 140, 70, 24); fill_stroke(ctx, "#D9B56A", lw=8)
    draw_sprite(ctx, text_sprite("$", 200, color=GREEN, path=FONTS["dela"]), 0, 50, 1, 1)
    ctx.restore()


def checker(ctx, x, y, s, gt=0.0, stamp=0.0):
    """Original robot: the 'proof checker'."""
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y + 6 * math.sin(gt * 3)); ctx.scale(s, s)
    ctx.move_to(0, -250); ctx.line_to(0, -200); ctx.set_source_rgba(*hexc(NAVY)); ctx.set_line_width(8); ctx.stroke()
    circle(ctx, 0, -260, 18, PINK, lw=5)
    rrect(ctx, -150, -200, 300, 200, 50); fill_stroke(ctx, "#C7D3E8", lw=8)
    rrect(ctx, -110, -165, 220, 110, 30); fill_stroke(ctx, NAVY, lw=5)
    for sx in (-1, 1):
        circle(ctx, sx * 45, -110, 20, "#7FF0C0", lw=0)
    rrect(ctx, -120, 10, 240, 200, 40); fill_stroke(ctx, "#A9B4C2", lw=8)
    draw_sprite(ctx, text_sprite("チェック", 44, color=NAVY, stroke="#FFFFFF", stroke_w=2, shadow=False, path=FONTS["mochiy"]), 0, 110, 1, 1)
    if stamp > 0:
        ctx.save(); ctx.translate(200, 40); ctx.rotate(-0.2); ctx.scale(stamp, stamp)
        circle(ctx, 0, 0, 90, "#FFFFFF", stroke=GREEN, lw=12)
        ctx.move_to(-45, 0); ctx.line_to(-10, 40); ctx.line_to(50, -40); ctx.set_source_rgba(*hexc(GREEN)); ctx.set_line_width(20); ctx.stroke()
        ctx.restore()
    ctx.restore()


def check(ctx, x, y, s):
    if s < 1e-3:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    circle(ctx, 0, 0, 40, GREEN, lw=6)
    ctx.move_to(-20, 0); ctx.line_to(-5, 18); ctx.line_to(22, -16); ctx.set_source_rgba(1, 1, 1); ctx.set_line_width(10); ctx.stroke()
    ctx.restore()


def zline(ctx, lt, gt, n=9, x0=None, h=820, dots=True, label_half=True, off=False):
    """The 'critical line': a vertical line with zeros popping onto it."""
    x0 = CX if x0 is None else x0
    top, bot = CY - h / 2 + 40, CY + h / 2 + 40
    ctx.move_to(x0, top); ctx.line_to(x0, bot); ctx.set_source_rgba(*hexc(PINK)); ctx.set_line_width(14); ctx.stroke()
    if label_half:
        txt(ctx, "1/2 の線", x0, bot + 60, 56, s=pin(lt, 0.1))
    if dots:
        for k in range(n):
            yy = bot - 60 - k * (h - 120) / max(1, n - 1)
            dx = 0
            if off and k == n // 2:
                dx = 160
            circle(ctx, x0 + dx, yy, 26 * pin(lt, 0.15 + 0.1 * k), YEL, lw=6)


# ---------------------------------------------------------------- scenes
def v_hook(ctx, lt, d, gt):
    person(ctx, CX - 230, CY + 260, 0.9 * pin(lt), gt, "wow")
    laptop(ctx, CX + 220, CY + 260, 0.7 * pin(lt, 0.2), gt)
    for i, (x, y, sz) in enumerate([(CX - 300, CY - 230, 150), (CX + 300, CY - 170, 190)]):
        draw_sprite(ctx, text_sprite("!?", sz, color=YEL, path=FONTS["dela"]), x, y, pin(lt, 0.2 + i * 0.15), 1, 0.2 * math.sin(gt * 4 + i))
    lbl(ctx, "リーマン予想", CX, CY - 440, 110, s=pin(lt, 0.1))


v_167 = bigtext("167年", "だれもとけなかった!")
v_167_big = bigtext("167年", None, size=330)
v_1m = bigtext("$100万", "日本円で1億円以上!", color=GREEN, size=200)
v_61gb = bigtext("61.5GB", "証明のデータ", size=190)
v_files = bigtext("175,187", "ファイル!", size=170)
v_27min = bigtext("27分42秒", "チェック完了!", size=150)
v_10t = bigtext("10兆個", "以上たしかめた", size=230)
v_4p = bigtext("4ページ", "発表のメモ", size=220)
v_200 = bigtext("200才", "リーマンの誕生日", size=230)
v_1000y = bigtext("1000年", "ねむっても…", size=250)


def v_ai_human(ctx, lt, d, gt):
    person(ctx, CX - 230, CY + 220, 0.95 * pin(lt), gt)
    laptop(ctx, CX + 220, CY + 240, 0.72 * pin(lt, 0.15), gt)
    for k in range(5):
        a = gt * 1.5 + k * 1.25
        star(ctx, CX + 260 * math.cos(a) * 0.4, CY - 120 + 60 * math.sin(a), 26 * pin(lt, 0.3), YEL)
    lbl(ctx, "人間 + AI", CX, CY - 430, 110, s=pin(lt, 0.1))


def v_primes(ctx, lt, d, gt):
    for i in range(20):
        n = i + 1
        x = CX - 330 + (i % 4) * 220; y = CY - 300 + (i // 4) * 190
        hot = n in PRIMES and lt > 0.6
        tile(ctx, x, y, n, 0.95 * pin(lt, 0.02 * i), hot)
    lbl(ctx, "素数はどれ?", CX, CY - 470, 96, s=pin(lt, 0.05))


def v_prime_def(ctx, lt, d, gt):
    card(ctx, CX - 450, CY - 300, 900, 230)
    txt(ctx, "6 = 2 × 3", CX, CY - 185, 100, s=pin(lt, 0.1), color=NAVY)
    card(ctx, CX - 450, CY + 0, 900, 230)
    txt(ctx, "7 = 1 × {7} だけ!", CX, CY + 115, 100, s=pin(lt, 0.4), color=NAVY)
    lbl(ctx, "わり切れない数", CX, CY - 440, 96, s=pin(lt, 0.05))
    piko(ctx, CX, CY + 440, gt, 0.7 * pin(lt, 0.5), "smile")


def v_atoms(ctx, lt, d, gt):
    for k, (n, col) in enumerate([(2, YEL), (3, BLUE), (5, PINK), (7, GREEN)]):
        x = CX - 330 + k * 220
        circle(ctx, x, CY - 60, 90 * pin(lt, 0.1 * k), col, lw=7)
        txt(ctx, str(n), x, CY - 60, 90, s=pin(lt, 0.1 * k + 0.1), color=NAVY, font="dela")
    txt(ctx, "12 = 2×2×3", CX, CY + 220, 92, s=pin(lt, 0.5))
    lbl(ctx, "数の「原子」", CX, CY - 430, 104, s=pin(lt, 0.05))


def v_infinite(ctx, lt, d, gt):
    for k in range(9):
        q = (k + (gt * 0.6) % 1) / 9
        s = 1.2 - q
        x = CX + (k - 4) * 10; y = CY + 380 - q * 700
        n = sorted(PRIMES)[k]
        tile(ctx, CX + (q - 0.5) * 0, y, n, 0.9 * s * pin(lt, 0.05 * k), True)
    lbl(ctx, "どこまでもある!", CX, CY - 440, 100, s=pin(lt, 0.1))


def v_irregular(ctx, lt, d, gt):
    y = CY + 60
    ctx.move_to(60, y); ctx.line_to(1020, y); ctx.set_source_rgba(1, 1, 1); ctx.set_line_width(10); ctx.stroke()
    for n in range(1, 48):
        x = 60 + n * 20
        if n in PRIMES:
            circle(ctx, x, y, 18 * pin(lt, 0.012 * n), YEL, lw=4)
            if n in (2, 3, 5, 7, 23, 29, 47):
                txt(ctx, str(n), x, y - 70 if n % 2 else y + 70, 44, s=pin(lt, 0.012 * n + 0.1))
    txt(ctx, "ならび方が バラバラ…", CX, CY + 300, 76, s=pin(lt, 0.5))
    lbl(ctx, "ルールはある?", CX, CY - 400, 100, s=pin(lt, 0.05))


def v_crypto(ctx, lt, d, gt):
    lock(ctx, CX, CY + 40, 1.0 * pin(lt), gt)
    rrect(ctx, CX - 420, CY + 300, 300, 190, 24); fill_stroke(ctx, BLUE, lw=7)
    txt(ctx, "カード", CX - 270, CY + 395, 54, s=pin(lt, 0.3))
    rrect(ctx, CX + 120, CY + 300, 300, 190, 24); fill_stroke(ctx, PINK, lw=7)
    txt(ctx, "ネット", CX + 270, CY + 395, 54, s=pin(lt, 0.4))
    lbl(ctx, "暗号に素数!", CX, CY - 430, 104, s=pin(lt, 0.1))


def v_cicada(ctx, lt, d, gt):
    cicada(ctx, CX - 230, CY + 40, 1.0 * pin(lt), gt, "13")
    cicada(ctx, CX + 230, CY + 40, 1.0 * pin(lt, 0.2), gt + 1, "17")
    lbl(ctx, "素数ゼミ", CX, CY - 430, 110, s=pin(lt, 0.1))
    txt(ctx, "13年・17年ごとに大発生", CX, CY + 380, 64, s=pin(lt, 0.4))


def v_paper1859(ctx, lt, d, gt):
    paper(ctx, CX - 60, CY + 40, 1.3 * pin(lt), -0.08, "1859年")
    paper(ctx, CX + 80, CY + 80, 1.3 * pin(lt, 0.15), 0.06, "10ページ")
    lbl(ctx, "たった10ページ!", CX, CY - 440, 100, s=pin(lt, 0.2))


def v_zeta_sum(ctx, lt, d, gt):
    terms = ["1", "+ 1/4", "+ 1/9", "+ 1/16", "+ …"]
    for k, t in enumerate(terms):
        txt(ctx, t, CX - 360 + k * 190, CY - 120, 76, s=pin(lt, 0.15 * k), font="dela")
    txt(ctx, "= π² ÷ 6 !", CX, CY + 120, 120, s=pin(lt, 0.9), color=YEL, font="dela")
    lbl(ctx, "オイラーの発見", CX, CY - 430, 100, s=pin(lt, 0.05))
    piko(ctx, CX, CY + 430, gt, 0.6 * pin(lt, 1.0), "wow")


def v_zeta_machine(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 40); ctx.scale(s, s)
    rrect(ctx, -300, -220, 600, 440, 50); fill_stroke(ctx, "#7B5CFF", lw=9)
    draw_sprite(ctx, text_sprite("ζ", 260, color=YEL, path=FONTS["dela"]), 0, -10, 1, 1, 0.1 * math.sin(gt * 2))
    ctx.restore()
    arrow(ctx, CX - 470, CY + 40, CX - 320, CY + 40, ease_out_cubic(clamp(lt / 0.5)))
    arrow(ctx, CX + 320, CY + 40, CX + 470, CY + 40, ease_out_cubic(clamp((lt - 0.4) / 0.5)))
    txt(ctx, "数", CX - 470, CY - 60, 60, s=pin(lt, 0.1))
    txt(ctx, "答え", CX + 460, CY - 60, 60, s=pin(lt, 0.5))
    lbl(ctx, "ゼータ関数", CX, CY - 430, 110, s=pin(lt, 0.05))


def v_zeros(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX - 280, CY - 80); ctx.scale(0.55 * s, 0.55 * s)
    rrect(ctx, -300, -220, 600, 440, 50); fill_stroke(ctx, "#7B5CFF", lw=9)
    draw_sprite(ctx, text_sprite("ζ", 260, color=YEL, path=FONTS["dela"]), 0, -10, 1, 1)
    ctx.restore()
    arrow(ctx, CX - 80, CY - 80, CX + 130, CY - 80, ease_out_cubic(clamp((lt - 0.2) / 0.4)))
    txt(ctx, "0", CX + 260, CY - 80, 220, s=pin(lt, 0.6), color=YEL, font="dela")
    txt(ctx, "答えが 0 になる場所", CX, CY + 260, 76, s=pin(lt, 0.4))
    lbl(ctx, "ゼロ点", CX, CY - 430, 120, s=pin(lt, 0.05))


def v_line(ctx, lt, d, gt):
    zline(ctx, lt, gt)
    lbl(ctx, "ぜんぶ1本の線の上?", CX, CY - 470, 86, s=pin(lt, 0.05))


def v_line_off(ctx, lt, d, gt):
    zline(ctx, lt, gt, off=True)
    if lt > 0.8:
        draw_sprite(ctx, text_sprite("×", 160, color=PINK, path=FONTS["dela"]), CX + 160, CY + 40, pin(lt, 0.8), 1)
    lbl(ctx, "1個でもはみ出したら…", CX, CY - 470, 80, s=pin(lt, 0.05))


def v_computer_count(ctx, lt, d, gt):
    laptop(ctx, CX - 200, CY + 220, 0.75 * pin(lt), gt, "計算中")
    zline(ctx, lt, gt, n=7, x0=CX + 280, h=700, label_half=False)
    lbl(ctx, "コンピューターで確認", CX, CY - 450, 86, s=pin(lt, 0.05))


def v_hilbert(ctx, lt, d, gt):
    person(ctx, CX, CY + 220, 1.1 * pin(lt), gt, "sleep", hair="#9A9A9A", coat="#5B6B8A")
    for k in range(3):
        q = (gt * 0.6 + k / 3) % 1
        txt(ctx, "Z", CX + 150 + 80 * q, CY - 60 - 200 * q, int(60 + 50 * q), s=pin(lt, 0.2), font="dela")
    lbl(ctx, "ヒルベルトの言葉", CX, CY - 440, 96, s=pin(lt, 0.05))


def v_seven(ctx, lt, d, gt):
    for k in range(7):
        x = CX - 360 + (k % 4) * 240; y = CY - 180 + (k // 4) * 300
        rrect(ctx, x - 95, y - 110, 190, 220, 30)
        fill_stroke(ctx, GREEN if k == 6 else ("#FFB3C7" if k == 0 else "#FFFFFF"), lw=7)
        txt(ctx, "?" if k not in (0, 6) else ("RH" if k == 0 else "済"), x, y, 90, s=pin(lt, 0.07 * k), color=NAVY, font="mochiy")
    lbl(ctx, "7つの難問", CX, CY - 450, 110, s=pin(lt, 0.05))
    bag(ctx, CX + 300, CY + 420, 0.45 * pin(lt, 0.6), gt)


def v_money(ctx, lt, d, gt):
    bag(ctx, CX, CY + 60, 1.1 * pin(lt), gt)
    lbl(ctx, "賞金100万ドル!", CX, CY - 440, 104, s=pin(lt, 0.1))


def v_who(ctx, lt, d, gt):
    person(ctx, CX - 220, CY + 200, 1.0 * pin(lt), gt)
    laptop(ctx, CX + 230, CY + 230, 0.7 * pin(lt, 0.2), gt, "Claude")
    lbl(ctx, "アルポゲさん", CX, CY - 440, 104, s=pin(lt, 0.1))


def v_remark(ctx, lt, d, gt):
    for k in range(4):
        paper(ctx, CX - 180 + k * 120, CY + 60 + k * 10, 0.9 * pin(lt, 0.12 * k), -0.1 + k * 0.07, "REMARK" if k == 3 else None)
    lbl(ctx, "11月20日に発表", CX, CY - 440, 100, s=pin(lt, 0.05))


def v_months(ctx, lt, d, gt):
    for k in range(6):
        x = CX - 375 + (k % 3) * 375; y = CY - 120 + (k // 3) * 330
        rrect(ctx, x - 150, y - 130, 300, 260, 30); fill_stroke(ctx, "#FFFFFF", lw=7)
        ctx.rectangle(x - 150, y - 130, 300, 70); ctx.set_source_rgba(*hexc(PINK)); ctx.fill()
        if lt > 0.2 + 0.12 * k:
            check(ctx, x, y + 30, 1.4)
    lbl(ctx, "何か月も いっしょに", CX, CY - 450, 86, s=pin(lt, 0.05))


def v_finish(ctx, lt, d, gt):
    ctx.move_to(CX + 300, CY - 260); ctx.line_to(CX + 300, CY + 420); ctx.set_source_rgba(1, 1, 1); ctx.set_line_width(10); ctx.stroke()
    for k in range(6):
        ctx.rectangle(CX + 300, CY - 260 + k * 40, 120, 40); ctx.set_source_rgba(*(hexc(NAVY) if k % 2 else (1, 1, 1, 1))); ctx.fill()
    run = ease_out_cubic(clamp(lt / max(0.6, d * 0.8)))
    laptop(ctx, CX - 350 + 560 * run, CY + 240, 0.55 * pin(lt), gt)
    person(ctx, CX - 380 + 380 * run, CY + 260, 0.6 * pin(lt), gt)
    lbl(ctx, "ゴール前で大活やく", CX, CY - 450, 86, s=pin(lt, 0.05))


def v_lean(ctx, lt, d, gt):
    checker(ctx, CX - 60, CY + 120, 1.0 * pin(lt), gt, pin(lt, 0.8))
    lbl(ctx, "Lean(リーン)", CX, CY - 440, 110, s=pin(lt, 0.05))


def v_lean_rule(ctx, lt, d, gt):
    for k in range(5):
        y = CY - 260 + k * 150
        rrect(ctx, CX - 420, y - 55, 640, 110, 24); fill_stroke(ctx, "#FFFFFF", lw=6)
        txt(ctx, f"ステップ{k + 1}", CX - 100, y, 56, s=pin(lt, 0.1 * k), color=NAVY)
        check(ctx, CX + 330, y, 1.2 * pin(lt, 0.3 + 0.15 * k))
    lbl(ctx, "1歩ずつ ぜんぶ確認", CX, CY - 450, 86, s=pin(lt, 0.05))


def v_file_stack(ctx, lt, d, gt):
    for k in range(10):
        q = pin(lt, 0.05 * k)
        rrect(ctx, CX - 260 + k * 8, CY + 380 - k * 70, 520, 60, 12); fill_stroke(ctx, BLUE if k % 2 else "#FFFFFF", lw=5)
    lbl(ctx, "ファイルの山!", CX, CY - 450, 104, s=pin(lt, 0.05))


def v_movies(ctx, lt, d, gt):
    for k in range(12):
        x = CX - 375 + (k % 4) * 250; y = CY - 200 + (k // 4) * 220
        rrect(ctx, x - 100, y - 70, 200, 140, 18); fill_stroke(ctx, "#2E3A5C", lw=6)
        ctx.move_to(x - 20, y - 35); ctx.line_to(x + 35, y); ctx.line_to(x - 20, y + 35); ctx.close_path()
        ctx.set_source_rgba(*hexc(YEL)); ctx.fill()
    lbl(ctx, "映画 何十本ぶん!?", CX, CY - 450, 92, s=pin(lt, 0.05))


def v_two_kernels(ctx, lt, d, gt):
    checker(ctx, CX - 230, CY + 150, 0.75 * pin(lt), gt, pin(lt, 0.6))
    checker(ctx, CX + 230, CY + 150, 0.75 * pin(lt, 0.15), gt + 1, pin(lt, 0.8))
    lbl(ctx, "べつべつの係でも合格", CX, CY - 450, 84, s=pin(lt, 0.05))


def v_running(ctx, lt, d, gt):
    checker(ctx, CX, CY + 150, 0.9 * pin(lt), gt)
    for k in range(3):
        circle(ctx, CX - 80 + k * 80, CY - 230, 22 * (0.6 + 0.4 * abs(math.sin(gt * 3 + k))), YEL, lw=4)
    lbl(ctx, "まだ続くチェックも", CX, CY - 450, 90, s=pin(lt, 0.05))


def v_experts(ctx, lt, d, gt):
    for k, (x, hair) in enumerate([(CX - 300, "#3A2A1A"), (CX, "#9A9A9A"), (CX + 300, "#6B3A1A")]):
        person(ctx, x, CY + 240, 0.7 * pin(lt, 0.12 * k), gt + k, "wow" if k == 1 else "smile", hair=hair)
    for k in range(3):
        draw_sprite(ctx, text_sprite("!?", 100, color=YEL, path=FONTS["dela"]), CX - 300 + 300 * k, CY - 120, pin(lt, 0.4 + 0.1 * k), 1)
    lbl(ctx, "数学者もびっくり", CX, CY - 450, 96, s=pin(lt, 0.05))


def v_maynard(ctx, lt, d, gt):
    person(ctx, CX, CY + 260, 1.0 * pin(lt), gt)
    s = pin(lt, 0.2)
    ctx.save(); ctx.translate(CX, CY - 170); ctx.scale(s, s)
    rrect(ctx, -420, -130, 840, 260, 60); fill_stroke(ctx, "#FFFFFF", lw=7)
    draw_sprite(ctx, text_sprite("歴史に残る\n一歩になる!", 64, color=NAVY, hi=PINK, stroke="#FFFFFF", stroke_w=2, shadow=False, path=FONTS["mochiy"]), 0, 0, 1, 1)
    ctx.restore()
    lbl(ctx, "フィールズ賞の数学者", CX, CY - 460, 82, s=pin(lt, 0.05))


def v_human_read(ctx, lt, d, gt):
    person(ctx, CX - 200, CY + 240, 0.9 * pin(lt), gt, "wow")
    for k in range(5):
        paper(ctx, CX + 200 + k * 14, CY + 200 - k * 20, 0.7 * pin(lt, 0.08 * k), 0.05 * k)
    lbl(ctx, "人間が わかるまで", CX, CY - 450, 92, s=pin(lt, 0.05))


def v_years(ctx, lt, d, gt):
    for k, t in enumerate(["雑誌にのる", "2年まつ", "賞をきめる"]):
        y = CY - 200 + k * 260
        rrect(ctx, CX - 380, y - 90, 760, 180, 40); fill_stroke(ctx, ["#FFFFFF", YEL, GREEN][k], lw=7)
        txt(ctx, t, CX, y, 80, s=pin(lt, 0.2 * k), color=NAVY)
        if k < 2:
            arrow(ctx, CX, y + 95, CX, y + 165, ease_out_cubic(clamp((lt - 0.2 * k - 0.15) / 0.3)))
    lbl(ctx, "賞はまだ先", CX, CY - 450, 104, s=pin(lt, 0.05))


def v_timeline(ctx, lt, d, gt):
    y = CY + 60
    ctx.move_to(100, y); ctx.line_to(980, y); ctx.set_source_rgba(1, 1, 1); ctx.set_line_width(12); ctx.stroke()
    for k, (yr, x) in enumerate([("1859", 160), ("1900", 400), ("2000", 700), ("2026", 920)]):
        circle(ctx, x, y, 30 * pin(lt, 0.15 * k), [BLUE, GREEN, YEL, PINK][k], lw=6)
        txt(ctx, yr, x, y - 90, 56, s=pin(lt, 0.15 * k + 0.1), font="dela")
    lbl(ctx, "167年の旅", CX, CY - 400, 110, s=pin(lt, 0.05))


def v_cake(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 160); ctx.scale(s, s)
    rrect(ctx, -300, -60, 600, 240, 30); fill_stroke(ctx, "#FFB3C7", lw=8)
    rrect(ctx, -220, -220, 440, 170, 30); fill_stroke(ctx, "#FFFFFF", lw=8)
    for k in range(5):
        x = -160 + k * 80
        rrect(ctx, x - 10, -320, 20, 100, 6); fill_stroke(ctx, BLUE, lw=4)
        circle(ctx, x, -340 + 4 * math.sin(gt * 9 + k), 14, YEL, lw=3)
    draw_sprite(ctx, text_sprite("200", 90, color=PINK, path=FONTS["dela"]), 0, -135, 1, 1)
    ctx.restore()
    lbl(ctx, "生まれて200年!", CX, CY - 440, 100, s=pin(lt, 0.1))


def v_fire(ctx, lt, d, gt):
    paper(ctx, CX - 120, CY + 140, 1.0 * pin(lt), -0.1)
    paper(ctx, CX + 120, CY + 160, 1.0 * pin(lt, 0.1), 0.12)
    for k in range(7):
        q = (gt * 1.2 + k / 7) % 1
        x = CX - 240 + k * 80
        ctx.new_path(); ctx.arc(x, CY + 360 - 200 * q, 40 * (1 - q) + 10, 0, 6.283)
        ctx.set_source_rgba(1, 0.45 + 0.4 * q, 0.1, 0.85 * (1 - q)); ctx.fill()
    lbl(ctx, "メモがもやされた!?", CX, CY - 440, 92, s=pin(lt, 0.05))


def v_found(ctx, lt, d, gt):
    paper(ctx, CX, CY + 120, 1.3 * pin(lt), 0.04, "1932年")
    for k in range(8):
        a = k / 8 * 6.283 + gt
        star(ctx, CX + 330 * math.cos(a), CY + 120 + 330 * math.sin(a), 22 * pin(lt, 0.3), YEL)
    lbl(ctx, "70年後に大発見", CX, CY - 440, 100, s=pin(lt, 0.05))


def v_myth(ctx, lt, d, gt):
    lock(ctx, CX, CY + 80, 0.95 * pin(lt), gt, 0.0)
    if lt > 0.5:
        draw_sprite(ctx, text_sprite("こわれない", 80, color=GREEN, path=FONTS["dela"]), CX, CY + 400, pin(lt, 0.5), 1)
    lbl(ctx, "暗号はだいじょうぶ?", CX, CY - 440, 90, s=pin(lt, 0.05))


def v_future(ctx, lt, d, gt):
    person(ctx, CX - 220, CY + 240, 0.9 * pin(lt), gt)
    laptop(ctx, CX + 220, CY + 260, 0.7 * pin(lt, 0.1), gt)
    for k in range(9):
        a = k / 9 * 6.283 + gt * 0.5
        star(ctx, CX + 400 * math.cos(a), CY - 60 + 200 * math.sin(a), 24 * pin(lt, 0.2), [YEL, "#FFFFFF", "#8FD3FF"][k % 3])
    lbl(ctx, "数学の新しい時代?", CX, CY - 450, 92, s=pin(lt, 0.05))


def v_physics(ctx, lt, d, gt):
    for k in range(3):
        ctx.new_path(); ctx.save(); ctx.translate(CX, CY + 80); ctx.rotate(k * 1.05 + gt * 0.5); ctx.scale(1, 0.35)
        ctx.arc(0, 0, 300, 0, 6.283); ctx.restore(); ctx.set_source_rgba(*hexc(BLUE)); ctx.set_line_width(8); ctx.stroke()
    circle(ctx, CX, CY + 80, 70 * pin(lt), PINK, lw=7)
    lbl(ctx, "物理ともつながる", CX, CY - 430, 96, s=pin(lt, 0.05))


def v_comment(ctx, lt, d, gt):
    person(ctx, CX - 200, CY + 220, 0.8 * pin(lt), gt, "wow")
    laptop(ctx, CX + 220, CY + 240, 0.6 * pin(lt, 0.1), gt)
    lbl(ctx, "どう思う?", CX, CY - 380, 110, s=pin(lt, 0.2))


def v_hello(ctx, lt, d, gt):
    piko(ctx, CX, CY + 200, gt, 1.0 * pin(lt), "smile")
    lbl(ctx, "またね!", CX, CY - 400, 120, s=pin(lt, 0.2))
