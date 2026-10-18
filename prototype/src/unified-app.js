// One workspace, one take model. The old layouts remain recoverable in Git.
const unifiedState=Object.assign(states.partituur,{unified:true,sessionStarted:false,booked:360,elapsed:42,remaining:320,sessionEnded:false,sessionPausedAt:null});
for(const id of Object.keys(states))states[id]=unifiedState;
let proposalView='recording';
const previousRenderDemo=renderDemo;
const previousToggleRecord=toggleRecord;
const previousComposer=composer;

function proposalSchedule(){
 const timing=scoreWorkflowTiming(unifiedState);
 // Shared example schedule; never claimed to be DAW timing.
 if(!unifiedState.unifiedTiming){Object.assign(timing.clock,{booked:360*60,remaining:320*60,plannedEndAt:Date.now()+(360*60-42*60)*1000});unifiedState.unifiedTiming=true;}
 return `<span class="proposal-schedule ${scoreWorkflowTiming(unifiedState).delta>0?'is-behind':'is-ahead'}" data-proposal-plan>${scoreWorkflowPlanText(scoreWorkflowTiming(unifiedState).delta)}</span>`;
}
function proposalDuration(seconds){return seconds>=3600?Math.floor(seconds/3600)+':'+String(Math.floor(seconds/60)%60).padStart(2,'0')+':'+String(seconds%60).padStart(2,'0'):time(seconds);}
function proposalClockTime(ms){return new Date(ms).toLocaleTimeString('en-GB',{hour:'2-digit',minute:'2-digit'});}
function proposalEndTime(timing,expected=true){return proposalClockTime(timing.clock.plannedEndAt+(expected?timing.delta:0)*1000);}
function proposalSessionBreak(s){
 if(!s.sessionStarted||running(s))return;
 const timing=scoreWorkflowTiming(s),now=Date.now();
 if(s.sessionPausedAt){
  const duration=now-s.sessionPausedAt;
  timing.clock.started+=duration;timing.clock.cueStarted+=duration;
  timing.clock.breakSeconds=(timing.clock.breakSeconds||0)+Math.floor(duration/1000);
  s.sessionPausedAt=null;
 }else s.sessionPausedAt=now;
 renderDemo();
}
function proposalEndSession(s){
 if(!s.sessionStarted||running(s))return;
 if(s.sessionPausedAt)proposalSessionBreak(s);
 const {clock,elapsed,cueElapsed}=scoreWorkflowTiming(s);
 clock.sessionBase=elapsed-clock.offset;clock.cueBase=cueElapsed-clock.offset+clock.cueOffset;
 clock.started=Date.now();clock.cueStarted=Date.now();
 s.sessionStarted=false;s.sessionEnded=true;renderDemo();
}
calmPanel=function(s){
 const status=proposalSchedule(),timing=scoreWorkflowTiming(s),t=running(s),c=cues[s.cue];
 const ready=!s.sessionStarted,paused=!!s.sessionPausedAt;
 const stateLabel=t?'● Recording · '+entryLabel(t):paused?'● On break':s.sessionEnded?'● Session ended':ready?'● Ready to start':'● Standby';
 return `<section id="main-panel" class="calm-main-panel proposal-main-panel" aria-label="Recording controls">
 <div class="proposal-main-top"><div class="calm-cue"><span class="rec-status ${t?'rolling':'standby'}">${stateLabel}</span><div class="main-cue"><b>${c[0]}</b><strong>${esc(c[1])}</strong></div><small>Music ${c[2]} · Planned cue time ${time(cuePlannedMinutes(s.cue)*60)}</small></div>
 <div class="proposal-session-clocks"><label>Time<b data-wall-clock>${new Date().toLocaleTimeString('en-GB')}</b></label><label>Expected end<b data-proposal-expected-end>${proposalEndTime(timing)}</b></label></div></div>
 <div class="proposal-main-actions">
 <div class="proposal-action-group calm-transport" role="group" aria-label="Take controls"><small>Take</small><div>${recordButton(s)}<button data-action="record-overdub" ${ready||paused||t?'disabled':''}>Overdub ${nextEntryNumber(s,s.cue,'overdub')}</button><label class="proposal-take-clock">Take time<b ${t?`data-live="${t.id}"`:''}>${time(t?position(t):0)}</b></label></div></div>
 <div class="proposal-action-group calm-cue-actions" role="group" aria-label="Cue controls"><small>Cue</small><div><button data-action="prev-cue" ${t?'disabled':''}>← Previous cue</button><button data-action="next-cue" ${t?'disabled':''}>Next cue →</button></div></div>
 <div class="proposal-action-group proposal-session-actions" role="group" aria-label="Session controls"><small>Session</small><div><button data-session-action="break" ${ready||t?'disabled':''}>${paused?'Resume':'Break'}</button><button data-session-action="end" class="proposal-end-session" ${ready||t?'disabled':''}>End session</button></div></div>
 </div>
 <div class="proposal-main-planning"><div class="calm-schedule">${status}</div><label>Cue time <b data-proposal-cue-clock>${time(timing.cueElapsed)}</b><span> / <b>${time(timing.budget)}</b> planned</span></label></div>
 <details class="calm-session" data-calm-session ${s.calmSessionOpen?'open':''}><summary>Session details</summary>${sourceSessionSummary(s)}<div class="calm-extra-times"><span>Session elapsed <b data-proposal-elapsed>${proposalDuration(timing.elapsed)}</b></span><span>Remaining work <b>${proposalDuration(timing.clock.remaining)}</b></span><span>Planned end <b data-proposal-planned-end>${proposalEndTime(timing,false)}</b></span></div></details>
 </section>`;
};
composer=function(s,t,score=false,place='list'){
 const output=previousComposer(s,t,score,place);
 return s.unified&&active.id!=='notities'?output.replace('<div class="composer-footer">',quickNoteSuggestions(t,place)+'<div class="composer-footer">'):output;
};
function proposalRatingFilter(s){return `<div class="review-filter"><label>Show takes <select data-rating-filter>${[[0,'All ratings'],[3,'3–5 stars'],[4,'4–5 stars'],[5,'Only 5 stars']].map(([n,label])=>`<option value="${n}" ${s.minRating===n?'selected':''}>${label}</option>`).join('')}</select></label></div>`;}
controls=function(){const s=state();return `<div class="calm-scroll control-scroll" id="cue-scroll" tabindex="0" aria-label="Recording workspace"><div class="sticky-slot" aria-hidden="true">${transport(s)}</div>${calmPanel(s)}${cueTimeline(s)}<div class="calm-content"><div class="proposal-cues">${proposalRatingFilter(s)}${calmCueList(s)}</div>${calmNotes(s)}</div><footer class="proposal-review-footer" lang="nl"></footer></div>`;};
selectCue=function(s,index){selectScoreCue(s,index);};
toggleRecord=function(s,kind='take'){
 s.sessionStarted=true;
 const before=running(s);previousToggleRecord(s,kind);
 if(!before&&running(s)){
  s.scoreCompared??={};s.scoreCompared[s.cue]=[s.selected];
  s.scoreComment=null;renderDemo();
 }
};
renderDemo=function(){
 document.body.classList.toggle('score-workspace',proposalView==='cutlist');
 document.body.classList.toggle('score-expanded',proposalView==='cutlist');
 // Keep the persistent review header outside the subtree being rebuilt.
 const reviewHeader=document.querySelector('.site-header');
 if(reviewHeader?.closest('#demo'))document.body.append(reviewHeader);
 previousRenderDemo();
 if(proposalView==='recording')document.querySelector('.proposal-review-footer')?.append(reviewHeader);
 if(proposalView==='recording'){
  for(const row of document.querySelectorAll('[data-calm-take]')){
   const t=takeById(unifiedState,row.dataset.calmTake);row.hidden=!!unifiedState.minRating&&t.rating<unifiedState.minRating;
  }
 }
 const toggle=document.querySelector('[data-proposal-view="'+proposalView+'"]');
 document.querySelectorAll('[data-proposal-view]').forEach(button=>button.setAttribute('aria-pressed',button===toggle));
 document.querySelector('.proposal-workspace-title').textContent=proposalView==='recording'?'Recording':'Cut list';
 const bar=document.querySelector('.proposal-live-bar');
 if(bar){bar.hidden=proposalView!=='cutlist';bar.innerHTML=proposalView==='cutlist'?transport(unifiedState):'';}
 const review=document.querySelector('.proposal-review-actions'),reviewHome=document.querySelector(proposalView==='cutlist'?'.proposal-cutlist-review':'.site-header');
 if(review&&reviewHome&&review.parentElement!==reviewHome)reviewHome.append(review);
 syncRecordingDock();
 if(typeof scheduleTourPosition==='function')scheduleTourPosition();
};
function showProposalView(view,{navigate=true}={}){
 cancelTakeNumberEntry();
 view=view==='cutlist'?'cutlist':'recording';
 if(active?.id==='partituur')rememberScoreView(unifiedState);
 if(proposalView==='recording')unifiedState.recordingScroll=document.querySelector('#cue-scroll')?.scrollTop||0;
 proposalView=view;active=ideas.find(i=>i.id===(view==='cutlist'?'partituur':'bediening'));variant='A';
 unifiedState.controlsPrevious=false;unifiedState.showMainScore=false;
 if(navigate)history.replaceState(null,'','#'+view);
 renderDemo();
 if(view==='recording'&&document.querySelector('#cue-scroll'))document.querySelector('#cue-scroll').scrollTop=unifiedState.recordingScroll||0;
 if(view==='cutlist'&&unifiedState.selected){
  const saved=takeById(unifiedState,unifiedState.selected)?.scoreViews?.[unifiedState.doc.id];
  if(saved&&document.querySelector('.score-canvas'))document.querySelector('.score-canvas').scrollTop=saved.top||0;
 }
 scheduleRecordingControls();
}
fullscreenPrototype=async function(){
 try{if(document.fullscreenElement)await document.exitFullscreen();else if(document.documentElement.requestFullscreen)await document.documentElement.requestFullscreen();else document.body.classList.toggle('proposal-expanded');}catch{document.body.classList.toggle('proposal-expanded');}
};
document.addEventListener('keydown',event=>{if(event.key==='Escape')document.body.classList.remove('proposal-expanded');});
function mountProposal(){
 document.body.classList.add('unified-proposal');document.title='MandoCues · voorstel van Floris';
 document.querySelector('.site-header').innerHTML=`<a class="wordmark" href="#recording"><span class="brand-icon">m<span>·</span></span>MandoCues<span class="divider">/</span><span class="header-label">voorstel van Floris</span></a><div class="proposal-review-actions"><button type="button" data-proposal-action="fullscreen" aria-label="Schermvullend" title="Schermvullend">⛶</button><button type="button" data-proposal-action="tour">Rondleiding</button><button type="button" data-proposal-action="questions">Vragen</button><button type="button" data-proposal-action="prompt">Claude-prompt <span data-proposal-selection-count>0</span></button></div>`;
 document.querySelector('#app').innerHTML=`<main class="proposal-shell"><header class="proposal-view-bar" lang="en"><div class="proposal-project-heading"><h1 class="proposal-workspace-title">Recording</h1><small>After Party · String quartet · 20 October</small></div><nav class="proposal-view-toggle" aria-label="Workspace view"><button type="button" data-proposal-view="recording" aria-pressed="true">Recording</button><button type="button" data-proposal-view="cutlist" aria-pressed="false">Cut list</button></nav><div class="proposal-live-bar" lang="en" hidden></div><small class="proposal-demo-label">Demo · no audio is recorded</small><div class="proposal-cutlist-review" lang="nl"></div></header><div class="browser-frame"><div class="demo" id="demo" lang="en"></div></div></main>`;
}
route=function(){
 if(!document.querySelector('.proposal-shell'))mountProposal();
 const hash=location.hash.slice(1);showProposalView(['cutlist','partituur'].includes(hash)?'cutlist':'recording',{navigate:false});
};
document.addEventListener('click',event=>{
 const action=event.target.closest('[data-session-action]');
 if(action){if(!action.disabled){if(action.dataset.sessionAction==='break')proposalSessionBreak(unifiedState);else proposalEndSession(unifiedState);}return;}
 const button=event.target.closest('[data-proposal-view]');if(!button)return;
 showProposalView(button.dataset.proposalView);
});
setInterval(()=>{
 if(!document.body.classList.contains('unified-proposal'))return;
 const timing=scoreWorkflowTiming(unifiedState);
 document.querySelectorAll('[data-proposal-plan]').forEach(el=>{el.textContent=scoreWorkflowPlanText(timing.delta);el.classList.toggle('is-behind',timing.delta>0);el.classList.toggle('is-ahead',timing.delta<=0);});
 document.querySelectorAll('[data-proposal-elapsed]').forEach(el=>el.textContent=proposalDuration(timing.elapsed));
 document.querySelectorAll('[data-proposal-cue-clock]').forEach(el=>el.textContent=time(timing.cueElapsed));
 document.querySelectorAll('[data-proposal-expected-end]').forEach(el=>el.textContent=proposalEndTime(timing));
 document.querySelectorAll('[data-proposal-planned-end]').forEach(el=>el.textContent=proposalEndTime(timing,false));
},200);
route();
