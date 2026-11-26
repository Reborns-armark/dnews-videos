"""Short (vertical, ~55 s): physicists sent a message through a brick wall using gravity and a 1950s elevator counterweight
(Groszek et al., 'Unblockable communication with gravity', Science Advances 2026, doi:10.1126/sciadv.aee0802; University of Queensland).
EXPERIMENT A (set 1, 2026-11-26 7:30; today's experiment A=set 1, B=set 3). Hypothesis H15: cut 1 is a question to the viewer
('あなたは、エレベーターで、かべの向こうに文字を送れる?') and the answer comes in cut 2 (within 3 s). Extraction point (elevator -> message through a wall)
and the cut-1 picture (drawn elevator/wall/gravimeter scene, same as the standard hook) are unchanged.
Facts cut out: it works (counterweight up=1/down=0, gravimeter next door) / one word took about an hour (quiz) / gravity can't be blocked.
Top-left badge shown the whole time."""
import sys, os, math
from common4 import *
from hera_vis import *
import hera_vis
hera_vis.PHOTO_LAYOUT.update(cy=640, scale=0.62)
from grav_vis import *
import grav_vis
grav_vis.OPTS["short"] = True
from space3 import eyes


def fit(vis, a=195.0, b=0.66):
    """Shrink a 1080x1920-stage scene so its title clears the header and its bottom clears the caption."""
    def f(ctx, lt, d, gt):
        ctx.save(); ctx.translate(CX * (1 - b), a); ctx.scale(b, b); vis(ctx, lt, d, gt); ctx.restore()
    return f


v_hook_s, v_word_s, v_bits_s, v_shield_s, v_stuck_s, v_comment_s, v_hour_s = map(
    fit, (v_hook_q, v_word, v_bits, v_shield, v_stuck, v_comment, v_hour))

OPT = ["約1秒", "約1分", "約1時間"]
CUTS = [
    eyes(Cut("あなたは、エレベーターで、かべの向こうに文字を送れる?", "かべの向こうに\n{文字を送れる}?", v_hook_s, capsize=80, mood="wow"), [], hit=True, word="エエッ!?"),
    Cut("答えは、送れる!オーストラリアの科学者が、重力を使って、本当に、送ったんです!", "答えは{送れる}!\n重力で本当に送った", v_word_s, capsize=92, point=True, word="スゴイ!"),
    Cut("一・八トンの、おもりが、上なら一、下ならゼロ。となりの部屋の、重力計が、読み取りました。", "おもりが上なら{1}\n下なら{0}", v_bits_s, capsize=92, point=True),
    teaser(),
    quiz("クイズ!グラビティ、の一語を、送るのに、かかった時間は?", "Q.1語を送るのに\n{かかった時間}は?", OPT, 2),
    reveal("正解は、C!およそ、一時間!一けた送るのに、一分かかる、のんびり通信です!", "正解は{C}!\n{約1時間}!", OPT, 2),
    Cut("でも、重力は、どんなかべでも、さえぎれない。鉄も、水も、すりぬけて、電波が、とどかない場所にも、とどくんです!", "重力は\n{さえぎれない}!", v_shield_s, capsize=92, point=True, word="ナルホド"),
    buildup(), openbox(),
    Cut("論文には、電波も、音も、通さない、エレベーターに、とじこめられたら、これで、助けを、よべる、なんて、ジョークまで!", "とじこめられたら\n{助けをよべる}!?", v_stuck_s, dream=True, capsize=88, point=True, word="ワクワク"),
    Cut("あなたなら、重力通信で、だれに、どんな言葉を送る?コメントで教えてね!", "重力で何を送る?\n{コメントで教えてね}!", v_comment_s, capsize=86, mood="wow"),
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
    name = "20261126_gravity_short"
    if len(sys.argv) > 2:
        BADGE["y"] = int(sys.argv[2])
    tl = build4(CUTS, seed=137)
    f0 = make_frame4(tl, "科学", "#2E86DE")
    def frame(ctx, gt):
        f0(ctx, gt); badge(ctx, gt)
        frame.e, frame.lt = f0.e, f0.lt
    print("total", round(tl["total"], 2), "cuts", len(tl["cuts"]), "points", tl["npoints"])
    for c in tl["cuts"][:2]:
        print(" cut", round(c["t0"], 2), round(c["d"], 2))
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
