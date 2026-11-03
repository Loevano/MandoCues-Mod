// A range belongs to a take; it never restarts numbering or implies an overdub.
function v4Ranges(s){s.v4Ranges??={};return s.v4Ranges[s.cue]??={presets:[],pending:null};}
function v4RangeLabel(range){return range?'Bars '+range.from+'–'+range.to:'Whole cue';}
function v4RangeControls(s){
 const ranges=v4Ranges(s),pending=ranges.pending,t=running(s),settings=v4State(s).settings;
 return `<section class="v4-take-range" aria-label="Bar range for the next take"><div class="v4-range-line"><span>${t?'Recording range':'Next take'}</span><button data-v4-range-all aria-pressed="${!pending}" ${t?'disabled':''}>Whole cue</button>${ranges.presets.map((range,i)=>`<button data-v4-range-preset="${i}" aria-pressed="${pending?.from===range.from&&pending?.to===range.to}" ${t?'disabled':''}>${v4RangeLabel(range)}</button>`).join('')}<button data-v4-range-add aria-expanded="${!!ranges.editing}" ${t?'disabled':''}>+ Range</button></div>${ranges.editing?`<form id="v4-next-range"><label>From bar<input name="from" type="number" inputmode="numeric" min="1" max="99999" value="${pending?.from??1}" required></label><label>Till bar<input name="to" type="number" inputmode="numeric" min="1" max="99999" value="${pending?.to??8}" required></label>${settings.ranges==='multiple'?'<small>Save a range, then add another preset for the next pass.</small>':''}<button type="submit">Use range</button><button type="button" data-v4-range-cancel>Cancel</button><p class="v4-range-error" role="status"></p></form>`:''}</section>`;
}
const v4RangeBaseRender=renderDemo;
renderDemo=function(){
 v4RangeBaseRender();const s=state();
 const slot=document.querySelector('.v4-range-slot');if(slot)slot.innerHTML=v4RangeControls(s);
 document.querySelectorAll('[data-calm-take]').forEach(row=>{
  const t=takeById(s,row.dataset.calmTake);if(!t)return;
  const name=row.querySelector('.calm-take-name');
  name?.insertAdjacentHTML('beforeend',`<span class="v4-take-range-label">${v4RangeLabel(t.barRange)}</span>`);
  const identity=row.querySelector('.calm-take-identity');
  identity?.insertAdjacentHTML('beforeend',`<button class="v4-edit-take-range" data-v4-edit-take-range="${t.id}" title="Edit bars for ${entryLabel(t)}" aria-label="Edit bars for ${entryLabel(t)}">Bars</button>`);
 });
};
const v4RangeBaseToggle=toggleRecord;
toggleRecord=function(s,kind='take'){
 const before=running(s),range=structuredClone(v4Ranges(s).pending);
 v4RangeBaseToggle(s,kind);
 const live=running(s);if(!before&&live){live.barRange=range;renderDemo();}
};
document.addEventListener('click',event=>{
 const s=state(),ranges=v4Ranges(s),b=event.target.closest('[data-v4-range-add],[data-v4-range-cancel],[data-v4-range-all],[data-v4-range-preset],[data-v4-edit-take-range]');if(!b||b.disabled)return;
 if(b.hasAttribute('data-v4-edit-take-range')){
  const t=takeById(s,b.dataset.v4EditTakeRange);if(!t)return;
  appDialog(entryLabel(t)+' · Bars',`<form id="v4-existing-range"><input type="hidden" name="take" value="${t.id}"><label>From bar<input name="from" type="number" min="1" max="99999" value="${t.barRange?.from??''}" placeholder="Whole cue"></label><label>Till bar<input name="to" type="number" min="1" max="99999" value="${t.barRange?.to??''}" placeholder="Whole cue"></label><p class="review-muted">Leave both empty for the whole cue.</p><p class="v4-range-error" role="status"></p></form>`,`<button type="submit" form="v4-existing-range">Save</button>`);return;
 }
 if(running(s))return;
 if(b.hasAttribute('data-v4-range-add'))ranges.editing=!ranges.editing;
 if(b.hasAttribute('data-v4-range-cancel'))ranges.editing=false;
 if(b.hasAttribute('data-v4-range-all')){ranges.pending=null;ranges.editing=false;}
 if(b.hasAttribute('data-v4-range-preset')){ranges.pending=structuredClone(ranges.presets[+b.dataset.v4RangePreset]);ranges.editing=false;}
 renderDemo();if(ranges.editing)document.querySelector('#v4-next-range [name=from]')?.focus({preventScroll:true});
});
document.addEventListener('submit',event=>{
 const form=event.target;if(!['v4-next-range','v4-existing-range'].includes(form.id))return;event.preventDefault();
 const values=new FormData(form),f=String(values.get('from')??''),t=String(values.get('to')??''),whole=!f&&!t;
 const from=Number(f),to=Number(t);
 if(!whole&&(!Number.isInteger(from)||!Number.isInteger(to)||from<1||to<from||to>99999)||form.id==='v4-next-range'&&whole){form.querySelector('.v4-range-error').textContent='Choose a start bar and an end bar at or after it.';return;}
 const s=state(),range=whole?null:{from,to};
 if(form.id==='v4-existing-range'){
  const take=takeById(s,values.get('take'));if(take)take.barRange=range;form.closest('dialog').close();
 }else{
  const ranges=v4Ranges(s);ranges.pending=range;ranges.editing=false;
  if(!ranges.presets.some(r=>r.from===from&&r.to===to))ranges.presets.push(range);
 }
 renderDemo();
});
// B focuses the range controls only when outside text fields and dialogs.
document.addEventListener('keydown',event=>{
 if(event.code!=='KeyB'||event.metaKey||event.ctrlKey||event.altKey||event.shiftKey||event.repeat||event.isComposing||!navigationKeysAvailable(event)||running(state()))return;
 event.preventDefault();event.stopImmediatePropagation();
 if(proposalView==='recording'){v4Ranges(state()).editing=true;renderDemo();document.querySelector('#v4-next-range [name=from]')?.focus();}
 else if(state().selected)document.querySelector(`[data-v4-edit-take-range="${state().selected}"]`)?.click();
},true);
renderDemo();
const v4RangeBaseLog=sessionTakeLog,v4RangeBaseExport=openSessionExport;
sessionTakeLog=function(s=unifiedState){const log=v4RangeBaseLog(s);for(const take of log.takes)take.barRange=structuredClone(takeById(s,take.takeId)?.barRange??null);return log;};
openSessionExport=function(kind){
 v4RangeBaseExport(kind);
 if(kind==='takes')document.querySelectorAll('.session-export-preview section').forEach((section,index)=>{const t=allTakes(state())[index];if(t)section.querySelector('b')?.insertAdjacentHTML('afterend',' · '+v4RangeLabel(t.barRange));});
};
