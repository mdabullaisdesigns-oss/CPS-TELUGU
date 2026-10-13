import json, os, re, unicodedata, fitz
os.makedirs("png", exist_ok=True)
def norm(s): return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s)).strip().lower()
found = {}
for root, _, files in os.walk("my_pdfs"):
    for f in files:
        if f.lower().endswith(".pdf"): found[norm(f)] = os.path.join(root, f)
missing = []
for b in json.load(open("books.json", encoding="utf-8")):
    src = found.get(norm(b["file"]))
    out = os.path.join("png", re.sub(r'[\\/:*?"<>|]', "_", b["png"]))
    if os.path.exists(out): continue
    if not src: missing.append(b["file"]); continue
    try:
        fitz.open(src)[0].get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(out)
        print("OK  ", out)
    except Exception as e:
        print("FAIL", b["file"], e)
print("\nPDFs not found in my_pdfs:", *missing, sep="\n  ")
