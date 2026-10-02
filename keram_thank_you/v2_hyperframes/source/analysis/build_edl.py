import json, wave, numpy as np
E='/home/user/edit/'
ch_en=json.load(open(E+'chunks_en.json')); ch_ar=json.load(open(E+'chunks.json'))
w=wave.open(E+'audio16k.wav'); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
SR=16000; hop=160
rms=np.array([np.sqrt(np.mean(a[i:i+320]**2)+1e-12) for i in range(0,len(a)-320,hop)])
db=20*np.log10(rms); nz=db[db>-100]; floor=float(np.percentile(nz,10)); TH=-45.0
speech=db>TH
def t2i(t): return int(round(t*100))
def onset(t):   # walk back from word start to where energy drops below threshold
    i=t2i(t)
    while i>0 and speech[i-1]: i-=1
    return i/100
def offset(t):
    i=t2i(t)
    while i<len(speech)-1 and speech[i]: i+=1
    return i/100
# chunks kept (source chunk starts), in output order
KEEP=[0.47,15.94,21.28,27.92,36.58,74.94,95.31,105.67,111.37,120.27,137.70,168.86,172.86]
byS={round(c['s'],2):c for c in ch_en}; byS[0.47]=[c for c in ch_ar if abs(c['s']-0.47)<.01][0]
words=[]
for k in KEEP:
    for x in byS[k]['words']: words.append(dict(text=x['w'].strip(),start=x['s'],end=x['e'],p=x['p'],chunk=k))
# group words into retained ranges: break when gap of real silence >= 0.30s
ranges=[];cur=None
for i,x in enumerate(words):
    if cur is None: cur=[x['start'],x['end'],[x]]; continue
    gap_s=offset(cur[1]-0.02); gap_e=onset(x['start']+0.02)
    silent=gap_e-gap_s
    if silent>=0.30 or x['chunk']!=cur[2][-1]['chunk'] and not (x['chunk']==172.86):
        ranges.append(cur); cur=[x['start'],x['end'],[x]]
    else: cur[1]=x['end']; cur[2].append(x)
ranges.append(cur)
FPS=25
out=[];t=0.0
for s,e,ws in ranges:
    so=min(onset(s+0.03),s)-0.10   # 0.10 s room before speech onset
    eo=max(offset(e-0.03),e)+0.12  # 0.12 s tail room
    so=round(max(0,so)*FPS)/FPS; eo=round(eo*FPS)/FPS
    out.append(dict(src_start=so,src_end=eo,dur=round(eo-so,3),out_start=round(t,3),out_end=round(t+eo-so,3),text=" ".join(x['text'] for x in ws)))
    t+=eo-so
# ensure no overlap in source between consecutive ranges
for a_,b_ in zip(out,out[1:]):
    if b_['src_start']<a_['src_end'] and b_['src_start']>a_['src_start']:
        mid=round(((a_['src_end']+b_['src_start'])/2)*FPS)/FPS; print('overlap fix',a_['src_end'],b_['src_start'])
json.dump(dict(fps=FPS,noise_floor_db=float(floor),threshold_db=float(TH),ranges=out),open('timing-map.json','w'),indent=1,ensure_ascii=False)
json.dump(words,open('analysis/words_kept_src.json','w'),ensure_ascii=False,indent=0)
for r in out: print(f"{r['src_start']:7.2f}-{r['src_end']:7.2f} ({r['dur']:5.2f}) -> {r['out_start']:6.2f} | {r['text'][:70]}")
print('total',round(t,2),'floor',round(floor,1))
