// One optional review round. A/B choices change the visible prototype immediately.
const v4ReviewChoices={timing:'A',workload:'A',ranges:'A',learning:'A',allocation:'A'};
try{Object.assign(v4ReviewChoices,JSON.parse(localStorage.getItem('mandocues-v4-review')||'{}').choices||{});}catch{}
let v4ReviewDemo=null;
const v4ReviewConfig=[
 {id:'v4-timing',key:'timing',title:'Welke tijden wil je direct zien?',text:'Probeer eerst de sessie te starten met Space. A toont cuetijd en sessieprognose. B klapt de overige tijden erbij open.',target:'#main-panel',view:'recording',a:'A · Twee hoofdsignalen',b:'B · Met timingdetails'},
 {id:'v4-workload',key:'workload',title:'Hoe vul je de opnameomvang in?',text:'Vul de muziek in die je echt gaat opnemen. A is één duur per cue. B heeft maatbereiken met elk een eigen duur. De maten alleen bepalen de duur niet.',target:'#main-panel .v4-cue-facts',view:'recording',a:'A · Duur per cue',b:'B · Duur per bereik'},
 {id:'v4-ranges',key:'ranges',title:'Instarten op verschillende maten',text:'Kies Whole cue of een maatbereik voor de volgende take. De take-nummers lopen door. A voegt een bereik toe; B toont twee voorbeeldbereiken om tussen te wisselen.',target:'.v4-take-range',view:'recording',a:'A · Bereik invoeren',b:'B · Bereiken klaarzetten'},
 {id:'v4-learning',key:'learning',title:'De schatting bijstellen',text:'A leert geleidelijk van afgeronde cues. B houdt het oorspronkelijke werktempo vast. Probeer het rekenvoorbeeld; je echte demo-invoer blijft apart.',target:'.v4-status-area',view:'recording',a:'A · Leren van afgeronde cues',b:'B · Tempo vast houden'},
 {id:'v4-allocation',key:'allocation',title:'Tijd verdelen over de volgende cues',text:'A verdeelt de overgebleven tijd opnieuw bij een cuewissel of afronding. B houdt de oorspronkelijke cuebudgetten vast. Een aangepaste eindtijd is geen bewijs dat je langzamer werkt.',target:'.cue-timeline',view:'recording',a:'A · Beschikbare tijd herverdelen',b:'B · Budgetten vasthouden'},
 {id:'v4-score',title:'De partituur erbij',text:'Kies een take en lees mee op de partituur. N opent het noteveld; dubbelklik op de score voor een note op die plek. De Comp tool is bewaard in v3.',target:'.score-paper',relatedTargets:['.score-take-picker'],view:'cutlist',prepare:'score'}
];
function v4ApplyChoice(key,choice){
 const s=state(),v=v4State(s);v4ReviewChoices[key]=choice;
 if(key==='timing')v.settings.timing=choice==='A'?'focus':'details';
 if(key==='workload')v.settings.workload=choice==='A'?'cue':'ranges';
 if(key==='learning')v.settings.learning=choice==='A'?'completed':'fixed';
 if(key==='allocation')v.settings.allocation=choice==='A'?'adaptive':'fixed';
 if(key==='ranges'){
  v.settings.ranges=choice==='A'?'single':'multiple';
  const ranges=v4Ranges(s);ranges.editing=choice==='A';
  if(choice==='B')for(const range of [{from:2,to:8},{from:12,to:19}])if(!ranges.presets.some(r=>r.from===range.from&&r.to===range.to))ranges.presets.push(range);
 }
 try{localStorage.setItem('mandocues-v4-review',JSON.stringify({version:4,choices:v4ReviewChoices}));}catch{}
 renderDemo();if(v4ReviewDemo==='learning')v4RenderLearningExample();else if(v4ReviewDemo==='allocation')v4RenderAllocationExample();
}
const v4ReviewBaseRebalance=v4Rebalance;
v4Rebalance=function(s,options={}){if(v4State(s).settings.allocation==='fixed'&&s.sessionStarted&&!options.force)return;v4ReviewBaseRebalance(s,options);};
function v4ReviewSummary(){
 closeProposalTour();
 reviewDialog('v4-review-summary','Jouw v4-keuzes',`<p>Dit zijn je keuzes in deze lokale proef. De gedeelde v3-presentatie is niet vervangen.</p><ul>${v4ReviewConfig.filter(step=>step.key).map(step=>`<li><b>${esc(step.title)}</b><br>${esc(v4ReviewChoices[step.key]==='B'?step.b:step.a)}</li>`).join('')}</ul><label class="v4-review-notes">Opmerkingen<textarea id="v4-review-notes" rows="4" placeholder="Wat wil je anders?"></textarea></label><footer><a href="../review-v3/index.html#cutlist" target="_blank" rel="noopener">Bewaarde v3 / Comp tool</a><button data-v4-review-download>Download keuzes</button></footer>`);
}
const v4TourParts=v4ReviewConfig.map(step=>({id:step.id,title:step.title,prompt:'v4-review: '+step.title}));
proposalTourSteps.splice(0,proposalTourSteps.length,...v4ReviewConfig.map((step,i)=>({...step,parts:[v4TourParts[i]]})));
proposalTourSuggestions.splice(0,proposalTourSuggestions.length,...proposalTourSteps);
proposalTourParts.splice(0,proposalTourParts.length,...v4TourParts);
const v4ReviewBaseOpen=openTourStep;
openTourStep=function(index){
 v4ReviewDemo=null;document.querySelectorAll('#v4-learning-example,#v4-allocation-example').forEach(el=>el.remove());
 v4ReviewBaseOpen(index);const step=v4ReviewConfig[index],card=document.querySelector('.proposal-tour-card');if(!step||!card)return;
 card.querySelector('header>span').textContent='v4 review · '+(index+1)+' van '+v4ReviewConfig.length;
 card.querySelector('.tour-prompt-choice')?.remove();
 if(step.key){const controls=document.createElement('div');controls.className='v4-review-options';controls.innerHTML=`<button data-v4-review-key="${step.key}" data-v4-review-choice="A" aria-pressed="${v4ReviewChoices[step.key]!=='B'}">${esc(step.a)}</button><button data-v4-review-key="${step.key}" data-v4-review-choice="B" aria-pressed="${v4ReviewChoices[step.key]==='B'}">${esc(step.b)}</button>`;card.querySelector('footer').before(controls);}
 if(step.key==='workload')card.querySelector('footer').insertAdjacentHTML('beforebegin','<button data-v4-try-workload>Probeer invoer voor deze cue</button>');
 if(step.key==='learning')card.querySelector('footer').insertAdjacentHTML('beforebegin','<button data-v4-learning-example>Toon rekenvoorbeeld</button>');
 if(step.key==='allocation')card.querySelector('footer').insertAdjacentHTML('beforebegin','<button data-v4-allocation-example>Toon verdelingsvoorbeeld</button>');
 if(index===v4ReviewConfig.length-1)card.querySelector('[data-tour-action=next]').textContent='Naar mijn keuzes';
 positionProposalTour();
};
document.addEventListener('click',event=>{
 const choice=event.target.closest('[data-v4-review-choice]');if(choice){const index=proposalTourIndex;v4ApplyChoice(choice.dataset.v4ReviewKey,choice.dataset.v4ReviewChoice);document.querySelectorAll('[data-v4-review-choice]').forEach(b=>b.setAttribute('aria-pressed',String(b===choice)));positionProposalTour();return;}
 if(event.target.closest('[data-v4-try-workload]')){v4EditCue(state().cue);return;}
 if(event.target.closest('[data-v4-learning-example]')){v4ReviewDemo='learning';v4RenderLearningExample();return;}
 if(event.target.closest('[data-v4-allocation-example]')){v4ReviewDemo='allocation';v4RenderAllocationExample();return;}
 if(event.target.closest('[data-v4-review-download]')){
  saveFile('MandoCues-v4-keuzes.json',JSON.stringify({version:4,at:new Date().toISOString(),choices:v4ReviewChoices,notes:document.querySelector('#v4-review-notes')?.value||''},null,2));return;
 }
 if(event.target.closest('[data-tour-action=next]')&&proposalTourIndex===proposalTourSteps.length-1){event.preventDefault();event.stopImmediatePropagation();v4ReviewSummary();}
},true);
openProposalPrompt=v4ReviewSummary;
function v4RenderLearningExample(){
 document.querySelector('#v4-learning-example')?.remove();
 const raw=[{id:0,musicSeconds:60,complexity:'Medium',workedSeconds:1140,done:true},{id:1,musicSeconds:60,complexity:'Hard',workedSeconds:0,done:false},{id:2,musicSeconds:120,complexity:'Medium',workedSeconds:0,done:false}];
 const learning=v4State(state()).settings.learning!=='fixed';raw[0].include=learning;
 const f=V4Planning.forecast(raw,{rate:6,prepSeconds:120,availableSeconds:1200});
 const card=document.querySelector('.proposal-tour-card');if(!card)return;
 card.querySelector('footer').insertAdjacentHTML('beforebegin',`<div id="v4-learning-example"><b>Los rekenvoorbeeld</b><p>Een afgeronde cue had 1 minuut muziek en Medium-complexiteit. Budget: 8 minuten, werkelijk werk: 19 minuten.</p><p>Resterende cues: 1 minuut Hard, 2 minuten Medium. Beschikbaar: 20 minuten.</p><strong>Nieuwe werkschatting: ${v4Duration(f.remaining)}</strong><p>${learning?'Het gemeten tempo telt voorzichtig mee; de langere en moeilijkere cues krijgen meer werkgewicht.':'Het referentietempo blijft gelijk; de gemeten cue verandert de volgende schattingen niet.'}</p><small>De echte demo-state is niet gewijzigd.</small></div>`);positionProposalTour();
}
function v4RenderAllocationExample(){
 document.querySelector('#v4-allocation-example')?.remove();const adaptive=v4State(state()).settings.allocation==='adaptive';
 document.querySelector('.proposal-tour-card footer')?.insertAdjacentHTML('beforebegin',`<div id="v4-allocation-example"><b>Los verdelingsvoorbeeld</b><p>Na uitloop blijft 25 minuten over. De volgende cues vragen naar schatting 10 en 20 minuten werk.</p><table><thead><tr><th></th><th>Beschikbaar</th><th>Werkschatting</th></tr></thead><tbody><tr><td>Volgende cue</td><td>${adaptive?'08:20':'10:00'}</td><td>10:00</td></tr><tr><td>Daarna</td><td>${adaptive?'16:40':'20:00'}</td><td>20:00</td></tr></tbody></table><p>${adaptive?'De beschikbare tijd wordt krapper verdeeld.':'De oorspronkelijke budgetten blijven staan.'} De werkschatting blijft in beide gevallen 30 minuten: 5 minuten verwachte uitloop. Herverdelen maakt het werk niet korter.</p><small>De echte demo-state is niet gewijzigd.</small></div>`);positionProposalTour();
}
// A genuine second input prototype: duration per selected recording section.
const v4ReviewBaseEdit=v4EditCue;
v4EditCue=function(j){
 v4ReviewBaseEdit(j);if(v4State(state()).settings.workload!=='ranges')return;
 const form=document.querySelector('#v4-cue-timing'),music=form.querySelector('[name=music]'),row=v4Row(state(),j);
 music.closest('label').hidden=true;
 const parts=structuredClone(row.musicParts||[{from:1,to:8,seconds:row.musicSeconds}]);
 const group=document.createElement('section');group.className='v4-music-parts';group.innerHTML='<b>Music to record per section</b><div data-v4-music-parts></div><button type="button" data-v4-music-add>+ Section</button><p data-v4-music-error role="status"></p>';
 form.prepend(group);
 for(const part of parts)v4AddMusicPart(group.querySelector('[data-v4-music-parts]'),part);
};
function v4AddMusicPart(group,part={from:1,to:8,seconds:0}){group.insertAdjacentHTML('beforeend',`<div class="v4-music-part"><label>From<input data-part-from type="number" min="1" max="99999" value="${part.from}" required></label><label>Till<input data-part-to type="number" min="1" max="99999" value="${part.to}" required></label><label>Music mm:ss<input data-part-duration value="${v4Duration(part.seconds)}" pattern="[0-9]+:[0-5][0-9]" required></label><button type="button" data-v4-music-remove aria-label="Remove section">×</button></div>`);}
document.addEventListener('click',event=>{
 if(event.target.closest('[data-v4-music-add]'))v4AddMusicPart(document.querySelector('[data-v4-music-parts]'));
 const remove=event.target.closest('[data-v4-music-remove]');if(remove)remove.closest('.v4-music-part').remove();
});
document.addEventListener('submit',event=>{
 const form=event.target;if(form.id!=='v4-cue-timing'||!form.querySelector('.v4-music-parts'))return;
 const parts=[...form.querySelectorAll('.v4-music-part')].map(part=>({from:+part.querySelector('[data-part-from]').value,to:+part.querySelector('[data-part-to]').value,seconds:v4Seconds(part.querySelector('[data-part-duration]').value)}));
 if(!parts.length||parts.some(part=>part.to<part.from||part.seconds==null)||parts.some((a,i)=>parts.some((b,j)=>j<i&&a.from<=b.to&&b.from<=a.to))){event.preventDefault();event.stopImmediatePropagation();form.querySelector('[data-v4-music-error]').textContent='Use valid, non-overlapping bar ranges and durations.';return;}
 form.querySelector('[name=music]').value=v4Duration(parts.reduce((sum,part)=>sum+part.seconds,0));v4Row(state(),+form.querySelector('[name=cue]').value).musicParts=parts;
},true);
const v4ReviewBaseRender=renderDemo;
renderDemo=function(){
 v4ReviewBaseRender();
 document.querySelector('[data-proposal-action=tour]').textContent='Review v4';document.querySelector('[data-proposal-action=prompt]').innerHTML='Mijn keuzes';
 document.querySelector('[data-proposal-action=questions]').hidden=true;
 document.querySelector('.header-label').textContent='v4 · planning & score';
 const target=document.querySelector('.proposal-demo-label');if(target)target.insertAdjacentHTML('beforeend',' · <button class="v4-shortcut-help" data-v4-shortcuts>Shortcuts</button> · <a href="../review-v3/index.html#cutlist" target="_blank" rel="noopener">Saved Comp tool</a>');
};
document.addEventListener('click',event=>{
 if(event.target.closest('[data-v4-shortcuts]'))appDialog('Shortcuts',`<dl class="v4-shortcut-list">${[['Space','Start session, then start / stop takes (outside text fields)'],['[ and ]','Previous / next cue'],['⌥[ and ⌥]','Previous / next take'],['⌥1 to ⌥9','Choose the actual take number'],['Hold ⌥ + ⌘, then two digits','Choose a take such as 12; release to cancel'],['N','Focus the note field and anchor the writing time'],['B','Set the next take range (Recording) or edit the selected take range (Score)'],['Enter','Save a note and prepare the next'],['Shift+Enter','New line in a note'],['⌘Z','Undo a score note change']].map(([key,meaning])=>`<div><dt>${shortcutText(key)}</dt><dd>${esc(meaning)}</dd></div>`).join('')}</dl>`);
});
// Apply stored review choices to this fresh demo without creating fake learning data.
for(const key of ['timing','workload','learning','allocation'])v4ApplyChoice(key,v4ReviewChoices[key]);
renderDemo();
