# Copies compositions/_base.css into every scene between the /*base:start*/ … /*base:end*/ markers.
import re,glob
base=open('compositions/_base.css').read()
for f in glob.glob('compositions/*.html'):
    s=open(f).read()
    n=re.sub(r'/\*base:start\*/.*?/\*base:end\*/', lambda m:'/*base:start*/\n'+base+'/*base:end*/', s, flags=re.S)
    if n!=s: open(f,'w').write(n); print('inlined',f)
