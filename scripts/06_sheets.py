import json, glob, re, numpy as np
from PIL import Image, ImageDraw, ImageFont
meta = {}
for f in sorted(glob.glob("work/thumbs_meta_*.json")): meta.update(json.load(open(f)))
# colore CAD dominante per prodotto
colr = {}
for code in sorted({m["file"] for m in meta.values()}):
    d = np.load(f"work/{code}.npz"); FP, FC, prods, cols = d["FP"], d["FC"], d["prods"], d["cols"]
    for pi, name in enumerate(prods):
        key = re.sub(r"[^A-Za-z0-9=_.-]", "_", name)
        if key in meta and meta[key]["file"] == code:
            m = FP == pi; c = np.bincount(FC[m], minlength=len(cols)).argmax(); meta[key]["cad"] = [int(x) for x in cols[c]]; meta[key]["ncol"] = int(len(np.unique(FC[m])))
items = sorted(meta.items(), key=lambda kv: -kv[1]["faces"])
json.dump(dict(items), open("work/products_meta.json", "w"), indent=1)
W, H, cols_, rows_ = 384, 216, 5, 4
per = cols_ * rows_
font = ImageFont.load_default(size=13)
for s in range(0, len(items), per):
    sheet = Image.new("RGB", (W * cols_, (H + 34) * rows_), "white"); dr = ImageDraw.Draw(sheet)
    for i, (key, m) in enumerate(items[s:s + per]):
        x, y = (i % cols_) * W, (i // cols_) * (H + 34)
        sheet.paste(Image.open(f"work/thumbs/{key}.png").convert("RGB").resize((W, H)), (x, y))
        dr.rectangle([x, y + H, x + W, y + H + 34], fill=(25, 25, 25))
        dr.text((x + 4, y + H + 2), f"{m['name'][:40]}", fill="white", font=font)
        dr.text((x + 4, y + H + 18), f"f{m['faces']} {'x'.join(str(int(v)) for v in m['size_mm'])}mm cad{tuple(m.get('cad',[]))}", fill=(255, 220, 120), font=font)
        c = m.get("cad", [128, 128, 128]); dr.rectangle([x + W - 24, y + H + 6, x + W - 6, y + H + 24], fill=tuple(max(0, v) for v in c))
    sheet.save(f"work/sheet_{s // per:02d}.png")
print(len(items), "prodotti,", (len(items) + per - 1) // per, "sheet")
