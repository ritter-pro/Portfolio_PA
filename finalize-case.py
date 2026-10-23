from pathlib import Path
from PIL import Image
from lxml import html as H
import json
R=Path(__file__).parent;D=R/'dist'
# Screenshot assets are captured from the actual finished pages, never fabricated.
for name in ['home','graphics','editorial']:
 src=Path('/workspace/scratch')/('pa-final-'+name+'.jpg');dst=D/'assets/projects'/('pa-final-'+name+'.webp')
 if src.exists():Image.open(src).convert('RGB').save(dst,'WEBP',quality=93,method=4)
G=json.loads((R/'atelier-data.json').read_text());c=next(x for x in G['web'] if x['id']=='pa2004');c['images']=['assets/projects/pa-final-home.webp','assets/projects/pa-final-graphics.webp','assets/projects/pa-final-editorial.webp'];(R/'atelier-data.json').write_text(json.dumps(G,ensure_ascii=False,indent=2))
for base in [D,R/'templates-final']:
 for p in base.rglob('*.html'):
  if 'assets' in p.parts:continue
  r=H.fromstring(p.read_text());pre='../' if p.parent.name=='en' else '';changed=False
  for im in r.xpath('//img'):
   if any('pa-main' in im.get(a,'') for a in ['src','data-src','srcset','data-srcset']):
    for a in ['srcset','data-srcset','data-src']:im.attrib.pop(a,None)
    im.set('src',pre+'assets/projects/pa-final-home.webp');changed=True
  if changed:p.write_text('<!DOCTYPE html>\n'+H.tostring(r,encoding='unicode',method='html'))
for en in [False,True]:
 p=D/('en' if en else '')/'portfolio-case.html';r=H.fromstring(p.read_text());pre='../' if en else ''
 stories=r.xpath('//div[@class="project-story-grid"]/article')
 if len(stories)>=5:
  stories[2].xpath('./p')[0].text='Responsive Russian and English pages, eight portfolio modules, physical print mockups, carousels, video and an optional interactive 3D model.' if en else 'Адаптивные страницы на русском и английском языках, восемь направлений портфолио, объёмная подача печатных работ, карусели, увеличение изображений, видео и интерактивная 3D-модель.'
  stories[4].xpath('./p')[0].text='A published portfolio with verified case covers and titles. Responsive images, local fonts, deferred media and precomputed print textures reduce loading work. A GitHub Pages publishing package is prepared.' if en else 'Опубликованное портфолио с проверенными названиями и обложками кейсов. Адаптивные изображения, локальные шрифты, отложенная загрузка медиа и заранее подготовленные печатные мокапы уменьшают нагрузку при открытии. Подготовлена версия для публикации на GitHub Pages.'
 for im in r.xpath('//section[1]//img'):
  im.set('src',pre+'assets/projects/pa-final-home.webp')
  for attr in ['srcset','data-srcset','data-src']:im.attrib.pop(attr,None)
 figures=r.xpath('//div[@class="website-gallery"]/figure');names=['Home / final interface','Technical illustration / verified manuals','Editorial / physical print presentation'] if en else ['Главная / финальный интерфейс','Графика / проверенные инструкции','Книги и вёрстка / объёмная подача']
 for fig,name,shot in zip(figures,names,['home','graphics','editorial']):
  src=pre+'assets/projects/pa-final-'+shot+'.webp';im=fig.xpath('.//img')[0];im.set('src',src);im.set('alt',name)
  for attr in ['srcset','data-srcset','data-src']:im.attrib.pop(attr,None)
  fig.xpath('.//a')[0].set('href',src);fig.xpath('./figcaption')[0].text=name
 p.write_text('<!DOCTYPE html>\n'+H.tostring(r,encoding='unicode',method='html'))
