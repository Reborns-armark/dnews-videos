"""Blender (bpy) scene for the blue-sucker Short: river surface -> dive -> fish -> head (otolith)."""
import bpy, math, random, sys, os
from mathutils import Vector

def mat(name, col, rough=0.5, metal=0.0, trans=0.0, emit=None, alpha=1.0, estr=4.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if trans:
        b.inputs["Transmission Weight"].default_value = trans
        b.inputs["IOR"].default_value = 1.33
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = estr
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
    return m

def hexrgb(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x ** 2.2 for x in c)

def setup():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 8
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 540, 960
    sc.cycles.max_bounces = 4; sc.cycles.transmission_bounces = 3; sc.cycles.glossy_bounces = 2
    w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (*hexrgb("#9FD8E8"), 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
    # sun
    bpy.ops.object.light_add(type='SUN', location=(4, -6, 12)); sun = bpy.context.object
    sun.data.energy = 6.5; sun.rotation_euler = (math.radians(35), math.radians(15), math.radians(20))
    sun.data.color = hexrgb("#FFF1C9")
    # water surface
    bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 0, 0)); water = bpy.context.object; water.name = "water"
    bpy.ops.object.modifier_add(type='SUBSURF'); water.modifiers[0].levels = 0
    wm = mat("water", hexrgb("#2FA39A"), rough=0.08, trans=0.75)
    nt = wm.node_tree; tex = nt.nodes.new("ShaderNodeTexNoise"); tex.inputs["Scale"].default_value = 3.0
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.25
    nt.links.new(tex.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], nt.nodes["Principled BSDF"].inputs["Normal"])
    water.data.materials.append(wm)
    # underwater tint: a big inverted box with emission-free volume is slow; use a dim 'haze' plane far behind
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 26, -2), rotation=(math.radians(90), 0, 0)); haze = bpy.context.object
    haze.data.materials.append(mat("haze", hexrgb("#3E7D5C"), rough=1, emit=hexrgb("#5FAE8E"), estr=1.0))
    haze.name = "haze"
    # riverbed + gravel
    bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 0, -4.2)); bed = bpy.context.object
    bed.data.materials.append(mat("bed", hexrgb("#8C7A4E"), rough=0.95))
    rnd = random.Random(7)
    cols = ["#B89B5E", "#7E6B45", "#C9B27A", "#5D5A47", "#A88452", "#6E7B58"]
    gm = [mat(f"g{i}", hexrgb(c), rough=0.8) for i, c in enumerate(cols)]
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1); base = bpy.context.object; base.name = "pebble"
    base.location = (0, 0, -50)
    for i in range(420):
        x = rnd.uniform(-9, 9); y = rnd.uniform(-8, 16)
        o = base.copy(); o.data = base.data.copy() if i < 6 else bpy.data.objects["pebble"].data
        bpy.context.collection.objects.link(o)
        r = rnd.uniform(0.12, 0.38)
        o.scale = (r * rnd.uniform(0.9, 1.5), r * rnd.uniform(0.9, 1.4), r * 0.6)
        o.location = (x, y, -4.2 + r * 0.2); o.rotation_euler = (0, 0, rnd.uniform(0, 6.3))
        o.active_material = None
        o.material_slots and None
        o.data.materials.clear() if i < 6 else None
        if i < 6:
            o.data.materials.append(gm[i])
        else:
            # object-level material link so shared mesh can vary colour
            o.data = bpy.data.objects["pebble"].data if False else o.data
    # assign colours via object material slots
    for i, o in enumerate([ob for ob in bpy.data.objects if ob.name.startswith("pebble.")]):
        if not o.data.materials:
            o.data.materials.append(gm[0])
        o.material_slots[0].link = 'OBJECT'; o.material_slots[0].material = gm[i % len(gm)]
    # weeds
    wmat = mat("weed", hexrgb("#4F7F3A"), rough=0.7)
    for i in range(28):
        bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.08, depth=rnd.uniform(1.0, 2.4),
                                        location=(rnd.choice([-1, 1]) * rnd.uniform(2.5, 8), rnd.uniform(-4, 14), -3.4))
        o = bpy.context.object; o.rotation_euler = (rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3), 0); o.data.materials.append(wmat)
    build_fish()

def build_fish():
    body_m = mat("fishbody", hexrgb("#B4C0C4"), rough=0.35, metal=0.2)
    belly = mat("belly", hexrgb("#C9CFC6"), rough=0.4)
    fin_m = mat("fin", hexrgb("#6F8C9E"), rough=0.4)
    eye_m = mat("eye", hexrgb("#111111"), rough=0.1)
    oto_m = mat("oto", hexrgb("#FFD24A"), rough=0.3, emit=hexrgb("#FFC21A"), estr=0.0)
    bpy.ops.object.empty_add(location=(0, 4, -3.0)); root = bpy.context.object; root.name = "fish"
    def part(op, name, loc, scale, m, rot=(0, 0, 0), **kw):
        op(location=loc, **kw); o = bpy.context.object; o.name = name; o.scale = scale; o.rotation_euler = rot
        o.data.materials.append(m); o.parent = root
        bpy.ops.object.shade_smooth()
        return o
    part(bpy.ops.mesh.primitive_uv_sphere_add, "body", (0, 0, 0), (2.3, 0.42, 0.55), body_m, segments=48, ring_count=24)
    part(bpy.ops.mesh.primitive_uv_sphere_add, "belly", (0.1, 0, -0.18), (2.0, 0.36, 0.38), belly, segments=32, ring_count=16)
    part(bpy.ops.mesh.primitive_uv_sphere_add, "head", (-1.9, 0, -0.05), (0.75, 0.36, 0.42), body_m, segments=32, ring_count=16)
    part(bpy.ops.mesh.primitive_uv_sphere_add, "snout", (-2.55, 0, -0.2), (0.25, 0.2, 0.2), belly, segments=24, ring_count=12)
    for s in (1, -1):
        part(bpy.ops.mesh.primitive_uv_sphere_add, f"eye{s}", (-2.2, 0.27 * s, 0.08), (0.07, 0.07, 0.07), eye_m)
        part(bpy.ops.mesh.primitive_cone_add, f"pec{s}", (-1.2, 0.38 * s, -0.4), (0.12, 0.45, 0.03), fin_m,
             rot=(math.radians(20 * s), 0, math.radians(30 * s)), vertices=12)
    tail = part(bpy.ops.mesh.primitive_cone_add, "tail", (2.75, 0, 0), (0.06, 0.7, 0.9), fin_m, rot=(0, math.radians(90), 0), vertices=3)
    tail.rotation_euler = (math.radians(90), math.radians(90), 0)
    part(bpy.ops.mesh.primitive_cone_add, "dorsal", (-0.5, 0, 0.75), (0.7, 0.04, 0.55), fin_m, rot=(0, math.radians(-25), 0), vertices=3)
    oto = part(bpy.ops.mesh.primitive_uv_sphere_add, "oto", (-1.85, 0.0, 0.05), (0.16, 0.09, 0.07), oto_m)
    oto.hide_render = True

def look(cam, target):
    d = Vector(target) - cam.location
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

def lerp(a, b, t): return tuple(x + (y - x) * t for x, y in zip(a, b))
def ease(t): t = max(0, min(1, t)); return t * t * (3 - 2 * t)

def pose(t, T1, T):
    """Camera + fish pose at time t. T1 = end of cut 1 (dive done), T = total 3D time."""
    fish = bpy.data.objects["fish"]
    fish.location = (0.0 - 0.25 * t, 4.0 - 0.0 * t, -3.0 + 0.05 * math.sin(t * 2))
    fish.rotation_euler = (0, 0, math.radians(90) + 0.06 * math.sin(t * 4))  # head points -y (toward camera)
    bpy.data.objects["tail"].rotation_euler = (math.radians(90), math.radians(90), 0.35 * math.sin(t * 6))
    cam = bpy.data.objects["Camera"]
    fx, fy, fz = fish.location
    head = (fx, fy - 2.0, fz)
    if t < T1:
        u = ease(t / T1)
        p = lerp((1.5, -16, 9), (2.6, -6.5, -2.4), u)
        tgt = lerp((0, 2, -2.5), (fx, fy - 0.5, fz - 0.3), u)
    else:
        u = ease((t - T1) / max(0.1, T - T1))
        p = lerp((2.6, -6.5, -2.4), (1.5, fy - 4.6, fz + 0.35), u)
        tgt = lerp((fx, fy - 0.5, fz - 0.3), (head[0], head[1], head[2] - 0.15), u)
    cam.location = p; look(cam, tgt)
    cam.data.lens = 26 + 6 * (ease((t - T1) / max(0.1, T - T1)) if t > T1 else 0)

if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    mode = argv[0]
    setup()
    bpy.ops.object.camera_add(); cam = bpy.context.object; cam.name = "Camera"; bpy.context.scene.camera = cam
    sc = bpy.context.scene
    if mode == "anim":
        T1, T, f0, f1, out = float(argv[1]), float(argv[2]), int(argv[3]), int(argv[4]), argv[5]
        os.makedirs(out, exist_ok=True)
        for f in range(f0, f1):
            fp = f"{out}/f{f:04d}.png"
            if os.path.exists(fp):
                continue
            pose(f / 30, T1, T)
            sc.render.filepath = fp
            bpy.ops.render.render(write_still=True)
    elif mode == "xray":
        out = argv[1]
        pose(6.0, 3.0, 6.0)
        for n in ("body", "head", "belly", "snout"):
            o = bpy.data.objects[n]; o.material_slots[0].link = 'OBJECT'
            o.material_slots[0].material = mat("xr" + n, hexrgb("#7FD3E6"), rough=0.2, alpha=0.25)
        o = bpy.data.objects["oto"]; o.hide_render = False
        o.active_material.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 12
        cam = bpy.data.objects["Camera"]; f = bpy.data.objects["fish"]
        cam.location = (f.location[0] + 1.2, f.location[1] - 3.6, f.location[2] + 0.5); look(cam, (f.location[0], f.location[1] - 1.85, f.location[2] + 0.05))
        cam.data.lens = 40
        sc.cycles.samples = 24
        sc.render.filepath = out; bpy.ops.render.render(write_still=True)
    elif mode == "bg":
        out = argv[1]
        bpy.data.objects["fish"].location = (0, 60, -3)
        for c in bpy.data.objects["fish"].children: c.hide_render = True
        cam = bpy.data.objects["Camera"]; cam.location = (0, -6, -2.6); look(cam, (0, 6, -3.6)); cam.data.lens = 22
        sc.cycles.samples = 24
        sc.render.filepath = out; bpy.ops.render.render(write_still=True)

if __name__ == "__main__" and mode == "frames":
    T1, T, out = float(argv[1]), float(argv[2]), argv[3]
    os.makedirs(out, exist_ok=True)
    for f in map(int, argv[4:]):
        pose(f / 30, T1, T); sc.render.filepath = f"{out}/f{f:04d}.png"; bpy.ops.render.render(write_still=True)
