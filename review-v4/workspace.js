// v4 keeps the existing transport, cue identity and note state, with planning first.
const v4OriginalTiming=scoreWorkflowTiming,v4OriginalCueMinutes=cuePlannedMinutes;
const v4BaseRender=renderDemo,v4BaseSelectCue=selectCue,v4BaseTransport=transport;
function v4Seconds(value){
 const match=String(value).trim().match(/^(\d{1,4}):([0-5]\d)$/);
 return match?Number(match[1])*60+Number(match[2]):null;
}
function v4Duration(n){return time(Math.max(0,Math.round(n)));}
function v4State(s){
 if(s.v4)return s.v4;
 const prep=(s.prepMinutes??3)*60;
 const rows=cues.map((cue,j)=>({id:j,musicSeconds:v4Seconds(cue[2])??0,complexity:s.cueSettings?.[j]?.complexity??'Medium',workCorrection:0,include:true,budget:null,remaining:null}));
 const rate=V4Planning.initialRate(rows,s.booked*60,prep);
 s.v4={rows,rate,prep,initialBooked:s.booked,settings:{timing:'focus',allocation:'adaptive',workload:'cue',ranges:'single',learning:'completed'},corrections:[],ready:false};
 const initial=V4Planning.forecast(rows,{rate,prepSeconds:prep,availableSeconds:s.booked*60});
 for(const row of rows)row.budget=initial.rows[row.id].suggestedBudget;
 return s.v4;
}
function v4Row(s,j){const v=v4State(s);while(v.rows.length<cues.length){const k=v.rows.length;v.rows.push({id:k,musicSeconds:v4Seconds(cues[k][2])??0,workCorrection:0,include:true,budget:0,remaining:null});}return v.rows[j];}
function v4Forecast(s,raw=v4OriginalTiming(s)){
 const v=v4State(s),now=Date.now(),clock=raw.clock;
 const wallNow=s.sessionEnded?(v.endedAt??now):now;
 // Use the same second phase as the work clocks, including for deadline time.
 const available=s.sessionStarted||s.sessionEnded||clock.fixedEndAt?Math.round((clock.plannedEndAt-clock.started)/1000)-Math.floor((wallNow-clock.started)/1000):s.booked*60;
 const inputs=cues.map((cue,j)=>{
  const row=v4Row(s,j),measured=j===s.cue?raw.cueElapsed:clock.cueSpent[j]??0;
  const worked=Math.max(0,measured+row.workCorrection);
  return {id:j,musicSeconds:row.musicSeconds,complexity:s.cueSettings?.[j]?.complexity??'Medium',workedSeconds:worked,done:!!s.cueSettings?.[j]?.complete,include:row.include&&v.settings.learning!=='fixed',remainingOverride:row.remaining?Math.max(0,row.remaining.seconds-(worked-row.remaining.workedAt)):null};
 });
 const prediction=V4Planning.forecast(inputs,{rate:v.rate,prepSeconds:(s.prepMinutes??3)*60,availableSeconds:available});
 const current=prediction.rows[s.cue],cueBudget=v4Row(s,s.cue).budget??current.suggestedBudget;
 return {...prediction,available,raw,current,cueBudget,cueLeft:cueBudget-current.workedSeconds,projectedAt:wallNow+prediction.remaining*1000};
}
function v4Rebalance(s,{rebase=false}={}){
 const v=v4State(s);
 if(rebase&&!s.sessionStarted&&!s.sessionEnded){v.rate=V4Planning.initialRate(v.rows.map((row,j)=>({...row,complexity:cueSettings(s,j).complexity})),s.booked*60,(s.prepMinutes??3)*60);}
 const p=v4Forecast(s);
 for(const row of p.rows){const config=v4Row(s,row.id);if(!config.manualBudget)config.budget=row.workedSeconds+row.suggestedBudget;}
}
scoreWorkflowTiming=function(s){const raw=v4OriginalTiming(s);if(!s.unified||!s.v4)return raw;const p=v4Forecast(s,raw);return {...raw,delta:p.delta,remaining:Math.max(0,p.available)};};
cuePlannedMinutes=function(j){const s=cuePlanningState;if(s?.v4){const b=v4Row(s,j).budget;return Math.max(0,(b??0)/60);}return v4OriginalCueMinutes(j);};
function v4CueTiming(s){
 const p=v4Forecast(s),done=p.current.done,left=p.cueLeft;
 return `<div class="v4-cue-countdown ${left<0?'is-over':''}"><span>${done?'Cue complete':left<0?'Over cue budget':'Available for this cue'}</span><strong data-v4-cue-left>${done?'Done':(left<0?'−':'')+v4Duration(Math.abs(left))}</strong><small data-v4-estimate>Estimated work left: ${v4Duration(p.current.remaining)}</small></div>`;
}
function v4SessionTiming(s){
 const p=v4Forecast(s),status=proposalPlanClass(p.delta);
 return `<div class="v4-session-forecast ${status}"><span>Session forecast</span><strong data-v4-forecast>${p.delta>0?'−'+v4Duration(p.delta):p.delta<0?'+'+v4Duration(-p.delta):'On schedule'}</strong><small data-v4-forecast-label>${p.delta>0?'Expected overrun':p.delta<0?'Expected spare time':'At the planned end'}</small><div class="v4-forecast-foot"><span>Finish by <b data-v4-finish>${proposalClockTime(p.raw.clock.plannedEndAt)}</b></span><span>Estimate <b data-v4-projected>${proposalClockTime(p.projectedAt)}</b></span></div><small data-v4-learning>${p.samples?'Based on '+p.samples+' completed '+(p.samples===1?'cue':'cues'):'Initial estimate · no completed cues yet'}</small></div>`;
}
function v4TimingDetails(s){const t=v4Forecast(s);return `<details class="v4-timing-details" ${v4State(s).settings.timing==='details'?'open':''}><summary>Timing details</summary><div><span>Session left <b data-v4-session-left>${v4Duration(t.available)}</b></span><span>Worked on cue <b data-v4-worked>${v4Duration(t.current.workedSeconds)}</b></span><span>Remaining work <b data-v4-total-work>${v4Duration(t.remaining)}</b></span><span>Time <b data-wall-clock>${formatWallClock()}</b></span></div></details>`;}
calmPanel=function(s){
 const t=running(s),ready=!s.sessionStarted,paused=!!s.sessionPausedAt,c=cues[s.cue];
 const status=t?'● Recording':paused?'On break':s.sessionEnded?'Session ended':ready?'Ready to start':'Standby';
 return `<section id="main-panel" class="v4-main-panel ${t?'is-recording':''}" aria-label="Recording and planning"><div class="v4-main-content"><div class="main-take-heading"><span class="rec-status ${t?'rolling':'standby'}">${status}</span><span class="v4-live-take" ${t?'':'aria-hidden="true"'}>${t?`<b>${entryLabel(t)}</b><b data-live="${t.id}">${time(position(t))}</b>`:'<b>Take 1</b><b>00:00</b>'}</span></div><div class="main-cue"><b>${c[0]}</b><strong>${esc(c[1])}</strong></div><div class="v4-cue-facts"><span>${v4Duration(v4Row(s,s.cue).musicSeconds)} to record</span><span>${cueSettings(s,s.cue).complexity}</span><button data-v4-edit-cue="${s.cue}">Edit cue timing</button></div><div class="v4-record-actions">${recordButton(s)}<button data-action="record-overdub" ${ready||paused||t?'disabled':''}>Overdub ${nextEntryNumber(s,s.cue,'overdub')}</button></div><div class="v4-range-slot"></div><div class="v4-cue-actions"><button data-action="prev-cue" ${t?'disabled':''}>← Previous <kbd>[</kbd></button><button data-action="next-cue" ${t?'disabled':''}>Next → <kbd>]</kbd></button>${cueJumpMenu(s)}<button data-v4-done-next ${t?'disabled':''}>${cueSettings(s,s.cue).complete?'Reopen cue':'Done & next'}</button></div></div><aside class="v4-status-area">${v4CueTiming(s)}${v4SessionTiming(s)}</aside><footer class="v4-main-footer">${v4TimingDetails(s)}<div class="v4-session-actions"><button data-session-action="break" ${ready||t?'disabled':''}>${paused?'Resume':'Break'}</button><button data-session-action="end" ${ready||t?'disabled':''}>End session</button><button data-session-action="reset" ${t?'disabled':''} aria-label="Reset takes and timers">${appIcon('reset')}</button></div></footer></section>`;
};
transport=function(s){const template=document.createElement('template');template.innerHTML=v4BaseTransport(s);const clock=template.content.querySelector('.transport-clocks');if(clock){const p=v4Forecast(s);clock.innerHTML=`<label>Cue left <b data-v4-compact-cue>${(p.cueLeft<0?'−':'')+v4Duration(Math.abs(p.cueLeft))}</b></label><span class="proposal-schedule ${proposalPlanClass(p.delta)}" data-proposal-plan>${proposalScheduleText(p.delta)}</span>`;}return template.innerHTML;};
calmCueList=function(s){
 const p=v4Forecast(s);
 return `<div class="calm-cue-list grouped-list"><div class="v4-list-head"><span>Cue / Title</span><span>To record</span><span>Complexity</span><span>Budget</span><span>Worked</span><span>Done</span></div>${cues.map((c,j)=>{
  const row=p.rows[j],settings=cueSettings(s,j),conf=v4Row(s,j);
  return `<section class="cue-group ${j===s.cue?'current':''} ${settings.complete?'is-complete':''}"><div class="v4-cue-heading"><div class="v4-cue-name"><button data-open-cue="${j}" aria-expanded="${s.open.has(j)}" aria-label="Show takes for ${c[0]}">${s.open.has(j)?'⌄':'›'}</button><button data-select-cue="${j}" aria-current="${s.cue===j}"><b>${c[0]}</b><span>${esc(c[1])}</span><small>${entryCountText(s,j)} · Alts: ${cueAltKeys(s,j).length}</small></button></div><button data-v4-edit-cue="${j}" class="v4-music-duration" aria-label="Edit music to record for ${c[0]}">${v4Duration(conf.musicSeconds)}</button><select data-cue-complexity="${j}" aria-label="Complexity for ${c[0]}">${['Easy','Medium','Hard'].map(x=>`<option ${settings.complexity===x?'selected':''}>${x}</option>`).join('')}</select><button data-v4-edit-cue="${j}" aria-label="Edit budget for ${c[0]}">${v4Duration(conf.budget)}</button><button data-v4-edit-cue="${j}" class="v4-worked" data-v4-cue-worked="${j}" aria-label="Correct worked time for ${c[0]}">${v4Duration(row.workedSeconds)}</button><input type="checkbox" data-cue-complete="${j}" aria-label="Mark ${c[0]} complete" ${settings.complete?'checked':''}></div><div class="calm-cue-takes" ${s.open.has(j)?'':'hidden'}>${s.takes[j].map(t=>calmTakeRow(s,t)).join('')||'<p class="notes-empty">No takes yet</p>'}</div></section>`;
 }).join('')}</div>`;
};
function v4EditCue(j){
 const s=state(),p=v4Forecast(s),c=v4Row(s,j),row=p.rows[j];
 appDialog(cues[j][0]+' · Cue timing',`<form id="v4-cue-timing"><input type="hidden" name="cue" value="${j}"><label>Music to record (mm:ss)<input name="music" value="${v4Duration(c.musicSeconds)}" required pattern="[0-9]+:[0-5][0-9]"></label><label>Cue budget (mm:ss)<input name="budget" value="${v4Duration(c.budget)}" required pattern="[0-9]+:[0-5][0-9]"></label><label>Worked on cue (mm:ss)<input name="worked" value="${v4Duration(row.workedSeconds)}" required pattern="[0-9]+:[0-5][0-9]"></label><label>Estimated work left (mm:ss)<input name="remaining" value="${c.remaining?v4Duration(row.remaining):''}" placeholder="Auto · ${v4Duration(row.remaining)}" pattern="[0-9]+:[0-5][0-9]"></label><label class="v4-check"><input type="checkbox" name="include" ${c.include?'checked':''}> Use this cue to learn the work pace when complete</label><p class="review-muted">Worked time includes work between takes. Correct it here if a cue switch was missed. Auto estimates keep a small finishing allowance until you mark the cue done.</p><div class="v4-correction-history">${v4State(s).corrections.filter(x=>x.cue===j).slice(-3).map(x=>`<small>Worked time corrected: ${v4Duration(x.from)} → ${v4Duration(x.to)}</small>`).join('')}</div></form>`,`<button data-v4-auto-cue="${j}">Use suggested budget</button><button type="submit" form="v4-cue-timing" class="review-primary">Save</button>`);
}
document.addEventListener('submit',event=>{
 if(event.target.id!=='v4-cue-timing')return;event.preventDefault();const form=event.target,data=new FormData(form),s=state(),j=Number(data.get('cue')),row=v4Row(s,j),p=v4Forecast(s),worked=p.rows[j].workedSeconds;
 const music=v4Seconds(data.get('music')),budget=v4Seconds(data.get('budget')),actual=v4Seconds(data.get('worked')),remaining=String(data.get('remaining')).trim();
 if(music===null||budget===null||actual===null||remaining&&v4Seconds(remaining)===null)return;
 row.musicSeconds=music;
 if(Math.abs(budget-row.budget)>1){row.budget=budget;row.manualBudget=true;}
 if(Math.abs(actual-worked)>=1){v4State(s).corrections.push({cue:j,at:new Date().toISOString(),from:worked,to:actual});row.workCorrection+=actual-worked;}
 row.include=data.get('include')==='on';row.remaining=remaining?{seconds:v4Seconds(remaining),workedAt:actual}:null;
 form.closest('dialog').close();v4Rebalance(s,{rebase:!s.sessionStarted});renderDemo();
});
document.addEventListener('click',event=>{
 const edit=event.target.closest('[data-v4-edit-cue]');if(edit){v4EditCue(+edit.dataset.v4EditCue);return;}
 const auto=event.target.closest('[data-v4-auto-cue]');if(auto){const s=state(),j=+auto.dataset.v4AutoCue;v4Row(s,j).manualBudget=false;auto.closest('dialog').close();v4Rebalance(s);renderDemo();return;}
 if(event.target.closest('[data-v4-done-next]')){
  const s=state();if(running(s))return;const setting=cueSettings(s,s.cue);setting.complete=!setting.complete;
  v4Rebalance(s);if(setting.complete){const next=reviewRecordingOrder(s).find(j=>!cueSettings(s,j).complete);if(next!==undefined){selectCue(s,next);return;}}renderDemo();
 }
});
document.addEventListener('change',event=>{
 const el=event.target,s=state();
 if(el.dataset.cueComplete!==undefined){event.stopImmediatePropagation();cueSettings(s,+el.dataset.cueComplete).complete=el.checked;v4Rebalance(s);renderDemo();}
 if(el.dataset.cueComplexity!==undefined){event.stopImmediatePropagation();cueSettings(s,+el.dataset.cueComplexity).complexity=el.value;v4Rebalance(s,{rebase:!s.sessionStarted});renderDemo();}
},true);
selectCue=function(s,j){if(j===s.cue)return;v4BaseSelectCue(s,j);if(s.cue===j){v4Rebalance(s);renderDemo();}};
const v4BaseSetBudget=setProposalBudget;
setProposalBudget=function(s,minutes){v4BaseSetBudget(s,Math.max(15,Math.min(1440,minutes)));v4Rebalance(s,{rebase:!s.sessionStarted&&!s.sessionEnded});v4Sync();};
const v4BasePlanning=proposalPlanning;
proposalPlanning=function(s){return v4BasePlanning(s).replace('</div></div></details>','</div><div class="planning-extend"><span>Bring end forward</span>'+[15,30,60].map(n=>`<button type="button" data-v4-shorten="${n}">−${n} min</button>`).join('')+'</div></div></details>');};
document.addEventListener('click',event=>{const b=event.target.closest('[data-v4-shorten]');if(b){const s=state();setProposalBudget(s,s.booked-Number(b.dataset.v4Shorten));s.scoreWorkflowClock.fixedEndAt=s.scoreWorkflowClock.plannedEndAt;}});
function v4Sync(){
 if(!state().v4)return;const s=state(),p=v4Forecast(s),set=(selector,value)=>document.querySelectorAll(selector).forEach(el=>{if(el.textContent!==value)el.textContent=value;});
 set('[data-v4-cue-left]',p.current.done?'Done':(p.cueLeft<0?'−':'')+v4Duration(Math.abs(p.cueLeft)));
 set('[data-v4-estimate]','Estimated work left: '+v4Duration(p.current.remaining));
 set('[data-v4-forecast]',p.delta>0?'−'+v4Duration(p.delta):p.delta<0?'+'+v4Duration(-p.delta):'On schedule');
 set('[data-v4-forecast-label]',p.delta>0?'Expected overrun':p.delta<0?'Expected spare time':'At the planned end');
 set('[data-v4-projected]',proposalClockTime(p.projectedAt));set('[data-v4-finish]',proposalClockTime(p.raw.clock.plannedEndAt));
 set('[data-v4-learning]',p.samples?'Based on '+p.samples+' completed '+(p.samples===1?'cue':'cues'):'Initial estimate · no completed cues yet');
 set('[data-v4-compact-cue]',(p.cueLeft<0?'−':'')+v4Duration(Math.abs(p.cueLeft)));
 set('[data-v4-session-left]',v4Duration(p.available));set('[data-v4-worked]',v4Duration(p.current.workedSeconds));set('[data-v4-total-work]',v4Duration(p.remaining));
 for(const row of p.rows)set(`[data-v4-cue-worked="${row.id}"]`,v4Duration(row.workedSeconds));
 document.querySelectorAll('.v4-session-forecast').forEach(el=>el.className='v4-session-forecast '+proposalPlanClass(p.delta));
 document.querySelectorAll('.v4-cue-countdown').forEach(el=>el.classList.toggle('is-over',p.cueLeft<0));
}
renderDemo=function(){
 const s=state();v4State(s);v4BaseRender();
 document.body.classList.add('v4-workspace');document.title='MandoCues · v4 · Session planning';
 document.querySelector('.proposal-version').textContent='v4';document.querySelector('.proposal-version').setAttribute('aria-label','Version 4');
 if(proposalView==='recording'){
  const layout=document.querySelector('.calm-content');layout?.classList.add('v4-recording-content');
  const filter=document.querySelector('.review-filter');if(filter&&!filter.querySelector('.v4-model-link'))filter.insertAdjacentHTML('beforeend','<button class="v4-model-link" data-v4-model>How this estimate works</button>');
 }
 v4Sync();
};
const v4BaseEndSession=proposalEndSession,v4BaseReset=resetProposalSession;
proposalEndSession=function(s){v4State(s).endedAt=Date.now();v4BaseEndSession(s);};
resetProposalSession=function(s){const ok=v4BaseReset(s);if(ok){delete s.v4;v4State(s);renderDemo();}return ok;};
document.addEventListener('click',event=>{if(event.target.closest('[data-v4-model]'))appDialog('How this estimate works',`<p>Music to record × complexity gives each cue a workload. Session length and preparation time provide the initial work pace.</p><p>Completed cues compare actual work with that workload. The estimate changes gradually; one unusual cue cannot reset the whole session. Use Cue timing to correct a missed cue switch or exclude technical delays from learning.</p><p>The cue budget is the time available. Estimated work is what remains to be done. Unfinished cues keep a finishing allowance until Done, or until you enter a remaining estimate.</p><p>This is a prototype model to test in a session. It does not know the musical progress or follow Pro Tools.</p>`);});
setInterval(v4Sync,200);
v4State(state());renderDemo();
