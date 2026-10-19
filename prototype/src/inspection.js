// Helpers derived from visible structure only. The pasted page is never executed.
function entryLabel(t) { return (t.kind==='overdub'?'Overdub ':'Take ')+t.num; }
function nextEntryNumber(s,cue,kind='take') {
  return Math.max(0,s.takeSerials?.[cue]?.[kind]||0,...s.takes[cue].filter(t=>(t.kind||'take')===kind).map(t=>t.num))+1;
}
function entryCountText(s,cue,fallback=0) {
  if(!s.takes)return fallback+' takes';
  const takes=s.takes[cue].filter(t=>t.kind!=='overdub').length;
  const overdubs=s.takes[cue].filter(t=>t.kind==='overdub').length;
  return takes+' '+(takes===1?'take':'takes')+(overdubs?' · '+overdubs+' '+(overdubs===1?'overdub':'overdubs'):'');
}
let cuePlanningState=null;
const inspectedCuePlan=[10,25,20,12,14,8,12,8,10,12,13,25,10,16,4,12,12,12,8,8,6,60.5,8,5,4,25.5];
function cueAutoMinutes(s,j){
 // Local estimate from the visible tooltip, not a reconstruction of the production scheduler.
 const prep=s?.prepMinutes??3,weight=k=>{const [m,sec]=cues[k][2].split(':').map(Number);return (m+sec/60)*({Low:.7,Medium:1,High:1.5}[s?.cueSettings?.[k]?.complexity]??1);};
 const total=cues.reduce((sum,_,k)=>sum+weight(k),0),available=Math.max(0,(s?.booked??360)-prep*cues.length);
 return Math.max(.5,Math.round((prep+available*weight(j)/(total||1))*2)/2);
}
function cuePlannedMinutes(j) {
 const setting=cuePlanningState?.cueSettings?.[j];
 return setting?.planned===null?cueAutoMinutes(cuePlanningState,j):setting?.planned??inspectedCuePlan[j]??cueAutoMinutes(cuePlanningState,j);
}
function sourceCueFacts(c,j) {
  const planned=cuePlannedMinutes(j);
  return `<span class="cue-source-facts"><span><small>Music</small><b>${c[2]}</b></span><span title="Demo schedule"><small>Planned</small><b>${time(planned*60)}</b></span></span>`;
}
function sourceSessionSummary(s=null) {
  return `<div class="source-session-summary" aria-label="Demo session settings"><span>Session length <b>${s?.booked!==undefined?Math.floor(s.booked/60)+'h '+String(s.booked%60).padStart(2,'0'):'6h 00'}</b></span><span>Preparation <b>${s?.prepMinutes??3} min/cue</b></span><span>Max. music length <b>${s?.maxMusicMinutes??60} min</b></span></div>`;
}
function sourceCuePlan(s) {
  return `<section class="source-cue-plan" aria-label="Session plan with complete cue codes"><div><b>Session plan</b><small>Demo · click to choose a cue</small></div><nav aria-label="Cue order">${cues.map((c,j)=>`<button data-session-cue="${j}" aria-label="Choose ${c[0]} ${esc(c[1])}" aria-current="${s.cue===j?'true':'false'}" title="${esc(c[1])}">${c[0]}</button>`).join('')}</nav></section>`;
}

function takeLabelInput(t){return `<input class="take-label-input" data-take-label="${t.id}" value="${esc(t.label||'')}" maxlength="80" placeholder="Take label" aria-label="Label for ${entryLabel(t)}">`;}
document.addEventListener('input',event=>{if(!event.target.dataset.takeLabel||!active)return;const t=takeById(state(),event.target.dataset.takeLabel);if(t)t.label=event.target.value.slice(0,80);});
document.addEventListener('change',event=>{if(event.target.dataset.takeLabel&&active)renderDemo();});

function takeDeleteButton(t){return `<button type="button" class="take-delete" data-delete-take="${t.id}" aria-label="Delete ${entryLabel(t)}" title="${t.rolling?'Stop this take before deleting it':'Delete '+entryLabel(t)}" ${t.rolling?'disabled':''}><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 4h10M6 4V2h4v2M4 4l1 10h6l1-10M7 6v6M9 6v6"/></svg></button>`;}
function deleteProposalTake(s,id){
 const t=takeById(s,id);if(!t||t.rolling)return;
 const list=s.takes[t.cue],index=list.indexOf(t),kind=t.kind||'take';
 s.takeSerials??={};s.takeSerials[t.cue]??={};s.takeSerials[t.cue][kind]=nextEntryNumber(s,t.cue,kind)-1;
 list.splice(index,1);
 if(s.scoreCompared?.[t.cue])s.scoreCompared[t.cue]=s.scoreCompared[t.cue].filter(key=>key!==id);
 if(s.selected===id){s.selected=s.scoreCompared?.[t.cue]?.at(-1)||list[index]?.id||list.at(-1)?.id||null;if(s.selected){s.scoreCompared??={};if(!s.scoreCompared[t.cue]?.length)s.scoreCompared[t.cue]=[s.selected];restoreScoreView(s);}else{s.scoreComment=null;s.focusedScoreNote=null;}}
 if(s.scoreRangeAnchor?.[t.cue]===id)s.scoreRangeAnchor[t.cue]=s.selected;
 if(s.scoreSelectedTakes?.[t.cue]===id)delete s.scoreSelectedTakes[t.cue];
 if(s.scoreComment?.take===id)s.scoreComment=null;
 document.querySelector('.app-dialog')?.close();renderDemo();toast(entryLabel(t)+' deleted.');
}
document.addEventListener('click',event=>{
 const confirm=event.target.closest('[data-confirm-delete-take]');if(confirm){deleteProposalTake(state(),confirm.dataset.confirmDeleteTake);return;}
 const button=event.target.closest('[data-delete-take]');if(!button||button.disabled||!active)return;
 const t=takeById(state(),button.dataset.deleteTake);if(!t||t.rolling)return;
 appDialog('Delete '+entryLabel(t)+'?',`<p>This deletes ${esc(entryLabel(t))} from ${esc(cues[t.cue][0])}, including its notes and bar selections.</p>`,'<button data-app-dialog-close>Cancel</button><button class="take-delete-confirm" data-confirm-delete-take="'+t.id+'">Delete take</button>');
});
