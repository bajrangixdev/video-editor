"""Creates the built-in sound effects (v6 - studio-style synthesis).  Replace any .wav in assets/sfx with your own anytime
(name_2.wav, name_3.wav ... are extra VARIANTS of the same sound - the mixer picks one at random and shifts the pitch a little).
Run again any time:  python make_assets.py"""
import os, wave, numpy as np
sr = 44100; here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "sfx"); os.makedirs(here, exist_ok=True)
for f in os.listdir(here):
    if f.endswith(".wav"): os.remove(os.path.join(here, f))
TAU = 2 * np.pi
def T(sec): return np.arange(int(sec * sr)) / sr
def rs(seed): return np.random.RandomState(seed)
def expd(t, k): return np.exp(-t * k)
def fade(x, fi=0.0008, fo=0.004):
    x = x.copy(); a, b = int(fi * sr), int(fo * sr)
    if a: x[:a] *= np.linspace(0, 1, a)
    if b: x[-b:] *= np.linspace(1, 0, b)
    return x
def fft_filter(x, kind, fc, order=2):
    N = 1 << (len(x) - 1).bit_length(); S = np.fft.rfft(x, N); f = np.fft.rfftfreq(N, 1 / sr) + 1e-9
    H = 1 / (1 + (f / fc) ** (2 * order)) if kind == "lp" else 1 / (1 + (fc / f) ** (2 * order))
    return np.fft.irfft(S * H, N)[:len(x)]
def lp(x, fc, o=2): return fft_filter(x, "lp", fc, o)
def hp(x, fc, o=2): return fft_filter(x, "hp", fc, o)
def bp(x, lo, hi): return hp(lp(x, hi), lo)
def svf(x, fc, qinv=0.35):
    """swept band-pass (state variable filter) - the heart of a good whoosh"""
    f = 2 * np.sin(np.pi * np.minimum(fc, 9000) / sr); low = band = 0.0; out = np.zeros(len(x))
    for i in range(len(x)):
        low += f[i] * band; high = x[i] - low - qinv * band; band += f[i] * high; out[i] = band
    return out
def bell(f0, t, decay, partials=((1, 1.0), (2.76, 0.5), (5.4, 0.3), (8.93, 0.16))):
    return sum(a * np.sin(TAU * f0 * r * t) * expd(t, decay * (1 + 0.55 * (r - 1) / 3)) for r, a in partials)
def tanh_drive(x, d): return np.tanh(x * d) / np.tanh(d)
def mixin(base, x, at):
    i = int(at * sr); n = min(len(x), len(base) - i)
    if n > 0: base[i:i + n] += x[:n]
    return base
def save(name, x, peak=0.92):
    x = fade(np.asarray(x, float)); x = x - x.mean() * 0.5; x = x / (np.abs(x).max() + 1e-9) * peak
    with wave.open(os.path.join(here, name + ".wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((x * 32767).astype(np.int16).tobytes())

# ------------------------------------------------------------------ UI: pop / pluck / tick / click / key
for i, f0 in enumerate((820, 700, 960, 760)):
    t = T(0.16); f = 340 + (f0 - 340) * expd(t, 55); ph = np.cumsum(f) / sr * TAU
    x = np.sin(ph) * expd(t, 30) + 0.25 * np.sin(ph * 2) * expd(t, 60) + 0.35 * rs(i).randn(len(t)) * expd(t, 400)
    save("pop" if i == 0 else "pop_%d" % (i + 1), x)
for i, f0 in enumerate((523.25, 587.33, 659.25, 783.99, 880.0)):                       # soft marimba-like pluck on a pentatonic scale
    t = T(0.45); x = np.sin(TAU * f0 * t) * expd(t, 9) + 0.32 * np.sin(TAU * f0 * 3.9 * t) * expd(t, 22) + 0.12 * np.sin(TAU * f0 * 9.2 * t) * expd(t, 45)
    x += 0.25 * rs(i + 20).randn(len(t)) * expd(t, 300); save("pluck" if i == 0 else "pluck_%d" % (i + 1), lp(x, 7000))
for i, f0 in enumerate((3000, 3500, 2600)):
    t = T(0.03); save("tick" if i == 0 else "tick_%d" % (i + 1), np.sin(TAU * f0 * t) * expd(t, 230) + 0.3 * rs(i + 30).randn(len(t)) * expd(t, 500))
for i in range(2):
    t = T(0.07); x = bp(rs(40 + i).randn(len(t)), 1500, 6000) * expd(t, 160) + np.sin(TAU * (1700 + 300 * i) * t) * expd(t, 260) * 0.7
    save("click" if i == 0 else "click_2", x)
for i in range(4):                                                                       # keyboard: bright tick + low 'thock'
    t = T(0.07); r = rs(50 + i); x = bp(r.randn(len(t)), 1800 + 500 * i, 5200) * expd(t, 190) + np.sin(TAU * (190 + 25 * i) * t) * expd(t, 70) * 0.9
    save("key" if i == 0 else "key_%d" % (i + 1), x)
for i in range(2):
    t = T(0.11); x = np.sin(TAU * (130 - 20 * i) * t) * expd(t, 45) + bp(rs(60 + i).randn(len(t)), 800, 4500) * expd(t, 220) * 0.7; save("cut" if i == 0 else "cut_2", x)
for i in range(2):
    t = T(0.12); x = bp(rs(70 + i).randn(len(t)), 2200, 7000) * expd(t, 90) + np.sin(TAU * (1250 + 150 * i) * t) * expd(t, 110) * 0.5; save("snap" if i == 0 else "snap_2", x)

# ------------------------------------------------------------------ MOTION: whoosh / swish / slide / riser / reveal
for i, (dirn, dur) in enumerate((("up", 0.5), ("down", 0.55), ("up", 0.42))):
    t = T(dur); n = rs(80 + i).randn(len(t)); u_ = t / t[-1]; env = np.sin(np.pi * u_ ** (0.8 if dirn == "up" else 1.25)) ** 2
    fc = (300 + 3800 * u_ ** 1.5) if dirn == "up" else (4200 - 3600 * u_ ** 0.8)
    x = svf(n, fc, 0.30) * env * 1.6 + lp(n, 220) * 0.6 * env
    save("whoosh" if i == 0 else "whoosh_%d" % (i + 1), x)
for i in range(3):
    t = T(0.28); n = rs(90 + i).randn(len(t)); u_ = t / t[-1]; env = np.sin(np.pi * u_ ** 0.7) ** 1.6
    x = svf(n, 1500 + 6000 * u_ ** (1 + 0.3 * i), 0.28) * env * 1.5
    save("swish" if i == 0 else "swish_%d" % (i + 1), x)
for i in range(2):
    t = T(0.42); n = rs(100 + i).randn(len(t)); u_ = t / t[-1]; env = np.sin(np.pi * u_) ** 2
    x = svf(n, (500 + 1500 * u_) if i == 0 else (2000 - 1200 * u_), 0.5) * env * 1.4 + 0.3 * np.sin(TAU * 140 * t) * env; save("slide" if i == 0 else "slide_2", x)
t = T(1.0); n = rs(110).randn(len(t)); u_ = t / t[-1]                                  # riser: rising filtered noise + harmonic tone, ends clean
x = svf(n, 250 + 5200 * u_ ** 2.2, 0.4) * (u_ ** 1.8) * 1.5 + np.sin(np.cumsum(180 + 900 * u_ ** 2) / sr * TAU) * 0.35 * u_ ** 2
save("riser", x * np.minimum(1, (1 - u_) * 18 + 0.0))
for i in range(2):                                                                      # soft 'reveal': air + rising chime
    t = T(0.55); n = rs(120 + i).randn(len(t)); u_ = t / t[-1]; env = np.sin(np.pi * u_ ** 0.8) ** 2
    x = svf(n, 1200 + 2600 * u_, 0.6) * env * 0.9 + np.sin(np.cumsum(520 * (1 + 0.5 * u_ ** 0.7 + 0.5 * i)) / sr * TAU) * 0.3 * env * expd(t, 2.2)
    save("reveal" if i == 0 else "reveal_2", x)

# ------------------------------------------------------------------ IMPACTS: hit / boom / impact / rumble
# (phone-speaker friendly: sub-bass for headphones + a driven 'body' sweep and mid noise so the punch is audible on small speakers too)
def thump(t, f_hi, f_lo, k_sweep, k_dec, drive, sub=0.7, seed=0, mid=0.5, crack=0.35):
    f = f_lo + (f_hi - f_lo) * expd(t, k_sweep); ph = np.cumsum(f) / sr * TAU
    body = tanh_drive(np.sin(ph) * expd(t, k_dec), drive)                                    # driven -> harmonics 200-900 Hz
    subb = np.sin(TAU * 44 * t) * expd(t, k_dec * 0.7) * sub
    midn = bp(rs(seed).randn(len(t)), 160, 1800) * expd(t, k_dec * 3.4) * mid * 3.4      # (band-passed noise is quiet: x3.4 restores its level)
    crk = hp(rs(seed + 1).randn(len(t)), 2500) * expd(t, 110) * crack
    return body + subb + midn + crk
for i in range(2):
    t = T(0.5); save("hit" if i == 0 else "hit_2", thump(t, 190 - 30 * i, 62, 30, 9.0 + 2 * i, 3.2, 0.55, 130 + i))
t = T(1.2); save("boom", thump(t, 300, 105, 14, 4.2, 4.0, 0.30, 140, 0.8, 0.25))
for i in range(2):
    t = T(1.0); x = thump(t, 340, 115, 20, 5.6, 4.0, 0.22, 150 + i, 0.9, 0.55) + 0.45 * bell(210 + 35 * i, t, 7, ((1, 1), (1.5, .4), (2.3, .3)))
    save("impact" if i == 0 else "impact_2", tanh_drive(x, 1.3))
t = T(0.8); n = lp(rs(160).randn(len(t)), 320, 3); am = 0.6 + 0.4 * np.sin(TAU * 17 * t); u_ = t / t[-1]          # camera-shake rumble (has 100-300 Hz so phones hear it)
save("rumble", (n + 0.6 * lp(rs(161).randn(len(t)), 110, 3)) * am * np.sin(np.pi * u_ ** 0.6) ** 1.2 * 4)

# ------------------------------------------------------------------ MONEY / SPARKLE: ding / coin / sparkle / shimmer / count
for i, f0 in enumerate((1568.0, 1318.5)):
    t = T(0.9); save("ding" if i == 0 else "ding_2", bell(f0, t, 5.2) * np.minimum(1, t * 3000))
for i in range(2):
    t = T(0.6); x = np.zeros(len(t)); a, b = (1318.5, 1976.0) if i == 0 else (1396.9, 2093.0)
    x += bell(a, t, 22, ((1, 1), (2.0, 0.4), (3.0, 0.2))) * (t < 0.085); y = bell(b, t - 0.07, 6.5, ((1, 1), (2.0, 0.45), (3.0, 0.25))) * (t >= 0.07) * np.minimum(1, np.maximum(0, t - 0.07) * 2000)
    x += y; x += 0.25 * hp(rs(170 + i).randn(len(t)), 5000) * expd(t, 150) * (t < 0.04); save("coin" if i == 0 else "coin_2", x)
for i in range(3):
    t = T(0.9); x = np.zeros(len(t)); r = rs(180 + i); scale = [1, 9 / 8, 5 / 4, 3 / 2, 5 / 3]
    for s0 in np.sort(r.uniform(0, 0.5, 11)):
        f0 = 2093 * r.choice(scale) * r.choice([1, 1, 2]); tt = t[:len(t) - int(s0 * sr)]
        mixin(x, bell(f0, tt, 14, ((1, 1), (2.76, 0.35), (5.4, 0.15))) * r.uniform(0.3, 1.0), s0)
    save("sparkle" if i == 0 else "sparkle_%d" % (i + 1), x)
for i in range(2):                                                                      # ascending chime run
    t = T(1.0); x = np.zeros(len(t)); notes = [1047, 1319, 1568, 2093, 2637, 3136] if i == 0 else [1175, 1480, 1760, 2349, 2960]
    for j, f0 in enumerate(notes): mixin(x, bell(f0, t[:len(t) - int((0.05 * j) * sr)], 9, ((1, 1), (2.76, 0.3), (5.4, 0.12))) * (0.55 + 0.1 * j), 0.05 * j)
    save("shimmer" if i == 0 else "shimmer_2", x)
t = T(0.9); x = np.zeros(len(t)); tk = 0.0; step = 0.085; k = 0                         # number counting: ticks that speed up and rise
while tk < 0.82:
    f0 = 1000 + 1900 * (tk / 0.82) ** 1.2; n_ = int(0.03 * sr); tt = np.arange(n_) / sr
    mixin(x, (np.sin(TAU * f0 * tt) * expd(tt, 190) + 0.25 * rs(190 + k).randn(n_) * expd(tt, 420)) * (0.6 + 0.4 * tk / 0.82), tk); tk += step; step = max(0.032, step * 0.9); k += 1
save("count", x)

# ------------------------------------------------------------------ TEXTURES: glitch / zap / shutter / ripple
for i in range(3):
    t = T(0.38); r = rs(200 + i); x = np.zeros(len(t)); pos = 0.0
    while pos < 0.33:
        ln = r.uniform(0.012, 0.045); n_ = int(ln * sr); tt = np.arange(n_) / sr; kind = r.randint(3)
        seg = (np.sign(np.sin(TAU * r.uniform(200, 1800) * tt)) * 0.6 if kind == 0 else np.round(r.randn(n_) * 3) / 3 * 0.7 if kind == 1 else np.sin(TAU * r.uniform(900, 4000) * tt) * 0.7)
        mixin(x, seg * np.minimum(1, np.minimum(tt * 3000, (ln - tt) * 3000)) * r.uniform(0.5, 1), pos); pos += ln + r.uniform(0, 0.03)
    save("glitch" if i == 0 else "glitch_%d" % (i + 1), x * expd(t, 2.2))
for i in range(2):
    t = T(0.32); f = 2800 * expd(t, 8 + 3 * i) + 120; ph = np.cumsum(f) / sr * TAU
    x = np.sin(ph + 2.2 * np.sin(ph * 0.5)) * expd(t, 9) * 0.8 + bp(rs(210 + i).randn(len(t)), 1500, 9000) * expd(t, 26) * 0.6; save("zap" if i == 0 else "zap_2", x)
for i in range(2):                                                                      # camera shutter: two mechanical clicks
    t = T(0.22); x = np.zeros(len(t))
    for s0, a in ((0.0, 1.0), (0.085 + 0.01 * i, 0.7)):
        n_ = int(0.05 * sr); tt = np.arange(n_) / sr; mixin(x, (bp(rs(220 + i).randn(n_), 900, 6500) * expd(tt, 140) + np.sin(TAU * 210 * tt) * expd(tt, 120) * 0.8) * a, s0)
    save("shutter" if i == 0 else "shutter_2", x)
for i in range(2):                                                                      # water ripple: three rising droplets
    t = T(0.7); x = np.zeros(len(t))
    for j, s0 in enumerate((0.0, 0.16, 0.34)):
        n_ = int(0.22 * sr); tt = np.arange(n_) / sr; f = (500 + 320 * j + 120 * i) * (1 + 1.4 * tt); mixin(x, np.sin(np.cumsum(f) / sr * TAU) * expd(tt, 17) * (1 - 0.25 * j), s0)
    save("ripple" if i == 0 else "ripple_2", lp(x, 6000))
t = T(2.2); u_ = t / t[-1]; x = sum(np.sin(TAU * f * t + k_) * a for k_, (f, a) in enumerate(((130.8, 1), (164.8, .8), (196, .8), (261.6, .5))))       # gentle swell (for endings)
save("swell", x * np.sin(np.pi * u_ ** 1.6) ** 1.5 * (1 + 0.0 * u_))
print("sound effects ready:", len([f for f in os.listdir(here) if f.endswith(".wav")]), "files")
