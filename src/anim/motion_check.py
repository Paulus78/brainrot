"""Findet Leerlauf: Stellen, an denen sich das Bild ueber laengere Zeit kaum aendert."""
import subprocess, sys
import numpy as np
path = sys.argv[1]
W_, H_ = 135, 240
raw = subprocess.run(["ffmpeg","-v","error","-i",path,"-vf",f"scale={W_}:{H_}","-pix_fmt","gray","-f","rawvideo","-"],capture_output=True,check=True).stdout
fr = np.frombuffer(raw,np.uint8).reshape(-1,H_,W_).astype(np.float32)
d = np.abs(np.diff(fr,axis=0)).mean(axis=(1,2))
thr = float(sys.argv[2]) if len(sys.argv)>2 else 0.6
print(f"{len(fr)} frames, median motion {np.median(d):.2f}")
run=None
for i,v in enumerate(d):
    if v<thr:
        run = i if run is None else run
    else:
        if run is not None and (i-run)>=9: print(f"  ruhig {run/30:.2f}-{i/30:.2f}s ({(i-run)/30:.2f}s, avg {d[run:i].mean():.2f})")
        run=None
if run is not None and len(d)-run>=9: print(f"  ruhig {run/30:.2f}-{len(d)/30:.2f}s")
print("Bewegung pro 0.5s:", " ".join(f"{d[i:i+15].mean():.1f}" for i in range(0,len(d),15)))
