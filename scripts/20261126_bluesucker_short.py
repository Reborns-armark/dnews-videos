"""Short (vertical, ~52 s): a 131-year-old river fish (blue sucker, Upper Missouri River, Montana).
Lackmann et al., 'Bomb-radiocarbon validated otoliths reveal 130-year lifespans and declining recruitment for blue sucker
Cycleptus elongatus of the Upper Missouri River, Montana, USA', Communications Biology 9, 1515 (2026-11-18), doi:10.1038/s42003-026-11219-3.
H15 (all Shorts): cut 1 = question to the viewer, cut 2 (3.05 s) = the answer (131).
Format type 1 (3D zoom dive): Blender camera dives from the river surface to the fish (cuts 1-2); the other cuts are 2.5D layers
over stills from the same 3D scene. Own palette (river green / amber), captions in a lower panel, calmer BGM (96 bpm).
No 'くわしい版' badge (no long video for this slot); last cut sends viewers to the channel."""
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
DL = "/home/claude/work/dl"
INK = "#0B2B29"; DEEP = "#0B3D3A"; TEAL = "#1E7A6E"; AMB = "#FFB000"; CREAM = "#FFF6DC"; PINK = "#FF5C8A"

CUTS, TOTAL = timeline()
T3 = CUTS[1]["t0"] + CUTS[1]["d"]


def img(path, w=None, h=None):
    im = Image.open(path).convert("RGBA")
    if w and h:
        im = im.resize((w, h), Image.LANCZOS)
    elif w:
        im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    return pil_to_surface(im)


def blit(ctx, surf, x, y, s=1.0, a=1.0, center=True):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if center:
        ctx.translate(-surf.get_width() / 2, -surf.get_height() / 2)
    ctx.set_source_surface(surf, 0, 0); ctx.paint_with_alpha(a); ctx.restore()


_cache = {}
def C(key, fn):
    if key not in _cache:
        _cache[key] = fn()
    return _cache[key]


def label(ctx, text, x, y, size, color="#FFFFFF", hi=AMB, s=1.0, rot=0.0, font="maru", stroke=INK, a=1.0):
    sp = text_sprite(text, size, color=color, hi=hi, stroke=stroke, path=FONTS[font])
    draw_sprite(ctx, sp, x, y, s, a, rot)


def pop(lt, t0=0.0, d=0.32):
    return max(1e-3, ease_out_back(clamp((lt - t0) / d)))


# ------------------------------------------------------------------ 3D frames (15 fps rendered -> blended to 30 fps)
def frame3d(t):
    f = t * 30
    a = int(f // 2) * 2; b = a + 2; w = (f - a) / 2
    def load(n):
        p = f"{HERE}/r3d/anim/f{n:04d}.png"
        if not os.path.exists(p):
            files = sorted(os.listdir(f"{HERE}/r3d/anim")); p = f"{HERE}/r3d/anim/{files[-1]}"
        return C(("3d", n), lambda: Image.open(p).convert("RGB").resize((W, H), Image.BICUBIC))
    ia, ib = load(a), load(b)
    im = Image.blend(ia, ib, w) if w > 0.01 else ia
    return pil_to_surface(im.convert("RGBA"))


# ------------------------------------------------------------------ shared 2.5D layers
def bg25(ctx, lt, gt, tint=0.0, zoom=1.08):
    bg = C("bg", lambda: img(f"{HERE}/r3d/bg.png", W, H))
    s = zoom + 0.02 * lt
    blit(ctx, bg, W / 2 + 20 * math.sin(gt * 0.4), H / 2 + 10 * math.sin(gt * 0.3), s)
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(*hexc(DEEP, 0.25 + tint)); ctx.fill()


def bubbles(ctx, gt, n=26, seed=3, front=False):
    rnd = random.Random(seed)
    for i in range(n):
        x0 = rnd.uniform(0, W); sp = rnd.uniform(60, 160) * (1.6 if front else 1); r = rnd.uniform(6, 18) * (1.8 if front else 1)
        y = H + 100 - ((gt * sp + rnd.uniform(0, H + 200)) % (H + 200))
        x = x0 + 18 * math.sin(gt * 2 + i)
        ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi)
        ctx.set_source_rgba(1, 1, 1, 0.18 if front else 0.28); ctx.fill_preserve()
        ctx.set_source_rgba(1, 1, 1, 0.55); ctx.set_line_width(2.5); ctx.stroke()


def weeds_front(ctx, gt):
    for k, (x, h, c) in enumerate([(40, 520, "#2F6B2A"), (110, 380, "#3F8A35"), (990, 560, "#2F6B2A"), (1050, 420, "#3F8A35")]):
        ctx.new_path(); ctx.move_to(x - 26, H)
        sw = 40 * math.sin(gt * 1.3 + k)
        ctx.curve_to(x - 30 + sw * 0.3, H - h * 0.4, x + sw, H - h * 0.7, x + sw * 1.4, H - h)
        ctx.curve_to(x + 16 + sw, H - h * 0.7, x + 20 + sw * 0.3, H - h * 0.4, x + 26, H)
        ctx.close_path(); ctx.set_source_rgba(*hexc(c, 0.92)); ctx.fill()


def fishicon(ctx, x, y, s, col="#B4C0C4", flip=False, gt=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(-s if flip else s, s); ctx.rotate(0.05 * math.sin(gt * 5 + x))
    ctx.new_path(); ctx.save(); ctx.scale(1, 0.32); ctx.arc(0, 0, 60, 0, 2 * math.pi); ctx.restore()
    fill_stroke(ctx, col, INK, 5)
    ctx.new_path(); ctx.move_to(52, 0); ctx.line_to(92, -26); ctx.line_to(84, 0); ctx.line_to(92, 26); ctx.close_path()
    fill_stroke(ctx, "#8DA6B4", INK, 5)
    ctx.new_path(); ctx.move_to(-18, -16); ctx.line_to(2, -44); ctx.line_to(14, -16); ctx.close_path(); fill_stroke(ctx, "#8DA6B4", INK, 4)
    circle(ctx, -40, -4, 5, INK, INK, 1)
    ctx.restore()


def credit(ctx, text, y):
    sp = text_sprite(text, 30, color="#FFFFFF", stroke=INK, stroke_w=5, shadow=False, path=FONTS["zen"])
    draw_sprite(ctx, sp, W / 2, y, min(1.0, 1000 / sp.get_width()), 1)


def photo_card(ctx, surf, x, y, s, rot=0.0, border=CREAM):
    w, h = surf.get_width() * s, surf.get_height() * s
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    rrect(ctx, -w / 2 - 16, -h / 2 - 16, w + 32, h + 32, 22); fill_stroke(ctx, border, INK, 7)
    ctx.save(); rrect(ctx, -w / 2, -h / 2, w, h, 10); ctx.clip()
    ctx.scale(s, s); ctx.set_source_surface(surf, -surf.get_width() / 2, -surf.get_height() / 2); ctx.paint(); ctx.restore()
    ctx.restore()


# ------------------------------------------------------------------ cut visuals: vis(ctx, lt, d, gt)
def v_hook(ctx, lt, d, gt):
    q = 1.0 + 0.06 * math.sin(gt * 6)
    label(ctx, "?", 840, 520 + 14 * math.sin(gt * 5), 260, color=AMB, font="dela", s=q, rot=0.15)
    label(ctx, "何才まで?", 380, 470, 120, color="#FFFFFF", font="dela", s=q, rot=-0.06)


def v_answer(ctx, lt, d, gt):
    s = pop(lt, 0.0, 0.35)
    burst(ctx, W / 2, 470, 330 + 20 * math.sin(gt * 10), gt, AMB, n=18, alpha=0.9)
    label(ctx, "131才", W / 2, 470, 250, color=CREAM, hi=AMB, font="dela", s=s * (1 + 0.04 * math.sin(gt * 9)), rot=-0.05)
    sparkles(ctx, W / 2, 470, lt, 0.1, "#FFFFFF", 14, 420)
    if lt > 1.4:
        label(ctx, "アメリカ・モンタナ州の川", W / 2, 690, 60, font="maru", s=pop(lt, 1.4))


def v_half(ctx, lt, d, gt):
    bg25(ctx, lt, gt)
    rrect(ctx, 70, 300, 940, 980, 40); ctx.set_source_rgba(*hexc(DEEP, 0.55)); ctx.fill()
    order = list(range(42)); random.Random(5).shuffle(order); old = set(order[:21])
    for i in range(42):
        r, c = divmod(i, 6)
        x = 170 + c * 148; y = 380 + r * 128
        s = pop(lt, 0.05 * (i % 12), 0.3) * 0.82
        isold = i in old
        t_on = 1.6 + 0.07 * sorted(old).index(i) if isold else 99
        on = lt > t_on
        fishicon(ctx, x, y, s, "#E9D9A6" if on else "#B4C0C4", flip=(i % 2 == 0), gt=gt)
        if on:
            label(ctx, "99+", x + 30, y - 40, 34, color=INK, hi=INK, stroke=AMB, font="dela", s=pop(lt, t_on, 0.25))
    if lt > 1.3:
        n = sum(1 for i in old if lt > 1.6 + 0.07 * sorted(old).index(i))
        label(ctx, f"99才以上 {n}ひき / 42ひき", W / 2, 1225, 60, font="dela", s=pop(lt, 1.3))


def v_photo(ctx, lt, d, gt):
    bg25(ctx, lt, gt, 0.15)
    ph = C("bsph", lambda: img(f"{DL}/bluesucker.jpg", 1000))
    # Ken Burns crop on the fish
    s = 0.96 + 0.05 * clamp(lt / d)
    photo_card(ctx, ph, W / 2 - 20 * clamp(lt / d), 640, s * pop(lt, 0, 0.3), -0.02)
    credit(ctx, "出典:Doug Canfield / USFWS(パブリックドメイン)", 640 + ph.get_height() * s / 2 + 52)
    if lt > 1.8:
        ctx.save(); ctx.translate(W / 2, 1140); ctx.rotate(-0.04); sc = pop(lt, 1.8)
        ctx.scale(sc, sc); rrect(ctx, -330, -90, 660, 180, 40); fill_stroke(ctx, AMB, INK, 8); ctx.restore()
        label(ctx, "1892年", W / 2 - 130, 1130, 84, color=INK, hi=INK, stroke=CREAM, font="dela", s=pop(lt, 1.8), rot=-0.04)
        label(ctx, "=明治25年", W / 2 + 170, 1150, 56, color=INK, hi=INK, stroke=CREAM, font="maru", s=pop(lt, 2.4), rot=-0.04)
    label(ctx, "ブルーサッカー", W / 2, 300, 84, font="dela", s=pop(lt, 0.2), rot=-0.03)


def human(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    circle(ctx, 0, -120, 40, "#FFD6B0", INK, 6)
    rrect(ctx, -45, -76, 90, 120, 30); fill_stroke(ctx, "#5DADE2", INK, 6)
    ctx.restore()


def v_compare(ctx, lt, d, gt):
    bg25(ctx, lt, gt, 0.2)
    base = 1020
    for k, (val, col, who) in enumerate([(122, "#5DADE2", "人間"), (131, AMB, "魚")]):
        x = 330 + k * 420
        g = ease_out_cubic(clamp((lt - 0.2 - 0.5 * k) / 1.0))
        h = 6.0 * val * g
        rrect(ctx, x - 110, base - h, 220, h + 1, 24); fill_stroke(ctx, col, INK, 8)
        if g > 0.05:
            label(ctx, f"{int(round(val * g))}才", x, base - h - 70, 84, font="dela", color=CREAM if k else "#FFFFFF")
        if k == 0:
            human(ctx, x, base + 150, 0.9)
        else:
            fishicon(ctx, x, base + 110, 1.2, "#E9D9A6", gt=gt)
        label(ctx, who, x, base + 250, 56, font="maru")
    if lt > 1.6:
        star(ctx, 750, base - 6 * 131 - 170, 50 * pop(lt, 1.6), AMB)


def v_how(ctx, lt, d, gt):
    bg25(ctx, lt, gt, 0.3)
    piko(ctx, W / 2, 900, gt, 2.1, "wow")
    for k, (x, y) in enumerate([(250, 520), (830, 470), (880, 760)]):
        label(ctx, "?", x, y + 12 * math.sin(gt * 4 + k), 150 - 20 * k, color=AMB, font="dela", s=pop(lt, 0.15 * k), rot=0.2 * (k - 1))


def v_xray(ctx, lt, d, gt):
    xr = C("xr", lambda: img(f"{HERE}/r3d/xray.png", W, H))
    z = 1.0 + 0.25 * ease_in_out(clamp(lt / d))
    # zoom toward the glowing stone (render centre)
    ctx.save(); ctx.translate(462, 929); ctx.scale(z, z); ctx.translate(-462, -929)
    blit(ctx, xr, W / 2, H / 2, 1.0); ctx.restore()
    if lt > 1.0:
        p = pop(lt, 1.0)
        label(ctx, "耳石(じせき)", W / 2, 330, 96, font="dela", color=CREAM, s=p)
        ctx.new_path(); ctx.arc(462, 929, 105 + 10 * math.sin(gt * 8), 0, 2 * math.pi)
        ctx.set_source_rgba(*hexc(AMB, 0.9)); ctx.set_line_width(10); ctx.stroke()
    label(ctx, "イメージ", 140, 1300, 36, font="zen", s=1)


def v_rings(ctx, lt, d, gt):
    bg25(ctx, lt, gt, 0.35)
    rg = C("rings", lambda: img(f"{DL}/rings.png", 960))
    s = 1.0 + 0.04 * clamp(lt / d)
    photo_card(ctx, rg, W / 2, 720, s * pop(lt, 0, 0.3))
    credit(ctx, "出典:Lackmann et al. 2026, Communications Biology(CC BY 4.0)", 720 + rg.get_height() * s / 2 + 52)
    # arrows pointing at the bands
    for k in range(3):
        t0 = 1.0 + 0.45 * k
        if lt > t0:
            x = 330 + 190 * k; y = 520 + 60 * k
            label(ctx, "↓", x, y - 30 + 8 * math.sin(gt * 8), 90, color=AMB, font="dela", s=pop(lt, t0))
    label(ctx, "しま1本=1年", W / 2, 360, 84, font="dela", s=pop(lt, 0.3), rot=-0.03)


def v_count(ctx, lt, d, gt):
    bg25(ctx, lt, gt, 0.35)
    o = C("oto", lambda: img(f"{DL}/oto130.png", 980))
    photo_card(ctx, o, W / 2, 700, pop(lt, 0, 0.3))
    credit(ctx, "出典:Lackmann et al. 2026, Communications Biology(CC BY 4.0)", 700 + o.get_height() / 2 + 52)
    n = int(130 * ease_out_cubic(clamp((lt - 0.4) / 2.6)))
    rrect(ctx, W / 2 - 260, 1000, 520, 170, 40); fill_stroke(ctx, AMB, INK, 8)
    label(ctx, f"{n}本", W / 2, 1085, 110, color=INK, hi=INK, stroke=CREAM, font="dela")
    label(ctx, "かぞえた!", W / 2, 360, 84, font="dela", s=pop(lt, 0.2))


def cake(ctx, x, y, s, gt):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -220, -40, 440, 200, 30); fill_stroke(ctx, "#FFE7C2", INK, 8)
    rrect(ctx, -220, -40, 440, 60, 30); fill_stroke(ctx, PINK, INK, 8)
    for k in range(5):
        cx = -160 + k * 80
        rrect(ctx, cx - 10, -130, 20, 90, 6); fill_stroke(ctx, "#7FD3E6", INK, 4)
        fl = 1 + 0.15 * math.sin(gt * 14 + k)
        ctx.save(); ctx.translate(cx, -150); ctx.scale(fl, fl)
        ctx.new_path(); ctx.move_to(0, -30); ctx.curve_to(18, -6, 12, 14, 0, 14); ctx.curve_to(-12, 14, -18, -6, 0, -30)
        fill_stroke(ctx, AMB, INK, 3); ctx.restore()
    ctx.restore()
    label(ctx, "131", x, y + 70 * s, 117, color=INK, hi=INK, stroke="#FFFFFF", font="dela", s=s / 1.3)


def v_comment(ctx, lt, d, gt):
    bg25(ctx, lt, gt, 0.3)
    cake(ctx, W / 2, 760, 1.3 * pop(lt, 0.1), gt)
    piko(ctx, 820, 1150, gt, 1.1, "smile")
    if lt > 2.2:
        label(ctx, "コメントで教えてね!", W / 2, 400, 80, font="dela", s=pop(lt, 2.2), rot=-0.04)


def v_end(ctx, lt, d, gt):
    bg25(ctx, lt, gt, 0.4)
    piko(ctx, W / 2, 900, gt, 2.0, "smile")
    label(ctx, "今日のワクワクニュース", W / 2, 420, 76, font="dela", s=pop(lt, 0.1), color=CREAM)
    for k in range(6):
        a = gt * 1.5 + k * math.pi / 3
        star(ctx, W / 2 + 330 * math.cos(a), 880 + 330 * math.sin(a), 34, [AMB, "#FFFFFF", PINK][k % 3])


VIS = [v_hook, v_answer, v_half, v_photo, v_compare, v_how, v_xray, v_rings, v_count, v_comment, v_end]
MOOD = ["wow", "wow", None, "smile", None, None, "smile", "smile", "wow", None, None]


# ------------------------------------------------------------------ chrome: top tag + caption panel
def top_tag(ctx, gt):
    rrect(ctx, 30, 40, 400, 74, 37); ctx.set_source_rgba(*hexc(DEEP, 0.85)); ctx.fill_preserve()
    ctx.set_source_rgba(*hexc(AMB)); ctx.set_line_width(4); ctx.stroke()
    label(ctx, "今日のワクワク|生き物", 230, 77, 36, font="maru", color="#FFFFFF", stroke=DEEP)


def caption(ctx, cut, lt):
    p = 1.0 if cut["i"] == 0 else ease_out_cubic(clamp(lt / 0.22))
    y = 1560 + 60 * (1 - p)
    rrect(ctx, 50, y - 150, W - 100, 300, 44); ctx.set_source_rgba(*hexc(DEEP, 0.88 * p)); ctx.fill_preserve()
    ctx.set_source_rgba(*hexc(AMB, p)); ctx.set_line_width(6); ctx.stroke()
    sp = text_sprite(cut["cap"], 84, color="#FFFFFF", hi=AMB, stroke=INK, path=FONTS["maru"])
    draw_sprite(ctx, sp, W / 2, y, min(1.0, 920 / sp.get_width()) * (0.9 + 0.1 * p), p)


def find(gt):
    for c in CUTS:
        if c["t0"] <= gt < c["t0"] + c["d"]:
            return c
    return CUTS[-1]


def frame(ctx, gt):
    c = find(gt); lt = gt - c["t0"]
    ctx.set_source_rgb(*hexc(DEEP)[:3]); ctx.paint()
    if gt < T3:
        blit(ctx, frame3d(min(gt, 8.5)), W / 2, H / 2, 1.0)
    VIS[c["i"]](ctx, lt, c["d"], gt)
    bubbles(ctx, gt, 22, front=False)
    if c["i"] >= 2:
        weeds_front(ctx, gt)
    if MOOD[c["i"]] and c["i"] not in (5,):
        piko(ctx, 930, 1270, gt, 0.75, MOOD[c["i"]])
    top_tag(ctx, gt)
    caption(ctx, c, lt)
    # quick white flash on cut change (short, not strobing)
    if lt < 0.08 and c["i"] > 0:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(1, 1, 1, 0.35 * (1 - lt / 0.08)); ctx.fill()


# ------------------------------------------------------------------ audio
def splash():
    n = int(0.8 * SR); tt = np.arange(n) / SR
    no = np.random.default_rng(3).standard_normal(n)
    lp = np.convolve(no, np.ones(30) / 30, mode="same")
    bub = sum(0.25 * np.sin(2 * np.pi * (300 + 500 * k) * tt * (1 + tt)) * np.exp(-((tt - 0.1 * k - 0.15) ** 2) / 0.002) for k in range(5))
    return 0.9 * lp * np.exp(-tt * 5) + bub


def SF(name):
    import engine3 as E3
    try:
        return E2.sfx(name)
    except KeyError:
        return E3.sfx3(name)


def build_audio(path):
    n = int(TOTAL * SR)
    voice = np.zeros(n); fx = np.zeros(n)
    def add(buf, sig, at, g=1.0):
        st = int(at * SR)
        if st >= n:
            return
        e = min(n, st + len(sig)); buf[st:e] += g * sig[: e - st]
    for c in CUTS:
        add(voice, c["audio"], c["t0"] + 0.06)
        if c["i"] > 0:
            add(fx, SF("whoosh"), c["t0"], 0.5)
    add(fx, splash(), 1.55, 1.0)
    add(fx, SF("impact"), CUTS[1]["t0"], 0.9); add(fx, SF("kira"), CUTS[1]["t0"] + 0.2, 0.7)
    for k in range(21):
        add(fx, SF("pop2"), CUTS[2]["t0"] + 1.6 + 0.07 * k, 0.25)
    add(fx, SF("ding"), CUTS[3]["t0"] + 1.8, 0.6)
    add(fx, SF("slideup"), CUTS[4]["t0"] + 0.2, 0.5); add(fx, SF("tada"), CUTS[4]["t0"] + 1.6, 0.6)
    add(fx, SF("hmm"), CUTS[5]["t0"] + 0.2, 0.6)
    add(fx, SF("kira"), CUTS[6]["t0"] + 1.0, 0.7)
    for k in range(3):
        add(fx, SF("tick"), CUTS[7]["t0"] + 1.0 + 0.45 * k, 0.6)
    for k in range(12):
        add(fx, SF("tick"), CUTS[8]["t0"] + 0.4 + 0.2 * k, 0.35)
    add(fx, SF("tada"), CUTS[8]["t0"] + 3.0, 0.6)
    add(fx, SF("kira"), CUTS[10]["t0"] + 0.1, 0.7)
    voice = voice / (np.max(np.abs(voice)) or 1) * 0.9
    envv = np.convolve(np.abs(voice) > 0.02, np.ones(int(0.15 * SR)) / int(0.15 * SR), mode="same")
    duck = 1 - 0.7 * np.clip(envv * 3, 0, 1)
    music = bgm(TOTAL, bpm=96, key=-3)[:n]
    music = music / (np.max(np.abs(music)) or 1) * 0.38 * duck
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
    name = "20261126_bluesucker_short"
    print("total", round(TOTAL, 2), "cut2 at", round(CUTS[1]["t0"], 2))
    if sys.argv[1:] and sys.argv[1] == "preview":
        ts = [float(x) for x in sys.argv[2:]] or [c["t0"] + min(1.8, c["d"] * 0.6) for c in CUTS]
        render(None, ts, f"{HERE}/preview")
    else:
        os.makedirs(f"{HERE}/out", exist_ok=True)
        if not (sys.argv[1:] and sys.argv[1] == "audio"):
            render(f"{HERE}/out/{name}_video.mp4")
        build_audio(f"{HERE}/out/{name}.wav")
        mux2(f"{HERE}/out/{name}_video.mp4", f"{HERE}/out/{name}.wav", f"{HERE}/out/{name}_final.mp4")
