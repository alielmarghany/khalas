import numpy as np, wave
SR=44100; BPM=128; B=60/BPM; DUR=15.3; N=int(SR*DUR)
rng=np.random.default_rng(7)
L=np.zeros(N); R=np.zeros(N)
def add(sig,t,gain=1.0,pan=0.0):
    i=int(t*SR); 
    if i>=N: return
    s=sig[:N-i]*gain
    L[i:i+len(s)]+=s*(1-pan)/1; R[i:i+len(s)]+=s*(1+pan)/1
def env(n,a=0.002,d=0.2):
    t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/d)
def kick():
    n=int(.35*SR); t=np.arange(n)/SR
    f=45+110*np.exp(-t/0.035); ph=2*np.pi*np.cumsum(f)/SR
    return np.tanh(2.2*np.sin(ph)*np.exp(-t/0.16))*0.9
def clap():
    n=int(.25*SR); x=rng.standard_normal(n); x=np.diff(x,prepend=0)
    e=env(n,0.001,0.06); e[:int(.012*SR)]*=1.3
    return x*e*0.35
def hat(open_=False):
    n=int((.18 if open_ else .05)*SR); x=np.diff(np.diff(rng.standard_normal(n),prepend=0),prepend=0)
    return x*env(n,0.0005,0.06 if open_ else 0.015)*0.12
def tone(freq,dur,shape='saw',decay=0.3,harm=12):
    n=int(dur*SR); t=np.arange(n)/SR; s=np.zeros(n)
    for h in range(1,harm+1):
        if shape=='sq' and h%2==0: continue
        if freq*h>12000: break
        s+=np.sin(2*np.pi*freq*h*t)/h
    return s*env(n,0.003,decay)
def darbuka(high=False):
    n=int(.15*SR); t=np.arange(n)/SR
    f=(420 if high else 180)*(1+0.3*np.exp(-t/0.01))
    s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/(0.04 if high else 0.08))
    s+=rng.standard_normal(n)*np.exp(-t/0.008)*0.3
    return s*0.35
D=73.42  # D2
hij=[0,1,4,5,7,8,10,12]  # D hijaz semitones
def note(semi,base=D): return base*2**(semi/12)
K=kick(); C=clap()
bars=int(DUR/(4*B))+1
for bar in range(bars):
    t0=bar*4*B
    night = 9.0<=t0<12.0
    for beat in range(4):
        tb=t0+beat*B
        if tb>=DUR: break
        if not night or beat in (0,2): add(K,tb,1.0 if not night else 0.6)
        if beat in (1,3) and not night: add(C,tb,1.0,0.0)
        # 16th hats
        for s in range(4):
            ts=tb+s*B/4
            add(hat(open_=(s==2)),ts,(1.0 if s==2 else 0.6)*(0.5 if night else 1),pan=0.3)
    # maqsoum darbuka: D T . T D . T .  (8ths)
    pat=['D','T',None,'T','D',None,'T',None]
    for k,p in enumerate(pat):
        if p: add(darbuka(p=='T'),t0+k*B/2,0.9*(0.6 if night else 1),pan=-0.25)
    # bass on offbeat 8ths
    bl=[0,0,1,0,0,0,-2,0]
    for k in range(8):
        ts=t0+k*B/2+B/4
        add(tone(note(bl[k]),B/2*0.9,'saw',0.12,8),ts,0.28*(0.5 if night else 1))
# lead riff (hijaz) on 16ths, 2-bar phrase
riff=[12,None,13,12,16,None,13,12, 17,16,13,None,12,None,10,12, 12,None,13,12,16,17,19,None, 17,16,13,12,13,None,12,None]
for bar in range(bars):
    t0=bar*4*B
    if t0>=DUR: break
    if 9.0<=t0<12.0: continue
    for k in range(16):
        semi=riff[(bar%2)*16+k]
        if semi is None: continue
        add(tone(note(semi,D*2),B/4*1.6,'sq',0.09,9),t0+k*B/4,0.07,pan=0.15)
# night pad 9-12
n=int(3.0*SR); t=np.arange(n)/SR
pad=sum(np.sin(2*np.pi*note(s,D*2)*t+np.sin(2*np.pi*0.3*t)) for s in (0,4,7))
pad*=np.minimum(1,t/0.3)*np.minimum(1,(3.0-t)/0.2)*0.06
add(pad,9.0)
# riser 11.0-12.0 (noise sweep)
n=int(0.55*SR); t=np.arange(n)/SR; x=rng.standard_normal(n)
x=x*(t/0.55)**2*0.25; add(x,11.45)
mix=np.stack([L,R],1)
# gentle master: soft clip + normalize
mix=np.tanh(mix*1.2); mix/=np.max(np.abs(mix))*1.12
# 5ms fade in, 0.3 fade out
fo=int(.3*SR); mix[-fo:]*=np.linspace(1,0,fo)[:,None]
w=wave.open('music.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix*32767).astype('<i2').tobytes()); w.close()
print('ok',mix.shape[0]/SR)
