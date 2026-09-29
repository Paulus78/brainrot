#!/bin/sh
set -eu

if [ "$#" -ne 6 ]; then
  echo "usage: $0 HOOK.mp4 SLAM.mp4 PAYOFF.mp4 VOICE_MASTER.wav FINAL.mp4 VOICE_ONLY.wav" >&2
  exit 2
fi

hook=$1
slam=$2
payoff=$3
voice=$4
final=$5
voice_only=$6
ffmpeg='/Applications/Streamlabs OBS.app/Contents/Resources/node_modules/ffmpeg-ffprobe-static/ffmpeg'

# Three long, genuinely animated Veo shots. The mild 1.08x speed-up keeps the
# short energetic without turning the physical actions into jumpy fragments.
# Dialogue is added from one previously accepted continuous voice take.
"$ffmpeg" -loglevel error -y \
  -i "$hook" -i "$slam" -i "$payoff" -i "$voice" \
  -filter_complex \
  "[0:v]trim=start=0:end=6.5,setpts=(PTS-STARTPTS)/1.08,scale=1080:1920:flags=lanczos,fps=24,setsar=1[v0]; \
   [1:v]trim=start=0:end=7.0,setpts=(PTS-STARTPTS)/1.08,scale=1080:1920:flags=lanczos,fps=24,setsar=1[v1]; \
   [2:v]trim=start=0:end=8.0,setpts=(PTS-STARTPTS)/1.08,scale=1080:1920:flags=lanczos,fps=24,setsar=1[v2]; \
   [v0][v1][v2]concat=n=3:v=1:a=0[vout]; \
   [0:a]atrim=start=0:end=6.5,asetpts=PTS-STARTPTS,atempo=1.08,afade=t=out:st=5.98:d=0.03[a0]; \
   [1:a]atrim=start=0:end=7.0,asetpts=PTS-STARTPTS,atempo=1.08,afade=t=in:st=0:d=0.03,afade=t=out:st=6.45:d=0.03[a1]; \
   [2:a]atrim=start=0:end=8.0,asetpts=PTS-STARTPTS,atempo=1.08,afade=t=in:st=0:d=0.03[a2]; \
   [a0][a1][a2]concat=n=3:v=0:a=1,volume=0.92[bed]; \
   [3:a]atrim=start=5.34:end=6.46,asetpts=PTS-STARTPTS,highpass=f=70,lowpass=f=12000,volume=0.94,afade=t=in:st=0:d=0.04,afade=t=out:st=1.04:d=0.08,adelay=18150,apad=whole_dur=19.907,atrim=start=0:end=19.907,asplit=2[snacko_mix][voicecheck]; \
   [bed][snacko_mix]amix=inputs=2:duration=first:dropout_transition=0,volume=2,alimiter=limit=0.95,loudnorm=I=-16:TP=-1.0:LRA=11,aresample=48000[aout]" \
  -map '[vout]' -map '[aout]' -c:v libx264 -preset medium -crf 17 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "$final" \
  -map '[voicecheck]' -c:a pcm_s24le "$voice_only"
