"""Short (vertical, ~55 s) for the 'wild life of homes' story (Allf et al., Ecology 2026). Standard format.
Facts cut out: ~2,100 species indoors / #1 is the lady beetle (quiz) / an alligator in a garage.
Top-left badge (Piko face button + "↓くわしい版はここから!") is shown the whole time."""
import sys, os, math
from common4 import *
from hera_vis import *
import hera_vis
hera_vis.PHOTO_LAYOUT.update(cy=640, scale=0.62)
from homebug_vis import *
import homebug_vis
homebug_vis.OPTS["short"] = True
from space3 import eyes


def fit(vis, a=195.0, b=0.66):
    """Shrink a 1080x1920-stage scene so its title clears the header and its bottom clears the caption."""
    def f(ctx, lt, d, gt):
        ctx.save(); ctx.translate(CX * (1 - b), a); ctx.scale(b, b); vis(ctx, lt, d, gt); ctx.restore()
    return f


v_hook_s, v_garage_s, v_gator_s, v_visitor_s, v_comment_s, v_phone_s, v_house_s = map(fit, (v_hook, v_garage, v_gator, v_visitor, v_comment, v_phone_snap, v_house_full))
v_2100_s = fit(bigtext("約2100種", "家の中の生き物", size=190), b=0.8)

P_lady = P("h_lady", "Naelin / iNaturalist / CC BY", "1位 ナミテントウ", box=(900, 675))
P_gator = P("h_gator", "Nancy Tognan / iNaturalist / CC BY", "アメリカアリゲーター", box=(620, 826))
OPT = ["ゴキブリ", "テントウムシ", "ハエ"]
CUTS = [
    eyes(Cut("あなたの家の中に、何種類の、生き物が、いると思う?", "あなたの家に\n{何種類}いる?", v_hook_s, capsize=100, mood="wow"), [], hit=True, word="ムムッ"),
    Cut("アメリカとカナダの、家の中を、三千人が、調べたら、なんと、およそ二千百種!", "家の中から\n{約2100種}!", v_2100_s, capsize=100, point=True, word="ドーン!"),
    Cut("スマホで撮った、生き物の写真を、みんなで、集めたんです。", "スマホの写真を\n{みんなで集めた}", v_phone_s, capsize=92),
    Cut("クモに、虫に、いろんな生き物が、家の中で、こっそり、くらしていたんです。", "家の中で\n{こっそりくらす}", v_house_s, capsize=96),
    teaser(),
    quiz("クイズ!いちばん多く、見つかった、一位の生き物は?", "Q.1位の生き物は\n{何}?", OPT, 1),
    reveal("正解は、B!テントウムシ!ゴキブリじゃ、なかったんです!", "正解は{B}!\n{テントウムシ}!", OPT, 1),
    Cut("ナミテントウ。じつは、もともと、日本などにいる、アジアの虫なんです!", "1位は\n{アジア生まれ}!", P_lady, capsize=96, point=True, word="エッ!"),
    buildup(), openbox(),
    Cut("そして、ある家の、ガレージには、なんと、ワニが!", "ガレージに\n{ワニ}!?", v_garage_s, dream=True, capsize=100, point=True, word="ギャー!"),
    Cut("たまたま、まよいこんだ、お客さんでした!", "まよいこんだ\n{お客さん}!", v_visitor_s, dream=True, capsize=96, word="ホッ"),
    Cut("家の中は、思っているより、ずっと、にぎやかな、生き物の世界なんですね!", "家の中は\n{にぎやか}!", v_house_s, dream=True, capsize=100, word="ワクワク"),
    Cut("あなたの家では、どんな生き物を、見たことある?コメントで教えてね!", "あなたの家では?\n{コメントで教えてね}!", v_comment_s, capsize=92, mood="wow"),
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
    name = "20261124_homebugs_short"
    if len(sys.argv) > 2:
        BADGE["y"] = int(sys.argv[2])
    tl = build4(CUTS, seed=73)
    f0 = make_frame4(tl, "生き物", "#3FAF5A")
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
