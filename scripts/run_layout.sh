#!/bin/bash
# Layout schematico + colli: Full HD (L1,L2,L6), master 4K (L1,L2), GLB (RAT a tessellazione web). Riprendibile per fase.
cd "$(dirname "$0")/.."
B=render_v2_2026-11-24/B_layout_RAT
[ -f $B/web_FHD/layout_L6_FHD.jpg ] || python3 -I scripts/layout_build.py --views L1,L2,L6 --res 1920x1080 --samples 96 --out $B/web_FHD
[ -f $B/master_4K/layout_L1_4K.png ] || python3 -I scripts/layout_build.py --views L1 --res 3840x2160 --samples 64 --masters --out $B/master_4K
[ -f $B/master_4K/layout_L2_4K.png ] || python3 -I scripts/layout_build.py --views L2 --res 3840x2160 --samples 96 --masters --out $B/master_4K
mkdir -p $B/glb; [ -f $B/glb/Layout_5000CPH_schematico.glb ] || LAYRAT=Zw3elementi python3 -I scripts/layout_build.py --views L1 --res 320x180 --samples 1 --out work/lay_glbtmp --glb $B/glb/Layout_5000CPH_schematico.glb
echo LAYOUT_DONE
