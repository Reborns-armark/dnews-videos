import sys; sys.path.insert(0,'/home/claude/dnews-engine')
from engine3 import tts3
from engine import SR
from script_lines import LINES, GAP
def timeline():
    t=0; out=[]
    for i,(say,cap) in enumerate(LINES):
        a=tts3(say); d=len(a)/SR+(0.2 if i==0 else GAP)+(1.2 if i==len(LINES)-1 else 0)
        out.append(dict(i=i,say=say,cap=cap,audio=a,t0=t,d=d)); t+=d
    return out,t
if __name__=="__main__":
    tl,T=timeline()
    for c in tl: print(round(c["t0"],2), round(c["d"],2), c["say"][:20])
    print("TOTAL",round(T,2))
