#!/bin/bash
# Coda produzione: master 4K (PNG 16 bit + JPG web derivato) poi viste restanti Full HD.
cd "$(dirname "$0")/.."
P="python3 -I scripts/render_all.py --out output"
$P --only PX0000381686 --views 34hero --res 3840x2160 --samples 96 --masters
for c in PX0000380493 PX0000381687 PX0000381735 PX0000381782; do $P --only $c --views 34 --res 3840x2160 --samples 96 --masters; done
for c in PX0000381771 PX0000381774; do $P --only $c --views 34 --res 3840x2160 --samples 96 --masters; done
$P --only PX0000381686 --skip 34hero --res 1920x1080 --samples 96 --save-blend
for c in PX0000380493 PX0000381687 PX0000381735 PX0000381782 PX0000381771 PX0000381774; do $P --only $c --skip 34 --res 1920x1080 --samples 96 --save-blend; done
echo QUEUE_DONE
