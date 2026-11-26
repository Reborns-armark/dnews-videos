"""Short (vertical, ~55 s) for the bumblebee-intelligence story (Science Perspective, Chittka & Heinze, 2026-11-19). STANDARD format (no experiment).
Facts cut out: a bee rolled a ball under an out-of-reach flower and used it as a step (quiz) / brain like a sesame seed, < 1 million neurons /
bees roll balls even with no reward (play).
Top-left badge (Piko face button + "↓くわしい版はここから!") is shown the whole time."""
import sys, os, math
from common4 import *
from hera_vis import *
import hera_vis
hera_vis.PHOTO_LAYOUT.update(cy=640, scale=0.62)
from bee_vis import *
import bee_vis
bee_vis.OPTS["short"] = True
from space3 import eyes


def fit(vis, a=195.0, b=0.66):
    """Shrink a 1080x1920-stage scene so its title clears the header and its bottom clears the caption."""
    def f(ctx, lt, d, gt):
        ctx.save(); ctx.translate(CX * (1 - b), a); ctx.scale(b, b); vis(ctx, lt, d, gt); ctx.restore()
    return f


v_hook_s, v_high_s, v_push_s, v_climb_s, v_play_s, v_sesame_s, v_brain_s, v_comment_s, v_unseen_s, v_chimp_s = map(
    fit, (v_hook, v_high_flower, v_push, v_climb, v_play, v_sesame_scene, v_brain_cmp, v_comment, v_unseen, v_chimp))

P_terr = P("b_terr", "William Harland / iNaturalist / CC BY", "マルハナバチ", box=(940, 669))
OPT = ["仲間にのった", "ボールをふみ台に", "あきらめた"]
CUTS = [
    eyes(Cut("ハチが、ボールを、ふみ台にした!?", "ハチが\n{ボールをふみ台}に!?", v_hook_s, capsize=100, mood="wow"), [], hit=True),
    Cut("主役は、モフモフの、マルハナバチ。サイエンス誌の、新しい論文で、そのかしこさが、まとめられました。", "モフモフの\n{マルハナバチ}", P_terr, capsize=96, point=True),
    Cut("天井の花に、あまいミツ。でも、ひくい箱の中で、飛び上がれず、とどきません。", "天井のミツに\n{とどかない}…", v_high_s, capsize=96),
    teaser(),
    quiz("クイズ!ハチは、どうやって、ミツをのんだ?", "Q.どうやって\n{ミツをのんだ}?", OPT, 1),
    reveal("正解は、B!ボールを、花の下まで、ころがして、ふみ台にしたんです!", "正解は{B}!\n{ボールをふみ台}に!", OPT, 1),
    Cut("よじのぼって、ゴクッ!", "よじのぼって\n{ゴクッ}!", v_climb_s, capsize=100, point=True, word="ゴクッ!"),
    Cut("花が、見えない場所でも、ちゃんと、そっちへ、ボールを、運べたそうです。", "見えない場所へも\n{運べた}!", v_unseen_s, capsize=96),
    Cut("しかも、脳は、ゴマつぶくらい。神経細胞は、百万個より、少ないんです!", "脳は{ゴマつぶ}\n神経細胞{100万未満}", v_sesame_s, capsize=92, point=True, word="ナント"),
    Cut("チンパンジーが、箱をふみ台に、バナナをとった、有名な実験に、にていますね!", "まるで\n{チンパンジー}!", v_chimp_s, capsize=96, word="スゴイ!"),
    buildup(), openbox(),
    Cut("さらに、ごほうびが、なくても、ボールを、ころがして、遊ぶらしいんです!", "ごほうびなしで\n{ボール遊び}!?", v_play_s, dream=True, capsize=96, point=True, word="コロコロ"),
    Cut("あなたなら、ハチに、どんなパズルを、出してみたい?コメントで教えてね!", "どんなパズルを出す?\n{コメントで教えてね}!", v_comment_s, capsize=90, mood="wow"),
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
    name = "20261124_bumblebee_short"
    if len(sys.argv) > 2:
        BADGE["y"] = int(sys.argv[2])
    tl = build4(CUTS, seed=93)
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
