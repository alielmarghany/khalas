# v3 (seller POV, 3D phone): voice clips + music ducked under voice + one SFX stem -> hf/assets/audio
import json, subprocess
O = '/home/user/khalas/reel/hf/assets/audio/'
VOICE = 'v3/chris'   # male voice (Chris); 'v3' holds the earlier Laura takes
T = json.load(open(VOICE + '/timing.json'))
V = [(f'{VOICE}/vo{i}.wav', T[f'vo{i}']['start']) for i in range(1, 6)]
S = [('vibrate',0.0,.9),('pop',0.15,.3),('vibrate',1.15,.8),('pop',1.0,.3),('pop',1.9,.3),('vibrate',2.25,.8),('pop',2.6,.3),
     ('whoosh',3.15,.8),('vibrate',3.2,.9),('notif',3.3,.7),('notif',3.86,.7),('notif',4.5,.7),('whoosh',4.9,.7),('vibrate',4.95,.8),
     ('notif',4.95,.5),('notif',5.4,.5),('notif',5.8,.5),('pop',5.2,.3),('pop',5.5,.3),('pop',6.1,.3),('pop',6.4,.3),
     ('lightson',6.68,1.0),('whoosh',6.7,.6),('typing',6.95,.35),('pop',7.38,.55),('pop',7.98,.55),('ding',8.36,.8),
     ('whoosh',9.45,.5),('night',9.5,.15),('vibrate',9.85,.35),('notif',9.85,.3),('vibrate',10.45,.2),('notif',10.45,.15),
     ('vibrate',11.05,.2),('notif',11.05,.15),('riser',11.62,.5),('boom',11.98,1.0),('whoosh',12.05,.7),('stamp',12.13,.5),('pop',13.25,.45)]
for k in range(13): S.append(('tick', round(26*60/128 + k*60/128, 3), .18))   # on the beat from 12.19 s
ins = ['-i', 'music.wav']; f = []; n = 1; vl = []; sl = []
for fn, st in V:
    ins += ['-i', fn]; f.append(f'[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(st*1000)}|{int(st*1000)}[v{n}]'); vl.append(f'[v{n}]'); n += 1
for nm, st, vol in S:
    ins += ['-i', f'sfx/{nm}.mp3']; f.append(f'[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={vol},adelay={int(st*1000)}|{int(st*1000)}[s{n}]'); sl.append(f'[s{n}]'); n += 1
f.append(''.join(vl) + f'amix=inputs={len(vl)}:normalize=0,volume=2.2,apad=whole_dur=16[vsc]')
f.append(''.join(sl) + f'amix=inputs={len(sl)}:normalize=0,atrim=0:15[sfx]')
f.append('[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.5[mus];[mus][vsc]sidechaincompress=threshold=0.03:ratio=8:attack=5:release=200,atrim=0:15,afade=t=out:st=14.8:d=0.2[musd]')
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(f), '-map', '[musd]', '-ar', '48000', O + 'music.wav', '-map', '[sfx]', '-ar', '48000', O + 'sfx.wav'], check=True)
for i in range(1, 6):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{VOICE}/vo{i}.wav', '-af', 'volume=2.2', '-ar', '48000', '-ac', '2', O + f'vo{i}.wav'], check=True)
print('ok')
