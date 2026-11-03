// Small presentation update on the preserved layout; no new planning behavior.
discussion.splice(0,discussion.length,...discussion.filter(item=>item.small),...activeProposalQuestions);
const removedTransportStep=proposalTourSteps.find(step=>step.id==='opnametoets');
if(removedTransportStep){
 proposalTourSteps.splice(proposalTourSteps.indexOf(removedTransportStep),1);
 proposalTourSelection.delete('opnametoets');
 proposalTourSuggestions.splice(0,proposalTourSuggestions.length,...proposalTourSteps.filter(step=>!step.transition));
 proposalTourParts.splice(0,proposalTourParts.length,...proposalTourSteps.flatMap(step=>step.parts));
}
const proposalVersionBadge=document.createElement('span');proposalVersionBadge.className='proposal-version';proposalVersionBadge.textContent='v'+activeProposalMeta.version;proposalVersionBadge.title=activeProposalMeta.date;proposalVersionBadge.setAttribute('aria-label','Version '+activeProposalMeta.version);
document.querySelector('.site-header .wordmark').append(proposalVersionBadge);
document.title='MandoCues · voorstel van Floris · v'+activeProposalMeta.version;
const minimalBaseRender=renderDemo,minimalRecordButton=recordButton;
recordButton=function(s){return minimalRecordButton(s).replace('<kbd>⌘ Enter</kbd>','<kbd>Space</kbd>');};
document.addEventListener('keydown',event=>{
 if(event.key==='Enter'&&event.metaKey&&!event.altKey&&!event.ctrlKey&&!event.shiftKey){event.preventDefault();event.stopImmediatePropagation();return;}
 if(event.code!=='Space'||event.altKey||event.metaKey||event.ctrlKey||event.shiftKey||event.isComposing)return;
 if(event.target.closest('input,textarea,select,[contenteditable]:not([contenteditable="false"]),dialog,[role="dialog"],[data-review-drag-cue],.proposal-review-actions,.proposal-tour-card,.proposal-review-dialog')||document.querySelector('dialog[open]')||state().scoreComment||reviewCueDrag)return;
 event.preventDefault();event.stopImmediatePropagation();if(!event.repeat)performRecordingAction(state());
},true);
function reviewRecordingOrder(s){
 s.reviewOrder??=[];const valid=new Set(cues.map((_,j)=>j));s.reviewOrder=s.reviewOrder.filter(j=>valid.delete(j));s.reviewOrder.push(...valid);return s.reviewOrder;
}
function reviewVisibleOrder(s){return s.reviewOrderSort==='cue'?cues.map((_,j)=>j).sort((a,b)=>cues[a][0].localeCompare(cues[b][0],undefined,{numeric:true})):reviewRecordingOrder(s);}
function reviewMoveCue(j,target){
 const s=state();if(running(s)||s.reviewOrderSort==='cue'){toast('Use recording order with no take running to reorder cues.');return;}
 const order=reviewRecordingOrder(s),from=order.indexOf(j),to=typeof target==='object'?(target.end?order.length-1:order.indexOf(target.before)):Math.max(0,Math.min(order.length-1,from+target));
 if(from<0||to<0||from===to)return;order.splice(from,1);order.splice(typeof target==='object'?(target.end?order.length:order.indexOf(target.before)):to,0,j);renderDemo();
}
const reviewOriginalTimeline=cueTimeline;
cueTimeline=function(s){
 const output=reviewOriginalTimeline(s),template=document.createElement('template');template.innerHTML=output;
 const track=template.content.querySelector('.cue-timeline-track');if(track){
  const nodes=[...track.children];
  for(const j of reviewRecordingOrder(s)){
   const button=nodes[j];button.dataset.reviewTimelineCue=String(j);button.dataset.reviewCueKey=String(j);
   button.draggable=false;button.title+=' · Drag to reorder';track.append(button);
  }
 }
 return template.innerHTML;
};
stepCue=function(s,direction){const order=reviewRecordingOrder(s),at=order.indexOf(s.cue),next=at+direction;if(next>=0&&next<order.length)selectCue(s,order[next]);};
renderDemo=function(){
 minimalBaseRender();
 if(proposalView!=='recording')return;
 const s=state(),list=document.querySelector('.calm-cue-list');if(!list)return;
 const nodes=[...list.querySelectorAll(':scope>.cue-group')],byCue=new Map(nodes.map(node=>[+node.querySelector('[data-select-cue]').dataset.selectCue,node]));
 for(const j of reviewVisibleOrder(s))list.append(byCue.get(j));
 const filter=document.querySelector('.review-filter');
 filter?.insertAdjacentHTML('beforeend',`<label class="minimal-cue-sort">Order<select data-review-cue-sort aria-label="Cue list order"><option value="recording" ${s.reviewOrderSort!=='cue'?'selected':''}>Recording order</option><option value="cue" ${s.reviewOrderSort==='cue'?'selected':''}>Cue order</option></select></label>`);
 const locked=!!running(s)||s.reviewOrderSort==='cue';
 for(const [j,node] of byCue){
  node.dataset.reviewCueKey=String(j);node.classList.add('v3-order-row');
  const handle=document.createElement('span');handle.className='v3-drag-handle';handle.setAttribute('role','button');handle.setAttribute('tabindex',locked?'-1':'0');handle.setAttribute('aria-disabled',String(locked));handle.draggable=false;handle.dataset.reviewDragCue=String(j);handle.title='Drag to reorder '+cues[j][0];handle.setAttribute('aria-label',handle.title);handle.textContent='⠿';node.prepend(handle);
 }
 if(!locked)list.insertAdjacentHTML('beforeend','<div class="v3-order-end" data-review-order-end aria-label="Move cue to end of recording order"></div>');
 const order=reviewRecordingOrder(s),index=order.indexOf(s.cue);
 document.querySelectorAll('[data-action="prev-cue"]').forEach(b=>b.disabled=!!running(s)||index===0);
 document.querySelectorAll('[data-action="next-cue"]').forEach(b=>b.disabled=!!running(s)||index===order.length-1);
};
document.addEventListener('change',e=>{if(e.target.matches('[data-review-cue-sort]')){state().reviewOrderSort=e.target.value;renderDemo();}});
let reviewCueDrag=null,reviewSuppressCueClickUntil=0;
function reviewCancelCueDrag(){
 document.querySelectorAll('.v3-cue-drop-target').forEach(el=>el.classList.remove('v3-cue-drop-target'));
 reviewCueDrag=null;
}
document.addEventListener('pointerdown',e=>{
 const handle=e.target.closest('[data-review-drag-cue],[data-review-timeline-cue]');if(!handle||e.button!==0)return;
 if(running(state())||state().reviewOrderSort==='cue')return;
 e.preventDefault();handle.setPointerCapture(e.pointerId);
 reviewCueDrag={id:+(handle.dataset.reviewDragCue??handle.dataset.reviewTimelineCue),timeline:handle.hasAttribute('data-review-timeline-cue'),pointer:e.pointerId,startY:e.clientY,startX:e.clientX,moved:false,target:null};
});
document.addEventListener('pointermove',e=>{
 const drag=reviewCueDrag;if(!drag||e.pointerId!==drag.pointer)return;
 drag.moved||=Math.hypot(e.clientY-drag.startY,e.clientX-drag.startX)>4;if(!drag.moved)return;e.preventDefault();
 const scroll=document.querySelector('#cue-scroll'),r=scroll?.getBoundingClientRect();if(r){if(e.clientY>r.bottom-45)scroll.scrollTop+=15;else if(e.clientY<r.top+45)scroll.scrollTop-=15;}
 document.querySelectorAll('.v3-cue-drop-target').forEach(el=>el.classList.remove('v3-cue-drop-target'));
 const target=document.elementFromPoint(e.clientX,e.clientY)?.closest('[data-review-cue-key],[data-review-order-end]');
 drag.target=target?target.hasAttribute('data-review-order-end')?{end:true}:{before:+target.dataset.reviewCueKey}:null;
 if(target?.hasAttribute('data-review-timeline-cue')){
  const rect=target.getBoundingClientRect(),after=e.clientX>rect.left+rect.width/2;
  if(after){const order=reviewRecordingOrder(state()),next=order[order.indexOf(+target.dataset.reviewCueKey)+1];drag.target=next===undefined?{end:true}:{before:next};}
  target.classList.toggle('v3-drop-after',after);
  const scroller=target.closest('.cue-timeline-scroll'),r=scroller.getBoundingClientRect();
  if(e.clientX>r.right-35)scroller.scrollLeft+=15;else if(e.clientX<r.left+35)scroller.scrollLeft-=15;
 }
 target?.classList.add('v3-cue-drop-target');
});
document.addEventListener('pointerup',e=>{const drag=reviewCueDrag;if(!drag||drag.pointer!==e.pointerId)return;e.preventDefault();reviewCancelCueDrag();if(drag.moved){reviewSuppressCueClickUntil=performance.now()+350;if(drag.target)reviewMoveCue(drag.id,drag.target);}});
document.addEventListener('click',e=>{if(performance.now()<reviewSuppressCueClickUntil&&e.target.closest('[data-session-cue],[data-review-drag-cue]')){e.preventDefault();e.stopImmediatePropagation();}},true);
document.addEventListener('pointercancel',reviewCancelCueDrag);
document.addEventListener('keydown',e=>{
 if(e.key==='Escape'&&reviewCueDrag){e.preventDefault();reviewCancelCueDrag();return;}
 const handle=e.target.closest('[data-review-drag-cue]');if(handle&&['ArrowUp','ArrowDown'].includes(e.key)){e.preventDefault();reviewMoveCue(+handle.dataset.reviewDragCue,e.key==='ArrowUp'?-1:1);}
},true);
const reviewBaseExport=openSessionExport;
openSessionExport=function(kind){reviewBaseExport(kind);if(kind==='order'){const body=document.querySelector('.session-export-preview tbody');if(body){const rows=[...body.children];for(const j of reviewRecordingOrder(state()))body.append(rows[j]);}}};

renderDemo();
