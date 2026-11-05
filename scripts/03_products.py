"""Tabella prodotti (nome geometria senza indice) -> conteggi/dimensioni/colori, su tutti i file."""
import json, re, glob, collections, csv
prod = collections.defaultdict(lambda: dict(files=set(), n=0, faces=0, sizes=[], colors=collections.Counter()))
for p in sorted(glob.glob("reports/PX*_struttura.json")):
    code = re.search(r"(PX\d+)", p).group(1)
    for i in json.load(open(p))["items"]:
        base = re.sub(r"_\d+$", "", i["geom"])
        e = prod[base]; e["files"].add(code); e["n"] += 1; e["faces"] += i["faces"]
        e["sizes"].append(tuple(i["size"])); e["colors"][str(i["color"])] += 1
rows = []
for k, e in prod.items():
    mx = max(e["sizes"], key=lambda s: max(s))
    rows.append([k, len(e["files"]), e["n"], e["faces"], "x".join(f"{v:.0f}" for v in sorted(mx, reverse=True)), e["colors"].most_common(1)[0][0]])
rows.sort(key=lambda r: -r[3])
with open("work/products.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["product","nfiles","ninst","faces","maxsize_mm","color"]); w.writerows(rows)
print(len(rows), "prodotti")
for r in rows: print(f"{r[0][:42]:42s} f{r[1]} n{r[2]:5d} fc{r[3]:7d} {r[4]:16s} {r[5]}")
