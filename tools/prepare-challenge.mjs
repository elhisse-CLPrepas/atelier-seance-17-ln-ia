import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {renderCarnet} from '../src/carnet.js';
import {blankState,proofText} from '../src/exports.js';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const dossier=path.join(root,'mon-dossier-challenge-Module05');
await fs.access(path.join(dossier,'index.html')).catch(()=>{throw new Error('Clonez d’abord le dépôt commun dans mon-dossier-challenge-Module05. Voir docs/VERSIONNEMENT-LOCAL.md.');});
const data=JSON.parse(await fs.readFile(path.join(root,'src/seance.json'),'utf8'));
const blank=blankState();
const files={
 '01-SUIVI/carnet-essai-S17.html':renderCarnet(data),
 '06-PORTFOLIO/carnet-essai-S17.md':proofText(blank,data),
 '06-PORTFOLIO/preuve-S17.md':proofText(blank,data),
 '02-PROMPTS/prompts-S17.md':'# Prompts de compréhension S17\n\n'+data.prompts.map(p=>`## ${p.title}\n\n${p.text}\n`).join('\n'),
 '06-PORTFOLIO/grille-revue-S17.md':'# Revue S17\n\n'+data.criteria.map(c=>'- [ ] '+c).join('\n')+'\n\nPilote :\nDate :\nObservation :\nStatut : À COMPLÉTER\n'
};
for(const [name,content]of Object.entries(files)){
 const target=path.join(dossier,name);await fs.mkdir(path.dirname(target),{recursive:true});
 try{await fs.writeFile(target,content,{flag:'wx'});console.log('Créé : '+name);}
 catch(error){if(error.code!=='EEXIST')throw error;console.log('Conservé : '+name);}
}
