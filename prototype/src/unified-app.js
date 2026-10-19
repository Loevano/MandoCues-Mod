// One workspace, one take model. The old layouts remain recoverable in Git.
let unifiedState=Object.assign(states.partituur,{unified:true,sessionStarted:false,booked:360,elapsed:0,remaining:360,sessionEnded:false,sessionPausedAt:null});
const initialSessionCues=cues.map(c=>[...c]);
const proposalSessionCatalog=[{id:'strings-20261020',label:'String quartet · 20 October',detail:'20 October 2026 · 10:00 AM · Studio Hana'},{id:'strings-demo-day2',label:'String quartet · 21 October (demo)',detail:'21 October 2026 · 10:00 AM · Studio Hana · Example session'}];
unifiedState.sessionId=proposalSessionCatalog[0].id;unifiedState.sessionCues=cues.map(c=>[...c]);
const proposalSessionStates=new Map([[unifiedState.sessionId,unifiedState]]);
function proposalSessionMeta(s){return proposalSessionCatalog.find(day=>day.id===s.sessionId)||proposalSessionCatalog[0];}
function createSessionExample(id){
 const previous=cues.map(c=>[...c]);cues.splice(0,cues.length,...initialSessionCues.map(c=>[...c]));
 try{const next=Object.assign(fresh('partituur'),{unified:true,sessionId:id,sessionCues:cues.map(c=>[...c]),sessionStarted:false,booked:360,elapsed:0,remaining:360,sessionEnded:false,sessionPausedAt:null});next.takes=cues.map(()=>[]);next.selected=null;next.cueNotes=cues.map(()=>[]);return next;}finally{cues.splice(0,cues.length,...previous);}
}
function switchProposalSession(id){
 if(id===unifiedState.sessionId||!proposalSessionCatalog.some(day=>day.id===id))return;
 if(running(unifiedState)){toast('Stop the active take before changing recording day.');document.querySelectorAll('[data-session-select]').forEach(el=>el.value=unifiedState.sessionId);return;}
 rememberScoreView(unifiedState);unifiedState.sessionCues=cues.map(c=>[...c]);
 unifiedState.recordingScroll=document.querySelector('#cue-scroll')?.scrollTop||unifiedState.recordingScroll||0;
 const view={zoom:unifiedState.zoom,scorePageColumns:unifiedState.scorePageColumns,scoreContinuous:unifiedState.scoreContinuous};
 if(!proposalSessionStates.has(id))proposalSessionStates.set(id,createSessionExample(id));
 unifiedState=proposalSessionStates.get(id);Object.assign(unifiedState,view);cues.splice(0,cues.length,...unifiedState.sessionCues.map(c=>[...c]));
 for(const key of Object.keys(states))states[key]=unifiedState;cuePlanningState=unifiedState;cancelTakeNumberEntry();renderDemo();renderSessionChat();
 const scroll=document.querySelector('#cue-scroll');if(scroll)scroll.scrollTop=unifiedState.recordingScroll||0;
}
document.addEventListener('change',event=>{if(event.target.matches('[data-session-select]'))switchProposalSession(event.target.value);});
function sessionPlanSummary(s){const minutes=cues.reduce((sum,_,j)=>sum+cuePlannedMinutes(j),0),duration=n=>Math.floor(n/60)+'h '+String(Math.round(n%60)).padStart(2,'0')+'m';return duration(minutes)+' planned · '+duration(s.booked)+' session';}
for(const id of Object.keys(states))states[id]=unifiedState;
cuePlanningState=unifiedState;
let proposalView='recording';
const previousRenderDemo=renderDemo;
const previousToggleRecord=toggleRecord;
const previousComposer=composer;

function initializeProposalTiming(s){
 const timing=scoreWorkflowTiming(s);
 // Example planning only; the production app keeps its own scheduling policy.
 if(s.unified&&!s.unifiedTiming){Object.assign(timing.clock,{booked:s.booked*60,plannedEndAt:Date.now()+(s.booked*60-timing.elapsed)*1000});s.unifiedTiming=true;}
 return scoreWorkflowTiming(s);
}
const PROPOSAL_DELAY_RED_AFTER=5*60;
function proposalPlanClass(delta){return delta>0?(delta>=PROPOSAL_DELAY_RED_AFTER?'is-late':'is-behind'):delta<0?'is-ahead':'is-on-time';}
function proposalScheduleText(delta){return delta===0?'On schedule':scoreWorkflowPlanText(delta);}
function proposalPlanLabel(delta){return delta===0?'On schedule':time(Math.abs(delta))+(delta>0?' behind schedule':' ahead of schedule');}
function proposalSchedule(){
 const timing=initializeProposalTiming(unifiedState);
 return `<span class="proposal-schedule ${proposalPlanClass(timing.delta)}" data-proposal-plan aria-label="${proposalPlanLabel(timing.delta)}" title="${proposalPlanLabel(timing.delta)}">${proposalScheduleText(timing.delta)}</span>`;
}
function proposalDuration(seconds){return seconds>=3600?Math.floor(seconds/3600)+':'+String(Math.floor(seconds/60)%60).padStart(2,'0')+':'+String(seconds%60).padStart(2,'0'):time(seconds);}
function proposalClockTime(ms){return formatLocalClock(ms,false);}
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
function confirmSessionReset(s){
 if(running(s))return;
 appDialog('Reset takes and timers?',`<p>Clear all takes, take notes, bar selections, cue completion and work timers for <strong>${esc(proposalSessionMeta(s).label)}</strong>?</p><p>Cue notes and planning settings stay. Take numbering starts again at 1.</p>`,'<button data-app-action="download-take-log">Download take log</button><button class="take-delete-confirm" data-confirm-session-reset="'+esc(s.sessionId)+'">Reset takes and timers</button>');
}
function resetProposalSession(s){
 if(s!==unifiedState||running(s))return false;
 const now=Date.now(),fixedEndAt=s.scoreWorkflowClock?.fixedEndAt??null;
 s.takes=cues.map(()=>[]);s.selected=null;s.takeSerials={};s.minRating=0;
 s.sessionStarted=false;s.sessionEnded=false;s.sessionPausedAt=null;s.elapsed=0;s.remaining=s.booked;
 for(const setting of Object.values(s.cueSettings||{}))setting.complete=false;
 s.scoreWorkflowClock={started:now,sessionBase:0,remaining:s.booked*60,booked:s.booked*60,offset:0,cueStarted:now,cueIndex:s.cue,cueBase:0,cueOffset:0,cueSpent:{},breakSeconds:0,fixedEndAt,plannedEndAt:fixedEndAt??now+s.booked*60000};
 s.unifiedTiming=true;s.open=new Set([s.cue]);s.scoreCompared={};s.scoreRangeAnchor={};s.scoreSelectedTakes={};
 s.scoreComment=null;s.focusedScoreNote=null;s.cutlistNotePreview=null;s.scoreFocus=null;delete s.pendingScoreScroll;
 document.querySelector('.app-dialog')?.close();cancelTakeNumberEntry();renderDemo();toast('Takes and timers reset for this recording day.');return true;
}
function completedCueText(s){return cues.filter((_,j)=>s.cueSettings?.[j]?.complete).length+' of '+cues.length+' cues done';}
function plannedPicker(s,j,place='list'){
 const value=cuePlannedMinutes(j),automatic=s.cueSettings?.[j]?.planned===null,values=Array.from({length:120},(_,i)=>i+1);if(value>120||!Number.isInteger(value))values.push(value);values.sort((a,b)=>a-b);
 return `<details class="planned-picker" data-planned-menu="${j}"><summary title="${automatic?'Automatic estimate':'Manual override'} · clear to use Auto" aria-label="Planned work in minutes for ${cues[j][0]}"><b>${value}</b>${place==='main'?' min':''}<span aria-hidden="true">⌄</span></summary><div class="planned-picker-panel"><input data-planned-input="${j}" type="text" inputmode="decimal" value="${automatic?'':value}" placeholder="Auto" aria-label="Planned minutes for ${cues[j][0]}"><div class="planned-choices" role="group" aria-label="Choose planned minutes"><button type="button" data-pick-planned="auto" data-planned-cue="${j}" aria-pressed="${automatic}">Auto · ${cueAutoMinutes(s,j)} min</button>${values.map(n=>`<button type="button" data-pick-planned="${n}" data-planned-cue="${j}" aria-pressed="${!automatic&&n===value}">${n} min</button>`).join('')}</div></div></details>`;
}
function closePlannedPickers(){document.querySelectorAll('.planned-picker[open]').forEach(el=>el.open=false);}
function positionPlannedPicker(menu){
 if(!menu?.open)return;const panel=menu.querySelector('.planned-picker-panel'),r=menu.querySelector('summary').getBoundingClientRect();
 Object.assign(panel.style,{left:Math.max(8,Math.min(innerWidth-panel.offsetWidth-8,r.left))+'px',top:(r.bottom+panel.offsetHeight+6<innerHeight?r.bottom+6:Math.max(8,r.top-panel.offsetHeight-6))+'px'});
}
function syncAutomaticPlanDisplay(s){
 document.querySelectorAll('[data-planned-menu]').forEach(menu=>{
  const j=+menu.dataset.plannedMenu;menu.querySelector('summary b').textContent=cuePlannedMinutes(j);
  const auto=menu.querySelector('[data-pick-planned="auto"]');if(auto)auto.textContent='Auto · '+cueAutoMinutes(s,j)+' min';
 });
 document.querySelectorAll('.cue-timeline [data-session-cue]').forEach(button=>{
  const j=+button.dataset.sessionCue,minutes=cuePlannedMinutes(j);button.style.flexBasis=minutes*8+'px';button.title=cues[j][0]+' · '+cues[j][1]+' · '+minutes+' min';button.setAttribute('aria-label',cues[j][0]+' '+cues[j][1]+', '+minutes+' minutes planned');
 });
 const end=document.querySelector('.cue-timeline>header>small');if(end)end.textContent=sessionPlanSummary(s);
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
function cueJumpMenu(s){
 return `<details class="cue-jump-menu" ${running(s)?'inert aria-disabled="true"':''}><summary aria-label="Go to cue">Go to cue <span aria-hidden="true">⌄</span></summary><div class="cue-jump-panel"><input type="search" data-cue-jump-search placeholder="Find cue…" aria-label="Find a cue" autocomplete="off"><div class="cue-jump-options" role="group" aria-label="Choose a cue">${cues.map((c,j)=>`<button type="button" data-go-to-cue="${j}" aria-current="${j===s.cue}" ${running(s)?'disabled':''}><b>${c[0]}</b><span>${esc(c[1])}</span>${cueSettings(s,j).complete?'<small aria-label="Completed">✓</small>':''}</button>`).join('')}</div><p class="cue-jump-empty" hidden>No matching cues.</p></div></details>`;
}
function closeCueJump(focus=false){const menu=document.querySelector('.cue-jump-menu[open]');if(!menu)return;menu.open=false;if(focus)menu.querySelector('summary').focus({preventScroll:true});}
function positionCueJump(){
 const menu=document.querySelector('.cue-jump-menu[open]');if(!menu)return;
 const panel=menu.querySelector('.cue-jump-panel'),r=menu.querySelector('summary').getBoundingClientRect();
 Object.assign(panel.style,{left:Math.max(8,Math.min(innerWidth-panel.offsetWidth-8,r.left))+'px',top:(r.bottom+panel.offsetHeight+6<innerHeight?r.bottom+6:Math.max(8,r.top-panel.offsetHeight-6))+'px'});
}
document.addEventListener('toggle',event=>{
 if(!event.target.matches('.cue-jump-menu')||!event.target.open)return;
 closeMeasurePickers();closePlannedPickers();const planning=document.querySelector('.session-planning-menu[open]');if(planning)planning.open=false;
 const menu=event.target,input=menu.querySelector('input');input.value='';menu.querySelectorAll('[data-go-to-cue]').forEach(button=>button.hidden=false);menu.querySelector('.cue-jump-empty').hidden=true;
 positionCueJump();menu.querySelector('[aria-current="true"]')?.scrollIntoView({block:'nearest'});input.focus({preventScroll:true});
},true);
document.addEventListener('input',event=>{
 if(!event.target.matches('[data-cue-jump-search]'))return;
 const menu=event.target.closest('details'),query=event.target.value.trim().toLowerCase();let count=0;
 menu.querySelectorAll('[data-go-to-cue]').forEach(button=>{button.hidden=!button.textContent.toLowerCase().includes(query);if(!button.hidden)count++;});menu.querySelector('.cue-jump-empty').hidden=!!count;positionCueJump();
});
document.addEventListener('click',event=>{
 const choice=event.target.closest('[data-go-to-cue]');if(choice){const j=+choice.dataset.goToCue;closeCueJump();selectCue(unifiedState,j);document.querySelector('.cue-jump-menu>summary')?.focus({preventScroll:true});return;}
 if(!event.target.closest('.cue-jump-menu'))closeCueJump();
});
document.addEventListener('keydown',event=>{
 const menu=document.querySelector('.cue-jump-menu[open]');if(!menu||!event.target.closest('.cue-jump-menu')||event.isComposing)return;
 if(event.key==='Escape'){event.preventDefault();closeCueJump(true);return;}
 const choices=[...menu.querySelectorAll('[data-go-to-cue]')].filter(button=>!button.hidden);
 if(event.key==='Enter'&&event.target.matches('[data-cue-jump-search]')){event.preventDefault();(choices.find(button=>button.getAttribute('aria-current')==='true')||choices[0])?.click();}
 if(event.key==='ArrowDown'||event.key==='ArrowUp'){
  event.preventDefault();const index=choices.indexOf(event.target),next=event.key==='ArrowDown'?Math.min(choices.length-1,index+1):Math.max(0,index-1);choices[next]?.focus({preventScroll:true});choices[next]?.scrollIntoView({block:'nearest'});
 }
});
addEventListener('resize',positionCueJump);document.addEventListener('scroll',positionCueJump,true);
function mainSessionTimes(timing){return `<div class="main-session-times" aria-label="Session timing"><label>Elapsed (working)<b data-proposal-elapsed>${proposalDuration(timing.elapsed)}</b></label><label>Remaining<b data-proposal-remaining>${proposalDuration(timing.remaining)}</b></label><label>Planned end<b data-proposal-planned-end>${proposalEndTime(timing,false)}</b></label><label>Projected end<b data-proposal-projected-end>${proposalEndTime(timing,true)}</b></label></div>`;}
function mainPlanCard(timing){return `<div class="main-plan-card ${proposalPlanClass(timing.delta)}" data-plan-card><strong data-plan-status data-proposal-plan class="proposal-schedule ${proposalPlanClass(timing.delta)}" aria-label="${proposalPlanLabel(timing.delta)}" title="${proposalPlanLabel(timing.delta)}">${proposalScheduleText(timing.delta)}</strong><small class="completed-cue-count">${completedCueText(unifiedState)}</small></div>`;}
calmPanel=function(s){
 const timing=scoreWorkflowTiming(s),t=running(s),c=cues[s.cue],ready=!s.sessionStarted,paused=!!s.sessionPausedAt;
 const stateLabel=t?'● Recording':paused?'On break':s.sessionEnded?'Session ended':ready?'Ready to start':'Standby';
 return `<section id="main-panel" class="calm-main-panel proposal-main-panel original-panel ${t?'is-recording':'is-idle'} ${proposalPlanClass(timing.delta)}" aria-label="Recording controls">
 <div class="original-cue-side"><div class="main-take-heading"><span class="rec-status ${t?'rolling':'standby'}" aria-label="${t?'Recording':'Not recording'}">${stateLabel}</span><span class="main-live-take ${t?'':'is-idle'}" ${t?'':'aria-hidden="true"'}><strong>${t?entryLabel(t):'Take 1'}</strong><b class="recording-take-duration" ${t?`data-live="${t.id}"`:''}>${t?time(position(t)):'00:00'}</b></span></div>
 <div class="main-cue"><b>${c[0]}</b><strong title="${esc(c[1])}">${esc(c[1])}</strong></div>
 <div class="original-cue-facts"><span><b>${c[2]}</b> of music</span><span>${cueSettings(s,s.cue).complexity.toLowerCase()}</span><span class="cue-planned-inline">Planned ${plannedPicker(s,s.cue,'main')}</span><span title="Cumulative work on this cue, including time between takes">Worked on cue <b data-proposal-cue-clock>${proposalDuration(timing.cueElapsed)}</b></span><span>${entryCountText(s,s.cue)}</span></div>
 <div class="proposal-action-group calm-transport" role="group" aria-label="Take controls">${recordButton(s)}<button data-action="record-overdub" ${ready||paused||t?'disabled':''}>${appIcon('music')} Overdub ${nextEntryNumber(s,s.cue,'overdub')}</button></div>
 <div class="original-secondary-actions"><div class="proposal-cue-switcher calm-cue-actions" role="group" aria-label="Cue controls"><button data-action="prev-cue" ${t||s.cue===0?'disabled':''} title="Previous cue · [">← Previous cue <kbd>[</kbd></button><button data-action="next-cue" ${t||s.cue===cues.length-1?'disabled':''} title="Next cue · ]">Next cue → <kbd>]</kbd></button>${cueJumpMenu(s)}</div><div class="proposal-action-group proposal-session-actions" role="group" aria-label="Session controls"><button data-session-action="break" ${ready||t?'disabled':''}>${appIcon('cup')}${paused?'Resume':'Break'}</button><button data-session-action="end" class="proposal-end-session" ${ready||t?'disabled':''}>End session</button><button data-session-action="reset" class="proposal-reset-session" title="Reset takes and timers" aria-label="Reset takes and timers" ${t?'disabled':''}>${appIcon('reset')}</button></div></div></div>
 <div class="proposal-session-clocks original-clock-side"><label class="original-wall-clock">Time<b data-wall-clock>${formatWallClock()}</b></label>${mainSessionTimes(timing)}${mainPlanCard(timing)}</div>
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
controls=function(){const s=state();return `<div class="calm-scroll control-scroll"><div class="sticky-slot" aria-hidden="true">${transport(s)}</div>${calmPanel(s)}${cueTimeline(s)}<div class="calm-content"><div class="proposal-cues">${proposalRatingFilter(s)}${calmCueList(s)}</div>${calmNotes(s)}</div></div>`;};
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
 const sessionSlot=document.querySelector('.proposal-session-header-slot');sessionSlot.hidden=proposalView!=='recording';sessionSlot.innerHTML=proposalView==='recording'?proposalSessionHeader(unifiedState):'';

 document.querySelector('.proposal-planning-slot').innerHTML=proposalPlanning(unifiedState);
 syncGlobalRecording();
 positionPlanningMenu();
 const bar=document.querySelector('.proposal-live-bar');
 if(bar){bar.hidden=proposalView!=='cutlist';bar.innerHTML=proposalView==='cutlist'?transport(unifiedState):'';}
 syncRecordingDock();
 if(typeof scheduleTourPosition==='function')scheduleTourPosition();
};
function syncGlobalRecording(){
 const t=running(unifiedState),badge=document.querySelector('.proposal-global-recording');document.body.classList.toggle('take-is-recording',!!t);
 document.body.style.setProperty('--review-height',document.querySelector('.site-header').getBoundingClientRect().bottom+'px');
 if(badge){badge.hidden=!t;badge.innerHTML=t?`<span>● RECORDING</span><b>${entryLabel(t)}</b><b data-live="${t.id}">${time(position(t))}</b>`:'';}
}
addEventListener('resize',syncGlobalRecording);
function showProposalView(view,{navigate=true}={}){
 cancelTakeNumberEntry();
 view=view==='cutlist'?'cutlist':'recording';
 if(view!==proposalView)unifiedState.planningOpen=false;
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
 document.querySelector('.site-header').innerHTML=`<a class="wordmark" href="#recording"><span class="brand-icon">m<span>·</span></span>MandoCues<span class="divider">/</span><span class="header-label">voorstel van Floris</span></a>${`<div class="proposal-global-recording" hidden></div>`}<div class="proposal-review-actions"><button type="button" data-proposal-action="fullscreen" aria-label="Schermvullend" title="Schermvullend">⛶</button><button type="button" data-proposal-action="tour">Rondleiding</button><button type="button" data-proposal-action="questions">Vragen</button><button type="button" data-proposal-action="prompt">Claude-prompt <span data-proposal-selection-count>0</span></button></div>`;
 document.querySelector('.site-header').insertAdjacentHTML('afterend',appSidebar());
 document.querySelector('#app').innerHTML=`<main class="proposal-shell"><header class="proposal-view-bar" lang="en"><div class="proposal-project-heading"><div class="proposal-heading-line"><h1>${appIcon('record')}<span class="proposal-workspace-title">Recording</span></h1><div class="proposal-planning-slot"></div></div><p class="proposal-project-title">After Party</p></div><nav class="proposal-view-toggle" aria-label="Workspace view"><button type="button" data-proposal-view="recording" aria-pressed="true">Recording</button><button type="button" data-proposal-view="cutlist" aria-pressed="false">Comp tool</button></nav><div class="proposal-live-bar" lang="en" hidden></div><small class="proposal-demo-label">Demo · no audio is recorded</small><div class="proposal-cutlist-review" lang="nl"></div></header><div class="proposal-session-header-slot"></div><div class="browser-frame"><div class="demo" id="demo" lang="en"></div></div></main>`;
}
route=function(){
 if(!document.querySelector('.proposal-shell'))mountProposal();
 const hash=location.hash.slice(1);showProposalView(['cutlist','partituur'].includes(hash)?'cutlist':'recording',{navigate:false});
};
document.addEventListener('change',event=>{
 const el=event.target;
 if(el.dataset.cueComplexity!==undefined){if(['Easy','Medium','Hard'].includes(el.value))cueSettings(unifiedState,+el.dataset.cueComplexity).complexity=el.value;else return;}
 else if(el.dataset.cuePlanned!==undefined){const value=Number(el.value);if(!el.value.trim()||!Number.isFinite(value)||value<1||value>1440){el.value=cuePlannedMinutes(+el.dataset.cuePlanned);return;}cueSettings(unifiedState,+el.dataset.cuePlanned).planned=value;}
 else if(el.dataset.cueComplete!==undefined)cueSettings(unifiedState,+el.dataset.cueComplete).complete=el.checked;
 else return;
 renderDemo();
});
document.addEventListener('keydown',event=>{if(event.key==='Enter'&&event.target.matches('[data-cue-planned]')&&!event.metaKey&&!event.ctrlKey&&!event.altKey&&!event.isComposing){event.preventDefault();event.target.blur();}});
document.addEventListener('click',event=>{
 const reset=event.target.closest('[data-confirm-session-reset]');if(reset){if(reset.dataset.confirmSessionReset===unifiedState.sessionId)resetProposalSession(unifiedState);return;}
 const action=event.target.closest('[data-session-action]');
 if(action){if(!action.disabled){if(action.dataset.sessionAction==='break')proposalSessionBreak(unifiedState);else if(action.dataset.sessionAction==='reset')confirmSessionReset(unifiedState);else proposalEndSession(unifiedState);}return;}
 const button=event.target.closest('[data-proposal-view]');if(!button)return;
 showProposalView(button.dataset.proposalView);
});
setInterval(()=>{
 if(!document.body.classList.contains('unified-proposal'))return;
 const timing=scoreWorkflowTiming(unifiedState);
 document.querySelectorAll('[data-proposal-plan]').forEach(el=>{el.textContent=proposalScheduleText(timing.delta);el.className='proposal-schedule '+proposalPlanClass(timing.delta);el.setAttribute('aria-label',proposalPlanLabel(timing.delta));el.title=proposalPlanLabel(timing.delta);});
 document.querySelectorAll('[data-proposal-elapsed]').forEach(el=>el.textContent=proposalDuration(timing.elapsed));
 document.querySelectorAll('[data-proposal-remaining]').forEach(el=>el.textContent=proposalDuration(timing.remaining));
 document.querySelectorAll('[data-plan-card]').forEach(el=>{el.className='main-plan-card '+proposalPlanClass(timing.delta);el.querySelector('[data-plan-status]').textContent=timing.delta===0?'On schedule':proposalScheduleText(timing.delta);});
 const panel=document.querySelector('#main-panel');if(panel){panel.classList.remove('is-late','is-behind','is-ahead','is-on-time');panel.classList.add(proposalPlanClass(timing.delta));}
 document.querySelectorAll('[data-proposal-cue-clock]').forEach(el=>el.textContent=proposalDuration(timing.cueElapsed));
 document.querySelectorAll('[data-cue-actual]').forEach(el=>{const j=+el.dataset.cueActual,seconds=cueActualSeconds(unifiedState,j);el.textContent=seconds===null?'—':proposalDuration(seconds);el.className='cue-actual '+cueActualClass(unifiedState,j,seconds);});
 document.querySelectorAll('[data-proposal-planned-end]').forEach(el=>el.textContent=proposalEndTime(timing,false));
 document.querySelectorAll('[data-proposal-projected-end]').forEach(el=>el.textContent=proposalEndTime(timing,true));
},200);
route();
