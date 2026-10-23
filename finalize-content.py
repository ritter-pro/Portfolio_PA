from pathlib import Path
from lxml import html as H
import json,re,copy,runpy
R=Path(__file__).parent;D=R/'dist';G=json.loads((R/'atelier-data.json').read_text())
video={'agrio':'_YVWS_vZryo','waycup':'X0xEnkp0ZE8','yoga':'bPs-3OqDB5M','white-square':'xYeiPWn7Nuk','cofefest':'SUaI1XBA3WE','keto':'aALJAe-B2NE','conference':'24DfiTJUmp8','sedelice':'RP_lIbX6Pqc'}
for c in G['web']:
 if c['id'] in video:c['youtube']=video[c['id']]
for c in G['graphics']:
 if c['id']=='manual-54638':c['title']=['Настольный светильник','Table lamp']
G['retouch']=[c for c in G['retouch'] if c['id'] not in []]
(R/'atelier-data.json').write_text(json.dumps(G,ensure_ascii=False,indent=2))
M=runpy.run_path(str(R/'render-final.py'));visual=M['visual'];slide=M['slide'];controls=M['controls'];esc=M['esc']
def parse(p):
 baseline=R/"templates-final"/p.relative_to(D)
 return H.fromstring((baseline if baseline.exists() else p).read_text())
def out(p,r):p.write_text('<!DOCTYPE html>\n'+H.tostring(r,encoding='unicode',method='html'))
def el(s):return H.fromstring(s)

def addstories(root,stories,lang,pre):
 stage=root.xpath('.//div[contains(concat(" ",@class," ")," showroom-stage ")]')[0]
 for c in stories:stage.append(el(slide(c,len(stage),lang,pre,'coding' if c.get('code') else 'social',c['url'])))
 rows=stage.xpath('./article')
 for i,s in enumerate(rows):
  s.set('aria-label',f'{i+1} / {len(rows)}');n=s.xpath('.//*[contains(concat(" ",@class," ")," scene-number ")]')
  if n:n[0].text=f'{i+1:02}'
 ctrl=root.xpath('.//div[@class="showroom-controls"]')[0];dots=ctrl.xpath('./div[@class="scene-dots"]')[0];dots.clear();dots.set('class','scene-dots')
 for i,s in enumerate(rows):
  titles=s.xpath('.//h2|.//h3');title=titles[0].text_content() if titles else str(i+1);dots.append(el(f'<button data-scene="{i}" aria-label="{esc(title)}">{i+1:02}</button>'))
newcode=[
 dict(id='manual-generator',title=['Генератор инструкций','Manual generator'],description=['CSV → характеристики в макете → отдельные PDF. Два сценария Illustrator для встраиваемых и накладных спотов сохраняют шрифты и оформление; пробный запуск позволяет проверить результат до обработки всей серии.','CSV → template fields → separate PDFs. Two Illustrator workflows for recessed and surface-mounted spotlights preserve typography, with a trial run before batch processing.'],kind='drawing',hero='assets/final/manual-54735-drawing.webp',images=['assets/final/manual-54735-drawing.webp'],url='#code-manual-generator',repo='illustrator-manual-generator',tech='ILLUSTRATOR / JSX / CSV'),
 dict(id='package-mockups',title=['Мокапы на потоке','Mockups at scale'],description=['Photoshop собирает лицевую и оборотную стороны упаковки: товар, индивидуальные тени, плёнка и евроотверстие. Настройки количества и масштаба, PNG 3000 × 3000 и редактируемый PSD.','Photoshop builds front and back packaging views with product instances, individual shadows, film and a euro slot. Quantity and scale controls, 3000 × 3000 PNGs and editable PSDs.'],kind='retouch',images=['assets/packaging/torino.webp'],url='#code-package-mockups',repo='photoshop-package-mockups',tech='PHOTOSHOP / JSX / PNG / PSD'),
 dict(id='pim-builder',title=['PIM Image Builder','PIM Image Builder'],description=['Развёртки, мокапы, чертежи и Excel → семь изображений на каждый товар. Приложение на Python проверяет исходники, управляет очередью и формирует отчёт. Рабочий сценарий рассчитан на 88 товаров — 616 файлов.','Dielines, mockups, drawings and Excel → seven images per product. A Python application validates inputs, manages the queue and produces a report. The workflow is designed for 88 products — 616 files.'],kind='retouch',images=['assets/final/retouch-light-IMG_0021.webp'],url='#code-pim-builder',repo='pim-image-builder',tech='PYTHON / TKINTER / PILLOW')]
# Use the existing published Torino mockup rather than infer a file name.
pack=json.loads((R/'packaging-data.json').read_text());
# Resolve the best available packaging preview from the gallery.
pkg=parse(D/'packaging.html');ims=[x for x in pkg.xpath('//img/@src') if x.endswith(('.webp','.png','.jpg'))];fallback=ims[0] if ims else 'assets/atelier/pa-main.webp'
newcode[1]['images']=[fallback]
for c in newcode:
 c['code']=True;c['kind']='workflow'
 if c['id']=='manual-generator':c['steps']=[['CSV / ДАННЫЕ ТОВАРОВ','AI / УТВЕРЖДЁННЫЙ МАКЕТ','PDF / ОТДЕЛЬНЫЙ ФАЙЛ НА ТОВАР'],['CSV / PRODUCT DATA','AI / APPROVED TEMPLATE','PDF / ONE FILE PER PRODUCT']]
 elif c['id']=='package-mockups':c['steps']=[['PDF / ЛИЦО И ОБОРОТ','ТОВАР / ТЕНИ / ПЛЁНКА','PNG 3000 × 3000 + PSD'],['PDF / FRONT AND BACK','PRODUCT / SHADOWS / FILM','PNG 3000 × 3000 + PSD']]
 else:c['steps']=[['PDF + PNG + ЧЕРТЕЖИ + EXCEL','7 ИЗОБРАЖЕНИЙ НА ТОВАР','88 ТОВАРОВ → 616 ФАЙЛОВ'],['PDF + PNG + DRAWINGS + EXCEL','7 IMAGES PER PRODUCT','88 PRODUCTS → 616 FILES']]
for lang in [0,1]:
 folder=D/('en' if lang else '');pre='../' if lang else ''
 # Extend social stories and their image collections.
 p=folder/'social.html';r=parse(p);gallery=r.xpath('//section[@id="social-gallery"]')[0]
 stories=[]
 for key,title,desc,prefix,count in [
 ('wall-light',['Бра: свет по сценарию','Wall lights: lighting scenarios'],['Гайд о выборе бра: направление света, высота установки и понятные интерьерные примеры. Четыре страницы в фирменной системе Ritter.','A wall-light guide covering light direction, mounting height and practical interior examples. Four pages in Ritter’s visual system.'],'guide7',4),
 ('home-kit',['Электрика под рукой','An electrical essentials kit'],['Шесть карточек: обложка и пять вещей для бытовых задач. Предметные изображения, технические детали и короткие жизненные ситуации помогают разобраться с выбором.','Six cards: a cover and five essentials for household tasks. Product imagery, technical details and short everyday scenarios make the choices clear.'],'guide8',6)]:
  images=[f'assets/final/{prefix}-guide{i}.webp' for i in range(1,count+1)];c=dict(id=key,title=title,description=desc,kind='digital-card',images=images,url='#social-'+key);stories.append(c)
  pics=''.join(f'<figure><button class="image-open" data-image="{pre}{im}" aria-label="{esc(title[lang])}">{M["img"](im,title[lang],pre)}</button><figcaption>{i+1:02} / {count:02}</figcaption></figure>' for i,im in enumerate(images))
  r.xpath('//main')[0].append(el(f'<section class="section case-collection" id="social-{key}"><div class="eyebrow">SOCIAL / GUIDE</div><h2>{title[lang]}</h2><p>{desc[lang]}</p><div class="media-grid">{pics}</div></section>'))
 addstories(gallery,stories,lang,pre)
 for node in gallery.xpath('.//div[@class="showroom-heading"]/p'):node.text='Рилсы, посты, реклама и гайды. Восемь подборок в единой системе.' if not lang else 'Reels, posts, ads and guides. Eight curated stories in one system.'
 out(p,r)
 # Coding: replace incorrect script claim with what the public JSX actually does.
 p=folder/'coding.html';r=parse(p);gallery=r.xpath('//section[@id="code-gallery"]')[0]
 for node in r.xpath('//*[contains(text(),"PDF → кривые") or contains(text(),"PDF → CURVES") or contains(text(),"PDF → outlines")]'):node.text='Объекты → символы' if not lang else 'Objects → symbols'
 for node in r.xpath('//*[contains(text(),"Пакетный сценарий описан") or contains(text(),"The batch workflow") or contains(text(),"The documented batch workflow")]'):node.text='JSX заменяет выделенные объекты экземплярами выбранного символа, сохраняя положение и высоту. Полезно при повторяющейся замене графики в макетах.' if not lang else 'A JSX script replaces selected objects with instances of a chosen symbol, preserving position and height for repeated graphics updates.'
 sec=r.xpath('//section[@id="code-script"]')
 if sec:
  old=sec[0];parent=old.getparent();parent.replace(old,el(f'<section class="section case-collection" id="code-script"><div class="eyebrow">ILLUSTRATOR / JSX</div><h2>{"Объекты → символы" if not lang else "Objects → symbols"}</h2><p>{"Опубликованный сценарий заменяет выделенные объекты экземплярами символа, сохраняет положение и высоту и масштабирует графику пропорционально." if not lang else "The published script replaces selected objects with symbol instances, preserves position and height, and scales the artwork proportionally."}</p><a class="atelier-link" href="https://github.com/ritter-pro/illustrator-batch-curves-rename" target="_blank" rel="noopener">GitHub ↗</a></section>'))
 # Update schematic labels too.
 codeSlides=gallery.xpath('.//article[contains(@class,"showroom-slide")]')
 if len(codeSlides)>2:
  flow=codeSlides[2].xpath('.//div[@class="system-flow"]')
  if flow:
   flow[0].clear();flow[0].set('class','system-flow')
   for txt in ['01 / SELECT OBJECTS','02 / CHOOSE SYMBOL','03 / REPLACE & SCALE']:flow[0].append(el('<span>'+txt+'</span>'))
 addstories(gallery,newcode,lang,pre)
 stage=gallery.xpath('.//div[@class="showroom-stage"]')[0]
 ranks={'#code-pim-builder':0,'bot.html':1,'portfolio-case.html':2,'#code-package-mockups':3,'#code-manual-generator':4,'#code-task':5,'#code-links':6,'#code-script':7}
 ordered=sorted(list(stage),key=lambda s:ranks.get(s.xpath('.//a/@href')[-1],99))
 for item in list(stage):stage.remove(item)
 for i,item in enumerate(ordered):
  item.set('aria-label',f'{i+1} / {len(ordered)}');item.xpath('.//span[@class="scene-number"]')[0].text=f'{i+1:02}'
  eyebrow=item.xpath('.//div[@class="eyebrow"]')[0];eyebrow.text=re.sub(r'^\d{2}\s*/\s*','',eyebrow.text or '')
  stage.append(item)
 ctrl=gallery.xpath('.//div[@class="showroom-controls"]')[0];gallery.replace(ctrl,el(controls([{'title':[item.xpath('.//h2|.//h3')[0].text_content()]*2} for item in ordered],lang)))
 for c in newcode:
  r.xpath('//main')[0].append(el(f'<section class="section case-collection" id="code-{c["id"]}"><div class="eyebrow">{c["tech"]}</div><h2>{c["title"][lang]}</h2><p>{c["description"][lang]}</p><div class="coding-outcome">{visual(c,lang,pre)}</div><p>{"Моя роль: постановка задачи, сценарий работы, визуальные требования и проверка результата. Реализация — с помощью ИИ." if not lang else "My role: requirements, workflow design, visual direction and validation. Implementation assisted by AI."}</p><a class="atelier-link" href="https://github.com/ritter-pro/{c["repo"]}" target="_blank" rel="noopener">GitHub / {c["repo"]} ↗</a></section>'))
 repos=json.loads((R/'github-projects.json').read_text());links=''.join(f'<a href="{x["html_url"]}" target="_blank" rel="noopener"><strong>{x["name"]} ↗</strong><span>{"Репозиторий создан · исходники будут добавлены" if x["name"]=="Portfolio_PA" and not lang else "Repository created · source to follow" if x["name"]=="Portfolio_PA" else (x.get("language") or "Project files")}</span></a>' for x in repos)
 r.xpath('//main')[0].append(el(f'<section class="section"><div class="eyebrow">GITHUB / 2026</div><h2>{"Открытые проекты" if not lang else "Public projects"}</h2><div class="repo-grid">{links}</div></section>'))
 out(p,r)
 # One work from each of the eight modules.
 p=folder/'index.html';r=parse(p);root=r.xpath('//section[@id="selected-work"]')[0];stage=root.xpath('.//div[@class="showroom-stage"]')[0];existing=list(stage)
 stage.remove(existing[2])
 selected=[('graphics',G['graphics'][0]),('coding',newcode[2]),('illustration',G['illustration'][0]),('web',next(c for c in G['web'] if c['id']=='pa2004')),('retouch',G['retouch'][0]),('editorial',G['editorial'][0])]
 for group,c in selected:
  url=('coding.html#code-pim-builder' if group=='coding' else 'atelier-'+c['id']+'.html');stage.append(el(slide(c,len(stage),lang,pre,group,url)))
 rows=list(stage)
 for i,s in enumerate(rows):
  s.set('aria-label',f'{i+1} / {len(rows)}')
  n=s.xpath('.//span[@class="scene-number"]')
  if n:n[0].text=f'{i+1:02}'
 ctrl=root.xpath('.//div[@class="showroom-controls"]')[0];root.replace(ctrl,el(controls([{'title':[s.xpath('.//h2|.//h3')[0].text_content()]*2} for s in rows],lang)))
 out(p,r)
# Remove requested projects from all case paths.
for lang in ['', 'en']:
 for ident in ['space','car','popup','dumai','dance','fish']:
  p=D/lang/('atelier-'+ident+'.html')
  if p.exists():p.unlink()
# Shared navigation and final design layer on every page.
for p in D.rglob('*.html'):
 if 'assets' in p.parts:continue
 s=p.read_text();pre='../' if p.parent.name=='en' else '';lang=p.parent.name=='en'
 s=s.replace('href="brand.html"','href="retouch.html"').replace('Фирменный стиль','Ретушь').replace('Brand identity','Retouching').replace('Бренд вне экрана.','Свет. Фактура. Детали.').replace('Brand beyond the screen.','Light. Texture. Details.').replace('Знак → система → носители','Съёмка → обработка → каталог').replace('Ретушь, корпоративные материалы и мерч.','Предметная ретушь, детали и сравнение до / после.')
 s=s.replace('Упаковки, иллюстрации, фирменный стиль и многостраничный дизайн.','Упаковки, иллюстрации, ретушь и многостраничный дизайн.')
 for name,typ in [('showroom.css','css'),('atelier.css','css'),('final.css','css'),('final.js','js'),('product.css','css'),('product.js','js')]:
  if name not in s:s=s.replace('</head>',(f'<link rel="stylesheet" href="{pre}assets/{name}">' if typ=='css' else f'<script defer src="{pre}assets/{name}"></script>')+'</head>')
 # Legacy inline labels may have lowercased SVG viewboxes.
 s=s.replace('viewbox=','viewBox=')
 p.write_text(s)
small=[{'name':x['name'],'url':x['html_url'],'language':x.get('language')} for x in repos];(D/'assets/repos.json').write_text(json.dumps(small,ensure_ascii=False))
print('Integrated eight home stories, social guides, GitHub projects and navigation')

runpy.run_path(str(R/"polish-site.py"))
