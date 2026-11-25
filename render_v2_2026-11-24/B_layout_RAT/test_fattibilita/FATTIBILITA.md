# Lavoro B – Layout 5000 CPH con RAT 30°: stato (25/11/2026)

**RAT 30°: fatto. Layout intero: NON ancora fatto – il DWG non e' leggibile con gli strumenti disponibili.**

## File ricevuti (cartella Drive del 25/11)
| File | Esito |
|---|---|
| `Z00000005863-1elemento / 2elementi / 3elementi .STEP` (SolidWorks, 94 componenti, 1 / 2 / 3 moduli) | **Letti e usati** |
| `LAYOUT-FEDEX-5000-sfondo bianco.dwg` (AutoCAD 2018, formato AC1032, 30 MB) | **Non letto** |
| 4 WeTransfer del 23/11, screenshot `image019/020` | non presenti nella cartella |

## Perche' il DWG non e' letto
Il formato DWG e' proprietario. In questo ambiente non esiste un lettore: nessun pacchetto Python affidabile (`ezdxf` legge solo DXF, `aspose-cad` e' commerciale), nessuno strumento installabile da apt. L'unica via, compilare LibreDWG dai sorgenti, e' stata bloccata dai permessi dell'ambiente e non l'ho aggirata.
**Per sbloccare: esportare dal CAD uno di questi formati** (in ordine di preferenza): DXF (2013 o precedente), PDF vettoriale della pianta, oppure un modello 3D (STEP) del layout. Serve anche l'indicazione della zona del RAT (cornice rossa della mail del 17/11).

## RAT: cosa e' stato prodotto (`B_layout_RAT/`)
- `web_FHD/`: 9 immagini Full HD (3 configurazioni × vista 3/4, vista dall'alto, dettaglio delle ruote).
- `master_4K/`: 3 master 4K PNG a 16 bit (vista 3/4 delle tre configurazioni).
- `glb/`: 3 GLB (banco singolo 3,2 MB, doppio 7,0 MB, triplo 10,4 MB) e `viewer.html`.

## Cosa risulta dal CAD del RAT
- Elemento: circa 1134 × 383 × 256 mm; il doppio e il triplo sono 1, 2 e 3 moduli affiancati (profondita' 256 / 511 / 766 mm).
- Ogni modulo ha 3 file × 13 ruote scanalate in gomma sul piano superiore, motoriduttori e trasmissione a cinghia all'interno.
- **L'angolo di 30° NON e' visibile nel singolo elemento**: misurando la geometria, il piano di rotolamento delle ruote del campo centrale e' allineato all'asse lungo del modulo (0°); solo le ruote di estremita' sono inclinate di circa 10°, 80° e 103° (sono ruote di guida). L'angolo di deviazione di 30° dipende quindi dalla posa del modulo nel layout (cioe' dal DWG). Non lo mostro come proprieta' del modello finche' non vedo il layout.

## [ASSUNZIONI] sui materiali del RAT (il CAD non ha colori)
Piano e pannelli in inox satinato; ruote in gomma/plastica grigio scuro; cinghie in gomma nera; viteria in inox; motoriduttori nel grigio-blu dei nastri; profilo estruso in alluminio satinato. I **GLB web escludono la ferramenta interna** (cuscinetti, mozzi e supporti sotto il piano superiore: circa 3 milioni di facce non visibili dall'esterno) per tenere il peso sotto 11 MB; i render invece usano il modello completo.

## Cosa resta per il layout (dopo l'export del DWG)
1. Importare la pianta e ricostruire i tratti di nastro con i modelli STEP esistenti (sezione W=340) e posare il RAT con l'angolo reale.
2. Immagine di prova a bassa risoluzione, poi L1 (layout intero), L2 (zona del RAT) e il collegamento con L3–L5 (gia' pronti).
3. Animazione L1 → L2 → L5 e clip brevi: 1,5–2,5 h per clip Full HD, 5–8 h per l'animazione continua (misurato sul render dell'assieme).
