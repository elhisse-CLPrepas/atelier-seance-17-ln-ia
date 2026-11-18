export const EMPTY = 'À compléter';
export const blankState = () => ({schema:'lnia-s17', version:2, fields:{targetState:'À fournir',status:'À COMPLÉTER'},checks:Array(7).fill(false),quiz:Array(8).fill(null),quizDone:false,known:[],cardOrder:Array.from({length:12},(_,i)=>i),card:0,demo:{},updatedAt:null});
export function normalizeState(value){
  if(!value || value.schema!=='lnia-s17' || value.version!==2) throw new Error('Ce fichier n’est pas un carnet S17 version 2.');
  const out=blankState();
  for(const [k,v] of Object.entries(value.fields||{})) if(/^[a-zA-Z]+$/.test(k)&&typeof v==='string') out.fields[k]=v.slice(0,40000);
  out.checks=out.checks.map((_,i)=>value.checks?.[i]===true);
  out.quiz=out.quiz.map((_,i)=>Number.isInteger(value.quiz?.[i])&&value.quiz[i]>=0&&value.quiz[i]<3?value.quiz[i]:null);
  out.quizDone=value.quizDone===true;
  out.known=Array.isArray(value.known)?[...new Set(value.known.filter(x=>Number.isInteger(x)&&x>=0&&x<12))]:[];
  if(Array.isArray(value.cardOrder)&&value.cardOrder.length===12&&new Set(value.cardOrder).size===12&&value.cardOrder.every(x=>Number.isInteger(x)&&x>=0&&x<12))out.cardOrder=value.cardOrder;
  out.card=Number.isInteger(value.card)&&value.card>=0&&value.card<12?value.card:0;
  if(value.demo&&typeof value.demo==='object')out.demo=value.demo;
  out.updatedAt=typeof value.updatedAt==='string'?value.updatedAt:null;
  if(!['À COMPLÉTER','À REVOIR','À VALIDER','VALIDÉ'].includes(out.fields.status))out.fields.status='À COMPLÉTER';
  if(!['À fournir','Disponible, à tester','Ouverture observée'].includes(out.fields.targetState))out.fields.targetState='À fournir';
  if(out.fields.status==='VALIDÉ'&&validationMissing(out).length)out.fields.status='À VALIDER';
  return out;
}
export function safeTarget(value=''){
  const s=value.trim();
  if(!s||/[\u0000-\u0020<>"()\\]/.test(s))return '';
  if(/^https?:\/\//i.test(s)){try{return new URL(s).href}catch{return ''}}
  if(/^[a-z][a-z0-9+.-]*:/i.test(s)||s.startsWith('//')||s.startsWith('/'))return '';
  return s;
}
const v=(f,k)=>f[k]?.trim()||EMPTY;
const quote=s=>s.split('\n').map(l=>'> '+l).join('\n');
export function planText(state){const f=state.fields;return `# Structure de ma page — S17

Statut du plan : ${v(f,'status')}
Projet : ${v(f,'project')}
Public : ${v(f,'audience')}
Besoin : ${v(f,'need')}
Format : plan Markdown

## Support ou source de départ

Référence, rubrique, version : ${v(f,'reference')}

${quote(v(f,'source'))}

## Mission et contraintes

Mission : ${v(f,'mission')}

Contraintes : ${v(f,'constraints')}

## 1. Titre

${v(f,'title')}

## 2. Accroche

${v(f,'hook')}

## 3. Problème du lecteur

${v(f,'problem')}

## 4. Promesse étayée

${v(f,'promise')}

Appui dans la source : ${v(f,'support')}

## 5. Bénéfices vérifiables

${v(f,'benefit')}

## 6. Action unique et destination

Libellé : ${v(f,'action')}

Cible : ${v(f,'target')}

État de la cible : ${v(f,'targetState')}

${safeTarget(f.target)?`[${v(f,'action').replace(/[\[\]]/g,'')}](${safeTarget(f.target)})`:'Lien à fournir. Indiquez un chemin relatif à ce plan ou une adresse HTTPS.'}

## Pièces associées

- [Preuve et revue S17](../06-PORTFOLIO/preuve-S17.md)
- [Relais S18](../06-PORTFOLIO/relais-S18.md)

Exportez ce plan dans 04-WEB/structure-page-projet.md. La mention d’une cible ne prouve pas son ouverture. Consignez l’essai réel dans la preuve.
`}
export function validationMissing(state){const f=state.fields;const need=['project','htmlRole','cssRole','jsRole','browserRole','localState','navigation','reader','testDate','observed','reopened','reason','pilot','reviewDate','review'];return need.filter(k=>!f[k]?.trim()).concat(state.checks.every(Boolean)?[]:['sept gestes à observer']);}
export function proofText(state,data){const f=state.fields;return `# Carnet d’essai et preuve S17 — Comprendre le Web

Projet : ${v(f,'project')}
Statut : ${v(f,'status')}

## Comprendre le support fourni

HTML : ${v(f,'htmlRole')}
CSS : ${v(f,'cssRole')}
JavaScript : ${v(f,'jsRole')}
Navigateur et console : ${v(f,'browserRole')}
Local ou publié : ${v(f,'localState')}

## Navigation et amélioration

Parcours, clavier, mobile : ${v(f,'navigation')}
Amélioration et nouvel essai : ${v(f,'navigationAfter')}
Question pour S18 : ${v(f,'question')}

## Support étudié

Source : ${v(f,'reference')}
Démonstration : [mini-site fourni](../04-WEB/mini-site-demonstration/index.html)
Carnet autonome : [carnet S17](../01-SUIVI/carnet-essai-S17.html)
Préparation facultative : [plan pour S18](../04-WEB/structure-page-projet.md)

## Prédiction avant essai

${v(f,'prediction')}

## Observation réelle

Binôme : ${v(f,'reader')}
Date de l’essai : ${v(f,'testDate')}

${v(f,'observed')}

## Correction ou maintien motivé

Avant : ${v(f,'before')}

Après : ${v(f,'after')}

Motif et appui : ${v(f,'reason')}

## Réouverture et nouvel essai

${v(f,'reopened')}

## Revue des sept gestes

${data.criteria.map((x,i)=>`- [${state.checks[i]?'x':' '}] ${x}`).join('\n')}

## Décision du pilote

Nom : ${v(f,'pilot')}
Date : ${v(f,'reviewDate')}
Observation et décision motivée : ${v(f,'review')}
Statut : ${v(f,'status')}
Prochaine action ou pièce manquante : ${v(f,'nextAction')}

Le quiz ne valide pas cette preuve. Les lignes non renseignées restent à compléter.
`}
export function indexText(state){return `# Entrée S17 à ajouter à mon index

Projet : ${v(state.fields,'project')}

| Séance | Production | Preuve | Statut |
| --- | --- | --- | --- |
| S17 | [Carnet d’essai](carnet-essai-S17.md) | [Preuve S17](preuve-S17.md) | ${v(state.fields,'status')} |

[Relais vers S18](relais-S18.md)

Reprenez cette entrée dans votre index existant. Gardez les productions S18, S19 et S20 comme étapes à réaliser.
`}
export function relayText(state){const f=state.fields;return `# Relais S17 vers S18

S18 : lundi 23 novembre 2026 — préparer et rédiger le contenu de votre projet.

Projet : ${v(f,'project')}
Public : ${v(f,'audience')}
Besoin : ${v(f,'need')}
Source ou support à rouvrir : ${v(f,'reference')}
Appui disponible : ${v(f,'support')}

## Reprendre les pièces

- [Plan S17](../04-WEB/structure-page-projet.md)
- [Preuve S17](preuve-S17.md)
- [Index du portfolio](index-portfolio.md)

Action choisie : ${v(f,'action')}
Cible à conserver : ${v(f,'target')}
État de la cible : ${v(f,'targetState')}
Statut de revue S17 : ${v(f,'status')}

## Point à reprendre

Question de compréhension : ${v(f,'question')}

Prochaine action : ${v(f,'nextAction')}

## Travail d’entrée S18

1. Rouvrir le carnet S17 et choisir le sujet de la future page.
2. Retrouver une source vérifiée et préparer le plan de page.
3. Rédiger un paragraphe en gardant l’appui factuel.
4. Raccourcir une phrase et motiver ce choix.
5. Conserver la même action ou justifier tout changement après essai.

Livrable attendu : 04-WEB/contenu-page-projet.md.
Preuve attendue : 06-PORTFOLIO/preuve-S18.md.

La revue de S17 conserve son statut actuel. Les productions S18 sont à construire.
`}
