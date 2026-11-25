"""Render del trasferitore RAT 30° (Z00000005863, 1/2/3 elementi). Materiali assegnati per REGOLE (il CAD non ha colori): [ASSUNZIONE].
Uso: rat_render.py CODICE[Z1elemento|Z2elementi|Z3elementi] [--views 34,alto,ruote] [--res 1920x1080] [--samples 96] [--out DIR] [--masters]"""
import argparse, os, sys, time, math; sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault("PROFILE", "v2")
from scene import *
from render_all import fit_dist

WHEELS = {"D00000134705", "A00000020992"}                         # griglia di ruote e relativi pneumatici sul piano superiore
RUBBER = {"A00000021041_PAR.", "A00000021462", "A00000021257"}    # cinghie
MOTOR = {"A00000021133", "A00000021132_SM Opposta"}               # motoriduttori
ALU = {"PX0000355444"}                                            # profilo estruso
def family(name, maxdim_mm):
    if name in WHEELS: return "PL_NERO"        # ruote/pneumatici: plastica/gomma grigio scuro-nero
    if name in RUBBER: return "GOMMA"
    if name in MOTOR: return "MOTORE"
    if name in ALU: return "ALU6061"
    return "INOX_VITE" if maxdim_mm <= 90 else "INOX"   # minuteria piccola vs lamiere/telaio: inox satinato

ap = argparse.ArgumentParser(); ap.add_argument("code"); ap.add_argument("--views", default="34,alto,ruote"); ap.add_argument("--res", default="1920x1080")
ap.add_argument("--samples", type=int, default=96); ap.add_argument("--out", default="render_v2_2026-11-24/B_layout_RAT/web_FHD"); ap.add_argument("--masters", action="store_true"); ap.add_argument("--tag", default="")
a = ap.parse_args(); code = a.code; os.makedirs(a.out, exist_ok=True)
t0 = time.time(); reset(); M = make_materials(); d = load(code); V, N, F, FP, prods = d["V"], d["N"], d["F"], d["FP"], d["prods"]
dims = np.zeros(len(prods))
for pi in range(len(prods)):
    vi = np.unique(F[FP == pi].ravel()); v = V[vi] * 1000; dims[pi] = (v.max(0) - v.min(0)).max() if len(v) else 0
fam_of = [family(str(n), dims[i]) for i, n in enumerate(prods)]; fams = sorted(set(fam_of)); fid = np.array([fams.index(f) for f in fam_of])[FP]
for i, f in enumerate(fams):
    ob = mesh_obj(f, V, N, F[fid == i]); ob.data.materials.append(M[f])
lo, hi = V.min(0), V.max(0); c = (lo + hi) / 2; Rr = float(np.linalg.norm(hi - lo)); studio(lo, hi, size_ref=max(Rr, 1.0)); cyc = make_cyc(max(Rr, 1.0), lo[2])
corners = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
wm = np.isin(FP, [i for i, n in enumerate(prods) if str(n) in WHEELS]); wc = V[F[wm].ravel()].mean(0)    # baricentro ruote (centro del piano superiore)
top = float(hi[2])
VIEWS = {"34": dict(az=38, el=28, lens=50, tgt=c, dist=fit_dist(c, 38, 28, 50, corners, margin=0.93)),
         "alto": dict(az=0, el=88, lens=50, tgt=c, dist=fit_dist(c, 0, 88, 50, corners, margin=0.93)),
         "ruote": dict(az=22, el=46, lens=85, tgt=np.array([wc[0], wc[1], top - 0.01]), dist=0.62)}
res = tuple(int(x) for x in a.res.split("x")); tag = "4K" if res[0] >= 3840 else "FHD"
print(f"scena pronta {time.time()-t0:.0f}s; famiglie {fams}; facce {len(F)}", flush=True)
for vn in a.views.split(","):
    v = VIEWS[vn]; ar, e = math.radians(v["az"]), math.radians(v["el"]); t = v["tgt"]
    loc = (t[0] + v["dist"] * math.cos(e) * math.sin(ar), t[1] - v["dist"] * math.cos(e) * math.cos(ar), t[2] + v["dist"] * math.sin(e))
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]: bpy.data.objects.remove(o)
    cam_look(loc, tuple(t), v["lens"]); place_cyc(cyc, v["az"], t, lo[2]); t1 = time.time()
    base = os.path.join(a.out, f"Z00000005863_{code[1:]}_{vn}_{tag}{a.tag}")
    render(base + (".png" if a.masters else ".jpg"), res, a.samples, False, "PNG" if a.masters else "JPEG", "16" if a.masters else "8")
    print(f"{code} {vn} {tag} {time.time()-t1:.0f}s", flush=True)
