INCOME VIDEO ENGINE  -  v7  (text edition)
==========================================
NEW IN v7: 15 TEXT ANIMATIONS + ANIMATED SUBTITLES.  Demo script: samples\text_demo.txt
  {text: Your words} {textfx: kinetic|typewriter|glow|extrude|reveal|tracking|bounce|shake|morph|mask|rotate3d|path|liquid|shine}
  morph: {text: Views -> Money -> Freedom}     path: {textpath: wave|arc|circle|spiral|sline}     mask: {textfill: photo.jpg}
  accent word: *word*     colour: {textcolor: 255,200,40}     size: {textsize: 1.3}     {textfx: auto} = a different effect every scene
  SUBTITLES: {captions: karaoke|pop|bar|glow|classic|off} per scene, or set  config.json -> "caption_style"  (default karaoke).
  Each effect has matching sound effects and camera hits (shake lands on emphasised words).  Full list: FEATURES.txt  (run list_features.py)

----- v6 (smooth edition) -----
WHAT IS NEW IN v6  (full list in FEATURES.txt)
  PHOTO ANIMATION   put photos in the  photos  folder.  Ken Burns zoom/pan, 2.5D parallax (depth layers), depth of field with focus pull,
                    mask reveals, card mode.  Script tags:  {photo: a.jpg}  {photo: a.jpg|b.jpg}  {kb: orbit}  {dof: pull}  {reveal: circle}  {photostyle: card}
                    (see photos\README_PHOTOS.txt).  Photos already in the folder are used automatically.  Demo:  samples\photo_demo.txt
  CAMERA            automatic shot variation (wide/medium/close + push/pull/pan/tilt/drift/punch/orbit), snap-zoom punch-ins on emphasised words,
                    handheld drift, smooth trauma shake, camera + object MOTION BLUR, parallax between layers, depth-of-field + bokeh.
  TRANSITIONS       23 kinds. Chosen from what the NEXT scene is (stat -> flash/zoom, screen -> iris/diag, channels -> blinds/split, photo -> dissolve/zoom-through ...).
                    The old scene keeps MOVING during the transition (v5 froze it).  New: slide, zoomthru, diag, diamond, clock, bars, dissolve, rgb.
  AUDIO-SYNC        list items / channel cards appear when the narrator SAYS them, captions pop harder on emphasised words, camera punches on them,
                    the character and icons bob with the voice.
  SOUND             all effects re-made (no clicks, fuller impacts, bells, swept whooshes) with 2-5 variants each; stereo, panned to the picture, ducked under
                    the voice, reverb on big hits, voice cleaned + compressed, optional music bed (drop a file into assets\music), mastered to -14 LUFS.
  SMOOTHNESS        everything moves at sub-pixel precision (v5 moved in 1-pixel steps = shimmer), spring physics for pops, motion blur, light film grain.
UPDATING FROM v5:  1) run  install.bat  again (adds OpenCV)   2) venv\Scripts\python.exe make_assets.py   3) old timeline.json files still render.
SPEED: v6 renders about 1.7x slower than v5 (more work per frame).  Use  --fast  or  config.json -> effects  to switch heavy effects off for quick tests.
SETTINGS: config.json -> "effects" (motion_blur, depth_of_field, parallax, bokeh, grain), "photos" (auto_photos, photo_chance), "audio" (sfx_volume, reverb, music_volume, loudness).
MUSIC: put any .mp3/.wav in  assets\music  - it is looped, faded in/out and automatically lowered while the voice speaks.

1) Double-click  install.bat   (one time; installs Python, FFmpeg, packages)
2) Double-click  run.bat       (drag your script, choose preview or final)
   Your video + an editable timeline.json appear in the "output" folder.

YOUR SCRIPT (a .txt file)
-------------------------
[scene name]
Narration text for this scene. {stat: 20K up} {char: happy} {bubble: ?}

Tags are optional. Anything you leave out, the engine decides itself.
  {stat: 20K up}      money/number card with green up or red down arrow
  {char: happy}       pose: idle thinking happy shocked pointing   ({char: none} = no character)
  {side: left}        which side the character stands on
  {bubble: text}      speech bubble
  {icon: money}       big glowing icon: audience chart click comment growth brain money
  {tracker: 3}        highlight icon 3 in the top progress bar
  {bg: purple}        background: purple blue teal wine
Lines without any [scene] header are each treated as their own scene.
Words like "plan number 2", "step 3", "sign one" automatically move the top tracker.
Numbers like "20000 rupees" automatically create a number card.

TRANSITIONS AND ANIMATION STYLES
--------------------------------
Between scenes the engine picks a transition automatically (never the same twice in a row, sometimes a plain cut):
   wipe zoom glitch dip push iris  +NEW:  whip (motion-blur whip pan)  blinds  pixel  flash  twist (spin-zoom)  ripple (water wave)  split (opens like doors)
Force one on a scene (the transition goes INTO that scene):   {transition: glitch}     {transition: none}
Cards, character, icons, bubbles and screen shots also enter with changing styles
(pop, rise, slide, drop-with-bounce, spin, flip, zoom-in) and leave in changing ways (up, down, shrink).
Change style number in run.bat for a new combination, or edit "style", "exit" and "kind" in timeline.json by hand.
New sounds (hit, glitch) are made by make_assets.py - if you updated an old install, run:  venv\Scripts\python.exe make_assets.py

COMPUTER SHOTS (screenshots / screen recordings)
------------------------------------------------
Put your screenshot (.png/.jpg) or screen recording (.mp4) in the  screens  folder, then in the script:
   [analytics]
   Look at this audience number. {screen: studio.png} {zoom: 0.60,0.30,0.25,0.20}
   {screen: demo}            shows a built-in fake dashboard (for testing)
   {zoom: x,y,w,h}           region to zoom into, as fractions of the screen (0 to 1). A neon box
                             highlights it, the cursor moves there, clicks, and the view zooms in.
   {cursor: x,y}             where the cursor goes (default = centre of the zoom region)
   {from: 12}                for recordings: start playing from second 12 of the clip
Without {zoom} the shot just shows the screen with a slow push-in.
To find the zoom numbers easily:
   venv\Scripts\python.exe pick_region.py screens\studio.png
   drag a box on the picture; it prints the {zoom: ...} tag to copy.

VOICE
-----
- No audio given  -> AI voice (edge-tts, needs internet). Change voice in config.json
  (example Hindi: hi-IN-SwaraNeural, India English: en-IN-NeerjaNeural).
- Your own audio  -> drag it in run.bat. Words are timed with Whisper
  (first run downloads a small model, needs internet once).
- If the voice cannot be made, a SILENT video with estimated timing is rendered.

DIFFERENT EDIT EVERY TIME
-------------------------
Same script + different "edit style number" = different backgrounds, motion styles, sides.

EDIT BY HAND (this is the "editor")
-----------------------------------
Open output\<name>_timeline.json. Every item has start, dur, layer, type.
Change times, delete items, switch pose/style, then render again:
   venv\Scripts\python.exe main.py --timeline output\<name>_timeline.json

USE YOUR OWN CARTOON ART
------------------------
Put transparent PNGs in  assets\characters\hero\  named:
   idle.png thinking.png happy.png shocked.png pointing.png
They replace the built-in placeholder character automatically.
Replace assets\sfx\pop.wav, ding.wav, whoosh.wav with your own sounds anytime.

SPEED
-----
Preview (854x480, 30fps) renders about as fast as the video length or faster.
Final 1080p 60fps is slower (roughly 5-10x the video length on a normal PC).

ANIMATION NUMBERS (engine/render.py top): IN=0.45s entry, OUT=0.35s exit, DRIFT=0.13 upward move.


NEW EFFECTS (v2)
----------------
- Moving backgrounds: floating glow dots, rings, plus signs, scrolling dot grid, sweeping light rays (random mix per scene; edit "fx" in timeline.json: dots rings plus grid rays).
- Camera: slow push-in / pull-out every scene, a punch + screen shake + RGB split when a number card or shocked pose appears.
- Number cards count up (0 -> 20000) and burst with coins (money), confetti (up) or sparks (down). Force with  {burst: coins|confetti|sparks}  on any scene.
- Character bounces and sways while talking, icons float, bubbles wobble, vignette on the whole frame.

SOUND EFFECTS (all placed automatically; files are in assets\sfx, replace any with your own .wav)
------------------------------------------------------------------------------------------------
pop (character/card in)   ding (tracker)   whoosh (wipe/push/screen in)   hit (zoom, shocked)   glitch (glitch)
coin (money burst)   sparkle (confetti)   zap (sparks, pixel)   count (number counting up)   boom (camera punch, flash)
shutter (blinds, split)   swish (whip, zoom-in on screen)   riser (dip, iris, twist)   ripple (ripple)   click (cursor click)
Add one by hand on any scene:  {sfx: coin}   (any wav name in assets\sfx).  Volume/time: edit "sfx" items in timeline.json.
After updating, run once:  venv\Scripts\python.exe make_assets.py

PRO EDIT PACK (v4)  -  makes videos in the style of fast "Decoding YT" edits
----------------------------------------------------------------------------
BEATS: every sentence becomes its own scene (new visual every ~3-4 s). Turn off with  "beats": false  in config.json.
Bottom captions can be hidden with  "captions": false.
The engine picks a LAYOUT per scene from your tags, then from words in the narration, then rotates so no two look alike.
Force one with  {layout: channels|thumbs|neon|list|screen|stat|suit|prop|icon|trio}  or use the tags below:
  {channels: Your Channel|4.5k; Channel No2|21.3k; Channel No3|9.9k}   1-3 channel cards, middle one glows
  {thumbs: 3}  or  {thumbs: row}     thumbnail column / row, middle one pink + glowing
  {label: Thumbnail}                 hand-written word with a swirl line that draws itself
  {neon: text to type}               glowing text that types itself (default = the narration) on a ghost-thumbnail grid
  {list: Point one | Point two | Point three}   check-mark pills that pop in one by one
  {prop: magnifier|youtube|bell}     big prop next to the character
  {who: suit|hero|trio}              suit = YouTube-logo-head character (default), trio = three of them, hero = old character
  {char: crossed|idle|pointing|happy|shocked|thinking}   pose (suit has "crossed" arms)
Screens (tilted in 3D with a sunburst behind):
  {screen: studio.png} {zoom: x,y,w,h}   as before, plus automatic marker highlight + red underline on the zoom area
  {mark: x,y,w,h}   {underline: x,y,w}   your own highlights (fractions 0-1 of the screenshot; shown when the zoom happens)
  Words like analytics / dashboard / audience automatically show the demo dashboard.
Own art: put transparent PNGs in assets\characters\suit\  (idle crossed pointing happy shocked thinking .png) to replace the suit character.
New sound: key (typing ticks).  Run make_assets.py once after updating.
Sample: samples\pro_demo.txt

QUALITY (v5)
------------
run.bat asks:  P = quick 720p test | H = HD 1080p 30fps | F = BEST 1080p 60fps (slow, upload this to YouTube) | U = 1440p 60fps
Command line:  python main.py script.txt --quality final      (preview / hd / final / uhd).  Settings in config.json (width, height, fps, crf, preset).
Tip: write and check everything with P, then render once with F.  Use a real narration (--audio) or the AI voice - both are used at full quality.

THE 11 TECHNIQUES + FULL FEATURE LIST
-------------------------------------
Open FEATURES.txt - it lists every text style, animation, effect, transition, layout, sound and script tag.
After you add something new run:  venv\Scripts\python.exe list_features.py   (it rewrites FEATURES.txt from the code).
Demo of all 11 techniques: samples\techniques_demo.txt
