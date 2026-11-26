"""Layout intralogistico 5000 CPH (schematico, ricostruito da immagini 2D del cliente) + RAT reale (Z00000005863-3elementi).
[ASSUNZIONE] scala: larghezza linea principale = lato lungo del RAT (1134 mm); nastri procedurali (non da CAD). Uso: layout_build.py [--views L1,L2] [--res 1280x720] [--samples 48] [--out DIR]"""
import argparse, os, sys, math, time; sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault("PROFILE", "v2"); os.environ.setdefault("FRENO_VARIANT", "a")
from scene import *
from render_all import fit_dist

Z_TOP = 0.75; W_MAIN = 1.10; W_BR = 0.90; E = W_MAIN / 2      # quota piano nastro, larghezze (m)
def path(segs, p0=(0, 0), h0=0.0, step=0.06):
    """segs: ('l',L) | ('a',gradi(+sinistra),R). Ritorna polilinea Nx3 (x,y,heading rad)."""
    x, y, h = p0[0], p0[1], math.radians(h0); pts = [(x, y, h)]
    for s in segs:
        if s[0] == "l":
            n = max(1, int(s[1] / step))
            for i in range(1, n + 1): pts.append((x + math.cos(h) * s[1] * i / n, y + math.sin(h) * s[1] * i / n, h))
            x, y = pts[-1][0], pts[-1][1]
        else:
            ang = math.radians(s[1]); R = s[2]; sg = 1 if ang > 0 else -1; cx = x - math.sin(h) * R * sg; cy = y + math.cos(h) * R * sg
            n = max(2, int(abs(ang) * R / step))
            for i in range(1, n + 1):
                hh = h + ang * i / n; pts.append((cx + math.sin(hh) * R * sg, cy - math.cos(hh) * R * sg, hh))
            x, y, h = pts[-1]
    return np.array(pts)
def shifted(P, dx, dy): Q = P.copy(); Q[:, 0] += dx; Q[:, 1] += dy; return Q
class Mesh:
    def __init__(s): s.V = []; s.F = []
    def add(s, V, F): o = len(s.V); s.V += [tuple(v) for v in V]; s.F += [tuple(o + i for i in f) for f in F]
def sweep(m, P, a, b, z0, z1):
    """Prisma chiuso lungo il percorso tra offset laterali a..b e quote z0..z1."""
    n = len(P); nx, ny = -np.sin(P[:, 2]), np.cos(P[:, 2]); V = []
    for off, z in ((a, z1), (b, z1), (b, z0), (a, z0)): V += [(P[i, 0] + nx[i] * off, P[i, 1] + ny[i] * off, z) for i in range(n)]
    F = []
    for k in range(4):
        k2 = (k + 1) % 4
        for i in range(n - 1): F.append((k * n + i, k * n + i + 1, k2 * n + i + 1, k2 * n + i))
    F.append((0, n, n + 0, 0)); F = [f for f in F if len(set(f)) == 4]
    F.append((3 * n, 2 * n, 1 * n, 0)); F.append((n - 1, n + n - 1, 2 * n + n - 1, 3 * n + n - 1))
    m.add(V, [(f[0], f[1], f[2]) for f in F] + [(f[0], f[2], f[3]) for f in F if len(set(f)) == 4])
def box(m, cx, cy, z0, z1, sx, sy):
    V = [(cx + dx * sx / 2, cy + dy * sy / 2, z) for z in (z0, z1) for dx, dy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    m.add(V, [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7)])
def to_obj(name, m, mat, smooth=True):
    me = bpy.data.meshes.new(name); me.from_pydata(m.V, [], m.F); me.update(); ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat)
    if smooth: bpy.context.view_layer.objects.active = ob; bpy.ops.object.shade_auto_smooth(angle=math.radians(40))
    return ob

def conveyor(G, P, width, belt="belt", legs_every=2.0, belt_z=Z_TOP):
    """Nastro: piano + 2 fiancate alluminio + corpo/gambe inox lungo il percorso P."""
    sweep(G[belt], P, -width / 2 + 0.02, width / 2 - 0.02, belt_z - 0.03, belt_z)
    sweep(G["alu"], P, width / 2 - 0.02, width / 2 + 0.05, belt_z - 0.20, belt_z + 0.08); sweep(G["alu"], P, -width / 2 - 0.05, -width / 2 + 0.02, belt_z - 0.20, belt_z + 0.08)
    sweep(G["inox"], P, -width / 2 + 0.02, width / 2 - 0.02, belt_z - 0.20, belt_z - 0.03)
    d = np.r_[0, np.cumsum(np.hypot(np.diff(P[:, 0]), np.diff(P[:, 1])))]; nxt = 0.5
    for i in range(len(P)):
        if d[i] >= nxt:
            nxt += legs_every
            for sgn in (-1, 1):
                lx = P[i, 0] - math.sin(P[i, 2]) * sgn * (width / 2 + 0.03); ly = P[i, 1] + math.cos(P[i, 2]) * sgn * (width / 2 + 0.03)
                box(G["inox"], lx, ly, 0.0, belt_z - 0.20, 0.05, 0.05); box(G["gomma"], lx, ly, 0.0, 0.02, 0.12, 0.12)

def rat_mesh(code="Z3elementi"):
    """RAT reale (3 elementi), parti visibili dall'esterno (come nei GLB web), famiglie per regola. Ritorna lista (famiglia, V, N, F)."""
    d = load(code); V, N, F, FP, prods = d["V"], d["N"], d["F"], d["FP"], d["prods"]
    W = {"D00000134705", "A00000020992"}; R = {"A00000021041_PAR.", "A00000021462", "A00000021257"}; M_ = {"A00000021133", "A00000021132_SM Opposta"}
    cnt = np.bincount(FP, minlength=len(prods)); K = 3; hide = set()
    for i in range(len(prods)):
        n = str(prods[i]); vv = V[np.unique(F[FP == i].ravel())] * 1000
        if n in W | R | M_: continue
        if cnt[i] > 40000 * K or (cnt[i] > 5000 * K and (vv.min(0)[2] + vv.max(0)[2]) / 2 < 385): hide.add(n)
    out = {}
    for i in range(len(prods)):
        n = str(prods[i]); m = FP == i
        if n in hide or not m.any(): continue
        vv = V[np.unique(F[m].ravel())] * 1000; md = (vv.max(0) - vv.min(0)).max()
        fam = "PL_NERO" if n in W else "GOMMA" if n in R else "MOTORE" if n in M_ else "ALU6061" if n == "PX0000355444" else ("INOX_VITE" if md <= 90 else "INOX")
        out.setdefault(fam, []).append(F[m])
    lo, hi = V.min(0), V.max(0); return V, N, {k: np.concatenate(v) for k, v in out.items()}, lo, hi

ap = argparse.ArgumentParser(); ap.add_argument("--views", default="L1,L2"); ap.add_argument("--res", default="1280x720"); ap.add_argument("--samples", type=int, default=48)
ap.add_argument("--out", default="work/lay_test"); ap.add_argument("--tag", default=""); ap.add_argument("--save-blend", action="store_true"); a = ap.parse_args()
os.makedirs(a.out, exist_ok=True); t0 = time.time(); reset(); M = make_materials()
G = {"belt": Mesh(), "alu": Mesh(), "inox": Mesh(), "gomma": Mesh(), "light": Mesh()}
# --- linea principale (+ curva busta) ---
X_END = 67.4; main_p = path([("l", X_END), ("a", -90, 1.65), ("l", 5.3)], (0, 0), 0)
JX = [38.9 + 4.575 * k for k in range(6)]; GAP = 0.45     # la linea principale e' interrotta dove sta il RAT (0,766 m lungo la linea)
edges = [(-1, JX[0] - GAP)] + [(JX[k] + GAP, JX[k + 1] - GAP) for k in range(5)] + [(JX[5] + GAP, X_END + 0.001)]
for x0, x1 in edges:
    sub = main_p[(main_p[:, 0] >= x0) & (main_p[:, 0] <= x1)]
    if len(sub) > 2: conveyor(G, sub, W_MAIN, "belt", legs_every=2.0)
conveyor(G, path([("a", -90, 1.65), ("l", 5.3)], (X_END, 0), 0), 1.0, "light")
# --- 6 uscite sopra e sotto: nastro a 30 gradi + curva a 90 gradi + tratto verticale (scuro poi chiaro) ---
Y_END = 8.25
for jx in JX:
    for sg in (1, -1):
        h0 = 30 * sg; p1 = path([("l", 3.2), ("a", 60 * sg, 1.6)], (jx - 1.3, sg * (E + 0.42)), h0); y1 = p1[-1, 1]; L2 = abs(sg * Y_END - y1)
        conveyor(G, p1, W_BR, "belt"); conveyor(G, path([("l", 1.9)], (p1[-1, 0], y1), 90 * sg), W_BR, "belt")
        conveyor(G, path([("l", L2 - 1.9)], (p1[-1, 0], y1 + sg * 1.9), 90 * sg), W_BR, "light")
# --- 7 canali in ingresso (3 sopra, 4 sotto) con raccordo a 30 gradi ---
for ya, mx in ((5.75, 12.25), (3.9, 8.5), (2.1, 5.1), (-2.1, 5.1), (-3.9, 8.75), (-5.75, 12.25), (-7.75, 15.75)):
    sg = 1 if ya > 0 else -1; segs = [("l", 2.2), ("a", -30 * sg, 1.0), ("l", (abs(ya) - E) / math.sin(math.radians(30)))]
    p = path(segs, (0, ya), 0); p = shifted(p, mx - p[-1, 0], 0); conveyor(G, p, W_BR, "belt")
# --- anello UNREAD (U sotto la linea) ---
CY = -E - 0.1 - 1.7; loop = path([("a", 180, 1.7), ("l", 14.0), ("a", 180, 1.7)], (19.5, CY + 1.7), 180); conveyor(G, loop, W_BR, "belt")
mats = {"belt": M["RETE_STD"], "alu": M["ALU6061"], "inox": M["INOX"], "gomma": M["GOMMA"], "light": M["PL_GRIGIO"]}
for k, m in G.items(): to_obj("lay_" + k, m, mats[k])
# --- RAT reale nei 6 incroci (istanze collegate) ---
V, N, fams, lo, hi = rat_mesh(); c = (lo + hi) / 2; rat_objs = []
for fam, Fm in fams.items():
    Vv = V.copy(); Vv[:, 0] -= c[0]; Vv[:, 1] -= c[1]; Vv[:, 2] += Z_TOP - hi[2] + 0.0
    ob = mesh_obj("RAT_" + fam, Vv, N, Fm); ob.data.materials.append(M[fam]); ob.rotation_euler = (0, 0, math.radians(90)); rat_objs.append(ob)
bpy.context.view_layer.update()
for jx in JX:
    for ob in rat_objs:
        if jx == JX[0]: ob.location = (jx, 0, 0)
        else: o2 = bpy.data.objects.new(ob.name + "_i", ob.data); o2.rotation_euler = ob.rotation_euler; o2.location = (jx, 0, 0); bpy.context.scene.collection.objects.link(o2)
allv = np.array([(0, -9.5), (X_END + 2.5, 9.5), (0, 9.5), (X_END + 2.5, -9.5)]); LO = np.array([0 - 2, -10.0, 0.0]); HI = np.array([X_END + 3, 10.0, 1.2])
c0 = (LO + HI) / 2; Rr = float(np.linalg.norm(HI - LO)); studio(LO, HI, size_ref=Rr); cyc = make_cyc(Rr, 0.0)
corners = np.array([[x, y, z] for x in (LO[0], HI[0]) for y in (LO[1], HI[1]) for z in (LO[2], HI[2])])
rz = np.array([JX[0], 0.0, Z_TOP]); mid = np.array([np.mean(JX), 0.0, Z_TOP])
VIEWS = {"L1": dict(az=0, el=58, lens=35, tgt=c0, dist=fit_dist(c0, 0, 58, 35, corners, margin=0.95)),
         "L2": dict(az=0, el=62, lens=50, tgt=np.array([JX[0], 0.0, 0.5]), dist=8.5),
         "L2b": dict(az=0, el=58, lens=40, tgt=np.array([np.mean(JX), 0.0, 0.5]), dist=26.0)}
res = tuple(int(x) for x in a.res.split("x")); print(f"scena pronta {time.time()-t0:.0f}s", flush=True)
for vn in a.views.split(","):
    v = VIEWS[vn]; ar, e = math.radians(v["az"]), math.radians(v["el"]); t = v["tgt"]
    loc = (t[0] + v["dist"] * math.cos(e) * math.sin(ar), t[1] - v["dist"] * math.cos(e) * math.cos(ar), t[2] + v["dist"] * math.sin(e))
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]: bpy.data.objects.remove(o)
    cam_look(loc, tuple(t), v["lens"]); place_cyc(cyc, v["az"], t, 0.0); t1 = time.time()
    render(os.path.join(a.out, f"layout_{vn}{a.tag}.jpg"), res, a.samples, False, "JPEG", "8"); print(f"{vn} {time.time()-t1:.0f}s", flush=True)
if a.save_blend: bpy.ops.wm.save_as_mainfile(filepath=os.path.join(a.out, "layout.blend"), compress=True)
