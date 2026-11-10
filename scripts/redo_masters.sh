#!/bin/bash
cd "$(dirname "$0")/.."
export FORCE=1
for c in PX0000380493 PX0000381771 PX0000381774; do python3 -I scripts/render_all.py --out output --only $c --views 34 --res 3840x2160 --samples 96 --masters; done
echo REDO_DONE
