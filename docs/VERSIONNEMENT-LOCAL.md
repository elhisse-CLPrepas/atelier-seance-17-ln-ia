# Deux dépôts Git locaux indépendants

## Emplacements et remotes

| Dépôt local | Branche | Remote origin |
| --- | --- | --- |
| Racine de l’atelier S17 | main | https://github.com/elhisse-CLPrepas/atelier-seance-17-ln-ia.git |
| mon-dossier-challenge-Module05/ | main | https://github.com/elhisse-CLPrepas/mon-dossier-challenge-Module05.git |

Le dossier Challenge conserve son emplacement physique pour préserver les chemins locaux. Son propre `.git` porte l’historique commun du Module 05. La racine S17 ignore entièrement ce dossier : une modification de la source commune se versionne dans le dépôt commun.

`public/dossier-challenge/`, le kit et `dist/` sont des instantanés de diffusion intégrés à S17. Ils ne sont pas des copies de travail du dépôt commun. Modifiez les sources dans `mon-dossier-challenge-Module05/`, puis reconstruisez S17 pour actualiser ses instantanés. Les copies et archives de diffusion excluent les métadonnées Git.

## Vérifier les deux dépôts

Depuis la racine de S17 :

```powershell
git status --short --branch
git remote -v
git -C mon-dossier-challenge-Module05 status --short --branch
git -C mon-dossier-challenge-Module05 remote -v
```

## Enregistrer le travail local

Pour une production commune S17 à S20 :

```powershell
git -C mon-dossier-challenge-Module05 status
git -C mon-dossier-challenge-Module05 add .
git -C mon-dossier-challenge-Module05 diff --cached --stat
git -C mon-dossier-challenge-Module05 commit -m "Documenter la production du Module 05"
```

Pour l’atelier S17 :

```powershell
git status
git add .
git diff --cached --stat
git commit -m "Actualiser l’atelier S17"
```

## Première synchronisation avec GitHub

La préparation locale ne réalise aucun envoi. Après validation du contenu à partager, les premiers envois pourront être effectués séparément :

```powershell
git -C mon-dossier-challenge-Module05 push -u origin main
git push -u origin main
```

Ces commandes établissent le suivi de `origin/main`. Si GitHub a reçu de nouveaux commits entre-temps, examiner l’historique distant avant de réessayer ; ne pas forcer l’envoi.

## Reprendre le dossier depuis un autre atelier

Au premier usage, depuis la racine de l’atelier concerné :

```powershell
git clone https://github.com/elhisse-CLPrepas/mon-dossier-challenge-Module05.git mon-dossier-challenge-Module05
```

Le dépôt de cet atelier doit également ignorer `/mon-dossier-challenge-Module05/`. Ensuite, avec un dossier de travail propre et après l’établissement du suivi distant :

```powershell
git -C mon-dossier-challenge-Module05 status
git -C mon-dossier-challenge-Module05 pull --ff-only
```

Enregistrer les productions de l’atelier dans le dépôt commun, puis les partager par un commit et un push dédiés. Un autre atelier les récupère par `pull --ff-only`. La synchronisation n’est pas automatique et les ateliers voisins ne sont pas modifiés par cette préparation.

## Reconstruire S17

Après un nouveau clone de S17, cloner le dépôt commun dans le sous-dossier indiqué avant de lancer `npm ci` et `npm run build`. La génération lit le dossier commun sans modifier ses productions.

`npm run prepare:challenge` est une commande explicite qui crée seulement les modèles S17 manquants. Elle conserve tout fichier déjà présent. Relire ces ajouts et les enregistrer dans le dépôt commun.

Les sauvegardes temporaires, dépendances locales et fichiers `.env` sont exclus du versionnement. Les règles de fins de ligne sont définies par `.gitattributes` dans chaque dépôt.
