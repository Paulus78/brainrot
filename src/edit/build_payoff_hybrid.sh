#!/bin/sh
set -eu

if [ "$#" -ne 4 ]; then
  echo "usage: $0 ERUPTION_START.png ERUPTION_MID.png PAYOFF_HOLD.png OUTPUT.mp4" >&2
  exit 2
fi

start=$1
mid=$2
hold=$3
output=$4
ffmpeg='/Applications/Streamlabs OBS.app/Contents/Resources/node_modules/ffmpeg-ffprobe-static/ffmpeg'

"$ffmpeg" -loglevel error -y \
  -loop 1 -framerate 24 -t 5 -i "$start" \
  -loop 1 -framerate 24 -t 5 -i "$mid" \
  -loop 1 -framerate 24 -t 5 -i "$hold" \
  -f lavfi -i 'anoisesrc=color=white:duration=2.3:amplitude=0.7' \
  -f lavfi -i 'anoisesrc=color=pink:duration=2.3:amplitude=0.5' \
  -f lavfi -i 'anoisesrc=color=white:duration=0.10:amplitude=0.7' \
  -filter_complex \
  "[0:v]scale=720:1280,format=gbrp[start]; \
   [1:v]scale=720:1280,format=gbrp[mid]; \
   [2:v]scale=720:1280,format=gbrp[hold]; \
   [start][mid]blend=all_expr='A*(1-min(max((T-0.25)/0.30,0),1))+B*min(max((T-0.25)/0.30,0),1)'[growing]; \
   [growing][hold]blend=all_expr='A*(1-min(max((T-1.10)/0.35,0),1))+B*min(max((T-1.10)/0.35,0),1)',format=yuv420p[v]; \
   [3:a]highpass=f=500,lowpass=f=3500,volume='if(lt(mod(t,0.16),0.028),0.18,0)':eval=frame[pops]; \
   [4:a]highpass=f=70,lowpass=f=900,afade=t=in:st=0:d=0.15,afade=t=out:st=1.40:d=0.90,volume=.16[whoosh]; \
   [5:a]highpass=f=600,lowpass=f=2600,afade=t=out:st=0.02:d=0.08,volume=.20,adelay=3200|3200[crunch]; \
   [pops][whoosh][crunch]amix=inputs=3:duration=longest[audio]" \
  -map '[v]' -map '[audio]' -t 5 -r 24 -c:v libx264 -preset slow -crf 16 \
  -c:a aac -b:a 192k -movflags +faststart "$output"
