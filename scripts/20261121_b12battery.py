"""Short (テック) 2026-11-21: rechargeable zinc-air battery using vitamin B12"""
import math
from common4 import *
from space2 import pin, CX, CY, v_comment
from space3 import eyes

PILL_A, PILL_B = "#FF4F8B", "#FFE14D"
ZINC = "#B8C4D6"


def pill(ctx, x, y, s, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -150, -60, 150, 120, 60); fill_stroke(ctx, PILL_A, lw=8)
    rrect(ctx, 0, -60, 150, 120, 60); fill_stroke(ctx, PILL_B, lw=8)
    ctx.new_path(); ctx.arc(-80, -25, 18, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.6); ctx.fill()
    ctx.restore()


def battery(ctx, x, y, s, level=1.0, col="#3CE07A"):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -130, -220, 260, 440, 40); fill_stroke(ctx, "#FFFFFF", lw=10)
    rrect(ctx, -50, -260, 100, 50, 14); fill_stroke(ctx, "#FFFFFF", lw=10)
    h = 380 * clamp(level)
    if h > 4:
        rrect(ctx, -100, 190 - h, 200, h, 24); fill_stroke(ctx, col, lw=0)
    ctx.move_to(25, -90); ctx.line_to(-35, 20); ctx.line_to(10, 20); ctx.line_to(-20, 110); ctx.line_to(45, -10); ctx.line_to(0, -10); ctx.close_path()
    fill_stroke(ctx, "#FFE14D", lw=7)
    ctx.restore()


def bubble(ctx, x, y, r, label="O₂"):
    circle(ctx, x, y, r, "#BFE9FF", lw=6)
    if r > 30:
        draw_sprite(ctx, text_sprite(label, int(r * 0.8), color="#1B6FB0", stroke="#FFFFFF", stroke_w=4, path=FONTS["dela"]), x, y, 1, 1)


def v_hook(ctx, lt, d, gt):
    pill(ctx, CX - 170, CY - 60, 1.1 * pin(lt), -0.3 + 0.08 * math.sin(gt * 3))
    battery(ctx, CX + 230, CY + 40, 0.75 * pin(lt, 0.15), level=0.5 + 0.5 * math.sin(gt * 2) ** 2)
    draw_sprite(ctx, text_sprite("?!", 200, color="#FFE14D", path=FONTS["dela"]), CX + 20, CY - 330, pin(lt, 0.25), 1, 0.15 * math.sin(gt * 5))


def v_b12(ctx, lt, d, gt):
    burst(ctx, CX, CY - 40, 360 * pin(lt), gt, PILL_B)
    draw_sprite(ctx, text_sprite("ビタミンB12", 130, color="#FF4F8B", stroke="#FFFFFF", stroke_w=8, path=FONTS["dela"]), CX, CY - 60, pin(lt, 0.05), 1, -0.05)
    sparkles(ctx, CX, CY, lt, 0.1, "#FFFFFF", 14, 460)


def v_spain(ctx, lt, d, gt):
    circle(ctx, CX, CY, 300 * pin(lt), "#3FA9F5", lw=10)
    ctx.save(); ctx.translate(CX - 30, CY - 60); s = pin(lt, 0.15); ctx.scale(s, s)
    rrect(ctx, -90, -60, 180, 120, 20); fill_stroke(ctx, "#FFC84A", lw=8)
    ctx.restore()
    draw_sprite(ctx, text_sprite("スペイン", 110, hi="#FFE14D", path=FONTS["dela"]), CX, CY + 360, pin(lt, 0.25), 1, -0.04)


def v_zincair(ctx, lt, d, gt):
    rrect(ctx, CX - 330, CY - 80, 260, 300, 30); fill_stroke(ctx, ZINC, lw=10)
    draw_sprite(ctx, text_sprite("亜鉛", 90, color="#1B1B3A", stroke="#FFFFFF", stroke_w=5, path=FONTS["dela"]), CX - 200, CY + 70, pin(lt), 1)
    for k in range(5):
        y = CY + 200 - ((lt * 180 + k * 110) % 540)
        bubble(ctx, CX + 200 + 60 * math.sin(k * 2 + gt), y, 46 + 8 * (k % 2))
    draw_sprite(ctx, text_sprite("+", 160, color="#FFE14D", path=FONTS["dela"]), CX - 10, CY + 60, pin(lt, 0.2), 1)
    draw_sprite(ctx, text_sprite("空気", 90, hi="#FFE14D", path=FONTS["dela"]), CX + 200, CY - 330, pin(lt, 0.3), 1)


def v_cobalt(ctx, lt, d, gt):
    s = pin(lt)
    for k in range(8):
        a = k * math.pi / 4 + gt * 0.6
        x, y = CX + 260 * s * math.cos(a), CY + 260 * s * math.sin(a)
        ctx.move_to(CX, CY); ctx.line_to(x, y); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(10); ctx.stroke()
        circle(ctx, x, y, 34 * s, ["#7FD3FF", "#FF8FB1", "#B6F07A"][k % 3], lw=6)
    circle(ctx, CX, CY, 120 * pin(lt, 0.15), "#4F7BFF", lw=10)
    draw_sprite(ctx, text_sprite("Co", 120, color="#FFFFFF", path=FONTS["dela"]), CX, CY, pin(lt, 0.2), 1)
    draw_sprite(ctx, text_sprite("コバルト", 90, hi="#FFE14D", path=FONTS["dela"]), CX, CY - 400, pin(lt, 0.3), 1, 0.05)


def v_melt(ctx, lt, d, gt):
    rrect(ctx, CX - 330, CY - 150, 660, 460, 50); fill_stroke(ctx, "#9FD8FF", lw=10)
    p = clamp(lt / max(d * 0.8, 0.5))
    for k in range(6):
        x = CX - 220 + k * 88
        y = CY - 40 + 220 * p + 20 * math.sin(gt * 4 + k)
        ctx.save(); ctx.push_group()
        pill(ctx, x, y, 0.32, 0.4 * k)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(1 - 0.7 * p); ctx.restore()
    draw_sprite(ctx, text_sprite("溶けちゃう!", 110, color="#FF4F8B", stroke="#FFFFFF", stroke_w=7, path=FONTS["dela"]), CX, CY - 330, pin(lt, 0.15), 1, -0.06)


def v_tube(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY); ctx.rotate(-0.35); ctx.scale(s, s)
    rrect(ctx, -420, -120, 840, 240, 120); fill_stroke(ctx, "#2E2E4A", lw=10)
    for i in range(-6, 7):
        for j in (-1, 0, 1):
            x, y = i * 64 + (32 if j % 2 else 0), j * 62
            ctx.new_path()
            for k in range(6):
                a = math.pi / 6 + k * math.pi / 3
                ctx.line_to(x + 30 * math.cos(a), y + 30 * math.sin(a))
            ctx.close_path(); ctx.set_source_rgba(0.6, 0.65, 0.8, 0.9); ctx.set_line_width(4); ctx.stroke()
    for k in range(5):
        circle(ctx, -320 + k * 160, -150 + 20 * math.sin(gt * 3 + k), 34 * pin(lt, 0.2 + k * 0.06), PILL_B, lw=6)
    ctx.restore()
    draw_sprite(ctx, text_sprite("炭素のチューブ", 96, hi="#FFE14D", path=FONTS["dela"]), CX, CY - 380, pin(lt, 0.3), 1)


def v_250(ctx, lt, d, gt):
    n = int(250 * ease_out_cubic(clamp(lt / max(d * 0.75, 0.5))))
    battery(ctx, CX + 280, CY + 120, 0.6, level=(gt * 0.8) % 1.0)
    draw_sprite(ctx, text_sprite(f"{n}回", 230, color="#3CE07A", stroke="#FFFFFF", stroke_w=10, path=FONTS["dela"]), CX - 120, CY - 120, pin(lt), 1, 0.04 * math.sin(gt * 4))


def v_safe(ctx, lt, d, gt):
    battery(ctx, CX, CY + 40, 0.9 * pin(lt), level=0.8)
    circle(ctx, CX + 260, CY - 260, 110 * pin(lt, 0.2), "#3CE07A", lw=10)
    ctx.move_to(CX + 205, CY - 260); ctx.line_to(CX + 245, CY - 215); ctx.line_to(CX + 320, CY - 310)
    ctx.set_source_rgba(1, 1, 1, 1); ctx.set_line_width(22); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    draw_sprite(ctx, text_sprite("燃えにくい", 100, hi="#FFE14D", path=FONTS["dela"]), CX, CY - 420, pin(lt, 0.3), 1)


def v_ear(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 220, math.pi * 0.75, math.pi * 2.25); ctx.set_source_rgba(*hexc("#FFD3B5")); ctx.fill_preserve()
    ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(10); ctx.stroke()
    ctx.restore()
    circle(ctx, CX + 40, CY + 40, 70 * pin(lt, 0.2), "#FFFFFF", lw=8)
    draw_sprite(ctx, text_sprite("補聴器", 110, hi="#FFE14D", path=FONTS["dela"]), CX, CY - 380, pin(lt, 0.3), 1)


def v_third(ctx, lt, d, gt):
    labels = [("血", "#FF4F4F"), ("酵素", "#7FD3FF"), ("B12", PILL_B)]
    for i, (t, c) in enumerate(labels):
        x = CX - 300 + i * 300
        circle(ctx, x, CY, 120 * pin(lt, i * 0.15), c, lw=8)
        draw_sprite(ctx, text_sprite(t, 70, color="#1B1B3A", stroke="#FFFFFF", stroke_w=5, path=FONTS["dela"]), x, CY, pin(lt, 0.1 + i * 0.15), 1)
    draw_sprite(ctx, text_sprite("3作目!", 140, color="#FFE14D", path=FONTS["dela"]), CX, CY - 340, pin(lt, 0.5), 1, -0.06)


def v_solarwind(ctx, lt, d, gt):
    circle(ctx, CX - 250, CY - 220, 110 * pin(lt), "#FFE14D", lw=8)
    ctx.save(); ctx.translate(CX + 250, CY - 120)
    ctx.move_to(0, 0); ctx.line_to(0, 320); ctx.set_source_rgba(1, 1, 1, 1); ctx.set_line_width(18); ctx.stroke()
    ctx.rotate(gt * 3)
    for k in range(3):
        ctx.rotate(2 * math.pi / 3)
        rrect(ctx, -14, -170, 28, 170, 14); fill_stroke(ctx, "#FFFFFF", lw=5)
    ctx.restore()
    battery(ctx, CX, CY + 250, 0.5 * pin(lt, 0.2), level=(gt * 0.5) % 1.0)


def v_future_home(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY + 80); ctx.scale(s, s)
    ctx.move_to(-260, -40); ctx.line_to(0, -260); ctx.line_to(260, -40); ctx.close_path(); fill_stroke(ctx, "#FF8FB1", lw=10)
    rrect(ctx, -220, -40, 440, 300, 20); fill_stroke(ctx, "#FFF4D6", lw=10)
    ctx.restore()
    pill(ctx, CX, CY + 160, 0.6 * pin(lt, 0.25), 0.1 * math.sin(gt * 3))
    sparkles(ctx, CX, CY, lt, 0.3, "#FFE14D", 14, 420)


def v_ask(ctx, lt, d, gt):
    pill(ctx, CX - 200, CY - 120, 0.7 * pin(lt), 0.3)
    for i, (x, y, sz) in enumerate([(CX + 120, CY - 260, 170), (CX + 300, CY - 60, 220)]):
        draw_sprite(ctx, text_sprite("?", sz, color="#FFE14D", path=FONTS["dela"]), x, y, pin(lt, 0.1 + i * 0.15), 1, 0.3 * math.sin(gt * 4 + i))


OPT = ["鉄", "コバルト", "金"]
CUTS = [
    eyes(Cut("毎日のサプリに入ってる、あのビタミンで、", "サプリの{ビタミン}で…", v_hook, capsize=106), [], word="ゴゴゴ"),
    eyes(Cut("充電できる電池が、できちゃった!", "{充電できる電池}が\nできちゃった!", v_b12, capsize=104, sfx=[(0.1, "kira")], mood="wow", point=True), [(CX, CY - 60, 30)], hit=True, word="ドーン!"),
    teaser(),
    Cut("作ったのは、スペインのコルドバ大学!", "スペインの\n{コルドバ大学}!", v_spain, capsize=104),
    Cut("使うのは、ビタミンB12!", "使うのは\n{ビタミンB12}!", v_b12, capsize=108, point=True),
    Cut("亜鉛と、空気の酸素で、電気をつくる電池です。", "{亜鉛}と{空気}で\n電気をつくる!", v_zincair, capsize=100),
    quiz("ここでクイズ!B12の真ん中にある金属は、どれ?", "Q.B12の真ん中の\n{金属}は?", OPT, 1),
    reveal("正解は、B!コバルト!", "正解は{B}!\nコバルト!", OPT, 1),
    Cut("このコバルトが、酸素の反応を、手伝うんです!", "コバルトが\n{酸素の反応}を手伝う!", v_cobalt, capsize=96, point=True),
    eyes(Cut("でもB12は、水に溶けやすい!", "でもB12は\n{水に溶けやすい}!", v_melt, capsize=104), [], word="ガーン!"),
    Cut("そこで、炭素の細いチューブに、くっつけた!", "{炭素のチューブ}に\nくっつけた!", v_tube, capsize=100, point=True),
    Cut("結果、二百五十回も、充電できた!", "{250回}も\n充電できた!", v_250, capsize=112, sfx=[(0.15, "tada")], point=True),
    Cut("液は水なので、燃えにくいのも、うれしい!", "液は水だから\n{燃えにくい}!", v_safe, capsize=100),
    buildup(), openbox(),
    Cut("じつは、亜鉛空気電池は、補聴器で、もう使われてる!", "補聴器で\n{もう使われてる}!", v_ear, dream=True, capsize=96, word="キラーン", point=True),
    Cut("チームは、血の成分などに続いて、これが、3作目!", "血の成分などに続き\n{3作目}!", v_third, dream=True, capsize=96, word="ジャーン", point=True),
    Cut("いつか、太陽や風の電気を、ためられるかも!", "{太陽や風}の電気を\nためられるかも!", v_solarwind, dream=True, capsize=96, word="ワクワク", point=True),
    Cut("身近なものが、未来の電池になる日が、来るかも!", "身近なものが\n{未来の電池}に!?", v_future_home, dream=True, capsize=96, point=True),
    Cut("あなたなら、次は何で、電池を作る?", "次は{何で}\n電池を作る?", v_ask, capsize=104),
    Cut("コメントで、教えてね!", "{コメント}で\n教えてね!", v_comment, capsize=112, sfx=[(0.2, "kira")]),
]

if __name__ == "__main__":
    run("20261121_b12battery", CUTS, 31, "テック", "#00A6C8", 2)
