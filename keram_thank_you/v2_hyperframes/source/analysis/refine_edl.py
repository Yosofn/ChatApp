import json,wave,numpy as np
w=wave.open('/home/user/edit/audio16k.wav'); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
db=20*np.log10(np.array([np.sqrt(np.mean(a[i:i+320]**2)+1e-12) for i in range(0,len(a)-320,160)]))
sp=db>-45
FPS=25; q=lambda t: round(t*FPS)/FPS
tm=json.load(open('timing-map.json')); words=json.load(open('analysis/words_kept_src.json'))
new=[];t=0.0
for r in tm['ranges']:
    i0,i1=int(r['src_start']*100),int(r['src_end']*100)
    idx=np.where(sp[i0:i1])[0]+i0
    if len(idx)==0: continue
    # speech islands
    isl=[[idx[0],idx[0]]]
    for i in idx[1:]:
        if i-isl[-1][1]<=26: isl[-1][1]=i     # merge gaps < 0.26 s
        else: isl.append([i,i])
    for s,e in isl:
        if e-s<8: continue  # ignore <80ms blips
        ss=q(s/100-0.08); ee=q((e+1)/100+0.10)
        if new and ss<new[-1]['src_end'] and ss>new[-1]['src_start']: ss=new[-1]['src_end']
        txt=" ".join(x['text'] for x in words if x['start']<ee-0.05 and x['end']>ss+0.05)
        new.append(dict(src_start=ss,src_end=ee))
        new[-1]['text']=txt
for r in new:
    r['dur']=round(r['src_end']-r['src_start'],3); r['out_start']=round(t,3); t+=r['dur']; r['out_end']=round(t,3)
tm['ranges']=new; tm['threshold_db']=-45.0; tm['notes']='Energy onsets (source pauses are gated to digital silence); internal pauses >=0.26s removed; 0.08s head / 0.10s tail room; frame-quantised at 25fps.'
json.dump(tm,open('timing-map.json','w'),indent=1,ensure_ascii=False)
for r in new: print(f"{r['src_start']:7.2f}-{r['src_end']:7.2f} ({r['dur']:4.2f}) -> {r['out_start']:6.2f}-{r['out_end']:6.2f} | {r['text'][:60]}")
print('total',round(t,2),'ranges',len(new))
