"""Short (vertical, ~55 s) for the Westminster Abbey Roman coffin story. Standard type (no experiment).
Top-left badge (Piko face button + "↓くわしい版はここから!") is shown the whole time."""
import sys, os, math
from common4 import *
from hera_vis import *
import hera_vis
hera_vis.PHOTO_LAYOUT.update(cy=640, scale=0.62)
from coffin_vis import *
import coffin_vis
coffin_vis.OPTS["short"] = True
from space3 import eyes

P_ext = P("abbey_ext", "Suicasmo / CC BY-SA 4.0", "ウェストミンスター寺院", box=(660, 900))
OPT = ["ローマ時代", "約1000年前", "1800年代"]
CUTS = [
    eyes(Cut("ローマ時代の石の棺に、ちがう人が、入っていた!", "ローマの石の棺に\n{ちがう人}!?", v_hook, capsize=100, mood="wow"), [], hit=True, word="ドーン!"),
    Cut("場所は、イギリスの、ウェストミンスター寺院。王さまの、戴冠式をする教会です。", "場所は\n{ウェストミンスター寺院}", P_ext, capsize=92, point=True),
    Cut("棺は、およそ千六百五十年前の、ローマ時代のもの。", "棺は\n{約1650年前}のもの", v_coffin, capsize=100, point=True),
    Cut("でも、中の骨がだれなのか、百五十年以上、なぞだったんです。", "骨はだれ?\n{150年以上のなぞ}", v_missing, capsize=96, word="ムムッ"),
    teaser(),
    Cut("そこで、骨を、最新の科学、炭素の時計で、調べてみると。", "中の骨を\n{炭素の時計}で調べると", v_c14, capsize=96, word="チクタク"),
    quiz("クイズ!骨の人が、生きていたのは、いつ?", "Q.骨の人が\n{生きていた}のは?", OPT, 1),
    reveal("正解は、B!およそ、千年前!", "正解は{B}!\n{約1000年前}!", OPT, 1),
    Cut("日本でいうと、源氏物語のころ。棺より、六百年以上も、あとの人だったんです!", "棺より\n{600年以上あと}の人!", v_gap, capsize=96, point=True, word="ワオ!"),
    Cut("つまり、古い棺を、リサイクルして、使っていた!", "古い棺を\n{リサイクル}!", v_recycle, capsize=100, word="ナルホド"),
    buildup(), openbox(),
    Cut("中の人は、この修道院の、修道院長かも!候補は、二人にまで、しぼられています!", "正体は\n{修道院長}かも!", v_two, dream=True, capsize=100, point=True, word="ドドン!"),
    Cut("あなたは、どっちだと思う?コメントで教えてね!", "どっちだと思う?\n{コメントで教えてね}!", v_comment, capsize=96, mood="wow"),
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
    name = "20261123_coffin_short"
    if len(sys.argv) > 2:
        BADGE["y"] = int(sys.argv[2])
    tl = build4(CUTS, seed=63)
    f0 = make_frame4(tl, "歴史", "#C9853A")
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
