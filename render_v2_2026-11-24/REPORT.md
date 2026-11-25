# Leantech – Report render v2 (24/11/2026)

Cartella di consegna: `render_v2_2026-11-24/`. I file consegnati il 10/11 non sono stati toccati (copia integrale in `_v1_pre-feedback/`).

## 1. Fatto
**Lavoro A – revisione render nastri serie CD: completato, video incluso (vedi §6).**
**Lavoro B – layout 5000 CPH con RAT 30°: NON eseguito, mancano i file indispensabili (vedi §5).**

| Cosa | Dove |
|---|---|
| 7 master 4K, PNG 16 bit (assieme hero, 4 nastri, 2 FTC) | `A_nastri/master_4K/` |
| 29 JPG Full HD (assieme 8, nastri 16, FTC 4, hero web) | `A_nastri/web_FHD/` |
| Varianti freno/lancio **a** (grigio + pattini neri) e **b** (grigio uniforme), per tutte le viste in cui il freno e' visibile (13 coppie, 4K per hero e freno) | `A_nastri/varianti_freno-lancio/` |
| 7 GLB (assieme 12,0 MB; nastri 6,3–7,2 MB; FTC < 1 MB) + `viewer.html`; GLB di assieme e freno anche in variante b | `A_nastri/glb/` |
| Confronti v1 / v2 affiancati: 34hero, 34alta, giunzione3 + un nastro per ciascuno dei 4 | `confronto_v1_v2/` |
| Video assieme (rotazione 360° + zoom) | `A_nastri/video/` |
| Nota di fattibilita' del layout | `B_layout_RAT/test_fattibilita/FATTIBILITA.md` |

Nomi: gli stessi della v1 con suffisso `_v2` (varianti: `_varA…` / `_varB…`). Il set principale usa la **variante a** per il freno.

## 2. Modifiche applicate (una riga per feedback)
| Feedback del cliente | Applicato | Dove |
|---|---|---|
| Alluminio opaco | `ALU6061`: roughness 0,30 → 0,52, anisotropia ridotta, albedo scurita per non farlo apparire bianco | tutti i render e i GLB |
| Inox satinato | `INOX` roughness 0,40 → 0,52 con spazzolatura direzionale; viteria `INOX_VITE` 0,25 → 0,45 | tutti i render e i GLB |
| Guide laterali in due colori | Faccia verso il nastro: grigio scuro = materiale del nastro grigio; faccia esterna: alluminio satinato. Nessuna geometria spezzata: il CAD ha gia' due gruppi di facce (488 + 1944) separati per colore | tutte le scene con guide |
| Blu accumulo uniforme | Nastro e testate azzurre usano un solo materiale (`#0A4F9E`, roughness 0,6, nessun bump, nessuna texture, nessun subsurface) | tutte le scene con accumulo |
| Freno/lancio grigio come nastro approvato | Variante a: base grigia identica al nastro approvato (`#3B4044`) con pattini neri. Variante b: stesso identico materiale del nastro grigio, senza pattini | vedi varianti |
| Nastro trasferimento e motoriduttore approvati | **Non modificati** (stessi parametri della v1) | — |

## 3. Assunzioni `[ASSUNZIONE]`
1. **Interno delle guide.** Nel mio modello il "piano di scorrimento" e' blu navy (visibile solo come filo ai bordi della rete), non grigio scuro. Per rispettare "grigio scuro" ho usato il grigio scuro del nastro grigio. Il piano di scorrimento in se' e' rimasto come nella v1, come da istruzioni.
2. **Rullini folli.** Il feedback chiede un blu uniforme senza bande tra i moduli: la texture indicativa a righe della v1 produce proprio quelle bande, quindi nei render v2 l'accumulo ha **blu piatto, senza rullini visibili**. Se il cliente vuole vederli, va deciso come compromesso (ad es. rilievo appena accennato).
3. **Pattini del freno (variante a)**: disposizione a griglia, 40×62 mm con passo 60×90 mm, scelta mia; il CAD non li contiene.
4. **Video**: 25 fps, 14 s (orbita 9 s, pausa 1 s, zoom 4 s), rotazione ottenuta girando camera, luci e fondale insieme (effetto piatto girevole), 16 sample con denoise. La camera si allontana fino a 25,6 m quando l'assieme e' visto di testa, per non tagliarlo, e torna a 20,8 m al ritorno nella posizione di partenza. Il frame 1 coincide con `34alta`, l'ultimo con `34hero`.
5. **Supporti bianchi FTC, strisce rosse delle guide, piano di scorrimento, colore del motoriduttore**: default della v1 (senza risposta del cliente).
6. **Reti**: i colori restano la proposta di Propaganda (blu RAL 5015 circa, antracite RAL 7016 circa).

## 4. Punti da confermare con il cliente
- **Freno/lancio: variante a o b?** (set principale = a.)
- Quote o modello reale di **rullini folli** e **pattini in gomma**; e se i rullini vanno visibili sull'accumulo nonostante il blu uniforme.
- Materiale dei **supporti bianchi FTC**, delle **strisce rosse** sulle guide e del **piano di scorrimento** (e se l'interno delle guide va bene cosi').
- Layout: parti ricostruite e semplificate accettabili per il sito? (da valutare quando avremo i file, vedi §5).

## 5. Esito della fattibilita' del layout (lavoro B)
**Bloccato.** Non ho ricevuto: il DWG del layout 5000 CPH, il 3D del RAT 30° nelle tre configurazioni, i 4 WeTransfer del 23/11, gli screenshot `image019/020`. Ho cercato nel repository, in `input/`, nella cartella Drive condivisa (contiene solo gli 8 file dei nastri), negli allegati della sessione e nell'intero filesystem.
Non ricostruisco il layout e soprattutto il RAT (brevettato) senza il loro modello: sarebbe una geometria inventata. Dettagli, elenco dei file richiesti, piano di lavoro e tempi in `B_layout_RAT/test_fattibilita/FATTIBILITA.md`.

## 6. Video dell'assieme (`A_nastri/video/`)
| File | Specifiche |
|---|---|
| `PX0000381686_rotazione360_zoom_v2.mp4` | 1920×1080, 25 fps, **14,0 s** (350 frame), H.264 `-preset veryfast` CRF 20, 3,0 MB |
| `PX0000381686_rotazione360_zoom_v2_web.mp4` | versione web 1280×720, CRF 26, `faststart`, 0,5 MB |
| `..._loop-andata-ritorno_web.mp4` | versione "loop" 1280×720, 28 s: il video in avanti e poi al contrario (andata e ritorno), 1,0 MB |
| `..._poster.jpg` | primo frame |

**Sequenza:** parte da `34alta`; rotazione completa di 360° in 9 s (ease in/out); pausa di 1 s nella posizione iniziale; zoom in 4 s (ease in/out, distanza 20,8 → 5,0 m a lente fissa 35 mm) fino a `34hero`. Nessun audio. Materiali v2, **freno in variante a**.
**Render:** 16 sample con denoise, circa 50 s a frame, **4,9 ore** di calcolo totali.
**Verifiche eseguite sul video:** il frame 249 (fine giro) e' identico al frame 0 (differenza media 0,0); il frame 1 coincide con `34alta` e l'ultimo con `34hero` (differenza media ~2 su 255, dovuta a rumore e compressione); nessuno scatto tra frame consecutivi (nessun picco rispetto alla media locale); la camera si allontana a 25,6 m quando l'assieme e' visto di testa per non tagliarlo.
**Limiti:** un loop continuo vero non e' possibile, perche' il video finisce sull'hero e non sulla partenza: la versione "andata e ritorno" fa girare l'assieme anche al contrario nella seconda meta'; se serve un altro tipo di loop (ad es. solo l'orbita) si ricava dai frame gia' renderizzati. L'assieme e' lungo 18 m e durante la rotazione appare piccolo nel frame (stesso effetto di `34alta`).

## 7. Verifica eseguita
- Tutte le 29 immagini principali riviste su contact sheet, piu' i confronti v1/v2: alluminio opaco, inox satinato, guide bicolore, blu uniforme, freno grigio, motore e trasferimento invariati.
- GLB: caricati nel viewer in Chromium, tutti senza errori (1,7–5 s con la CPU occupata dal render).
- Video: vedi §6. Nei dettagli FTC la piastra inox satinata risulta molto chiara in luce piena (non corretto).
- Repository: i PNG 4K e gli zip non sono nel branch (si rigenerano dagli stessi file della cartella di consegna).
- Non verificato: contenuto dei WeTransfer, layout e RAT (file assenti).
