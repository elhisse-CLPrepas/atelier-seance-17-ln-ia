export const sections = [
  ['accueil', 'Accueil', 'house'],
  ['presentation', 'Présentation', 'play-circle'],
  ['methode', 'Méthode', 'signpost-split'],
  ['demonstration', 'Démonstration', 'layers'],
  ['atelier', 'Carnet d’essai', 'pencil-square'],
  ['prompts', 'Prompts', 'braces'],
  ['flashcards', 'Flashcards', 'stack'],
  ['quiz', 'Quiz', 'question-circle'],
  ['validation', 'Validation', 'check2-square'],
  ['portfolio', 'Portfolio', 'folder2-open'],
  ['ressources', 'Ressources', 'book']
];

export const projectFields = [
  ['project', 'Projet et sujet', 'Sujet de votre future page'],
  ['audience', 'Public visé', 'À qui la page s’adresse-t-elle ?'],
  ['need', 'Besoin du lecteur', 'Ce que votre lecteur cherche à faire'],
  ['reference', 'Référence du support ou de votre source', 'Ex. variantes-communication-projet.md, Message corrigé, V2'],
  ['source', 'Passage source vérifié', 'Recopiez le passage qui appuie votre futur contenu.'],
  ['mission', 'Mission de production', 'Structurer la page de mon projet'],
  ['constraints', 'Contraintes et limites', 'Informations disponibles, pièces à fournir, ton attendu'],
  ['title', 'Titre de la page', 'Le sujet que votre lecteur doit identifier'],
  ['hook', 'Accroche', 'Une phrase qui relie le sujet au besoin'],
  ['problem', 'Problème du lecteur', 'Le besoin auquel la page répond'],
  ['promise', 'Promesse étayée', 'Ce que la ressource permet effectivement'],
  ['benefit', 'Bénéfices vérifiables', 'L’utilité précise de la ressource'],
  ['support', 'Passage qui justifie la promesse', 'Citation ou repère dans la source'],
  ['action', 'Action unique', 'Un verbe concret et son objet'],
  ['target', 'Chemin de la cible', 'Ex. mini-site-demonstration/index.html, relatif au plan exporté']
];

export const proofFields = [
  ['htmlRole', 'HTML : un élément observé et son rôle'],
  ['cssRole', 'CSS : une disposition observée et son rôle'],
  ['jsRole', 'JavaScript : les deux états du bouton'],
  ['browserRole', 'Navigateur et console : ce que je peux expliquer'],
  ['localState', 'Local ou publié : état du support et justification'],
  ['navigation', 'Navigation : parcours, clavier, mobile et difficulté'],
  ['navigationAfter', 'Amélioration de navigation et résultat du nouvel essai'],
  ['question', 'Ma question pour S18'],
  ['prediction', 'Ma prédiction avant l’essai'],
  ['reader', 'Nom ou initiales du binôme'],
  ['testDate', 'Date de l’essai'],
  ['observed', 'Mots du lecteur et cible réellement ouverte'],
  ['before', 'Passage ou libellé avant correction'],
  ['after', 'Après correction ou maintien'],
  ['reason', 'Motif de ma décision et appui'],
  ['reopened', 'Résultat après réouverture et nouvel essai']
];

export const reviewFields = [
  ['pilot', 'Nom du pilote'],
  ['reviewDate', 'Date de revue'],
  ['review', 'Observation et décision motivée'],
  ['nextAction', 'Pièce ou action encore attendue']
];

export const resources = [
  { group: 'Projeter et animer', title: 'Présentation PowerPoint', format: 'PPTX', path: 'supports/presentation-S17.pptx', detail: '22 diapositives modifiables avec notes du présentateur.' },
  { group: 'Projeter et animer', title: 'Diaporama PDF', format: 'PDF', path: 'supports/presentation-S17.pdf', detail: 'Les mêmes 22 vues pour la projection ou la lecture.' },
  { group: 'Projeter et animer', title: 'Conducteur du formateur', format: 'PDF', path: 'supports/conducteur-S17.pdf', detail: 'Six phases, 90 minutes, gestes et relances.' },
  { group: 'Projeter et animer', title: 'Notes de présentation', format: 'MD', path: 'supports/notes-formateur-S17.md', detail: 'Une note orale et un geste pour chaque vue.' },
  { group: 'Projeter et animer', title: 'Affiche de séance', format: 'PNG', path: 'assets/affiche-S17.png', detail: 'S17, vendredi 20 novembre 2026.' },
  { group: 'Produire et documenter', title: 'Kit candidat complet', format: 'ZIP', path: 'supports/kit-candidat-S17.zip', detail: 'Modèles du plan, preuve, index, relais et fiche imprimable.' },
  { group: 'Produire et documenter', title: 'Fiche candidat à imprimer', format: 'PDF', path: 'supports/fiche-candidat-S17.pdf', detail: 'Rôles du Web, observation, navigation et décision.' },
  { group: 'Produire et documenter', title: 'Modèle du plan S17', format: 'MD', path: 'supports/kit-candidat/04-WEB/structure-page-projet.md', detail: 'À compléter dans votre dossier personnel.' },
  { group: 'Produire et documenter', title: 'Modèle de preuve S17', format: 'MD', path: 'supports/kit-candidat/06-PORTFOLIO/preuve-S17.md', detail: 'Référence, prédiction, observation et motif.' },
  { group: 'Produire et documenter', title: 'Index du portfolio', format: 'MD', path: 'supports/kit-candidat/06-PORTFOLIO/index-portfolio.md', detail: 'Ligne S17 et chemins des pièces du module.' },
  { group: 'Produire et documenter', title: 'Relais vers S18', format: 'MD', path: 'supports/kit-candidat/06-PORTFOLIO/relais-S18.md', detail: 'Plan et source à rouvrir le lundi 23 novembre.' },
  { group: 'Reprendre et approfondir', title: 'Prompts du candidat', format: 'MD', path: 'supports/prompts-S17.md', detail: 'Prompt maître, consignes après replay et quatre missions.' },
  { group: 'Comprendre avec le support fourni', title: 'Mon dossier Challenge', format: 'HTML', path: 'dossier-challenge/index.html', detail: 'Accueil, parcours, démonstration, carnet et portfolio.' },
  { group: 'Comprendre avec le support fourni', title: 'Mini-site de démonstration', format: 'HTML', path: 'dossier-challenge/04-WEB/mini-site-demonstration/index.html', detail: 'HTML, CSS, JavaScript, navigateur et local/public.' },
  { group: 'Comprendre avec le support fourni', title: 'Carnet d’essai autonome', format: 'HTML', path: 'dossier-challenge/01-SUIVI/carnet-essai-S17.html', detail: 'Saisie locale, reprise JSON et export Markdown.' },
  { group: 'Reprendre et approfondir', title: 'Guide des notions web', format: 'PDF', path: 'supports/guide-web-S17.pdf', detail: 'HTML, CSS, JavaScript, Bootstrap, Vite et métadonnées.' },
  { group: 'Reprendre et approfondir', title: 'Cartes et quiz corrigé', format: 'PDF', path: 'supports/revision-S17.pdf', detail: '12 cartes et 24 explications pour les huit situations.' },
  { group: 'Reprendre et approfondir', title: 'Prompt maître du Module 05', format: 'MD', path: 'supports/PROMPT-MAITRE-MODULE-05.md', detail: 'Le cadre de production des séances S17 à S20.' },
  { group: 'Sources du parcours', title: 'Atelier S16 et relais', format: 'WEB', url: 'https://elhisse-clprepas.github.io/atelier-seance-16-ln-ia/', detail: 'Retrouver le message corrigé et la clôture du module 04.' },
  { group: 'Sources du parcours', title: 'Modèle de relais S16', format: 'MD', path: 'supports/relais-S16-original.md', detail: 'Modèle provenant du dépôt S16, pour comparer les champs.' },
  { group: 'Sources du parcours', title: 'Bootstrap avec Vite', format: 'WEB', url: 'https://getbootstrap.com/docs/5.3/getting-started/vite/', detail: 'Documentation officielle d’intégration.' },
  { group: 'Sources du parcours', title: 'Publication statique avec Vite', format: 'WEB', url: 'https://vite.dev/guide/static-deploy.html', detail: 'Configuration et utilisation de la sortie dist.' },
  { group: 'Sources du parcours', title: 'Principes du référencement', format: 'WEB', url: 'https://developers.google.com/search/docs/fundamentals/seo-starter-guide?hl=fr', detail: 'Titres, contenu lisible et liens descriptifs.' }
];
