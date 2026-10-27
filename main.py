import argparse, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import script_parser, timing, planner, render
from engine.util import ROOT

ap = argparse.ArgumentParser(description="Income Video Engine: script -> animated cartoon video")
ap.add_argument("script", nargs="?", help="script .txt file")
ap.add_argument("--audio", help="your own narration (mp3/wav). Without it an AI voice is used")
ap.add_argument("--out", help="output mp4")
ap.add_argument("--preview", action="store_true", help="fast 720p test render")
ap.add_argument("--quality", choices=["preview", "hd", "final", "uhd"], help="preview=720p30  hd=1080p30  final=1080p60 (best for YouTube)  uhd=1440p60")
ap.add_argument("--seed", type=int, default=1, help="change for a different edit of the same script")
ap.add_argument("--voice")
ap.add_argument("--fast", action="store_true", help="turn off motion blur / depth of field / parallax for the quickest possible test render")
ap.add_argument("--timeline", help="render an edited timeline.json instead of planning again")
a = ap.parse_args()
cfg = json.load(open(os.path.join(ROOT, "config.json")))
if a.voice: cfg["voice"] = a.voice
qname = a.quality or ("preview" if a.preview else "final"); q = cfg[qname]
os.makedirs(os.path.join(ROOT, "output"), exist_ok=True)
work = os.path.join(ROOT, "output", "_work")

if a.timeline:
    data = json.load(open(a.timeline)); tl, total = data["timeline"], data["total"]
    import numpy as np
    narr = timing.decode(data["narration"]) if data.get("narration") and os.path.exists(data["narration"]) else np.zeros(int(total * 44100), np.float32)
    base = os.path.splitext(os.path.basename(a.timeline))[0]
else:
    if not a.script: ap.error("give a script file")
    scenes = script_parser.parse(open(a.script, encoding="utf-8").read(), cfg.get("beats", True))
    print("Scenes:", len(scenes))
    scenes, narr = timing.get(scenes, a.audio, cfg, work)
    tl = planner.plan(scenes, a.seed, cfg.get("captions", True), narr, dict(cfg.get("photos", {}), caption_style=cfg.get("caption_style", "karaoke"))); total = scenes[-1]["t1"]
    base = os.path.splitext(os.path.basename(a.script))[0] + "_s%d" % a.seed
    import wave
    nar_path = os.path.join(ROOT, "output", base + "_narration.wav")
    with wave.open(nar_path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100); w.writeframes((narr * 32767).astype("int16").tobytes())
    tpath = os.path.join(ROOT, "output", base + "_timeline.json")
    json.dump({"total": total, "narration": nar_path, "timeline": tl}, open(tpath, "w"), indent=1)
    print("Timeline saved (edit it, then use --timeline):", tpath)
out = a.out or os.path.join(ROOT, "output", base + ("" if qname == "final" else "_" + qname) + ".mp4")
t0 = time.time()
fx_ = cfg.get("effects", {}); opts = dict(mb=fx_.get("motion_blur", True), mb_samples=q.get("mb_samples", fx_.get("mb_samples", 5)), dof=fx_.get("depth_of_field", True),
                                           parallax=fx_.get("parallax", True), bokeh=fx_.get("bokeh", True), grain=fx_.get("grain", 0.6))
if a.fast: opts.update(mb=False, dof=False, parallax=False, bokeh=False, grain=0)
render.render(tl, total, narr, out, q["width"], q["height"], q["fps"], qname == "preview", work, q.get("crf"), q.get("preset"), opts, cfg.get("audio", {}))
print("Took %.0f s" % (time.time() - t0))
