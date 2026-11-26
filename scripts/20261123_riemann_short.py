"""Short (vertical, ~55 s) for the Riemann hypothesis / Claude story. Standard format (no experiment).
Top-left badge (Piko face button + "↓くわしい版はここから!") is shown the whole time."""
import sys, os, math
from common4 import *
from hera_vis import *
import hera_vis
hera_vis.PHOTO_LAYOUT.update(cy=640, scale=0.62)
from riemann_vis import *
import riemann_vis
riemann_vis.OPTS["short"] = True
from space3 import eyes

def fit(vis, a=195.0, b=0.66):
    """Shrink a 1080x1920-stage scene so its title clears the header and its bottom clears the caption."""
    def f(ctx, lt, d, gt):
        ctx.save(); ctx.translate(CX * (1 - b), a); ctx.scale(b, b); vis(ctx, lt, d, gt); ctx.restore()
    return f


v_line, v_who, v_ai_human, v_lean, v_human_read, v_comment = map(fit, (v_line, v_who, v_ai_human, v_lean, v_human_read, v_comment))

v_167_big = bigtext("167年", None, size=300)
P_riemann = P("riemann", "パブリックドメイン(Wikimedia Commons)", "リーマン", box=(620, 840))
OPT = ["1万円", "100万ドル", "1億ドル"]
CUTS = [
    eyes(Cut("百六十七年、だれにも、とけなかった、数学の、超難問が、とけたかもしれない!", "167年の超難問が\n{とけた}!?", v_167_big, capsize=100, mood="wow"), [], hit=True, word="ドーン!"),
    Cut("その名も、リーマン予想。素数の、ならび方の、ひみつを、にぎる、問題です。", "その名も\n{リーマン予想}", P_riemann, capsize=96, point=True),
    Cut("コンピューターで、何兆個も、調べて、ぜんぶ、正しかった。でも、証明は、だれにも、できなかったんです。", "何兆個調べても\n{証明はできない}", v_line, capsize=92),
    teaser(),
    quiz("クイズ!この問題をとくと、もらえるかもしれない、賞金は?", "Q.賞金は\n{いくら}?", OPT, 1),
    reveal("正解は、B!百万ドル!日本円で、一億円以上!", "正解は{B}!\n{100万ドル}!", OPT, 1),
    Cut("証明を、見つけたと、発表したのは、数学者の、アルポゲさんと、AIの、クロード!", "人間と{AI}の\nチーム!", v_who, capsize=96, point=True, word="ワオ!"),
    Cut("アルポゲさんは、子どものころから、この問題を、ずっと、夢見ていたそうです。", "子どものころからの\n{夢}だった!", v_ai_human, capsize=92),
    Cut("証明を、チェックする、ソフトの、きびしい、確認にも、合格しました!", "チェックソフトに\n{合格}!", v_lean, capsize=96, point=True, word="ピカッ"),
    buildup(), openbox(),
    Cut("でも、人間の、数学者が、中身を、理解するのは、これから。何年も、かかるかもしれません!", "人間が理解するのは\n{これから}!", v_human_read, dream=True, capsize=92, point=True),
    Cut("あなたは、AIと、人間の、数学チーム、どう思う?コメントで教えてね!", "どう思う?\n{コメントで教えてね}!", v_comment, capsize=96, mood="wow"),
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
    name = "20261123_riemann_short"
    if len(sys.argv) > 2:
        BADGE["y"] = int(sys.argv[2])
    tl = build4(CUTS, seed=93)
    f0 = make_frame4(tl, "数学", "#4FA3FF")
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
