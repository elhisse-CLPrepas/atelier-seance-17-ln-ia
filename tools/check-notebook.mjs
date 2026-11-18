import fs from 'node:fs/promises';
import vm from 'node:vm';
import assert from 'node:assert/strict';

// Test the actual standalone inline code without a browser or extra dependency.
const html=await fs.readFile('mon-dossier-challenge-Module05/01-SUIVI/carnet-essai-S17.html','utf8');
const code=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const elements=new Map();
const element=id=>{if(!elements.has(id))elements.set(id,{value:'',textContent:'',checked:false,click(){}});return elements.get(id)};
const checks=Array.from({length:7},(_,i)=>({dataset:{check:String(i)},checked:false}));
const storage=new Map();const downloads=[];
const context=vm.createContext({
 document:{querySelector:element,querySelectorAll:()=>checks,createElement:()=>({click(){}})},
 localStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)},
 location:{pathname:'/test-carnet'},window:{print(){}},confirm:()=>true,
 URL:{createObjectURL:blob=>{downloads.push(blob);return 'blob:test'},revokeObjectURL(){}},
 Blob,setTimeout:()=>0,console
});
vm.runInContext(code,context);
const text=()=>vm.runInContext('text()',context);
assert(text().includes('\n\nStatut : À COMPLÉTER'));
assert(!text().includes('\\n'),'Markdown must contain real newlines');
assert(text().includes('HTML : un élément observé et son rôle\n\nÀ compléter'));
element('#notebook').oninput({target:{dataset:{},name:'observed',value:'Le second clic masque la zone.'}});
assert(text().includes('Le second clic masque la zone.'));
assert.equal(storage.size,1);
vm.runInContext('state=normal(JSON.parse([...localStorage.getItem("lnia-carnet-comprendre-s17:/test-carnet")].join("")));populate()',context);
assert.equal(element('#n-observed').value,'Le second clic masque la zone.');
element('#notebook').oninput({target:{dataset:{},name:'status',value:'VALIDÉ'}});
assert.equal(vm.runInContext('state.fields.status',context),'À VALIDER');
element('#export-md').onclick();
assert((await downloads[0].text()).includes('Le second clic masque la zone.'));
await element('#restore').onchange({target:{files:[{size:20,text:async()=>'{"version":99}'}],value:'test'}});
assert(element('#save-status').textContent.includes('Import impossible'));
console.log('Carnet autonome vérifié : code exécuté, saisie, sauvegarde/reprise, export avec sauts de ligne, statut incomplet et import invalide.');
