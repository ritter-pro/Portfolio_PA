from pathlib import Path
from lxml import html
from urllib.parse import urlsplit,unquote
import json
D=Path(__file__).parent/'dist';errors=[];pages={}
for p in D.rglob('*.html'):
 if 'assets' in p.parts:continue
 try:r=html.fromstring(p.read_text());pages[p]=r
 except Exception as e:errors.append((str(p),str(e)))
for p,r in pages.items():
 for e in r.xpath('//*[@href or @src or @data-src or @data-image]'):
  for attr in ['href','src','data-src','data-image']:
   v=e.get(attr)
   if not v or v.startswith(('http:','https:','mailto:','tel:','data:','javascript:')):continue
   u=urlsplit(v);dest=(p.parent/unquote(u.path)).resolve() if u.path else p.resolve()
   if not dest.exists():errors.append((str(p.relative_to(D)),attr,v))
   elif attr=='href' and u.fragment and dest.suffix=='.html':
    target=pages.get(dest)
    if target is None:target=html.fromstring(dest.read_text())
    if not target.xpath('//*[@id=$id]',id=unquote(u.fragment)) and not (dest.name=='packaging.html' and any(c['slug']==u.fragment for c in json.loads((D.parent/'packaging-data.json').read_text()))):errors.append((str(p.relative_to(D)),'anchor',v))
print('PAGES',len(pages),'ERRORS',len(errors))
for e in errors[:100]:print(e)
(D.parent/'.sites-runtime').mkdir(exist_ok=True)
(D.parent/'.sites-runtime'/'site-audit.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2))

raise SystemExit(bool(errors))
