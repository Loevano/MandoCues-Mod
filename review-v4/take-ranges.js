// One range control per take. Editing floats above the page, never inside its rows.
function v4Ranges(s){s.v4Ranges??={};return s.v4Ranges[s.cue]??={presets:[],pending:null};}
function v4RangeLabel(range){return range?'Bars '+range.from+'–'+range.to:'All bars';}
function v4RangeValue(range){return range?range.from+'–'+range.to:'All bars';}
function v4RangeControls(s){
 const live=running(s),range=live?.barRange??v4Ranges(s).pending;
 return `<div class="v4-take-range" aria-label="Bar range for the next take"><span>${live?'Take '+live.num:'Next take '+nextEntryNumber(s,s.cue)}</span><button type="button" class="v4-range-trigger" data-v4-range-open="next" aria-haspopup="dialog" ${live?'disabled':''}>${v4RangeValue(range)} <span aria-hidden="true">⌄</span></button></div>`;
}
const v4RangeBaseRow=calmTakeRow;
calmTakeRow=function(s,t){
 const template=document.createElement('template');template.innerHTML=v4RangeBaseRow(s,t);
 const identity=template.content.querySelector('.calm-take-identity'),name=identity.querySelector('.calm-take-name'),top=document.createElement('div');top.className='v4-take-title-line';name.replaceWith(top);top.append(name);
 top.insertAdjacentHTML('beforeend',`<button type="button" class="v4-take-range-value" data-v4-edit-take-range="${t.id}" aria-label="Edit bars for ${entryLabel(t)}" aria-haspopup="dialog" title="${entryLabel(t)} · ${v4RangeLabel(t.barRange)}">${v4RangeValue(t.barRange)} <span aria-hidden="true">⌄</span></button>`);
 return template.innerHTML;
};
const v4RangeBaseRender=renderDemo;
renderDemo=function(){v4CloseRange(false);v4RangeBaseRender();const slot=document.querySelector('.v4-range-slot');if(slot)slot.innerHTML=v4RangeControls(state());};
const v4RangeBaseToggle=toggleRecord;
toggleRecord=function(s,kind='take'){
 const before=running(s),range=structuredClone(v4Ranges(s).pending);
 v4RangeBaseToggle(s,kind);const live=running(s);if(!before&&live){live.barRange=range;renderDemo();}
};
let v4RangeEditor=null;
function v4CloseRange(restoreFocus=false){
 const editor=document.querySelector('#v4-range-popover'),anchor=v4RangeEditor?.anchor;editor?.remove();v4RangeEditor=null;if(restoreFocus&&anchor?.isConnected)anchor.focus({preventScroll:true});
}
function v4PositionRange(){
 const context=v4RangeEditor,popup=document.querySelector('#v4-range-popover');if(!context||!popup)return;
 if(!context.anchor.isConnected){v4CloseRange();return;}
 const r=context.anchor.getBoundingClientRect(),height=popup.offsetHeight,width=popup.offsetWidth;
 const below=r.bottom+7,above=r.top-height-7;
 Object.assign(popup.style,{left:Math.max(8,Math.min(innerWidth-width-8,r.left))+'px',top:Math.max(8,Math.min(innerHeight-height-8,below+height<=innerHeight-8?below:above))+'px'});
}
function v4OpenRange(anchor,takeId=null){
 v4CloseRange();const s=state();if(!takeId&&running(s))return;
 const take=takeId?takeById(s,takeId):null;if(takeId&&!take)return;
 const range=take?take.barRange:v4Ranges(s).pending,presets=v4State(s).settings.ranges==='multiple'?v4Ranges(s).presets:[];
 v4RangeEditor={anchor,takeId,cue:s.cue,session:s.sessionId};
 const popup=document.createElement('div');popup.id='v4-range-popover';popup.className='v4-range-popover';popup.lang='en';popup.setAttribute('role','dialog');popup.setAttribute('aria-labelledby','v4-range-title');
 popup.innerHTML=`<header><b id="v4-range-title">${take?entryLabel(take):'Next take '+nextEntryNumber(s,s.cue)} · Bars</b><button type="button" data-v4-range-close aria-label="Close bar range">×</button></header><form id="v4-range-form"><div class="v4-range-fields"><label>From bar<input name="from" type="number" inputmode="numeric" min="1" max="99999" value="${range?.from??''}" placeholder="Start"></label><span aria-hidden="true">–</span><label>Till bar<input name="to" type="number" inputmode="numeric" min="1" max="99999" value="${range?.to??''}" placeholder="End"></label></div><p class="v4-range-error" role="status"></p>${presets.length?`<div class="v4-range-recent"><small>Saved ranges</small>${presets.map((r,i)=>`<button type="button" data-v4-use-range="${i}">${v4RangeValue(r)}</button>`).join('')}</div>`:''}<footer><button type="button" data-v4-range-whole>All bars</button><button type="submit" class="review-primary">Apply</button></footer></form>`;
 document.body.append(popup);v4PositionRange();popup.querySelector('[name=from]').focus({preventScroll:true});
}
function v4ApplyRange(range){
 const context=v4RangeEditor,s=state();if(!context||s.cue!==context.cue||s.sessionId!==context.session)return;
 const owner=context.takeId?takeById(s,context.takeId):null;
 if(context.takeId&&!owner)return;
 if(owner)owner.barRange=structuredClone(range);else{if(running(s))return;v4Ranges(s).pending=structuredClone(range);}
 if(range&&!v4Ranges(s).presets.some(r=>r.from===range.from&&r.to===range.to))v4Ranges(s).presets.push(structuredClone(range));
 const id=context.takeId;v4CloseRange();renderDemo();
 document.querySelector(id?`[data-v4-edit-take-range="${id}"]`:'[data-v4-range-open="next"]')?.focus({preventScroll:true});
}
document.addEventListener('click',event=>{
 const trigger=event.target.closest('[data-v4-range-open],[data-v4-edit-take-range]');if(trigger&&!trigger.disabled){v4OpenRange(trigger,trigger.dataset.v4EditTakeRange||null);return;}
 if(event.target.closest('[data-v4-range-close]')){v4CloseRange(true);return;}
 if(event.target.closest('[data-v4-range-whole]')){v4ApplyRange(null);return;}
 const saved=event.target.closest('[data-v4-use-range]');if(saved){v4ApplyRange(v4Ranges(state()).presets[+saved.dataset.v4UseRange]);return;}
 if(v4RangeEditor&&!event.target.closest('#v4-range-popover'))v4CloseRange();
});
document.addEventListener('submit',event=>{
 if(event.target.id!=='v4-range-form')return;event.preventDefault();const form=event.target,data=new FormData(form),from=String(data.get('from')).trim(),to=String(data.get('to')).trim();
 if(!from&&!to){v4ApplyRange(null);return;}
 const first=Number(from),last=Number(to);
 if(!from||!to||!Number.isInteger(first)||!Number.isInteger(last)||first<1||last<first||last>99999){form.querySelector('.v4-range-error').textContent='Choose an end bar at or after the start bar.';v4PositionRange();return;}
 v4ApplyRange({from:first,to:last});
});
addEventListener('keydown',event=>{
 if(event.key==='Escape'&&v4RangeEditor){event.preventDefault();event.stopImmediatePropagation();v4CloseRange(true);}
},true);
document.addEventListener('keydown',event=>{
 if(event.code!=='KeyB'||event.metaKey||event.ctrlKey||event.altKey||event.shiftKey||event.repeat||event.isComposing||!navigationKeysAvailable(event)||running(state()))return;
 const anchor=proposalView==='recording'?document.querySelector('[data-v4-range-open="next"]'):document.querySelector(`[data-v4-edit-take-range="${state().selected}"]`);
 if(anchor){event.preventDefault();event.stopImmediatePropagation();v4OpenRange(anchor,proposalView==='recording'?null:state().selected);}
},true);
addEventListener('resize',v4PositionRange);document.addEventListener('scroll',v4PositionRange,true);
const v4RangeBaseLog=sessionTakeLog,v4RangeBaseExport=openSessionExport;
sessionTakeLog=function(s=unifiedState){const log=v4RangeBaseLog(s);for(const take of log.takes)take.barRange=structuredClone(takeById(s,take.takeId)?.barRange??null);return log;};
openSessionExport=function(kind){v4RangeBaseExport(kind);if(kind==='takes')document.querySelectorAll('.session-export-preview section').forEach((section,index)=>{const t=allTakes(state())[index];if(t)section.querySelector('b')?.insertAdjacentHTML('afterend',' · '+v4RangeLabel(t.barRange));});};
renderDemo();
