"""Short (宇宙) 2026-11-19: Voyager 1 reaches one light-day from Earth"""
import math
from common4 import *
from space2 import pin, CX, CY, STARPAL, v_light, v_comment
from space3 import probe, eyes, v_dream_intro
from space import planet, sun

EARTH = "#3FA9F5"


def trail(ctx, x, y, n=5):
    for k in range(n):
        ctx.new_path(); ctx.arc(x - 60 * (k + 1), y + 40 * (k + 1), 16 - 2.5 * k, 0, 2 * math.pi)
        ctx.set_source_rgba(1, 0.85, 0.3, 0.8 - 0.14 * k); ctx.fill()


def v_far(ctx, lt, d, gt):
    planet(ctx, 170, CY + 260, 110 * pin(lt), EARTH)
    p = ease_out_cubic(clamp(lt / max(d, 0.6)))
    x, y = 330 + 520 * p, CY + 150 - 380 * p
    trail(ctx, x, y)
    probe(ctx, x, y, 1.4 * pin(lt, 0.1), gt)


def v_oneday(ctx, lt, d, gt):
    burst(ctx, CX, CY, 400 * pin(lt), gt, "#FFE14D")
    draw_sprite(ctx, text_sprite("光で1日", 170, color="#FFE14D", path=FONTS["dela"]), CX, CY - 40, pin(lt, 0.05), 1, -0.06)
    sparkles(ctx, CX, CY, lt, 0.1, "#FFFFFF", 16, 480)


def v_launch(ctx, lt, d, gt):
    planet(ctx, CX, CY + 380, 260, EARTH)
    p = ease_in_out(clamp(lt / max(d, 0.6)))
    probe(ctx, CX, CY + 80 - 420 * p, 1.2 * pin(lt), gt)
    draw_sprite(ctx, text_sprite("1977年", 120, hi="#FFE14D", path=FONTS["dela"]), CX - 220, CY - 330, pin(lt, 0.15), 1, -0.08)


def v_49(ctx, lt, d, gt):
    n = int(49 * ease_out_cubic(clamp(lt / max(d * 0.7, 0.4))))
    draw_sprite(ctx, text_sprite(f"{n}年", 260, color="#FFE14D", path=FONTS["dela"]), CX, CY - 60, pin(lt), 1, 0.05 * math.sin(gt * 4))
    probe(ctx, CX + 300, CY + 250, 0.9, gt)


def v_planets(ctx, lt, d, gt):
    planet(ctx, CX - 220, CY - 120, 190 * pin(lt), "#E0A56B", t=gt)
    planet(ctx, CX + 250, CY + 120, 150 * pin(lt, 0.2), "#EAD28A", ring="#C9B06A", t=gt)
    draw_sprite(ctx, text_sprite("木星", 60, path=FONTS["mochiy"]), CX - 220, CY + 110, pin(lt, 0.1), 1)
    draw_sprite(ctx, text_sprite("土星", 60, path=FONTS["mochiy"]), CX + 250, CY + 320, pin(lt, 0.3), 1)


def v_exit(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.set_dash([20, 14])
    ctx.new_path(); ctx.arc(CX - 260, CY, 380 * s, -1.0, 1.0)
    ctx.set_source_rgba(*hexc("#9FD8FF")); ctx.set_line_width(12); ctx.stroke(); ctx.restore()
    sun(ctx, CX - 260, CY, 90 * s, gt)
    p = ease_out_cubic(clamp((lt - 0.2) / 0.8))
    probe(ctx, CX + 60 + 280 * p, CY - 40, 1.0, gt)
    draw_sprite(ctx, text_sprite("太陽系の外へ", 70, hi="#FFE14D", path=FONTS["rock"]), CX + 120, CY - 330, pin(lt, 0.3), 1, 0.06)


def v_dist(ctx, lt, d, gt):
    draw_sprite(ctx, text_sprite("259億km", 150, color="#FFE14D", path=FONTS["dela"]), CX, CY - 60, pin(lt), 1, -0.05)
    for k in range(6):
        star(ctx, 120 + k * 170, CY + 250 + 40 * math.sin(gt * 3 + k), 26, "#FFFFFF")


def v_neptune(ctx, lt, d, gt):
    sun(ctx, 120, CY, 80 * pin(lt), gt)
    planet(ctx, 300, CY, 40 * pin(lt, 0.1), "#4F7BFF")
    draw_sprite(ctx, text_sprite("海王星", 46, path=FONTS["mochiy"]), 300, CY + 85, pin(lt, 0.15), 1)
    p = ease_out_cubic(clamp((lt - 0.2) / 0.8))
    ctx.move_to(360, CY); ctx.line_to(360 + 560 * p, CY)
    ctx.set_source_rgba(*hexc("#FFE14D")); ctx.set_line_width(14); ctx.set_dash([2, 30]); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke(); ctx.set_dash([])
    probe(ctx, 960, CY - 10, 0.8 * pin(lt, 0.3), gt)
    draw_sprite(ctx, text_sprite("5.6倍", 130, color="#FF3D7F", stroke="#FFFFFF", stroke_w=6, path=FONTS["dela"]), CX + 120, CY - 280, pin(lt, 0.4), 1, -0.1)


def v_first(ctx, lt, d, gt):
    burst(ctx, CX, CY, 380 * pin(lt), gt, "#FF3D7F")
    probe(ctx, CX, CY + 40, 1.8 * pin(lt, 0.08), gt)
    draw_sprite(ctx, text_sprite("人類初", 150, color="#FFE14D", path=FONTS["dela"]), CX, CY - 300, pin(lt, 0.2), 1, 0.08)
    sparkles(ctx, CX, CY, lt, 0.15, "#FFE14D", 18, 520)


def v_round(ctx, lt, d, gt):
    planet(ctx, 170, CY, 100 * pin(lt), EARTH)
    probe(ctx, 930, CY, 0.9 * pin(lt, 0.1), gt)
    p = (lt % 1.6) / 1.6
    for sx, y, col in ((1, CY - 60, "#FFE14D"), (-1, CY + 60, "#9FD8FF")):
        x = 280 + 560 * (p if sx > 0 else 1 - p)
        ctx.new_path(); ctx.arc(x, y, 22, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(col)); ctx.fill()
    draw_sprite(ctx, text_sprite("往復48時間", 110, color="#FFE14D", path=FONTS["dela"]), CX, CY - 300, pin(lt, 0.2), 1, -0.05)


def v_speed(ctx, lt, d, gt):
    for k in range(7):
        y = CY - 240 + k * 80
        off = (gt * 900 + k * 170) % 1200
        ctx.move_to(W - off, y); ctx.line_to(W - off + 220, y)
        ctx.set_source_rgba(1, 1, 1, 0.5); ctx.set_line_width(10); ctx.stroke()
    probe(ctx, CX, CY, 1.3 * pin(lt), gt)
    draw_sprite(ctx, text_sprite("秒速17km", 120, color="#FFE14D", path=FONTS["dela"]), CX, CY - 330, pin(lt, 0.2), 1, 0.06)


def v_twin(ctx, lt, d, gt):
    probe(ctx, CX - 250, CY - 80, 1.0 * pin(lt), gt)
    probe(ctx, CX + 250, CY + 80, 1.0 * pin(lt, 0.15), gt + 1)
    draw_sprite(ctx, text_sprite("1号", 70, path=FONTS["mochiy"]), CX - 250, CY + 80, pin(lt, 0.1), 1)
    draw_sprite(ctx, text_sprite("2号は2035年", 70, hi="#FFE14D", path=FONTS["mochiy"]), CX + 250, CY + 250, pin(lt, 0.3), 1)


def v_record(ctx, lt, d, gt):
    s = pin(lt)
    ctx.save(); ctx.translate(CX, CY); ctx.rotate(gt * 1.5); ctx.scale(s, s)
    circle(ctx, 0, 0, 260, "#F2C14E", lw=12)
    for r in (200, 150, 100):
        ctx.new_path(); ctx.arc(0, 0, r, 0, 2 * math.pi); ctx.set_source_rgba(0.6, 0.42, 0.1, 0.8); ctx.set_line_width(5); ctx.stroke()
    circle(ctx, 0, 0, 40, "#FFF7E0", lw=6)
    ctx.restore()
    sparkles(ctx, CX, CY, lt, 0.2, "#FFFFFF", 14, 420)


def v_star445(ctx, lt, d, gt):
    star(ctx, CX + 200, CY - 180, 150 * pin(lt), "#FFB36B")
    p = ease_in_out(clamp(lt / max(d * 0.9, 0.6)))
    x, y = CX - 380 + 420 * p, CY + 300 - 330 * p
    trail(ctx, x, y)
    probe(ctx, x, y, 1.1, gt)
    draw_sprite(ctx, text_sprite("4万年後", 110, color="#FFE14D", path=FONTS["dela"]), CX - 160, CY - 330, pin(lt, 0.2), 1, -0.08)


def v_hello(ctx, lt, d, gt):
    planet(ctx, CX, CY + 250, 200 * pin(lt), EARTH)
    for k in range(3):
        r = (lt * 260 + k * 160) % 520
        ctx.new_path(); ctx.arc(CX, CY + 250, 200 + r, math.pi * 1.15, math.pi * 1.85)
        ctx.set_source_rgba(1, 0.88, 0.3, max(0, 1 - r / 520)); ctx.set_line_width(12); ctx.stroke()
    piko(ctx, CX, CY - 220, gt, 0.6, "wow")


def v_question(ctx, lt, d, gt):
    probe(ctx, CX, CY + 40, 1.6 * pin(lt), gt)
    for i, (x, y, sz) in enumerate([(CX - 300, CY - 260, 170), (CX + 300, CY - 200, 220)]):
        draw_sprite(ctx, text_sprite("?", sz, color="#FFE14D", path=FONTS["dela"]), x, y, pin(lt, 0.1 + i * 0.15), 1, 0.3 * math.sin(gt * 4 + i))


OPT = ["24分", "24時間", "24日"]
CUTS = [
    eyes(Cut("人類の探査機が、ついに、", "人類の探査機が\n{ついに}…", v_far, pal=STARPAL, capsize=104), []),
    eyes(Cut("光で一日かかる場所に、とうちゃく!", "{光で1日}の場所に\nとうちゃく!", v_oneday, capsize=110, sfx=[(0.1, "kira")], mood="wow", point=True), [(CX, CY - 40, 30)], hit=True, word="ドーン!"),
    teaser(),
    Cut("それが、千九百七十七年に打ち上げた、ボイジャー1号!", "1977年打ち上げ\n{ボイジャー1号}!", v_launch, capsize=104, point=True),
    eyes(Cut("四十九年も、旅を続けてる!", "{49年}も\n旅を続けてる!", v_49, capsize=110, point=True), [], word="ガーン!"),
    Cut("木星と土星を、間近で観察して、", "{木星}と{土星}を\n間近で観察", v_planets, capsize=96),
    Cut("二千十二年には、太陽系の外へ!", "2012年には\n{太陽系の外}へ!", v_exit, capsize=100, pal=STARPAL, point=True),
    Cut("十一月十八日、ついに、光で一日分の距離に!", "11月18日\n{光で1日分}の距離に!", v_light, capsize=92, sfx=[(0.1, "zip")]),
    Cut("その距離、およそ、二百五十九億キロ!", "およそ\n{259億km}!", v_dist, capsize=112, point=True),
    eyes(Cut("ここまで来たのは、人類初です!", "ここまで来たのは\n{人類初}!", v_first, capsize=100, sfx=[(0.15, "tada")], mood="wow", point=True), [(CX, CY + 40, 30)], hit=True, word="ジャーン!"),
    quiz("ここでクイズ!地球からの電波は、ボイジャーまで、片道どれくらい?", "Q.電波は片道\n{どれくらい}?", OPT, 1),
    reveal("正解は、B!片道二十四時間!", "正解は{B}!\n片道24時間", OPT, 1),
    Cut("返事が来るまで、まる二日!", "返事が来るまで\n{まる2日}!", v_round, capsize=104, point=True),
    Cut("いまも、秒速十七キロで、進み続けてる!", "いまも{秒速17km}で\n進み続けてる!", v_speed, capsize=96),
    buildup(), openbox(),
    Cut("ボイジャーには、地球の音を入れた、金色のレコードが、積んである!", "地球の音を入れた\n{金色のレコード}!", v_record, dream=True, capsize=92, word="キラーン", point=True),
    Cut("約四万年後には、別の星の近くを、通るかも!", "約{4万年後}には\n別の星の近くへ!?", v_star445, dream=True, capsize=92, word="ヒュー", point=True),
    Cut("宇宙のだれかが、聞いてくれたら、最高!", "宇宙のだれかが\n{聞いてくれたら}最高!", v_hello, dream=True, capsize=88, word="ワクワク", point=True),
    Cut("あなたなら、レコードに、どんな音を入れる?", "あなたなら\n{どんな音}を入れる?", v_question, capsize=96),
    Cut("コメントで、教えてね!", "{コメント}で\n教えてね!", v_comment, capsize=112, sfx=[(0.2, "kira")]),
]

if __name__ == "__main__":
    run("voyager", CUTS, 19, "宇宙", "#7B5CFF", 0)
