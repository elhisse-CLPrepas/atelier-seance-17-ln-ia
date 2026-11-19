"""Append original poster plates to the existing editable S17 deck and PDF."""
from pathlib import Path
from io import BytesIO
import json, zipfile, html
from lxml import etree as E
from PIL import Image

R = Path(__file__).resolve().parents[1]
POSTERS = json.loads((R/'src/affiches.json').read_text(encoding='utf-8'))
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
RID = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
CT = 'http://schemas.openxmlformats.org/package/2006/content-types'

def xml(node):
    return E.tostring(node, xml_declaration=True, encoding='UTF-8', standalone=True)

def reset_deck(path):
    """Remove only our generated appendix before the existing synchronizer runs."""
    with zipfile.ZipFile(path) as z:
        files = {n:z.read(n) for n in z.namelist()}
    pres = E.fromstring(files['ppt/presentation.xml'])
    ids = pres.find('{'+P+'}sldIdLst')
    for node in list(ids):
        if node.get('{'+RID+'}id','').startswith('poster'):
            ids.remove(node)
    files['ppt/presentation.xml'] = xml(pres)
    rels = E.fromstring(files['ppt/_rels/presentation.xml.rels'])
    owned = set()
    for node in list(rels):
        if node.get('Id','').startswith('poster'):
            owned.add('/ppt/'+node.get('Target'))
            rels.remove(node)
    files['ppt/_rels/presentation.xml.rels'] = xml(rels)
    content = E.fromstring(files['[Content_Types].xml'])
    for node in list(content):
        if node.get('PartName','') in owned: content.remove(node)
    files['[Content_Types].xml'] = xml(content)
    for name in list(files):
        relation='/'+name.replace('/_rels/','/').removesuffix('.rels')
        if '/'+name in owned or relation in owned or name.startswith('ppt/media/poster-'):
            del files[name]
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in files.items(): z.writestr(name,data)

def append_deck(path):
    with zipfile.ZipFile(path) as z: files = {n:z.read(n) for n in z.namelist()}
    pres = E.fromstring(files['ppt/presentation.xml'])
    size = pres.find('{'+P+'}sldSz'); w,h = int(size.get('cx')),int(size.get('cy'))
    ids = pres.find('{'+P+'}sldIdLst')
    rels = E.fromstring(files['ppt/_rels/presentation.xml.rels'])
    content = E.fromstring(files['[Content_Types].xml'])
    if not any(n.get('Extension')=='png' for n in content):
        E.SubElement(content,'{'+CT+'}Default',Extension='png',ContentType='image/png')
    def textbox(identifier,text,x,y,cx,cy,points,color):
        return f'<p:sp><p:nvSpPr><p:cNvPr id="{identifier}" name="Légende {identifier}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square"/><a:lstStyle/><a:p><a:r><a:rPr lang="fr-FR" sz="{points*100}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:latin typeface="Arial"/></a:rPr><a:t>{html.escape(text)}</a:t></a:r></a:p></p:txBody></p:sp>'
    for i,poster in enumerate(POSTERS,23):
        name=f'poster{i}'; image=R/'AFFICHES'/poster['source']
        iw,ih=Image.open(image).size
        maxw,maxh=int(w*.55),int(h*.75); scale=min(maxw/iw,maxh/ih)
        pw,ph=int(iw*scale),int(ih*scale); x,y=(w-pw)//2,int(h*.14)
        root=E.fromstring(f'<p:sld xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{RID}"><p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="071B33"/></a:solidFill><a:effectLst/></p:bgPr></p:bg><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')
        tree=root.find('.//{'+P+'}spTree')
        tree.append(E.fromstring(f'<root xmlns:p="{P}" xmlns:a="{A}">'+textbox(2,poster['title'],int(w*.05),int(h*.025),int(w*.9),int(h*.1),22,'FFFFFF')+'</root>')[0])
        tree.append(E.fromstring(f'<p:pic xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{RID}"><p:nvPicPr><p:cNvPr id="3" name="{html.escape(poster["title"])}" descr="Affiche originale non recadrée"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="image"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{pw}" cy="{ph}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>'))
        caption=f'Annexe {i-22}/9. '+poster['caption']+' Calendrier de référence : automne 2026.'
        tree.append(E.fromstring(f'<root xmlns:p="{P}" xmlns:a="{A}">'+textbox(4,caption,int(w*.05),int(h*.91),int(w*.9),int(h*.08),11,'D4DFE9')+'</root>')[0])
        files[f'ppt/slides/slide{i}.xml']=xml(root)
        sr=E.Element('{'+REL+'}Relationships',nsmap={None:REL})
        E.SubElement(sr,'{'+REL+'}Relationship',Id='image',Type=RID+'/image',Target=f'../media/poster-{i}.png')
        E.SubElement(sr,'{'+REL+'}Relationship',Id='layout',Type=RID+'/slideLayout',Target='../slideLayouts/slideLayout1.xml')
        files[f'ppt/slides/_rels/slide{i}.xml.rels']=xml(sr)
        files[f'ppt/media/poster-{i}.png']=image.read_bytes()
        E.SubElement(ids,'{'+P+'}sldId',id=str(max(int(n.get('id')) for n in ids)+1),attrib={'{'+RID+'}id':name})
        E.SubElement(rels,'{'+REL+'}Relationship',Id=name,Type=RID+'/slide',Target=f'slides/slide{i}.xml')
        E.SubElement(content,'{'+CT+'}Override',PartName=f'/ppt/slides/slide{i}.xml',ContentType='application/vnd.openxmlformats-officedocument.presentationml.slide+xml')
    files['ppt/presentation.xml']=xml(pres); files['ppt/_rels/presentation.xml.rels']=xml(rels); files['[Content_Types].xml']=xml(content)
    if 'docProps/app.xml' in files:
        app=E.fromstring(files['docProps/app.xml'])
        for node in app.iter():
            if E.QName(node).localname=='Slides': node.text='31'
        files['docProps/app.xml']=xml(app)
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in files.items(): z.writestr(name,data)

def append_pdf(canvas,W,H,para):
    from reportlab.lib.colors import HexColor,white
    for i,poster in enumerate(POSTERS,1):
        canvas.setFillColor(HexColor('#071b33'));canvas.rect(0,0,W,H,fill=1,stroke=0)
        para(poster['title'],48,20,864,22,white,True,60)
        image=R/'AFFICHES'/poster['source']; iw,ih=Image.open(image).size
        scale=min(650/iw,405/ih); pw,ph=iw*scale,ih*scale
        canvas.drawImage(str(image),(W-pw)/2,65,pw,ph,mask='auto')
        para(f'Annexe {i}/9. '+poster['caption'],48,487,864,10,white,maxheight=30)
        para('Support original conservé. Calendrier de référence : automne 2026.',48,519,864,9,white)
        canvas.showPage()
