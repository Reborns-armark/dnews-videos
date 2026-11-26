import bpy, math, random, os
random.seed(7)
R=math.radians
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene
s.render.engine='CYCLES'; s.cycles.samples=20; s.cycles.device='CPU'; s.cycles.use_denoising=True

s.render.resolution_x=1080; s.render.resolution_y=1920
s.render.fps=12; s.frame_start=1; s.frame_end=120
def mat(name,col,rough=0.55):
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; b=nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value=col; b.inputs["Roughness"].default_value=rough
    w=nt.nodes.new("ShaderNodeTexWave"); w.inputs["Scale"].default_value=14; w.inputs["Distortion"].default_value=9
    n=nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value=40
    mx=nt.nodes.new("ShaderNodeMath"); mx.operation='ADD'
    nt.links.new(w.outputs["Fac"],mx.inputs[0]); nt.links.new(n.outputs["Fac"],mx.inputs[1])
    bp=nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value=0.5; bp.inputs["Distance"].default_value=0.02
    nt.links.new(mx.outputs[0],bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"],b.inputs["Normal"])
    return m
boils=[]
def clayify(o,st=0.06,sc=0.5,lv=3):
    o.modifiers.new("s0",'SUBSURF').levels=lv
    tex=bpy.data.textures.new(o.name+"t",'CLOUDS'); tex.noise_scale=sc
    d=o.modifiers.new("d",'DISPLACE'); d.texture=tex; d.strength=st; boils.append(d)
    bpy.ops.object.shade_smooth()
def sphere(name,r,loc,col):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r,location=loc,segments=24,ring_count=12); o=bpy.context.object; o.name=name
    o.data.materials.append(mat(name+"m",col)); clayify(o); return o
def crate(name,loc):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.name=name
    bv=o.modifiers.new("bv",'BEVEL'); bv.width=0.14; bv.segments=3
    o.data.materials.append(mat(name+"m",(0.95,0.45,0.06,1),0.6)); clayify(o,0.03,0.6,2); return o
def K(o,f,loc=None,sc=None,rot=None):
    if loc is not None: o.location=loc; o.keyframe_insert("location",frame=f)
    if sc is not None: o.scale=sc; o.keyframe_insert("scale",frame=f)
    if rot is not None: o.rotation_euler=rot; o.keyframe_insert("rotation_euler",frame=f)
# set
bpy.ops.mesh.primitive_plane_add(size=60,location=(0,0,-0.05)); fl=bpy.context.object; fl.data.materials.append(mat("floor",(0.45,0.75,0.3,1),0.85))
bpy.ops.mesh.primitive_plane_add(size=60,location=(0,16,15),rotation=(R(90),0,0)); bk=bpy.context.object; bk.data.materials.append(mat("back",(0.75,0.92,1.0,1),0.9))
# water: grid rising
bpy.ops.mesh.primitive_grid_add(x_subdivisions=40,y_subdivisions=40,size=60,location=(0,0,-0.65)); wt=bpy.context.object; wt.name="water"
wm=mat("watm",(0.04,0.35,0.95,1),0.12)
try: wm.node_tree.nodes["Principled BSDF"].inputs["Transmission Weight"].default_value=0.5
except: pass
wt.data.materials.append(wm); clayify(wt,0.12,1.2,1)
def wz(f): return -0.65+min(f-1,104)*0.031
for f in range(1,121,3): K(wt,f,(0,0,wz(f)))
# blob
body=sphere("body",1,(0,0,1),(1.0,0.32,0.05,1)); body.modifiers["d"].strength=0.05
eyes=[]; pupils=[]
for x in (-0.36,0.36):
    e=sphere("eye",0.24,(x,-0.82,1.35),(0.98,0.97,0.94,1)); e.modifiers["d"].strength=0.02
    p=sphere("pupil",0.11,(x,-1.03,1.33),(0.02,0.02,0.03,1)); p.modifiers["d"].strength=0.01
    for o in (e,p): o.parent=body; o.matrix_parent_inverse=body.matrix_world.inverted()
    eyes.append(e); pupils.append(p)

# --- face: mouth + brows
mo=sphere("mouth",0.3,(0,-0.93,0.68),(0.25,0.02,0.03,1)); mo.modifiers["d"].strength=0.01
mo.parent=body; mo.matrix_parent_inverse=body.matrix_world.inverted()
brows=[]
for sx in (-1,1):
    b_=sphere("brow",0.2,(sx*0.36,-0.78,1.74),(0.25,0.12,0.04,1)); b_.modifiers["d"].strength=0.01
    b_.parent=body; b_.matrix_parent_inverse=body.matrix_world.inverted(); brows.append(b_)
def E(f,eye=(1,1,1),pup=(1,1,1),look=(0,0),mouth=(1,0.3,0.25),raise_=0.0,tilt=0.0):
    for e in eyes: K(e,f,sc=eye)
    for i,p in enumerate(pupils):
        x=(-0.36,0.36)[i]; K(p,f,(x+look[0],-1.03,1.33+look[1]),pup)
    K(mo,f,sc=mouth)
    for i,b_ in enumerate(brows):
        sx=(-1,1)[i]; K(b_,f,(sx*0.36,-0.78,1.74+raise_*0.35),(0.9,0.3,0.3),(0,0,R(sx*tilt)))
# crates (tower under blob)
fis=[40,48,56,64]; cr=[]
for i,fi in enumerate(fis):
    c=crate("crate%d"%i,(0,0,0.5+i)); cr.append(c)
    K(c,1,sc=(0.001,0.001,0.001)); K(c,fi-2,sc=(0.001,0.001,0.001)); K(c,fi-1,sc=(1.25,1.25,0.6)); K(c,fi+1,sc=(0.92,0.92,1.1)); K(c,fi+3,sc=(1,1,1))
# S1 sleep
for f in range(1,22,3):
    b=1+0.06*math.sin(f*0.7); K(body,f,(0,0,1),(1.05*b,1.05*b,0.92/b),(0,0,R(-8)))
# S2 wake (water touches): eyes pop, body jolts
K(body,24,(0,0,1.35),(0.8,0.8,1.35),(0,0,R(-8))); K(body,27,(0,0,1),(1.15,1.15,0.85),(0,0,R(-8))); K(body,32,(0,0,1),(1,1,1),(0,0,0))
# S3 hops onto each new crate
L=1
for fi in fis:
    K(body,fi-4,(0,0,L),(1.25,1.25,0.7)); K(body,fi-1,(0,0,L+1.7),(0.82,0.82,1.35)); K(body,fi+1,(0,0,L+1.05),(1.25,1.25,0.7)); K(body,fi+3,(0,0,L+1),(1,1,1))
    L+=1
# S4 panic wiggle on top then proud
for f,a in [(68,-5),(71,-35),(74,-5),(77,-35),(80,-5),(84,-30),(90,0),(100,-20),(110,10),(120,0)]: K(body,f,(0,0,L),(1,1,1),(0,0,R(a)))

# --- expression timeline (sleep -> shock -> worry -> determined hops -> shivering -> relief -> smug)
SL=(1,1,0.08)
for f in (1,12,22): E(f,eye=SL,pup=(1,1,1),mouth=(0.9,0.3,0.12),raise_=-0.05)
E(23,eye=SL,mouth=(0.9,0.3,0.12))
E(24,eye=(1.55,1.55,1.55),pup=(0.45,0.45,0.45),mouth=(0.7,0.5,1.0),raise_=0.3,tilt=-8)   # gasp O
E(27,eye=(1.45,1.45,1.45),pup=(0.4,0.4,0.4),look=(0,-0.08),mouth=(0.75,0.5,1.1),raise_=0.32,tilt=-10)
E(31,eye=(1.15,1.15,1.15),pup=(0.6,0.6,0.6),look=(0,-0.12),mouth=(1.2,0.3,0.45),raise_=0.15,tilt=-18)  # worry
E(36,eye=(1.1,1.1,1.1),pup=(0.7,0.7,0.7),look=(0.08,-0.1),mouth=(1.0,0.3,0.4),raise_=0.1,tilt=-20)
for i,fi in enumerate(fis):
    E(fi-4,eye=(1,1,0.8),pup=(0.9,0.9,0.9),look=(0,0.05),mouth=(1.3,0.3,0.4),raise_=-0.05,tilt=14)    # determined, brows angry
    E(fi-1,eye=(1.15,1.15,1.15),pup=(0.8,0.8,0.8),look=(0,0.12),mouth=(1.0,0.4,1.3),raise_=0.0,tilt=18)  # shout while jumping
    E(fi+2,eye=(1,1,0.55),pup=(0.9,0.9,0.9),look=(0,-0.05),mouth=(1.4,0.3,0.3),raise_=-0.08,tilt=12)    # grunt on landing
for k,f in enumerate(range(68,92,2)):   # shivering: teeth chatter
    E(f,eye=(1.35,1.35,1.35),pup=(0.45,0.45,0.45),look=(0.05*(-1)**k,-0.1),mouth=(1.5 if k%2 else 0.9,0.3,0.5 if k%2 else 0.18),raise_=0.2,tilt=-22)
E(94,eye=(1.2,1.2,1.2),pup=(0.6,0.6,0.6),look=(0,0.1),mouth=(1.1,0.3,0.6),raise_=0.15,tilt=-12)   # sees water stop
E(100,eye=(1.05,1.05,1.05),pup=(0.9,0.9,0.9),look=(0,0.12),mouth=(1.5,0.3,0.28),raise_=0.15,tilt=0)  # relief smile
E(108,eye=(1,1,0.6),pup=(1,1,1),look=(0,0),mouth=(1.9,0.3,0.14),raise_=0.12,tilt=10)  # smug grin
E(120,eye=(1,1,0.5),pup=(1,1,1),look=(0.05,0),mouth=(1.9,0.3,0.14),raise_=0.12,tilt=10)
for f in range(1,121):
    for d in boils: d.mid_level=0.5+random.uniform(-0.025,0.025); d.keyframe_insert("mid_level",frame=f)
def area(loc,rot,e,size,col=(1,1,1)):
    bpy.ops.object.light_add(type='AREA',location=loc,rotation=rot); l=bpy.context.object; l.data.energy=e; l.data.size=size; l.data.color=col
area((-5,-8,9),(R(45),0,R(-30)),1800,6,(1,0.93,0.82)); area((7,4,5),(R(-60),R(40),0),700,3,(0.7,0.85,1)); area((0,-10,2),(R(85),0,0),250,8)
world=bpy.data.worlds.new("w"); s.world=world; world.color=(0.6,0.7,0.85)
def cam(name,f,loc,rot,lens,moves=(),fs=2.8):
    bpy.ops.object.camera_add(location=loc,rotation=tuple(R(a) for a in rot)); c=bpy.context.object; c.name=name; c.data.lens=lens
    c.data.dof.use_dof=True; c.data.dof.focus_object=body; c.data.dof.aperture_fstop=fs
    c.keyframe_insert("location",frame=f); c.keyframe_insert("rotation_euler",frame=f)
    for mf,ml,mr in moves:
        c.location=ml; c.rotation_euler=tuple(R(a) for a in mr); c.keyframe_insert("location",frame=mf); c.keyframe_insert("rotation_euler",frame=mf)
    s.timeline_markers.new(name,frame=f).camera=c; return c
cam("S1_wide",1,(2,-12,2.6),(80,0,0),32,[(21,(0.6,-10,2.0),(80,0,0))])
cam("S2_ecu",22,(0,-4.4,1.4),(90,0,0),55,[(32,(0,-3.4,1.4),(90,0,0))],1.8)
cam("S3_low_up",33,(3.0,-7,1.0),(90,0,22),24,[(70,(3.0,-8,3.5),(86,0,18))],4.0)
cam("S4_high_down",71,(1.5,-3.5,11),(22,0,8),30,[(100,(0.5,-4.5,8.5),(26,0,4))],5.6)
cam("S5_pullback",101,(0,-8,5.5),(75,0,0),28,[(120,(0,-18,7.5),(76,0,0))],5.6)
A=int(os.environ.get('F_START','1')); B=int(os.environ.get('F_END','120'))
outdir=os.environ.get('OUT_DIR','/tmp/out'); os.makedirs(outdir,exist_ok=True)
s.render.image_settings.file_format='PNG'
for f in range(A,B+1):
    s.frame_set(f); s.render.filepath=os.path.join(outdir,'f_%04d.png'%f); bpy.ops.render.render(write_still=True)
