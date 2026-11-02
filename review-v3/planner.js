// Explicit replan preview. No change reaches cue budgets until Apply is clicked.
function reviewPlannerState(s){
 if(!s.reviewPlanner)s.reviewPlanner={finish:formatLocalClock(Date.now()+90*60000,false),breakMinutes:10,bufferMinutes:5,prepMinutes:0,locks:{},message:''};
 return s.reviewPlanner;
}
function reviewSpent(s,j){const timing=scoreWorkflowTiming(s);return j===s.cue?timing.cueElapsed:timing.clock.cueSpent[j]||0;}
function reviewAllocate(seconds,rows){
 if(!rows.length)return [];
 const weight=rows.reduce((sum,r)=>sum+r.weight,0),raw=rows.map(r=>seconds*(weight?r.weight/weight:1/rows.length)),out=raw.map(Math.floor);
 const remaining=seconds-out.reduce((a,b)=>a+b,0),rank=raw.map((v,i)=>({i,f:v-out[i]})).sort((a,b)=>b.f-a.f||a.i-b.i);
 for(let i=0;i<remaining;i++)out[rank[i%rank.length].i]++;
 return out;
}
function reviewPlanPreview(s,variant=reviewVariant('planning')){
 const config=reviewPlannerState(s),clock=parseLocalClock(config.finish);
 if(!clock)return {error:'Use an end time such as 06:00 PM.'};
 const now=Date.now(),end=new Date(now);end.setHours(clock.hours,clock.minutes,0,0);if(end.getTime()<=now)end.setDate(end.getDate()+1);
 const available=Math.floor((end.getTime()-now)/1000),reserved=Math.round((config.breakMinutes+config.bufferMinutes)*60);
 const rows=cues.map((cue,j)=>({j,cue,spent:reviewSpent(s,j),weight:(()=>{const [m,sec]=cue[2].split(':').map(Number);return (m*60+sec)*({Easy:.7,Medium:1,Hard:1.5}[cueSettings(s,j).complexity]||1);})(),locked:variant==='B'&&!!config.locks[j]})).filter(r=>!cueSettings(s,r.j).complete);
 const prep=Math.round(config.prepMinutes*60),fixed=rows.filter(r=>r.locked).reduce((sum,r)=>sum+Math.max(0,Math.round(cuePlannedMinutes(r.j)*60-r.spent)),0);
 const flexible=rows.filter(r=>!r.locked),musicBudget=available-reserved-fixed-flexible.length*prep;
 if(musicBudget<0)return {error:'Not enough time for the fixed budgets, preparation and reserved break/buffer.',rows,endAt:end.getTime(),available,reserved};
 if(!flexible.length&&musicBudget>0)return {error:'All remaining budgets are fixed. Unlock a cue to distribute the available time.',rows,endAt:end.getTime(),available,reserved};
 if(!rows.length)return {error:'All cues are done. There is no remaining work to redistribute.',rows,endAt:end.getTime(),available,reserved};
 const shares=reviewAllocate(musicBudget,flexible);let k=0;
 for(const row of rows)row.remaining=row.locked?Math.max(0,Math.round(cuePlannedMinutes(row.j)*60-row.spent)):prep+shares[k++];
 return {rows,endAt:end.getTime(),available,reserved,total:rows.reduce((sum,r)=>sum+r.remaining,0),musicBudget};
}
function reviewPlannerPanel(s){
 const config=reviewPlannerState(s),preview=reviewPlanPreview(s),variant=reviewVariant('planning');
 return `<section class="v3-feature-panel v3-planner" aria-label="Replan remaining cues"><header><div><b>Replan remaining cues</b><small>${variant==='A'?'Redistribute all unfinished cues':'Keep selected budgets fixed'}</small></div><button data-review-plan-unlock ${variant==='A'?'hidden':''}>Unlock all</button></header><div class="v3-plan-inputs"><label>Finish by<input type="text" data-review-plan-field="finish" value="${esc(config.finish)}" placeholder="06:00 PM"></label><label>Upcoming break (min)<input type="number" min="0" max="180" data-review-plan-field="breakMinutes" value="${config.breakMinutes}"></label><label>Buffer (min)<input type="number" min="0" max="180" data-review-plan-field="bufferMinutes" value="${config.bufferMinutes}"></label><label>Prep per remaining cue (min)<input type="number" min="0" max="60" step="0.5" data-review-plan-field="prepMinutes" value="${config.prepMinutes}"></label></div><div class="v3-plan-table-wrap"><table><thead><tr><th>Cue</th><th>Music</th><th>Complexity</th><th>Current remaining</th><th>New remaining</th>${variant==='B'?'<th>Keep budget</th>':''}</tr></thead><tbody>${(preview.rows||[]).map(r=>`<tr><td>${r.cue[0]} <small>${esc(r.cue[1])}</small></td><td>${r.cue[2]}</td><td>${cueSettings(s,r.j).complexity}</td><td>${time(Math.max(0,cuePlannedMinutes(r.j)*60-r.spent))}</td><td>${r.remaining===undefined?'—':time(r.remaining)}</td>${variant==='B'?`<td><input type="checkbox" data-review-plan-lock="${r.j}" ${r.locked?'checked':''} aria-label="Keep remaining budget for ${r.cue[0]}"></td>`:''}</tr>`).join('')}</tbody></table></div><footer><p class="${preview.error?'v3-field-error':'v3-plan-total'}" role="status">${preview.error||time(preview.total)+' for cues + '+time(preview.reserved)+' break/buffer = '+time(preview.available)+' until '+formatLocalClock(preview.endAt,false)}</p><button data-review-plan-apply ${preview.error?'disabled':''}>Apply to this demo</button></footer>${config.message?`<p role="status">${esc(config.message)}</p>`:''}<small>Preview only until Apply. Music duration × complexity; completed cues stay unchanged.</small></section>`;
}
function reviewApplyPlan(){
 const invalid=[...document.querySelectorAll('.v3-plan-inputs input')].find(el=>!el.checkValidity());if(invalid){invalid.reportValidity();return;}
 const s=state(),preview=reviewPlanPreview(s);if(preview.error)return;
 if(running(s)){toast('Stop the take before applying a new plan.');return;}
 const config=reviewPlannerState(s),timing=scoreWorkflowTiming(s),clock=timing.clock;
 for(const row of preview.rows)cueSettings(s,row.j).planned=(row.spent+row.remaining)/60;
 // Keep already-spent work. Planned end is fixed; reserve future break and buffer separately.
 const pastBreak=(clock.breakSeconds||0)+(s.sessionPausedAt?Math.floor((Date.now()-s.sessionPausedAt)/1000):0);
 clock.booked=timing.elapsed+pastBreak+preview.available;clock.plannedEndAt=preview.endAt;clock.fixedEndAt=preview.endAt;
 s.booked=Math.ceil(clock.booked/60);
 s.reviewReserve={breakSeconds:Math.round(config.breakMinutes*60),bufferSeconds:Math.round(config.bufferMinutes*60),pastBreak};
 config.message='Plan applied to this demo. Completed cues and previous take data were kept.';renderDemo();
}
const reviewBaseTiming=scoreWorkflowTiming;
scoreWorkflowTiming=function(s){
 const timing=reviewBaseTiming(s),reserve=s.reviewReserve;if(!reserve)return timing;
 const used=(timing.clock.breakSeconds||0)+(s.sessionPausedAt?Math.floor((Date.now()-s.sessionPausedAt)/1000):0)-reserve.pastBreak;
 timing.delta+=Math.max(0,reserve.breakSeconds-Math.max(0,used))+reserve.bufferSeconds;
 return timing;
};
reviewUpdates.push(()=>{document.querySelectorAll('.v3-planner').forEach(el=>el.remove());if(sessionReview.feature==='planning'&&proposalView==='recording')document.querySelector('.v3-review-caption')?.insertAdjacentHTML('afterend',reviewPlannerPanel(state()));});
document.addEventListener('change',e=>{
 const root=e.target.closest('.v3-planner');if(!root)return;
 const config=reviewPlannerState(state()),key=e.target.dataset.reviewPlanField;
 if(key){const val=key==='finish'?e.target.value:+e.target.value;if(key!=='finish'&&(!Number.isFinite(val)||val<0||!e.target.checkValidity())){e.target.reportValidity();return;}config[key]=val;config.message='';renderDemo();}
 if(e.target.dataset.reviewPlanLock!==undefined){config.locks[e.target.dataset.reviewPlanLock]=e.target.checked;renderDemo();}
});
document.addEventListener('click',e=>{if(e.target.closest('[data-review-plan-apply]'))reviewApplyPlan();if(e.target.closest('[data-review-plan-unlock]')){reviewPlannerState(state()).locks={};renderDemo();}});
