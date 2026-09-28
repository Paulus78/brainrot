#!/bin/sh
set -eu

if [ "$#" -ne 5 ]; then
  echo "usage: $0 READY.png CONTACT.png REACTION.png REACTION_RUMBLE.png OUTPUT.mp4" >&2
  exit 2
fi

ready=$1
contact=$2
reaction=$3
reaction_rumble=$4
output=$5
ffmpeg='/Applications/Streamlabs OBS.app/Contents/Resources/node_modules/ffmpeg-ffprobe-static/ffmpeg'

"$ffmpeg" -loglevel error -y \
  -loop 1 -framerate 24 -t 4.25 -i "$ready" \
  -loop 1 -framerate 24 -t 4.25 -i "$contact" \
  -loop 1 -framerate 24 -t 4.25 -i "$reaction" \
  -loop 1 -framerate 24 -t 4.25 -i "$reaction_rumble" \
  -f lavfi -i 'anoisesrc=color=white:duration=0.06:amplitude=1' \
  -f lavfi -i 'anoisesrc=color=white:duration=0.07:amplitude=1' \
  -f lavfi -i 'anoisesrc=color=white:duration=0.09:amplitude=1' \
  -f lavfi -i 'anoisesrc=color=brown:duration=0.875:amplitude=0.45' \
  -filter_complex \
  "[0:v]scale=720:1280,format=gbrp[ready]; \
   [1:v]scale=720:1280,format=gbrp[contact]; \
   [2:v]scale=720:1280,format=gbrp[reaction]; \
   [3:v]scale=720:1280,format=gbrp[reaction_rumble]; \
   [ready][contact]blend=all_expr='A*(1-max(max(max(0,1-abs(T-0.333)/0.125),max(0,1-abs(T-0.958)/0.167)),max(0,1-abs(T-1.646)/0.25)))+B*max(max(max(0,1-abs(T-0.333)/0.125),max(0,1-abs(T-0.958)/0.167)),max(0,1-abs(T-1.646)/0.25))'[taps]; \
   [taps][reaction]blend=all_expr='A*(1-min(max((T-2.458)/0.35,0),1))+B*min(max((T-2.458)/0.35,0),1)'[reacting]; \
   [reacting][reaction_rumble]blend=all_expr='A*(1-if(between(T,2.80,3.333),abs(sin(25*T)),0))+B*if(between(T,2.80,3.333),abs(sin(25*T)),0)',format=yuv420p[v]; \
   [4:a]highpass=f=150,lowpass=f=1100,afade=t=out:st=0.015:d=0.045,volume=.10,adelay=300|300[t1]; \
   [5:a]highpass=f=130,lowpass=f=950,afade=t=out:st=0.02:d=0.05,volume=.16,adelay=900|900[t2]; \
   [6:a]highpass=f=100,lowpass=f=800,afade=t=out:st=0.025:d=0.065,volume=.24,adelay=1580|1580[t3]; \
   [7:a]highpass=f=60,lowpass=f=420,volume=.16,adelay=2458|2458[rumble]; \
   [t1][t2][t3][rumble]amix=inputs=4:duration=longest[a]" \
  -map '[v]' -map '[a]' -t 4.25 -r 24 -c:v libx264 -preset slow -crf 16 \
  -c:a aac -b:a 192k -movflags +faststart "$output"
