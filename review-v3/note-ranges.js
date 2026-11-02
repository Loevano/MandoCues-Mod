// Note ranges are metadata, never a prefix inside the user's comment text.
const reviewOriginalMeasure=noteMeasure,reviewOriginalAdd=addNote,reviewOriginalSetMeasure=setNoteMeasure;
let reviewNoteTarget=null;
noteMeasure=function(s,t,n,score,place){
 const result=reviewOriginalMeasure(s,t,n,score,place);
 const end=n.measureEnd;
 return result.replace(`<b>${n.measureScope==='all'?'All':n.measure||'+'}</b>`,`<b>${n.measureScope==='all'?'All':n.measure?(end&&end!==n.measure?n.measure+'–'+end:n.measure):'+'}</b>`)+`<button type="button" class="v3-note-range-button" data-review-note-range="${n.id}" data-take="${t.id}" aria-label="Choose a bar range for this note" title="Bar range · ⌘J">↔</button>`;
};
setNoteMeasure=function(take,id,value,place){const n=metadataNote(takeById(state(),take),id);if(n&&(String(value).toLowerCase()==='all'||value===''||(Number.isInteger(+value)&&+value>=1&&+value<=99999)))delete n.measureEnd;return reviewOriginalSetMeasure(take,id,value,place);};
addNote=function(id,place){
 const t=takeById(state(),id);if(!t||!t.draft.text.trim())return;
 const end=t.draft.measureEnd,count=t.notes.length;
 reviewOriginalAdd(id,place);
 if(t.notes.length>count){if(end)t.notes.at(-1).measureEnd=end;t.draft.measureEnd=end;renderDemo();const field=document.querySelector(`.calm-notes [data-draft="${id}"]`);field?.focus({preventScroll:true});}
};
function reviewNoteFields(n,inline=false){
 return `<div class="v3-range-controls">${inline?`<label>From<input type="number" min="1" max="99999" data-review-note-from value="${n.measure??''}" placeholder="All"></label><span>–</span><label>To<input type="number" min="1" max="99999" data-review-note-to value="${n.measureEnd??n.measure??''}" placeholder="Same bar"></label>`:`<label>Bar or range<input type="text" data-review-note-value value="${n.measure?reviewRangeValue({from:n.measure,to:n.measureEnd||n.measure}):''}" placeholder="All, 13, or 13–20"></label>`}<button type="button" data-review-note-apply>Set label</button></div>`;
}
function reviewOpenNoteRange(take,id='draft'){
 const t=takeById(state(),take),n=metadataNote(t,id);if(!n)return;
 reviewNoteTarget={take,id};
 const field=document.activeElement;
 if(field?.matches('[data-draft]'))reviewNoteTarget.selection=[field.selectionStart,field.selectionEnd];
 document.querySelector('.v3-note-range-popover')?.remove();
 if(sessionReview.feature==='notes'&&reviewVariant('notes')==='B'&&id==='draft'){
  document.querySelector('[data-review-note-from]')?.focus();document.querySelector('[data-review-note-from]')?.select();return;
 }
 const panel=document.createElement('section');panel.className='v3-note-range-popover';panel.lang='en';panel.setAttribute('role','dialog');panel.setAttribute('aria-label','Set note bar range');
 panel.innerHTML=`<header><b>${entryLabel(t)} · Note label</b><button data-review-note-close aria-label="Close bar range">×</button></header>${reviewNoteFields(n)}<p class="v3-field-error" role="status"></p>`;
 document.body.append(panel);const anchor=document.querySelector(`.calm-notes [data-composer="${take}"]`)||document.querySelector('.v3-notes-column');const r=anchor?.getBoundingClientRect();
 Object.assign(panel.style,{left:Math.max(8,Math.min(innerWidth-330,(r?.left??innerWidth-350)))+'px',top:Math.max(8,Math.min(innerHeight-panel.offsetHeight-8,(r?.bottom??250)))+'px'});
 panel.querySelector('input').focus();panel.querySelector('input').select();
}
function reviewApplyNoteRange(root){
 const target=reviewNoteTarget||{take:state().selected,id:'draft'},t=takeById(state(),target.take),n=metadataNote(t,target.id);if(!n)return;
 try{
  const value=root.querySelector('[data-review-note-value]'),from=root.querySelector('[data-review-note-from]')?.value||'',to=root.querySelector('[data-review-note-to]')?.value||'';
  if(!value&&!from&&to)throw new Error('Choose a starting bar first.');
  const range=reviewParseBars(value?value.value:from+(to?'–'+to:''));
  if(n.id!=='draft')rememberScoreChange(state(),t);
  n.measure=range?.from??(n.id==='draft'?'':null);n.measureEnd=range?.to??null;n.measureScope=range?'bar':'all';n.useMeasure=true;n.measureAuto=false;n.source??=state().doc.id;syncSavedScorePage(n);
  document.querySelector('.v3-note-range-popover')?.remove();reviewNoteTarget=null;renderDemo();
  const field=document.querySelector(`.calm-notes [data-draft="${t.id}"]`);field?.focus({preventScroll:true});
  if(target.selection&&field?.setSelectionRange)field.setSelectionRange(...target.selection);
 }catch(error){(root.querySelector('.v3-field-error')||root.appendChild(document.createElement('p'))).textContent=error.message;}
}
reviewUpdates.push(()=>{
 if(sessionReview.feature!=='notes'||reviewVariant('notes')!=='B'||proposalView!=='recording')return;
 const t=takeById(state(),state().selected);if(!t)return;
 reviewNoteTarget=null;
 document.querySelector('.calm-notes .note-composer .composer-footer')?.insertAdjacentHTML('afterend',`<section class="v3-inline-note-range" aria-label="Bar range for this note">${reviewNoteFields(t.draft,true)}<p class="v3-field-error" role="status"></p></section>`);
});
document.addEventListener('click',e=>{
 const button=e.target.closest('[data-review-note-range]');if(button){reviewOpenNoteRange(button.dataset.take,button.dataset.reviewNoteRange);return;}
 if(e.target.closest('[data-review-note-close]')){document.querySelector('.v3-note-range-popover')?.remove();reviewNoteTarget=null;document.querySelector('.calm-notes [data-draft]')?.focus({preventScroll:true});return;}
 if(e.target.closest('[data-review-note-apply]'))reviewApplyNoteRange(e.target.closest('.v3-note-range-popover,.v3-inline-note-range'));
});
document.addEventListener('keydown',e=>{
 if(e.isComposing||e.repeat)return;
 if(e.metaKey&&!e.shiftKey&&!e.altKey&&!e.ctrlKey&&e.code==='KeyJ'&&!document.querySelector('dialog[open]')){
  const field=e.target.closest('[data-draft]');if(!field)return;
  e.preventDefault();e.stopImmediatePropagation();reviewOpenNoteRange(field.dataset.draft);return;
 }
 const root=e.target.closest('.v3-note-range-popover,.v3-inline-note-range');if(!root)return;
 if(e.key==='Enter'){e.preventDefault();e.stopImmediatePropagation();reviewApplyNoteRange(root);}
 if(e.key==='Escape'){e.preventDefault();e.stopImmediatePropagation();document.querySelector('.v3-note-range-popover')?.remove();reviewNoteTarget=null;document.querySelector('.calm-notes [data-draft]')?.focus({preventScroll:true});}
},true);
