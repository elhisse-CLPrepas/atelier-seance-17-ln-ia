# Instructions pratiques — Atelier S17

**Module 05 · Comprendre les fondations du Web**  
**Séance : vendredi 20 novembre 2026 · Durée proposée : 90 minutes**  
**Livrable : carnet d’essai et preuve personnelle · Démonstration locale, à valider**

## 1. But de l’atelier

Observer une page de démonstration, expliquer les rôles de HTML, CSS, JavaScript et du navigateur, puis conserver la trace de ses essais. La production du support par l’IA est une préparation du formateur ; pendant S17, le participant étudie le mini-site fourni. Le sujet personnel et le plan du futur site se préparent pour S18.

## 2. Préparer les supports — avant les 90 minutes

Le formateur rassemble :

- un guide source lisible, en PDF, DOCX, Markdown ou texte ;
- une ou plusieurs affiches originales ;
- les compléments utiles : logo, illustrations, schémas, textes ou liens documentaires ;
- les consignes S17 et le calendrier confirmé ;
- le [prompt maître](PROMPT-MAITRE-MINI-SITE-S17.md).

Dans ce dossier, les références S17 sont le [conducteur](public/supports/conducteur-S17.md), le [cadrage du module](docs/PROMPT-MAITRE-MODULE-05.md) et la [grille de revue](public/dossier-challenge/06-PORTFOLIO/grille-revue-S17.md). Le guide `Web-developpement-ln-ia.docx` peut être joint comme source de contenu ; les affiches sont dans `AFFICHES/`. Le prompt demande à l’IA de lire les pièces réellement fournies avant de produire la page.

Pour préparer un nouveau support :

1. Copier le bloc du prompt maître dans l’outil IA choisi.
2. Renseigner ses champs et joindre les fichiers ou donner leurs chemins accessibles.
3. Faire produire une copie distincte du mini-site, avec le statut **V1 — À VALIDER**.
4. Contrôler les contenus, images, chemins et interactions avant de le distribuer.

Pour animer immédiatement S17, utiliser le support existant : [mini-site fourni](mini-site-demonstration-seance-17-v1-a-valider/index.html). La copie de travail se trouve dans `mon-dossier-challenge-Module05/04-WEB/mini-site-demonstration/`. Conserver les originaux et travailler sur une copie.

## 3. Ouvrir son espace

1. Extraire complètement le pack si nécessaire.
2. Ouvrir `OUVRIR-SEANCE-17.html`, puis l’accueil `mon-dossier-challenge-Module05/index.html`.
3. Retrouver le mini-site, le carnet dans `01-SUIVI/carnet-essai-S17.html` et le portfolio `06-PORTFOLIO/`.
4. Ouvrir le mini-site dans le navigateur et ses fichiers dans un éditeur.

Les trois fichiers à repérer sont `index.html`, `css/styles.css` et `js/app.js`. La démonstration doit fonctionner localement sans installation ni connexion. Une adresse de fichier local ne constitue pas une publication sur Internet.

## 4. Suivre le parcours S17

| Temps | Action du participant | Trace attendue |
| --- | --- | --- |
| 00–08 min | Ouvrir le dossier, le mini-site et le carnet. | Retrouver les trois éléments. |
| 08–20 min | Associer un titre à HTML, une couleur ou disposition à CSS et une interaction à JavaScript. | Un exemple visible et le fichier correspondant pour chaque rôle. |
| 20–35 min | Prédire l’effet du bouton, l’activer, revenir à l’état initial et ouvrir la console. | Prédiction puis observation réelle des deux états. |
| 35–65 min | Tester les liens, le clavier et une largeur mobile ; renseigner le carnet. | Parcours, difficulté éventuelle et explication personnelle. |
| 65–80 min | Faire retrouver l’interaction puis le carnet par un binôme, sans aide orale. | Chemin suivi, hésitations, amélioration proposée et nouvel essai. |
| 80–90 min | Exporter le carnet, rouvrir les traces et préparer une question pour S18. | Fichiers retrouvables dans le portfolio et revue humaine. |

## 5. Réaliser les essais

- **HTML :** retrouver un titre, une section et un lien dans le code, puis les montrer dans la page.
- **CSS :** retrouver une règle qui explique un effet visible. Sur la copie, changer une seule valeur réversible, actualiser, comparer et rétablir si nécessaire.
- **JavaScript :** écrire sa prédiction avant le clic ; observer l’apparition puis la disparition du texte et le changement de libellé. Retrouver le gestionnaire dans `js/app.js`.
- **Navigateur et console :** ouvrir les outils de développement, repérer le message de démonstration et noter toute erreur réellement rencontrée. Le navigateur lit et assemble les ressources ; la console aide à observer les messages et erreurs.
- **Navigation :** utiliser Tab et Maj+Tab, puis Entrée sur les liens et Entrée ou Espace sur le bouton. Vérifier le focus visible et le retour en haut.
- **Affichage :** réduire la fenêtre à environ 375 px et essayer le zoom à 200 %. Noter les débordements ou contenus inaccessibles.
- **Binôme :** demander « Retrouvez l’interaction puis le carnet ». Observer sans indiquer le chemin, proposer une correction limitée et rejouer le même parcours.

Une explication de l’IA reste à confronter au fichier et au navigateur. Ne pas recopier un résultat d’essai qui n’a pas été observé.

## 6. Conserver ses preuves

Dans le carnet, renseigner les rôles des trois technologies, le navigateur, la console, local/publié, la prédiction, les observations, l’amélioration et la question pour S18.

Exporter le Markdown vers `06-PORTFOLIO/carnet-essai-S17.md` et compléter `06-PORTFOLIO/preuve-S17.md`. Conserver aussi le JSON de sauvegarde du carnet si une reprise est nécessaire. Un téléchargement ne remplace pas automatiquement un fichier existant : choisir son emplacement et rouvrir la copie enregistrée.

## 7. Faire la revue humaine

- [ ] Je retrouve un titre et une section dans le HTML.
- [ ] J’explique une couleur ou une disposition avec le CSS.
- [ ] Je décris les deux états du bouton et le rôle de JavaScript.
- [ ] J’explique le navigateur et la console.
- [ ] J’atteins une section puis le carnet à la souris ou au clavier.
- [ ] Je distingue fichiers locaux et site publié.
- [ ] Je rouvre le carnet et la preuve depuis mon dossier.

Le pilote consigne son nom, la date, une observation et sa décision dans la preuve. Les réponses, résultats et validations restent **À COMPLÉTER** jusqu’au travail réel. Le quiz aide à réviser ; la revue humaine apprécie la compréhension.

## 8. Préparer S18

Conserver une question précise, une amélioration à poursuivre et un sujet personnel possible. S18 prépare le contenu et le plan ; S19 assemble une première version ; S20 observe un lecteur et améliore le résultat. Aucune publication n’est réalisée pendant S17.
