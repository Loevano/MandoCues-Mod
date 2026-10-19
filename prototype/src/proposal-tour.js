// The tour only selects existing, static prompt sections; it never generates text.
const proposalTourConfig=JSON.parse(document.querySelector('#proposal-tour-source').textContent);
const proposalTourSteps=proposalTourConfig.steps;
const proposalTourSuggestions=proposalTourSteps.filter(step=>!step.transition);
const proposalTourParts=proposalTourSteps.flatMap(step=>step.parts);
const proposalTourSelection=new Set(proposalTourParts.map(part=>part.id));
// Store explicit opt-outs; an older partial selection must not turn defaults off.
const proposalTourStorageKey='mandocues-proposal-tour-v2';
try{
 const saved=JSON.parse(localStorage.getItem(proposalTourStorageKey)||'null');
 if(saved&&Array.isArray(saved.excluded))for(const id of saved.excluded)proposalTourSelection.delete(id);
}catch{}
let proposalTourIndex=-1,tourPositionFrame=0,tourTarget=null,tourShortcutTimer=null;
function stopTourShortcutHint(){
 clearTimeout(tourShortcutTimer);document.body.classList.remove('tour-start-shortcut');
}
const tourPromptIntro=proposalTourConfig.promptIntro;
function tourStepSelected(step){return step.parts.some(part=>proposalTourSelection.has(part.id));}
function tourPromptFor(step,selectedOnly=false){return step.parts.filter(part=>!selectedOnly||proposalTourSelection.has(part.id)).map(part=>part.discussion?discussion.find(item=>item.id===part.discussion).text:part.prompt).join('\n\n');}
function syncTourChoices(){
 for(const checkbox of document.querySelectorAll('[data-tour-choice]')){
  const step=proposalTourSteps.find(step=>step.id===checkbox.dataset.tourChoice);
  const count=step.parts.filter(part=>proposalTourSelection.has(part.id)).length;
  checkbox.checked=count>0;checkbox.indeterminate=count>0&&count<step.parts.length;
 }
}
function selectedTourPrompt(){
 const selected=proposalTourSteps.filter(tourStepSelected);
 return selected.length?tourPromptIntro+selected.map((step,index)=>`## ${index+1}. ${step.title}\n\n${tourPromptFor(step,true)}`).join('\n\n---\n\n')+proposalTourConfig.promptClosing:'';
}
function persistTourSelection(){
 try{localStorage.setItem(proposalTourStorageKey,JSON.stringify({excluded:proposalTourParts.filter(part=>!proposalTourSelection.has(part.id)).map(part=>part.id)}));}catch{}
 document.querySelectorAll('[data-proposal-selection-count]').forEach(el=>el.textContent=proposalTourSteps.filter(tourStepSelected).length);
}
function reviewDialog(id,title,body){
 document.querySelector('#'+id)?.remove();
 const dialog=document.createElement('dialog');dialog.id=id;dialog.className='proposal-review-dialog';dialog.lang='nl';
 dialog.setAttribute('aria-labelledby',id+'-title');dialog.innerHTML=`<header><h2 id="${id}-title">${title}</h2><button type="button" data-tour-action="close-dialog" aria-label="Sluiten">×</button></header>${body}`;
 document.body.append(dialog);dialog.showModal();
 dialog.addEventListener('close',()=>dialog.remove(),{once:true});
 return dialog;
}
function showProposalWelcome(){
 reviewDialog('proposal-welcome','Een paar ideeën van Floris',`<p>Probeer wat je aanspreekt. Vink uit wat je niet wilt meegeven aan Claude.</p><p class="review-muted">Jouw programma en workflow blijven het uitgangspunt.</p><footer><button type="button" data-tour-action="welcome-skip">Zelf bekijken</button><button type="button" class="review-primary" data-tour-action="welcome-start">Rondleiding starten</button></footer>`);
}
function closeProposalTour(){
 stopTourShortcutHint();
 proposalTourIndex=-1;tourTarget=null;document.body.classList.remove('tour-cue-selection','tour-take-notes','tour-note-metadata','tour-score','tour-score-selection','tour-score-notes');
 document.querySelector('.proposal-tour-card')?.remove();document.querySelector('.proposal-tour-highlight')?.remove();
 document.querySelector('[data-proposal-action="tour"]')?.focus({preventScroll:true});
}
function tourInlineText(text){return shortcutText(text);}
function tourScheduleExamples(step){
 if(!step.scheduleExamples)return '';
 return `<figure class="tour-schedule-examples"><figcaption>Voorbeelden</figcaption>${step.scheduleExamples.map(example=>`<div class="main-plan-card ${proposalPlanClass(example.delta)}"><strong>${esc(proposalScheduleText(example.delta))}</strong><small>${esc(example.label)}</small></div>`).join('')}</figure>`;
}
function openTourStep(index){
 if(index<0||index>=proposalTourSteps.length)return;
 stopTourShortcutHint();
 proposalTourIndex=index;const step=proposalTourSteps[index],s=unifiedState;
 document.body.classList.toggle('tour-cue-selection',step.id==='cue-aanklikken');
 document.body.classList.toggle('tour-take-notes',step.id==='noteplek');
 document.body.classList.toggle('tour-note-metadata',step.id==='maat-aanpassen');
 document.body.classList.toggle('tour-score',step.view==='cutlist');
 document.body.classList.toggle('tour-score-selection',step.id==='score-selecteren');
 document.body.classList.toggle('tour-score-notes',step.id==='score-notes');
 showProposalView(step.view);
 if(step.view==='recording'){
  // Demonstrate take-based suggestions on populated examples, without creating takes during a tour.
  if(['noteplek','maat-aanpassen','sterren'].includes(step.id)&&!s.takes[s.cue].length&&!running(s)){
   const example=s.takes.findIndex(takes=>takes.length);if(example>=0)selectCue(s,example);
  }
  s.open.add(s.cue);
 }
 if(step.prepare==='session')s.calmSessionOpen=true;
 if(step.prepare==='all'&&s.cutlistView!=='all'){rememberScoreView(s);s.cutlistView='all';}
 if(step.prepare==='score'&&s.cutlistView==='all'){s.cutlistView='score';restoreScoreView(s);}
 renderDemo();
 if(step.prepare==='sticky'){
  const scroll=document.querySelector('#cue-scroll'),button=document.querySelector('#main-panel .record');scroll.scrollTop+=button.getBoundingClientRect().bottom-scroll.getBoundingClientRect().top+12;syncSticky();
 }
 document.querySelector('.proposal-tour-card')?.remove();
 const card=document.createElement('section');card.className='proposal-tour-card';card.lang='nl';card.setAttribute('aria-labelledby','proposal-tour-title');card.setAttribute('aria-label','Rondleiding');
 card.innerHTML=`<header><span>${step.transition?'Recording → Comp tool':'Suggestie '+(proposalTourSuggestions.indexOf(step)+1)+' van '+proposalTourSuggestions.length}</span><button type="button" data-tour-action="close" aria-label="Rondleiding sluiten">×</button></header><h2 id="proposal-tour-title" tabindex="-1">${tourInlineText(step.title)}</h2>${step.text?`<p>${tourInlineText(step.text)}</p>`:""}${tourScheduleExamples(step)}${step.inlineHelp?`<div class="tour-extra tour-inline-help"><strong>${esc(step.inlineHelp.title)}</strong><p>${tourInlineText(step.inlineHelp.text)}</p></div>`:""}${step.details?`<details class="tour-extra"><summary>${esc(step.details.title)}</summary><p>${tourInlineText(step.details.text)}</p></details>`:""}${step.transition?'':`<label class="tour-prompt-choice"><input type="checkbox" data-tour-choice="${step.id}" ${tourStepSelected(step)?'checked':''}><span>Voeg toe aan de prompt voor Claude</span></label>`}<footer><button type="button" data-tour-action="previous" ${index===0?'disabled':''}>Terug</button><button type="button" class="review-primary" data-tour-action="next">${step.transition?'Comp tool bekijken →':index===proposalTourSteps.length-1?'Naar mijn selectie':'Volgende →'}</button></footer>`;
 document.body.append(card);syncTourChoices();
 if(!document.querySelector('.proposal-tour-highlight')){const highlight=document.createElement('div');highlight.className='proposal-tour-highlight';highlight.setAttribute('aria-hidden','true');document.body.append(highlight);}
 tourTarget=findTourTarget(step);
 if(step.id==='cue-aanklikken'&&tourTarget){
  const scroll=document.querySelector('#cue-scroll');
  scroll.scrollTop+=tourTarget.getBoundingClientRect().top-scroll.getBoundingClientRect().top-80;
  syncSticky();
 }else if(step.id==='noteplek'&&tourTarget){
  const scroll=document.querySelector('#cue-scroll');
  const anchor=tourTarget;
  scroll.scrollTop+=anchor.getBoundingClientRect().top-scroll.getBoundingClientRect().top-90;
  syncSticky();
 }else revealTourTarget(tourTarget);
 syncSticky();
 if(step.id==='opnametoets'&&!s.sessionStarted){
  document.body.classList.add('tour-start-shortcut');
  tourShortcutTimer=setTimeout(stopTourShortcutHint,2100);
 }
 document.querySelector('#proposal-tour-title').focus({preventScroll:true});
 positionProposalTour();scheduleTourPosition();
}
// Bring each step into its own scroll viewport, including a previously scrolled list.
function revealTourTarget(target){
 if(!target)return;
 // Fixed transport is already on screen; scrolling its sticky ancestor would hide it.
 if(target.closest('.sticky-slot'))return;
 const canvas=target.closest('.score-canvas');
 const viewport=canvas?.clientHeight||document.querySelector('#cue-scroll')?.clientHeight||innerHeight;
 target.scrollIntoView({block:target.offsetHeight>viewport-120?'start':'center',inline:'nearest',behavior:'instant'});
 // Leave room for the sticky start/stop bar in the recording list.
 const scroll=target.closest('#cue-scroll');
 if(scroll){
  const r=target.getBoundingClientRect(),bounds=scroll.getBoundingClientRect();
  if(r.top<bounds.top+80)scroll.scrollTop-=bounds.top+80-r.top;
 }
}
// Use only the part inside the real scroll viewport; score pages can be taller than it.
function tourTargetRect(el){
 const box=el.getBoundingClientRect();
 let left=Math.max(0,box.left),top=Math.max(0,box.top),right=Math.min(innerWidth,box.right),bottom=Math.min(innerHeight,box.bottom);
 for(let p=el.parentElement;p&&p!==document.body;p=p.parentElement){
  const style=getComputedStyle(p),r=p.getBoundingClientRect();
  if(/auto|scroll|hidden|clip/.test(style.overflowX)){left=Math.max(left,r.left);right=Math.min(right,r.right);}
  if(/auto|scroll|hidden|clip/.test(style.overflowY)){top=Math.max(top,r.top);bottom=Math.min(bottom,r.bottom);}
 }
 return {left,top,right,bottom,width:Math.max(0,right-left),height:Math.max(0,bottom-top)};
}
function findTourTarget(step){
 let fallback=null;
 for(const selector of step.target.split(',')){
  const matches=[...document.querySelectorAll(selector.trim())].filter(el=>{
   const box=el.getBoundingClientRect();return box.width>0&&box.height>0&&getComputedStyle(el).visibility==='visible'&&!el.closest('[hidden]');
  });
  fallback??=matches[0];
  const visible=matches.map(el=>({el,rect:tourTargetRect(el)})).filter(item=>item.rect.width>0&&item.rect.height>0).sort((a,b)=>b.rect.width*b.rect.height-a.rect.width*a.rect.height);
  if(visible.length)return visible[0].el;
 }
 return fallback??null;
}
function scheduleTourPosition(){
 if(proposalTourIndex<0||tourPositionFrame)return;
 tourPositionFrame=requestAnimationFrame(()=>{tourPositionFrame=0;positionProposalTour();});
}
function positionProposalTour(){
 if(proposalTourIndex<0)return;
 const card=document.querySelector('.proposal-tour-card'),highlight=document.querySelector('.proposal-tour-highlight');if(!card||!highlight)return;
 tourTarget=findTourTarget(proposalTourSteps[proposalTourIndex]);
 if(!tourTarget){
  highlight.hidden=true;
  Object.assign(card.style,{left:Math.max(12,innerWidth-card.offsetWidth-12)+'px',top:Math.max(12,innerHeight-card.offsetHeight-12)+'px'});
  return;
 }
 const step=proposalTourSteps[proposalTourIndex];
 const popup=step.id==='maat-aanpassen'?document.querySelector('.measure-picker[open] .measure-picker-panel'):null;
 const rects=[tourTarget,...(step.relatedTargets||[]).map(selector=>document.querySelector(selector)).filter(Boolean),...(popup?[popup]:[])].map(tourTargetRect).filter(r=>r.width&&r.height);
 if(!rects.length){highlight.hidden=true;return;}
 const r={left:Math.min(...rects.map(r=>r.left)),top:Math.min(...rects.map(r=>r.top)),right:Math.max(...rects.map(r=>r.right)),bottom:Math.max(...rects.map(r=>r.bottom))},margin=12,padding=5;
 const left=Math.max(4,r.left-padding),top=Math.max(4,r.top-padding),right=Math.min(innerWidth-4,r.right+padding),bottom=Math.min(innerHeight-4,r.bottom+padding);
 highlight.hidden=right<=left||bottom<=top;
 Object.assign(highlight.style,{left:left+'px',top:top+'px',width:Math.max(0,right-left)+'px',height:Math.max(0,bottom-top)+'px'});
 const width=card.offsetWidth,height=card.offsetHeight;
 const positions=[{x:right+16,y:top},{x:left-width-16,y:top},{x:left,y:bottom+16},{x:left,y:top-height-16}];
 const fit=positions.find(p=>p.x>=margin&&p.x+width<=innerWidth-margin&&p.y>=margin&&p.y+height<=innerHeight-margin);
 const preferred=proposalTourSteps[proposalTourIndex].id==='cue-aanklikken'&&innerWidth<760?{x:margin,y:innerHeight-height-margin}:fit||{x:innerWidth-width-margin,y:innerHeight-height-margin};
 Object.assign(card.style,{left:Math.max(margin,Math.min(innerWidth-width-margin,preferred.x))+'px',top:Math.max(margin,Math.min(innerHeight-height-margin,preferred.y))+'px'});
}
function tourChoiceRow(step){return `<label class="tour-summary-choice"><input type="checkbox" data-tour-choice="${step.id}" ${tourStepSelected(step)?'checked':''}><span>${tourInlineText(step.title)}</span></label>`;}
function openProposalPrompt(){
 closeProposalTour();
 const selected=proposalTourSteps.filter(tourStepSelected),other=proposalTourSuggestions.filter(step=>!tourStepSelected(step));
 reviewDialog('proposal-prompt','Jouw selectie voor Claude',`<p>Alleen aangevinkte suggesties komen in de prompt.</p><div class="tour-selected-list">${selected.length?selected.map(tourChoiceRow).join(''):'<p class="review-muted">Kies hieronder suggesties of start de rondleiding.</p>'}</div>${other.length?`<details class="tour-other-choices"><summary>Andere suggesties (${other.length})</summary>${other.map(tourChoiceRow).join('')}</details>`:''}<details class="tour-prompt-preview"><summary>Bekijk de prompt</summary><pre tabindex="0">${tourInlineText(selectedTourPrompt()||'Vink eerst een suggestie aan.')}</pre></details><footer><button type="button" data-tour-action="download" ${selected.length?'':'disabled'}>Download</button><button type="button" class="review-primary" data-tour-action="copy" ${selected.length?'':'disabled'}>Kopieer prompt</button></footer>`);
 syncTourChoices();
}
function refreshPromptPreview(){
 const dialog=document.querySelector('#proposal-prompt');if(!dialog)return;
 dialog.querySelector('pre').innerHTML=tourInlineText(selectedTourPrompt()||'Vink eerst een suggestie aan.');
 dialog.querySelectorAll('[data-tour-action="copy"],[data-tour-action="download"]').forEach(button=>button.disabled=!proposalTourSelection.size);
}
function openProposalQuestions(){
 closeProposalTour();
 reviewDialog('proposal-questions','Nog een paar vragen',`<ul class="proposal-questions-list">${openQuestions().map(q=>`<li>${esc(q.title)}${q.text?' '+esc(q.text):''}</li>`).join('')}</ul><footer><button type="button" data-tour-action="close-dialog">Terug naar de werkruimte</button></footer>`);
}
document.addEventListener('click',async event=>{
 if(proposalTourSteps[proposalTourIndex]?.transition&&event.target.closest('[data-proposal-view="cutlist"]')){
  event.preventDefault();event.stopImmediatePropagation();openTourStep(proposalTourIndex+1);return;
 }
 const button=event.target.closest('[data-proposal-action],[data-tour-action]');if(!button)return;
 event.preventDefault();event.stopImmediatePropagation();
 const action=button.dataset.proposalAction||button.dataset.tourAction;
 if(button.disabled)return;
 if(action==='fullscreen'){await fullscreenPrototype();return;}
 if(action==='tour'){openTourStep(0);return;}
 if(action==='questions'){openProposalQuestions();return;}
 if(action==='prompt'){openProposalPrompt();return;}
 if(action==='close-dialog'||action==='welcome-skip'){button.closest('dialog')?.close();return;}
 if(action==='welcome-start'){button.closest('dialog')?.close();openTourStep(0);return;}
 if(action==='close'){closeProposalTour();return;}
 if(action==='previous'){openTourStep(proposalTourIndex-1);return;}
 if(action==='next'){if(proposalTourIndex+1<proposalTourSteps.length)openTourStep(proposalTourIndex+1);else openProposalPrompt();return;}
 if(action==='copy'){await copyText(selectedTourPrompt(),document.querySelector('#proposal-prompt pre'),document.querySelector('.tour-prompt-preview'),'Selectie gekopieerd — klaar voor Claude.');return;}
 if(action==='download')saveFile('Claude-geselecteerde-suggesties.md',selectedTourPrompt());
},true);
document.addEventListener('change',event=>{
 const id=event.target.dataset.tourChoice,step=proposalTourSteps.find(step=>step.id===id);if(!step)return;
 for(const part of step.parts)event.target.checked?proposalTourSelection.add(part.id):proposalTourSelection.delete(part.id);
 syncTourChoices();persistTourSelection();refreshPromptPreview();
});
document.addEventListener('keydown',event=>{
 if(event.target.closest('.proposal-review-dialog[open]')&&event.key==='Enter'&&event.metaKey){event.preventDefault();event.stopImmediatePropagation();return;}
 if(event.key==='Escape'&&event.target.closest('.measure-picker[open],.note-time-value:not([readonly])'))return;
 if(event.key==='Escape'&&proposalTourIndex>=0){event.preventDefault();event.stopImmediatePropagation();closeProposalTour();}
},true);
document.addEventListener('scroll',scheduleTourPosition,true);window.addEventListener('resize',scheduleTourPosition);
document.addEventListener('toggle',event=>{if(event.target.matches('.tour-extra'))scheduleTourPosition();},true);
persistTourSelection();showProposalWelcome();
