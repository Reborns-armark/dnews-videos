"""Short (vertical, ~55 s) for the moon-potato story. Standard type (no experiment).
Top-left badge (Piko face button + "↓くわしい版はここから!") is shown the whole time."""
import sys, os, math
from common4 import *
from hera_vis import *
import hera_vis
hera_vis.PHOTO_LAYOUT.update(cy=640, scale=0.62)
from potato_vis import *
import potato_vis
potato_vis.OPTS["short"] = True
from space3 import eyes

OPT = ["砂糖", "ミミズのふん", "コーラ"]
CUTS = [
    eyes(Cut("月の砂で、ジャガイモが、育った!", "月の砂で\n{ジャガイモ}が育った!", v_hook, capsize=104, mood="wow"), [], hit=True, word="ドーン!"),
    Cut("アメリカの大学が、月の砂そっくりの土で、育ててみたんです。", "月の砂{そっくりの土}で\n育ててみた!", v_moon_potato, capsize=96, point=True),
    Cut("いつか、月に住む人の、食べ物を作るためです!", "月に住む人の\n{食べ物づくり}!", v_base, capsize=100),
    Cut("これが本物の月の砂。栄養がなくて、金属が多い、きびしい砂!", "本物の月の砂は\n{栄養ゼロ}!", P_boot, capsize=100, word="ガーン!"),
    teaser(),
    Cut("そのままだと、根っこも、イモも、ほとんどできない。", "そのままだと\n{ほとんど育たない}", v_zero, capsize=96, word="ショボン"),
    quiz("クイズ!何をまぜたら、地球の畑と同じくらい、育った?", "Q.何をまぜたら\n{地球なみ}に育った?", OPT, 1),
    reveal("正解は、B!ミミズのふん!", "正解は{B}!\n{ミミズのふん}!", OPT, 1),
    Cut("ミミズのふんの堆肥を、三割まぜたら、地球の畑と、同じくらい、育ったんです!", "3割まぜたら\n{地球の畑なみ}!", v_compare, capsize=96, point=True, word="ジャーン!"),
    Cut("芽が出て、花がさいて、新しいイモまで、ちゃんとできた!", "芽→花→\n{新しいイモ}まで!", v_life_cycle, capsize=100, word="キラーン"),
    buildup(), openbox(),
    Cut("でも、その味は、まだ、だれも知らない!研究チームも、まだ食べていないんです!", "味は\n{まだだれも知らない}!", v_not_tasted, dream=True, capsize=96, point=True, word="ワオ!"),
    Cut("いつか、月の基地で、じゃがバターが、食べられるかも!", "月の基地で\n{じゃがバター}!?", v_base, dream=True, capsize=100, word="キラーン"),
    Cut("あなたなら、月のジャガイモで、何を作る?コメントで教えてね!", "何を作る?\n{コメントで教えてね}!", v_menu, capsize=96, mood="wow"),
    Cut("続きは、下のリンクの特別編で!", "続きは\n{下のリンクの特別編}で!", v_longvideo, capsize=88, sfx=[(0.2, "kira")]),
]

BADGE = {"x": 24, "y": 6}


def badge(ctx, gt):
    x, y = BADGE["x"], BADGE["y"]
    rrect(ctx, x, y, 470, 92, 46); ctx.set_source_rgba(1, 1, 1, 0.95); ctx.fill_preserve()
    ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(5); ctx.stroke()
    circle(ctx, x + 46, y + 46, 38, "#FF3D7F", lw=4)
    piko(ctx, x + 46, y + 52, gt, 0.22, "smile")
    draw_sprite(ctx, text_sprite("↓くわしい版はここから!", 36, color="#1B1B3A", hi="#FF3D7F", stroke="#FFFFFF", stroke_w=3,
                                 shadow=False, path=FONTS["mochiy"]), x + 275, y + 46, 1, 1)


if __name__ == "__main__":
    name = "20261122_moonpotato_short"
    if len(sys.argv) > 2:
        BADGE["y"] = int(sys.argv[2])
    tl = build4(CUTS, seed=53)
    f0 = make_frame4(tl, "宇宙", "#7B5CFF")
    def frame(ctx, gt):
        f0(ctx, gt); badge(ctx, gt)
        frame.e, frame.lt = f0.e, f0.lt
    print("total", round(tl["total"], 2), "cuts", len(tl["cuts"]), "points", tl["npoints"])
    if sys.argv[1:] and sys.argv[1] == "preview":
        ts = [c["t0"] + min(0.6, c["d"] / 2) for c in tl["cuts"]]
        render3(None, tl, frame, ts, f"preview4/{name}")
    elif sys.argv[1:] and sys.argv[1] == "time":
        pass
    else:
        os.makedirs("out4", exist_ok=True)
        render3(f"out4/{name}_video.mp4", tl, frame)
        build_audio4(f"out4/{name}.wav", tl, 0)
        mux2(f"out4/{name}_video.mp4", f"out4/{name}.wav", f"out4/{name}_final.mp4")
