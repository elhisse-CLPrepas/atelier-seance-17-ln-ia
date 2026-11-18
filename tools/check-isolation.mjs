import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const common=path.join(root,'mon-dossier-challenge-Module05');
async function hashes(dir,base=dir){
 const result={};
 for(const entry of await fs.readdir(dir,{withFileTypes:true})){
  if(['.git','node_modules','__pycache__'].includes(entry.name))continue;
  const target=path.join(dir,entry.name);
  if(entry.isDirectory())Object.assign(result,await hashes(target,base));
  else result[path.relative(base,target)]=createHash('sha256').update(await fs.readFile(target)).digest('hex');
 }
 return result;
}
const git=(cwd,...args)=>execFileSync('git',args,{cwd,encoding:'utf8'}).trim();
assert.equal(path.resolve(git(root,'rev-parse','--show-toplevel')).toLowerCase(),root.toLowerCase());
assert.equal(path.resolve(git(common,'rev-parse','--show-toplevel')).toLowerCase(),common.toLowerCase());
assert.equal(git(root,'remote','get-url','origin'),'https://github.com/elhisse-CLPrepas/atelier-seance-17-ln-ia.git');
assert.equal(git(common,'remote','get-url','origin'),'https://github.com/elhisse-CLPrepas/mon-dossier-challenge-Module05.git');
assert(git(root,'check-ignore','mon-dossier-challenge-Module05/index.html'));
assert.equal(git(root,'ls-files','mon-dossier-challenge-Module05'),'');
const before=await hashes(common);
execFileSync(process.execPath,['tools/generate.mjs'],{cwd:root,stdio:'pipe'});
execFileSync(process.execPath,['tools/prepare-challenge.mjs'],{cwd:root,stdio:'pipe'});
assert.deepEqual(await hashes(common),before,'Existing shared productions must survive generation and preparation unchanged');
for(const relative of ['public/dossier-challenge','public/supports/kit-candidat']){
 async function noGit(dir){for(const entry of await fs.readdir(dir,{withFileTypes:true})){assert.notEqual(entry.name,'.git');if(entry.isDirectory())await noGit(path.join(dir,entry.name));}}
 await noGit(path.join(root,relative));
}
console.log('Isolation vérifiée : deux racines Git, remotes distincts, source commune ignorée par S17, génération sans modification des productions, aucune métadonnée Git dans les copies.');
