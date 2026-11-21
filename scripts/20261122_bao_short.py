"""Short (vertical, ~55 s): a star swallowed its companion. Only the most fun part; points to the long version."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common4 import *
from space3 import eyes
from bao_vis import *
import hera_vis
hera_vis.PHOTO_LAYOUT.update(cy=700, scale=0.7)


def low(vis):
    """Shift every scene down a little so the top-left badge never touches it."""
    def f(ctx, lt, d, gt):
        ctx.save(); ctx.translate(CX, CY + 170); ctx.scale(0.85, 0.85); ctx.translate(-CX, -CY)
        vis(ctx, lt, d, gt); ctx.restore()
    return f


def badge(ctx, gt):
    """Top-left, always on: Piko face button + 'くわしい版はここから!'."""
    x, y, w, h = 36, 338, 520, 84
    rrect(ctx, x, y, w, h, 42); ctx.set_source_rgba(1, 1, 1, 0.95); ctx.fill_preserve()
    ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(5); ctx.stroke()
    bx, by = x + 44, y + h / 2
    circle(ctx, bx, by + 3, 36, "#C4302B", lw=0)
    circle(ctx, bx, by, 36, "#FF3D3D", stroke="#1B1B3A", lw=4)
    ctx.save(); ctx.new_path(); ctx.arc(bx, by, 32, 0, 2 * math.pi); ctx.clip()
    circle(ctx, bx, by + 4, 26, "#FFD23F", stroke="#1B1B3A", lw=3)
    for sx in (-1, 1):
        circle(ctx, bx + sx * 9, by, 4.5, "#1B1B3A", lw=0)
    ctx.new_path(); ctx.arc(bx, by + 8, 8, 0.2, math.pi - 0.2); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(3); ctx.stroke()
    ctx.restore()
    bob = 4 * math.sin(gt * 5)
    draw_sprite(ctx, text_sprite("↓くわしい版はここから!", 38, color="#1B1B3A", hi="#FF3D7F", stroke="#FFFFFF", stroke_w=2,
                                 shadow=False, path=FONTS["mochiy"]), x + 300, y + h / 2 + bob, 1, 1)


OPT = ["35倍", "350倍", "3500倍"]
CUTS = [
    eyes(Cut("星が、となりの星を、まるごと、食べちゃった!", "星が星を\n{まるごと食べた}!", low(v_hook_eat), capsize=104, mood="wow"), [], hit=True, word="パクッ!"),
    Cut("え!?星が、星を、食べるの!?", "え!?星が\n{星を食べる}の!?", low(v_question), capsize=104, mood="wow", word="ムムッ"),
    Cut("場所は、アンドロメダ銀河。その一部始終を、はじめて、まるごと観測!", "{はじめて}\nまるごと観測!", low(P_main), capsize=100, capy=1420, point=True, word="ワオ!"),
    teaser(),
    Cut("食べたのは、ぶくぶくに、ふくらんだ、巨大な星。", "食べたのは\n{ふくらんだ巨大な星}", low(v_binary), capsize=96),
    quiz("クイズ!その星の直径は、太陽の、何倍?", "Q.直径は\n{太陽の何倍}?", OPT, 1),
    reveal("正解は、B!三百五十倍!", "正解は{B}!\n{350倍}!", OPT, 1),
    Cut("太陽が、この点だとしたら、画面に、入りきらない!", "太陽が点なら\n{画面に入らない}!", low(v_sun_vs), capsize=100, word="ドーン!"),
    Cut("太陽の場所に置いたら、火星の通り道まで、すっぽり!", "火星の通り道まで\n{すっぽり}!", low(v_orbits), capsize=100, point=True, word="ゴゴゴ"),
    Cut("小さな星は、ガスの中で、ぐるぐる落ちて、パクッ!", "ぐるぐる落ちて\n{パクッ}!", low(v_spiral), capsize=100),
    Cut("ガスの中で、ブレーキがかかって、もう、にげられないんだ!", "ブレーキがかかって\n{にげられない}!", low(v_brake), capsize=96),
    buildup(), openbox(),
    Cut("最後は、たった一週間で、大爆発!星の中で、爆弾が爆発したみたいだって!", "{1週間}で大爆発!\n星の中で{爆弾}!?", low(v_bomb), dream=True, capsize=92, point=True, word="ドーン!"),
    Cut("アンドロメダ銀河は、いま、秋の夜空で見られるよ!", "アンドロメダ銀河は\n{いま秋の夜空に}!", low(v_sky), dream=True, capsize=96, point=True, word="キラーン"),
    Cut("じつは、二百五十万年前の事件?太陽は大丈夫?答えは、くわしい版で!", "250万年前の事件!?\n{太陽は大丈夫}?", low(v_question), dream=True, capsize=92),
    Cut("続きは、下のリンクの特別編で!", "続きは\n{下のリンクの特別編}で!", low(v_long_short), capsize=96, sfx=[(0.2, "kira")]),
]

if __name__ == "__main__":
    name = "20261122_bao_short"
    tl = build4(CUTS, seed=53)
    f4 = make_frame4(tl, "宇宙", "#7B5CFF")
    def frame(ctx, gt):
        f4(ctx, gt); badge(ctx, gt)
        frame.e, frame.lt = f4.e, f4.lt
    print("total", round(tl["total"], 2), "cuts", len(tl["cuts"]), "points", tl["npoints"], flush=True)
    if sys.argv[1:] and sys.argv[1] == "preview":
        ts = [c["t0"] + min(0.6, c["d"] / 2) for c in tl["cuts"]] + [c["t0"] + c["d"] - 0.3 for c in tl["cuts"]]
        render3(None, tl, frame, ts, f"preview4/{name}")
    else:
        os.makedirs("out4", exist_ok=True)
        render3(f"out4/{name}_video.mp4", tl, frame)
        build_audio4(f"out4/{name}.wav", tl, 1)
        mux2(f"out4/{name}_video.mp4", f"out4/{name}.wav", f"out4/{name}_final.mp4")
        print("done", flush=True)
