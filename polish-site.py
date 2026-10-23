from pathlib import Path
from lxml import html as H
import re,json
R=Path(__file__).parent;D=R/'dist'
icon='<svg viewBox="0 0 240 180" fill="none" stroke="currentColor" stroke-width="2"><rect x="42" y="25" width="156" height="126" rx="8"/><path d="M120 25v126M57 130l38-43 25 22M120 110l24-30 39 50"/><circle cx="82" cy="60" r="11"/><path d="M149 39l4 10 10 4-10 4-4 10-4-10-10-4 10-4zM173 67v14m-7-7h14"/></svg>'
for p in D.rglob('*.html'):
 if 'assets' in p.parts or p.name.startswith('__'):continue
 s=p.read_text();s=s.replace('Mark → system → applications','Capture → retouch → catalogue').replace('Retouching, corporate materials and merchandise.','Product retouching, detail views and before / after comparisons.').replace('Вайбкодинг','Вайб-кодинг').replace('Vibe coding','Vibe-coding')
 if p.name=='index.html':
  def fix(m):
   x=m.group()
   if 'retouch.html' not in x:return x
   return re.sub(r'(<div[^>]*class="module-diagram">).*?</div>',lambda k:k[1]+icon+'</div>',x,flags=re.S)
  s=re.sub(r'(<article[^>]*class="module-card module-info".*?</article>)',fix,s,flags=re.S)
 if p.name in ['social.html','coding.html']:
  s=re.sub(r'(<div class="showroom-heading">.*?)(<h2>)(.*?)(</h2>)',lambda m:m[1]+'<h1>'+m[3]+'</h1>',s,count=1,flags=re.S)
 # Final assets use explicit revisions so returning visitors receive the update.
 for filename in ['final.css','final.js','refinement.js','product.css','product.js','showroom.js']:
  s=re.sub(r'(assets/'+re.escape(filename)+r')(?:\?[^"\s>]*)?',r'\1?v=20261023-products-v2',s)
 r=H.fromstring(s)
 desc=r.xpath('//main//p[normalize-space()][1]')
 if desc:
  value=desc[0].text_content().strip()[:175]
  s=re.sub(r'<meta\b(?=[^>]*\bname="description")[^>]*>',lambda m:'<meta name="description" content="'+__import__('html').escape(value,quote=True)+'">',s,count=1)
 p.write_text(s)
print('Final typography, navigation, metadata and cache revisions applied')
