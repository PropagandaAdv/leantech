#!/bin/bash
# Video assieme: orbita 360 + pausa + zoom fino a 34hero. 14 s, 25 fps, 1920x1080. Riprendibile (frame esistenti saltati).
cd "$(dirname "$0")/.."
export PROFILE=v2 FRENO_VARIANT=a
python3 -I scripts/video_orbit_zoom.py --fps 25 --orbit 9 --hold 1 --zoom 4 --res 1920x1080 --samples 16 --frames-dir work/video_frames
N=$(ls work/video_frames/frame_*.jpg 2>/dev/null | wc -l)
if [ "$N" -ge 350 ]; then
  mkdir -p output/video
  ffmpeg -y -loglevel error -framerate 25 -i work/video_frames/frame_%04d.jpg -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -movflags +faststart output/video/PX0000381686_rotazione360_zoom_v2.mp4
  ffmpeg -y -loglevel error -framerate 25 -i work/video_frames/frame_%04d.jpg -vf scale=1280:720 -c:v libx264 -preset veryfast -crf 26 -pix_fmt yuv420p -movflags +faststart output/video/PX0000381686_rotazione360_zoom_v2_web.mp4
  echo VIDEO_DONE
fi
