"""Export GLB web: mesh saldate + decimate per famiglia, materiali PBR (senza nodi procedurali), texture planare pattini/rullini, Draco.
Uso: 08_export_glb.py CODICE [target_triangoli]"""
import sys, os, json, math, time; sys.path.insert(0, os.path.dirname(__file__))
from lib import *
import facemat, scene
from PIL import Image, ImageDraw

code = sys.argv[1]; target = int(sys.argv[2]) if len(sys.argv) > 2 else 400000
OUT = f"output/web/{code}.glb"; os.makedirs("output/web", exist_ok=True); os.makedirs("work/tex", exist_ok=True)
PBR = {"ALU6061": ((0.80, 0.82, 0.86), 1.0, 0.30), "INOX": ((0.36, 0.335, 0.30), 1.0, 0.40), "INOX_VITE": ((0.50, 0.48, 0.45), 1.0, 0.25),
       "GOMMA": ((0.012, 0.012, 0.012), 0.0, 0.72), "PL_SENSORE": ((0.03, 0.03, 0.035), 0.0, 0.3)}
def pbr(fam):
    if fam in PBR: return PBR[fam]
    if fam in ("MOTORE", "RETE_STD", "RETE_ACC", "RETE_FRE", "PL_NERO", "PL_PIGNONE", "PL_BLU", "PL_NAVY", "PL_ROSSO", "PL_VERDE", "PL_GRIGIO", "PL_CAVO"):
        return (scene.color(fam), 0.0, 0.42)
    return ((0.5, 0.5, 0.5), 0.5, 0.5)

def srgb(lin): return tuple(int(round(255 * (c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055))) for c in lin)
def pattern_tex(fam):
    P = scene.CFG["pattern"]; base = srgb(scene.color(fam))
    if fam == "RETE_FRE":
        px, py, w, l = P["pad_pitch_x_mm"], P["pad_pitch_y_mm"], P["pad_w_mm"], P["pad_l_mm"]; W, H = 8 * px, 8 * py
        im = Image.new("RGB", (W, H), base); dr = ImageDraw.Draw(im); dr.rectangle([(px - w) // 2, (py - l) // 2, (px + w) // 2, (py + l) // 2], fill=(5, 5, 5))
        return im.resize((128, 192)), (px / 1000, py / 1000)
    p = P["roller_pitch_mm"]; im = Image.new("RGB", (16, 8 * p), base); dr = ImageDraw.Draw(im)
    for y in range(8 * p):
        t = abs(math.sin(math.pi * y / (8 * p))); k = 0.55 + 0.45 * min(1, t * 3); dr.line([(0, y), (16, y)], fill=tuple(int(c * k) for c in base))
    return im.resize((16, 256)), (0.016, p / 1000)

def weld(V, F, tol=2e-5):
    q = np.round(V / tol).astype(np.int64); _, idx, inv = np.unique(q, axis=0, return_index=True, return_inverse=True)
    F2 = inv.ravel()[F]; ok = (F2[:, 0] != F2[:, 1]) & (F2[:, 1] != F2[:, 2]) & (F2[:, 0] != F2[:, 2]); return V[idx], F2[ok]

t0 = time.time(); reset(); d = load(code); V, F = d["V"], d["F"]
fams, fid, _ = facemat.face_families(code, {k: d[k] for k in d}); n = len(F)
keep = np.array([f != "FRECCIA" for f in fams])[fid]; fams_used = {}
total_w = 0; parts = []
for i, f in enumerate(fams):
    if f == "FRECCIA": continue
    Vi, Fi = weld(V, F[fid == i]); parts.append((f, Vi, Fi)); total_w += len(Fi)
print("facce saldate", total_w, "target", target, flush=True)
ratio = min(1.0, target / total_w)
for f, Vi, Fi in parts:
    vi, inv = np.unique(Fi.ravel(), return_inverse=True); co = Vi[vi].astype(np.float32); fl = inv.reshape(-1, 3).astype(np.int32)
    me = bpy.data.meshes.new(f); me.vertices.add(len(co)); me.vertices.foreach_set("co", co.ravel())
    me.loops.add(len(fl) * 3); me.loops.foreach_set("vertex_index", fl.ravel()); me.polygons.add(len(fl)); me.polygons.foreach_set("loop_start", np.arange(len(fl), dtype=np.int32) * 3)
    me.update(calc_edges=True); ob = bpy.data.objects.new(f, me); bpy.context.scene.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    r = ratio if f not in ("RETE_STD", "RETE_ACC", "RETE_FRE") else 1.0      # reti: poche facce, non decimare
    if r < 0.98 and len(fl) > 400:
        md = ob.modifiers.new("dec", "DECIMATE"); md.ratio = max(r, 0.02); bpy.ops.object.modifier_apply(modifier="dec")
    bpy.ops.object.shade_auto_smooth(angle=math.radians(35))
    base, metal, rough = pbr(f); m = bpy.data.materials.new(f); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1); b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough
    if f in ("RETE_FRE", "RETE_ACC"):
        im, (tu, tv) = pattern_tex(f); tp = f"work/tex/{f}.png"; im.save(tp)
        uv = ob.data.uv_layers.new(name="UV"); co2 = np.array([v.co[:] for v in ob.data.vertices]); loops = np.array([l.vertex_index for l in ob.data.loops])
        uvs = np.stack([co2[loops, 0] / tu, co2[loops, 1] / tv], 1).astype(np.float32); uv.data.foreach_set("uv", uvs.ravel())
        tn = m.node_tree.nodes.new("ShaderNodeTexImage"); tn.image = bpy.data.images.load(os.path.abspath(tp)); tn.interpolation = "Linear"
        m.node_tree.links.new(tn.outputs["Color"], b.inputs["Base Color"])
    ob.data.materials.append(m)
print("mesh pronte", round(time.time() - t0), "s; triangoli finali", sum(len(o.data.polygons) for o in bpy.data.objects if o.type == "MESH"), flush=True)
kw = dict(filepath=OUT, export_format="GLB", export_apply=True, export_yup=True)
for extra in (dict(export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=7), dict(export_meshopt_compression_enable=True), {}):
    try: bpy.ops.export_scene.gltf(**kw, **extra); print("export ok", extra); break
    except Exception as e: print("export fallito", extra, str(e)[:120])
print(OUT, round(os.path.getsize(OUT) / 1e6, 2), "MB", round(time.time() - t0), "s")
