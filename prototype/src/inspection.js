// Helpers derived from visible structure only. The pasted page is never executed.
function entryLabel(t) { return (t.kind==='overdub'?'Overdub ':'Take ')+t.num; }
function nextEntryNumber(s,cue,kind='take') {
  return Math.max(0,...s.takes[cue].filter(t=>(t.kind||'take')===kind).map(t=>t.num))+1;
}
function entryCountText(s,cue,fallback=0) {
  if(!s.takes)return fallback+' takes';
  const takes=s.takes[cue].filter(t=>t.kind!=='overdub').length;
  const overdubs=s.takes[cue].filter(t=>t.kind==='overdub').length;
  return takes+' '+(takes===1?'take':'takes')+(overdubs?' · '+overdubs+' '+(overdubs===1?'overdub':'overdubs'):'');
}
function cuePlannedMinutes(j) { return [10,25,20,12,14,8,12,8,10,12,13,25][j]||10; }
function sourceCueFacts(c,j) {
  const planned=cuePlannedMinutes(j);
  return `<span class="cue-source-facts"><span><small>Music</small><b>${c[2]}</b></span><span title="Demo schedule"><small>Planned</small><b>${time(planned*60)}</b></span></span>`;
}
function sourceSessionSummary(s=null) {
  return `<div class="source-session-summary" aria-label="Demo session settings"><span>Session length <b>${s?.booked!==undefined?Math.floor(s.booked/60)+'h '+String(s.booked%60).padStart(2,'0'):'6h 00'}</b></span><span>Preparation <b>${s?.prepMinutes??3} min/cue</b></span><span>Max. music length <b>${s?.maxMusicMinutes??60} min</b></span></div>`;
}
function sourceCuePlan(s) {
  return `<section class="source-cue-plan" aria-label="Session plan with complete cue codes"><div><b>Session plan</b><small>Demo · click to choose a cue</small></div><nav aria-label="Cue order">${cues.map((c,j)=>`<button data-session-cue="${j}" aria-label="Choose ${c[0]} ${esc(c[1])}" aria-current="${s.cue===j?'true':'false'}" title="${esc(c[1])}">${c[0]}</button>`).join('')}</nav></section>`;
}
