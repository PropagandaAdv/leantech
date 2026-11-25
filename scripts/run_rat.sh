#!/bin/bash
# Render RAT 30 gradi: 3 configurazioni. FHD (3 viste) poi master 4K (vista 3/4). Riprendibile a livello di configurazione/vista.
cd "$(dirname "$0")/.."
for c in Z1elemento Z2elementi Z3elementi; do python3 -I scripts/rat_render.py $c --res 1920x1080 --samples 96; done
for c in Z1elemento Z2elementi Z3elementi; do python3 -I scripts/rat_render.py $c --views 34 --res 3840x2160 --samples 96 --masters --out render_v2_2026-11-24/B_layout_RAT/master_4K; done
echo RAT_DONE
