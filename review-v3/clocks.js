// Display preferences affect the session clock only; note and take timestamps stay intact.
sessionReview.clocks={primary:'local',secondary:'',elapsed:true,remaining:true,planned:true,projected:true};
const reviewTimeZones=[['local','Local time'],['UTC','UTC'],['America/Los_Angeles','Los Angeles'],['Europe/Amsterdam','Amsterdam']];
function reviewZoneClock(zone){return new Date().toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:true,...(zone&&zone!=='local'?{timeZone:zone}:{})});}
formatWallClock=function(){return reviewZoneClock(sessionReview.clocks.primary);};
function reviewClockSettings(){
 const c=sessionReview.clocks;
 return `<div class="v3-clock-options"><label>Main clock<select data-review-clock-zone="primary">${reviewTimeZones.map(([value,label])=>`<option value="${value}" ${c.primary===value?'selected':''}>${label}</option>`).join('')}<option disabled>Project timecode — not connected</option></select></label><label>Second clock<select data-review-clock-zone="secondary"><option value="">Off</option>${reviewTimeZones.map(([value,label])=>`<option value="${value}" ${c.secondary===value?'selected':''}>${label}</option>`).join('')}</select></label><fieldset><legend>Show session times</legend>${[['elapsed','Elapsed (working)'],['remaining','Remaining'],['planned','Planned end'],['projected','Projected end']].map(([key,label])=>`<label><input type="checkbox" data-review-clock-toggle="${key}" ${c[key]?'checked':''}>${label}</label>`).join('')}</fieldset></div>`;
}
function reviewApplyClocks(){
 const c=sessionReview.clocks;
 for(const [key,selector] of [['elapsed','[data-proposal-elapsed]'],['remaining','[data-proposal-remaining]'],['planned','[data-proposal-planned-end]'],['projected','[data-proposal-projected-end]']])document.querySelectorAll('#main-panel '+selector).forEach(el=>el.closest('label').hidden=!c[key]);
 document.querySelectorAll('.v3-secondary-clock').forEach(el=>el.remove());
 const label=reviewTimeZones.find(([z])=>z===c.primary)?.[1]||'Local time';
 document.querySelectorAll('[data-wall-clock]').forEach(el=>el.title=label);
 const heading=document.querySelector('.original-wall-clock');if(heading?.firstChild?.nodeType===Node.TEXT_NODE)heading.firstChild.textContent='Time · '+label;
 if(c.secondary)document.querySelector('.original-wall-clock')?.insertAdjacentHTML('beforeend',`<small class="v3-secondary-clock"><span>${reviewTimeZones.find(([z])=>z===c.secondary)?.[1]}</span> <b data-review-world-clock>${reviewZoneClock(c.secondary)}</b></small>`);
}
reviewUpdates.push(()=>{
 reviewApplyClocks();
 if(sessionReview.feature!=='clocks'||proposalView!=='recording')return;
 const html=reviewVariant('clocks')==='A'?`<details class="v3-clock-settings"><summary>Clock display</summary>${reviewClockSettings()}</details>`:`<section class="v3-feature-panel v3-inline-clock-settings" aria-label="Clock display"><header><b>Clock display</b><small>Display preferences only</small></header>${reviewClockSettings()}</section>`;
 document.querySelector('.v3-control-column')?.insertAdjacentHTML('afterbegin',html);
});
document.addEventListener('change',e=>{
 const key=e.target.dataset.reviewClockToggle,zone=e.target.dataset.reviewClockZone;
 if(key&&key in sessionReview.clocks)sessionReview.clocks[key]=e.target.checked;
 else if(zone&&['primary','secondary'].includes(zone))sessionReview.clocks[zone]=e.target.value;
 else return;
 reviewApplyClocks();document.querySelectorAll('[data-wall-clock]').forEach(el=>el.textContent=formatWallClock());
});
setInterval(()=>document.querySelectorAll('[data-review-world-clock]').forEach(el=>el.textContent=reviewZoneClock(sessionReview.clocks.secondary)),200);
