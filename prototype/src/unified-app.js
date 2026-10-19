// One workspace, one take model. The old layouts remain recoverable in Git.
const unifiedState=Object.assign(states.partituur,{unified:true,sessionStarted:false,booked:360,elapsed:42,remaining:320,sessionEnded:false,sessionPausedAt:null});
for(const id of Object.keys(states))states[id]=unifiedState;
cuePlanningState=unifiedState;
let proposalView='recording';
const previousRenderDemo=renderDemo;
const previousToggleRecord=toggleRecord;
const previousComposer=composer;

function initializeProposalTiming(s){
 const timing=scoreWorkflowTiming(s);
 // Example planning only; the production app keeps its own scheduling policy.
 if(s.unified&&!s.unifiedTiming){Object.assign(timing.clock,{booked:s.booked*60,remaining:s.remaining*60,plannedEndAt:Date.now()+(s.booked*60-timing.elapsed)*1000});s.unifiedTiming=true;}
 return scoreWorkflowTiming(s);
}
const PROPOSAL_DELAY_RED_AFTER=5*60;
function proposalPlanClass(delta){return delta>0?(delta>=PROPOSAL_DELAY_RED_AFTER?'is-late':'is-behind'):delta<0?'is-ahead':'is-on-time';}
function proposalPlanLabel(delta){return delta===0?'On schedule':time(Math.abs(delta))+(delta>0?' behind schedule':' ahead of schedule');}
function proposalSchedule(){
 const timing=initializeProposalTiming(unifiedState);
 return `<span class="proposal-schedule ${proposalPlanClass(timing.delta)}" data-proposal-plan aria-label="${proposalPlanLabel(timing.delta)}" title="${proposalPlanLabel(timing.delta)}">${scoreWorkflowPlanText(timing.delta)}</span>`;
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
function plannedPicker(s,j,place='list'){
 const value=cuePlannedMinutes(j),automatic=s.cueSettings?.[j]?.planned===null,values=Array.from({length:120},(_,i)=>i+1);if(value>120||!Number.isInteger(value))values.push(value);values.sort((a,b)=>a-b);
 return `<details class="planned-picker" data-planned-menu="${j}"><summary title="${automatic?'Automatic estimate':'Manual override'} · clear to use Auto" aria-label="Planned work in minutes for ${cues[j][0]}"><b>${value}</b>${place==='main'?' min':''}<span aria-hidden="true">⌄</span></summary><div class="planned-picker-panel"><input data-planned-input="${j}" type="text" inputmode="decimal" value="${automatic?'':value}" placeholder="Auto" aria-label="Planned minutes for ${cues[j][0]}"><div class="planned-choices" role="group" aria-label="Choose planned minutes"><button type="button" data-pick-planned="auto" data-planned-cue="${j}" aria-pressed="${automatic}">Auto · ${cueAutoMinutes(s,j)} min</button>${values.map(n=>`<button type="button" data-pick-planned="${n}" data-planned-cue="${j}" aria-pressed="${!automatic&&n===value}">${n} min</button>`).join('')}</div></div></details>`;
}
function closePlannedPickers(){document.querySelectorAll('.planned-picker[open]').forEach(el=>el.open=false);}
function positionPlannedPicker(menu){
 if(!menu?.open)return;const panel=menu.querySelector('.planned-picker-panel'),r=menu.querySelector('summary').getBoundingClientRect();
 Object.assign(panel.style,{left:Math.max(8,Math.min(innerWidth-panel.offsetWidth-8,r.left))+'px',top:(r.bottom+panel.offsetHeight+6<innerHeight?r.bottom+6:Math.max(8,r.top-panel.offsetHeight-6))+'px'});
}
function choosePlanned(j,value){
 if(value==='auto'||!String(value).trim()){cueSettings(unifiedState,+j).planned=null;closePlannedPickers();renderDemo();return;}
 if(!String(value).trim()||!Number.isFinite(+value)||+value<1||+value>1440){toast('Choose planned minutes from 1 to 1440.');return;}
 cueSettings(unifiedState,+j).planned=+value;closePlannedPickers();renderDemo();
}
document.addEventListener('toggle',event=>{
 const menu=event.target;if(!menu.matches('.planned-picker')||!menu.open)return;
 document.querySelectorAll('.planned-picker[open]').forEach(other=>{if(other!==menu)other.open=false;});closeMeasurePickers();
 positionPlannedPicker(menu);const list=menu.querySelector('.planned-choices'),chosen=list.querySelector('[aria-pressed="true"]');if(chosen)list.scrollTop=chosen.offsetTop-(list.clientHeight-chosen.offsetHeight)/2;
 const input=menu.querySelector('input');input.focus({preventScroll:true});input.select();
},true);
document.addEventListener('click',event=>{
 const choice=event.target.closest('[data-pick-planned]');if(choice){choosePlanned(choice.dataset.plannedCue,choice.dataset.pickPlanned);return;}
 if(!event.target.closest('.planned-picker'))closePlannedPickers();
});
document.addEventListener('keydown',event=>{
 if(!event.target.matches('[data-planned-input]'))return;
 if(event.key==='Enter'&&!event.metaKey&&!event.ctrlKey&&!event.isComposing){event.preventDefault();choosePlanned(event.target.dataset.plannedInput,event.target.value);}
 if(event.key==='Escape'){event.preventDefault();const summary=event.target.closest('details').querySelector('summary');closePlannedPickers();summary.focus({preventScroll:true});}
});
addEventListener('resize',()=>document.querySelectorAll('.planned-picker[open]').forEach(positionPlannedPicker));
document.addEventListener('scroll',()=>document.querySelectorAll('.planned-picker[open]').forEach(positionPlannedPicker),true);
let mainPanelLayout='A';
function mainPanelOptions(){return `<div class="main-panel-options" lang="nl" role="group" aria-label="Indeling vergelijken"><span>Indeling proberen</span><button data-main-layout="A" aria-pressed="${mainPanelLayout==='A'}">A · Klok midden</button><button data-main-layout="B" aria-pressed="${mainPanelLayout==='B'}">B · Klok boven</button></div>`;}
calmPanel=function(s){
 const timing=scoreWorkflowTiming(s),t=running(s),selected=takeById(s,s.selected),c=cues[s.cue];
 const ready=!s.sessionStarted,paused=!!s.sessionPausedAt;
 const stateLabel=t?'● Recording':paused?'On break · Not recording':s.sessionEnded?'Session ended · Not recording':ready?'Ready to start · Not recording':'Standby · Not recording';
 return `<section id="main-panel" class="calm-main-panel proposal-main-panel layout-${mainPanelLayout} ${t?'is-recording':'is-idle'}" aria-label="Recording controls">
 <div class="calm-cue"><span class="rec-status ${t?'rolling':'standby'}">${stateLabel}</span><div class="main-cue"><b>${c[0]}</b><strong title="${esc(c[1])}">${esc(c[1])}</strong></div><small>Music length ${c[2]}</small><div class="proposal-cue-switcher calm-cue-actions" role="group" aria-label="Cue controls"><button data-action="prev-cue" ${t||s.cue===0?'disabled':''} title="Previous cue · [">← Previous cue <kbd>[</kbd></button><button data-action="next-cue" ${t||s.cue===cues.length-1?'disabled':''} title="Next cue · ]">Next cue → <kbd>]</kbd></button></div></div>
 <div class="proposal-session-clocks"><label>Time<b data-wall-clock>${new Date().toLocaleTimeString('en-GB')}</b></label><div class="proposal-clock-plan">${proposalSchedule()}</div><div class="proposal-main-planning"><label>Cue work <b data-proposal-cue-clock>${time(timing.cueElapsed)}</b><span> / ${plannedPicker(s,s.cue,'main')} planned</span></label></div></div>
 <div class="proposal-action-group calm-transport" role="group" aria-label="Take controls"><div class="main-take-heading"><strong>${t?entryLabel(t):selected?entryLabel(selected):'No take selected'}</strong><span>${t&&selected&&t.id!==selected.id?'Viewing '+entryLabel(selected):t?'Recording':selected?'Selected take':''}</span></div><div class="main-take-actions">${recordButton(s)}<button data-action="record-overdub" ${ready||paused||t?'disabled':''}>Overdub ${nextEntryNumber(s,s.cue,'overdub')}</button><label class="proposal-take-clock">Take duration<b ${t?`data-live="${t.id}"`:''}>${time(t?position(t):selected?.duration||0)}</b></label></div></div>
 <aside class="main-session-rail" aria-label="Session settings and controls">${proposalSessionHeader(s)}<div class="proposal-action-group proposal-session-actions" role="group" aria-label="Session controls"><button data-session-action="break" ${ready||t?'disabled':''}>${appIcon('cup')}${paused?'Resume':'Break'}</button><button data-session-action="end" class="proposal-end-session" ${ready||t?'disabled':''}>End session</button></div><div class="main-session-times"><span>Worked <b data-proposal-elapsed>${proposalDuration(timing.elapsed)}</b></span><span>Remaining <b>${proposalDuration(timing.clock.remaining)}</b></span><span>Planned end <b data-proposal-planned-end>${proposalEndTime(timing,false)}</b></span></div></aside>
 </section>`;
};
composer=function(s,t,score=false,place='list'){
 const output=previousComposer(s,t,score,place);
 return s.unified&&active.id!=='notities'?output.replace('<div class="composer-footer">',quickNoteSuggestions(t,place)+'<div class="composer-footer">'):output;
};
function cueSettings(s,j){s.cueSettings??={};return s.cueSettings[j]??={complexity:'Medium',planned:cuePlannedMinutes(j),complete:false};}
function cueActualSeconds(s,j){const timing=scoreWorkflowTiming(s);return j===s.cue?timing.cueElapsed:timing.clock.cueSpent[j]??null;}
function cueActualClass(s,j,seconds){if(seconds===null)return '';const over=seconds-cuePlannedMinutes(j)*60;return over>0?proposalPlanClass(over):cueSettings(s,j).complete?'is-complete':'';}
function cueActual(s,j){const seconds=cueActualSeconds(s,j);return `<span class="cue-actual ${cueActualClass(s,j,seconds)}" data-cue-actual="${j}" aria-label="Actual work time for ${cues[j][0]}">${seconds===null?'—':proposalDuration(seconds)}</span>`;}
function proposalRatingFilter(s){return `<div class="review-filter"><label>Show takes <select data-rating-filter>${[[0,'All ratings'],[3,'3–5 stars'],[4,'4–5 stars'],[5,'Only 5 stars']].map(([n,label])=>`<option value="${n}" ${s.minRating===n?'selected':''}>${label}</option>`).join('')}</select></label></div>`;}
controls=function(){const s=state();return `<div class="calm-scroll control-scroll"><div class="sticky-slot" aria-hidden="true">${transport(s)}</div>${mainPanelOptions()}${calmPanel(s)}${cueTimeline(s)}<div class="calm-content"><div class="proposal-cues">${proposalRatingFilter(s)}${calmCueList(s)}</div>${calmNotes(s)}</div></div>`;};
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
 initializeProposalTiming(unifiedState);
 document.body.classList.toggle('recording-workspace',proposalView==='recording');
 const shell=document.querySelector('.proposal-shell');
 if(proposalView==='recording'){shell.id='cue-scroll';shell.tabIndex=0;shell.setAttribute('aria-label','Recording workspace');}
 else{shell.removeAttribute('id');shell.removeAttribute('tabindex');shell.removeAttribute('aria-label');shell.scrollTop=0;}
 document.body.classList.toggle('score-workspace',proposalView==='cutlist');
 document.body.classList.toggle('score-expanded',proposalView==='cutlist');
 previousRenderDemo();
 if(proposalView==='recording'){
  for(const row of document.querySelectorAll('[data-calm-take]')){
   const t=takeById(unifiedState,row.dataset.calmTake);row.hidden=!!unifiedState.minRating&&t.rating<unifiedState.minRating;
  }
 }
 const toggle=document.querySelector('[data-proposal-view="'+proposalView+'"]');
 document.querySelectorAll('[data-proposal-view]').forEach(button=>button.setAttribute('aria-pressed',button===toggle));
 document.querySelector('.proposal-workspace-title').textContent=proposalView==='recording'?'Recording':'Comp tool';
 const sessionSlot=document.querySelector('.proposal-session-header-slot');sessionSlot.hidden=true;sessionSlot.innerHTML='';
 const bar=document.querySelector('.proposal-live-bar');
 if(bar){bar.hidden=proposalView!=='cutlist';bar.innerHTML=proposalView==='cutlist'?transport(unifiedState):'';}
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
 document.querySelector('.site-header').insertAdjacentHTML('afterend',appSidebar());
 document.querySelector('#app').innerHTML=`<main class="proposal-shell"><header class="proposal-view-bar" lang="en"><div class="proposal-project-heading"><h1 class="proposal-workspace-title">Recording</h1><small>After Party · String quartet · 20 October</small></div><nav class="proposal-view-toggle" aria-label="Workspace view"><button type="button" data-proposal-view="recording" aria-pressed="true">Recording</button><button type="button" data-proposal-view="cutlist" aria-pressed="false">Comp tool</button></nav><div class="proposal-live-bar" lang="en" hidden></div><small class="proposal-demo-label">Demo · no audio is recorded</small><div class="proposal-cutlist-review" lang="nl"></div></header><div class="proposal-session-header-slot"></div><div class="browser-frame"><div class="demo" id="demo" lang="en"></div></div></main>`;
}
route=function(){
 if(!document.querySelector('.proposal-shell'))mountProposal();
 const hash=location.hash.slice(1);showProposalView(['cutlist','partituur'].includes(hash)?'cutlist':'recording',{navigate:false});
};
document.addEventListener('change',event=>{
 const el=event.target;
 if(el.dataset.cueComplexity!==undefined){if(['Low','Medium','High'].includes(el.value))cueSettings(unifiedState,+el.dataset.cueComplexity).complexity=el.value;else return;}
 else if(el.dataset.cuePlanned!==undefined){const value=Number(el.value);if(!el.value.trim()||!Number.isFinite(value)||value<1||value>1440){el.value=cuePlannedMinutes(+el.dataset.cuePlanned);return;}cueSettings(unifiedState,+el.dataset.cuePlanned).planned=value;}
 else if(el.dataset.cueComplete!==undefined)cueSettings(unifiedState,+el.dataset.cueComplete).complete=el.checked;
 else return;
 renderDemo();
});
document.addEventListener('keydown',event=>{if(event.key==='Enter'&&event.target.matches('[data-cue-planned]')&&!event.metaKey&&!event.ctrlKey&&!event.altKey&&!event.isComposing){event.preventDefault();event.target.blur();}});
document.addEventListener('click',event=>{
 const layout=event.target.closest('[data-main-layout]');if(layout){mainPanelLayout=layout.dataset.mainLayout==='B'?'B':'A';renderDemo();return;}
 const action=event.target.closest('[data-session-action]');
 if(action){if(!action.disabled){if(action.dataset.sessionAction==='break')proposalSessionBreak(unifiedState);else proposalEndSession(unifiedState);}return;}
 const button=event.target.closest('[data-proposal-view]');if(!button)return;
 showProposalView(button.dataset.proposalView);
});
setInterval(()=>{
 if(!document.body.classList.contains('unified-proposal'))return;
 const timing=scoreWorkflowTiming(unifiedState);
 document.querySelectorAll('[data-proposal-plan]').forEach(el=>{el.textContent=scoreWorkflowPlanText(timing.delta);el.className='proposal-schedule '+proposalPlanClass(timing.delta);el.setAttribute('aria-label',proposalPlanLabel(timing.delta));el.title=proposalPlanLabel(timing.delta);});
 document.querySelectorAll('[data-proposal-elapsed]').forEach(el=>el.textContent=proposalDuration(timing.elapsed));
 document.querySelectorAll('[data-proposal-cue-clock]').forEach(el=>el.textContent=time(timing.cueElapsed));
 document.querySelectorAll('[data-cue-actual]').forEach(el=>{const j=+el.dataset.cueActual,seconds=cueActualSeconds(unifiedState,j);el.textContent=seconds===null?'—':proposalDuration(seconds);el.className='cue-actual '+cueActualClass(unifiedState,j,seconds);});
 document.querySelectorAll('[data-proposal-planned-end]').forEach(el=>el.textContent=proposalEndTime(timing,false));
},200);
route();
