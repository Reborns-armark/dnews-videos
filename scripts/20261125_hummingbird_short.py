"""Short (vertical, ~55 s) for the record hummingbird migration (Rhodes et al., Ecology and Evolution 2026; Science news 2026-11-23).
EXPERIMENT A (set 2, 2026-11-25 10:00). Changed element (only one): WHAT is pulled to the first second. Standard would open with the
headline result (record distance). Here cut 1 opens with the everyday-object angle: passers-by's smartphones were tracking the bird.
Wording style ("〜!?" exclamation, no greeting) and the first picture (drawn illustration) stay standard.
Facts cut out: passing phones picked up the tag / 0.06 g battery-free solar tag (= 2-3 grains of rice) / 3.7 g bird flew ~6,500 km
in 38 days, Alabama -> Alaska, longest hummingbird track (quiz).
Top-left badge (Piko face button + "↓くわしい版はここから!") is shown the whole time."""
import sys, os, math
from common4 import *
from hera_vis import *
import hera_vis
hera_vis.PHOTO_LAYOUT.update(cy=640, scale=0.62)
from humming_vis import *
import humming_vis
humming_vis.OPTS["short"] = True
from space3 import eyes


def fit(vis, a=195.0, b=0.66):
    """Shrink a 1080x1920-stage scene so its title clears the header and its bottom clears the caption."""
    def f(ctx, lt, d, gt):
        ctx.save(); ctx.translate(CX * (1 - b), a); ctx.scale(b, b); vis(ctx, lt, d, gt); ctx.restore()
    return f


v_hook_s, v_catch_s, v_upload_s, v_rice_s, v_route_s, v_full_s, v_coins_s, v_comment_s, v_yourphone_s, v_solar_s = map(
    fit, (v_hook, v_catch, v_upload, v_rice, v_route, v_route_full, v_coins, v_comment, v_yourphone, v_solar))

v_rest_s = fit(v_rest)
CR = "Rhodes et al. 2026 / CC BY 4.0"
P_tag = P("p_tag", CR, "本物の発信機!", box=(500, 875), crop=(60, 100, 470, 820))
P_map = P("p_map", CR, "本物の記録", box=(800, 877), crop=(0, 0, 560, 614))
OPT = ["メキシコ", "アラスカ", "カナダの東"]
CUTS = [
    eyes(Cut("道ゆく人のスマホが、小さな鳥を、追いかけていた!?", "みんなのスマホが\n{鳥を追いかけた}!?", v_hook_s, capsize=96, mood="wow"), [], hit=True),
    Cut("鳥は、ハチドリ。せなかに、お米、二、三つぶ分の、発信機。", "せなかに\n{お米2〜3つぶ}の発信機", P_tag, capsize=92, point=True),
    Cut("電池なしの、太陽電池で、三秒ごとに、ピッ!", "電池なし\n{3秒ごとにピッ}!", v_solar_s, capsize=96, word="ピッ!"),
    Cut("近くを通った、スマホなどが、キャッチして、場所を、記録するんです!", "近くのスマホが\n{キャッチ}!", v_catch_s, capsize=96, point=True),
    Cut("町を歩く人も、車の中の人も、知らないうちに、鳥の見はり役!", "知らないうちに\n{見はり役}!", v_upload_s, capsize=96, word="ナルホド"),
    teaser(),
    quiz("クイズ!アラバマ州を、出発したハチドリ。三十八日後、どこにいた?", "Q.38日後\n{どこにいた}?", OPT, 1),
    reveal("正解は、B!北の、アラスカ!およそ、六千五百キロ!", "正解は{B}!\n{アラスカ}!", OPT, 1),
    Cut("体重、一円玉、四枚くらいの鳥が、毎日、およそ、百七十キロも!", "1円玉4枚の鳥が\n{毎日約170km}!", v_coins_s, capsize=92, word="エエッ!"),
    Cut("ハチドリで、記録された、いちばん長い旅です!", "ハチドリで\n{いちばん長い旅}!", P_map, capsize=96, point=True, word="ドドン!"),
    buildup(), openbox(),
    Cut("休む場所が、わかれば、花や森を、守ることにも、つながります。", "休む場所の\n{花や森を守る}", v_rest_s, dream=True, capsize=92),
    Cut("いつか、あなたのスマホも、生き物の、大冒険を、見守るかも!", "あなたのスマホも\n{見守り役}に!?", v_yourphone_s, dream=True, capsize=92, point=True, word="ワクワク"),
    Cut("あなたなら、どんな生き物を、追いかけたい?コメントで教えてね!", "どの生き物を追う?\n{コメントで教えてね}!", v_comment_s, capsize=90, mood="wow"),
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
    name = "20261125_hummingbird_short"
    if len(sys.argv) > 2:
        BADGE["y"] = int(sys.argv[2])
    tl = build4(CUTS, seed=103)
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
