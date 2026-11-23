#!/usr/bin/env bash
# Synthesized SFX (no samples) for the 10s looping skit:
# pop = incoming, click = sent, sad "wah-wah-wah" sting at 6.0s, very quiet room-tone bed.
set -euo pipefail
OUT=${1:-audio.m4a}
SR=48000
D=10
# incoming pop: fast upward chirp 700->1400Hz with exponential decay (~90ms)
POP="0.55*sin(2*PI*(700*t+3500*t*t))*exp(-t*45)*min(1,t*400)"
# sent click: short bright tick + soft body (~40ms)
CLICK="0.35*(sin(2*PI*2200*t)*exp(-t*160)+0.6*sin(2*PI*900*t)*exp(-t*90))*min(1,t*800)"
# sad trombone: 4 descending notes, brassy harmonics, vibrato on last note (~2.6s)
F="(if(lt(t,0.42),293.66,if(lt(t,0.84),277.18,if(lt(t,1.26),261.63,246.94))))"
TS="(if(lt(t,0.42),0,if(lt(t,0.84),0.42,if(lt(t,1.26),0.84,1.26))))"
DUR="(if(lt(t,1.26),0.40,1.3))"
LT="(t-$TS)"
VIB="(if(gte(t,1.26),0.012*sin(2*PI*5.5*t)*min(1,(t-1.3)*3)*gte(t,1.3),0))"
PH="(2*PI*$F*(1+$VIB)*$LT)"
TONE="(sin($PH)+0.7*sin(2*$PH)+0.5*sin(3*$PH)+0.32*sin(4*$PH)+0.2*sin(5*$PH)+0.12*sin(6*$PH))"
ENV="(min(1,$LT/0.05)*min(1,max(0,($DUR-$LT)/0.08))*(0.75+0.25*sin(PI*min(1,$LT/0.25))))"
WAH="0.16*$TONE*$ENV"
# Room tone: 10.5s of filtered brown noise (same seed rendered twice); the extra 0.5s tail is crossfaded (equal power)
# into the first 0.5s, so sample D-1 flows continuously into sample 0 when the video loops.
ffmpeg -loglevel error -y \
  -f lavfi -i "aevalsrc='$POP':s=$SR:d=0.25" \
  -f lavfi -i "aevalsrc='$CLICK':s=$SR:d=0.12" \
  -f lavfi -i "aevalsrc='$WAH':s=$SR:d=2.6" \
  -f lavfi -i "anoisesrc=c=brown:r=$SR:a=1:seed=7:d=10.5" \
  -f lavfi -i "anoisesrc=c=brown:r=$SR:a=1:seed=7:d=10.5" \
  -filter_complex "
    [3]highpass=f=40,lowpass=f=500,volume=-34dB,atrim=0:$D,asetpts=PTS-STARTPTS,afade=t=in:d=0.5:curve=qsin[body];
    [4]highpass=f=40,lowpass=f=500,volume=-34dB,atrim=$D:10.5,asetpts=PTS-STARTPTS,afade=t=out:d=0.5:curve=qsin,apad=whole_dur=$D[tail];
    [body][tail]amix=inputs=2:normalize=0:duration=first[bed];
    [0]asplit=3[p1][p2][p3];
    [1]asplit=2[c1][c2];
    [p1]adelay=1500:all=1[a1];[p2]adelay=3000:all=1[a2];[p3]adelay=6000:all=1[a3];
    [c1]adelay=1000:all=1[b1];[c2]adelay=3800:all=1[b2];
    [2]lowpass=f=1800,equalizer=f=700:t=q:w=1:g=4,adelay=6050:all=1[w];
    [bed][a1][a2][a3][b1][b2][w]amix=inputs=7:normalize=0:duration=first,
      aformat=sample_fmts=fltp:channel_layouts=stereo,alimiter=limit=0.9:level=disabled[out]" \
  -map "[out]" -t $D -c:a aac -b:a 128k "$OUT"
