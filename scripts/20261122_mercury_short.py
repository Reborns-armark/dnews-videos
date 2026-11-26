"""Short (vertical, ~55 s) for the BepiColombo / Mercury story. H01 experiment: first cut = big number close-up.
Top-left badge (Piko face button + "↓くわしい版はここから!") is shown the whole time."""
import sys, os, math
from common4 import *
from hera_vis import *
from mercury_vis import *
from space3 import eyes
import hera_vis
hera_vis.PHOTO_LAYOUT.update(cy=640, scale=0.62)
import mercury_vis
mercury_vis.OPTS["short"] = True

OPT = ["3回", "6回", "9回"]
CUTS = [
    eyes(Cut("お隣の水星まで、なんと、八年もかかった!", "お隣の水星まで\n{8年}!", v_eight_years, capsize=104, mood="wow"), [], hit=True, word="ドーン!"),
    Cut("冥王星に行った探査機でも、約九年半。ほとんど同じくらい!", "冥王星へは\n約{9年半}!", v_pluto, capsize=100, word="ガーン!"),
    Cut("じつは水星は、冥王星に行くより、大変だと言われる惑星!", "{冥王星}に行くより\n大変!?", v_pluto, capsize=100, point=True, word="ムムッ"),
    teaser(),
    Cut("太陽に近づくと、坂道を転がるみたいに、どんどん速くなっちゃうから!", "坂道みたいに\n{どんどん速く}なる!", v_slope, capsize=96, point=True, word="ギュイーン"),
    Cut("止まるには、思いきりブレーキが必要!", "止まるには\n{ブレーキ}が必要!", v_brake, capsize=100, word="キキーッ"),
    Cut("そこで、惑星の重力を使って、少しずつブレーキ!", "惑星の重力で\n{少しずつブレーキ}", v_swingby, capsize=96, word="ヒュー"),
    quiz("クイズ!ブレーキのために、惑星のそばを、何回通った?", "Q.惑星のそばを\n{何回}通った?", OPT, 2),
    reveal("正解は、C!九回!", "正解は{C}!\n{9回}!", OPT, 2),
    Cut("地球で一回、金星で二回、水星で六回!", "地球1・金星2\n{水星6回}!", v_flybys, capsize=100),
    Cut("これが、探査機ベピコロンボが撮った、本物の水星!", "探査機が撮った\n{本物の水星}!", P_selfie, capsize=96, point=True, sfx=[(0.1, "kira")]),
    Cut("はしに写ってるのは、探査機の、うで!", "はしに写ってるのは\n{探査機のうで}!", P_selfie, capsize=96, word="パシャ"),
    buildup(), openbox(),
    Cut("そしていま、水星の重力に、つかまえてもらう大作戦!", "水星の重力に\n{つかまえてもらう}!", v_capture, dream=True, capsize=96, point=True, word="ヒュー"),
    Cut("八年間の、長い長い旅の、ゴールです!", "8年間の旅の\n{ゴール}!", v_route, dream=True, capsize=100, word="キラーン"),
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
    name = "20261122_mercury_short"
    if len(sys.argv) > 2:
        BADGE["y"] = int(sys.argv[2])
    tl = build4(CUTS, seed=43)
    f0 = make_frame4(tl, "宇宙", "#7B5CFF")
    def frame(ctx, gt):
        f0(ctx, gt); badge(ctx, gt)
        frame.e, frame.lt = f0.e, f0.lt
    print("total", round(tl["total"], 2), "cuts", len(tl["cuts"]), "points", tl["npoints"])
    if sys.argv[1:] and sys.argv[1] == "preview":
        ts = [c["t0"] + min(0.6, c["d"] / 2) for c in tl["cuts"]]
        render3(None, tl, frame, ts, f"preview4/{name}")
    else:
        os.makedirs("out4", exist_ok=True)
        render3(f"out4/{name}_video.mp4", tl, frame)
        build_audio4(f"out4/{name}.wav", tl, 0)
        mux2(f"out4/{name}_video.mp4", f"out4/{name}.wav", f"out4/{name}_final.mp4")
