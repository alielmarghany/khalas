import subprocess
V=[('tr_liam_a_l1.wav',0.05,1.35,2.2),('tr_liam_b_l2.wav',2.75,1.2,2.2),('tr_liam_a_l3.wav',5.10,1.12,2.2),('tr_l4d.wav',9.25,1.1,2.8),('tr_liam_b_l5.wav',12.60,1.05,2.2)]
S=[('pop',0.0,.5),('pop',0.13,.45),('pop',0.27,.5),('pop',0.41,.45),('pop',0.6,.45),('pop',0.82,.4),('pop',1.05,.4),('pop',1.25,.35),
('whoosh',0.0,.7),('buzz',1.46,.75),('scratch',1.44,.7),('pop',1.7,.35),('pop',2.05,.35),
('whoosh',2.58,.8),('stamp',2.72,1.0),('whoosh',3.38,.8),('stamp',3.52,1.0),('whoosh',4.18,.8),('stamp',4.32,1.0),
('whoosh',4.96,.9),('swoosh_multi',5.5,.8),('pop',5.95,.4),('pop',6.2,.4),('pop',6.45,.4),
('whoosh',6.95,.8),('stamp',7.0,.7),('ding',7.48,.8),('whoosh',8.17,.6),('pop',8.22,.5),('pop',8.38,.5),('pop',8.54,.5),
('whoosh',8.96,.8),('night',9.0,.2),('pop',9.12,.4),('typing',9.45,.2),('pop',9.85,.4),('pop',10.3,.35),
('whoosh',10.56,.6),('ding',10.62,.45),('riser',11.42,.5),
('boom',11.98,1.0),('tick',12.2,.5),('whoosh',12.6,.8),('stamp',12.66,.7),('pop',13.82,.5)]
for k in range(13): S.append(('tick',12.94+k*60/128,.22))
ins=['-i','music.wav']; f=[]; n=1; vl=[]; sl=[]
for fn,st,tp,g in V:
    ins+=['-i',fn]; f.append(f'[{n}:a]atempo={tp},aformat=sample_rates=44100:channel_layouts=stereo,adelay={int(st*1000)}|{int(st*1000)},volume={g}[v{n}]'); vl.append(f'[v{n}]'); n+=1
for nm,st,vol in S:
    ins+=['-i',f'sfx/{nm}.mp3']; f.append(f'[{n}:a]aformat=sample_rates=44100:channel_layouts=stereo,volume={vol},adelay={int(st*1000)}|{int(st*1000)}[s{n}]'); sl.append(f'[s{n}]'); n+=1
f.append(''.join(vl)+f'amix=inputs={len(vl)}:normalize=0,asplit=2[vo][vsc]')
f.append(''.join(sl)+f'amix=inputs={len(sl)}:normalize=0[sfx]')
f.append('[0:a]volume=0.5[mus];[mus][vsc]sidechaincompress=threshold=0.03:ratio=8:attack=5:release=200[musd]')
f.append('[vo][musd][sfx]amix=inputs=3:normalize=0,acompressor=threshold=0.3:ratio=3:attack=3:release=80,alimiter=limit=0.95,atrim=0:15,afade=t=out:st=14.85:d=0.15[out]')
subprocess.run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',';'.join(f),'-map','[out]','-ar','48000','mix.wav'],check=True)
