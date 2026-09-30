"""Hazel as a vinyl-toy 3D render (Blender as a Python module). Usage: python3 hazel3d.py <out.png> <size> <samples> [variant]"""
import bpy, sys, math, time
from mathutils import Vector, Euler

OUT, SIZE, SAMPLES = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
VARIANT = sys.argv[4] if len(sys.argv) > 4 else "night"
EXPR = sys.argv[5] if len(sys.argv) > 5 else "neutral"
POSE = sys.argv[6] if len(sys.argv) > 6 else "coin"
TRANSPARENT = VARIANT.startswith("clear")
SCR = "/tmp/claude-0/-home-claude/ff4f78c9-8964-5602-980c-e8f6bc4eb1a6/scratchpad"

def hexc(h, g=1.0):
    h = h.lstrip("#"); r, gg, b = (int(h[i:i+2], 16)/255 for i in (0, 2, 4))
    srgb = lambda c: ((c+0.055)/1.055)**2.4 if c > 0.04045 else c/12.92
    return (srgb(r)*g, srgb(gg)*g, srgb(b)*g, 1.0)

NAVY, RUST, TAIL, TAIL_L, CREAM, INK, BRASS, BRASS_D = "#132440", "#B4552A", "#8E3F1F", "#D57F4A", "#F1EADC", "#0F1F33", "#C9A45E", "#B5762F"

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.render.resolution_x = sc.render.resolution_y = SIZE
sc.render.film_transparent = TRANSPARENT
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"; sc.view_settings.exposure = -0.35

def mat(name, color, rough=0.45, metal=0.0, sss=0.0, spec=0.5):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = hexc(color)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if sss:
        b.inputs["Subsurface Weight"].default_value = sss
        b.inputs["Subsurface Radius"].default_value = (0.3, 0.15, 0.08)
        b.inputs["Subsurface Scale"].default_value = 0.4
    return m

M = dict(rust=mat("rust", RUST, 0.5, sss=0.12), tail=mat("tail", TAIL, 0.5, sss=0.1), tail_l=mat("tail_l", TAIL_L, 0.5, sss=0.1),
         cream=mat("cream", CREAM, 0.45, sss=0.1), ink=mat("ink", INK, 0.12), eye=mat("eye", "#0A1526", 0.06),
         brass=mat("brass", BRASS, 0.38, metal=1.0), brass_d=mat("brass_d", BRASS_D, 0.35, metal=1.0),
         navy=mat("navy", NAVY, 0.9), paper=mat("paper", "#F2F7FB", 0.9), sky=mat("sky", "#DCEAF5", 0.9))

parts = []
def sphere(loc, scale, m, rot=(0, 0, 0), seg=64, name="p"):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, segments=seg, ring_count=seg//2, location=loc)
    o = bpy.context.object; o.scale = scale; o.rotation_euler = Euler([math.radians(a) for a in rot])
    bpy.ops.object.shade_smooth(); o.data.materials.append(m); o.name = name; parts.append(o); return o

# ---- character (faces -Y toward the camera; turned ~20° so we see her 3/4)
# body
sphere((0, 0.1, 0.0), (1.05, 0.95, 1.25), M["rust"], name="body")
sphere((0, -0.55, -0.05), (0.62, 0.45, 0.85), M["cream"], name="chest")
# head
HZ = 1.95
sphere((0, -0.15, HZ), (1.0, 0.95, 0.95), M["rust"], name="head")
HC = Vector((0, -0.15, HZ)); HS = Vector((1.0, 0.95, 0.95))
def on_head(az, el, depth=0.0):
    d = Vector((math.sin(math.radians(az))*math.cos(math.radians(el)), -math.cos(math.radians(az))*math.cos(math.radians(el)), math.sin(math.radians(el))))
    return HC + Vector((d.x*HS.x, d.y*HS.y, d.z*HS.z)) * (1.0 - depth)
sphere(on_head(0, -22, 0.25), (0.52, 0.34, 0.36), M["cream"], name="muzzle")
sphere(on_head(0, -12, -0.08), (0.10, 0.08, 0.08), M["ink"], name="nose")
# eyes — big glossy beads sitting in the surface
MZ = on_head(0, -22, 0.25); MS = Vector((0.52, 0.34, 0.36))
def on_muzzle(x, z, out=0.0):
    """point on the muzzle ellipsoid's front surface at local (x, z)."""
    q = max(0.0, 1 - (x/MS.x)**2 - (z/MS.z)**2)
    return Vector((MZ.x + x, MZ.y - MS.y*math.sqrt(q) - out, MZ.z + z))
def mouth_line(name, pts, r=0.02):
    bpy.ops.object.metaball_add(type="BALL", location=(0, 0, 0)); mb = bpy.context.object; mb.name = name
    mb.data.resolution = 0.05; mb.data.render_resolution = 0.008; mb.data.threshold = 0.6
    mb.data.elements[0].radius = 0.001; mb.data.elements[0].hide = True
    for q in pts:
        e = mb.data.elements.new(); e.co = q; e.radius = r*2.4
    mb.data.materials.append(M["ink"]); parts.append(mb); return mb
squint = EXPR in ("smile", "open", "tilt", "wink", "cat", "dimple", "cheek")
for az in (-27, 27):
    e = sphere(on_head(az, 9, 0.10), (0.18, 0.18, 0.18), M["eye"], name="eye")
    if squint: e.scale = (0.18, 0.18, 0.155); e.location.z -= 0.01
    g = on_head(az - (5 if az > 0 else 2), 14, -0.045); sphere(g, (0.035, 0.03, 0.035), M["cream"], name="eye_glint")
if POSE == "sleep":
    for e_ in [o for o in parts if o.name.startswith("eye")]: parts.remove(e_); bpy.data.objects.remove(e_)
    for az in (-27, 27):
        mouth_line("Sleep%d" % az, [on_head(az + 10*u, 9 + 5*(1-u*u), -0.02) for u in [-1 + 2*k/24 for k in range(25)]], r=0.022)
if EXPR == "wink":
    # right eye (her left, camera right) becomes a happy closed arch
    right = [o for o in parts if o.name.startswith("eye")][-1]; parts.remove(right); bpy.data.objects.remove(right)
    c = on_head(30, 10, 0.02)
    arch = []
    for k in range(25):
        u = -1 + 2*k/24
        q = on_head(30 + 11*u, 12 + 6*(1-u*u), -0.02)
        arch.append(q)
    mouth_line("Wink", arch, r=0.022)
    # brow-cheek lift: small cream cheek bump
if EXPR in ("cat", "tilt"):
    # squirrel/cat mouth: two short arcs from under the nose curving out and up
    nz = -0.02   # just under the nose on the muzzle
    for sgn in (-1, 1):
        pts = [on_muzzle(sgn*0.14*u, nz - 0.07*math.sin(math.pi*u) , -0.004) for u in [k/14 for k in range(15)]]
        mouth_line("Cat%d" % sgn, pts, r=0.016)
if EXPR == "dimple":
    # smile implied by the corners only
    for sgn in (-1, 1):
        pts = [on_muzzle(sgn*(0.13 + 0.05*u), -0.075 + 0.05*u*u, -0.004) for u in [k/8 for k in range(9)]]
        mouth_line("Dimple%d" % sgn, pts, r=0.017)
if EXPR == "cheek":
    # shorter, higher smile tucked right under the nose, with fuller cheeks
    m_ = [o for o in parts if o.name.startswith("muzzle")][0]; m_.scale = (0.56, 0.34, 0.37)
    mouth_line("Smile", [on_muzzle(x, -0.06 + 0.07*(x/0.15)**2, -0.005) for x in [-0.15 + 0.30*k/24 for k in range(25)]], r=0.017)
if EXPR in ("smile", "wink"):
    zc = -0.075
    mouth_line("Smile", [on_muzzle(x, zc + 0.10*(x/0.20)**2, -0.005) for x in [-0.20 + 0.40*k/24 for k in range(25)]], r=0.018)
if EXPR == "open":
    # open, warm smile: dark mouth pocket set into the muzzle, with a smile line rim
    zc = -0.09
    mo = sphere(on_muzzle(0, zc - 0.045, -0.01), (0.15, 0.05, 0.045), M["ink"], name="mouth")
    mouth_line("Smile", [on_muzzle(x, zc + 0.10*(x/0.20)**2, -0.005) for x in [-0.20 + 0.40*k/24 for k in range(25)]], r=0.018)
# feet (only in view on the wider pose framing) and a hint of cheek
for sx in (-0.42, 0.42):
    sphere((sx, -0.78, -1.02), (0.30, 0.40, 0.17), M["rust"], name="foot")
    sphere((sx*1.05, -1.08, -1.0), (0.2, 0.1, 0.11), M["cream"], name="foot_pad") if False else None
CHEEK = mat("cheek", "#D98457", 0.55, sss=0.15)
for az in (-46, 46):
    sphere(on_head(az, -14, -0.01), (0.13, 0.09, 0.1), CHEEK, name="cheek")
# ears
for sx, rot in ((-0.55, 18), (0.60, -14)):
    sphere((sx, -0.05, HZ+0.95), (0.25, 0.16, 0.45), M["rust"], rot=(0, rot, 0), name="ear")
    sphere((sx*0.98, -0.15, HZ+0.95), (0.14, 0.08, 0.30), M["cream"], rot=(0, rot, 0), name="ear_in")
# ---- props
font = bpy.data.fonts.load(f"{SCR}/fonts/Nunito.ttf")
def box(loc, scale, m, rot=(0, 0, 0), name="box", bevel=0.03):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object
    o.scale = scale; o.rotation_euler = Euler([math.radians(v) for v in rot]); o.data.materials.append(m); o.name = name
    bv = o.modifiers.new("bevel", "BEVEL"); bv.width = bevel; bv.segments = 4; bpy.ops.object.shade_smooth(); parts.append(o); return o
def coin_at(loc, tilt=84, r=0.70, yaw=0.0):
    rot = Euler((math.radians(tilt), 0, math.radians(yaw)))
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=0.14, vertices=128, location=loc)
    c = bpy.context.object; c.rotation_euler = rot; c.data.materials.append(M["brass"]); bpy.ops.object.shade_smooth(); parts.append(c)
    n = rot.to_matrix() @ Vector((0, 0, 1))   # face normal toward the camera side
    bpy.ops.mesh.primitive_torus_add(major_radius=r*0.95, minor_radius=r*0.065, major_segments=128, minor_segments=24, location=Vector(loc) + n*0.075)
    rm = bpy.context.object; rm.rotation_euler = rot; rm.data.materials.append(M["brass_d"]); parts.append(rm)
    bpy.ops.object.text_add(location=Vector(loc) + n*0.11 + Vector((0, 0, -0.02))); t = bpy.context.object
    t.data.body = "£"; t.data.font = font; t.data.size = r*1.43; t.data.extrude = 0.04; t.data.bevel_depth = 0.006
    t.data.align_x = "CENTER"; t.data.align_y = "CENTER"; t.rotation_euler = rot
    t.data.materials.append(M["navy" if VARIANT.endswith("-navyglyph") else "cream"]); parts.append(t)
def arm(sx, loc, rot, length=0.45):
    sphere(loc, (0.24, 0.24, length), M["rust"], rot=rot, name="arm")
def paw(loc, r=0.16):
    return sphere(loc, (r*1.06, r*0.95, r*0.95), M["rust"], name="paw")

def limb(a, b, r=0.22):
    """A capsule-ish arm from point a to point b."""
    a, b = Vector(a), Vector(b); d = b - a; L = d.length
    o = sphere(tuple((a + b) / 2), (r, r, L/2 + r*0.6), M["rust"], name="arm")
    o.rotation_euler = d.to_track_quat("Z", "Y").to_euler(); return o

def hold_coin(loc, r, sides=(-1, 1), tilt=84):
    """Arms from the shoulders to the coin, paws cupping its lower edge with fingers curled over the front."""
    loc = Vector(loc)
    rot = Euler((math.radians(tilt), 0, 0)); n = rot.to_matrix() @ Vector((0, 0, 1))   # toward the camera
    for sx in sides:
        ang = math.radians(-35 if sx > 0 else 215)                # 4 o'clock / 8 o'clock on the rim
        rim = loc + Vector((r*math.cos(ang), 0, r*math.sin(ang)))
        shoulder = Vector((sx*0.82, -0.35, 0.95))
        limb(shoulder, rim + Vector((sx*0.08, 0.12, 0.0)), r=0.2)
        # the mitt: a flattened ball on the rim, mostly in front of the coin
        mitt = sphere(tuple(rim + n*0.07 + Vector((sx*0.03, 0, -0.02))), (0.2, 0.15, 0.15), M["rust"], name="paw")
        mitt.rotation_euler = Euler((0, 0, ang + math.pi/2))
        # three fingers curling over the front face just inside the rim
        for k in range(3):
            fa = ang + (k - 1) * math.radians(13)
            fp = loc + Vector(((r - 0.09)*math.cos(fa), 0, (r - 0.09)*math.sin(fa))) + n*0.19
            sphere(tuple(fp), (0.062, 0.05, 0.062), M["rust"], name="finger")

if POSE == "coin":
    coin_at((0, -1.05, 0.55)); hold_coin((0, -1.05, 0.55), 0.70)
elif POSE == "wave":
    # left arm holds the coin low; right arm up, open paw
    coin_at((-0.15, -1.0, 0.45), r=0.6); hold_coin((-0.15, -1.0, 0.45), 0.6, sides=(-1,))
    arm(1, (1.05, -0.35, 1.45), (-10, 25, 0), length=0.55); paw((1.25, -0.5, 1.95), r=0.19)
    for k in range(3):   # fingers
        sphere((1.15 + 0.1*k, -0.55, 2.13 + (0.04 if k == 1 else 0)), (0.06, 0.05, 0.09), M["rust"], name="finger")
elif POSE == "thumbs":
    coin_at((-0.15, -1.0, 0.45), r=0.6); hold_coin((-0.15, -1.0, 0.45), 0.6, sides=(-1,))
    arm(1, (1.0, -0.45, 1.2), (0, 20, 0), length=0.5); paw((1.05, -0.55, 1.7), r=0.19)
    sphere((1.0, -0.6, 1.98), (0.07, 0.07, 0.15), M["rust"], name="thumb")
elif POSE == "point":
    coin_at((-0.15, -1.0, 0.45), r=0.6); hold_coin((-0.15, -1.0, 0.45), 0.6, sides=(-1,))
    arm(1, (1.15, -0.5, 1.1), (0, 72, 0), length=0.5); paw((1.62, -0.55, 1.22), r=0.17)
    sphere((1.86, -0.58, 1.26), (0.17, 0.07, 0.07), M["rust"], name="finger")
elif POSE == "laptop":
    lap = mat("laptop", "#1B2E4F", 0.35); scr = mat("screen", "#DCEAF5", 0.5)
    # base tilted 10° toward her, held at chest height; lid open toward her face
    box((0, -1.12, 0.55), (1.25, 0.82, 0.06), lap, rot=(10, 0, 0), name="lapbase")
    box((0, -0.78, 0.95), (1.25, 0.06, 0.78), lap, rot=(-8, 0, 0), name="laplid")
    box((0, -0.825, 0.95), (1.1, 0.02, 0.64), scr, rot=(-8, 0, 0), name="screen", bevel=0.005)
    # carrying it: upper arm down the outside, forearm under the base, mitt below each front corner,
    # fingers in front of the lip. Base: x ±0.625, front face y≈-1.39, underside z≈0.48-0.50.
    for sx in (-1, 1):
        limb((sx*0.82, -0.35, 0.95), (sx*0.90, -1.05, 0.42), r=0.19)              # upper arm, clear of the base
        limb((sx*0.90, -1.05, 0.36), (sx*0.50, -1.28, 0.34), r=0.115)             # forearm, under the base
        sphere((sx*0.55, -1.35, 0.36), (0.16, 0.15, 0.085), M["rust"], name="paw")   # mitt under the front corner
        for k in range(3):
            sphere((sx*0.55 + (k-1)*0.08, -1.585, 0.48), (0.045, 0.05, 0.06), M["rust"], name="finger")
elif POSE == "chart":
    # a navy card with three rising brass bars, held up on her right
    box((0.95, -0.9, 1.15), (1.15, 0.08, 0.95), mat("card", "#1B2E4F", 0.4), rot=(0, 0, -12), name="card", bevel=0.05)
    for i, h in enumerate((0.28, 0.45, 0.68)):
        box((0.62 + 0.3*i, -0.97 - 0.06*i, 0.78 + h/2), (0.2, 0.06, h), M["brass"], rot=(0, 0, -12), name="bar", bevel=0.02)
    arm(1, (0.95, -0.55, 0.85), (35, -40, 0)); paw((0.95, -0.98, 0.62), r=0.15)
    coin_at((-0.15, -1.0, 0.45), r=0.6); hold_coin((-0.15, -1.0, 0.45), 0.6, sides=(-1,))
elif POSE == "sleep":
    coin_at((0, -1.05, 0.55)); hold_coin((0, -1.05, 0.55), 0.70)
    bpy.ops.object.text_add(location=(1.35, -0.4, 3.0)); z = bpy.context.object
    z.data.body = "z"; z.data.font = font; z.data.size = 0.62; z.data.extrude = 0.03; z.rotation_euler = Euler((math.radians(90), 0, math.radians(-15)))
    z.data.materials.append(M["cream"]); parts.append(z)
    bpy.ops.object.text_add(location=(1.65, -0.3, 3.35)); z2 = bpy.context.object
    z2.data.body = "z"; z2.data.font = font; z2.data.size = 0.42; z2.data.extrude = 0.03; z2.rotation_euler = Euler((math.radians(90), 0, math.radians(-15)))
    z2.data.materials.append(M["cream"]); parts.append(z2)

# tail: chain of spheres rising behind on her right, joined and remeshed into one blob
tail_pts = []
for k in range(14):
    u = k/13
    a = math.radians(-70 + 165*u)
    cx, cz, R = 0.75, 1.45, 1.2
    x = cx + R*math.cos(a)*0.8
    z = cz + R*math.sin(a)
    y = 0.95 - 0.1*u
    r = 0.24 + 0.34*math.sin(math.pi*(0.15+0.85*u))**0.9
    tail_pts.append(((x, y, z), r))
def metatail(name, pts, m, scale=1.0, off=(0, 0, 0)):
    bpy.ops.object.metaball_add(type="BALL", location=(0, 0, 0)); mb = bpy.context.object; mb.name = name
    mb.data.resolution = 0.08; mb.data.render_resolution = 0.035; mb.data.threshold = 0.6
    mb.data.elements[0].radius = 0.001; mb.data.elements[0].hide = True
    for p, r in pts:
        e = mb.data.elements.new(); e.co = Vector(p) + Vector(off); e.radius = r*scale*1.15
    mb.data.materials.append(m); return mb
tail = metatail("TailBlob", tail_pts, M["tail"])
stripe = metatail("TailStripe", tail_pts[3:12], M["tail_l"], scale=0.68, off=(-0.08, -0.26, 0.0))
parts.append(stripe)

if EXPR == "tilt":
    bpy.ops.object.select_all(action="DESELECT")
    for o in parts:
        if o.name.split(".")[0].startswith(("head", "muzzle", "nose", "eye", "ear", "Smile", "Wink", "Sleep", "mouth", "tongue", "Cat", "Dimple")): o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.transform.rotate(value=math.radians(9), orient_axis="Y", center_override=tuple(HC))
    bpy.ops.transform.rotate(value=math.radians(-6), orient_axis="Z", center_override=tuple(HC))
# turn the whole character a little so the camera sees a 3/4 view
bpy.ops.object.select_all(action="DESELECT")
for o in parts + [tail]: o.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.transform.rotate(value=math.radians(-18), orient_axis="Z", center_override=(0, 0, 0))
bpy.ops.transform.rotate(value=math.radians(4), orient_axis="X", center_override=(0, 0, 1))

# ---- ground presets: backdrop, floor, world tint, key colour, optional sun / sea
PRESETS = {
  "night":   dict(back=NAVY,      floor=NAVY,      world=(NAVY, 0.6),      key=(1.0, 0.95, 0.9), fill=(0.9, 0.93, 1.0)),
  "apricot": dict(back="#F3B27A", floor="#E89A5E", world=("#F3B27A", 0.5), key=(1.0, 0.96, 0.9), fill=(1.0, 0.9, 0.85)),
  "sage":    dict(back="#9DBBA4", floor="#86A88E", world=("#9DBBA4", 0.5), key=(1.0, 0.97, 0.9), fill=(0.9, 1.0, 0.95)),
  "teal":    dict(back="#2E7F8C", floor="#256A76", world=("#2E7F8C", 0.5), key=(1.0, 0.95, 0.88), fill=(0.85, 0.95, 1.0)),
  "sky":     dict(back="#BFE0F2", floor="#A9D3EA", world=("#BFE0F2", 0.6), key=(1.0, 0.97, 0.92), fill=(0.9, 0.95, 1.0)),
  "holiday": dict(back="#8FD0EC", floor="#1F8A9A", world=("#8FD0EC", 0.7), key=(1.0, 0.95, 0.85), fill=(0.9, 0.97, 1.0), sun=True, sea=True),
}
PRESETS["clear"] = dict(back=NAVY, floor=NAVY, world=("#F2F7FB", 0.5), key=(1.0, 0.95, 0.9), fill=(0.9, 0.93, 1.0))
PRE = PRESETS[VARIANT.split("-")[0]]
backm = mat("back", PRE["back"], 0.9); floorm = mat("floor", PRE["floor"], 0.25 if PRE.get("sea") else 0.9)
if not TRANSPARENT:
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 7, 1)); p = bpy.context.object
    p.rotation_euler = Euler((math.radians(90), 0, 0)); p.data.materials.append(backm)
if not TRANSPARENT:
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -1.25)); f = bpy.context.object; f.data.materials.append(floorm)
if PRE.get("sun"):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.6, location=(2.6, 6.5, 3.2)); sun = bpy.context.object
    sm = bpy.data.materials.new("sun"); sm.use_nodes = True; nt = sm.node_tree
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = hexc("#FFD98A"); em.inputs["Strength"].default_value = 2.2
    nt.links.new(em.outputs[0], nt.nodes["Material Output"].inputs["Surface"]); sun.data.materials.append(sm)
    bpy.ops.object.shade_smooth()

# ---- lights: warm key front-left, fill right, rim behind top-right
def light(loc, energy, size, color=(1, 1, 1), look_at=(0, -0.3, 1.4)):
    bpy.ops.object.light_add(type="AREA", location=loc); L = bpy.context.object
    L.data.energy = energy; L.data.size = size; L.data.color = color
    d = Vector(look_at) - Vector(loc); L.rotation_euler = d.to_track_quat("-Z", "Y").to_euler(); return L
light((-3.2, -4.5, 4.5), 1100, 3.0, PRE["key"])
light((4.0, -4.0, 2.0), 380, 4.0, PRE["fill"])
light((2.5, 3.5, 4.5), 900, 2.0, (1.0, 0.85, 0.7))
world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = hexc(PRE["world"][0], 0.6)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = PRE["world"][1]

# ---- camera: slightly above eye line, head + coin fill the square
WIDE = POSE != "coin"
bpy.ops.object.camera_add(location=(0.35, -8.4 if WIDE else -7.6, 2.0)); cam = bpy.context.object
cam.data.lens = 55 if WIDE else 62
d = Vector((0.15, -0.3, 1.45)) - cam.location; cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
sc.camera = cam

sc.render.filepath = OUT
t0 = time.time(); bpy.ops.render.render(write_still=True); print("rendered", OUT, round(time.time()-t0, 1), "s")
