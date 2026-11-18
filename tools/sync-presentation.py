"""Synchronize text in the existing editable deck and render the matching PDF.

The deck retains its masters, geometry, images and text styling. XML edits only
replace the existing text placeholders and presenter notes.
"""
from pathlib import Path
import json,zipfile,io,html
from lxml import etree as E
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor,white

R=Path(__file__).resolve().parents[1]
D=json.loads((R/'src/seance.json').read_text(encoding='utf-8'))
P=R/'public/supports/presentation-S17.pptx'
NS={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
REL='http://schemas.openxmlformats.org/package/2006/relationships'
RID='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
source=zipfile.ZipFile(io.BytesIO(P.read_bytes()))
out=io.BytesIO()
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for entry in source.infolist():
  payload=source.read(entry.filename)
  if entry.filename.startswith('ppt/slides/slide') and entry.filename.endswith('.xml'):
   number=int(entry.filename.split('slide')[-1].split('.')[0]);s=D['slides'][number-1]
   root=E.fromstring(payload);nodes=root.findall('.//a:t',NS)
   values=['MODULE 05  /  SÉANCE 17',f'{number:02} / 22',s['gesture']]
   if number==1:
    values+=['Comprendre','le Web',s['lead']]+[v for pair in s['points'] for v in pair]+['SUPPORT FOURNI','HTML · CSS · JS','Observer, expliquer,','essayer.','Ouvrir le mini-site']
   elif number==4:
    values+=[s['title'],s['lead']]+[v for i,pair in enumerate(s['points'],1) for v in [f'{i:02}',*pair]]
   else:
    values+=[s['title'],s['lead']]+[v for pair in s['points'] for v in pair]
    if number==22:values+=['Trace','Carnet et question pour S18']
   if len(values)!=len(nodes):raise ValueError(f'Slide {number}: {len(values)} values, {len(nodes)} text nodes')
   for node,value in zip(nodes,values):node.text=value
   if s.get('resource'):
    run=nodes[2].getparent();props=run.find('{'+NS['a']+'}rPr')
    if props is None:props=E.Element('{'+NS['a']+'}rPr');run.insert(0,props)
    for old in props.findall('{'+NS['a']+'}hlinkClick'):props.remove(old)
    E.SubElement(props,'{'+NS['a']+'}hlinkClick',{'{'+RID+'}id':'S17Support'})
   payload=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
  elif entry.filename.startswith('ppt/slides/_rels/slide') and entry.filename.endswith('.xml.rels'):
   number=int(entry.filename.split('/slide')[-1].split('.')[0]);s=D['slides'][number-1]
   if s.get('resource'):
    root=E.fromstring(payload)
    for old in list(root):
     if old.get('Id')=='S17Support':root.remove(old)
    E.SubElement(root,'{'+REL+'}Relationship',Id='S17Support',Type=RID+'/hyperlink',Target='../'+s['resource'],TargetMode='External')
    payload=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
  elif entry.filename.startswith('ppt/notesSlides/notesSlide') and entry.filename.endswith('.xml'):
   number=int(entry.filename.split('notesSlide')[-1].split('.')[0]);root=E.fromstring(payload)
   nodes=root.findall('.//a:t',NS)
   for i,node in enumerate(nodes):node.text=D['slides'][number-1]['note'] if i==0 else ''
   payload=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
  elif entry.filename=='docProps/core.xml':
   root=E.fromstring(payload)
   for node in root:
    if E.QName(node).localname in ['title','subject','description','keywords']:node.text='S17 — Comprendre les fondations du Web — support fourni'
   payload=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
  z.writestr(entry,payload)
P.write_bytes(out.getvalue())

# Screen-readable landscape PDF, sharing the exact slide content and order.
W,H=960,540
C=canvas.Canvas(str(R/'public/supports/presentation-S17.pdf'),pagesize=(W,H))
C.setTitle('S17 — Comprendre les fondations du Web');C.setAuthor(D['meta']['author'])
NAVY=HexColor('#071b33');GOLD=HexColor('#b08740');MUTED=HexColor('#52667a')
def para(text,x,top,width,size,color,bold=False,maxheight=None):
 style=ParagraphStyle('slide',fontName='Helvetica-Bold' if bold else 'Helvetica',fontSize=size,leading=size*1.35,textColor=color)
 p=Paragraph(html.escape(text),style);_,height=p.wrap(width,H)
 if maxheight is not None and height>maxheight:raise ValueError(f'Text overflows PDF: {text}')
 p.drawOn(C,x,H-top-height);return height
for i,s in enumerate(D['slides']):
 dark=s['dark'];fg=white if dark else NAVY;muted=HexColor('#d4dfe9') if dark else MUTED
 C.setFillColor(NAVY if dark else HexColor('#f7f9fb'));C.rect(0,0,W,H,fill=1,stroke=0)
 para('MODULE 05 / SÉANCE 17',48,29,600,10,muted,True)
 C.setFillColor(white);C.rect(815,465,96,48,fill=1,stroke=0);C.drawImage(str(R/'public/assets/logo-LN-IA.png'),819,469,88,40,preserveAspectRatio=True,mask='auto')
 para(s['title'],48,91,850,30,fg,True,90)
 para(s['lead'],48,170,850,17,muted,maxheight=48)
 n=len(s['points']);cols=1 if n==1 else 2 if n in [2,4,6] else 3
 rows=(n+cols-1)//cols;cw=(864-(cols-1)*24)/cols;rh=215/rows
 for j,(label,text) in enumerate(s['points']):
  x=48+(j%cols)*(cw+24);top=244+(j//cols)*rh
  C.setStrokeColor(GOLD);C.setLineWidth(1);C.line(x,H-top,x+cw,H-top)
  lh=para(label,x,top+9,cw,13 if n>4 else 15,fg,True,maxheight=48)
  para(text,x,top+14+lh,cw,12 if n>4 else 14,muted,maxheight=rh-lh-18)
 C.setStrokeColor(GOLD);C.line(48,55,912,55)
 para(s['gesture'],48,493,815,10,muted,maxheight=30)
 if s.get('resource'):
  para(s['resourceLabel'],48,514,815,9,muted)
  C.linkURL('../'+s['resource'],(48,8,700,27),relative=1)
 para(f'{i+1:02} / 22',865,493,60,10,muted)
 C.showPage()
C.save()
# The workshop poster is a render of the current cover, never a cached old slide.
import fitz
with fitz.open(R/'public/supports/presentation-S17.pdf') as document:
 document[0].get_pixmap(matrix=fitz.Matrix(1280/W,1280/W)).save(R/'public/assets/affiche-S17.png')
print('22 diapositives et notes synchronisées ; PDF régénéré.')
