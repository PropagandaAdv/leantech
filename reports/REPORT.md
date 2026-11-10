# Leantech – render realistici nastri da file STEP (anteprima)

Stato: **consegna completa** per quanto previsto dal brief, tranne le versioni con sfondo trasparente e il turntable (vedi §7).
Sono anteprime generate dal CAD: i nastri reali sono in produzione.

## 1. File prodotti
| Cartella | Contenuto |
|---|---|
| `output/renders/assieme/` | `PX0000381686_*`: 34alta, 34bassa, laterale, alto (formato 4:1), 3 giunzioni, **34hero** (4K + FHD) |
| `output/renders/nastri/` | per ciascuno dei 4 nastri: 3/4 (**master 4K** + FHD), laterale, testata, rete; per L=10000 anche **fuga** |
| `output/renders/ftc/` | `PX0000381771_*`, `PX0000381774_*`: 3/4 (**master 4K** + FHD) e dettaglio |
| `output/renders/clay/` | 6 render clay per famiglia di materiale (controllo assegnazione) + `LEGENDA.txt` |
| `output/web/` | 7 GLB (Draco) + `viewer.html` (`<model-viewer>`) |
| `output/blender/` | 7 file `.blend` sorgente, uno per scena |
| `reports/` | `*_struttura.json`, `materials_map.csv`, questo report |

Totale: **7 master 4K** (3840×2160, PNG 16 bit, ~22 MB l'uno) e **29 JPG Full HD** (1920×1080; l'assieme laterale/alto sono 1920×480).
Naming: `<codice>_<vista>_<4K|FHD>.<png|jpg>`.

### GLB per il sito
| File | Peso | Triangoli | Obiettivo |
|---|---|---|---|
| `PX0000381686.glb` assieme | 12,0 MB | ~615k | < 15 MB ✔ |
| `PX0000380493.glb` accumulo | 7,3 MB | ~352k | < 8 MB ✔ |
| `PX0000381687.glb` freno/lancio | 6,4 MB | ~351k | < 8 MB ✔ |
| `PX0000381735.glb` trasferimento 750 | 6,4 MB | ~350k | < 8 MB ✔ |
| `PX0000381782.glb` trasferimento 10000 | 6,3 MB | ~361k | < 8 MB ✔ |
| `PX0000381771.glb` / `PX0000381774.glb` FTC | 0,8 / 0,9 MB | ~45k / ~49k | — |

Prova eseguita in Chromium (Playwright) tramite `viewer.html`: tutti i modelli si caricano senza errori, in **1,6–3,7 s in locale** (con rete reale i tempi dipendono dalla banda). Nel GLB i materiali sono PBR semplici: **la spazzolatura procedurale dei render non e' presente**; la texture di pattini e rullini e' applicata con UV planari.

## 2. Decisioni prese – proposte nostre da validare con il cliente
| # | Decisione | Default adottato | Dove cambiarla |
|---|---|---|---|
| D1 | Colori reti (il cliente ha chiesto solo che siano diversi) | Accumulo: blu (RAL 5015 circa, `#0A4F9E`, scelto piu' saturo perche' il rendering lo schiarisce); Freno/Lancio: grigio chiaro / bianco perla (`#DCDCD6`); Trasferimento: antracite (RAL 7016 circa, `#3B4044`) | `config/colors.json` o variabili d'ambiente |
| D2 | Colore motoriduttore (nel CAD e' rosso, colore di servizio) | Grigio-blu verniciato (RAL 7031 circa, `#3F4A52`) | `config/colors.json` → `MOTORE` |
| D3 | **Rullini folli (accumulo) e pattini in gomma (freno/lancio) NON esistono nel CAD**: la rete e' una lamiera liscia | Texture procedurale: righe di rullini con passo 30 mm; pattini neri a griglia 40×62 mm, passo 60×90 mm. **Disposizione e dimensioni sono assunzioni di lavoro** | `config/colors.json` → `pattern` |
| D4 | Freccia di direzione bianca (250×375 mm, 1 mm) sulle reti accumulo e freno | Nascosta (`--show-arrow` per mostrarla) | `render_all.py` |
| D5 | Piano di scorrimento sotto la rete (CAD blu scuro) | Mantenuto blu scuro; visibile solo come filo ai bordi | `PL_NAVY` |
| D6 | Strisce rosse sulle guide laterali | Plastica rossa (ruolo non determinabile con certezza) | `PL_ROSSO` |

**Coerenza con le specifiche:** l'immagine di esempio inviata al cliente si chiamava "Brushed AISI 304 stainless steel side frame", ma le specifiche dicono che le **fiancate sono in alluminio 6061**: i render seguono le specifiche. Alluminio = chiaro e freddo, spazzolatura morbida; inox = piu' scuro e caldo, spazzolatura piu' marcata. Le due famiglie sono distinguibili a colpo d'occhio.

## 3. Come sono stati letti i file CAD
- STEP AP214 (SolidWorks 2024), conversione OpenCASCADE (`cascadio`), deviazione lineare 0,1 mm, normali per faccia, bevel shader 0,4 mm sui metalli e sulle plastiche.
- Assi: Z lunghezza, Y verticale, X larghezza. Lunghezze verificate (teste incluse): 840 / 1506 / 6058 / 10045 mm per i nastri; 18288 mm l'assieme. Larghezza rete 340 mm confermata.
- I nomi dei componenti sono codici; il file dell'**assieme non contiene i colori CAD**, ricavati dai nastri singoli via nome faccia/prodotto.
- Le reti sono modellate come lamiere continue: nessuna maglia modulare nel CAD.

## 4. Componenti con materiale non determinabile con certezza
Elenco completo in `reports/materials_map.csv` (225 coppie prodotto/colore: 26 a confidenza alta, 183 media, 16 bassa). Casi incerti, con il trattamento adottato:
- **Supporti bianchi dei gruppi FTC** (`A00000017420`, `D00000121538`, `D00000086722`): colore CAD bianco, ruolo non chiaro → trattati come minuteria inox. Un tentativo di renderli in plastica e' stato scartato perche' coinvolgeva anche lamiere.
- Tamburi/rulli di ritorno (`A00000003857`, `A00000008654`), boccole senza colore (`A00000017567`): default inox / plastica scura.
- Strisce rosse sulle guide, piano di scorrimento blu, corpi sensore (verde/nero): colori da CAD.
- Lenti delle fotocellule: non individuate come parti separate, quindi **non** rese trasparenti.

## 5. Tempi di render (CPU 4 core, Cycles + OpenImageDenoise)
| Tipo | Tempo misurato |
|---|---|
| Full HD, 96 sample | 77–376 s a vista (media ~260 s) |
| Master 4K, 96 sample | 12–20 min: nastri ~14–15, FTC ~12,5, assieme ~19 |
| Export GLB | 1–72 s per modello |

Produzione complessiva: circa 8 ore di calcolo effettivo, ripartite su piu' sessioni (i processi in background non sopravvivono ai riavvii del contenitore; la coda salta quanto gia' prodotto).

## 6. Rigenerare tutto o un singolo nastro con altri colori
```bash
# tutto, Full HD
FORCE=1 python3 scripts/render_all.py --res 1920x1080 --samples 96
# un solo nastro con rete di altro colore (es. accumulo arancio)
FORCE=1 RETE_ACC='#d98a00' python3 scripts/render_all.py --only PX0000380493
# master 4K di una vista
FORCE=1 python3 scripts/render_all.py --only PX0000380493 --views 34 --res 3840x2160 --samples 96 --masters
# GLB di un nastro con lo stesso colore
RETE_ACC='#d98a00' python3 scripts/08_export_glb.py PX0000380493 350000
```
Senza `FORCE=1` gli script saltano le immagini gia' presenti. Variabili colore: `RETE_ACC`, `RETE_FRE`, `RETE_STD`, `MOTORE` (hex).

## 7. Non fatto / limiti
- **Versioni con sfondo trasparente**: non prodotte (opzione `--transparent` disponibile, un render in piu' per vista).
- **Turntable MP4** (opzionale nel brief): non realizzato.
- Vista laterale e dall'alto dell'assieme: 18 m in un solo frame restano poco leggibili; le inquadrature utili sono hero e giunzioni.
- Le reti standard (antracite) in primo piano risultano uniformi: nel CAD non c'e' alcun dettaglio sulla superficie, a parte due linee sottili.
- I render non mostrano dati tecnici (motori, portate, velocita'): solo quanto e' nel CAD.
