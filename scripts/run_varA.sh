#!/bin/bash
# Viste che mostrano il nastro freno/lancio, variante a (grigio + pattini neri). File *_v2_varA. Riprendibile.
cd "$(dirname "$0")/.."
export PROFILE=v2 FRENO_VARIANT=a
P="python3 -I scripts/render_all.py --out output --suffix _v2_varA --samples 96"
$P --only PX0000381687 --skip 34 --res 1920x1080
$P --only PX0000381686 --views 34alta,34bassa,laterale,alto,giunzione1,giunzione2 --res 1920x1080
$P --only PX0000381687 --views 34 --res 3840x2160 --masters
$P --only PX0000381686 --views 34hero --res 3840x2160 --masters
echo VARA_DONE
