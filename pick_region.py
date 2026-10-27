"""Click-and-drag on a screenshot to get the {zoom: ...} tag.   Usage: venv\\Scripts\\python.exe pick_region.py screenshot.png"""
import sys
import tkinter as tk
from PIL import Image, ImageTk
if len(sys.argv) < 2: sys.exit("usage: pick_region.py image.png")
im = Image.open(sys.argv[1]).convert("RGB"); sc = min(1.0, 1100 / im.width, 700 / im.height)
sh = im.resize((int(im.width * sc), int(im.height * sc)))
root = tk.Tk(); root.title("Drag a box around the part to zoom into, then close the window")
cv = tk.Canvas(root, width=sh.width, height=sh.height); cv.pack(); tkimg = ImageTk.PhotoImage(sh); cv.create_image(0, 0, anchor="nw", image=tkimg)
st = {}
def down(e): st["a"] = (e.x, e.y); st["r"] = cv.create_rectangle(e.x, e.y, e.x, e.y, outline="magenta", width=3)
def move(e): cv.coords(st["r"], st["a"][0], st["a"][1], e.x, e.y)
def up(e):
    x0, y0 = st["a"]; x1, y1 = e.x, e.y; x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1))
    print("{zoom: %.3f,%.3f,%.3f,%.3f}" % (x0 / sh.width, y0 / sh.height, (x1 - x0) / sh.width, (y1 - y0) / sh.height))
cv.bind("<ButtonPress-1>", down); cv.bind("<B1-Motion>", move); cv.bind("<ButtonRelease-1>", up); root.mainloop()
