#!/bin/sh
set -eu

if [ "$#" -ne 4 ]; then
  echo "usage: $0 PICTURE_CUT.mp4 VOICE_MASTER.wav FINAL.mp4 VOICE_ONLY.wav" >&2
  exit 2
fi

picture=$1
voice=$2
final=$3
voice_only=$4
ffmpeg='/Applications/Streamlabs OBS.app/Contents/Resources/node_modules/ffmpeg-ffprobe-static/ffmpeg'

"$ffmpeg" -loglevel error -y \
  -i "$picture" -i "$voice" \
  -filter_complex \
  "[0:a]volume=1.55[bed]; \
   [1:a]atrim=start=0.82:end=1.52,asetpts=PTS-STARTPTS,highpass=f=70,lowpass=f=12000,volume=0.78,afade=t=in:st=0:d=0.04,afade=t=out:st=0.64:d=0.06,adelay=4000,apad=whole_dur=14.959,atrim=start=0:end=14.959,asplit=2[bucketo_mix][bucketo_solo]; \
   [1:a]atrim=start=5.34:end=6.46,asetpts=PTS-STARTPTS,highpass=f=70,lowpass=f=12000,volume=0.94,afade=t=in:st=0:d=0.04,afade=t=out:st=1.04:d=0.08,adelay=11780,apad=whole_dur=14.959,atrim=start=0:end=14.959,asplit=2[snacko_mix][snacko_solo]; \
   [bed][bucketo_mix][snacko_mix]amix=inputs=3:duration=first:dropout_transition=0,volume=3,alimiter=limit=0.89,aresample=48000[aout]; \
   [bucketo_solo][snacko_solo]amix=inputs=2:duration=longest:dropout_transition=0,volume=2,alimiter=limit=0.89,aresample=48000[voicecheck]" \
  -map 0:v -map '[aout]' -c:v copy -c:a aac -b:a 192k -movflags +faststart "$final" \
  -map '[voicecheck]' -c:a pcm_s24le "$voice_only"
