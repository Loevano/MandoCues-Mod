// Ordinary takes may cover different bar ranges; take numbers keep increasing.
function reviewParseBars(value){
 const text=String(value??'').trim();if(!text||/^all$/i.test(text))return null;
 const m=text.match(/^(\d{1,5})(?:\s*[-–]\s*(\d{1,5}))?$/);
 if(!m||+m[1]<1||+(m[2]||m[1])<+m[1])throw new Error('Use a bar or range, for example 4 or 4–10.');
 return {from:+m[1],to:+(m[2]||m[1])};
}
function reviewBarsText(range){return !range?'All bars':range.from===range.to?'Bar '+range.from:'Bars '+range.from+'–'+range.to;}
function reviewRangeValue(range){return range?(range.from===range.to?String(range.from):range.from+'–'+range.to):'';}
function reviewSection(s){return s.reviewSections?.[s.cue]||null;}
function reviewSectionEditor(s){
 const r=reviewSection(s),busy=!!running(s);
 return `<section class="v3-feature-panel v3-section-editor" aria-label="Bar range for the next take"><header><b>Next take · ${cues[s.cue][0]}</b><small>${shortcutText('⌘⇧J')}</small></header><div class="v3-range-controls">${reviewVariant('sections')==='A'?`<label>Bars<input data-review-section-range class="v3-section-input" value="${reviewRangeValue(r)}" placeholder="All, 4, or 4–10" ${busy?'disabled':''}></label>`:`<label>From<input type="number" min="1" max="99999" data-review-section-from class="v3-section-input" value="${r?.from??''}" placeholder="All" ${busy?'disabled':''}></label><span>–</span><label>To<input type="number" min="1" max="99999" data-review-section-to value="${r?.to??''}" placeholder="Same bar" ${busy?'disabled':''}></label>`}<button data-review-section-apply ${busy?'disabled':''}>Set range</button><button data-review-section-clear ${busy?'disabled':''}>All bars</button></div><small>${busy?'Stop the take to set the next range.':reviewBarsText(r)+' · applies to the next take; existing takes stay unchanged.'}</small><p class="v3-field-error" data-review-section-error role="status"></p></section>`;
}
function reviewCommitSection(clear=false){
 const s=state();if(running(s))return;
 const root=document.querySelector('.v3-section-editor');if(!root)return;
 try{
  const one=root.querySelector('[data-review-section-range]'),from=root.querySelector('[data-review-section-from]')?.value||'',to=root.querySelector('[data-review-section-to]')?.value||'';
  if(!one&&!from&&to&&!clear)throw new Error('Choose a starting bar first.');
  const range=clear?null:reviewParseBars(one?one.value:from+(to?'–'+to:''));
  s.reviewSections??={};s.reviewSections[s.cue]=range;renderDemo();
 }catch(error){root.querySelector('[data-review-section-error]').textContent=error.message;}
}
const reviewSectionToggle=toggleRecord;
toggleRecord=function(s,kind='take'){
 const before=running(s);reviewSectionToggle(s,kind);
 const live=running(s);if(!before&&live){live.barRange=structuredClone(reviewSection(s));renderDemo();}
};
const reviewSectionTakeList=reviewActiveTakes;
reviewActiveTakes=function(s){
 if(sessionReview.feature!=='sections'||reviewVariant('sections')!=='B')return reviewSectionTakeList(s);
 const groups=new Map();for(const take of s.takes[s.cue]){const label=reviewBarsText(take.barRange);if(!groups.has(label))groups.set(label,[]);groups.get(label).push(take);}
 return `<section class="v3-active-takes" aria-label="Takes grouped by bar range"><header><b>${cues[s.cue][0]} · Takes by range</b><small>Same take numbering</small></header>${[...groups].map(([label,takes])=>`<div class="v3-take-range-group"><small>${label}</small><div class="v3-active-take-buttons">${takes.map(t=>`<button data-select-take="${t.id}" aria-pressed="${s.selected===t.id}"><b>${entryLabel(t)}</b><small>${t.rolling?'● Recording':time(t.duration)}</small></button>`).join('')}</div></div>`).join('')||'<p>No takes yet.</p>'}</section>`;
};
reviewUpdates.push(()=>{
 if(sessionReview.feature==='sections'&&proposalView==='recording')document.querySelector('#main-panel .original-cue-facts')?.insertAdjacentHTML('afterend',reviewSectionEditor(state()));
 for(const owner of document.querySelectorAll('[data-calm-take],.score-take-row')){
  const id=owner.dataset.calmTake||owner.querySelector('[data-select-take]')?.dataset.selectTake,t=takeById(state(),id);
  if(t?.barRange)(owner.querySelector('.calm-take-identity')||owner).insertAdjacentHTML('beforeend',`<small class="v3-take-range-badge">${reviewBarsText(t.barRange)}</small>`);
 }
});
document.addEventListener('click',e=>{if(e.target.closest('[data-review-section-apply]'))reviewCommitSection();if(e.target.closest('[data-review-section-clear]'))reviewCommitSection(true);});
document.addEventListener('keydown',e=>{
 if(e.isComposing||e.repeat)return;
 if(e.metaKey&&e.shiftKey&&!e.altKey&&!e.ctrlKey&&e.code==='KeyJ'&&!document.querySelector('dialog[open]')){
  e.preventDefault();e.stopImmediatePropagation();if(running(state())){toast('Stop the take before changing its range.');return;}
  if(typeof reviewGo==='function')reviewGo('sections');document.querySelector('.v3-section-input')?.focus();document.querySelector('.v3-section-input')?.select();
 }
 if(e.key==='Enter'&&e.target.closest('.v3-section-editor')){e.preventDefault();e.stopImmediatePropagation();reviewCommitSection();}
},true);

// Preserve new metadata in the existing downloadable take-log snapshot.
const reviewBaseTakeLog=sessionTakeLog;
sessionTakeLog=function(s=unifiedState){const output=reviewBaseTakeLog(s);for(const row of output.takes){const take=takeById(s,row.takeId);row.barRange=structuredClone(take?.barRange||null);for(const note of row.notes){note.barEnd=take?.notes.find(n=>n.id===note.id)?.measureEnd||note.bar||null;}}return output;};
