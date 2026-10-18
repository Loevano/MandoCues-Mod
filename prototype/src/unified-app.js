// One workspace, one take model. The old layouts remain recoverable in Git.
const unifiedState=Object.assign(states.partituur,{unified:true,booked:360,elapsed:42,remaining:320});
for(const id of Object.keys(states))states[id]=unifiedState;
let proposalView='recording';
const previousRenderDemo=renderDemo;
const previousToggleRecord=toggleRecord;
const previousComposer=composer;
const previousCalmPanel=calmPanel;

function proposalSchedule(){
 const timing=scoreWorkflowTiming(unifiedState);
 // Shared example schedule; never claimed to be DAW timing.
 if(!unifiedState.unifiedTiming){Object.assign(timing.clock,{booked:360*60,remaining:320*60});unifiedState.unifiedTiming=true;}
 return `<span class="proposal-schedule ${scoreWorkflowTiming(unifiedState).delta>0?'is-behind':'is-ahead'}" data-proposal-plan>${scoreWorkflowPlanText(scoreWorkflowTiming(unifiedState).delta)}</span>`;
}
function proposalDuration(seconds){return seconds>=3600?Math.floor(seconds/3600)+':'+String(Math.floor(seconds/60)%60).padStart(2,'0')+':'+String(seconds%60).padStart(2,'0'):time(seconds);}
calmPanel=function(s){
 const status=proposalSchedule(),timing=scoreWorkflowTiming(s);
 return previousCalmPanel(s).replace('<div class="calm-schedule">On schedule</div>',`<div class="calm-schedule">${status}</div>`).replace('<b>14:42</b>',`<b data-proposal-elapsed>${proposalDuration(timing.elapsed)}</b>`).replace('<b>5:45:18</b>',`<b>${proposalDuration(timing.clock.remaining)}</b>`);
};
composer=function(s,t,score=false,place='list'){
 const output=previousComposer(s,t,score,place);
 return s.unified&&active.id!=='notities'?output.replace('<div class="composer-footer">',quickNoteSuggestions(t,place)+'<div class="composer-footer">'):output;
};
function proposalRatingFilter(s){return `<div class="review-filter"><label>Show takes <select data-rating-filter>${[[0,'All ratings'],[3,'3–5 stars'],[4,'4–5 stars'],[5,'Only 5 stars']].map(([n,label])=>`<option value="${n}" ${s.minRating===n?'selected':''}>${label}</option>`).join('')}</select></label></div>`;}
controls=function(){const s=state();return `<div class="calm-scroll control-scroll" id="cue-scroll" tabindex="0" aria-label="Recording workspace"><div class="sticky-slot" aria-hidden="true">${transport(s)}</div>${calmPanel(s)}${cueTimeline(s)}<div class="calm-content"><div class="proposal-cues">${proposalRatingFilter(s)}${calmCueList(s)}</div>${calmNotes(s)}</div></div>`;};
selectCue=function(s,index){selectScoreCue(s,index);};
toggleRecord=function(s,kind='take'){
 const before=running(s);previousToggleRecord(s,kind);
 if(!before&&running(s)){
  s.scoreCompared??={};s.scoreCompared[s.cue]=[s.selected];
  s.scoreComment=null;renderDemo();
 }
};
renderDemo=function(){
 previousRenderDemo();
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
 syncRecordingDock();
 if(typeof scheduleTourPosition==='function')scheduleTourPosition();
};
function showProposalView(view,{navigate=true}={}){
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
function mountProposal(){
 document.body.classList.add('unified-proposal');document.title='MandoCues · voorstel van Floris';
 document.querySelector('.site-header').innerHTML=`<a class="wordmark" href="#recording"><span class="brand-icon">m<span>·</span></span>MandoCues<span class="divider">/</span><span class="header-label">voorstel van Floris</span></a><div class="proposal-review-actions"><button type="button" data-proposal-action="tour">Rondleiding</button><button type="button" data-proposal-action="questions">Vragen</button><button type="button" data-proposal-action="prompt">Claude-prompt <span data-proposal-selection-count>0</span></button></div>`;
 document.querySelector('#app').innerHTML=`<main class="proposal-shell"><header class="proposal-view-bar" lang="en"><div><h1 class="proposal-workspace-title">Recording</h1><small>After Party · String quartet · 20 October</small></div><nav class="proposal-view-toggle" aria-label="Workspace view"><button type="button" data-proposal-view="recording" aria-pressed="true">Recording</button><button type="button" data-proposal-view="cutlist" aria-pressed="false">Cut list</button></nav><small class="proposal-demo-label">Demo · no audio is recorded</small></header><div class="proposal-live-bar" lang="en" hidden></div><div class="browser-frame"><div class="demo" id="demo" lang="en"></div></div></main>`;
}
route=function(){
 if(!document.querySelector('.proposal-shell'))mountProposal();
 const hash=location.hash.slice(1);showProposalView(['cutlist','partituur'].includes(hash)?'cutlist':'recording',{navigate:false});
};
document.addEventListener('click',event=>{
 const button=event.target.closest('[data-proposal-view]');if(!button)return;
 showProposalView(button.dataset.proposalView);
});
setInterval(()=>{
 if(!document.body.classList.contains('unified-proposal'))return;
 const timing=scoreWorkflowTiming(unifiedState);
 document.querySelectorAll('[data-proposal-plan]').forEach(el=>{el.textContent=scoreWorkflowPlanText(timing.delta);el.classList.toggle('is-behind',timing.delta>0);el.classList.toggle('is-ahead',timing.delta<=0);});
 document.querySelectorAll('[data-proposal-elapsed]').forEach(el=>el.textContent=proposalDuration(timing.elapsed));
},200);
route();
