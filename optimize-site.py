"""Offline textures, responsive media and a smaller critical loading path."""
from pathlib import Path
from PIL import Image
from lxml import html as H
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import json,hashlib,re
R=Path(__file__).parent;D=R/'dist';A=D/'assets'
def variant(job):
 src,dest,width=job;im=Image.open(src);im.thumbnail((width,10000),Image.Resampling.LANCZOS);im.save(dest,'WEBP',quality=86,method=4)
def main():
 ready=A/'print-ready';ready.mkdir(exist_ok=True);lookup={}
 for info in json.loads((A/'print-manifest.json').read_text()).values():
  src=D/info['image'];dst=ready/(src.stem+'.webp');lookup[info['image']]=dst.relative_to(D).as_posix()
  if dst.exists():continue
  a=np.array(Image.open(src).convert('RGBA').crop(tuple(info['crop'])));mask=a[:,:,3]>=250;h,w=mask.shape
  left=np.argmax(mask,axis=1);right=w-1-np.argmax(mask[:,::-1],axis=1);top=np.argmax(mask,axis=0);bottom=h-1-np.argmax(mask[::-1,:],axis=0)
  yy,xx=np.where(~mask);sx=np.where(xx<left[yy],left[yy],right[yy]);sy=np.where(yy<top[xx],top[xx],bottom[xx]);rd=np.where(mask.any(axis=1)[yy],abs(sx-xx),10**8);cd=np.where(mask.any(axis=0)[xx],abs(sy-yy),10**8);use=cd<rd
  a[yy,xx,:3]=a[np.where(use,sy,yy),np.where(use,xx,sx),:3];a[yy,xx,3]=255
  Image.fromarray(a).convert('RGB').save(dst,'WEBP',quality=92,method=4)
 responsive={};thumbs=A/'responsive';thumbs.mkdir(exist_ok=True);jobs=[]
 for folder in ['atelier','packaging','final','projects','print-ready']:
  for file in (A/folder).glob('*.webp'):
   im=Image.open(file);variants=[]
   for width in [480,960,1440]:
    if im.width<=width*1.12:continue
    dest=thumbs/(folder+'-'+file.stem+f'-{width}.webp')
    if not dest.exists():jobs.append((str(file),str(dest),width))
    variants.append((dest.relative_to(D).as_posix(),width))
   variants.append((file.relative_to(D).as_posix(),im.width));responsive[file.relative_to(D).as_posix()]=(variants,im.size)
 with ProcessPoolExecutor(max_workers=4) as pool:list(pool.map(variant,jobs))
 for page in D.rglob('*.html'):
  if 'assets' in page.parts or page.name.startswith('__'):continue
  root=H.fromstring(page.read_text());pre='../' if page.parent.name=='en' else ''
  for node in root.xpath('//*[@data-print-src]'):
   for attr in ['data-print-src','data-back-src']:
    old=node.get(attr)
    if old and old.removeprefix(pre) in lookup:node.set(attr,pre+lookup[old.removeprefix(pre)])
  for im in root.xpath('//img[@src]'):
   src=im.get('src');key=src.removeprefix(pre);im.set('decoding','async')
   if key not in responsive:continue
   variants,(w,h)=responsive[key];im.set('width',str(w));im.set('height',str(h));im.set('loading','lazy')
   if len(variants)>1:
    im.set('srcset',', '.join(pre+path+' '+str(width)+'w' for path,width in variants));im.set('sizes','(max-width: 700px) 92vw, (max-width: 1100px) 70vw, 960px');im.set('src',pre+variants[min(1,len(variants)-1)][0])
   if im.xpath('ancestor::*[contains(concat(" ",@class," ")," showroom-slide ") or contains(concat(" ",@class," ")," pack-shot ")]'):
    im.set('data-src',im.attrib.pop('src'))
    if im.get('srcset'):im.set('data-srcset',im.attrib.pop('srcset'))
  heroes=root.xpath('//main/section[1]//img')
  if heroes and page.name!='index.html':heroes[0].set('loading','eager');heroes[0].set('fetchpriority','high')
  for script in root.xpath('//script[@src]'):
   if script.get('src').split('/')[-1].split('?')[0] in ['three.min.js','GLTFLoader.js','DRACOLoader.js','hologram.js']:script.getparent().remove(script)
  if root.xpath('//*[@id="model"]') and not root.xpath('//script[contains(@src,"model-loader.js")]'):root.xpath('//head')[0].append(H.Element('script',src=pre+'assets/model-loader.js',defer=''))
  css=root.xpath('//link[@rel="stylesheet"]');parts=[]
  for link in css:
   path=D/link.get('href').split('?')[0].removeprefix(pre)
   if path.exists():parts.append(path.read_text())
  if parts:
   text='\n'.join(parts);digest=hashlib.sha256(text.encode()).hexdigest()[:12];name='bundle-'+digest+'.css';(A/name).write_text(text);css[0].set('href',pre+'assets/'+name)
   for link in css[1:]:link.getparent().remove(link)
  out='<!DOCTYPE html>\n'+H.tostring(root,encoding='unicode',method='html')
  for filename in ['refinement.js','showroom.js','packaging.js','product.js','model-loader.js']:out=re.sub(r'(assets/'+re.escape(filename)+r')(?:\?[^"\s>]*)?',r'\1?v=20261023-fast-final',out)
  page.write_text(out)
 refs=''.join(p.read_text() for p in D.rglob('*.html'))
 for bundle in A.glob('bundle-*.css'):
  if bundle.name not in refs:bundle.unlink()
 (D/'.nojekyll').touch();print('Precomputed textures:',len(lookup),'responsive image sets:',len(responsive),'new variants:',len(jobs))
if __name__=='__main__':main()
