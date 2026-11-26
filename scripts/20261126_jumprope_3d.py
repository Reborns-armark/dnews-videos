"""Blender scene for the jump-rope Short (format 2: 3D size comparison).
A gym floor with 8 columns in a row; column k = k glowing rope loops stacked (1重〜8重).
Camera flows along the row from 1 to 8 (cut 1), then rises to show the tall 8-loop column (cut 2)."""
import bpy, math, sys, os
from mathutils import Vector

def hexrgb(h):
    h = h.lstrip('#'); return tuple((int(h[i:i+2], 16) / 255) ** 2.2 for i in (0, 2, 4))

def mat(name, col, rough=0.5, metal=0.0, emit=None, estr=3.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = estr
    return m

SP = 3.2  # spacing between columns
COLS = ["#FFB703", "#FB8500", "#FF006E", "#8338EC", "#3A86FF", "#06D6A0", "#FFD166", "#FF4D6D"]

def setup():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 8; sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 540, 960
    sc.cycles.max_bounces = 3
    sc.view_settings.view_transform = 'Standard'
    w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (*hexrgb("#1B2A52"), 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.6
    bpy.ops.object.light_add(type='SUN', location=(0, -10, 20)); s = bpy.context.object
    s.data.energy = 4.0; s.rotation_euler = (math.radians(40), 0, math.radians(-25)); s.data.color = hexrgb("#FFF4E0")
    bpy.ops.object.light_add(type='AREA', location=(12, -8, 14)); a = bpy.context.object; a.data.energy = 3000; a.data.size = 10
    a.rotation_euler = (math.radians(50), 0, math.radians(40))
    # gym floor (wood) with court lines
    bpy.ops.mesh.primitive_plane_add(size=120, location=(12, 10, 0)); fl = bpy.context.object
    fm = mat("floor", hexrgb("#D9A066"), rough=0.35)
    nt = fm.node_tree; wave = nt.nodes.new("ShaderNodeTexWave"); wave.inputs["Scale"].default_value = 1.2
    wave.inputs["Distortion"].default_value = 3
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*hexrgb("#C98B4E"), 1); ramp.color_ramp.elements[1].color = (*hexrgb("#E6B57A"), 1)
    nt.links.new(wave.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    fl.data.materials.append(fm)
    lm = mat("line", hexrgb("#FFFFFF"), rough=0.4)
    for y in (-2.2, 2.2):
        bpy.ops.mesh.primitive_cube_add(location=(12, y, 0.01)); o = bpy.context.object; o.scale = (40, 0.06, 0.01); o.data.materials.append(lm)
    # back wall (navy) with stripe
    bpy.ops.mesh.primitive_plane_add(size=120, location=(12, 18, 0), rotation=(math.radians(90), 0, 0)); wl = bpy.context.object
    wl.data.materials.append(mat("wall", hexrgb("#14213D"), rough=0.8))
    bpy.ops.mesh.primitive_cube_add(location=(12, 17.9, 3.0)); o = bpy.context.object; o.scale = (60, 0.05, 0.4)
    o.data.materials.append(mat("stripe", hexrgb("#FF7A00"), rough=0.5, emit=hexrgb("#FF7A00"), estr=1.5))
    pm = mat("ped", hexrgb("#F1F5F9"), rough=0.3)
    for k in range(1, 9):
        x = (k - 1) * SP
        bpy.ops.mesh.primitive_cylinder_add(radius=1.3, depth=0.3, location=(x, 0, 0.15)); p = bpy.context.object
        p.data.materials.append(pm); bpy.ops.object.shade_smooth()
        rm = mat(f"rope{k}", hexrgb(COLS[k - 1]), rough=0.3, emit=hexrgb(COLS[k - 1]), estr=2.5)
        for j in range(k):
            bpy.ops.mesh.primitive_torus_add(major_radius=0.85, minor_radius=0.09, location=(x, 0, 0.6 + j * 0.62),
                                             rotation=(math.radians(90), 0, math.radians(8 * j)))
            t = bpy.context.object; t.name = f"loop{k}_{j}"; t.data.materials.append(rm); bpy.ops.object.shade_smooth()
        bpy.ops.object.text_add(location=(x, -1.75, 0.02), rotation=(math.radians(60), 0, 0)); tx = bpy.context.object
        tx.data.body = str(k); tx.data.size = 0.9; tx.data.align_x = 'CENTER'; tx.data.extrude = 0.06
        tx.data.materials.append(mat(f"num{k}", hexrgb("#14213D"), rough=0.4))

def look(cam, target):
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat('-Z', 'Y').to_euler()
def lerp(a, b, t): return tuple(x + (y - x) * t for x, y in zip(a, b))
def ease(t): t = max(0, min(1, t)); return t * t * (3 - 2 * t)

def spin(t):
    # loops rotate (rope turning) - faster for more loops
    for k in range(1, 9):
        for j in range(k):
            o = bpy.data.objects[f"loop{k}_{j}"]
            o.rotation_euler = (math.radians(90), 0, math.radians(8 * j) + t * (0.8 + 0.35 * k))

def pose(t, T1, T):
    cam = bpy.data.objects["Camera"]; spin(t)
    if t < T1:
        u = ease(t / T1)
        x = lerp((-1.0,), (6.6 * SP / 1.0 * 1.0,), u)[0]
        cam.location = (x - 4.0, -9.0, 3.4 - 0.4 * u); look(cam, (x + 3.0, 0, 1.4 + 1.2 * u)); cam.data.lens = 24
    else:
        u = ease((t - T1) / max(0.1, T - T1))
        x8 = 7 * SP
        p0 = (6.6 * SP - 4.0, -9.0, 3.0); p1 = (x8 - 2.0, -6.2, 3.2)
        cam.location = lerp(p0, p1, u); look(cam, lerp((6.6 * SP + 3.0, 0, 2.6), (x8, 0, 2.8), u)); cam.data.lens = 24 + 2 * u

if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:]
    mode = argv[0]; setup()
    bpy.ops.object.camera_add(); cam = bpy.context.object; cam.name = "Camera"; bpy.context.scene.camera = cam
    sc = bpy.context.scene
    if mode == "anim":
        T1, T, out = float(argv[1]), float(argv[2]), argv[3]
        os.makedirs(out, exist_ok=True)
        for f in map(int, argv[4:]):
            fp = f"{out}/f{f:04d}.png"
            if os.path.exists(fp): continue
            pose(f / 30, T1, T); sc.render.filepath = fp; bpy.ops.render.render(write_still=True)
    elif mode == "bg":
        out = argv[1]; spin(1.0)
        cam.location = (3.5 * SP, -17, 4.5); look(cam, (3.5 * SP, 0, 2.0)); cam.data.lens = 22
        sc.cycles.samples = 24; sc.render.filepath = out; bpy.ops.render.render(write_still=True)
    elif mode == "bg2":
        out = argv[1]
        for o in bpy.data.objects:
            if o.name.startswith(("loop", "Text")) or o.type == 'FONT': o.hide_render = True
        cam.location = (3.5 * SP, -9, 3.0); look(cam, (3.5 * SP, 6, 2.0)); cam.data.lens = 22
        sc.cycles.samples = 24; sc.render.filepath = out; bpy.ops.render.render(write_still=True)
