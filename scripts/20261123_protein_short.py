"""Short (vertical, ~55 s) for the 'protein from CO2' story. EXPERIMENT H01 (2nd run): first cut is a big number close-up ("7日").
Top-left badge (Piko face button + "↓くわしい版はここから!") is shown the whole time."""
import sys, os, math
from common4 import *
from hera_vis import *
import hera_vis
hera_vis.PHOTO_LAYOUT.update(cy=640, scale=0.62)
from protein_vis import *
import protein_vis
protein_vis.OPTS["short"] = True
from space3 import eyes

P_oncom = P("oncom", "Midori / CC BY-SA 3.0", "赤いオンチョム", box=(980, 735))
OPT = ["細菌", "カビ", "海そう"]
CUTS = [
    eyes(Cut("たった七日!空気から、食べられる、たんぱく質が、できちゃった!", "空気から{たんぱく質}!?", v_7days_big, capsize=100, mood="wow"), [], hit=True, word="ドーン!"),
    Cut("材料は、空気の中の、二酸化炭素。", "材料は\n{二酸化炭素}", v_air, capsize=100, point=True),
    Cut("そう、わたしたちが、はく息にも入っている、あのガスです。", "はく息にも\n{入っているガス}", v_air, capsize=96, word="フーッ"),
    Cut("アメリカの、ワシントン大学が、電気の力で、二酸化炭素を、ある生き物の、ごはんに変えました。", "電気でCO2を\n{生き物のごはん}に", v_ethanol, capsize=92),
    teaser(),
    quiz("クイズ!そのごはんを食べて、たんぱく質に変える、主役の生き物は?", "Q.主役の\n{生き物}は?", OPT, 1),
    reveal("正解は、B!オレンジ色の、カビ!", "正解は{B}!\n{オレンジ色のカビ}!", OPT, 1),
    Cut("このカビ、牛なら六百四十五日かかる、たんぱく質づくりを、たった七日で!", "牛は645日\nカビは{7日}!", v_days, capsize=96, point=True, word="ワオ!"),
    Cut("育ったカビを、かわかして、こなにすれば、たんぱく質の、パウダーの、できあがり!", "こなにして\n{パウダー}に!", v_powder, capsize=96, word="サラサラ"),
    buildup(), openbox(),
    Cut("しかも、なかまのカビは、インドネシアで、オンチョムとして、もう食べられているんです!", "{もう食べられている}!", P_oncom, dream=True, capsize=96, point=True, word="ナルホド"),
    Cut("あなたなら、空気から作ったたんぱく質で、何を作る?コメントで教えてね!", "何を作る?\n{コメントで教えてね}!", v_comment, capsize=96, mood="wow"),
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
    name = "20261123_protein_short"
    if len(sys.argv) > 2:
        BADGE["y"] = int(sys.argv[2])
    tl = build4(CUTS, seed=73)
    f0 = make_frame4(tl, "テック", "#FF8A2B")
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
