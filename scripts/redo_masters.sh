#!/bin/bash
# Rifacimento mirato dopo correzione materiali (FORCE=1 ignora i file gia' presenti)
cd "$(dirname "$0")/.."
export FORCE=1
P="python3 -I scripts/render_all.py --out output"
for c in PX0000381771 PX0000381774; do $P --only $c --views dettaglio --res 1920x1080 --samples 96; done
for c in PX0000380493 PX0000381771 PX0000381774; do $P --only $c --views 34 --res 3840x2160 --samples 96 --masters; done
$P --only PX0000381686 --views giunzione1,giunzione2,giunzione3 --res 1920x1080 --samples 96
echo REDO_DONE
