#!/bin/bash
# Animazioni layout/RAT: 1 continua (13 s) + 3 clip (3 s). Riprendibile (frame esistenti saltati). Output: B_layout_RAT/video/
cd "$(dirname "$0")/.."
export PROFILE=v2 FRENO_VARIANT=a
V=render_v2_2026-11-24/B_layout_RAT/video; mkdir -p $V
enc() {  # dir nome
  n=$(ls $1/frame_*.jpg 2>/dev/null | wc -l); [ "$n" -ge "$3" ] || return
  ffmpeg -y -loglevel error -framerate 25 -i $1/frame_%04d.jpg -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -movflags +faststart $V/$2.mp4
  ffmpeg -y -loglevel error -framerate 25 -i $1/frame_%04d.jpg -vf scale=1280:720 -c:v libx264 -preset veryfast -crf 26 -pix_fmt yuv420p -movflags +faststart $V/$2_web.mp4
}
python3 -I scripts/layout_anim.py --dir work/anim_main --samples 12; enc work/anim_main Layout_L1-L2-L5_animazione 325; echo MAIN_DONE
for c in Z1elemento Z2elementi Z3elementi; do python3 -I scripts/rat_anim.py $c --samples 12 --dir work/anim_$c; enc work/anim_$c RAT_clip_${c} 75; echo CLIP_${c}_DONE; done
echo ANIM_DONE
