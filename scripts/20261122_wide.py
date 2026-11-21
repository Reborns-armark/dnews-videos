import os, math, subprocess
import cairo
from common4 import *
import engine2 as E2, engine3 as E3, engine4 as E4
WW, HH = 1920, 1080

# ---------------------------------------------------------------- widescreen frame
def _patch(w, h):
    for m in (E2, E3, E4):
        m.W, m.H = w, h


def chapter_at(tl, idx):
    name = "オープニング"
    for e in tl["cuts"][: idx + 1]:
        name = e["cut"].kw.get("chapter", name)
    return name


def make_wide(tl, genre="宇宙", gcol="#7B5CFF"):
    cuts = tl["cuts"]; total = tl["total"]
    pts = [e for e in cuts if e["point"]]
    P = max(1, len(pts))
    stage = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920)

    def frame(ctx, gt):
        e = cuts[-1]
        for c in cuts:
            if c["t0"] <= gt < c["t0"] + c["d"]:
                e = c; break
        lt = gt - e["t0"]
        nb = sum(1 for b in e["beats"] if b <= lt)
        pal = e["pal"]
        if nb:
            pal = E3.EXTRA_PATS[(e["i"] + nb) % len(E3.EXTRA_PATS)] if nb % 2 else E2.PALETTES[(e["i"] * 2 + nb) % len(E2.PALETTES)]
            if e["dream"]:
                pal = E3.DREAM_PALS[(e["i"] + nb) % len(E3.DREAM_PALS)]
        _patch(WW, HH)
        try:
            hi = E3.draw_bg3(ctx, pal, lt, gt)
        finally:
            _patch(1080, 1920)
        # --- stage: the vertical scene, drawn on a transparent layer, placed on the left
        sc = cairo.Context(stage)
        sc.set_operator(cairo.OPERATOR_CLEAR); sc.paint(); sc.set_operator(cairo.OPERATOR_OVER)
        sc.save(); E2.camera(sc, e, lt); e["cut"].vis(sc, lt, e["d"], gt)
        for (ex, ey, er) in e["cut"].kw.get("eyes", []):
            E3.googly(sc, ex, ey, er, gt, e["i"])
        sc.restore()
        E3.word_sticker(sc, e, lt)
        stage.flush()
        S = 0.78
        wob = 0.02 * math.sin(gt * 5.3)
        ctx.save(); ctx.translate(560, 625); ctx.rotate(wob); ctx.scale(S, S); ctx.translate(-540, -760)
        ctx.set_source_surface(stage, 0, 0); ctx.paint(); ctx.restore()
        # --- right panel: chapter + caption
        chap = chapter_at(tl, e["i"])
        rrect(ctx, 1110, 170, 760, 96, 48); fill_stroke(ctx, "#FFFFFF", lw=6)
        cs = text_sprite(chap, 44, color="#1B1B3A", hi="#FF3D7F", stroke="#FFFFFF", stroke_w=3, shadow=False, path=FONTS["mochiy"])
        draw_sprite(ctx, cs, 1490, 218, min(1.0, 700 / max(1, cs.get_width())), 1)
        cap = e["cut"].cap
        if cap:
            size = 88
            spr = text_sprite(cap, size, color="#FFFFFF", hi=hi, stroke="#1B1B3A", stroke_w=12, path=FONTS[e["font"]])
            fit = min(1.0, 740 / max(1, spr.get_width()), 420 / max(1, spr.get_height()))
            p = clamp((lt - 0.04) / 0.28) if e["i"] else 1.0
            s = fit * (ease_out_back(p, 2.4) if p < 1 else 1.0)
            for b in e["beats"]:
                if b <= lt < b + 0.2:
                    s *= 1 + 0.06 * (1 - (lt - b) / 0.2)
            draw_sprite(ctx, spr, 1490, 560, max(s, 1e-3), clamp(p * 3), -0.02 if e["i"] % 2 else 0.02)
        # chapter splash on the first second of a chapter
        if e["cut"].kw.get("chapter") and e["i"] > 0 and lt < 1.4:
            q = clamp(lt / 0.25); a = clamp((1.4 - lt) / 0.3)
            rrect(ctx, 140, 510, 840, 200, 40); ctx.set_source_rgba(0.1, 0.1, 0.23, 0.85 * a); ctx.fill()
            draw_sprite(ctx, text_sprite(chap, 76, color="#FFE14D", hi="#FF3D7F", path=FONTS["dela"]), 560, 610, ease_out_back(q, 2.2), a)
        # --- mascot (bottom right), talking bounce
        bounce = abs(math.sin(gt * 7)) * 18
        mood = "wow" if (nb % 2 or e["cut"].kw.get("mood") == "wow") else "smile"
        piko(ctx, 1780, 930 - bounce, gt, 0.55, mood, look=-0.6)
        # --- header
        card(ctx, 40, 24, 1840, 104, "#FFFFFF", 0.97, 52)
        draw_sprite(ctx, text_sprite("今日の{ワクワク}ニュース 特別編", 52, color="#1B1B3A", hi="#FF3D7F", stroke="#FFFFFF",
                                     stroke_w=3, shadow=False, path=FONTS["mochiy"]), 460, 76)
        rrect(ctx, 1620, 44, 236, 64, 32); fill_stroke(ctx, gcol, lw=6)
        draw_sprite(ctx, text_sprite(genre, 38, color="#FFFFFF", stroke="#1B1B3A", stroke_w=5, shadow=False, path=FONTS["mochiy"]), 1738, 76)
        # progress (whole video) + chapter ticks
        rrect(ctx, 40, 140, 1840, 14, 7); ctx.set_source_rgba(0, 0, 0, 0.3); ctx.fill()
        pr = clamp(gt / total)
        if pr > 0.005:
            rrect(ctx, 40, 140, 1840 * pr, 14, 7); ctx.set_source_rgba(*hexc("#FFE14D")); ctx.fill()
        for c in cuts:
            if c["cut"].kw.get("chapter") and c["i"] > 0:
                x = 40 + 1840 * c["t0"] / total
                circle(ctx, x, 147, 11, "#FFFFFF", lw=4)
        # --- wakuwaku meter (right panel, bottom)
        got = sum(1 for x in pts if gt >= x["t0"] + 0.85)
        rrect(ctx, 1130, 900, 520, 30, 15); ctx.set_source_rgba(0, 0, 0, 0.35); ctx.fill()
        if got:
            g = cairo.LinearGradient(1130, 0, 1650, 0)
            for k, c in enumerate(["#4FF0FF", "#FFE14D", "#FF3D7F"]):
                g.add_color_stop_rgb(k / 2, *hexc(c)[:3])
            rrect(ctx, 1130, 900, max(30, 520 * got / P), 30, 15); ctx.set_source(g); ctx.fill()
        rrect(ctx, 1130, 900, 520, 30, 15); ctx.set_source_rgba(*hexc("#1B1B3A")); ctx.set_line_width(4); ctx.stroke()
        lab = "ワクワク度 MAX!" if got == P else f"ワクワク度 {got}/{P}"
        draw_sprite(ctx, text_sprite(lab, 36, color="#FFFFFF", hi="#FFE14D", stroke="#1B1B3A", stroke_w=5, path=FONTS["dela"]), 1390, 960, 1, 1)
        for x in pts:
            l2 = gt - x["t0"]
            if 0.35 <= l2 < 0.85:
                q = ease_in_out((l2 - 0.35) / 0.5)
                tx = 1130 + 520 * (x["pidx"] / P)
                cx_, cy_ = 560 + (tx - 560) * q, 650 + (915 - 650) * q - math.sin(q * math.pi) * 200
                circle(ctx, cx_, cy_, 34 * (1 - 0.4 * q), "#FFD23F", lw=6)
                draw_sprite(ctx, text_sprite("+1", 52, color="#FFE14D", path=FONTS["dela"]), cx_ + 56, cy_ - 40, 1, 1 - q * 0.5)
        # transition flash
        if lt < 0.12 and e["i"]:
            ctx.rectangle(0, 0, WW, HH); ctx.set_source_rgba(1, 1, 1, 0.5 * (1 - lt / 0.12)); ctx.fill()

    return frame


def render_wide(path, tl, frame, preview_times=None, preview_dir=None, vbit="1250k"):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, WW, HH)
    def draw(t):
        ctx = cairo.Context(surf); frame(ctx, t); surf.flush()
    if preview_times:
        os.makedirs(preview_dir, exist_ok=True)
        for pt in preview_times:
            draw(pt); surf.write_to_png(os.path.join(preview_dir, f"t{pt:06.2f}.png"))
        return
    tmp = path[:-4] + ".tmp.mp4"
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{WW}x{HH}",
                             "-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-b:v", vbit,
                             "-maxrate", "1800k", "-bufsize", "3600k", "-g", "60", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    n = int(round(tl["total"] * 30))
    for i in range(n):
        draw(i / 30)
        proc.stdin.write(bytes(surf.get_data()))
        if i % 1800 == 0:
            print(f"frame {i}/{n}", flush=True)
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg failed")
    os.replace(tmp, path)


