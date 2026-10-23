from pathlib import Path
from PIL import Image
import html
R=Path(__file__).parent;D=R/'dist';esc=html.escape

def book(c,lang,pre,img):
 pages=c['spread'];im=Image.open(D/pages[0]);ratio=(im.width*2)/im.height
 return f'<div class="physical-product physical-book" style="--product-ratio:{ratio}"><div class="product-floor"></div><div class="book-block"><div class="real-book-page page-left">{img(pages[0],c["title"][lang],pre,True)}</div><div class="real-book-page page-right">{img(pages[1],c["title"][lang],pre,True)}</div><span class="real-book-spine"></span></div></div>'

def printed(c,lang,pre):
 p=c['print'];typ=c['product'];panels=3 if typ=='fold' else 2 if typ in ['magazine','jacket'] else 1
 crop=','.join(str(n) for n in p['crop']);label=esc(c['title'][lang]);back=''
 if typ=='laminated' and len(c.get('printImages',[]))>1:
  b=c['printImages'][1];back=f' data-back-src="{pre}{b["image"]}" data-back-crop="{",".join(str(n) for n in b["crop"])}"'
 return f'<div class="physical-product physical-print is-{typ}" data-print-src="{pre}{p["image"]}" data-print-crop="{crop}"{back} style="--product-ratio:{p["ratio"]};--panels:{panels}" role="img" aria-label="{label}"><div class="product-floor"></div><div class="product-underlay"></div><div class="print-surface">'+''.join(f'<div class="print-panel" style="--panel:{i}"><span class="panel-ink"></span><span class="paper-light"></span></div>' for i in range(panels))+'</div><div class="paper-edge"></div><span class="product-loading" aria-hidden="true">PA–2004 / PRINT</span></div>'

def proof(info,lang,pre,title):
 crop=','.join(str(n) for n in info['crop']);return f'<div class="print-proof" data-print-src="{pre}{info["image"]}" data-print-crop="{crop}" style="--product-ratio:{info["ratio"]}" role="img" aria-label="{esc(title)}"><div class="proof-ink"></div></div>'
