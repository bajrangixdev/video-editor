"""Writes FEATURES.txt = the full list of text styles, animations, effects, transitions, layouts, sounds and tags this engine has.
It reads the real code lists, so it is always up to date.  Run it after you add anything:   python list_features.py
(New thing you added?  Add one line for it in the DESCRIPTIONS below so it is explained in the file.)"""
import os, json, datetime
from engine.transitions import KINDS
from engine import planner, sprites, masks, camera, typo

ROOT = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(ROOT, "config.json")))
import re as _re
_files = sorted(f[:-4] for f in os.listdir(os.path.join(ROOT, "assets", "sfx")) if f.endswith(".wav")) if os.path.isdir(os.path.join(ROOT, "assets", "sfx")) else []
sfx = sorted({_re.sub(r"_\d+$", "", f) for f in _files})                     # unique sound names (name_2, name_3 ... are variants of the same sound)

TEXT_STYLES = {
    "caption": "word-by-word captions at the bottom, current word highlighted yellow",
    "neon": "glowing text that types itself with a cursor and pulses   {neon: text}",
    "heavy": "fat yellow italic headline with glow (thumbnail style)   {title: TEXT}  or  {textstyle: heavy}",
    "outline": "hollow white outline letters   {textstyle: outline}",
    "gradient": "pink to yellow gradient letters   {textstyle: gradient}",
    "numbered list": "yellow numbers + white italic text, 1 or 2 columns   {numlist: A | B | C}",
    "handwritten label": "hand-written word with a swirl line that draws itself   {label: Thumbnail}",
    "big counter": "giant glowing number that counts up   {counter: 1575689 | Views}",
}
TECHNIQUES = {   # the 11 techniques of the Decoding YT 'TECHNIQUES USED' slide
    "1 Line Animation": "glowing lines / arrows / frames that draw themselves   {line: x1,y1,x2,y2}  {frame: x,y,w,h}  (also auto under neon text and around the main card)",
    "2 3D Moving Layer": "cards keep swinging in 3D perspective (channel cards, thumbnails, list pills) + tilted dashboards with a sunburst",
    "3 Shake Effect": "camera shake + item shake on impact   {shake: 1}  (auto on number cards, titles, shocked pose)",
    "4 Shine Effect": "a glossy light band sweeps across cards, logos, titles every ~2.5 s",
    "5 Glowing Text": "neon / heavy / gradient text with a pulsing glow",
    "6 Grid Motion BG": "two line grids scrolling at different speeds (parallax)   {fx: mgrid|spot}",
    "7 3D Rotating Logo": "YouTube logo spinning in 3D with shading   {prop: youtube}",
    "8 Number Animation": "numbers count up (small cards and the giant counter) with coin / confetti burst at the end",
    "9 Move Along Path": "any prop or thumbnail flies along a curved path with a glow trail   {fly: youtube|magnifier|bell|thumb}",
    "10 Null Layer": "invisible controller that moves / zooms / rotates a whole group of items together (thumbnail group, list)",
    "11 Head Movement": "the suit character's head tilts, bobs and nods on spoken words, separate from the body",
}
LAYOUT_DOC = {"stat": "number card + character", "channels": "1-3 channel cards", "thumbs": "thumbnail column/row (+label)", "neon": "typing glowing text on ghost grid",
              "list": "check-mark pills", "prop": "magnifier / youtube / bell next to character", "suit": "character + icon", "trio": "three suit characters",
              "icon": "big icon", "screen": "tilted dashboard / screenshot / recording with zoom + highlight", "title": "heavy yellow headline", "numlist": "numbered list (like Techniques Used)",
              "counter": "giant counting number", "fly": "prop flying along a path"}
TAGS = {"stat": "{stat: 20K up}", "char": "{char: crossed|idle|pointing|happy|shocked|thinking}", "who": "{who: suit|hero|trio}", "icon": "{icon: chart}", "tracker": "{tracker: 2}",
        "bubble": "{bubble: ?}", "bg": "{bg: dark|navy|black|purple|blue|teal|wine}", "side": "{side: left|right}", "transition": "{transition: whip|none|...}",
        "screen": "{screen: file.png|file.mp4|demo}", "zoom": "{zoom: x,y,w,h}", "cursor": "{cursor: x,y}", "from": "{from: seconds}", "mark": "{mark: x,y,w,h}", "underline": "{underline: x,y,w}",
        "layout": "{layout: ...}", "channels": "{channels: A|4.5k; B|9k}", "thumbs": "{thumbs: 3}", "neon": "{neon: text}", "textstyle": "{textstyle: neon|heavy|outline|gradient}",
        "title": "{title: TEXT}", "numlist": "{numlist: A | B | C}", "counter": "{counter: 1,575,689 | Views}", "list": "{list: A | B | C}", "label": "{label: Thumbnail}",
        "prop": "{prop: magnifier|youtube|bell}", "fly": "{fly: youtube|magnifier|bell|thumb}", "burst": "{burst: coins|confetti|sparks}", "sfx": "{sfx: coin}", "fx": "{fx: dots|rings|plus|grid|mgrid|rays|ghost|sun|spot}",
        "photo": "{photo: a.jpg | a.jpg|b.jpg | auto}", "photostyle": "{photostyle: full|card}", "kb": "{kb: in|out|left|right|up|down|diag|orbit}", "dof": "{dof: fg|pull|pullfg|none}",
        "parallax": "{parallax: 0..2}", "reveal": "{reveal: circle|diamond|clock|diag|wipe_l|bars_h...}", "focus": "{focus: 0.5,0.45}", "shot": "{shot: push|pull|pan_l|pan_r|tilt_u|tilt_d|drift|punch|orbit|static}",
        "size": "{size: wide|medium|close}", "nophoto": "{nophoto: 1}", "sync": "{sync: 0}  (turn off word-anchoring of list items)",
        "line": "{line: x1,y1,x2,y2,...}", "frame": "{frame: x,y,w,h}", "shake": "{shake: 1}"}
ENTRY = "pop (spring), rise, slide, drop (bounce), spin, flip, zoomin, mask (shape reveal)"; EXIT = "up (drift), down, shrink"

L = []
def H(t): L.extend(["", "=" * 70, t, "=" * 70])
L.append("INCOME VIDEO ENGINE - FEATURES   (written %s by list_features.py)" % datetime.date.today())
H("QUALITY LEVELS  (run.bat: P / H / F / U   or   --quality name)")
for k in ("preview", "hd", "final", "uhd"):
    q = cfg[k]; L.append("  %-8s %dx%d  %dfps  crf %s  preset %s" % (k, q["width"], q["height"], q["fps"], q.get("crf"), q.get("preset")))
L.append("  (lower crf = better quality + bigger file.  'final' 1080p60 is the one to upload to YouTube)")
H("THE 11 TECHNIQUES (Decoding YT 'Techniques Used')")
for k, v in TECHNIQUES.items(): L.append("  %-20s %s" % (k, v))
H("TEXT STYLES")
for k, v in TEXT_STYLES.items(): L.append("  %-18s %s" % (k, v))
H("TRANSITIONS (%d)  - {transition: name}" % len(KINDS))
for k, (T, mode) in KINDS.items(): L.append("  %-8s %.2fs  %-6s  sound: %s" % (k, T, mode, planner.TSFX.get(k, "whoosh")))
H("LAYOUTS (picked automatically, or {layout: name})")
for k in LAYOUT_DOC: L.append("  %-9s %s" % (k, LAYOUT_DOC[k]))
H("ENTRY / EXIT ANIMATIONS")
L.append("  entry: " + ENTRY); L.append("  exit : " + EXIT)
H("BACKGROUNDS")
L.append("  colours: " + ", ".join(sprites.PAL.keys()))
L.append("  moving layers: dots rings plus grid(dot grid) mgrid(line grid) rays ghost(thumbnail grid) sun(sunburst) spot(spotlight)")
H("CAMERA  (v6)")
L.append("  automatic SHOT VARIATION: every scene gets a framing (wide/medium/close) + move (%s); never the same twice in a row" % ", ".join(camera.MOVES))
L.append("  long scenes get a SNAP-ZOOM punch-in on the strongest spoken word;  smooth HANDHELD drift;  TRAUMA SHAKE (decays smoothly) + RGB split on impact")
L.append("  CAMERA MOTION BLUR (sub-frame sampling)  +  2.5D PARALLAX: background / cards / character / foreground move at different speeds")
L.append("  DEPTH OF FIELD: soft background with a focus pull at the start of every scene + foreground bokeh lights")
H("PHOTO ANIMATION  (v6)  - put photos in the  photos  folder")
L.append("  KEN BURNS      smooth zoom + pan over a still photo:  in out left right up down diag orbit          {kb: ...}")
L.append("  2.5D PARALLAX  photo split into back / middle / front layers by a depth map (your own  name_depth.png  or automatic)   {parallax: 0..2}")
L.append("  DEPTH OF FIELD back layer inpainted + blurred, focus pull between front and back                        {dof: fg|pull|pullfg|none}")
L.append("  MASK REVEALS   a shape wipes the next photo in:  " + " ".join(masks.KINDS) + "          {reveal: ...}")
L.append("  CARD MODE      photo in a rounded glowing frame                                                         {photostyle: card}")
L.append("  AUTO           photos in the folder are used automatically in ~75% of the generic scenes (config.json -> photos)")
H("TEXT ANIMATION  (v7)  - {text: Your words} {textfx: ...}")
L.append("  1 kinetic     words fly / slam / spin in, a different move for each word (*word* = accent colour)      {textfx: kinetic}")
L.append("  2 typewriter  terminal panel, letters typed with key clicks, blinking caret                            {textfx: typewriter}")
L.append("  3 glow        neon tube that flickers on, then pulses (cyan -> pink)                                   {textfx: glow}")
L.append("  4 extrude     3D extruded letters, depth grows, light angle swings                                     {textfx: extrude}")
L.append("  5 reveal      colour bar sweeps each line, then uncovers the text                                      {textfx: reveal}")
L.append("  6 tracking    letter-spacing animates wide -> tight with blur-in                                       {textfx: tracking}")
L.append("  7 bounce      letters drop with bounce + squash, then a jumping wave                                   {textfx: bounce}")
L.append("  8 shake       slam + shake bursts with red/cyan split (bursts land on emphasised words)                {textfx: shake}")
L.append("  9 morph       one text melts into the next (liquid blob morph).  {text: A -> B -> C}                    {textfx: morph}")
L.append(" 10 mask        text is a window onto moving colour or a photo                                           {textfx: mask} {textfill: photo.jpg|aurora}")
L.append(" 11 rotate3d    solid extruded text spinning in real 3D perspective                                      {textfx: rotate3d}")
L.append(" 12 path        letters ride a path: " + " ".join(typo.PATHS) + "                                {textfx: path} {textpath: wave}")
L.append(" 13 liquid      water-like distortion + colour fringe that settles                                       {textfx: liquid}")
L.append(" 14 shine       gold text with a light sweep + sparkles                                                  {textfx: shine}")
L.append(" 15 subtitles   animated captions: " + " | ".join(typo.CAPTION_STYLES) + "     {captions: pop}   (default in config.json -> caption_style)")
L.append("  extras: {textcolor: 255,200,40}  {textsize: 1.3}   {textfx: auto} picks a different effect each scene.  Every effect plays its own sound effects + camera hits.")
H("AUDIO  (v6)")
L.append("  AUDIO-SYNCED ANIMATION: items appear when the narrator SAYS them; captions pop harder on emphasised words;")
L.append("    camera punches on emphasis; character / icons bob with the voice loudness")
L.append("  SOUND: stereo, %d sounds (%d files incl. variants - the mixer picks one at random), tiny random pitch/volume, panned to the picture, " % (len(sfx), len(_files)) + "ducked under the voice,")
L.append("    reverb on big hits, attack aligned to the visual hit, voice high-pass + compressor, optional MUSIC BED (assets/music, auto-ducks), mastered to -14 LUFS")
H("SMOOTHNESS  (v6)")
L.append("  sub-pixel placement for everything (no 1-pixel stutter), spring physics on pops, per-item + camera motion blur, scrolling layers at float precision, light film grain (kills banding)")
L.append("  turn effects off in config.json -> effects, or add --fast for the quickest test render")
H("PROPS / ICONS / CHARACTER POSES")
L.append("  props: " + ", ".join(planner.PROPS) + "     icons: " + ", ".join(planner.ICONS))
L.append("  suit poses: idle crossed pointing happy shocked thinking     (own art: assets/characters/suit/<pose>.png)")
H("BURSTS")
L.append("  coins (money) | confetti (increase) | sparks (decrease)   + shock ring")
H("SOUND EFFECTS (%d)   assets/sfx/*.wav  - replace any with your own" % len(sfx))
L.append("  " + ", ".join(sfx))
H("ALL SCRIPT TAGS")
for k, v in TAGS.items(): L.append("  %-11s %s" % (k, v))
H("HOW TO ADD A NEW THING")
L.append("  1) add the code (engine/*.py)   2) add one line in list_features.py   3) run:  venv\\Scripts\\python.exe list_features.py")
open(os.path.join(ROOT, "FEATURES.txt"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("FEATURES.txt written (%d lines)" % len(L))
