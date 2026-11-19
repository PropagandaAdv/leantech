# Piano tecnico – video assieme PX0000381686 (FASE 2, NON AVVIATA)

Proposta del cliente: partire da `PX0000381686_34alta_FHD`, far ruotare l'assieme di 360°; tornati alla posizione iniziale, zoom progressivo fino a `PX0000381686_34hero_4K`.
**Nessun frame e' stato renderizzato: attendo l'ok.** Si usano gli stessi materiali, luci e ciclorama dei render v2.

## 1. Percorso camera (lente fissa 35 mm, come 34alta e 34hero)
| Fase | Camera | Note |
|---|---|---|
| A. Orbita 360° | Stesso punto di partenza di `34alta`: az 62°, el 30°, distanza **20,8 m**, target al centro dell'assieme (X 0,08 / Y −3,13 / Z 0,38 m). L'azimut gira di 360° a elevazione e distanza costanti | Il frame 1 coincide con `34alta`. Accelerazione e decelerazione morbide (ease in-out) |
| B. Pausa | Fermo su `34alta` | ~1 s, per rendere leggibile il ritorno alla posizione iniziale |
| C. Zoom | Da `34alta` a `34hero`: target dal centro alla zona di giunzione, azimut 62→58°, elevazione 30→24°, distanza 20,8→5,0 m, lente invariata (35 mm) | Interpolazione della distanza in scala logaritmica per uno zoom percepito costante; ease in-out. L'ultimo frame coincide con `34hero` |

La ciclorama (fondale curvo) viene riorientata a ogni frame dietro al soggetto, come nei render singoli, quindi lo sfondo resta uniforme durante la rotazione.

## 2. Durata e frame rate (proposta)
- Totale **16 s**: orbita 10 s + pausa 1 s + zoom 5 s.
- **24 fps** → 384 frame (alternativa 30 fps → 480 frame).
- Uscita: MP4 H.264 (`yuv420p`, CRF 18), 1920×1080; stima 20–40 MB. ffmpeg e' disponibile.

## 3. Tempi di render stimati (CPU 4 core, Cycles + OIDN, nessuna GPU)
Misurato sullo stesso soggetto: `34alta` Full HD a 96 sample = **~190 s a frame**. Per un video si scende a 32 sample (con denoise) e si usa la persistenza della geometria tra i frame.

| Opzione | Frame | Tempo/frame (stima) | Totale |
|---|---|---|---|
| **Anteprima di controllo** 640×360, 12 fps, 16 s, 16 sample | 192 | 6–10 s | **~20–30 min** |
| Bozza 1280×720, 24 fps, 32 sample | 384 | 25–40 s | ~3–4 h |
| **Finale 1920×1080, 24 fps, 32 sample** | 384 | 45–75 s | **~5–8 h** |
| Finale 1920×1080, 30 fps, 32 sample | 480 | 45–75 s | ~6–10 h |
| Finale 4K | 384 | 4× | non consigliato (20+ h) |

Le stime per frame non sono misurate sul video: le confermo con 5–10 frame di prova prima di lanciare tutto.

## 4. Come lo eseguo
1. Script unico che scrive un PNG per frame (riprendibile: salta i frame esistenti, importante perche' i processi in background possono essere interrotti).
2. Anteprima a bassa risoluzione → vostra approvazione del percorso, della durata e della velocita'.
3. Render finale e montaggio con ffmpeg; consegno anche il primo e l'ultimo frame per confronto con `34alta` e `34hero`.

## 5. Da decidere (con voi)
- Durata e velocita' di rotazione (10 s per 360° e' un giro piuttosto vivace; 14–16 s e' piu' elegante ma allunga il video e i tempi).
- Senso di rotazione (oraria o antioraria).
- 24 o 30 fps; risoluzione finale (Full HD consigliata).
- Eventuale loop o dissolvenza iniziale/finale; nessun audio previsto.
- Nota: l'assieme e' lungo 18 m, quindi durante la rotazione il soggetto appare molto allungato e piccolo nel frame: e' la stessa resa di `34alta`.
