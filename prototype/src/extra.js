// Isolated, browser-local examples for additional questions. No DAW or recorder connection.
function freshExtra(id) {
  if (id === 'planning') return {booked:180, elapsed:42, remaining:140, selectedCue:0};
  if (id === 'take-afspraak') return {proposed:4, engineer:4, last:3, confirmed:null, live:null, registrations:[]};
}

function planningClock(minutes){return String(Math.floor(minutes/60)%24).padStart(2,'0')+':'+String(minutes%60).padStart(2,'0');}
function planningStatus(s){
 const delta=s.elapsed+s.remaining-s.booked,status=delta>0?'behind':delta<0?'ahead':'on schedule',signed=delta>0?'+'+delta:delta<0?'−'+Math.abs(delta):'0';
 const end=600+s.elapsed+s.remaining,clock=String(Math.floor(end/60)%24).padStart(2,'0')+':'+String(end%60).padStart(2,'0');
 return `<div class="schedule-badge schedule-focus ${delta>0?'late':delta<0?'ahead':'on-time'}" role="status"><strong>${signed} min</strong><b>${status}</b><small>Projected end ${clock}</small></div>`;
}
function planningInputs(s){return `<details class="planning-adjust" data-planning-panel ${s.planningOpen?'open':''}><summary>Adjust demo schedule</summary><div class="planning-inputs">${[['booked','Booked'],['elapsed','Elapsed'],['remaining','Remaining work']].map(([key,label])=>`<label>${label}<span><input type="number" min="0" max="1440" step="1" data-planning="${key}" value="${s[key]}"> min</span></label>`).join('')}</div><div class="extra-actions"><button data-extra="faster">1 min faster</button><button data-extra="pause-five">5 min break</button></div><small>Example values; no automatic prediction.</small></details>`;}
function planningDemo(){const s=state();return recordingScreen(s,groupedList(s),'Session schedule');}

function usedTakeNumber(s,number) { return (number>=1&&number<=3)||s.registrations.some(r=>r.number===number); }
function agreementDemo() {
  const s=state(), mismatch=s.proposed!==s.engineer, used=usedTakeNumber(s,s.proposed);
  const valid=Number.isInteger(s.proposed)&&Number.isInteger(s.engineer)&&s.proposed>0&&s.engineer>0;
  return demoTop('gedeelde take-identiteit')+`<section class="extra-demo agreement-demo">
    <div class="shared-take"><span>Afspraak met muzikanten en engineer</span><h3>1M02 · Arrival · Take ${s.confirmed??s.proposed??'—'}</h3><p>${s.confirmed?'Nummer handmatig bevestigd':'Nummer eerst samen bevestigen'}</p></div>
    <div class="agreement-inputs"><label>Voorstel take-nummer<input type="number" min="1" max="9999" data-agreement="proposed" value="${s.proposed??''}" ${s.live?'disabled':''}></label><label>Nummer volgens engineer<input type="number" min="1" max="9999" data-agreement="engineer" value="${s.engineer??''}" ${s.live?'disabled':''}></label></div>
    <p class="agreement-status" role="status">${!valid?'Vul twee geldige take-nummers in.':mismatch?'Verschil in nummering. Stem dit samen af vóór registratie.':used?'Dit nummer is al gebruikt. Bestaande takes worden niet hernummerd.':s.confirmed?'Afspraak staat: Take '+s.confirmed+'.':'Beide nummers gelijk. Bevestig de afspraak voordat je registreert.'}</p>
    <div class="extra-actions"><button data-extra="confirm-take" ${!valid||mismatch||used||s.confirmed||s.live?'disabled':''}>Bevestig Take ${s.proposed??'—'}</button>
      ${variant==='A'?`<button class="${s.live?'stop':'record'}" data-extra="timed-take" ${!s.confirmed&&!s.live?'disabled':''}>${s.live?'■ Stop registratie':'● Start bevestigde take'}</button>${s.live?`<b class="registry-clock" data-registry-clock>${time(Math.floor((Date.now()-s.live.started)/1000))}</b>`:''}`:`<button data-extra="log-take" ${!s.confirmed?'disabled':''}>Log bevestigde take</button>`}
    </div>
    <p class="demo-caption">${variant==='A'?'A houdt een voorbeeld-timer bij. Er wordt geen audio opgenomen.':'B registreert één take zonder timer. Registratietijd is geen take-positie of automatisch maatanker.'}</p>
    <div class="registration-list"><h3>Vastgelegde takes</h3>${s.registrations.length?s.registrations.map(r=>`<article class="registration" data-registration="${r.id}"><header><b>1M02 · Take ${r.number}</b><span>${r.mode==='timed'?'Met timer · '+time(r.duration):'Alleen gelogd · geen take-duur'}</span></header><small>Geregistreerd ${r.at} · vaste ID ${r.id}</small><label class="source-file-label">${r.file?'Bronbestand: '+esc(r.file):'Optioneel: wijs zelf een bronbestand aan'}<input type="file" data-registry-file="${r.id}"></label><p>${r.file?'Handmatig aangewezen; niet door de DAW bevestigd.':'Geen bronbestand gekoppeld.'}</p></article>`).join(''):'<p class="notes-empty">Nog niets geregistreerd. De laatste bestaande take is Take 3.</p>'}</div>
    <p class="demo-caption">Creation date alleen bewijst geen Pro Tools-/Logic-koppeling. Bestand kiezen bewaart hier alleen de naam in de demo; niets wordt geüpload.</p>
  </section>`;
}

function cutSegments(s) {
  const rows=[];
  s.assignments.forEach((take,index)=>{
    const measure=s.first+index, previous=rows.at(-1);
    if(previous&&previous.take===take)previous.to=measure;
    else rows.push({from:measure,to:measure,take});
  });
  return rows;
}
function cutCsv(s) {
  return 'Cue,VanMaat,TotMaat,Take,Status\r\n'+cutSegments(s).map(r=>`1M02,${r.from},${r.to},${r.take??''},${r.take?'Conceptkeuze':'OPEN'}`).join('\r\n');
}
function cutListDemo() {
  const s=state(), gaps=s.assignments.filter(t=>t===null).length;
  return demoTop('concept-kniplijst')+`<section class="extra-demo cut-demo">
    <header class="cut-heading"><h3>1M02 · Arrival</h3><span>${gaps?gaps+' maten zonder keuze':'Alle maten hebben een conceptkeuze'}</span></header>
    <div class="cue-measure-bounds"><label>Cue van maat<input type="number" min="1" max="99999" id="cue-first" value="${s.first}"></label><label>Tot en met<input type="number" min="1" max="99999" id="cue-last" value="${s.last}"></label><button data-extra="cut-bounds">Bereik aanpassen</button></div>
    ${variant==='A'?`<div class="cut-table-wrap"><table class="cut-table"><thead><tr><th>Maten</th><th>Selected take</th><th>Status</th></tr></thead><tbody>${cutSegments(s).map(r=>`<tr><td>${r.from}–${r.to}</td><td>${r.take?'Take '+r.take:'—'}</td><td>${r.take?'Concept':'OPEN · nog kiezen'}</td></tr>`).join('')}</tbody></table></div>`:`<div class="measure-timeline" role="group" aria-label="Takekeuze per maat">${s.assignments.map((take,j)=>`<button data-cut-measure="${j}" class="${take?'take-color-'+take:'unassigned'}" aria-label="Bar ${s.first+j}: ${take?'Take '+take:'nog geen take'}. Klik om te wisselen."><small>Bar ${s.first+j}</small><b>${take?'T'+take:'—'}</b></button>`).join('')}</div><p class="demo-caption">Klik: Take 1 → Take 2 → nog geen keuze. Dit is een maatindeling, geen audiotijdlijn.</p>`}
    <div class="cut-editor"><h4>Keuze for een maatbereik</h4><div><label>Take<select data-cut-input="take"><option value="1" ${s.take===1?'selected':''}>Take 1</option><option value="2" ${s.take===2?'selected':''}>Take 2</option></select></label><label>Van<input type="number" min="${s.first}" max="${s.last}" data-cut-input="from" value="${s.from}"></label><label>Tot en met<input type="number" min="${s.first}" max="${s.last}" data-cut-input="to" value="${s.to}"></label></div><p>Gebruiken vervangt bestaande keuzes in dit bereik. Uitsluiten verwijdert alleen de gekozen take en laat een gat open.</p><div class="extra-actions"><button data-extra="cut-include">Gebruik deze take</button><button data-extra="cut-exclude">Sluit deze take uit</button></div></div>
    <div class="extra-actions"><button data-extra="cut-download">Download concept-kniplijst CSV</button><span>Voor de editor · controleer overgangen en open maten</span></div>
    <p class="demo-caption">Geen automatische audio-edit of DAW-export. De maat/tijdkoppeling naar echte bronbestanden is een aparte vervolgstap. Deze proef toont maximaal 64 maten tegelijk.</p>
  </section>`;
}

function registerDemoTake(s,mode) {
  const number=s.confirmed;
  if(!number||usedTakeNumber(s,number)){toast('Bevestig eerst een ongebruikt take-nummer.');return;}
  s.registrations.push({id:'demo-1M02-t'+number,number,mode,at:new Date().toLocaleTimeString('en-GB'),duration:mode==='timed'?Math.floor((Date.now()-s.live.started)/1000):null,file:null});
  s.last=Math.max(s.last,number);s.proposed=s.last+1;s.engineer=s.last+1;s.confirmed=null;s.live=null;renderDemo();
}
function handleExtraClick(b) {
  if(b.dataset.planCue!==undefined){state().selectedCue=+b.dataset.planCue;renderDemo();return true;}
  if(b.dataset.cutMeasure!==undefined){const s=state(),j=+b.dataset.cutMeasure;s.assignments[j]=s.assignments[j]===1?2:s.assignments[j]===2?null:1;renderDemo();return true;}
  if(!b.dataset.extra)return false;
  const s=state();
  switch(b.dataset.extra){
    case 'faster':s.remaining=Math.max(0,s.remaining-1);break;
    case 'pause-five':s.elapsed+=5;break;
    case 'confirm-take':if(!Number.isInteger(s.proposed)||s.proposed<1||s.proposed!==s.engineer||usedTakeNumber(s,s.proposed))return true;s.confirmed=s.proposed;break;
    case 'timed-take':if(s.live){registerDemoTake(s,'timed');return true;}if(!s.confirmed)return true;s.live={started:Date.now()};break;
    case 'log-take':registerDemoTake(s,'log');return true;
    case 'cut-bounds':{
      const first=+$('#cue-first').value,last=+$('#cue-last').value;
      if(!Number.isInteger(first)||!Number.isInteger(last)||first<1||last<first||last>99999||last-first>=64){toast('Choose een geldig bereik van maximaal 64 maten.');return true;}
      const old=new Map(s.assignments.map((t,j)=>[s.first+j,t]));s.assignments=Array.from({length:last-first+1},(_,j)=>old.get(first+j)??null);s.first=first;s.last=last;s.from=first;s.to=last;break;
    }
    case 'cut-include':case 'cut-exclude':{
      const {from,to,take}=s;
      if(!Number.isInteger(from)||!Number.isInteger(to)||from<s.first||to>s.last||from>to||![1,2].includes(take)){toast('Choose een geldig maatbereik binnen deze cue.');return true;}
      for(let m=from;m<=to;m++){if(b.dataset.extra==='cut-include')s.assignments[m-s.first]=take;else if(s.assignments[m-s.first]===take)s.assignments[m-s.first]=null;}break;
    }
    case 'cut-download':saveFile('1M02-concept-kniplijst.csv',cutCsv(s),'text/csv;charset=utf-8');return true;
  }
  renderDemo();return true;
}
function handleExtraChange(el) {
  if(el.dataset.planning){const value=+el.value;if(!Number.isInteger(value)||value<0||value>1440||el.value===''){el.reportValidity();return true;}state()[el.dataset.planning]=value;renderDemo();return true;}
  if(el.dataset.agreement){if(state().live)return true;const value=+el.value;state()[el.dataset.agreement]=Number.isInteger(value)&&value>0&&value<=9999&&el.value!==''?value:null;state().confirmed=null;renderDemo();return true;}
  if(el.dataset.cutInput){state()[el.dataset.cutInput]=el.value===''?null:+el.value;return true;}
  if(el.dataset.registryFile){const r=state().registrations.find(r=>r.id===el.dataset.registryFile);if(r&&el.files[0])r.file=el.files[0].name;renderDemo();return true;}
  return false;
}
function syncExtraClocks(){if(active?.id==='take-afspraak'&&state().live){const el=$('[data-registry-clock]');if(el)el.textContent=time(Math.floor((Date.now()-state().live.started)/1000));}}

function quickNoteSuggestions(t,place) {
  return `<section class="quick-note-suggestions" aria-label="Quick notes"><span>Quick notes</span><div>${['Intonation','More expressive','Less expressive','Tight','Alt take'].map(text=>`<button type="button" data-quick-note="${text}" data-take="${t.id}" data-editor-place="${place}">${text}</button>`).join('')}</div></section>`;
}
// Navigation has the same meaning in Recording and Comp tool.
let takeNumberEntry=null,takeNumberTimer=null,bracketKeyHold=null;
function navigationKeysAvailable(event){
 return active&&['bediening','partituur'].includes(active.id)
  &&!document.querySelector('dialog[open]')
  &&!event.target.closest('input,textarea,select,[contenteditable]:not([contenteditable="false"])')
  &&!scoreGesture&&!scoreNoteDrag;
}
function cancelTakeNumberEntry(){
 takeNumberEntry=null;clearTimeout(takeNumberTimer);
 document.querySelector('.take-number-entry')?.remove();
}
function showTakeNumberEntry(release=false){
 let panel=document.querySelector('.take-number-entry');
 if(!panel){panel=document.createElement('div');panel.className='take-number-entry';panel.lang='en';panel.setAttribute('role','status');panel.setAttribute('aria-live','polite');document.body.append(panel);}
 panel.textContent='Take '+takeNumberEntry.digits.padEnd(2,'_')+' · '+(release?'Release ⌥⌘, then type two digits':'Type two digits')+' · Esc to cancel';
 clearTimeout(takeNumberTimer);takeNumberTimer=setTimeout(cancelTakeNumberEntry,5000);
}
function takeShortcutTitle(t){
 if(t.kind==='overdub')return 'View '+entryLabel(t)+' · ⌥[ previous take · ⌥] next take';
 return t.num<=9?'Go to '+entryLabel(t)+' · ⌥'+t.num:t.num<=99?'Go to '+entryLabel(t)+' · ⌥⌘, release, then type '+String(t.num).padStart(2,'0'):'View '+entryLabel(t);
}
function selectNavigationTake(s,t){
 if(!t){toast('That take does not exist in this cue.');return;}
 if(active.id==='partituur')selectScoreTake(s,t.id);
 else if(s.selected!==t.id){
  s.selected=t.id;t.collapsed=false;s.open.add(s.cue);
  s.scoreCompared??={};s.scoreCompared[s.cue]=[t.id];
  restoreScoreView(s);renderDemo();
 }
 const picker=document.querySelector('.score-take-picker'),button=picker?.querySelector(`[data-select-take="${t.id}"]`);
 if(picker&&button){const r=button.getBoundingClientRect(),b=picker.getBoundingClientRect();if(r.top<b.top)picker.scrollTop-=b.top-r.top;else if(r.bottom>b.bottom)picker.scrollTop+=r.bottom-b.bottom;}
 document.querySelector(active.id==='partituur'?'.score-canvas, .all-takes-scroll':'#cue-scroll')?.focus({preventScroll:true});
}
function chooseTakeNumber(number){
 const s=state(),t=s.takes[s.cue].find(t=>(!t.kind||t.kind==='take')&&t.num===number);
 selectNavigationTake(s,t);
}
function handleTakeNumberEntry(e){
 if(!navigationKeysAvailable(e)){if(takeNumberEntry)cancelTakeNumberEntry();return;}
 const modifier=['Alt','Meta'].includes(e.key);
 if(!takeNumberEntry&&modifier&&e.altKey&&e.metaKey&&!e.ctrlKey&&!e.shiftKey&&!e.repeat&&!e.isComposing){
  e.preventDefault();e.stopImmediatePropagation();takeNumberEntry={digits:'',cue:state().cue};showTakeNumberEntry(true);return;
 }
 if(!takeNumberEntry)return;
 if(e.key==='Escape'){e.preventDefault();e.stopImmediatePropagation();cancelTakeNumberEntry();return;}
 if(modifier||e.isComposing)return;
 const digit=/^(Digit|Numpad)[0-9]$/.test(e.code)?e.code.slice(-1):null;
 if(digit!==null&&!e.ctrlKey&&!e.shiftKey){
  e.preventDefault();e.stopImmediatePropagation();
  if(e.repeat)return;
  if(e.altKey||e.metaKey){showTakeNumberEntry(true);return;}
  takeNumberEntry.digits+=digit;showTakeNumberEntry();
  if(takeNumberEntry.digits.length===2){const number=Number(takeNumberEntry.digits);cancelTakeNumberEntry();chooseTakeNumber(number);}
  return;
 }
 cancelTakeNumberEntry();
}
document.addEventListener('keydown',handleTakeNumberEntry,true);
document.addEventListener('keyup',e=>{if(['BracketLeft','BracketRight'].includes(e.code))bracketKeyHold=null;if(takeNumberEntry&&!e.altKey&&!e.metaKey)showTakeNumberEntry();},true);
document.addEventListener('pointerdown',cancelTakeNumberEntry,true);
document.addEventListener('focusin',e=>{if(takeNumberEntry&&!navigationKeysAvailable(e))cancelTakeNumberEntry();});
window.addEventListener('blur',()=>{bracketKeyHold=null;cancelTakeNumberEntry();});
function handleExtraKey(e) {
 if(!active||e.isComposing)return false;
 if(e.repeat&&!['BracketLeft','BracketRight'].includes(e.code))return false;
 if(active.id==='take-afspraak'&&e.key==='Enter'&&(e.metaKey||e.ctrlKey)&&!e.shiftKey&&!e.altKey){e.preventDefault();if(state().live)registerDemoTake(state(),'timed');else toast('Er is recording geen take-registratie om te stoppen.');return true;}
 if(!navigationKeysAvailable(e)||e.metaKey||e.ctrlKey||e.shiftKey)return false;
 const direction=e.code==='BracketLeft'?-1:e.code==='BracketRight'?1:0;
 if(direction){
  e.preventDefault();const s=state(),now=Date.now();
  if(e.repeat){
   if(!bracketKeyHold||bracketKeyHold.code!==e.code||bracketKeyHold.alt!==e.altKey)return true;
   const interval=now-bracketKeyHold.started<900?240:110;
   if(now-bracketKeyHold.last<interval)return true;
   bracketKeyHold.last=now;
  }else bracketKeyHold={code:e.code,alt:e.altKey,started:now,last:now};
  if(e.altKey){
   const takes=s.takes[s.cue],index=takes.findIndex(t=>t.id===s.selected);
   if(!takes.length){toast('No takes in this cue yet.');return true;}
   const next=index<0?(direction>0?0:takes.length-1):Math.max(0,Math.min(takes.length-1,index+direction));
   if(takes[next].id!==s.selected)selectNavigationTake(s,takes[next]);
  }else stepCue(s,direction);
  return true;
 }
 if(e.altKey&&/^(Digit|Numpad)[1-9]$/.test(e.code)){e.preventDefault();chooseTakeNumber(+e.code.slice(-1));return true;}
 return false;
}
function extraPurpose() {
  return `<details class="extra-purpose" id="extra-input"><summary>Aanvullende input · waarom, aandachtspunten en aanvullingen</summary><div><h3>Wat willen we oplossen?</h3><ul><li>Notes op papier raken onoverzichtelijk en je kunt niet altijd snel genoeg meeschrijven.</li><li>Digitaal kun je makkelijker corrigeren en de informatie doorgeven aan andere workflows.</li><li>De hoofdtaken: planning bewaken, snel noteren en een kniplijst voor de editor maken.</li></ul><h3>Eén gedeelde take-telling</h3><p>Aandachtspunt: spreek met muzikanten en engineer af wanneer iets als take telt en welk nummer het krijgt. De app mag geen tweede, afwijkende waarheid creëren.</p><p>De kniplijst staat bij prototype 04; export naar de editor is voorlopig een opmerking. Timen of alleen loggen blijft een ontwerpvraag onder Vragen.</p><button class="text-button" data-action="export-extra">Lees of bewaar de aanvullende input ↓</button></div></details>`;
}
function extraArt(id) {
  if(id==='planning')return '<div class="mini-window mini-planning"><small>LOPEN WE OP SCHEMA?</small><b>+1 min</b><span>achter · verwacht einde 13:01</span></div>';
  if(id==='take-afspraak')return '<div class="mini-window"><div class="mini-line"><b>1M02 · Take 4</b></div><div class="mini-note">Engineer: Take 4<br>✓ Nummer samen bevestigd</div><div class="mini-note">Timen of alleen loggen?</div></div>';
  return '<div class="mini-window"><div class="mini-line"><b>1M02 · Kniplijst</b></div><div class="mini-note">Maat 1–4 → Take 1<br>Maat 5–6 → Take 2<br>Maat 7–9 → Take 1</div></div>';
}
