"""Famiglia materiale per faccia. L'assieme (PX0000381686) non ha colori CAD: si ricavano dai nastri singoli via nome faccia/prodotto."""
import glob, re, collections, numpy as np
from materials_rules import classify
ASSEMBLY = "PX0000381686"

def _load(code):
    d = np.load(f"work/{code}.npz"); return {k: d[k] for k in d.files}

_lookup = None
def lookup():
    global _lookup
    if _lookup: return _lookup
    geom, prod = {}, collections.defaultdict(collections.Counter)
    for p in sorted(glob.glob("work/PX*.npz")):
        code = re.search(r"(PX\d+)", p).group(1)
        if code == ASSEMBLY: continue
        d = _load(code); u, idx = np.unique(d["FG"], return_index=True)
        for g, i in zip(u, idx):
            c = tuple(int(x) for x in d["cols"][d["FC"][i]]); geom[str(d["gnames"][g])] = c
            prod[str(d["prods"][d["FP"][i]])][c] += 1
    _lookup = (geom, prod); return _lookup

def face_families(code, d=None):
    """-> (famiglie[list], fam_id per faccia[int array], colore CAD risolto per faccia[(n,3)])"""
    d = d or _load(code); geom, prod = lookup()
    cols = d["cols"]; FC, FG, FP = d["FC"], d["FG"], d["FP"]
    if code == ASSEMBLY:
        gcol = np.zeros((len(d["gnames"]), 3), np.int16)
        for gi, gn in enumerate(d["gnames"]):
            gn = str(gn); c = geom.get(gn)
            if c is None:
                base = re.sub(r"_\d+$", "", gn); pc = prod.get(base)
                c = pc.most_common(1)[0][0] if pc else (-1, -1, -1)
            gcol[gi] = c
        fcol = gcol[FG]
    else:
        fcol = cols[FC].astype(np.int16)
    key = (FP.astype(np.int64) * 16777216 + (fcol[:, 0].astype(np.int64) + 1) * 65536 + (fcol[:, 1].astype(np.int64) + 1) * 256 + (fcol[:, 2].astype(np.int64) + 1))
    u, inv = np.unique(key, return_inverse=True)
    fams = {}; ufam = np.zeros(len(u), np.int32)
    first = np.zeros(len(u), np.int64); first[inv[::-1]] = np.arange(len(inv))[::-1]
    for k in range(len(u)):
        i = first[k]; f = classify(str(d["prods"][FP[i]]), tuple(int(x) for x in fcol[i]))[0]
        ufam[k] = fams.setdefault(f, len(fams))
    return list(fams), ufam[inv], fcol
