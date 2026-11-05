"""GLB per-faccia -> npz compatto: vertici mondo (m), normali, facce, prodotto e colore CAD per faccia."""
import sys, re, glob, time, numpy as np, trimesh
codes = sys.argv[1:] or [re.search(r"(PX\d+)", p).group(1) for p in sorted(glob.glob("work/PX*.glb"))]
for code in codes:
    t = time.time()
    s = trimesh.load(f"work/{code}.glb", process=False)
    prods, cols, gnames = {}, {}, {}
    V, N, F, FP, FC, FG = [], [], [], [], [], []
    off = 0
    gcache = {}
    for node in s.graph.nodes_geometry:
        T, gname = s.graph[node]
        g = s.geometry[gname]
        if gname not in gcache:
            m = getattr(g.visual, "material", None)
            c = tuple(int(x) for x in m.baseColorFactor[:3]) if m is not None and getattr(m, "baseColorFactor", None) is not None else (-1, -1, -1)
            base = re.sub(r"_\d+$", "", gname)
            gcache[gname] = (np.asarray(g.vertices, np.float64), np.asarray(g.vertex_normals, np.float64), np.asarray(g.faces, np.int32),
                             prods.setdefault(base, len(prods)), cols.setdefault(c, len(cols)), gnames.setdefault(gname, len(gnames)))
        v, n, f, pi, ci, gi = gcache[gname]
        R = T[:3, :3]
        V.append(((v @ R.T) + T[:3, 3]).astype(np.float32)); N.append((n @ R.T).astype(np.float32))
        F.append(f + off); FP.append(np.full(len(f), pi, np.int32)); FC.append(np.full(len(f), ci, np.int16)); FG.append(np.full(len(f), gi, np.int32)); off += len(v)
    np.savez_compressed(f"work/{code}.npz", V=np.concatenate(V), N=np.concatenate(N), F=np.concatenate(F),
                        FP=np.concatenate(FP), FC=np.concatenate(FC), FG=np.concatenate(FG), gnames=np.array(list(gnames)),
                        prods=np.array(list(prods)), cols=np.array(list(cols), np.int16))
    print(code, f"{time.time()-t:.0f}s", len(prods), "prodotti", off, "vertici", flush=True)
