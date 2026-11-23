"""Audit local deliverables, nested archives and internal navigation."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from io import BytesIO
import zipfile,re,json,hashlib
import fitz

R=Path(__file__).resolve().parents[1]
# Assembled identifiers avoid retaining removed project labels in the pack.
removed=[' '.join(['roue','libre']),'-'.join(['roue','libre']),' '.join(['cap','études']),'-'.join(['cap','etudes']),' '.join(['studio','nadia']),'-'.join(['studio','nadia']),'-'.join(['terre','argile']),'terre d’'+'argile','terre & '+'argile','cas '+'fictif','cas-'+'fictifs','03-'+'cas']
errors=[];counts={'files':0,'archives':0,'pdf_pages':0,'links':0}
def audit_text(text,label):
 # Independent reference pack: S17 editorial exclusions do not apply.
 if label.startswith('Pack-Web-developpement-ln-ia.zip'):return
 normalized=text.lower()
 for old in removed:
  if old == 'cas '+'fictif' and 'livrables-S18' in label:continue
  if old in normalized:errors.append(f'Obsolete label in {label}: {old}')
def payload(data,name,label):
 audit_text(name,label+' [name]')
 if name.lower().endswith(('.zip','.pptx')):
  counts['archives']+=1
  with zipfile.ZipFile(BytesIO(data))as z:
   for entry in z.infolist():
    if '.git' in entry.filename.replace('\\','/').split('/'):errors.append(f'Git metadata in archive: {label}!{entry.filename}')
    if not entry.is_dir():payload(z.read(entry),entry.filename,label+'!'+entry.filename)
 elif name.lower().endswith('.pdf'):
  with fitz.open(stream=data,filetype='pdf')as doc:
   for i,page in enumerate(doc):counts['pdf_pages']+=1;audit_text(page.get_text(),f'{label}:{i+1}')
 elif name.lower().endswith(('.html','.md','.txt','.json','.js','.mjs','.css','.xml','.rels','.yml','.py')):
  audit_text(data.decode('utf-8-sig',errors='replace'),label)
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=set();self.links=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id'in a:
   if a['id']in self.ids:errors.append('Duplicate HTML id: '+a['id'])
   self.ids.add(a['id'])
  for attr in ['href','src']:
   if attr in a:self.links.append(a[attr])
cache={}
def page(p):
 if p not in cache:cache[p]=Page(p.read_text(encoding='utf-8-sig'))
 return cache[p]
for p in R.rglob('*'):
 if not p.is_file() or any(part in p.parts for part in ['node_modules','__pycache__','.git','tmp','Web-developpement-ln-ia']) or p.name=='MANIFEST-SHA256.txt':continue
 counts['files']+=1;payload(p.read_bytes(),str(p.relative_to(R)),str(p.relative_to(R)))
 if p.suffix=='.html':
  for link in page(p).links:
   u=urlsplit(link)
   if u.scheme or u.netloc or not link:continue
   target=(R/u.path.lstrip('/')) if u.path.startswith('/') else p.parent/unquote(u.path) if u.path else p
   target=target.resolve()
   # Vite serves the public directory at the root for the source index.
   if p==R/'index.html' and not target.exists() and target.is_relative_to(R):
    public_target=R/'public'/target.relative_to(R)
    if public_target.exists():target=public_target.resolve()
   if not target.is_relative_to(R):errors.append(f'Link escapes atelier: {p}: {link}');continue
   if not target.exists():errors.append(f'Missing HTML target: {p.relative_to(R)} -> {link}');continue
   if target.suffix=='.html' and u.fragment and unquote(u.fragment) not in page(target).ids:errors.append(f'Missing anchor: {p.relative_to(R)} -> {link}')
   counts['links']+=1
if errors:
 print('\n'.join(errors));raise SystemExit(1)
manifest=[]
for p in sorted(R.rglob('*')):
 if p.is_file() and not any(part in p.parts for part in ['node_modules','__pycache__','.git','tmp','Web-developpement-ln-ia']) and p.relative_to(R).parts[0]!='mon-dossier-challenge-Module05' and p.name!='MANIFEST-SHA256.txt':manifest.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(R).as_posix())
(R/'MANIFEST-SHA256.txt').write_text('\n'.join(manifest)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(counts,ensure_ascii=False));print('Pack vérifié : contenu, archives, PDF, liens HTML et ancres. Manifeste actualisé.')
