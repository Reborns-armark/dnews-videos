"""Short (vertical, ~55 s) for the 'Jonathan, 194-year-old tortoise' story (Science Advances 2026).
EXPERIMENT H01 (3rd run): first cut is a big number close-up ("194才").
Facts cut out: 194 years old (born in Japan's Edo period) / he is in a photo from ~1882 / DNA from his cheek (quiz) -> key gene switches still 'young'.
Top-left badge (Piko face button + "↓くわしい版はここから!") is shown the whole time."""
import sys, os, math
from common4 import *
from hera_vis import *
import hera_vis
hera_vis.PHOTO_LAYOUT.update(cy=640, scale=0.62)
from jonathan_vis import *
import jonathan_vis
jonathan_vis.OPTS["short"] = True
from space3 import eyes


def fit(vis, a=195.0, b=0.66):
    """Shrink a 1080x1920-stage scene so its title clears the header and its bottom clears the caption."""
    def f(ctx, lt, d, gt):
        ctx.save(); ctx.translate(CX * (1 - b), a); ctx.scale(b, b); vis(ctx, lt, d, gt); ctx.restore()
    return f


v_194_s = fit(bigtext("194才", None, size=320), b=0.8)
v_edo_s, v_cheek_s, v_food_s, v_stable_s, v_party_s, v_comment_s, v_caution_s = map(fit, (v_edo, v_cheek, v_food_trick, v_stable, v_party, v_comment, v_caution))
v_272_s = fit(v_272, b=0.8)

WM = "Wikimedia Commons"
P_gep = P("j_gepford", f"Kevin Gepford / CC BY-SA 4.0 / {WM}", "ジョナサン", box=(900, 675))
P_old = P("j_old", f"作者不明(パブリックドメイン)/ {WM}", "1882年ごろの写真", box=(900, 674))
OPT = ["血をとる", "ほっぺの内側", "こうらをけずる"]
CUTS = [
    eyes(Cut("百九十四才!今も元気に生きている、世界一、長生きの、陸の動物!", "今も元気な{194才}!", v_194_s, capsize=100, mood="wow"), [], hit=True, word="ドーン!"),
    Cut("名前は、ジョナサン。大西洋の、セントヘレナ島に、住む、ゾウガメです。", "ゾウガメの\n{ジョナサン}", P_gep, capsize=96, point=True),
    Cut("生まれたのは、日本が、まだ、江戸時代のころ!", "生まれは\n{江戸時代}!", v_edo_s, capsize=100, word="エッ!"),
    Cut("これは、千八百八十二年ごろの写真。左が、ジョナサンです!", "{1882年ごろ}の写真!", P_old, capsize=96, point=True, word="ワオ!"),
    teaser(),
    quiz("クイズ!長生きのひみつを調べるため、DNAを、どうやってとった?", "Q.DNAを\n{どうやってとった}?", OPT, 1),
    reveal("正解は、B!ごはんで、口を、あーんと、開けてもらって、ほっぺの内側を、こすったんです!", "正解は{B}!\n{ほっぺの内側}!", OPT, 1),
    buildup(), openbox(),
    Cut("すると、体の、大事なスイッチが、二百年近く、わかいカメと、同じように、ととのったままでした!", "大事なスイッチが\n{わかいまま}!", v_272_s, dream=True, capsize=96, point=True, word="スゴイ!"),
    Cut("でも、調べたのは、五ひきだけ。本当の、ひみつは、これからの、研究です!", "本当のひみつは\n{これから}!", v_caution_s, dream=True, capsize=96, word="ワクワク"),
    Cut("二百才まで、あと六年!お祝い、何がいい?コメントで教えてね!", "200才のお祝い\n{コメントで教えてね}!", v_party_s, capsize=92, mood="wow"),
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
    name = "20261124_jonathan_short"
    if len(sys.argv) > 2:
        BADGE["y"] = int(sys.argv[2])
    tl = build4(CUTS, seed=83)
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
