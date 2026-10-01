import subprocess, sys, os, numpy as np
from PIL import Image
FPS=25; W,H=1080,1920; SW,SH=720,1280
# zoom plan: (seg_start, seg_end, s0, s1) in first-cut time; plus eased punches
ZP=[(0,10.72,1.00,1.06),(10.72,13.92,1.14,1.16),(13.92,16.32,1.02,1.05),(16.32,19.84,1.0,1.0),
    (19.84,22.68,1.14,1.16),(22.68,25.84,1.0,1.10),(25.84,29.76,1.15,1.17),(29.76,34.84,1.0,1.0),
    (34.84,41.64,1.02,1.07),(41.64,46.28,1.15,1.17),(46.28,49.9,1.0,1.05),(49.9,99,1.05,1.05)]
def ease(x): return x*x*(3-2*x)
def zoom(t):
    for a,b,s0,s1 in ZP:
        if a<=t<b:
            z=s0+(s1-s0)*ease(min(1,(t-a)/max(0.01,b-a)))
            if a==46.28 and t>=49.9: pass
            return z
    return 1.0
def zoom_final(t):
    z=zoom(t)
    if 49.9<=t<52: z=1.05+0.09*ease(min(1,(t-49.9)/0.5))  # emphasis on final line
    return z
def frame_zoom(img,t):
    z=zoom_final(t)
    if abs(z-1)<1e-3: return img.resize((W,H),Image.LANCZOS)
    cw,ch=SW/z,SH/z; cx,cy=SW/2,SH/2
    box=(cx-cw/2,cy-ch/2,cx+cw/2,cy+ch/2)
    return img.resize((W,H),Image.LANCZOS,box=box)
LAYERS=["cards","broll","captions","logo"]
def comp(base,fr,root):
    out=base.convert("RGBA")
    for L in LAYERS:
        p=f"{root}/{L}/{fr:05d}.png"
        if os.path.exists(p): out.alpha_composite(Image.open(p).convert("RGBA"))
    return out.convert("RGB")
if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="preview":
        root=sys.argv[2]; outs=[]
        for t in sys.argv[3].split(","):
            t=float(t); fr=int(round(t*FPS)); tt=min(t,51.96)
            raw=subprocess.run(["ffmpeg","-v","error","-ss",str(tt),"-i","first_cut.mp4","-frames:v","1","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
            img=Image.frombytes("RGB",(SW,SH),raw)
            outs.append(comp(frame_zoom(img,t),fr,root).resize((360,640)))
        sheet=Image.new("RGB",(360*6,640*((len(outs)+5)//6)))
        for i,o in enumerate(outs): sheet.paste(o,((i%6)*360,(i//6)*640))
        sheet.save(sys.argv[4])
    else:
        root=sys.argv[2]; out=sys.argv[3]; total=float(sys.argv[4])
        dec=subprocess.Popen(["ffmpeg","-v","error","-i","first_cut.mp4","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
        enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
             "-c:v","libx264","-preset","slow","-crf","17","-pix_fmt","yuv420p",out],stdin=subprocess.PIPE)
        n=int(round(total*FPS)); last=None
        for fr in range(n):
            raw=dec.stdout.read(SW*SH*3)
            if len(raw)==SW*SH*3: last=Image.frombytes("RGB",(SW,SH),raw)
            t=fr/FPS
            enc.stdin.write(comp(frame_zoom(last,t),fr,root).tobytes())
            if fr%250==0: print("frame",fr,flush=True)
        enc.stdin.close(); enc.wait(); dec.kill()
