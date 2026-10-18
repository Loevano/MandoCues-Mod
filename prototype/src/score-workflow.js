// Optional score-first layout; reuses the existing take layers and score tools.
function scoreWorkflowTiming(s){
 const now=Date.now();
 const clock=s.scoreWorkflowClock??={started:now,sessionBase:42*60,remaining:140*60,booked:180*60,offset:0,cueStarted:now,cueIndex:s.cue,cueBase:s.cue===0?8*60:0,cueOffset:0,cueSpent:{}};
 const elapsed=clock.sessionBase+Math.floor((now-clock.started)/1000)+clock.offset;
 const cueElapsed=clock.cueBase+Math.floor((now-clock.cueStarted)/1000)+clock.offset-clock.cueOffset;
 const budget=cuePlannedMinutes(s.cue)*60,delta=elapsed+clock.remaining-clock.booked;
 return {clock,elapsed,cueElapsed,budget,delta};
}
function scoreWorkflowSwitchCue(s,index){
 if(!s.scoreWorkflowClock)return;
 const {clock,cueElapsed}=scoreWorkflowTiming(s);
 clock.cueSpent[s.cue]=cueElapsed;clock.cueBase=clock.cueSpent[index]||0;
 clock.cueStarted=Date.now();clock.cueIndex=index;clock.cueOffset=clock.offset;
}
function scoreWorkflowPlanText(delta){return (delta>0?'+':delta<0?'−':'')+time(Math.abs(delta))+' '+(delta>0?'behind':delta<0?'ahead':'on schedule');}
function scoreWorkflowReminder(timing){return timing.cueElapsed>timing.budget?'Cue '+time(timing.cueElapsed-timing.budget)+' over budget':'';}
function scoreWorkflowDock(s){
 const timing=scoreWorkflowTiming(s),t=running(s),selected=takeById(s,s.selected);
 return `<section class="score-session-dock" aria-label="Compact session controls"><header><span><b>${cues[s.cue][0]}</b> ${esc(cues[s.cue][1])}</span><small>${t?'● RECORDING':'STAND BY'}</small></header><div class="score-session-active"><strong>${t?entryLabel(t):selected?entryLabel(selected):'No take yet'}</strong>${t?`<b data-live="${t.id}">${time(position(t))}</b>`:''}</div>${t&&selected?.id!==t.id?`<small class="score-viewing-other">Viewing ${selected?entryLabel(selected):'no take'} · ${entryLabel(t)} keeps recording</small>`:''}<div class="score-session-actions"><button class="${t?'stop':'record'}" data-action="record">${t?'■ Stop take':'+ New take'}</button><button data-action="next-cue" ${t?'disabled':''} aria-label="Next cue">Next cue →</button></div><div class="score-session-status"><span>Cue <b data-score-cue-clock>${time(timing.cueElapsed)} / ${time(timing.budget)}</b></span><strong data-score-workflow-plan class="${timing.delta>0?'behind':'ahead'}">${scoreWorkflowPlanText(timing.delta)}</strong></div><p class="score-session-reminder" data-score-workflow-reminder role="status" ${scoreWorkflowReminder(timing)?'':'hidden'}>${scoreWorkflowReminder(timing)}</p><details class="score-session-details" data-score-session-details ${s.scoreSessionDetails?'open':''}><summary>Timing & reminder</summary><div><span>Session <b data-score-session-elapsed>${time(timing.elapsed)}</b></span><span>Remaining work <b>${time(timing.clock.remaining)}</b></span><span>Time <b data-wall-clock>${new Date().toLocaleTimeString('en-GB')}</b></span></div><button data-score-workflow-later>Try: 2 minutes later</button><small>Demo schedule · reminder when the cue runs over its budget. No audio is recorded.</small></details></section>`;
}
function scoreWorkflow(){
 const s=state();
 return `<div class="score-layout cutlist-layout score-first-layout">${scoreSidebar(s,{workflow:true})}<div class="score-first-stage"><div class="score-first-intro"><b>Work from the score?</b><p>Takes and notes on the left.<br>Compact session controls at the top right.</p></div>${scoreWorkflowDock(s)}${scoreView(s)}</div></div>`;
}
function syncScoreWorkflowClocks(){
 if(active?.id!=='partituur'||variant!=='B'||!document.querySelector('.score-session-dock'))return;
 const timing=scoreWorkflowTiming(state());
 document.querySelector('[data-score-cue-clock]').textContent=time(timing.cueElapsed)+' / '+time(timing.budget);
 const plan=document.querySelector('[data-score-workflow-plan]');plan.textContent=scoreWorkflowPlanText(timing.delta);plan.className=timing.delta>0?'behind':'ahead';
 const reminder=document.querySelector('[data-score-workflow-reminder]');reminder.textContent=scoreWorkflowReminder(timing);reminder.hidden=!reminder.textContent;
 document.querySelector('[data-score-session-elapsed]').textContent=time(timing.elapsed);
}
