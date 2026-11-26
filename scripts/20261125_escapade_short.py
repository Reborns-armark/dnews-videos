"""Short (vertical, ~55 s) for the ESCAPADE farewell-Earth photo (NASA blog 2026-11-23). EXPERIMENT B (set 1, 2026-11-25 07:30).
Changed element (only one): the FIRST picture. Cut 1 shows the real NASA photo of Earth taken by ESCAPADE (with credit) instead of a drawn
illustration. Narration style of cut 1 stays standard ("〜!?" exclamation, no greeting).
Facts cut out: photo of Earth from ~62,000 km by a Mars-bound probe / it waited ~1 year 1.5 million km away, then fired its engine
while skimming past Earth (quiz) / twins will study how Mars lost its air (arrive Sept 2027).
Top-left badge (Piko face button + "↓くわしい版はここから!") is shown the whole time."""
import sys, os, math
from common4 import *
from hera_vis import *
import hera_vis
hera_vis.PHOTO_LAYOUT.update(cy=640, scale=0.62)
from escapade_vis import *
import escapade_vis
escapade_vis.OPTS["short"] = True
from space3 import eyes


def fit(vis, a=195.0, b=0.66):
    """Shrink a 1080x1920-stage scene so its title clears the header and its bottom clears the caption."""
    def f(ctx, lt, d, gt):
        ctx.save(); ctx.translate(CX * (1 - b), a); ctx.scale(b, b); vis(ctx, lt, d, gt); ctx.restore()
    return f


v_l2_s, v_flyby_s, v_burn_s, v_skate_s, v_strip_s, v_two_s, v_comment_s, v_route_s, v_earth5_s, v_year_s = map(
    fit, (v_l2, v_flyby, v_burn, v_skate, v_strip, v_two_orbits, v_comment, v_route, v_earth5, v_year))

CAM = "NASA/UC Berkeley/Northern Arizona University"
P_hook = P("e_vis", CAM, None, box=(1037, 1000), crop=(120, 50, 700, 675))
P_vis = P("e_vis", CAM, "本物の写真!", box=(880, 709), crop=(250, 0, 800, 650))
P_ro = P("e_ir_ro", CAM, "赤外線だと…", box=(880, 721))
P_twin = P("k_twin", "NASA/Kim Shiflett", "ふたごの探査機", box=(960, 640))
OPT = ["月のうら側", "地球から150万km", "もう火星のそば"]
CUTS = [
    eyes(Cut("火星へ行く探査機が、ふりかえって、地球を撮った!?", "火星へ行く探査機が\n{地球を撮った}!?", P_hook, capsize=96, mood="wow"), [], hit=True),
    Cut("撮ったのは、NASAの、ふたごの探査機、エスカペード。十一月二十三日に、公開されました。", "NASAの\n{エスカペード}", P_twin, capsize=96, point=True),
    Cut("地球から、およそ、六万二千キロ。地球、五こ分の、きょりです。", "約{6万2000km}\n地球5こ分", v_earth5_s, capsize=96),
    Cut("手前は、探査機の、太陽電池パネル。まるで、自撮りですね!", "手前は\n{パネル}で自撮り!", P_vis, capsize=96, word="パチリ!"),
    teaser(),
    quiz("クイズ!打ち上げから、およそ一年。この探査機は、どこで待っていた?", "Q.1年間\n{どこで待っていた}?", OPT, 1),
    reveal("正解は、B!地球から、百五十万キロの、場所で、まちぼうけ!", "正解は{B}!\n{150万km}でまちぼうけ", OPT, 1),
    Cut("火星への、ならびを待って、地球の、すぐ横を、すりぬけながら、エンジンを、九分間ふかして、加速したんです!", "すりぬけながら\n{9分間噴射}!", v_burn_s, capsize=92, point=True, word="ゴオォ!"),
    buildup(), openbox(),
    Cut("火星に着くのは、二千二十七年、九月。二台で、火星の空気が、にげた、なぞに、いどみます!", "2027年9月\n{火星のなぞ}に挑む!", v_two_s, dream=True, capsize=92, point=True, word="ワクワク"),
    Cut("あなたなら、宇宙から、何を撮りたい?コメントで教えてね!", "宇宙から何を撮る?\n{コメントで教えてね}!", v_comment_s, capsize=90, mood="wow"),
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
    name = "20261125_escapade_short"
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
