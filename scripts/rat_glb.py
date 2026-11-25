"""GLB web del RAT 30 gradi: saldatura vertici, decimazione per famiglia (minuteria molto, ruote meno), PBR semplice, Draco.
Uso: rat_glb.py Z1elemento|Z2elementi|Z3elementi [outdir]"""
import sys, os, math, time; sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault("PROFILE", "v2")
from lib import *
import scene
WHEELS = {"D00000134705", "A00000020992"}; RUBBER = {"A00000021041_PAR.", "A00000021462", "A00000021257"}; MOTOR = {"A00000021133", "A00000021132_SM Opposta"}; ALU = {"PX0000355444"}
HEAVY = set()   # prodotti con molte facce (cuscinetti, mozzi, ruote interne), riempito a runtime
PANEL = set()
def family(n, md):
    if n in WHEELS: return "PL_NERO"
    if n in RUBBER: return "GOMMA"
    if n in MOTOR: return "MOTORE"
    if n in ALU: return "ALU6061"
    if n in HEAVY: return "INOX_INT"
    return "INOX_VITE" if md <= 90 else "INOX"
RATIO = {"PL_NERO": 0.10, "GOMMA": 0.12, "MOTORE": 0.10, "ALU6061": 1.0, "INOX_VITE": 0.04, "INOX": 1.0, "INOX_INT": 0.03}
PLANAR = set()   # lamiere/profili: dissoluzione planare (non deforma le superfici piane)
PBR = {"INOX_INT": ((0.36, 0.335, 0.30), 1.0, 0.52), "ALU6061": ((0.62, 0.645, 0.69), 1.0, 0.52), "INOX": ((0.36, 0.335, 0.30), 1.0, 0.52), "INOX_VITE": ((0.50, 0.48, 0.45), 1.0, 0.45),
       "GOMMA": ((0.012, 0.012, 0.012), 0.0, 0.72), "PL_NERO": ((0.06, 0.06, 0.065), 0.0, 0.5), "MOTORE": (scene.color("MOTORE"), 0.0, 0.42)}
def weld(V, F, tol=2e-5):
    q = np.round(V / tol).astype(np.int64); _, idx, inv = np.unique(q, axis=0, return_index=True, return_inverse=True)
    F2 = inv.ravel()[F]; ok = (F2[:, 0] != F2[:, 1]) & (F2[:, 1] != F2[:, 2]) & (F2[:, 0] != F2[:, 2]); return V[idx], F2[ok]
code = sys.argv[1]; outdir = sys.argv[2] if len(sys.argv) > 2 else "render_v2_2026-11-24/B_layout_RAT/glb"; os.makedirs(outdir, exist_ok=True)
t0 = time.time(); reset(); d = load(code); V, F, FP, prods = d["V"], d["F"], d["FP"], d["prods"]
cnt = np.bincount(FP, minlength=len(prods)); K = int([ch for ch in code if ch.isdigit()][0]); HEAVY.update(str(prods[i]) for i in range(len(prods)) if cnt[i] > 40000 * K)
for i in range(len(prods)):        # ferramenta interna pesante sotto il piano superiore (quota < 385 mm): non visibile dall'esterno
    if cnt[i] > 5000 * K:
        vv = V[np.unique(F[FP == i].ravel())] * 1000
        if (vv.min(0)[1] + vv.max(0)[1]) / 2 < 385: HEAVY.add(str(prods[i]))
dims = []; PANEL = set()
for pi in range(len(prods)):
    vi = np.unique(F[FP == pi].ravel()); v = V[vi] * 1000; sz = (v.max(0) - v.min(0)) if len(v) else np.zeros(3); dims.append(sz.max())
    ctop = ((v.min(0) + v.max(0)) / 2)[1]      # quota (Y glTF = Z Blender) del baricentro
    if (sz.max() >= 150 and np.sort(sz)[0] <= 30) or ctop >= 0.395 * 1000: PANEL.add(str(prods[pi]))
fam_of = [family(str(n), dims[i]) for i, n in enumerate(prods)]
HIDDEN = {"INOX_INT"}   # componenti interni (cuscinetti, mozzi) non visibili dall'esterno: esclusi dal GLB web [ASSUNZIONE]
fid = np.array([sorted(set(fam_of)).index(f) for f in fam_of])[FP]; fams = sorted(set(fam_of)); tot = 0
for i, f in enumerate(fams):
    if f in HIDDEN: continue
    if f == "INOX":   # lamiere: normali ORIGINALI del CAD, nessuna saldatura/decimazione (evita sfumature sulle svasature)
        ob = mesh_obj(f, V, d["N"], F[fid == i]); bpy.context.view_layer.objects.active = ob; fl = ob.data.polygons
        base, metal, rough = PBR[f]; m = bpy.data.materials.new(f); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (*base, 1); b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough; ob.data.materials.append(m)
        tot += len(fl); print(f"  {f}: {len(fl)} tri (normali CAD)", flush=True); continue
    Vi, Fi = weld(V, F[fid == i]); vi, inv = np.unique(Fi.ravel(), return_inverse=True); co = Vi[vi].astype(np.float32); fl = inv.reshape(-1, 3).astype(np.int32)
    me = bpy.data.meshes.new(f); me.vertices.add(len(co)); me.vertices.foreach_set("co", co.ravel()); me.loops.add(len(fl) * 3); me.loops.foreach_set("vertex_index", fl.ravel())
    me.polygons.add(len(fl)); me.polygons.foreach_set("loop_start", np.arange(len(fl), dtype=np.int32) * 3); me.update(calc_edges=True)
    ob = bpy.data.objects.new(f, me); bpy.context.scene.collection.objects.link(ob); bpy.context.view_layer.objects.active = ob
    if f in PLANAR:
        md = ob.modifiers.new("dec", "DECIMATE"); md.decimate_type = "DISSOLVE"; md.angle_limit = math.radians(3); md.delimit = {"NORMAL"}; bpy.ops.object.modifier_apply(modifier="dec")
    elif RATIO[f] < 0.98 and len(fl) > 400:
        md = ob.modifiers.new("dec", "DECIMATE"); md.ratio = RATIO[f]; bpy.ops.object.modifier_apply(modifier="dec")
    bpy.ops.object.shade_auto_smooth(angle=math.radians(35))
    base, metal, rough = PBR[f]; m = bpy.data.materials.new(f); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1); b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough; ob.data.materials.append(m)
    tot += len(ob.data.polygons); print(f"  {f}: {len(fl)} -> {len(ob.data.polygons)} tri", flush=True)
out = os.path.join(outdir, f"Z00000005863_{code.replace('Zw','').replace('Z','')}.glb")
for extra in (dict(export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=7), {}):
    try: bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", export_apply=True, export_yup=True, export_draco_position_quantization=12, export_draco_normal_quantization=8, **extra); break
    except Exception as e: print("export fallito", str(e)[:100])
print(out, round(os.path.getsize(out) / 1e6, 2), "MB;", tot, "triangoli;", round(time.time() - t0), "s")
