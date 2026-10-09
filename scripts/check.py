#!/usr/bin/env python3
"""Validate links, images, styles, metadata and independent static runtime."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import re,sys,json
root=(Path(__file__).resolve().parents[1]/(sys.argv[1] if len(sys.argv)>1 else '_site')).resolve()
errors=[];pages=list(root.rglob('*.html'));ids={};refs=[]
class Audit(HTMLParser):
 def __init__(self,path):super().__init__();self.path=path;self.h1=0;self.title=False;self.desc=False;self.faq=0;self.robots=''
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id'in d:ids[self.path].add(d['id'])
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  if tag=='details':self.faq+=1
  if tag=='meta' and d.get('name')=='description':self.desc=True
  if tag=='meta' and d.get('name')=='robots':self.robots=d.get('content','')
  if tag=='iframe' and not d.get('title'):errors.append(f'{self.path}: iframe title missing')
  if tag=='img' and 'alt'not in d:errors.append(f'{self.path}: img alt missing')
  for key in ['href','src']:
   if key in d:refs.append((self.path,d[key]))
  # Image custom properties are resolved where used in the external CSS file.
  for u in re.findall(r'url\(([^)]+)\)',d.get('style','')):refs.append((root/'assets/css/accessibility.css',u.strip('\"\'')))
for path in pages:
 ids[path]=set();s=path.read_text();p=Audit(path);p.feed(s)
 if p.h1!=1:errors.append(f'{path}: expected one h1, found {p.h1}')
 if not p.title:errors.append(f'{path}: title missing')
 if path.name!='404.html' and not p.desc:errors.append(f'{path}: description missing')
 if not p.robots:errors.append(f'{path}: robots missing')
 if re.search(r'\{\{[A-Z_]+\}\}',s):errors.append(f'{path}: unresolved template')
 if re.search(r'https://(?:[^\"\s]*studio(?:design|\.site|\.design)|storage.googleapis.com)',s):errors.append(f'{path}: Studio dependency')
 if '<sd-toggle'in s or 'onclick='in s:errors.append(f'{path}: old runtime handler')
 for body in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):json.loads(body)
for path in root.rglob('*.css'):
 for u in re.findall(r'url\(([^)]+)\)',path.read_text()):refs.append((path,u.strip('\"\'')))
for path,u in refs:
 parsed=urlsplit(u)
 if parsed.scheme or u.startswith('//'):continue
 if not parsed.path and not parsed.fragment:continue
 if parsed.path.startswith('/'):errors.append(f'{path}: root absolute link {u}');continue
 target=(path.parent/unquote(parsed.path)).resolve() if parsed.path else path
 if target.is_dir():target=target/'index.html'
 if not target.exists():errors.append(f'{path.relative_to(root)}: missing {u}')
 elif parsed.fragment and target.suffix=='.html' and parsed.fragment not in ids.get(target,set()):errors.append(f'{path}: missing anchor {u}')
expected={'index.html':12,'yomogi/index.html':3,'spine/index.html':3,'facial/index.html':3,'headspa/index.html':0}
for p,count in expected.items():
 if len(re.findall(r'<details\b',(root/p).read_text()))!=count:errors.append(f'{p}: FAQ count mismatch')
if errors:
 print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(pages)} HTML pages; local links, anchors, assets, FAQ counts, titles, alt/title attributes, robots and JSON-LD. No Studio runtime/CDN references.')
