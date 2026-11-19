# CHANGELOG render v2 – feedback cliente (Leantech, serie CD)

**AGGIORNAMENTO – ambito esteso a tutte le viste.** Su indicazione ("procedi con le opzioni consigliate e rigenera tutte le viste") il profilo v2 e' ora il **default del progetto** e tutte le viste sono state rigenerate con suffisso `_v2`: 29 JPG Full HD (assieme 8, nastri 16, FTC 4 + hero derivato) e 7 master 4K, piu' i 7 GLB e i 6 render clay. Opzioni consigliate applicate: piano di scorrimento = grigio scuro del nastro grigio; nastro freno grigio uniforme senza riquadri neri; blu unico per nastro e testate. Per tornare ai materiali v1: `PROFILE=v1`. I file v1 restano in `_v1_pre-feedback/`.

Output dei tre render richiesti inizialmente (stessi nomi dei file v1 con suffisso `_v2`, cartella `output/renders/assieme/`):
- `PX0000381686_34hero_4K_v2.png` (3840×2160, 16 bit) e `..._34hero_FHD_v2.jpg` (derivato web)
- `PX0000381686_34alta_FHD_v2.jpg`
- `PX0000381686_giunzione3_FHD_v2.jpg`
- Confronti prima/dopo: `PX0000381686_34hero_4K_v2_compare.png`, `..._34alta_FHD_v2_compare.png`, `..._giunzione3_FHD_v2_compare.png` (a sinistra v1, a destra v2; per l'hero il confronto usa le versioni Full HD).

Backup di materiali e render v1: `_v1_pre-feedback/`. Inquadrature, luci, sfondo e geometrie **non sono state modificate** (stessi preset camera in `scripts/render_all.py`; stessi sample: 96).
Render eseguiti con `scripts/run_v2.sh` (profilo materiali `PROFILE=v2`).

## Regole globali
| Punto del feedback | Cosa e' stato modificato | Parametri |
|---|---|---|
| Alluminio tutto satinato | Materiale `ALU6061` (fiancate e parte esterna delle guide) reso opaco | roughness **0,30 → 0,52**, metallic 1, anisotropia 0,5 → 0,3, albedo `(0,80 0,82 0,86)` → `(0,62 0,645 0,69)` (abbassata per evitare che l'alluminio opaco appaia bianco). Resta piu' chiaro e freddo dell'inox |
| Acciaio inox tutto satinato | Materiale `INOX` (lamiere, barre) e `INOX_VITE` (viteria) | `INOX` roughness **0,40 → 0,52**, spazzolatura direzionale lungo l'asse del nastro mantenuta (bump 0,35 → 0,30); `INOX_VITE` roughness **0,25 → 0,45** |
| Motoriduttore: colore OK | **Non modificato** | `#3F4A52`, roughness 0,5 |

Le due modifiche sono nel codice di base (`scripts/scene.py`): ogni render o GLB generato da ora le usa. I render e i GLB **gia' consegnati delle altre scene sono ancora v1** (vedi "Da rifare").

## `34hero_4K`
| Punto | Modifica | Note |
|---|---|---|
| Nastro centrale (riquadri neri) → grigio come l'adiacente | Il materiale `RETE_FRE` e' sostituito dallo **stesso identico materiale** `RETE_STD` (antracite `#3B4044`, roughness 0,5), non una copia | Per questo i **riquadri neri dei pattini non compaiono piu'**. Vedi dubbio D2 |
| Colore dell'altro nastro (blu) OK | Tinta invariata `#0A4F9E` | Cambia solo la finitura piatta (vedi sotto) |
| Alluminio opaco, acciaio satinato | Regole globali | — |

## `34alta_FHD`
| Punto | Modifica | Note |
|---|---|---|
| Stesse note dell'hero per tutti i nastri | Nastro freno grigio, alluminio e inox satinati | Come sopra |
| Blu uniforme, un unico elemento | Nastro blu (`RETE_ACC`) e testate azzurre delle guide (`PL_BLU`) usano **un solo materiale `BLU_UNICO`**: tinta `#0A4F9E`, roughness 0,6, nessun subsurface, nessun bump e nessuna texture/gradiente | Prima le testate erano `#0A6BC4` (piu' chiare) e il nastro `#0A4F9E` con modulazione. Il filo blu navy del piano di scorrimento (`PL_NAVY`) **non** e' incluso: vedi dubbio D3 |

## `giunzione3_FHD`
| Punto | Modifica | Come |
|---|---|---|
| Guide laterali bicolore | **Parte interna** (verso il nastro): grigio scuro, materiale `RETE_STD`. **Parte esterna**: alluminio satinato, stesso materiale delle fiancate | Nessuna geometria spezzata: le guide hanno gia' nel CAD due gruppi di facce con colori diversi (488 facce grigie sul lato interno, |X| 130–142 mm; 1944 facce in alluminio su quello esterno). Il codice le mappava tutte su alluminio; ora il gruppo grigio e' una famiglia a parte `GUIDA_INT` (regola in `scripts/materials_rules.py`) con un secondo slot materiale. Nel file dell'assieme, privo di colori CAD, il gruppo e' riconosciuto dai nomi delle facce |
| Nastro blu senza chiaroscuro | Tolta la modulazione di colore e il rilievo delle stecche (prima: bump 0,55 e rampa di colore); un solo materiale piatto, roughness 0,6 uniforme | Nessun cambio di luci. Le righe dei rullini non si vedono piu'; erano comunque una resa indicativa non presente nel CAD |

## Dubbi e punti non risolti (da confermare)
- **D1 – "Piano di scorrimento" della guida.** Nel mio modello il piano di scorrimento (`PL_NAVY`) e' blu navy e si vede solo come filo ai bordi della rete: non e' grigio scuro. Ho quindi riusato per la parte interna delle guide il **grigio scuro gia' presente nella scena** (antracite `RETE_STD`). Se il cliente intendeva un altro materiale (ad es. le strisce grigie `PL_GRIGIO`, `#9A9C9E`, piu' chiare), cambio una riga e rifaccio la sola giunzione (~6 min).
- **D2 – Riquadri neri del nastro freno.** Applicando "esattamente lo stesso materiale" del nastro grigio, i riquadri neri spariscono. Se vanno mantenuti, si puo' tenere il pattern sulla base grigia (il nastro non sarebbe piu' identico).
- **D3 – Filo blu navy.** Il filo ai bordi della rete (piano di scorrimento) resta blu navy, quindi nel 34alta e nella giunzione e' l'unica parte blu con una tinta diversa. Se va unificato col blu del nastro, o reso grigio come la guida, va deciso insieme a D1.
- **D4 – Alluminio chiaro.** Satinato, l'alluminio delle fiancate risulta molto chiaro (quasi bianco opaco) nelle viste in luce piena. Si puo' scurire ancora l'albedo senza toccare le luci.
- **Ambito.** Risolto: profilo v2 esteso a tutto il progetto (vedi in cima).
- **D5 – Conseguenze dell'estensione.** (a) Nei render del **nastro freno singolo** il nastro e' ora identico al nastro di trasferimento (grigio uniforme, senza pattini): le due versioni si distinguono solo dalla struttura. (b) Nel nastro accumulo **le righe dei rullini non si vedono piu'**: nei primi piani il blu e' piatto, con una lieve sfumatura morbida dovuta alla luce dello studio e appare piu' chiaro della tinta impostata (`#0A4F9E`). (c) La piastra inox satinata dei gruppi FTC risulta molto chiara nei dettagli in luce piena.

## Cosa resta fuori
- I GLB v2 (assieme 12,0 MB, nastri 6,3–7,2 MB) usano materiali PBR semplici: colori piatti, nessuna texture di rullini o pattini e nessuna spazzolatura procedurale.
- Il video (Fase 2) non e' avviato: solo piano tecnico in `reports/PIANO_VIDEO_fase2.md`.
- Versioni con sfondo trasparente non prodotte.
