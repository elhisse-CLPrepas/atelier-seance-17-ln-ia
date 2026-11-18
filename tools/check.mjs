import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {sections,resources} from '../src/content.js';
import {blankState,normalizeState,safeTarget,planText,proofText,validationMissing} from '../src/exports.js';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const data=JSON.parse(await fs.readFile(path.join(root,'src/seance.json'),'utf8'));
assert.equal(sections.length,11);assert.equal(data.slides.length,22);assert.equal(data.cards.length,12);assert.equal(data.quiz.length,8);assert.equal(data.criteria.length,7);assert.equal(data.cases,undefined);
for(const [q,choices,correct,explanations]of data.quiz){assert(q);assert.equal(choices.length,3);assert.equal(explanations.length,3);assert(correct>=0&&correct<3)}
for(const r of resources.filter(x=>x.path))assert((await fs.stat(path.join(root,'public',r.path))).size>10,r.path);
assert((await fs.stat(path.join(root,'public/dossier-challenge/01-SUIVI/carnet-essai-S17.html'))).size>100);
const html=await fs.readFile(path.join(root,'index.html'),'utf8');
for(const [id]of sections)assert(html.includes(`id="${id}"`),id);
const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);assert.equal(new Set(ids).size,ids.length,'IDs uniques');
assert(html.includes('application/ld+json'));assert(html.includes('og:description'));assert(html.includes('lang="fr"'));
for(const bad of ['javascript:alert(1)','data:text/html,test','//example.org','https://bad.test/(a)','/etc/passwd'])assert.equal(safeTarget(bad),'',bad);
assert.equal(safeTarget('mini-site-demonstration/index.html#interaction'),'mini-site-demonstration/index.html#interaction');
const state=blankState();assert(validationMissing(state).length>0);assert(planText(state).includes('À compléter'));assert(proofText(state,data).includes('À COMPLÉTER'));
state.fields.status='VALIDÉ';assert.equal(normalizeState(state).fields.status,'À VALIDER');
assert.throws(()=>normalizeState({version:1}));
const build=await fs.readFile(path.join(root,'dist/index.html'),'utf8');assert(build.includes('titre-accueil'));
for(const file of ['OUVRIR-SEANCE-17.html','PROJECTION-SEANCE-17.html']){const h=await fs.readFile(path.join(root,file),'utf8');assert(!h.includes('<script type="module"'));assert(h.includes('data-resource-base="./dist/"'));assert(h.includes('./dist/assets/logo-LN-IA.png'))}
console.log('Vérifié : 11 rubriques, 22 vues, support fourni, carnet, 12 cartes, 8 questions, 24 corrections, 7 repères et entrées hors ligne.');
