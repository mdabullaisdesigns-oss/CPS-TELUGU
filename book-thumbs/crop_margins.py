"""Trims white margins from every PNG in the png folder.
Originals are backed up to png_original first.
Setup: pip3 install pillow      Run: python3 crop_margins.py"""
import os, shutil
from PIL import Image
SRC, BAK = "png", "png_original"
if not os.path.exists(BAK): shutil.copytree(SRC, BAK)
for f in sorted(os.listdir(BAK)):
    if not f.lower().endswith(".png"): continue
    img = Image.open(os.path.join(BAK, f)).convert("RGB")   # always crop from the original
    mask = img.convert("L").point(lambda p: 255 if p < 240 else 0)
    box = mask.getbbox()
    w, h = img.size
    if not box or (box[2]-box[0]) * (box[3]-box[1]) < 0.25 * w * h:
        img.save(os.path.join(SRC, f)); print("kept ", f); continue
    img.crop(box).save(os.path.join(SRC, f)); print("cropped", f)
