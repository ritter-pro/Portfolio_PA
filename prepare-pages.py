from pathlib import Path
import argparse,shutil
p=argparse.ArgumentParser();p.add_argument('--url',required=True);p.add_argument('--output',default='_site');a=p.parse_args();src=Path(__file__).parent/'dist';out=Path(a.output)
if out.resolve()==src.resolve():raise SystemExit('Choose a separate output directory')
shutil.copytree(src,out,dirs_exist_ok=True)
for page in out.rglob('*.html'):
 s=page.read_text().replace('https://polina-pa2004.wintrypetal1.chatgpt.site',a.url.rstrip('/'));page.write_text(s)
(out/'.nojekyll').touch();print('Prepared static site:',out)
