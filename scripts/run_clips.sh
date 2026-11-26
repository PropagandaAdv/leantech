#!/bin/bash
cd "$(dirname "$0")/.."; export PROFILE=v2 FRENO_VARIANT=a
V=render_v2_2026-11-24/B_layout_RAT/video; mkdir -p $V
for c in Z1elemento Z2elementi Z3elementi; do
  python3 -I scripts/rat_anim.py $c --samples 12 --dir work/anim_$c
  n=$(ls work/anim_$c/frame_*.jpg | wc -l)
  if [ "$n" -ge 75 ]; then
    ffmpeg -y -loglevel error -framerate 25 -i work/anim_$c/frame_%04d.jpg -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -movflags +faststart $V/RAT_clip_$c.mp4
    ffmpeg -y -loglevel error -framerate 25 -i work/anim_$c/frame_%04d.jpg -vf scale=1280:720 -c:v libx264 -preset veryfast -crf 26 -pix_fmt yuv420p -movflags +faststart $V/RAT_clip_${c}_web.mp4
  fi
  echo CLIP_${c}_DONE
done
echo ANIM_DONE
