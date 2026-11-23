"""Package the approved S17 demonstration for a standalone cPanel directory."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib
import stat
import zipfile

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'mini-site-demonstration-seance-17'
BASE = 'https://clprepas.com/mini-site-demonstration-seance-17/'
WORKSHOP = 'https://elhisse-clprepas.github.io/atelier-seance-17-ln-ia/'
ARCHIVE = ROOT / 'mini-site-demonstration-seance-17-cpanel.zip'

files = {p.relative_to(SOURCE).as_posix(): p.read_bytes()
         for p in SOURCE.rglob('*') if p.is_file()}
html = files['index.html'].decode('utf-8')
html = html.replace('../mon-dossier-challenge-Module05/', WORKSHOP + 'dossier-challenge/')
html = html.replace('../OUVRIR-SEANCE-17.html#demonstration', WORKSHOP + '#demonstration')
html = html.replace('  <meta charset="utf-8">',
                    '  <meta charset="utf-8">\n  <link rel="canonical" href="' + BASE + '">')
html = html.replace('· Démonstration locale</p>', '· Support validé · Version cPanel</p>')
files['index.html'] = html.encode('utf-8')

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for key in ('src', 'href'):
            if key in attrs:
                self.links.append(attrs[key])

parser = Links()
parser.feed(html)
for link in parser.links:
    target = urlsplit(link)
    if target.scheme or target.netloc:
        continue
    if target.path:
        assert unquote(target.path) in files, f'Missing local resource: {link}'
    elif target.fragment:
        assert target.fragment in parser.ids, f'Missing anchor: {link}'
assert '../' not in html, 'A parent-directory dependency remains'

readme = files['README.md'].decode('utf-8')
readme += f'''\n## Distribution cPanel\n
Cette copie est préparée pour {BASE}. Le statut de validation du support
provient du README source. Les adaptations de distribution concernent les liens
vers l’atelier et le carnet (versions GitHub Pages), l’URL canonique et le pied
de page. Le déploiement cPanel reste à effectuer par le propriétaire.
'''
files['README.md'] = readme.encode('utf-8')
files['readme.txt'] = files['README.md']
files['DEPLOIEMENT-CPANEL.md'] = f'''# Déployer le mini-site validé sur cPanel

URL prévue : {BASE}

1. Dans cPanel, ouvrir le gestionnaire de fichiers et retrouver la racine
   documentaire du domaine clprepas.com (souvent public_html ; vérifier dans Domaines).
2. Créer le dossier mini-site-demonstration-seance-17 dans cette racine.
3. Si ce dossier contient déjà un site, en conserver une sauvegarde avant remplacement.
4. Téléverser ce ZIP dans le dossier créé, puis l’extraire à cet endroit.
   index.html doit être directement dans mini-site-demonstration-seance-17/,
   à côté de css/, js/ et assets/, sans dossier supplémentaire imbriqué.
5. Supprimer le ZIP téléversé après extraction.
   Vérifier les permissions : dossiers 755 et fichiers 644, notamment index.html.
6. Ouvrir {BASE} puis vérifier les images, les deux états du bouton,
   l’agrandissement de l’affiche, les ancres, le clavier et l’affichage mobile.
7. Vérifier les liens vers l’atelier, le dossier Challenge et le carnet :
   ils rejoignent GitHub Pages et demandent une connexion Internet.

Aucune installation, base de données ou configuration PHP n’est nécessaire.
Le mini-site conserve ses ressources locales et peut aussi être ouvert hors ligne
après extraction ; les accès GitHub Pages demandent une connexion.
Le carnet est hébergé sur GitHub Pages : ses données locales restent associées
à ce navigateur et à cette origine. Exporter les traces depuis le carnet.

## Contrôles du paquet

La génération vérifie les chemins locaux et les ancres HTML, la présence des
fichiers et l’intégrité ZIP. Les essais sur l’hébergement cPanel restent à faire
après téléversement. Aucun déploiement cPanel n’est exécuté par ce script.
'''.encode('utf-8')

with zipfile.ZipFile(ARCHIVE, 'w', zipfile.ZIP_DEFLATED) as archive:
    directories = sorted({parent.as_posix() + '/'
                          for name in files for parent in Path(name).parents
                          if parent != Path('.')})
    for name in directories:
        entry = zipfile.ZipInfo(name)
        entry.create_system = 3
        entry.external_attr = ((stat.S_IFDIR | 0o755) << 16) | 0x10
        archive.writestr(entry, b'')
    for name, content in sorted(files.items()):
        entry = zipfile.ZipInfo(name)
        entry.create_system = 3
        entry.external_attr = (stat.S_IFREG | 0o644) << 16
        entry.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(entry, content)
with zipfile.ZipFile(ARCHIVE) as archive:
    assert archive.testzip() is None
    assert 'index.html' in archive.namelist()
    for entry in archive.infolist():
        assert stat.S_IMODE(entry.external_attr >> 16) == (0o755 if entry.is_dir() else 0o644)
digest = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
ARCHIVE.with_suffix('.zip.sha256').write_text(f'{digest}  {ARCHIVE.name}\n', encoding='ascii')
print(f'ZIP: {ARCHIVE}\nFiles: {len(files)}\nBytes: {ARCHIVE.stat().st_size}\nSHA256: {digest}')
