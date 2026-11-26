"""Short (vertical, ~52 s): Japanese jump-roper Kirato Hidaka (Yamaguchi) - 8 rope turns in one jump (GWR 'most revolutions in a
single skip', 17 Jul 2023) and on GWR Day 2026 (19 Nov): 39 consecutive quintuple unders, 11 sextuple, 2 septuple.
Sources: GWR news 'All the action from GWR Day 2026' (19 Nov 2026); GWR record page 114745; NBC (19 Jul 2023); The Japan News/Yomiuri via ANN.
H15: cut 1 = question to the viewer, cut 2 (2.99 s) = the answer (8).
Format type 2 (3D size comparison): Blender row of columns with 1..8 rope loops, camera flows along the row to the 8-loop column
(cuts 1-2); other cuts are 2.5D over a still of the same 3D gym. Palette: navy + orange gym, captions in an UPPER panel, BGM 128 bpm.
No 'くわしい版' badge; last cut sends viewers to the channel."""
import sys, os, math, random
sys.path.insert(0, "/home/claude/dnews-engine")
import numpy as np
import cairo
from PIL import Image
from engine import (W, H, FPS, SR, clamp, ease_out_back, ease_out_cubic, ease_in_out, hexc, text_sprite, draw_sprite,
                    rrect, fill_stroke, circle, burst, sparkles, star, piko, bgm, pil_to_surface)
import engine2 as E2
from engine2 import FONTS, mux2
from timeline import timeline

HERE = os.path.dirname(os.path.abspath(__file__))
INK = "#0D1630"; NAVY = "#14213D"; ORG = "#FF7A00"; CREAM = "#FFF6DC"; PINK = "#FF4D6D"; SKY = "#3A86FF"; YEL = "#FFD166"
COLS = ["#FFB703", "#FB8500", "#FF006E", "#8338EC", "#3A86FF", "#06D6A0", "#FFD166", "#FF4D6D"]

CUTS, TOTAL = timeline()
T3 = CUTS[1]["t0"] + CUTS[1]["d"]


def blit(ctx, surf, x, y, s=1.0, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.translate(-surf.get_width() / 2, -surf.get_height() / 2)
    ctx.set_source_surface(surf, 0, 0); ctx.paint_with_alpha(a); ctx.restore()


_cache = {}
def C(key, fn):
    if key not in _cache:
        _cache[key] = fn()
    return _cache[key]


def label(ctx, text, x, y, size, color="#FFFFFF", hi=ORG, s=1.0, rot=0.0, font="dela", stroke=INK, a=1.0):
    sp = text_sprite(text, size, color=color, hi=hi, stroke=stroke, path=FONTS[font])
    draw_sprite(ctx, sp, x, y, s, a, rot)


def pop(lt, t0=0.0, d=0.32):
    return max(1e-3, ease_out_back(clamp((lt - t0) / d)))


def frame3d(t):
    f = t * 30; a = int(f // 2) * 2; b = a + 2; w = (f - a) / 2
    def load(n):
        p = f"{HERE}/r3d/anim/f{n:04d}.png"
        if not os.path.exists(p):
            fs = sorted(os.listdir(f"{HERE}/r3d/anim")); p = f"{HERE}/r3d/anim/{fs[-1]}"
        return C(("3d", n), lambda: Image.open(p).convert("RGB").resize((W, H), Image.BICUBIC))
    ia, ib = load(a), load(b)
    im = Image.blend(ia, ib, w) if w > 0.01 else ia
    return pil_to_surface(im.convert("RGBA"))


def bg25(ctx, lt, gt, dim=0.35, which="bg"):
    bg = C(which, lambda: pil_to_surface(Image.open(f"{HERE}/r3d/{which}.png").convert("RGBA").resize((W, H), Image.BICUBIC)))
    blit(ctx, bg, W / 2 + 24 * math.sin(gt * 0.35), H / 2 + 8 * math.sin(gt * 0.27), 1.1 + 0.015 * lt)
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(*hexc(NAVY, dim)); ctx.fill()


def panel(ctx, x, y, w, h, col=NAVY, a=0.8, edge=ORG):
    rrect(ctx, x, y, w, h, 36); ctx.set_source_rgba(*hexc(col, a)); ctx.fill_preserve()
    ctx.set_source_rgba(*hexc(edge)); ctx.set_line_width(6); ctx.stroke()


def loops(ctx, x, y, n, s, gt, col, gap=34):
    """a column of n rope loops (front view ellipses), bottom at y"""
    for j in range(n):
        yy = y - j * gap * s
        ph = gt * (3 + 0.6 * n) + j * 0.5
        rx = 90 * s * (0.55 + 0.45 * abs(math.cos(ph))); ry = 26 * s
        ctx.save(); ctx.translate(x, yy); ctx.scale(rx, ry); ctx.new_path(); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
        ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(14 * s); ctx.stroke_preserve()
        ctx.set_source_rgba(*hexc(col)); ctx.set_line_width(8 * s); ctx.stroke()


def jumper(ctx, x, y, s, gt, air=0.0, rope_turn=0.0, col=SKY, rope=ORG):
    """generic illustrated person jumping rope (not a likeness). air: 0..1 height, rope_turn: radians"""
    ctx.save(); ctx.translate(x, y - 160 * air * s); ctx.scale(s, s)
    # rope behind / in front depending on angle
    ang = rope_turn % (2 * math.pi)
    def rope_path():
        ctx.new_path(); ctx.save(); ctx.translate(0, -60); ctx.scale(150, 210 * math.cos(ang) if abs(math.cos(ang)) > 0.05 else 10)
        ctx.arc(0, 0, 1, math.pi, 2 * math.pi) if math.cos(ang) > 0 else ctx.arc(0, 0, 1, 0, math.pi); ctx.restore()
    rope_path(); ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(14); ctx.stroke_preserve(); ctx.set_source_rgba(*hexc(rope)); ctx.set_line_width(8); ctx.stroke()
    # legs (tucked when in air)
    k = 30 * air
    for sx in (-1, 1):
        ctx.new_path(); ctx.move_to(sx * 22, 40); ctx.line_to(sx * (28 + k), 100 - k); ctx.line_to(sx * 26, 150 - 2 * k)
        ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(26); ctx.stroke_preserve(); ctx.set_source_rgba(*hexc("#2B2D42")); ctx.set_line_width(16); ctx.stroke()
    rrect(ctx, -48, -60, 96, 115, 34); fill_stroke(ctx, col, INK, 7)
    for sx in (-1, 1):  # arms to handles
        ctx.new_path(); ctx.move_to(sx * 40, -40); ctx.line_to(sx * 110, 0); ctx.line_to(sx * 150, -60)
        ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(22); ctx.stroke_preserve(); ctx.set_source_rgba(*hexc("#FFD6B0")); ctx.set_line_width(13); ctx.stroke()
        rrect(ctx, sx * 150 - 12, -90, 24, 50, 10); fill_stroke(ctx, ORG, INK, 5)
    circle(ctx, 0, -110, 46, "#FFD6B0", INK, 7)
    ctx.new_path(); ctx.arc(0, -122, 48, math.pi, 2 * math.pi); ctx.set_source_rgba(*hexc("#2B2D42")); ctx.fill()
    circle(ctx, -16, -104, 6, INK, INK, 1); circle(ctx, 16, -104, 6, INK, INK, 1)
    ctx.restore()


# ------------------------------------------------------------------ cuts
def v_hook(ctx, lt, d, gt):
    q = 1.0 + 0.06 * math.sin(gt * 6)
    label(ctx, "何回?", W / 2, 760, 200, color=CREAM, s=q * pop(lt, 0.0, 0.25), rot=-0.05)
    label(ctx, "?", 880, 640 + 14 * math.sin(gt * 5), 220, color=ORG, s=q, rot=0.18)


def v_answer(ctx, lt, d, gt):
    s = pop(lt, 0.0, 0.35)
    burst(ctx, W / 2, 720, 330 + 20 * math.sin(gt * 10), gt, ORG, n=18, alpha=0.85)
    label(ctx, "8回!", W / 2, 720, 270, color=CREAM, s=s * (1 + 0.04 * math.sin(gt * 9)), rot=-0.05)
    sparkles(ctx, W / 2, 720, lt, 0.1, "#FFFFFF", 14, 420)
    if lt > 1.3:
        p = pop(lt, 1.3)
        ctx.save(); ctx.translate(W / 2, 1000); ctx.scale(p, p); rrect(ctx, -330, -60, 660, 120, 60); fill_stroke(ctx, ORG, INK, 7); ctx.restore()
        label(ctx, "ひだか きらと選手(山口県)", W / 2, 1000, 50, color="#FFFFFF", font="maru", s=p)


def v_x4(ctx, lt, d, gt):
    bg25(ctx, lt, gt, 0.45)
    panel(ctx, 60, 620, 960, 900, a=0.7)
    loops(ctx, 300, 1300, 2, 1.25 * pop(lt, 0.1), gt, COLS[1], gap=60)
    loops(ctx, 780, 1300, 8, 1.25 * pop(lt, 0.6), gt, COLS[7], gap=60)
    label(ctx, "二重とび", 300, 1420, 60, font="maru", s=pop(lt, 0.1))
    label(ctx, "八重とび", 780, 1420, 60, font="maru", s=pop(lt, 0.6))
    if lt > 1.2:
        label(ctx, "×4", 540, 950, 170, color=ORG, hi=ORG, stroke=CREAM, s=pop(lt, 1.2), rot=-0.1)


def v_instant(ctx, lt, d, gt):
    bg25(ctx, lt, gt, 0.5)
    cyc = 1.4; u = (lt % cyc) / cyc
    air = math.sin(math.pi * u)
    turns = int(min(8, 8 * u + 0.001)) if u < 0.999 else 8
    jumper(ctx, W / 2, 1300, 1.7, gt, air=air, rope_turn=u * 8 * 2 * math.pi)
    # counter of turns during the jump
    rrect(ctx, W / 2 - 170, 650, 340, 170, 40); fill_stroke(ctx, CREAM, INK, 8)
    label(ctx, f"{turns}回", W / 2, 735, 110, color=INK, hi=INK, stroke=CREAM)
    label(ctx, "イメージ", 130, 1500, 36, font="zen")
    # floor shadow
    ctx.save(); ctx.translate(W / 2, 1560); ctx.scale(200 * (1 - 0.4 * air), 26); ctx.new_path(); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
    ctx.set_source_rgba(0, 0, 0, 0.35); ctx.fill()


def v_tries(ctx, lt, d, gt):
    bg25(ctx, lt, gt, 0.55)
    # clock
    cx, cy, R = 330, 1000, 210
    p = pop(lt, 0.05)
    ctx.save(); ctx.translate(cx, cy); ctx.scale(p, p)
    circle(ctx, 0, 0, R, CREAM, INK, 10)
    g = ease_in_out(clamp((lt - 0.4) / 3.0))
    ctx.new_path(); ctx.move_to(0, 0); ctx.arc(0, 0, R - 20, -math.pi / 2, -math.pi / 2 + 2 * math.pi * 50 / 60 * g); ctx.close_path()
    ctx.set_source_rgba(*hexc(ORG, 0.55)); ctx.fill()
    for k in range(12):
        a = k * math.pi / 6; ctx.new_path(); ctx.move_to((R - 30) * math.cos(a), (R - 30) * math.sin(a)); ctx.line_to((R - 10) * math.cos(a), (R - 10) * math.sin(a))
        ctx.set_source_rgba(*hexc(INK)); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()
    label(ctx, f"{int(50 * g)}分", cx, cy + R + 90, 90, s=p)
    # tries counter
    n = int(28 * ease_out_cubic(clamp((lt - 0.6) / 3.2)))
    rrect(ctx, 600, 820, 400, 360, 40); fill_stroke(ctx, NAVY, ORG, 8)
    label(ctx, "ちょうせん", 800, 890, 54, font="maru")
    label(ctx, f"約{n}回", 800, 1040, 110, color=CREAM)
    label(ctx, "2023年・中学生のとき", W / 2, 1480, 60, font="maru", s=pop(lt, 0.3))


def v_day(ctx, lt, d, gt):
    bg25(ctx, lt, gt, 0.45)
    p = pop(lt, 0.05)
    ctx.save(); ctx.translate(W / 2, 1050); ctx.scale(p, p); ctx.rotate(-0.04)
    rrect(ctx, -300, -330, 600, 660, 40); fill_stroke(ctx, "#FFFFFF", INK, 10)
    rrect(ctx, -300, -330, 600, 160, 40); fill_stroke(ctx, ORG, INK, 10)
    for k in (-200, 200):
        rrect(ctx, k - 18, -380, 36, 100, 14); fill_stroke(ctx, "#9AA5B1", INK, 6)
    ctx.restore()
    label(ctx, "2026年11月", W / 2, 960 - 210 * p + 10, 64, color="#FFFFFF", s=p, rot=-0.04)
    label(ctx, "19", W / 2, 1110, 300, color=INK, hi=INK, stroke="#FFFFFF", s=p, rot=-0.04)
    if lt > 1.4:
        label(ctx, "ギネス世界記録の日", W / 2, 1500, 76, color=CREAM, s=pop(lt, 1.4), rot=-0.03)


def v_39(ctx, lt, d, gt):
    bg25(ctx, lt, gt, 0.5)
    per = 0.07; n = min(39, int(max(0, lt - 0.3) / per))
    u = ((lt - 0.3) % per) / per if n < 39 else 0.5
    jumper(ctx, 330, 1350, 1.15, gt, air=0.6 * math.sin(math.pi * u), rope_turn=u * 5 * 2 * math.pi, col=COLS[4])
    rrect(ctx, 580, 840, 440, 330, 40); fill_stroke(ctx, CREAM, INK, 8)
    label(ctx, "五重とび", 800, 910, 56, color=INK, hi=INK, stroke=CREAM, font="maru")
    label(ctx, f"{n}回", 800, 1060, 140, color=ORG, hi=ORG, stroke=INK)
    if n >= 39:
        burst(ctx, 800, 1060, 280 + 15 * math.sin(gt * 10), gt, YEL, n=16, alpha=0.7)
        label(ctx, "連続!", 800, 1260, 90, color=CREAM, s=pop(lt, 0.3 + 39 * per))
    label(ctx, "イメージ", 130, 1560, 36, font="zen")


def v_bars(ctx, lt, d, gt):
    bg25(ctx, lt, gt, 0.5)
    panel(ctx, 50, 640, 980, 1000, a=0.72)
    base = 1440
    for k, (lab, val, col) in enumerate([("五重", 39, COLS[4]), ("六重", 11, COLS[5]), ("七重", 2, COLS[7])]):
        x = 230 + k * 310
        g = ease_out_cubic(clamp((lt - 0.2 - 0.6 * k) / 0.9))
        h = 14 * val * g
        rrect(ctx, x - 100, base - h - 4, 200, h + 4, 22); fill_stroke(ctx, col, INK, 8)
        if g > 0.05:
            label(ctx, f"{int(round(val * g))}回", x, base - h - 70, 84, color=CREAM)
        label(ctx, lab, x, base + 80, 66, font="maru")
    label(ctx, "連続記録", W / 2, 700, 66, font="maru", s=pop(lt, 0.1))


def v_195(ctx, lt, d, gt):
    bg25(ctx, lt, gt, 0.55)
    panel(ctx, 50, 600, 980, 1000, a=0.72)
    n = int(195 * ease_in_out(clamp((lt - 0.4) / 3.4)))
    for i in range(195):
        r, c = divmod(i, 13); x = 125 + c * 70; y = 700 + r * 52
        on = i < n
        ctx.save(); ctx.translate(x, y); ctx.scale(26, 16); ctx.new_path(); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
        ctx.set_source_rgba(*hexc(COLS[(i // 5) % 8] if on else "#3B4A6B")); ctx.set_line_width(7); ctx.stroke()
    rrect(ctx, W / 2 - 250, 1490, 500, 150, 40); fill_stroke(ctx, CREAM, INK, 8)
    label(ctx, f"{n}回", W / 2, 1565, 110, color=ORG, hi=ORG, stroke=INK)
    label(ctx, "5回 × 39ジャンプ", W / 2, 530, 64, font="maru", s=pop(lt, 0.2))


def v_comment(ctx, lt, d, gt):
    bg25(ctx, lt, gt, 0.4)
    u = (gt % 0.6) / 0.6
    jumper(ctx, 400, 1300, 1.3, gt, air=0.5 * math.sin(math.pi * u), rope_turn=u * 2 * 2 * math.pi, col=PINK)
    piko(ctx, 840, 1250, gt, 1.2, "smile")
    if lt > 1.6:
        label(ctx, "コメントで教えてね!", W / 2, 800, 80, s=pop(lt, 1.6), rot=-0.04)


def v_end(ctx, lt, d, gt):
    bg25(ctx, lt, gt, 0.5)
    piko(ctx, W / 2, 1050, gt, 2.0, "smile")
    label(ctx, "今日のワクワクニュース", W / 2, 700, 76, s=pop(lt, 0.1), color=CREAM)
    for k in range(6):
        a = gt * 1.5 + k * math.pi / 3
        star(ctx, W / 2 + 330 * math.cos(a), 1030 + 330 * math.sin(a), 34, [ORG, "#FFFFFF", PINK][k % 3])


VIS = [v_hook, v_answer, v_x4, v_instant, v_tries, v_day, v_39, v_bars, v_195, v_comment, v_end]
MOOD = ["wow", "wow", "wow", None, "smile", "smile", None, "wow", "wow", None, None]


def top_tag(ctx):
    rrect(ctx, 30, 40, 420, 74, 37); ctx.set_source_rgba(*hexc(NAVY, 0.88)); ctx.fill_preserve()
    ctx.set_source_rgba(*hexc(ORG)); ctx.set_line_width(4); ctx.stroke()
    label(ctx, "今日のワクワク|スポーツ", 240, 77, 36, font="maru", color="#FFFFFF", stroke=NAVY)


def caption(ctx, cut, lt):
    p = 1.0 if cut["i"] == 0 else ease_out_cubic(clamp(lt / 0.22))
    y = 330 - 40 * (1 - p)
    ctx.save(); ctx.translate(W / 2, y); ctx.rotate(-0.02)
    rrect(ctx, -500, -140, 1000, 280, 30); ctx.set_source_rgba(*hexc(ORG, p)); ctx.fill_preserve()
    ctx.set_source_rgba(*hexc(INK, p)); ctx.set_line_width(8); ctx.stroke(); ctx.restore()
    sp = text_sprite(cut["cap"], 84, color="#FFFFFF", hi=YEL, stroke=INK, path=FONTS["dela"])
    draw_sprite(ctx, sp, W / 2, y, min(1.0, 930 / sp.get_width(), 250 / sp.get_height()) * (0.9 + 0.1 * p), p, -0.02)


def find(gt):
    for c in CUTS:
        if c["t0"] <= gt < c["t0"] + c["d"]:
            return c
    return CUTS[-1]


def frame(ctx, gt):
    c = find(gt); lt = gt - c["t0"]
    ctx.set_source_rgb(*hexc(NAVY)[:3]); ctx.paint()
    if gt < T3:
        blit(ctx, frame3d(min(gt, 7.85)), W / 2, H / 2, 1.0)
    VIS[c["i"]](ctx, lt, c["d"], gt)
    if MOOD[c["i"]]:
        piko(ctx, 940, 1680, gt, 0.7, MOOD[c["i"]])
    top_tag(ctx)
    caption(ctx, c, lt)
    if lt < 0.08 and c["i"] > 0:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(1, 1, 1, 0.35 * (1 - lt / 0.08)); ctx.fill()


def SF(name):
    import engine3 as E3
    try:
        return E2.sfx(name)
    except KeyError:
        return E3.sfx3(name)


def whirl(dur=0.9, turns=8):
    n = int(dur * SR); tt = np.arange(n) / SR
    env = np.abs(np.sin(np.pi * turns * tt / dur)) ** 3 * np.exp(-tt * 0.8)
    no = np.random.default_rng(5).standard_normal(n); no = np.convolve(no, np.ones(8) / 8, mode="same")
    return 0.6 * no * env


def build_audio(path):
    n = int(TOTAL * SR); voice = np.zeros(n); fx = np.zeros(n)
    def add(buf, sig, at, g=1.0):
        st = int(at * SR)
        if st >= n: return
        e = min(n, st + len(sig)); buf[st:e] += g * sig[: e - st]
    for c in CUTS:
        add(voice, c["audio"], c["t0"] + 0.06)
        if c["i"] > 0:
            add(fx, SF("whoosh"), c["t0"], 0.5)
    add(fx, whirl(), 0.6, 0.8)
    add(fx, SF("impact"), CUTS[1]["t0"], 0.9); add(fx, SF("kira"), CUTS[1]["t0"] + 0.2, 0.7)
    add(fx, SF("tada"), CUTS[2]["t0"] + 1.2, 0.6)
    for k in range(3):
        add(fx, whirl(1.2, 8), CUTS[3]["t0"] + 1.4 * k, 0.5)
    for k in range(10):
        add(fx, SF("tick"), CUTS[4]["t0"] + 0.6 + 0.3 * k, 0.35)
    add(fx, SF("ding"), CUTS[5]["t0"] + 1.4, 0.6)
    for k in range(39):
        add(fx, SF("pop2"), CUTS[6]["t0"] + 0.3 + 0.07 * k, 0.18)
    add(fx, SF("tada"), CUTS[6]["t0"] + 0.3 + 39 * 0.07, 0.6)
    add(fx, SF("slideup"), CUTS[7]["t0"] + 0.2, 0.5)
    add(fx, SF("kira"), CUTS[8]["t0"] + 3.8, 0.6)
    add(fx, SF("kira"), CUTS[10]["t0"] + 0.1, 0.7)
    voice = voice / (np.max(np.abs(voice)) or 1) * 0.9
    envv = np.convolve(np.abs(voice) > 0.02, np.ones(int(0.15 * SR)) / int(0.15 * SR), mode="same")
    duck = 1 - 0.7 * np.clip(envv * 3, 0, 1)
    music = bgm(TOTAL, bpm=128, key=2)[:n]
    music = music / (np.max(np.abs(music)) or 1) * 0.36 * duck
    mix = voice * 1.15 + music + fx * 0.5
    mix = mix / max(np.max(np.abs(mix)), 1e-6) * 0.9
    import wave
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())


def render(path, times=None, prev_dir=None):
    import subprocess
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    def draw(t):
        ctx = cairo.Context(surf); frame(ctx, t); surf.flush()
    if times:
        os.makedirs(prev_dir, exist_ok=True)
        for t in times:
            draw(t); surf.write_to_png(f"{prev_dir}/t{t:05.2f}.png")
        return
    tmp = path[:-4] + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(int(round(TOTAL * FPS))):
        draw(i / FPS); p.stdin.write(bytes(surf.get_data()))
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError("ffmpeg failed")
    os.replace(tmp, path)


if __name__ == "__main__":
    name = "20261126_jumprope_short"
    print("total", round(TOTAL, 2), "cut2 at", round(CUTS[1]["t0"], 2))
    if sys.argv[1:] and sys.argv[1] == "preview":
        ts = [float(x) for x in sys.argv[2:]] or [c["t0"] + min(2.2, c["d"] * 0.7) for c in CUTS]
        render(None, ts, f"{HERE}/preview")
    else:
        os.makedirs(f"{HERE}/out", exist_ok=True)
        if not (sys.argv[1:] and sys.argv[1] == "audio"):
            render(f"{HERE}/out/{name}_video.mp4")
        build_audio(f"{HERE}/out/{name}.wav")
        mux2(f"{HERE}/out/{name}_video.mp4", f"{HERE}/out/{name}.wav", f"{HERE}/out/{name}_final.mp4")
