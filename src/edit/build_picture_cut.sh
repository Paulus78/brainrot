#!/bin/sh
set -eu

if [ "$#" -ne 5 ]; then
  echo "usage: $0 HOOK.mp4 BANANA.mp4 TAPS.mp4 PAYOFF.mp4 OUTPUT.mp4" >&2
  exit 2
fi

hook=$1
banana=$2
taps=$3
payoff=$4
output=$5
ffmpeg='/Applications/Streamlabs OBS.app/Contents/Resources/node_modules/ffmpeg-ffprobe-static/ffmpeg'

"$ffmpeg" -loglevel error -y \
  -i "$hook" -i "$banana" -i "$taps" -i "$payoff" \
  -filter_complex \
  "[0:v]trim=duration=2.5,setpts=PTS-STARTPTS[v0]; \
   [0:a]atrim=duration=2.5,asetpts=PTS-STARTPTS[a0]; \
   [1:v]trim=duration=3.2,setpts=PTS-STARTPTS[v1]; \
   [1:a]atrim=duration=3.2,asetpts=PTS-STARTPTS[a1]; \
   [2:v]trim=duration=4.25,setpts=PTS-STARTPTS[v2]; \
   [2:a]atrim=duration=4.25,asetpts=PTS-STARTPTS[a2]; \
   [3:v]trim=duration=5,setpts=PTS-STARTPTS[v3]; \
   [3:a]atrim=duration=5,asetpts=PTS-STARTPTS[a3]; \
   [v0][a0][v1][a1][v2][a2][v3][a3]concat=n=4:v=1:a=1[v][a]" \
  -map '[v]' -map '[a]' -r 24 -c:v libx264 -preset slow -crf 16 \
  -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "$output"
