"""Short (vertical, ~55 s) for Enceladus ice grains (Postberg, Sekine et al., Science Advances 2026, doi:10.1126/sciadv.aee7256;
ELSI/Institute of Science Tokyo release; sorae 2026-11-24). STANDARD (set 4, 2026-11-25 16:00; today's experiment A=set 2, B=set 1).
Cut 1 (standard type): the most surprising point first, no greeting: the ocean spray from Saturn's moon has a different salt in each grain.
Facts cut out: Enceladus sprays its under-ice ocean into space (Cassini photo) / each grain carries a different salt /
why: slow freezing separates the salts (quiz) like a frozen juice block. Top-left badge shown the whole time."""
import sys, os, math
from common4 import *
from hera_vis import *
import hera_vis
hera_vis.PHOTO_LAYOUT.update(cy=640, scale=0.62)
from enc_vis import *
import enc_vis
enc_vis.OPTS["short"] = True
from space3 import eyes


def fit(vis, a=195.0, b=0.66):
    """Shrink a 1080x1920-stage scene so its title clears the header and its bottom clears the caption."""
    def f(ctx, lt, d, gt):
        ctx.save(); ctx.translate(CX * (1 - b), a); ctx.scale(b, b); vis(ctx, lt, d, gt); ctx.restore()
    return f


v_hook_s, v_salts_s, v_slowfast_s, v_juice_s, v_crash_s, v_future_s, v_comment_s, v_jets_s = map(
    fit, (v_hook, v_salts, v_slowfast, v_juice, v_crash, v_future_probe, v_comment, v_jets))

SSI = "NASA/JPL-Caltech/Space Science Institute"
P_color = P("enc_color", SSI, None, box=(640, 900))
P_found = P("fountains", SSI, None, box=(960, 820))
OPT = ["ゆっくりこおった", "いそいでこおった", "土星の風でまざった"]
CUTS = [
    eyes(Cut("宇宙にふき出す、海のしぶき。その、氷のつぶは、ひとつぶずつ、塩の種類が、ちがっていた!?", "宇宙にふき出す海のしぶき\n{1つぶずつ塩がちがう}!?", v_hook_s, capsize=80, mood="wow"), [], hit=True, word="エエッ!"),
    Cut("これは、土星の月、エンケラドス。氷の下に、海が、あります。", "土星の月\n{エンケラドス}", P_color, capsize=96, point=True),
    Cut("南極の、われめから、その海の水が、宇宙へ、ふき出しているんです!", "海の水が\n{宇宙へふき出す}!", P_found, capsize=92, word="ブシューッ!"),
    Cut("探査機カッシーニが、つぶを、しらべると、食塩、炭酸、リンなど、つぶごとに、塩が、バラバラ!", "つぶごとに\n{塩がバラバラ}!", v_salts_s, capsize=92, point=True),
    teaser(),
    quiz("クイズ!同じ海の水なのに、塩が、分かれたのは、なぜ?", "Q.塩が分かれたのは\n{なぜ}?", OPT, 0),
    reveal("正解は、A!ゆっくり、こおったから!日本の、実験で、わかりました!", "正解は{A}!\n{ゆっくりこおった}!", OPT, 0),
    Cut("ジュースを、ゆっくり、こおらせると、まん中だけ、味が、こくなる。それと、同じなんです!", "ジュースの氷と\n{同じしくみ}!", v_juice_s, capsize=88, point=True, word="ナルホド"),
    buildup(), openbox(),
    Cut("つぶを、ひとつずつ、しらべれば、海の、生き物の、しるしも、見つけやすくなるかも!", "海の{生き物のしるし}も\n見つけやすく!?", v_future_s, dream=True, capsize=84, point=True, word="ワクワク"),
    Cut("あなたは、この海に、生き物が、いると思う?コメントで教えてね!", "生き物はいると思う?\n{コメントで教えてね}!", v_comment_s, capsize=86, mood="wow"),
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
    name = "20261125_enceladus_short"
    if len(sys.argv) > 2:
        BADGE["y"] = int(sys.argv[2])
    tl = build4(CUTS, seed=97)
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
