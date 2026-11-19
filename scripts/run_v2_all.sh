#!/bin/bash
# Rigenera TUTTE le viste con il profilo v2 (feedback cliente). File *_v2; i file gia' presenti vengono saltati (riprendibile).
cd "$(dirname "$0")/.."
P="python3 -I scripts/render_all.py --out output --suffix _v2 --samples 96 --save-blend"
$P --only PX0000381686 --skip 34hero,34alta,giunzione3 --res 1920x1080
for c in PX0000380493 PX0000381687 PX0000381735 PX0000381782 PX0000381771 PX0000381774; do $P --only $c --skip 34 --res 1920x1080; done
for c in PX0000380493 PX0000381687 PX0000381735 PX0000381782 PX0000381771 PX0000381774; do $P --only $c --views 34 --res 3840x2160 --masters; done
echo V2ALL_DONE
