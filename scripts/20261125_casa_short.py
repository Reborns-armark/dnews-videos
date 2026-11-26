"""Short (vertical, ~55 s) for Webb / Cassiopeia A dust (ESA/Webb weic2624, 2026-11-23). STANDARD (set 3, 2026-11-25 12:15).
Cut 1 (standard type): the most surprising point first, no greeting: what happened hours before the explosion is left in the dust.
Facts cut out: Cas A = star explosion whose light reached us ~340 years ago / one dust spot is mostly silica = glass material (quiz) /
layers inside the star mixed, perhaps only hours before it exploded.
Top-left badge (Piko face button + "↓くわしい版はここから!") is shown the whole time."""
import sys, os, math
from common4 import *
from hera_vis import *
import hera_vis
hera_vis.PHOTO_LAYOUT.update(cy=640, scale=0.62)
from casa_vis import *
import casa_vis
casa_vis.OPTS["short"] = True
from space3 import eyes


def fit(vis, a=195.0, b=0.66):
    """Shrink a 1080x1920-stage scene so its title clears the header and its bottom clears the caption."""
    def f(ctx, lt, d, gt):
        ctx.save(); ctx.translate(CX * (1 - b), a); ctx.scale(b, b); vis(ctx, lt, d, gt); ctx.restore()
    return f


v_hook_s, v_merge_s, v_clock_s, v_glass_s, v_stardust_s, v_comment_s, v_340_s, v_three_s, v_light_s, v_tama_s = map(
    fit, (v_hook, v_merge, v_clock, v_glass, v_stardust, v_comment, v_340, v_three, v_light, v_tamanegi))

W26 = "ESA/Webb, NASA & CSA"
P_new = P("c26", W26, None, box=(960, 876))
P_gm = P("c26", W26, None, box=(940, 900), crop=(470, 480, 450, 430))
OPT = ["ガラス", "プラスチック", "鉄のくぎ"]
CUTS = [
    eyes(Cut("星が爆発する、数時間前のようすが、ちりに、残っていた!?", "爆発の数時間前が\n{ちりに残っていた}!?", v_hook_s, capsize=84, mood="wow"), [], hit=True, word="ドカーン!"),
    Cut("ウェッブ宇宙望遠鏡が、撮った、カシオペヤ座A。十一月二十三日に、発表されました。", "ウェッブが撮った\n{カシオペヤ座A}", P_new, capsize=96, point=True),
    Cut("およそ、三百四十年前に、光がとどいた、星の、爆発のあとです。", "約{340年前}の\n星の爆発あと", v_340_s, capsize=96),
    Cut("場所は、一万一千光年先。光の速さでも、一万一千年かかる、遠くです。", "{1万1000光年}先", v_light_s, capsize=96),
    teaser(),
    quiz("クイズ!ここの、ちりの多くは、シリカ。シリカは、何の材料?", "Q.シリカは\n{何の材料}?", OPT, 0),
    reveal("正解は、A!ガラスです!宇宙に、ガラスの材料が、うかんでいるんです!", "正解は{A}!\n{ガラス}の材料!", OPT, 0),
    Cut("さらに、ちりの中身から、星の中の層が、爆発の、数時間前に、まざっていた、しるしが、見つかったんです!", "爆発の数時間前に\n{層がまざった}!?", v_merge_s, capsize=84, point=True, word="エエッ!"),
    Cut("星の中は、たまねぎのような、層。それが、ぐるぐると、まざってしまったんです。", "たまねぎみたいな層が\n{ぐるぐる}", v_tama_s, capsize=88),
    buildup(), openbox(),
    Cut("星の、さいごの、数時間を、ちりが、日記のように、記録していたんですね!", "ちりは\n{星の日記}!", P_gm, dream=True, capsize=92, point=True, word="ワクワク"),
    Cut("あなたは、星の、どんなことを、知りたい?コメントで教えてね!", "星の何を知りたい?\n{コメントで教えてね}!", v_comment_s, capsize=90, mood="wow"),
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
    name = "20261125_casa_short"
    if len(sys.argv) > 2:
        BADGE["y"] = int(sys.argv[2])
    tl = build4(CUTS, seed=99)
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
