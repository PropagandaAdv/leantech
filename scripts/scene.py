"""Scena Blender: shader PBR, studio, luci, camera, render. I colori reti si leggono da config/colors.json (override: env RETE_ACC/RETE_FRE/RETE_STD)."""
import sys, os, json, math; sys.path.insert(0, os.path.dirname(__file__))
from lib import *
import facemat

CFG = json.load(open(os.path.join(os.path.dirname(__file__), "..", "config", "colors.json")))
def hex2lin(h):
    h = h.lstrip("#"); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple((x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4) for x in c)
def color(fam):
    return hex2lin(os.environ.get(fam, CFG[fam]["hex"]))

def _n(nt, t, **kw):
    n = nt.nodes.new(t)
    for k, v in kw.items(): setattr(n, k, v)
    return n
def _in(n, name, v): n.inputs[name].default_value = v

def new_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL": nt.nodes.remove(n)
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    b = nt.nodes.new("ShaderNodeBsdfPrincipled"); nt.links.new(b.outputs[0], out.inputs[0])
    return m, nt, b

def brushed(nt, b, strength=0.2, scale=700, stretch=0.02, rough_var=0.06, base_rough=None):
    """Spazzolatura direzionale lungo Y (asse lunghezza): rumore stirato -> bump + variazione roughness."""
    tc = _n(nt, "ShaderNodeTexCoord"); mp = _n(nt, "ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1, stretch, 1)
    nz = _n(nt, "ShaderNodeTexNoise"); _in(nz, "Scale", scale); _in(nz, "Detail", 4); _in(nz, "Roughness", 0.6)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"]); nt.links.new(mp.outputs[0], nz.inputs["Vector"])
    bm = _n(nt, "ShaderNodeBump"); _in(bm, "Strength", strength); _in(bm, "Distance", 0.0004)
    nt.links.new(nz.outputs["Fac"], bm.inputs["Height"])
    bv = _n(nt, "ShaderNodeBevel"); bv.samples = 4; _in(bv, "Radius", 0.0004)
    nt.links.new(bv.outputs[0], bm.inputs["Normal"]); nt.links.new(bm.outputs[0], b.inputs["Normal"])
    if base_rough is not None and rough_var:
        mr = _n(nt, "ShaderNodeMapRange"); _in(mr, "To Min", base_rough - rough_var); _in(mr, "To Max", base_rough + rough_var)
        nt.links.new(nz.outputs["Fac"], mr.inputs["Value"]); nt.links.new(mr.outputs[0], b.inputs["Roughness"])

def bevel_only(nt, b, r=0.0004):
    bv = _n(nt, "ShaderNodeBevel"); bv.samples = 4; _in(bv, "Radius", r); nt.links.new(bv.outputs[0], b.inputs["Normal"])

def metal(name, rgb, rough, strength=0.2, aniso=0.0):
    m, nt, b = new_mat(name); _in(b, "Base Color", (*rgb, 1)); _in(b, "Metallic", 1.0); _in(b, "Roughness", rough)
    _in(b, "Anisotropic", aniso)
    brushed(nt, b, strength=strength, base_rough=rough); return m

def plastic(name, rgb, rough=0.42, sss=0.0, micro=0.04, spec=0.5, bevel=True):
    m, nt, b = new_mat(name); _in(b, "Base Color", (*rgb, 1)); _in(b, "Roughness", rough); _in(b, "Metallic", 0.0)
    _in(b, "Subsurface Weight", sss); _in(b, "Subsurface Radius", (0.012, 0.008, 0.006)); _in(b, "Subsurface Scale", 0.8)
    b.inputs["Specular IOR Level"].default_value = spec
    if micro:
        tc = _n(nt, "ShaderNodeTexCoord"); nz = _n(nt, "ShaderNodeTexNoise"); _in(nz, "Scale", 1800); _in(nz, "Detail", 3)
        bm = _n(nt, "ShaderNodeBump"); _in(bm, "Strength", micro); _in(bm, "Distance", 0.0002)
        nt.links.new(tc.outputs["Object"], nz.inputs["Vector"]); nt.links.new(nz.outputs["Fac"], bm.inputs["Height"])
        if bevel:
            bv = _n(nt, "ShaderNodeBevel"); bv.samples = 4; _in(bv, "Radius", 0.0004); nt.links.new(bv.outputs[0], bm.inputs["Normal"])
        nt.links.new(bm.outputs[0], b.inputs["Normal"])
    elif bevel: bevel_only(nt, b)
    return m

def rete_acc(rgb):
    """Rete accumulo: plastica + righe di rullini folli (ASSUNZIONE: non modellati nel CAD) -> bump sinusoidale trasversale + solchi scuri."""
    p = CFG["pattern"]["roller_pitch_mm"] / 1000
    m, nt, b = new_mat("RETE_ACC"); _in(b, "Roughness", 0.5); b.inputs["Specular IOR Level"].default_value = 0.25; _in(b, "Subsurface Weight", 0.01); _in(b, "Subsurface Radius", (0.012, 0.008, 0.006)); _in(b, "Subsurface Scale", 0.8)
    tc = _n(nt, "ShaderNodeTexCoord"); sp = _n(nt, "ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], sp.inputs[0])
    mu = _n(nt, "ShaderNodeMath", operation="MULTIPLY"); mu.inputs[1].default_value = 2 * math.pi / p; nt.links.new(sp.outputs["Y"], mu.inputs[0])
    si = _n(nt, "ShaderNodeMath", operation="SINE"); nt.links.new(mu.outputs[0], si.inputs[0])
    mr = _n(nt, "ShaderNodeMapRange"); _in(mr, "From Min", -1); _in(mr, "From Max", 1); nt.links.new(si.outputs[0], mr.inputs["Value"])
    bm = _n(nt, "ShaderNodeBump"); _in(bm, "Strength", 0.55); _in(bm, "Distance", 0.0012); nt.links.new(mr.outputs[0], bm.inputs["Height"]); nt.links.new(bm.outputs[0], b.inputs["Normal"])
    cr = _n(nt, "ShaderNodeValToRGB"); cr.color_ramp.elements[0].position = 0.0; cr.color_ramp.elements[1].position = 0.22
    cr.color_ramp.elements[0].color = (*[c * 0.35 for c in rgb], 1); cr.color_ramp.elements[1].color = (*rgb, 1)
    nt.links.new(mr.outputs[0], cr.inputs["Fac"]); nt.links.new(cr.outputs[0], b.inputs["Base Color"]); return m

def rete_fre(rgb):
    """Rete freno/lancio: plastica chiara + pattini in gomma nera (ASSUNZIONE disposizione: griglia) come maschera procedurale."""
    P = CFG["pattern"]; px, py, w, l = [P[k] / 1000 for k in ("pad_pitch_x_mm", "pad_pitch_y_mm", "pad_w_mm", "pad_l_mm")]
    m, nt, b = new_mat("RETE_FRE"); b.inputs["Specular IOR Level"].default_value = 0.25; _in(b, "Subsurface Weight", 0.01); _in(b, "Subsurface Radius", (0.012, 0.008, 0.006)); _in(b, "Subsurface Scale", 0.8)
    tc = _n(nt, "ShaderNodeTexCoord"); sp = _n(nt, "ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], sp.inputs[0])
    def band(axis, pitch, width):
        md = _n(nt, "ShaderNodeMath", operation="PINGPONG"); md.inputs[1].default_value = pitch / 2  # simmetrico attorno al centro cella
        nt.links.new(sp.outputs[axis], md.inputs[0])
        lt = _n(nt, "ShaderNodeMath", operation="LESS_THAN"); lt.inputs[1].default_value = width / 2 + 0.0  # da PINGPONG (0..pitch/2)
        # PINGPONG: dist dal bordo cella (0..pitch/2); pad centrato = distanza > (pitch-width)/2
        gt = _n(nt, "ShaderNodeMath", operation="GREATER_THAN"); gt.inputs[1].default_value = (pitch - width) / 2
        nt.links.new(md.outputs[0], gt.inputs[0]); return gt.outputs[0]
    mx = _n(nt, "ShaderNodeMath", operation="MULTIPLY"); nt.links.new(band("X", px, w), mx.inputs[0]); nt.links.new(band("Y", py, l), mx.inputs[1])
    mix = _n(nt, "ShaderNodeMix", data_type="RGBA"); nt.links.new(mx.outputs[0], mix.inputs["Factor"])
    mix.inputs["A"].default_value = (*rgb, 1); mix.inputs["B"].default_value = (0.012, 0.012, 0.012, 1)
    nt.links.new(mix.outputs["Result"], b.inputs["Base Color"])
    rr = _n(nt, "ShaderNodeMix", data_type="FLOAT"); nt.links.new(mx.outputs[0], rr.inputs["Factor"]); rr.inputs["A"].default_value = 0.42; rr.inputs["B"].default_value = 0.7
    nt.links.new(rr.outputs["Result"], b.inputs["Roughness"])
    return m

def make_materials(hide_arrow=True):
    M = {}
    M["ALU6061"] = metal("ALU6061", (0.80, 0.82, 0.86), 0.30, strength=0.14, aniso=0.5)      # alluminio anodizzato naturale, freddo
    M["INOX"] = metal("INOX_SATIN", (0.36, 0.335, 0.30), 0.40, strength=0.35)                # AISI 304 satinato, piu' scuro e caldo
    M["INOX_VITE"] = metal("INOX_VITE", (0.50, 0.48, 0.45), 0.25, strength=0.08)
    M["MOTORE"] = plastic("MOTORE", color("MOTORE"), rough=0.5, micro=0.03, spec=0.5)
    M["RETE_STD"] = plastic("RETE_STD", color("RETE_STD"), rough=0.5, sss=0.01, micro=0.05, spec=0.25)
    M["RETE_ACC"] = rete_acc(color("RETE_ACC")); M["RETE_FRE"] = rete_fre(color("RETE_FRE"))
    M["GOMMA"] = plastic("GOMMA", (0.012, 0.012, 0.012), rough=0.72, micro=0.08, spec=0.25)
    M["PL_NERO"] = plastic("PL_NERO", color("PL_NERO"), rough=0.45)
    M["PL_SENSORE"] = plastic("PL_SENSORE", (0.03, 0.03, 0.035), rough=0.3)
    for f in ("PL_PIGNONE", "PL_BLU", "PL_NAVY", "PL_ROSSO", "PL_VERDE", "PL_GRIGIO", "PL_CAVO"):
        M[f] = plastic(f, color(f), rough=0.4 if f != "PL_CAVO" else 0.35)
    M["FRECCIA"] = plastic("FRECCIA", (0.8, 0.8, 0.8), rough=0.5)
    return M

def build_objects(code, M, hide_arrow=True):
    d = load(code); V, N, F = d["V"], d["N"], d["F"]
    fams, fid, _ = facemat.face_families(code, {k: d[k] for k in d})
    objs = {}
    for i, f in enumerate(fams):
        if f == "FRECCIA" and hide_arrow: continue
        ob = mesh_obj(f, V, N, F[fid == i]); ob.data.materials.append(M.get(f, M["INOX"])); objs[f] = ob
    return d, objs

def studio(lo, hi, key_az=-40, size_ref=None):
    """Cielo + pavimento + softbox (key/fill/rim) dimensionati sul modello. lo/hi: bbox (Blender, m)."""
    sc = bpy.context.scene; c = (lo + hi) / 2; S = float(np.linalg.norm(hi - lo)); R = size_ref or S
    w = bpy.data.worlds.new("studio"); w.use_nodes = True; nt = w.node_tree
    bg = nt.nodes["Background"]; gr = nt.nodes.new("ShaderNodeTexGradient"); tc = nt.nodes.new("ShaderNodeTexCoord")
    cr = nt.nodes.new("ShaderNodeValToRGB"); cr.color_ramp.elements[0].color = (0.88, 0.89, 0.90, 1); cr.color_ramp.elements[1].color = (0.95, 0.95, 0.96, 1)
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Rotation"].default_value = (0, math.radians(-90), 0)
    nt.links.new(tc.outputs["Generated"], mp.inputs[0]); nt.links.new(mp.outputs[0], gr.inputs[0]); nt.links.new(gr.outputs["Fac"], cr.inputs["Fac"]); nt.links.new(cr.outputs[0], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = 0.32; sc.world = w
    def area(name, az, el, dist, size, energy, tint=(1, 1, 1)):
        a, e = math.radians(az), math.radians(el)
        loc = (c[0] + dist * math.cos(e) * math.sin(a), c[1] - dist * math.cos(e) * math.cos(a), c[2] + dist * math.sin(e))
        ld = bpy.data.lights.new(name, "AREA"); ld.shape = "RECTANGLE"; ld.size, ld.size_y = size, size * 0.6; ld.energy = energy; ld.color = tint
        ob = bpy.data.objects.new(name, ld); sc.collection.objects.link(ob); ob.location = loc
        ob.rotation_euler = (mathutils.Vector(c) - mathutils.Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    d = R * 1.1
    area("key", key_az, 42, d, R * 0.7, 55 * d * d); area("fill", -key_az + 20, 25, d * 1.2, R * 0.9, 18 * d * d, (0.92, 0.95, 1.0))
    area("rim", 170, 30, d * 1.1, R * 0.6, 45 * d * d); area("top", 0, 85, d, R * 0.9, 20 * d * d)

def cam_look(loc, target, lens, dof_f=None, sensor=36):
    cam = camera(loc, target, lens); cam.data.sensor_width = sensor
    if dof_f:
        cam.data.dof.use_dof = True; cam.data.dof.focus_distance = float(np.linalg.norm(np.array(loc) - np.array(target))); cam.data.dof.aperture_fstop = dof_f
    return cam

def render(path, res=(1920, 1080), samples=128, transparent=False, fmt="PNG", depth="8"):
    sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"
    sc.cycles.samples = samples; sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.02
    sc.cycles.use_denoising = True; sc.cycles.denoiser = "OPENIMAGEDENOISE"; sc.cycles.max_bounces = 6; sc.cycles.glossy_bounces = 4; sc.cycles.transparent_max_bounces = 4
    sc.render.resolution_x, sc.render.resolution_y = res; sc.render.resolution_percentage = 100
    sc.render.film_transparent = transparent
    sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"; sc.view_settings.exposure = -0.5
    sc.render.image_settings.file_format = fmt; sc.render.image_settings.color_depth = depth
    if fmt == "PNG": sc.render.image_settings.color_mode = "RGBA" if transparent else "RGB"
    if fmt == "JPEG": sc.render.image_settings.quality = 92
    sc.render.filepath = path; bpy.ops.render.render(write_still=True)


def make_cyc(R, z0):
    """Ciclorama curva (pavimento -> raccordo -> fondale). Locale: +Y = lontano dalla camera. Il materiale simula un pavimento satinato leggermente riflettente."""
    R = float(R); z0 = float(z0); Rc = 3.0 * R; yf0, y0 = -30 * R, 4.0 * R; zt = 25 * R; xs = (-40 * R, 40 * R)
    prof = [(yf0, 0.0), (y0, 0.0)]
    for t in np.linspace(0, math.pi / 2, 24)[1:]: prof.append((y0 + Rc * math.sin(t), Rc * (1 - math.cos(t))))
    prof.append((y0 + Rc, zt))
    verts, faces = [], []
    for (y, z) in prof:
        for x in xs: verts.append((x, y, z))
    for i in range(len(prof) - 1):
        a, b, c, d = 2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2; faces.append((a, b, c, d))
    me = bpy.data.meshes.new("cyc"); me.from_pydata(verts, [], faces); me.update()
    for p_ in me.polygons: p_.use_smooth = True
    ob = bpy.data.objects.new("cyc", me); bpy.context.scene.collection.objects.link(ob)
    m, nt, b = new_mat("cyc"); _in(b, "Base Color", (0.70, 0.70, 0.71, 1)); _in(b, "Roughness", 0.30); b.inputs["Specular IOR Level"].default_value = 0.5
    _in(b, "Emission Color", (0.8, 0.8, 0.82, 1)); _in(b, "Emission Strength", 0.10); ob.data.materials.append(m)
    ob["z0"] = z0; return ob

def place_cyc(ob, az_deg, tgt, z0):
    ob.location = (tgt[0], tgt[1], z0 - 0.0005); ob.rotation_euler = (0, 0, math.radians(az_deg))
