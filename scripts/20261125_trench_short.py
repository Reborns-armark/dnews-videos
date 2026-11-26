"""Short (vertical, ~55 s) for the deepest explosive volcanic deposits, >6,000 m down the Mariana Trench (Stern et al., Frontiers in Earth Science 2026,
doi:10.3389/feart.2026.1929806; UT Dallas release; Discover 2026-11-23). STANDARD (set 5, 2026-11-25 19:30; today's experiment A=set 2, B=set 1).
Cut 1 (standard type): the most surprising point first, no greeting: a volcano exploded on the sea floor 6,000 m down.
Facts cut out: deepest record, found by robot in the Mariana Trench (real photo at 6,148 m) / quiz: deep-sea blast is gentler /
why: water can't puff up into steam, it turns supercritical. Top-left badge shown the whole time."""
import sys, os, math
from common4 import *
from hera_vis import *
import hera_vis
hera_vis.PHOTO_LAYOUT.update(cy=640, scale=0.62)
from trench_vis import *
import trench_vis
trench_vis.OPTS["short"] = True
from space3 import eyes


def fit(vis, a=195.0, b=0.66):
    """Shrink a 1080x1920-stage scene so its title clears the header and its bottom clears the caption."""
    def f(ctx, lt, d, gt):
        ctx.save(); ctx.translate(CX * (1 - b), a); ctx.scale(b, b); vis(ctx, lt, d, gt); ctx.restore()
    return f


v_hook_s, v_trench_s, v_super_s, v_3pct_s, v_dive_s, v_comment_s, v_pyro_s = map(
    fit, (v_hook, v_trench, v_super, v_3pct, v_dive_deeper, v_comment, v_pyro_sea))

CR = "Stern et al. 2026(CC BY 4.0)"
P_flow = P("flow6148", CR, None, box=(1000, 640))
P_cool = P("cool6334", CR, None, box=(900, 700))
OPT = ["陸よりはげしい", "陸よりおだやか", "まったく同じ"]
CUTS = [
    eyes(Cut("深さ、六千メートルの、海の底で、火山が、爆発していた!?", "深さ6000mの海の底で\n{火山が爆発}!?", v_hook_s, capsize=80, mood="wow"), [], hit=True, word="エエッ!"),
    Cut("場所は、世界一深い、マリアナ海溝。海底ロボットが、見つけました。", "世界一深い\n{マリアナ海溝}", v_trench_s, capsize=96, point=True),
    Cut("これが、深さ、六千百四十八メートルの、本物の写真。熱い、火山のかけらが、流れた、あとなんです!", "深さ{6148m}の\n本物の写真!", P_flow, capsize=92, word="スゴイ!"),
    Cut("海で、いちばん深い、爆発の、記録です!", "海で{いちばん深い}\n爆発の記録!", P_cool, capsize=92, point=True),
    teaser(),
    quiz("クイズ!深海の、火山の爆発は、陸とくらべて、どうなる?", "Q.深海の爆発は\n{陸とくらべて}?", OPT, 1),
    reveal("正解は、B!おだやかに、なるんです!", "正解は{B}!\n{陸よりおだやか}!", OPT, 1),
    Cut("水の重さで、ぎゅっと、おされて、水が、水蒸気に、ふくらめない。液体でも、気体でもない、超臨界に、なるんです!", "液体でも気体でもない\n{超臨界}!", v_super_s, capsize=86, point=True, word="ナルホド"),
    Cut("だから、ドカンと、ならずに、ゆっくり、流れて、止まったんですね。", "ゆっくり流れて\n{止まった}", v_pyro_s, capsize=92),
    buildup(), openbox(),
    Cut("もっと深い、海の底には、まだ、だれも見ていない、火山が、あるかも!", "もっと深くに\n{まだ見ぬ火山}が!?", v_dive_s, dream=True, capsize=88, point=True, word="ワクワク"),
    Cut("あなたは、深海で、何を見つけたい?コメントで教えてね!", "深海で何を見つけたい?\n{コメントで教えてね}!", v_comment_s, capsize=86, mood="wow"),
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
    name = "20261125_trench_short"
    if len(sys.argv) > 2:
        BADGE["y"] = int(sys.argv[2])
    tl = build4(CUTS, seed=131)
    f0 = make_frame4(tl, "地球", "#1FA37A")
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
