"""Downloads each PDF from Google Drive and saves page 1 as <book name>.png
Setup:  pip install gdown pymupdf
Run:    python make_thumbnails.py
Requires the Drive files to be shared "Anyone with the link"."""
import json, os, re, gdown, fitz
os.makedirs("pdfs", exist_ok=True); os.makedirs("png", exist_ok=True)
for b in json.load(open("books.json", encoding="utf-8")):
    out = os.path.join("png", re.sub(r'[\\/:*?"<>|]', "_", b["png"]))
    if os.path.exists(out): continue
    pdf = os.path.join("pdfs", b["drive_id"] + ".pdf")
    try:
        if not os.path.exists(pdf):
            gdown.download(id=b["drive_id"], output=pdf, quiet=True)
        doc = fitz.open(pdf)
        doc[0].get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(out)
        print("OK  ", out)
    except Exception as e:
        print("FAIL", b["file"], e)
