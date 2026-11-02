// One review sequence; A/B choices are preferences, never production approvals.
const reviewSteps=[
 {id:'workspace',title:'Bediening en notes bij elkaar',text:'A houdt de vorige indeling. B zet actieve takes en het noteveld naast de bediening. Probeer een cue, schrijf iets en wissel A/B.',a:'Vorige indeling',b:'Notes naast de bediening',target:'.v3-cue-workspace,#main-panel'},
 {id:'history',title:'Eerdere opmerkingen teruglezen',text:'A toont de notes van de gekozen take. B toont de notes van alle takes van deze cue samen, met het take-nummer erbij. Klik een take om daar verder te schrijven.',a:'Notes per take',b:'Alle notes van de cue',target:'.v3-notes-column'},
 {id:'sections',title:'Deel van een cue opnemen',text:'Gewone takes, met een maatbereik erbij. A: typ bijvoorbeeld 4–10 in één veld. B: kies Van/Tot en bekijk takes per bereik. ⌘⇧J opent de invoer; daarna Space om op te nemen.',a:'Eén bereikveld',b:'Van/tot en groeperen',target:'.v3-section-editor'},
 {id:'notes',title:'Een maatlabel tijdens het typen',text:'Schrijf een note. A: ⌘J opent een klein veld voor bijvoorbeeld 13–20. B: Van/Tot staat direct bij het noteveld. Het bereik is een apart label; Enter slaat de note op.',a:'Snelle invoer met ⌘J',b:'Van/tot direct zichtbaar',target:'.calm-notes .note-composer'},
 {id:'planning',title:'De rest opnieuw verdelen',text:'Verander de eindtijd, pauze of buffer. A verdeelt de resterende tijd opnieuw naar muziekduur en moeilijkheid. B laat je budgetten vastzetten. Vergelijk de preview; pas daarna toe op de demo.',a:'Alles herverdelen',b:'Budgetten vastzetten',target:'.v3-planner'},
 {id:'order',title:'Opnamevolgorde zelf bepalen',text:'A: sleep aan de greep naast een cue. B: gebruik de pijltjes. Wissel tussen Recording order en Cue order; je opnamevolgorde blijft bewaard. Current cue springt bewust naar de actieve cue.',a:'Slepen',b:'Pijltjes',target:'.v3-cue-order-controls'},
 {id:'clocks',title:'Alleen de klokken die je gebruikt',text:'Kies de hoofdklok, eventueel een tweede tijdzone en welke kleinere tijden zichtbaar zijn. A zet de opties achter Clock display; B toont ze direct. Notes houden hun eigen kloktijd.',a:'Compact menu',b:'Directe instellingen',target:'.v3-clock-settings,.v3-inline-clock-settings'},
 {id:'score',title:'Partituur bij de hand',text:'A zet een leespartituur naast de notes. B opent de grote Comp tool, met notes en maatselecties op de score. Probeer zoomen; de schaal blijft gelijk bij wisselen. A4 op papier kan er gewoon naast blijven.',a:'Leespartituur naast notes',b:'Grote Comp tool',target:'.v3-reference-score,.score-canvas'}
];
let reviewIndex=0,reviewFinished=false,reviewChoices={},reviewComments={};
try{
 const saved=JSON.parse(localStorage.getItem('mandocues-v3-review-round')||'{}');
 for(const step of reviewSteps){if(['A','B','skip'].includes(saved.choices?.[step.id]))reviewChoices[step.id]=saved.choices[step.id];if(typeof saved.comments?.[step.id]==='string')reviewComments[step.id]=saved.comments[step.id];}
}catch{}
function reviewPersist(){try{localStorage.setItem('mandocues-v3-review-round',JSON.stringify({choices:reviewChoices,comments:reviewComments}));}catch{}}
function reviewSummaryData(){return {format:'mandocues-v3-review-20261102',exportedAt:new Date().toISOString(),baseline:'before-session-review-v3-20261102',status:'preferences-only-not-implementation-approval',displayPreferences:{...sessionReview.clocks},confirmed:{firstSpace:'session-only',typingSpace:'text',proTools:'deferred'},steps:reviewSteps.map(s=>({id:s.id,title:s.title,choice:reviewChoices[s.id]||null,choiceLabel:reviewChoices[s.id]==='A'?s.a:reviewChoices[s.id]==='B'?s.b:null,comment:reviewComments[s.id]||''}))};}
function reviewDrawToolbar(){
 const toolbar=document.querySelector('.v3-review-toolbar');if(!toolbar)return;
 const step=reviewSteps[reviewIndex],choice=reviewChoices[step.id];
 toolbar.innerHTML=`<div class="v3-review-topline"><strong>v3 · ${reviewFinished?'Jouw keuzes':(reviewIndex+1)+' van '+reviewSteps.length}</strong><nav aria-label="Reviewvolgorde"><button data-review-prev ${reviewIndex===0&&!reviewFinished?'disabled':''}>← Terug</button><button data-review-overview>Overzicht</button><button data-review-next ${reviewFinished?'hidden':''}>${reviewIndex===reviewSteps.length-1?'Naar mijn keuzes':'Volgende →'}</button></nav><a href="PLAN.md" target="_blank">Plan ↗</a></div>${reviewFinished?'':`<div class="v3-review-step-copy"><div><h2>${esc(step.title)}</h2><p>${shortcutText(step.text)}</p></div><div class="v3-review-variants" role="group" aria-label="Vergelijk opties"><button data-review-variant="A" aria-pressed="${reviewVariant(step.id)==='A'}"><b>A</b> ${esc(step.a)}</button><button data-review-variant="B" aria-pressed="${reviewVariant(step.id)==='B'}"><b>B</b> ${esc(step.b)}</button></div></div><div class="v3-review-bottomline"><span>${choice==='skip'?'Overgeslagen':choice?'Keuze '+choice+' bewaard':'Bekijk A/B; klik je voorkeur om die te bewaren.'}</span><button data-review-skip>Overslaan</button><details class="v3-review-feedback"><summary>Opmerking</summary><textarea data-review-comment aria-label="Opmerking bij dit voorstel" placeholder="Wat zou je anders willen?">${esc(reviewComments[step.id]||'')}</textarea></details><small>Space: eerst sessiestart, daarna takes · Pro Tools uitgesteld</small></div>`}`;
 document.body.classList.toggle('v3-review-summary-open',reviewFinished);
 document.querySelector('.v3-review-summary')?.remove();
 if(reviewFinished){
  const section=document.createElement('main');section.className='v3-review-summary';section.lang='nl';
  section.innerHTML=`<header><h1>Alles in één overzicht</h1><p>Je voorkeuren staan hieronder. Dit verandert de bestaande versie niet.</p></header>${running(state())?`<aside class="v3-summary-live" lang="en"><b>● Recording ${entryLabel(running(state()))}</b><span data-live="${running(state()).id}">${time(position(running(state())))}</span>${recordButton(state())}</aside>`:''}<div class="v3-summary-rows">${reviewSteps.map((s,i)=>`<article><div><b>${i+1}. ${esc(s.title)}</b><p>${reviewChoices[s.id]==='A'?'A · '+esc(s.a):reviewChoices[s.id]==='B'?'B · '+esc(s.b):reviewChoices[s.id]==='skip'?'Overgeslagen':'Nog geen keuze'}</p>${reviewComments[s.id]?`<small>${esc(reviewComments[s.id])}</small>`:''}</div><button data-review-open-step="${i}">Opnieuw bekijken</button></article>`).join('')}</div><footer><button data-review-download>Download keuzes</button><button data-review-restart>Alles nog eens bekijken</button></footer><p class="v3-summary-footnote">Bevestigd: Space start eerst alleen de sessie; daarna start/stop van takes. Tijdens typen blijft spatie tekst. Pro Tools staat voorlopig on hold. Keuzes blijven op dit apparaat bewaard; demo-notes en takes verdwijnen bij herladen.</p>`;
  document.body.append(section);
 }
}
function reviewUpdateContext(){
 if(!reviewFinished){
  const step=reviewSteps[reviewIndex];document.querySelector('.v3-review-caption').textContent='Reviewproef · '+step.title+' · keuzes worden alleen lokaal bewaard.';
  document.body.classList.toggle('v3-history-feed',step.id==='history'&&reviewVariant('history')==='B');
  document.querySelectorAll('.v3-review-target').forEach(el=>el.classList.remove('v3-review-target'));
  for(const selector of step.target.split(',')){const el=document.querySelector(selector);if(el){el.classList.add('v3-review-target');break;}}
 }
 reviewDrawToolbar();
 document.querySelector('.app-sidebar').style.top=(document.querySelector('.site-header').getBoundingClientRect().bottom)+'px';
}
reviewUpdates.push(reviewUpdateContext);
function reviewGo(idOrIndex){
 const index=typeof idOrIndex==='number'?idOrIndex:reviewSteps.findIndex(s=>s.id===idOrIndex);
 if(index<0||index>=reviewSteps.length)return;
 closeProposalTour();document.querySelector('.v3-note-range-popover')?.remove();reviewNoteTarget=null;
 reviewFinished=false;reviewIndex=index;const step=reviewSteps[index];sessionReview.feature=step.id;
 if(['A','B'].includes(reviewChoices[step.id]))sessionReview.variants[step.id]=reviewChoices[step.id];
 sessionReview.layout=step.id==='workspace'?reviewVariant('workspace'):'B';
 if(step.id==='history')sessionReview.history=false;
 showProposalView(step.id==='score'&&reviewVariant('score')==='B'?'cutlist':'recording');
 {
  const target=document.querySelector(step.target);target?.scrollIntoView({block:step.id==='order'?'start':'nearest',inline:'nearest',behavior:'instant'});
  if(step.id!=='order'&&proposalView==='recording'){const scroll=document.querySelector('#cue-scroll');scroll.scrollTop=0;}
 }
}
function reviewChoose(value){const step=reviewSteps[reviewIndex];sessionReview.variants[step.id]=value;reviewChoices[step.id]=value;reviewPersist();reviewGo(reviewIndex);}
document.addEventListener('click',e=>{
 const v=e.target.closest('[data-review-variant]');if(v){reviewChoose(v.dataset.reviewVariant);return;}
 if(e.target.closest('[data-review-prev]')){reviewGo(reviewFinished?reviewSteps.length-1:reviewIndex-1);return;}
 if(e.target.closest('[data-review-next]')){if(reviewIndex<reviewSteps.length-1)reviewGo(reviewIndex+1);else{reviewFinished=true;reviewDrawToolbar();}return;}
 if(e.target.closest('[data-review-overview]')){reviewFinished=true;reviewDrawToolbar();return;}
 const open=e.target.closest('[data-review-open-step]');if(open){reviewGo(+open.dataset.reviewOpenStep);return;}
 if(e.target.closest('[data-review-skip]')){reviewChoices[reviewSteps[reviewIndex].id]='skip';reviewPersist();if(reviewIndex<reviewSteps.length-1)reviewGo(reviewIndex+1);else{reviewFinished=true;reviewDrawToolbar();}return;}
 if(e.target.closest('[data-review-download]')){saveFile('MandoCues-v3-review-keuzes.json',JSON.stringify(reviewSummaryData(),null,2),'application/json');return;}
 if(e.target.closest('[data-review-restart]'))reviewGo(0);
});
document.addEventListener('input',e=>{if(e.target.matches('[data-review-comment]')){reviewComments[reviewSteps[reviewIndex].id]=e.target.value;reviewPersist();}});
// Useful section examples, clearly part of the existing demonstration takes.
for(const t of unifiedState.takes[0])if(!t.barRange)t.barRange=t.num===1?{from:1,to:8}:{from:12,to:15};
reviewGo(0);
