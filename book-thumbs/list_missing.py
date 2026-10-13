"""Checks the png folder and makes missing_books.html with a clickable list
of books that still need to be downloaded.  Run: python3 list_missing.py"""
import json, os, re, html, unicodedata
def norm(s): return unicodedata.normalize("NFC", s)
have = {norm(f) for f in os.listdir("png")} if os.path.isdir("png") else set()
books = json.load(open("books.json", encoding="utf-8"))
missing = [b for b in books if norm(re.sub(r'[\\/:*?"<>|]', "_", b["png"])) not in have]
rows = ""
for i, b in enumerate(missing, 1):
    url = f"https://drive.google.com/file/d/{b['drive_id']}/view"
    dl = f"https://drive.google.com/uc?export=download&id={b['drive_id']}"
    rows += (f"<tr><td><input type=checkbox></td><td>{i}</td>"
             f"<td><a href='{url}' target=_blank>{html.escape(b['file'])}</a> "
             f"&nbsp;<a class=dl href='{dl}' target=_blank>⬇ download</a></td>"
             f"<td>{html.escape(b['title_telugu'])}</td><td>{html.escape(b['category'])}</td></tr>\n")
open("missing_books.html", "w", encoding="utf-8").write(f"""<!doctype html><meta charset=utf-8>
<title>Missing books</title><style>body{{font-family:sans-serif;margin:30px}}
td,th{{padding:6px 10px;border-bottom:1px solid #ccc;text-align:left}}</style>
<h2>Books still to download: {len(missing)} of {len(books)}</h2>
<p>Click a name, download the PDF from Drive, and put it in the <b>my_pdfs</b> folder.</p>
<button id=all style="font-size:18px;padding:10px 20px;cursor:pointer">⬇ Download all {len(missing)} PDFs</button>
<span id=st style="margin-left:15px"></span>
<table><tr><th>Done</th><th>#</th><th>File (click to open)</th><th>Telugu title</th><th>Category</th></tr>
{rows}</table>
<script>
document.getElementById('all').onclick=async()=>{{
 const L=[...document.querySelectorAll('a.dl')];
 for(let i=0;i<L.length;i++){{
  document.getElementById('st').textContent='Starting '+(i+1)+' of '+L.length+' ... (allow multiple downloads if Chrome asks)';
  const f=document.createElement('iframe');f.style.display='none';f.src=L[i].href;document.body.appendChild(f);
  L[i].closest('tr').querySelector('input').checked=true;
  await new Promise(r=>setTimeout(r,4000));
 }}
 document.getElementById('st').textContent='Done. Check your Downloads folder.';
}};
</script>""")
print(f"{len(missing)} books missing. Open missing_books.html in your browser.")
