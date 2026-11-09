# Leantech – render realistici nastri da file STEP (anteprima)

> Bozza di lavoro: le sezioni marcate **[DA COMPLETARE]** si chiudono a fine produzione.

## 1. File prodotti
**[DA COMPLETARE]** elenco finale in `output/` (renders/, web/, blender/) e `reports/`.

## 2. Decisioni prese – proposte nostre, da validare con il cliente
| # | Decisione | Default adottato | Dove cambiarla |
|---|---|---|---|
| D1 | Colori reti (il cliente ha chiesto solo che siano diversi) | Accumulo: blu (RAL 5015 circa, `#0A4F9E`); Freno/Lancio: grigio chiaro / bianco perla (`#DCDCD6`); Trasferimento: antracite (RAL 7016 circa, `#3B4044`) | `config/colors.json` oppure variabili d'ambiente |
| D2 | Colore motoriduttore (nel CAD e' rosso, colore di servizio) | Grigio-blu verniciato (RAL 7031 circa, `#3F4A52`) | `config/colors.json` → `MOTORE` |
| D3 | **Rullini folli (accumulo) e pattini in gomma (freno/lancio) NON esistono nel CAD**: la rete e' una lamiera liscia | Resi come texture procedurale: righe di rullini con passo 30 mm; pattini neri a griglia 40x62 mm, passo 60x90 mm. Disposizione e dimensioni sono **assunzioni di lavoro** | `config/colors.json` → `pattern` |
| D4 | Freccia di direzione bianca (250x375 mm, spessore 1 mm) presente sulle reti accumulo e freno | Nascosta di default (`--show-arrow` per mostrarla) | opzione `render_all.py` |
| D5 | Piano di scorrimento sotto la rete (CAD blu scuro) | Mantenuto blu scuro (visibile solo come filo ai bordi) | `PL_NAVY` |
| D6 | Strisce rosse sulle guide laterali | Plastica rossa (ruolo non determinabile con certezza) | `PL_ROSSO` |

**Nota di coerenza:** l'immagine di esempio inviata al cliente si chiamava "Brushed AISI 304 stainless steel side frame". Le specifiche cliente dicono che le **fiancate sono alluminio 6061**: i render seguono le specifiche. Alluminio = chiaro, freddo, spazzolatura morbida; inox = piu' scuro e caldo, spazzolatura piu' marcata.

## 3. Come sono stati letti i file CAD
- STEP AP214 (SolidWorks 2024), conversione con OpenCASCADE (`cascadio`), deviazione lineare 0,1 mm.
- Assi: Z lunghezza, Y verticale, X larghezza. Lunghezze verificate (teste incluse): 840 / 1506 / 6058 / 10045 mm per i nastri, 18288 mm per l'assieme.
- I nomi dei componenti sono solo codici; il file dell'assieme **non contiene i colori CAD**: sono stati ricavati dai nastri singoli via nome faccia/prodotto.
- Le rete modellate come lamiere continue: nessuna maglia modulare nel CAD.

## 4. Materiali di cui non si e' potuto determinare il ruolo con certezza
Elenco completo con confidenza in `reports/materials_map.csv` (381 righe → 225 coppie prodotto/colore). Casi incerti trattati con un default dichiarato: tamburi/rulli di ritorno (`A00000003857`, `A00000008654`), boccole senza colore (`A00000017567`), strisce rosse sulle guide, piano di scorrimento, corpi sensore.

## 5. Tempi di render (CPU 4 core, Cycles + OIDN)
**[DA COMPLETARE]** a fine produzione. Misurato finora: Full HD 96 sample ≈ 3–6 min per vista; assieme ≈ 3–6 min; master 4K **[da misurare]**.

## 6. Rigenerare tutto o un singolo nastro con altri colori
```bash
# tutto
python3 scripts/render_all.py --res 1920x1080 --samples 96
# un solo nastro con rete di altro colore
RETE_ACC='#d98a00' python3 scripts/render_all.py --only PX0000380493
```
**[DA COMPLETARE]** verificare il comando di un solo nastro sul risultato finale.

## 7. Limiti noti
- GLB web: materiali PBR senza spazzolatura procedurale; texture pattini/rullini applicata via UV planari.
- I render non mostrano dati tecnici (motori, portate, velocita'): solo cio' che e' nel CAD.
