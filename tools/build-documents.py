"""Regenerate the printable supports from src/seance.json (pip install reportlab)."""
from pathlib import Path
import json,html,shutil,zipfile
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'public/supports'; OUT.mkdir(exist_ok=True,parents=True)
D=json.loads((ROOT/'src/seance.json').read_text())
fontdir=Path('/usr/share/fonts/truetype/dejavu')
if fontdir.exists():
    for name,file in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,str(fontdir/file)))
else:
    pdfmetrics.registerFontFamily('Helvetica',normal='Helvetica',bold='Helvetica-Bold')
FONT='Body' if fontdir.exists() else 'Helvetica';BOLD='Bold' if fontdir.exists() else 'Helvetica-Bold'
pdfmetrics.registerFontFamily(FONT,normal=FONT,bold=BOLD,italic=FONT,boldItalic=BOLD)
NAVY=colors.HexColor('#071b33'); GOLD=colors.HexColor('#b08740');MUTED=colors.HexColor('#52667a');LINE=colors.HexColor('#d9e2e8')
S=getSampleStyleSheet()
for name,fontsize,leading,color,font in [('Title',28,33,NAVY,BOLD),('Heading1',19,24,NAVY,BOLD),('Heading2',13,18,NAVY,BOLD),('BodyText',10.2,16,NAVY,FONT),('Normal',10.2,16,NAVY,FONT)]:
    S[name].fontName=font;S[name].fontSize=fontsize;S[name].leading=leading;S[name].textColor=color;S[name].spaceAfter=10
S.add(ParagraphStyle('Small',fontName=FONT,fontSize=8.5,leading=13,textColor=MUTED,spaceAfter=8))
S.add(ParagraphStyle('Kicker',fontName=BOLD,fontSize=8,leading=12,textColor=GOLD,spaceAfter=10))
S.add(ParagraphStyle('Label',fontName=BOLD,fontSize=9.5,leading=14,textColor=NAVY,spaceAfter=5))
S.add(ParagraphStyle('Quote',fontName=FONT,fontSize=13,leading=21,textColor=NAVY,leftIndent=13,spaceAfter=17))
def p(text,style='BodyText'):return Paragraph(html.escape(str(text)).replace('\n','<br/>'),S[style])
def head(k,title,intro=''):
    return [p(k.upper(),'Kicker'),p(title,'Title')]+([p(intro)]if intro else[])+[Spacer(1,12)]
def label(l,t):return [p(l,'Heading2'),p(t)]
def rulelines(count=2):
    t=Table([['']]*count,colWidths=[481],rowHeights=[22]*count)
    t.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),.4,LINE)]));return t
def frame(canvas,doc):
    canvas.saveState();w,h=doc.pagesize
    canvas.setFillColor(NAVY);canvas.rect(0,h-64,w,64,fill=1,stroke=0)
    canvas.setFillColor(colors.white);canvas.rect(36,h-55,77,39,fill=1,stroke=0)
    canvas.drawImage(str(ROOT/'public/assets/logo-LN-IA.png'),38,h-53,73,36.5,preserveAspectRatio=True,anchor='c')
    canvas.setFont(BOLD,8.5);canvas.setFillColor(colors.white);canvas.drawString(132,h-31,'CHALLENGE 100 JOURS · AUTOMNE 2026')
    canvas.setFont(FONT,8);canvas.setFillColor(colors.HexColor('#f0cc83'));canvas.drawString(132,h-46,'MODULE 05  /  SÉANCE 17')
    canvas.setStrokeColor(GOLD);canvas.setLineWidth(.8);canvas.line(40,42,w-40,42)
    canvas.setFillColor(MUTED);canvas.setFont(FONT,7.5);canvas.drawString(40,28,'LN-IA · Prof. Abderrahman EL HISSE');canvas.drawRightString(w-40,28,f'{doc.page}')
    canvas.restoreState()
def pdf(name,story):
    doc=SimpleDocTemplate(str(OUT/name),pagesize=(595.28,841.89),rightMargin=48,leftMargin=48,topMargin=91,bottomMargin=62,title=name.replace('-',' ').replace('.pdf',''),author=D['meta']['author'])
    doc.build(story,onFirstPage=frame,onLaterPages=frame)

story=[]
for j in range(3):
    if j:story.append(PageBreak())
    story+=head('CONDUCTEUR · 90 MINUTES', 'Comprendre les fondations du Web' if j==0 else ['','Essayer et expliquer','Conserver et transmettre'][j],D['meta']['dateLabel'] if j==0 else 'Appuyez chaque décision sur une pièce visible.')
    if j==0:story+=[p('Avant la séance','Heading2'),p('Ouvrir le dossier Challenge et le mini-site fourni. Vérifier la projection, le mini-site fourni et le carnet et les téléchargements. Préparer le dossier candidat et les binômes. Horaire à communiquer par le formateur.')]
    for phase in D['phases'][j*2:j*2+2]:
        story+=[p(phase['time']+' min · '+phase['verb']+' · vues '+phase['slides'],'Heading1')]
        for a,k in [('Formateur','trainer'),('Candidat','candidate'),('À observer','observe'),('Relance','relance')]:story+=[p(a,'Label'),p(phase[k])]
    if j==2:story+=[p('Décision de fin de séance','Heading2'),p('Le pilote nomme la pièce examinée, date sa revue et consigne son observation. Le score du quiz et les cases cochées ne suffisent pas à valider une production.')]
pdf('conducteur-S17.pdf',story)

story=head('CARNET D’ESSAI S17 · 1 / 2','Comprendre le Web','Ouvrez le mini-site fourni depuis votre dossier Challenge. Notez uniquement vos observations réelles.')
for l in ['Projet, nom et date','HTML : élément observé et rôle','CSS : disposition observée et rôle','JavaScript : prédiction avant le clic','JavaScript : état avant, après, puis au second clic','Navigateur et console : mon explication']:
    story += [p(l,'Label'),rulelines(2),Spacer(1,8)]
story += [PageBreak()] + head('CARNET D’ESSAI S17 · 2 / 2','Navigation et trace','Testez le parcours au clavier et à la souris, puis réduisez la fenêtre.')
for l in ['Parcours de navigation et difficulté','Amélioration proposée et nouvel essai','Local ou publié : état et justification','Mots du binôme et décision motivée','Question à reprendre en S18','Pilote, date et statut']:
    story += [p(l,'Label'),rulelines(2),Spacer(1,8)]
pdf('fiche-candidat-S17.pdf',story)

guide=[
 ('Lire une page web','Trois rôles complémentaires',[
  ('HTML organise le contenu','Un titre, un paragraphe, une liste et un lien sont des éléments de structure. Le titre décrit la ressource. Le lien relie le libellé à une cible.'),
  ('CSS présente la structure','La feuille de style règle la largeur, les espacements, les couleurs et la typographie. Elle aide à lire les informations dans un ordre clair.'),
  ('JavaScript fait réagir la page','Le code peut changer la diapositive, retourner une carte, corriger un quiz ou sauvegarder un carnet. Un site de lecture simple peut aussi fonctionner sans ces interactions.'),
  ('Manipulation en séance','Dans Démonstration, modifiez le titre HTML, la couleur CSS puis affichez le détail JavaScript. Observez une variation à la fois.')]),
 ('Construire et distribuer','Bootstrap et Vite dans cet atelier',[
  ('Bootstrap','Le mini-site emploie la grille responsive, les formulaires, les boutons et le menu repliable de Bootstrap. Le style LN-IA complète ces structures.'),
  ('Vite','Vite sert le projet pendant le travail et assemble une version statique dans dist. Les fichiers JavaScript et CSS sont groupés pour la diffusion. Les dépendances sont verrouillées dans package-lock.json.'),
  ('Deux modes d’ouverture','Après extraction complète, OUVRIR-SEANCE-17.html charge les fonctions intégrées et les ressources de dist. Pour modifier les sources : npm ci puis npm run dev. Pour reconstruire : npm run build.'),
  ('Les fichiers de référence','src/seance.json porte les diapositives, les observations, les cartes, le quiz et les prompts. Les supports PDF et PPTX du pack partagent cet ordre et ce contenu. Une modification des slides exige aussi de régénérer les supports de présentation.')]),
 ('Être lisible et identifiable','Le référencement d’une ressource pédagogique',[
  ('Un contenu identifiable','Le titre de page et la description annoncent le sujet. La langue, les titres de sections et les liens descriptifs aident la lecture. Les métadonnées ne garantissent aucun rang dans un moteur.'),
  ('Le partage social','Les balises Open Graph et Twitter décrivent la séance. Une image de partage et une URL absolue s’ajoutent lorsque publicUrl est renseigné dans site.config.json.'),
  ('Avant publication','Le pack reste en noindex tant que l’adresse publique n’est pas renseignée et indexable n’est pas activé. Lors de la publication autorisée, renseigner l’URL HTTPS réelle, choisir indexable: true, puis reconstruire. Le canonical et le sitemap sont alors générés.'),
  ('Les références officielles','Bootstrap : getbootstrap.com/docs/5.3/getting-started/vite/\nVite : vite.dev/guide/static-deploy.html\nGoogle : developers.google.com/search/docs/fundamentals/seo-starter-guide?hl=fr')])]
story=[]
for i,(k,t,items) in enumerate(guide):
    if i:story.append(PageBreak())
    story+=head(k,t)
    for a,b in items:story+=label(a,b)+[Spacer(1,10)]
pdf('guide-web-S17.pdf',story)

story=[]
for chunk in range(3):
    if chunk:story.append(PageBreak())
    story+=head('RÉVISION · FLASHCARDS','Expliquer avec vos propres mots','Lisez la question, répondez puis confrontez votre réponse au repère.')
    for i,(q,a) in enumerate(D['cards'][chunk*4:chunk*4+4],chunk*4+1):story+=[p(str(i)+'. '+q,'Heading2'),p(a),Spacer(1,15)]
for chunk in range(4):
    story.append(PageBreak());story+=head('RÉVISION · QUIZ CORRIGÉ','Comparer les trois choix','Le score sert à reprendre les notions. La validation du dossier repose sur vos pièces et votre essai.')
    for i,(q,choices,correct,explanations) in enumerate(D['quiz'][chunk*2:chunk*2+2],chunk*2+1):
        story+=[p(str(i)+'. '+q,'Heading2')]
        for j,(choice,exp) in enumerate(zip(choices,explanations)):story+=[p(str(j+1)+'. '+choice+(' · Choix attendu'if j==correct else ''),'Label'),p(exp,'Small')]
        story.append(Spacer(1,13))
pdf('revision-S17.pdf',story)
shutil.copyfile(OUT/'fiche-candidat-S17.pdf',OUT/'kit-candidat/fiche-candidat-S17.pdf')
shutil.copyfile(OUT/'prompts-S17.md',OUT/'kit-candidat/prompts-S17.md')
with zipfile.ZipFile(OUT/'kit-candidat-S17.zip','w',zipfile.ZIP_DEFLATED)as z:
    for pth in sorted((OUT/'kit-candidat').rglob('*')):
        if pth.is_file():z.write(pth,'kit-candidat-S17/'+str(pth.relative_to(OUT/'kit-candidat')))
print('Conducteur, carnet candidat, guide web, révision et kit produits.')
