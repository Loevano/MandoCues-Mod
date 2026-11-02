// Local review layer. It leaves the v2 source, tour and hosting checkout unchanged.
const sessionReview={layout:'A',space:true,history:false,moreTiming:false,setupOpen:false,scrolls:{A:0,B:0},decision:null};
const reviewBaseControls=controls,reviewBaseRender=renderDemo,reviewRecordButton=recordButton;
const reviewBaseSessionHeader=proposalSessionHeader;
document.querySelector('#proposal-welcome')?.close();
document.title='MandoCues · v3 review';document.body.classList.add('v3-review');
closeProposalTour();
const reviewToolbar=document.createElement('header');reviewToolbar.className='v3-review-toolbar';reviewToolbar.lang='nl';
reviewToolbar.innerHTML=`<div class="v3-review-name"><b>v3 · Werkplek voor de actieve cue</b><small>Reviewproef · v2 is bewaard</small></div><nav aria-label="Vergelijk de indeling"><button data-review-layout="A" aria-pressed="true">A · Huidige indeling</button><button data-review-layout="B" aria-pressed="false">B · Notes bij de bediening</button></nav><label><input type="checkbox" data-review-space checked> Spatie proberen</label><button data-review-decision>Mijn voorkeur</button><a href="PLAN.md" target="_blank">Plan ↗</a>`;
document.body.prepend(reviewToolbar);
// The old tour explains v2. Keep it out of this unapproved layout experiment.
document.querySelectorAll('.proposal-review-actions [data-proposal-action="tour"],.proposal-review-actions [data-proposal-action="prompt"]').forEach(b=>b.hidden=true);
recordButton=function(s){return sessionReview.space?reviewRecordButton(s).replace('<kbd>⌘ Enter</kbd>','<kbd>Space</kbd>'):reviewRecordButton(s);};
proposalSessionHeader=function(s){
 const markup=reviewBaseSessionHeader(s);
 if(sessionReview.layout==='A')return markup;
 return `<details class="v3-session-setup" ${sessionReview.setupOpen?'open':''}><summary>Session setup <span>${esc(proposalSessionMeta(s).label)}</span></summary>${markup}</details>`;
};
function reviewActiveTakes(s){return `<section class="v3-active-takes" aria-label="Takes in the active cue"><header><b>${cues[s.cue][0]} · Takes</b><small>${entryCountText(s,s.cue)}</small></header><div class="v3-active-take-buttons">${s.takes[s.cue].map(t=>`<button type="button" data-select-take="${t.id}" aria-pressed="${s.selected===t.id}"><b>${entryLabel(t)}</b><small>${t.rolling?'● Recording':time(t.duration)}</small></button>`).join('')||'<p>No takes yet. Start a take to write notes.</p>'}</div></section>`;}
function reviewCueHistory(s){
 const rows=s.takes[s.cue].flatMap(t=>t.notes.map(n=>({t,n})));
 return `<section class="v3-cue-history"><header><button type="button" data-review-history aria-expanded="${sessionReview.history}">${sessionReview.history?'⌄':'›'} Earlier notes in this cue <span>${rows.length}</span></button></header>${sessionReview.history?`<div class="v3-history-list">${rows.map(({t,n})=>`<article><button type="button" data-select-take="${t.id}" aria-label="Read notes for ${entryLabel(t)}">${entryLabel(t)}</button><span>${n.measureScope==='all'?'All bars':n.measure?'Bar '+n.measure:'No bar'}</span><p>${esc(n.text)}</p></article>`).join('')||'<p>No saved notes in this cue yet.</p>'}</div>`:''}</section>`;
}
controls=function(){
 if(sessionReview.layout==='A')return reviewBaseControls();
 const s=state();return `<div class="calm-scroll control-scroll"><div class="sticky-slot" aria-hidden="true">${transport(s)}</div><div class="v3-cue-workspace"><div class="v3-control-column">${calmPanel(s).replace(/(<div class="main-session-times"[^>]*>.*?<\/div>)/s,markup=>'<details class="v3-more-timing" '+(sessionReview.moreTiming?'open':'')+'><summary>More timing</summary>'+markup+'</details>')}</div><div class="v3-notes-column">${reviewActiveTakes(s)}${calmNotes(s)}${reviewCueHistory(s)}</div></div>${cueTimeline(s)}<section class="v3-all-cues" aria-label="All session cues"><header><h2>Session cues</h2><div><button type="button" data-review-workspace>Back to notes ↑</button> <button type="button" data-review-current>Current cue <b>${cues[s.cue][0]}</b></button></div></header>${proposalRatingFilter(s)}${calmCueList(s)}</section></div>`;
};
renderDemo=function(){
 document.body.classList.toggle('v3-layout-b',sessionReview.layout==='B');
 reviewBaseRender();
 for(const b of document.querySelectorAll('[data-review-layout]'))b.setAttribute('aria-pressed',String(b.dataset.reviewLayout===sessionReview.layout));
 document.querySelector('.v3-review-caption')?.remove();
 const caption=document.createElement('p');caption.className='v3-review-caption';caption.lang='nl';
 caption.textContent=sessionReview.layout==='A'?'A behoudt de huidige opzet. B zet de actieve takes en notes direct naast de bediening.':'B zet actieve takes en notes direct naast de bediening. Alle cues blijven eronder; Current cue springt er bewust naartoe.';
 document.querySelector('.proposal-session-header-slot').after(caption);
 document.querySelectorAll('.v3-history-list article p').forEach(el=>el.lang='en');
 syncGlobalRecording();
};
function reviewSpaceAction(){
 // First press starts only the session; subsequent presses start/stop takes.
 performRecordingAction(state());
}
document.addEventListener('keydown',event=>{
 if(!sessionReview.space||event.code!=='Space'||event.altKey||event.metaKey||event.ctrlKey||event.shiftKey)return;
 if(event.isComposing)return;
 const target=event.target;
 if(target.closest('input,textarea,select,[contenteditable]:not([contenteditable="false"]),[role="textbox"],dialog,.v3-review-toolbar,.proposal-review-actions,.score-inline-editor')||document.querySelector('dialog[open]')||state().scoreComment)return;
 event.preventDefault();event.stopImmediatePropagation();if(!event.repeat)reviewSpaceAction();
},true);
document.addEventListener('change',event=>{
 if(!event.target.matches('[data-review-space]'))return;
 sessionReview.space=event.target.checked;renderDemo();
});
document.addEventListener('click',event=>{
 const record=event.target.closest('[data-action="record"]');if(record&&sessionReview.space&&!state().sessionStarted&&!document.querySelector('dialog[open]')){event.preventDefault();event.stopImmediatePropagation();reviewSpaceAction();}
},true);
document.addEventListener('click',event=>{
 const layout=event.target.closest('[data-review-layout]');
 if(layout){
  if(layout.dataset.reviewLayout===sessionReview.layout)return;
  closeProposalTour();const scroll=document.querySelector('#cue-scroll');if(scroll)sessionReview.scrolls[sessionReview.layout]=scroll.scrollTop;
  sessionReview.layout=layout.dataset.reviewLayout;renderDemo();
  const next=document.querySelector('#cue-scroll');if(next)next.scrollTop=sessionReview.scrolls[sessionReview.layout];
  syncSticky();return;
 }
 if(event.target.closest('[data-review-workspace]')){document.querySelector('.v3-cue-workspace')?.scrollIntoView({block:'start',behavior:'smooth'});return;}
 if(event.target.closest('[data-review-current]')){
  const target=document.querySelector('.v3-all-cues .cue-group.current')||document.querySelector('.calm-cue-list .cue-group.current');
  target?.scrollIntoView({block:'center',behavior:'smooth'});return;
 }
 if(event.target.closest('[data-review-history]')){sessionReview.history=!sessionReview.history;renderDemo();return;}
 if(event.target.closest('[data-review-decision]')){
  reviewDialog('v3-layout-decision','Welke indeling voelt prettiger?',`<p>Deze keuze bewaart alleen je voorkeur voor de review.</p><p class="review-muted">Spatieproef: de eerste spatie start alleen de sessie; daarna start/stop je takes. In een tekstveld blijft spatie gewone tekst.</p><footer><button data-review-prefer="A">A behouden</button><button data-review-prefer="B">B verder uitwerken</button><button data-review-prefer="adjust">Nog aanpassen</button></footer>`);return;
 }
 const prefer=event.target.closest('[data-review-prefer]');if(prefer){
  sessionReview.decision={layout:prefer.dataset.reviewPrefer,space:sessionReview.space,at:new Date().toISOString()};
  try{localStorage.setItem('mandocues-v3-review',JSON.stringify(sessionReview.decision));}catch{}
  prefer.closest('dialog').close();toast('Review preference saved on this device.');
 }
});
renderDemo();

document.addEventListener('toggle',event=>{if(!event.target.isConnected)return;if(event.target.matches('.v3-more-timing'))sessionReview.moreTiming=event.target.open;if(event.target.matches('.v3-session-setup'))sessionReview.setupOpen=event.target.open;},true);
