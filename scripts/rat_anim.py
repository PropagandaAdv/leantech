"""Clip breve RAT (1/2/3 elementi): camera in lento orbit + collo che attraversa il modulo a 30 gradi rispetto al flusso.
Uso: rat_anim.py Z1elemento|Z2elementi|Z3elementi [--fps 25] [--secs 3] [--res 1920x1080] [--samples 12] [--dir DIR] [--only 0,10]"""
import sys, os, math, time, argparse
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ.setdefault("PROFILE", "v2")
from scene import *
from render_all import fit_dist
ap = argparse.ArgumentParser(); ap.add_argument("code"); ap.add_argument("--fps", type=int, default=25); ap.add_argument("--secs", type=float, default=3.0); ap.add_argument("--res", default="1920x1080")
ap.add_argument("--samples", type=int, default=12); ap.add_argument("--dir", default=""); ap.add_argument("--only", default=""); A = ap.parse_args()
code = A.code; D = A.dir or f"work/anim_{code}"; os.makedirs(D, exist_ok=True); K = int([c for c in code if c.isdigit()][0])
reset(); M = make_materials(); d = load(code); V, N, F, FP, prods = d["V"], d["N"], d["F"], d["FP"], d["prods"]
W = {"D00000134705", "A00000020992"}; R = {"A00000021041_PAR.", "A00000021462", "A00000021257"}; M_ = {"A00000021133", "A00000021132_SM Opposta"}
cnt = np.bincount(FP, minlength=len(prods)); fams = {}
for i in range(len(prods)):
    n = str(prods[i]); m = FP == i
    if not m.any(): continue
    vv = V[np.unique(F[m].ravel())] * 1000; zc = (vv.min(0)[2] + vv.max(0)[2]) / 2; md = (vv.max(0) - vv.min(0)).max()
    if n not in W | R | M_ and (cnt[i] > 40000 * K or (cnt[i] > 5000 * K and zc < 385)): continue      # componenti interni non visibili: esclusi (render piu' veloci, stesso aspetto esterno)
    fam = "PL_NERO" if n in W else "GOMMA" if n in R else "MOTORE" if n in M_ else "ALU6061" if n == "PX0000355444" else ("INOX_VITE" if md <= 90 else "INOX")
    fams.setdefault(fam, []).append(F[m])
for fam, Fl in fams.items():
    ob = mesh_obj(fam, V, N, np.concatenate(Fl)); ob.data.materials.append(M[fam])
lo, hi = V.min(0), V.max(0); c = (lo + hi) / 2; Rr = float(np.linalg.norm(hi - lo)); studio(lo, hi, size_ref=max(Rr, 1.0)); cyc = make_cyc(max(Rr, 1.0), lo[2])
corners = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]); top = float(hi[2])
# collo: flusso lungo -Y del modulo; direzione deviata di 30 gradi verso +X
bx, by, bz = {1: (0.22, 0.16, 0.12), 2: (0.34, 0.26, 0.20), 3: (0.46, 0.34, 0.28)}[K]; head = -60.0
me = bpy.data.meshes.new("collo"); me.from_pydata([(dx * bx / 2, dy * by / 2, z) for z in (0, bz) for dx, dy in ((-1, -1), (1, -1), (1, 1), (-1, 1))], [], [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7)])
me.update(); box = bpy.data.objects.new("collo", me); bpy.context.scene.collection.objects.link(box); box.rotation_euler = (0, 0, math.radians(head))
box.data.materials.append(plastic("CARTONE", (0.30, 0.19, 0.09), rough=0.8, micro=0.0, bevel=False))
depth = hi[1] - lo[1]; dirv = np.array([math.cos(math.radians(head)), math.sin(math.radians(head))])
# il collo entra dal bordo di ingresso (a cavallo) ed esce dal bordo opposto: percorso lungo la direzione a 30 gradi rispetto al flusso
trav = (depth + 0.6 * by) / abs(dirv[1]); start = np.array([c[0] - dirv[0] * trav / 2, hi[1] + 0.3 * by]); fps = A.fps; Nf = int(round(A.secs * fps))
ease = lambda u: u * u * (3 - 2 * u); res = tuple(int(x) for x in A.res.split("x")); idx = [int(x) for x in A.only.split(",")] if A.only else range(Nf)
dist = fit_dist(c, 36, 32, 50, corners, margin=0.85); tg = np.array([c[0], c[1], top - 0.02]); print(f"{code}: frame {Nf}, dist {dist:.2f} m, collo {bx}x{by}x{bz}", flush=True); t0 = time.time(); done = 0
for i in idx:
    out = os.path.join(D, f"frame_{i:04d}.jpg")
    if os.path.exists(out): continue
    u = ease(i / max(1, Nf - 1)); pc = start + dirv * trav * u; box.location = (pc[0], pc[1], top + 0.001)
    az = 22 + 30 * (i / max(1, Nf - 1)); ar, e = math.radians(az), math.radians(32)
    loc = (tg[0] + dist * math.cos(e) * math.sin(ar), tg[1] - dist * math.cos(e) * math.cos(ar), tg[2] + dist * math.sin(e))
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]: bpy.data.objects.remove(o)
    cam_look(loc, tuple(tg), 50); place_cyc(cyc, az, tg, lo[2]); t1 = time.time(); render(out, res, A.samples, False, "JPEG", "8"); done += 1; print(f"frame {i}/{Nf-1} {time.time()-t1:.0f}s", flush=True)
print("FRAMES_DONE", done, f"{time.time()-t0:.0f}s", flush=True)
