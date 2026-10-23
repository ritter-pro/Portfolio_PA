from pathlib import Path
from PIL import Image
from lxml import html as LH
import html,json,re,copy,runpy
P=runpy.run_path(str(Path(__file__).parent/"product-markup.py"))
R=Path(__file__).parent;D=R/'dist';G=json.loads((R/'atelier-data.json').read_text());esc=html.escape
names={'illustration':['Иллюстрации','Illustrations'],'web':['Веб-дизайн','Web design'],'editorial':['Книги и вёрстка','Books & editorial'],'graphics':['Графика и инструкции','Technical illustration'],'retouch':['Ретушь','Retouching']}
colors=['#76f8db','#bb8cff','#f0fa58','#fb8dc8','#78baff']
def img(path,title,pre='',eager=False):
 im=Image.open(D/path);w,h=im.size
 return f'<img src="{pre}{path}" alt="{esc(title)}" width="{w}" height="{h}" loading="{"eager" if eager else "lazy"}" decoding="async">'
def visual(c,lang,pre=''):
 title=c['title'][lang];k=c['kind']
 if c.get('product')=='bound-book':return P['book'](c,lang,pre,img)
 if k=='printed-product':return P['printed'](c,lang,pre)
 if k=='workflow':
  steps=c['steps'][lang];return '<div class="screen-schematic"><div class="window-bar">PA–2004 / AUTOMATION</div><strong>'+esc(title)+'</strong><div class="system-flow">'+''.join('<span>'+esc(step)+'</span>' for step in steps)+'</div><small class="schematic-note">'+('Сценарий работы инструмента' if not lang else 'Tool workflow diagram')+'</small></div>'
 p=c.get('hero',c['images'][0]);im=img(p,title,pre,True);w,h=Image.open(D/p).size;ratio=w/h
 if k=='book' and 'spread'in c:return '<div class="bound-spread">'+''.join('<div class="bound-page">'+img(x,title,pre)+'</div>' for x in c['spread'])+'<span class="book-gutter"></span></div>'
 if 'spreadImage'in c:return '<div class="printed-spread">'+im+'<span class="book-gutter"></span></div>'
 if k in ['laptop','phone','tablet']:
  # Screen follows the work orientation; only long landing pages scroll.
  landscape=c.get('landscape',False) or (k=='tablet' and ratio>1.1)
  deviceRatio=ratio if k!='laptop' else 1.6
  if c.get('scroll'): deviceRatio=1.6
  return f'<div class="atelier-device {k} {"landscape" if landscape else ""}" style="--screen-ratio:{deviceRatio}"><div class="device-screen {"scroll-screen" if c.get("scroll") else "fit-screen"}" tabindex="0" aria-label="{esc(title)}">{im}</div></div>'
 if k in ['frame','easel']:return f'<div class="gallery-wall"><div class="gilt-frame" style="--art-ratio:{ratio}"><div class="mat-board">{im}</div></div><span class="gallery-caption">PA–2004 / {esc(title)}</span></div>'
 if k=='retouch':return '<div class="retouch-display">'+im+'<span>STUDIO / FINAL</span></div>'
 if k=='drawing':return f'<div class="technical-board" style="--product-ratio:{ratio}">'+im+'</div>'
 if k in ['digital-card','print']:return f'<div class="digital-card" style="--product-ratio:{ratio}">'+im+'</div>'
 if k=='fold':return '<div class="folded-print">'+im+'<i></i><b></b></div>'
 if k=='laminated':return '<div class="laminated-print">'+im+'</div>'
 if k=='cover':return '<div class="hardback-cover">'+im+'</div>'
 return '<div class="printed-spread">'+im+'<span class="book-gutter"></span></div>'
def shell(template,body,title,file,lang,pre):
 t=re.sub(r'<main\b.*?</main>',f'<main id="main">{body}</main>',template,flags=re.S)
 t=re.sub(r'<title>.*?</title>',f'<title>{esc(title)} — PA–2004</title>',t)
 t=re.sub(r'<link[^>]+rel="alternate"[^>]*>','',t)
 t=re.sub(r'<nav aria-label="[^"]*" class="language-switch">.*?</nav>',f'<nav aria-label="Language" class="language-switch"><a href="{"../" if lang else ""}{file}" lang="ru">RU</a><span>/</span><a href="{"" if lang else "en/"}{file}" lang="en">EN</a></nav>',t,flags=re.S)
 for name,typ in [('showroom.css','css'),('atelier.css','css'),('showroom.js','js'),('final.css','css'),('final.js','js'),('product.css','css'),('product.js','js')]:
  if name not in t:t=t.replace('</head>',(f'<link rel="stylesheet" href="{pre}assets/{name}">' if typ=='css' else f'<script defer src="{pre}assets/{name}"></script>')+'</head>')
 return t

def controls(rows,lang):
 dots=''.join(f'<button data-scene="{i}" aria-label="{esc(c["title"][lang])}">{i+1:02}</button>' for i,c in enumerate(rows))
 return f'<div class="showroom-controls"><button data-prev aria-label="{"Предыдущая" if not lang else "Previous"}">←</button><button data-next aria-label="{"Следующая" if not lang else "Next"}">→</button><span class="scene-status" aria-live="polite"></span><div class="scene-progress" aria-hidden="true"><i></i></div><button data-play>Ⅱ</button><div class="scene-dots">{dots}</div></div>'
def slide(c,i,lang,pre,group,url=None):
 title=c['title'][lang];desc=c['description'][lang]
 return f'<article class="showroom-slide" data-color="{colors[i%5]}" aria-label="{i+1} / {len(G.get(group,[]))}"><div class="scene-visual">{visual(c,lang,pre)}</div><div class="scene-copy"><span class="scene-number" aria-hidden="true">{i+1:02}</span><div class="eyebrow">{names.get(group,[group,group])[lang]} / {i+1:02}</div><h2>{esc(title)}</h2><p>{esc(desc)}</p><button class="scene-more" data-more aria-expanded="false">{"Подробнее" if not lang else "Details"} +</button><p class="scene-description">{"Внутри — детали проекта и изображения целиком." if not lang else "Explore the project and full-size artwork."}</p><a href="{url or "atelier-"+c["id"]+".html"}">{"Открыть кейс" if not lang else "Open case"} ↗</a></div></article>'
for lang in [0,1]:
 folder=D/('en' if lang else '');pre='../' if lang else ''
 for group,rows in G.items():
  tplfile=folder/('brand.html' if group=='retouch' else group+'.html');template=tplfile.read_text();m=re.search(r'<section class="section category-head">.*?</section>',template,re.S)
  intro=m.group() if m else ''
  if group=='retouch':intro=f'<section class="section category-head"><a class="breadcrumb" href="index.html#modules">← {"Все направления" if not lang else "All modules"}</a><div class="eyebrow">{"МОДУЛЬ" if not lang else "MODULE"} 07 / PA–2004</div><h1>{names[group][lang]}<em>.</em></h1><div class="category-intro"><h2>{"Чистота кадра.<br>Характер материала." if not lang else "A clear image.<br>Material character."}</h2><p>{"Предметная ретушь, каталожная подача и детали. Реальные рабочие кадры и результат обработки." if not lang else "Product retouching, catalogue imagery and details. Real source images and finished work."}</p></div></section>'
  for i,c in enumerate(rows):
   title=c['title'][lang];desc=c['description'][lang];url='atelier-'+c['id']+'.html'
   pictures=''
   printmap={x['image'].split('/')[-1].replace('-original.png','.webp'):x for x in c.get('printImages',[])}
   for j,x in enumerate(c['images']):
    info=printmap.get(Path(x).name)
    content=P['proof'](info,lang,pre,title) if info else img(x,title,pre)
    source=info['image'] if info else x
    pictures+=f'<figure><button class="image-open" data-image="{pre}{source}" aria-label="{"Увеличить" if not lang else "Enlarge"}: {esc(title)}">{content}</button><figcaption>{j+1:02} / {esc(title)}</figcaption></figure>'
   compare=''
   if c.get('before'):
    # Different crops are shown side by side, so both original and final stay intact.
    compare=f'<section class="section comparison"><div class="eyebrow">{"СЪЁМКА → ОБРАБОТКА" if not lang else "CAPTURE → RETOUCH"}</div><h2>{"До и после" if not lang else "Before and after"}</h2><div class="compare-pair"><figure>{img(c["before"],"До обработки" if not lang else "Before retouching",pre)}<figcaption>{"Исходная съёмка" if not lang else "Original capture"}</figcaption></figure><figure>{img(c["after"],"После обработки" if not lang else "After retouching",pre)}<figcaption>{"После обработки" if not lang else "Finished image"}</figcaption></figure></div></section>'
   pdf=f'<a class="atelier-link" href="{pre}{c["pdf"]}" target="_blank" rel="noopener">{"Полная инструкция / PDF" if not lang else "Full manual / PDF"} ↗</a>' if c.get('pdf') else ''
   link=f'<a class="atelier-link" href="{c["link"]}">{"О проекте" if not lang else "Project story"} ↗</a>' if c.get('link') else ''
   video=''
   if c.get('youtube'):video=f'<section class="section motion-case"><div class="eyebrow">MOTION / PROTOTYPE</div><h2>{"Интерфейс в движении" if not lang else "Interface in motion"}</h2><div class="video-embed" data-youtube="{c["youtube"]}"><button class="load-video"><span>▶</span>{"Смотреть анимацию" if not lang else "Play animation"}</button></div><a class="atelier-link" href="https://www.youtube.com/watch?v={c["youtube"]}" target="_blank" rel="noopener">YouTube ↗</a></section>'
   body=f'<section class="section atelier-case-head"><a class="breadcrumb" href="{group}.html">← {names[group][lang]}</a><div class="eyebrow">PA–2004 / {names[group][lang]}</div><h1>{esc(title)}</h1><p>{esc(desc)}</p>{pdf}{link}<div class="atelier-hero scene-visual">{visual(c,lang,pre)}</div></section>{compare}{video}<section class="section atelier-originals"><div class="eyebrow">{"ДЕТАЛИ ПРОЕКТА / ОРИГИНАЛЫ" if not lang else "PROJECT DETAILS / ORIGINALS"}</div><h2>{"Рассмотреть ближе" if not lang else "A closer look"}</h2><div class="original-grid">{pictures}</div></section><a class="next-module" href="{group}.html"><span>{"ВЕРНУТЬСЯ В ГАЛЕРЕЮ" if not lang else "BACK TO GALLERY"}</span><strong>{names[group][lang]}</strong><b>↗</b></a>'
   (folder/url).write_text(shell(template,body,title,url,lang,pre))
  body=intro+f'<section class="showroom atelier-showroom" id="gallery" aria-label="{names[group][lang]}"><div class="showroom-heading"><div class="eyebrow">{"ЖИВАЯ ГАЛЕРЕЯ" if not lang else "LIVING GALLERY"} / {len(rows):02}</div><p>{"Листайте, наводите, открывайте. На телефоне — свайп и нажатие." if not lang else "Swipe, hover, explore. Tap to open on mobile."}</p></div><div class="showroom-stage">'+''.join(slide(c,i,lang,pre,group) for i,c in enumerate(rows))+'</div>'+controls(rows,lang)+'</section>'
  (folder/(group+'.html')).write_text(shell(template,body,names[group][lang],group+'.html',lang,pre))
  if group=='retouch':(folder/'brand.html').write_text(shell(template,body,names[group][lang],'brand.html',lang,pre))
print('Rendered galleries and cases')
