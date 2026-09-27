import sys, time, resource, numpy as np, soundfile as sf
from faster_whisper import WhisperModel
A="/tmp/claude-0/-home-user-chiron-quests/a3d3f8a3-a2de-5718-9a60-89ea0a9bcadb/scratchpad/rfaudit/Halleck45_OpenPronounce/assets/"
parts=[]
for f in ["harvard.wav","harvard_2_errors.wav","mispronounced_audio.wav","developer1.wav"]:
    x,sr=sf.read(A+f,dtype="float32")
    if x.ndim>1: x=x.mean(1)
    if sr!=16000: x=np.interp(np.arange(0,len(x),sr/16000),np.arange(len(x)),x).astype("float32")
    parts.append(x)
one=np.concatenate(parts); target=int(sys.argv[2])*16000
audio=np.tile(one, target//len(one)+1)[:target]
name=sys.argv[1]
t=time.time(); m=WhisperModel(name, device="cpu", compute_type="int8", cpu_threads=2); load=time.time()-t
t=time.time(); segs,info=m.transcribe(audio, language="en", word_timestamps=True, vad_filter=True, beam_size=1)
words=sum(len(s.words or []) for s in segs); dt=time.time()-t
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
print(f"{name}: audio={len(audio)/16000:.0f}s load={load:.1f}s transcribe={dt:.1f}s RTF={dt/(len(audio)/16000):.3f} words={words} maxRSS={rss:.0f}MB")
