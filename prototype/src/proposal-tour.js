// The tour only selects existing, static prompt sections; it never generates text.
const proposalTourConfig=JSON.parse(document.querySelector('#proposal-tour-source').textContent);
const proposalTourSteps=proposalTourConfig.steps;
const proposalTourSelection=new Set(proposalTourSteps.map(step=>step.id));
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
function tourPromptFor(step){return step.discussion?discussion.find(item=>item.id===step.discussion).text:step.prompt;}
function selectedTourPrompt(){
 const selected=proposalTourSteps.filter(step=>proposalTourSelection.has(step.id));
 return selected.length?tourPromptIntro+selected.map((step,index)=>`## ${index+1}. ${step.title}\n\n${tourPromptFor(step)}`).join('\n\n---\n\n')+proposalTourConfig.promptClosing:'';
}
function persistTourSelection(){
 try{localStorage.setItem(proposalTourStorageKey,JSON.stringify({excluded:proposalTourSteps.filter(step=>!proposalTourSelection.has(step.id)).map(step=>step.id)}));}catch{}
 document.querySelectorAll('[data-proposal-selection-count]').forEach(el=>el.textContent=proposalTourSelection.size);
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
 proposalTourIndex=-1;tourTarget=null;document.body.classList.remove('tour-cue-selection','tour-take-notes','tour-note-metadata');
 document.querySelector('.proposal-tour-card')?.remove();document.querySelector('.proposal-tour-highlight')?.remove();
 document.querySelector('[data-proposal-action="tour"]')?.focus({preventScroll:true});
}
function openTourStep(index){
 if(index<0||index>=proposalTourSteps.length)return;
 stopTourShortcutHint();
 proposalTourIndex=index;const step=proposalTourSteps[index],s=unifiedState;
 document.body.classList.toggle('tour-cue-selection',step.id==='cue-aanklikken');
 document.body.classList.toggle('tour-take-notes',step.id==='noteplek');
 document.body.classList.toggle('tour-note-metadata',step.id==='maat-aanpassen');
 showProposalView(step.view);
 if(step.view==='recording'){
  // Demonstrate take-based suggestions on populated examples, without creating takes during a tour.
  if(['cue-takes','noteplek','maat-aanpassen','protools-sync','sterren','alt-best'].includes(step.id)&&!s.takes[s.cue].length&&!running(s))selectCue(s,0);
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
 card.innerHTML=`<header><span>Suggestie ${index+1} van ${proposalTourSteps.length}</span><button type="button" data-tour-action="close" aria-label="Rondleiding sluiten">×</button></header><h2 id="proposal-tour-title" tabindex="-1">${esc(step.title)}</h2>${step.text?`<p>${esc(step.text)}</p>`:""}<label class="tour-prompt-choice"><input type="checkbox" data-tour-choice="${step.id}" ${proposalTourSelection.has(step.id)?'checked':''}><span>Voeg toe aan de prompt voor Claude</span></label><footer><button type="button" data-tour-action="previous" ${index===0?'disabled':''}>Terug</button><button type="button" class="review-primary" data-tour-action="next">${index===proposalTourSteps.length-1?'Naar mijn selectie':'Volgende →'}</button></footer>`;
 document.body.append(card);
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
function findTourTarget(step){
 for(const selector of step.target.split(','))for(const el of document.querySelectorAll(selector.trim())){
  const box=el.getBoundingClientRect();if(box.width>0&&box.height>0&&getComputedStyle(el).visibility==='visible'&&!el.closest('[hidden]'))return el;
 }
 return null;
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
 const rects=[tourTarget,...(step.relatedTargets||[]).map(selector=>document.querySelector(selector)).filter(Boolean),...(popup?[popup]:[])].map(el=>el.getBoundingClientRect()).filter(r=>r.width&&r.height);
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
function tourChoiceRow(step){return `<label class="tour-summary-choice"><input type="checkbox" data-tour-choice="${step.id}" ${proposalTourSelection.has(step.id)?'checked':''}><span>${esc(step.title)}</span></label>`;}
function openProposalPrompt(){
 closeProposalTour();
 const selected=proposalTourSteps.filter(step=>proposalTourSelection.has(step.id)),other=proposalTourSteps.filter(step=>!proposalTourSelection.has(step.id));
 reviewDialog('proposal-prompt','Jouw selectie voor Claude',`<p>Alleen aangevinkte suggesties komen in de prompt.</p><div class="tour-selected-list">${selected.length?selected.map(tourChoiceRow).join(''):'<p class="review-muted">Kies hieronder suggesties of start de rondleiding.</p>'}</div>${other.length?`<details class="tour-other-choices"><summary>Andere suggesties (${other.length})</summary>${other.map(tourChoiceRow).join('')}</details>`:''}<details class="tour-prompt-preview"><summary>Bekijk de prompt</summary><pre tabindex="0">${esc(selectedTourPrompt()||'Vink eerst een suggestie aan.')}</pre></details><footer><button type="button" data-tour-action="download" ${selected.length?'':'disabled'}>Download</button><button type="button" class="review-primary" data-tour-action="copy" ${selected.length?'':'disabled'}>Kopieer prompt</button></footer>`);
}
function refreshPromptPreview(){
 const dialog=document.querySelector('#proposal-prompt');if(!dialog)return;
 dialog.querySelector('pre').textContent=selectedTourPrompt()||'Vink eerst een suggestie aan.';
 dialog.querySelectorAll('[data-tour-action="copy"],[data-tour-action="download"]').forEach(button=>button.disabled=!proposalTourSelection.size);
}
function openProposalQuestions(){
 closeProposalTour();
 reviewDialog('proposal-questions','Nog een paar vragen',`<ul class="proposal-questions-list">${openQuestions().map(q=>`<li>${esc(q.title)}${q.text?' '+esc(q.text):''}</li>`).join('')}</ul><footer><button type="button" data-tour-action="close-dialog">Terug naar de werkruimte</button></footer>`);
}
document.addEventListener('click',async event=>{
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
 const id=event.target.dataset.tourChoice;if(!id||!proposalTourSteps.some(step=>step.id===id))return;
 event.target.checked?proposalTourSelection.add(id):proposalTourSelection.delete(id);persistTourSelection();refreshPromptPreview();
});
document.addEventListener('keydown',event=>{
 if(event.target.closest('.proposal-review-dialog[open]')&&event.key==='Enter'&&event.metaKey){event.preventDefault();event.stopImmediatePropagation();return;}
 if(event.key==='Escape'&&event.target.closest('.measure-picker[open],.note-time-value:not([readonly])'))return;
 if(event.key==='Escape'&&proposalTourIndex>=0){event.preventDefault();event.stopImmediatePropagation();closeProposalTour();}
},true);
document.addEventListener('scroll',scheduleTourPosition,true);window.addEventListener('resize',scheduleTourPosition);
persistTourSelection();showProposalWelcome();
