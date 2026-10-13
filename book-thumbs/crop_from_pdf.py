"""Re-makes chosen thumbnails from their PDFs, cropped exactly to the cover image.
Needs the PDFs to still be in my_pdfs (or pdfs).
Usage: python3 crop_from_pdf.py "Devuni Odilo" "TAZKIYAH" ...
Setup: pip3 install pymupdf pillow"""
import sys, os, re, json, unicodedata, io, fitz
from PIL import Image
def norm(s): return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s)).strip().lower()
pdfs = {}
for folder in ("my_pdfs", "pdfs"):
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(".pdf"): pdfs.setdefault(norm(f), os.path.join(root, f))
books = json.load(open("books.json", encoding="utf-8"))
Z = 2.0
for q in sys.argv[1:]:
    hits = [b for b in books if q.lower() in b["file"].lower()]
    if not hits: print("NOT FOUND:", q)
    for b in hits:
        src = pdfs.get(norm(b["file"])) or pdfs.get(b["drive_id"].lower())
        if not src: print("NO PDF   :", b["file"]); continue
        page = fitz.open(src)[0]; pr = page.rect; clip = None
        try:
            boxes = [fitz.Rect(i["bbox"]) & pr for i in page.get_image_info()]
            boxes = [r for r in boxes if r.get_area() > 0.3 * pr.get_area()]
            if boxes:
                clip = boxes[0]
                for r in boxes[1:]: clip |= r
        except Exception: pass
        pix = page.get_pixmap(matrix=fitz.Matrix(Z, Z), clip=clip)
        img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        how = "cover image" if clip else "edge trim"
        if not clip:  # gentle fallback: trim only near-pure-white edges
            box = img.convert("L").point(lambda p: 255 if p < 250 else 0).getbbox()
            if box: img = img.crop(box)
        img.save(os.path.join("png", b["png"]))
        print(f"done ({how}): {b['png']}  {img.size[0]}x{img.size[1]}")
