#!/bin/bash
# Render v2 (feedback cliente): stessi nomi con suffisso _v2. Profilo materiali PROFILE=v2 (solo assieme).
cd "$(dirname "$0")/.."
export PROFILE=v2 FORCE=1
P="python3 -I scripts/render_all.py --only PX0000381686 --out output --suffix _v2 --samples 96"
$P --views giunzione3 --res 1920x1080
$P --views 34alta --res 1920x1080
$P --views 34hero --res 3840x2160 --masters
echo V2_DONE
