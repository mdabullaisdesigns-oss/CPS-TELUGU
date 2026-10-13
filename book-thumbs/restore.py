import sys, os, shutil
for q in sys.argv[1:]:
    hits = [f for f in os.listdir("png_original") if q.lower() in f.lower()]
    if not hits: print("NOT FOUND:", q)
    for f in hits:
        shutil.copy(os.path.join("png_original", f), os.path.join("png", f))
        print("restored", f)
