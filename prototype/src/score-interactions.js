// Independent cut-list layers; original score PDFs are never modified.
const scoreInstruments=[{id:'vln1',name:'Violin 1',short:'Vln 1'},{id:'vln2',name:'Violin 2',short:'Vln 2'},{id:'vla',name:'Viola',short:'Vla'},{id:'vc',name:'Cello',short:'Vc'}];
const scoreInstrumentIds=scoreInstruments.map(i=>i.id);
function scoreTakeColor(t){if(!t)return '#8d83c6';const ordinal=2*(t.num-1)+(t.kind==='overdub'?1:0);return t.color??=`hsl(${((215+ordinal*137.507764)%360).toFixed(2)} 65% 46%)`;}
function scorePageComments(s,t,page){
 const positions=scoreTextPlacements(s,page);
 return `<div class="score-annotation-layer" aria-label="Notes on score page ${page}">${scoreVisibleTakes(s).map(owner=>owner.notes.filter(n=>n.source===s.doc.id&&n.page===page&&n.id!==s.scoreComment?.editId).map(n=>{
  const anchor=positions.get(owner.id+':'+n.id);if(!anchor)return '';
  return `<button type="button" class="score-note-text score-text-annotation ${owner.id!==s.selected?'comparison-note':''} ${anchor.x>.78?'opens-left':''} ${s.focusedScoreNote===n.id?'is-focused':''}" data-score-note="${n.id}" data-score-take="${owner.id}" style="left:${anchor.x*100}%;top:${anchor.y*100}%;--take-color:${scoreTakeColor(owner)}" title="Click to edit · Drag to move" aria-label="Edit ${entryLabel(owner)}: ${esc(n.text)}">${esc(n.text)}</button>`;
 }).join('')).join('')}</div>`;
}
function scoreInstrumentLabel(ids){return !ids||ids.length===4?'All instruments':scoreInstruments.filter(i=>ids.includes(i.id)).map(i=>i.name).join(', ');}
function scoreCellKey(measure,instrument){return measure+':'+instrument;}
function scoreSelection(s,t){
 if(!t)return [];t.scoreSelections??={};
 const values=t.scoreSelections[s.doc.id]||[];
 // Preserve instrument selections; legacy bar-only values cover every staff.
 return t.scoreSelections[s.doc.id]=[...new Set(values.flatMap(value=>{
  const [bar,instrument]=String(value).split(':'),measure=Number(bar);
  if(!Number.isInteger(measure)||measure<1)return [];
  return instrument?(scoreInstrumentIds.includes(instrument)?[scoreCellKey(measure,instrument)]:[]):scoreInstrumentIds.map(i=>scoreCellKey(measure,i));
 }))].sort();
}
function scoreSelectionMeasures(selection){return [...new Set(selection.map(key=>Number(key.split(':')[0])))].sort((a,b)=>a-b);}
function formatScoreMeasures(values){const numbers=[...new Set(values)].sort((a,b)=>a-b),ranges=[];for(let i=0;i<numbers.length;i++){let start=numbers[i],end=start;while(numbers[i+1]===end+1)end=numbers[++i];ranges.push(start===end?String(start):start+'–'+end);}return ranges.join(', ');}
function scoreCells(s,page=s.page){
 const a=scoreAsset(s.doc.id),regions=scoreRegions(s,page),bookPage=a?.bookPages[page-1];
 const labels=assets.production.staffLabels.find(p=>p.bookPage===bookPage)?.labels||[];
 return regions.flatMap(r=>{
  const centers=scoreInstruments.map(i=>labels.find(l=>l.instrument===i.id&&l.y>=r.y-.01&&l.y<=r.y+r.height+.01)?.y);
  const found=centers.every(v=>Number.isFinite(v));
  const edges=found?[Math.max(r.y,centers[0]-(centers[1]-centers[0])/2),...centers.slice(0,3).map((y,i)=>(y+centers[i+1])/2),Math.min(r.y+r.height,centers[3]+(centers[3]-centers[2])/2)]:Array.from({length:5},(_,i)=>r.y+r.height*i/4);
  return scoreInstruments.map((instrument,i)=>({...r,page,instrument:instrument.id,y:edges[i],height:edges[i+1]-edges[i],key:scoreCellKey(r.measure,instrument.id)}));
 });
}
function scoreSnapshot(s,t){return {notes:structuredClone(t.notes.filter(n=>n.source===s.doc.id)),selection:[...scoreSelection(s,t)]};}
function rememberScoreChange(s,t=takeById(s,s.selected)){
 if(active?.id!=='partituur'||!t)return;
 t.scoreUndo??={};t.scoreRedo??={};const stack=t.scoreUndo[s.doc.id]??=[];stack.push(scoreSnapshot(s,t));if(stack.length>80)stack.shift();t.scoreRedo[s.doc.id]=[];
}
function undoScoreChange(s,redo=false){
 const t=takeById(s,s.selected);if(!t)return;
 const from=(redo?t.scoreRedo:t.scoreUndo)?.[s.doc.id];if(!from?.length)return;
 const to=redo?(t.scoreUndo??={}):(t.scoreRedo??={});(to[s.doc.id]??=[]).push(scoreSnapshot(s,t));
 const previous=from.pop();t.notes=[...t.notes.filter(n=>n.source!==s.doc.id),...previous.notes];t.scoreSelections[s.doc.id]=previous.selection;if(t.scoreCommentDrafts)delete t.scoreCommentDrafts[s.doc.id];s.scoreComment=null;s.focusedScoreNote=null;renderDemo();
}
function rememberScoreView(s){
 if(s.cutlistView==='all')return;
 const t=takeById(s,s.selected);if(!t)return;
 const paper=document.querySelector('.score-paper'),canvas=document.querySelector('.score-canvas');
 if(paper&&(paper.dataset.scoreTake!==t.id||paper.dataset.scoreSource!==s.doc.id))return;
 t.scoreCommentDrafts??={};if(s.scoreComment?.take===t.id&&s.scoreComment.source===s.doc.id)t.scoreCommentDrafts[s.doc.id]=structuredClone(s.scoreComment);
 t.scoreViews??={};t.scoreViews[s.doc.id]={page:s.page,measure:s.measure,zoom:1,top:canvas?.scrollTop||0,left:0};
}
function restoreScoreView(s){const v=takeById(s,s.selected)?.scoreViews?.[s.doc.id];s.page=v?.page||1;s.measure=v?.measure??null;s.zoom=1;s.scoreFocus=null;s.focusedScoreNote=null;s.scoreComment=structuredClone(takeById(s,s.selected)?.scoreCommentDrafts?.[s.doc.id]||null);s.pendingScoreScroll={top:v?.top||0,left:0};}
function selectScoreTake(s,id,keepComparison=false,keepPosition=true){const scrollY=window.scrollY,page=s.page;const t=takeById(s,id);if(!t)return;if(!keepComparison){s.scoreCompared??={};s.scoreCompared[s.cue]=[id];}if(s.selected!==id){rememberScoreView(s);s.selected=id;t.collapsed=false;s.scoreComment=null;restoreScoreView(s);if(keepPosition){delete s.pendingScoreScroll;s.page=page;}}renderDemo();if(keepPosition)window.scrollTo({top:scrollY,behavior:'instant'});}
function selectScoreCue(s,index){if(index===s.cue)return;if(running(s)){renderDemo();toast('Stop the active take before switching cues.');return;}rememberScoreView(s);s.scoreSelectedTakes??={};s.scoreSelectedTakes[s.cue]=s.selected;scoreWorkflowSwitchCue(s,index);s.cue=index;s.open.add(index);const previous=s.scoreSelectedTakes[index];s.selected=s.takes[index].some(t=>t.id===previous)?previous:s.takes[index].at(-1)?.id||null;switchScoreDocument(s,productionScoreDoc(cues[index][0]),false);renderDemo();}
function newEmptyScoreTake(s){if(running(s)){toast('Stop the active take first.');return;}rememberScoreView(s);const t=newTake(s.cue,nextEntryNumber(s,s.cue));Object.assign(t,{duration:0,cursor:0,base:0,rating:0,best:false,followMeasure:false});s.takes[s.cue].push(t);s.selected=t.id;s.scoreCompared??={};s.scoreCompared[s.cue]=[t.id];restoreScoreView(s);renderDemo();}
function scoreCueOverview(s){
 const a=scoreAsset(productionScoreDoc(cues[s.cue][0]).id);
 return `<div class="score-cue-overview"><label>Cue<select id="score-cue" aria-label="Choose a cue and its score">${cues.map((c,j)=>`<option value="${j}" ${j===s.cue?'selected':''}>${c[0]} · ${esc(c[1])}</option>`).join('')}</select></label><p><span>Bars ${a.measureRange.join('–')} · ${a.pages} pages</span>${a.cue==='1M09AB'?'<small>Shared score 1M09AB; separate takes per cue.</small>':''}</p></div>`;
}
function scoreTakeList(s,{newButton=true}={}){const compared=scoreVisibleTakes(s).map(t=>t.id);return `<section class="score-take-list"><header><h3>Takes</h3>${newButton?'<button data-score-new-take>+ New take</button>':''}</header><div class="take-picker score-take-picker" role="group" aria-label="Select a take">${s.takes[s.cue].map(t=>`<div class="score-take-row"><button data-select-take="${t.id}" style="--take-color:${scoreTakeColor(t)}" aria-pressed="${compared.includes(t.id)}" aria-current="${s.selected===t.id}"><b><i class="take-color-dot" aria-hidden="true"></i>${entryLabel(t)}</b><small>${t.rolling?'● Recording · ':''}${s.selected===t.id?'Editing · ':compared.includes(t.id)?'Comparing · ':''}${t.notes.filter(n=>n.source===s.doc.id).length} ${t.notes.filter(n=>n.source===s.doc.id).length===1?'note':'notes'}</small></button>${starRating(t.rating,t.id,cues[t.cue][0]+' '+entryLabel(t))}</div>`).join('')||'<p class="notes-empty">Create a take to get started.</p>'}</div><small class="score-compare-help">⌘/Ctrl+click: compare takes</small></section>`;}
// Overview of the current cue; bar selections and score notes are edited on the score.
function scoreViewSwitcher(s){
 return `<div class="cutlist-view-switch"><button type="button" data-score-toggle aria-label="Show score PDF" title="Show score PDF" aria-pressed="${s.cutlistView!=='all'}"><span aria-hidden="true">♪</span></button></div>`;
}
function scoreAllTakes(s){
 const bars=[...new Set(Array.from({length:s.doc.pages},(_,i)=>scoreRegions(s,i+1)).flat().map(r=>r.measure))].sort((a,b)=>a-b);
 const preview=s.cutlistNotePreview,owner=takeById(s,preview?.take);
 const previewNotes=owner?.cue===s.cue?owner.notes.filter(n=>n.source===s.doc.id&&n.measure===preview.bar):[];
 function cells(t,instrument=null){
  const selection=new Set(scoreSelection(s,t));
  return bars.map(bar=>{
   const count=scoreInstrumentIds.filter(id=>selection.has(scoreCellKey(bar,id))).length;
   const selected=instrument?selection.has(scoreCellKey(bar,instrument)):count>0;
   const notes=t.notes.filter(n=>n.source===s.doc.id&&n.measure===bar&&(!instrument||!n.instruments||n.instruments.includes(instrument)));
   const label=`${entryLabel(t)}, bar ${bar}${instrument?', '+scoreInstrumentLabel([instrument]):''}: ${selected?(instrument||count===4?'selected':'some instruments selected'):'no selection'}`;
   return `<td class="all-takes-cell ${selected?'has-selection':''} ${!instrument&&count>0&&count<4?'partial-selection':''}"><button type="button" data-cutlist-bar="${bar}" data-take="${t.id}" data-instrument="${instrument||''}" aria-label="${esc(label)} · Open score" title="${esc(label)}"><span aria-hidden="true">${selected?'━':''}</span></button>${notes.length?`<button type="button" class="all-takes-note" data-cutlist-notes="${bar}" data-take="${t.id}" aria-label="Show ${notes.length} ${notes.length===1?'note':'notes'} for ${entryLabel(t)}, bar ${bar}" title="Show notes">●</button>`:''}</td>`;
  }).join('');
 }
 return `<section class="score-viewer cutlist-viewer all-takes-view">${scoreViewSwitcher(s)}<h3>All takes · ${esc(cues[s.cue][0])}</h3><p class="all-takes-help">Coloured bars show selections. Stripes mean some instruments are selected. Click a bar to open the score; click a dot to read notes.</p>${bars.length?`<div class="all-takes-scroll" tabindex="0" role="region" aria-label="All takes by bar"><table class="all-takes-table"><caption class="sr-only">Selections and notes for every take in this cue</caption><thead><tr><th scope="col">Take / Bar</th>${bars.map(bar=>`<th scope="col">${bar}</th>`).join('')}</tr></thead><tbody>${s.takes[s.cue].map(t=>{
  const expanded=s.scoreLinkInstruments===false&&s.cutlistExpanded?.[t.id];
  return `<tr style="--take-color:${scoreTakeColor(t)}" class="${s.selected===t.id?'current-take':''}"><th scope="row"><div class="all-takes-label"><button type="button" data-cutlist-take="${t.id}" aria-current="${s.selected===t.id}"><i class="take-color-dot" style="--take-color:${scoreTakeColor(t)}" aria-hidden="true"></i>${entryLabel(t)}${t.rolling?' · Recording':''}</button><div class="all-takes-tools"><button class="best" data-take-best="${t.id}" aria-pressed="${t.best}">Best</button><button class="alt" data-take-alt="${t.id}" aria-pressed="${!!t.alt}">${altLabel(s,t.cue,t.id)}</button></div>${s.scoreLinkInstruments===false?`<button type="button" class="all-takes-expand" data-cutlist-expand="${t.id}" aria-expanded="${!!expanded}">${expanded?'⌄':'›'} Instruments</button>`:''}</div></th>${cells(t)}</tr>${expanded?scoreInstruments.map(i=>`<tr class="all-takes-instrument" style="--take-color:${scoreTakeColor(t)}"><th scope="row">${i.name}</th>${cells(t,i.id)}</tr>`).join(''):''}`;
 }).join('')}</tbody></table></div>`:'<p>No mapped bars are available for this score. Open Score to view the PDF.</p>'}${previewNotes.length?`<section class="all-takes-preview" aria-label="Notes at the selected bar" tabindex="-1"><h4>${entryLabel(owner)} · Bar ${preview.bar}</h4>${previewNotes.map(n=>`<p><small>${scoreInstrumentLabel(n.instruments)}</small>${esc(n.text)}</p>`).join('')}<button data-cutlist-bar="${preview.bar}" data-take="${owner.id}">Open in score</button></section>`:''}</section>`;
}
function scoreNoteList(s,t){
 const notes=t.notes.filter(n=>n.source===s.doc.id);
 const editIcon='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m16 3 5 5-12 12-6 1 1-6Z M14 5l5 5"/></svg>';
 const deleteIcon='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18 M9 6V3h6v3 M5 6l1 15h12l1-15 M10 10v7 M14 10v7"/></svg>';
 return `<section class="cutlist-notes-list" aria-label="Notes for the selected take"><div class="score-note-list-heading" aria-hidden="true"><span>Bar</span><span>Note</span><span>Time</span><span></span></div><div class="note-list" role="list" data-notes-for="${t.id}">${notes.map(n=>`<article role="listitem" class="score-note-row ${s.focusedScoreNote===n.id?'score-note-focused':''}" data-note-id="${n.id}"><div class="score-note-position">${noteMeasure(s,t,n,true,'score-list')}</div><p class="score-note-copy">${esc(n.text)}</p><span class="score-note-time" title="Take time">${n.useTime!==false?time(n.at):'—'}</span><div class="score-note-row-actions"><button type="button" class="score-note-icon" data-score-note="${n.id}" data-score-take="${t.id}" aria-label="Edit note: ${esc(n.text)}" title="Edit note">${editIcon}</button><button type="button" class="score-note-icon note-delete" data-delete-note="${n.id}" data-take="${t.id}" aria-label="Delete note: ${esc(n.text)}" title="Delete note">${deleteIcon}</button></div></article>`).join('')}${notes.length?'':'<p class="notes-empty">No notes for this take yet.</p>'}</div></section>`;
}
function scoreSidebar(s,{workflow=false}={}){
 const t=takeById(s,s.selected);
 const selection=scoreSelection(s,t),measures=scoreSelectionMeasures(selection);
 return `<aside class="score-notes cutlist-sidebar">${scoreCueOverview(s)}${scoreTakeList(s,{newButton:!workflow})}<div class="cutlist-undo"><button data-score-undo ${!t?.scoreUndo?.[s.doc.id]?.length?'disabled':''}>↶ Undo</button><button data-score-redo ${!t?.scoreRedo?.[s.doc.id]?.length?'disabled':''}>↷ Redo</button><button data-score-clear-selection ${!selection.length?'disabled':''}>Clear</button></div><p class="cutlist-selection">Selection: ${measures.length?'bar '+formatScoreMeasures(measures):'None'}</p>${t?scoreNoteList(s,t):''}</aside>`;
}
function openScoreComment(s,measure,anchor,page,instruments,existing=null){
 const t=takeById(s,s.selected);if(!t){toast('Create a take before adding a note.');return;}
 s.cutlistView='score';
 s.scoreComment={take:t.id,source:s.doc.id,page,measure:measure||'',text:existing?.text||'',at:existing?.at??position(t),anchor:{...anchor},instruments:[...instruments],placement:existing?.placement||'auto',editId:existing?.id||null};
 s.page=page;s.measure=measure||null;s.scoreFocus={page,measure,instruments};renderDemo();
}
function scoreCommentDialog(s,page){
 const c=s.scoreComment;if(!c||c.page!==page)return '';
 return `<div id="score-comment-dialog" class="score-inline-editor " style="--take-color:${scoreTakeColor(takeById(s,c.take))};left:clamp(0px,${c.anchor.x*100}%,max(0px,calc(100% - 285px)));top:${c.anchor.y*100}%" role="dialog" aria-label="Score note"><header><b>${entryLabel(takeById(s,c.take))}</b><label>Bar <input id="score-comment-measure" type="number" min="1" max="99999" value="${c.measure}"></label></header><div class="score-note-options"><label>For<select id="score-comment-instrument"><option value="all" ${c.instruments.length===4?'selected':''}>All instruments</option>${scoreInstruments.map(i=>`<option value="${i.id}" ${c.instruments.length===1&&c.instruments[0]===i.id?'selected':''}>${i.name}</option>`).join('')}</select></label><label>Placement<select id="score-comment-placement">${[['auto','Automatic · above'],['below','Below'],['free','At click position']].map(([value,label])=>`<option value="${value}" ${c.placement===value?'selected':''}>${label}</option>`).join('')}</select></label></div><textarea id="score-comment-text" aria-label="Note" placeholder="Write your note…">${esc(c.text)}</textarea><footer><button data-score-cancel-comment>Cancel</button><button data-score-save-comment>Add</button></footer><small>Enter = add · Shift+Enter = new line</small></div>`;
}
function syncScoreCommentDialog(){document.querySelector('#score-comment-text')?.focus({preventScroll:true});}
function saveScoreComment(s){
 const c=s.scoreComment,t=takeById(s,c?.take);if(!c||!t||!c.text.trim())return;
 if(c.measure!==''&&(!Number.isInteger(+c.measure)||+c.measure<1||+c.measure>99999)){toast('Enter a valid bar number.');return;}
 if(!c.instruments.length){toast('Choose an instrument or All.');return;}
 rememberScoreChange(s,t);
 const n={id:c.editId||'note-'+(++s.noteSerial),text:c.text.trim(),useTime:true,at:c.at,measure:c.measure===''?null:+c.measure,useMeasure:c.measure!=='',page:c.page,source:c.source,anchor:{...c.anchor},placement:c.placement,instruments:[...c.instruments]};
 syncSavedScorePage(n);if(c.editId)t.notes[t.notes.findIndex(n=>n.id===c.editId)]=n;else t.notes.push(n);
 if(t.scoreCommentDrafts)delete t.scoreCommentDrafts[s.doc.id];s.scoreComment=null;s.focusedScoreNote=n.id;renderDemo();
}
function handleScoreClick(b,event){
 if(active?.id!=='partituur')return false;const s=state();
 if(b.hasAttribute('data-score-toggle')){const showScore=s.cutlistView==='all';if(showScore)restoreScoreView(s);else rememberScoreView(s);s.cutlistView=showScore?'score':'all';renderDemo();document.querySelector('[data-score-toggle]')?.focus({preventScroll:true});return true;}
 if(b.dataset.cutlistTake){if(event?.metaKey||event?.ctrlKey)toggleScoreComparison(s,b.dataset.cutlistTake);else selectScoreTake(s,b.dataset.cutlistTake);return true;}
 if(b.dataset.cutlistExpand){s.cutlistExpanded??={};s.cutlistExpanded[b.dataset.cutlistExpand]=!s.cutlistExpanded[b.dataset.cutlistExpand];renderDemo();document.querySelector(`[data-cutlist-expand="${b.dataset.cutlistExpand}"]`)?.focus({preventScroll:true});return true;}
 if(b.dataset.cutlistNotes){s.cutlistNotePreview={take:b.dataset.take,bar:+b.dataset.cutlistNotes};renderDemo();document.querySelector('.all-takes-preview')?.focus({preventScroll:true});return true;}
 if(b.dataset.cutlistBar){
  const loc=scoreLocation(s.doc.id,+b.dataset.cutlistBar);if(!loc)return true;
  selectScoreTake(s,b.dataset.take,false,false);s.cutlistView='score';s.page=loc.page;s.measure=+b.dataset.cutlistBar;s.scoreFocus={page:loc.page,measure:s.measure,instruments:b.dataset.instrument?[b.dataset.instrument]:scoreInstrumentIds};renderDemo();revealScoreMeasure();document.querySelector('.score-measure.chosen')?.focus({preventScroll:true});return true;
 }
 if(b.dataset.scoreSetting){const key=b.dataset.scoreSetting;if(!['scoreLinkInstruments','scoreSeeOtherTakes'].includes(key))return false;s[key]=s[key]===false;renderDemo();document.querySelector(`[data-score-setting="${key}"]`)?.focus({preventScroll:true});return true;}
 if(b.dataset.selectTake){if(event?.metaKey||event?.ctrlKey)toggleScoreComparison(s,b.dataset.selectTake);else selectScoreTake(s,b.dataset.selectTake);return true;}
 if(b.hasAttribute('data-score-workflow-later')){scoreWorkflowTiming(s).clock.offset+=120;const live=running(s);if(live)live.base+=120;syncScoreWorkflowClocks();return true;}
 if(b.hasAttribute('data-score-new-take')){newEmptyScoreTake(s);return true;}
 if(b.hasAttribute('data-score-undo')){undoScoreChange(s);return true;}
 if(b.hasAttribute('data-score-redo')){undoScoreChange(s,true);return true;}
 if(b.hasAttribute('data-score-clear-selection')){const t=takeById(s,s.selected);if(t&&scoreSelection(s,t).length){rememberScoreChange(s,t);t.scoreSelections[s.doc.id]=[];}renderDemo();return true;}
 if(b.hasAttribute('data-score-save-comment')){saveScoreComment(s);return true;}
 if(b.hasAttribute('data-score-cancel-comment')){const t=takeById(s,s.selected);if(t?.scoreCommentDrafts)delete t.scoreCommentDrafts[s.doc.id];s.scoreComment=null;renderDemo();return true;}
 if(b.hasAttribute('data-score-note-all')){s.scoreComment.instruments=[...scoreInstrumentIds];renderDemo();return true;}
 if(b.dataset.scoreNoteInstrument){const c=s.scoreComment,id=b.dataset.scoreNoteInstrument;c.instruments=c.instruments.length===4?[id]:c.instruments.includes(id)?c.instruments.filter(i=>i!==id):[...c.instruments,id];renderDemo();return true;}
 if(b.dataset.scoreNote||b.dataset.scoreMeasure)return true;
 return false;
}
function changeScoreSelection(s,keys,mode){
 const t=takeById(s,s.selected);if(!t){toast('Create a take before making a selection.');return;}
 const measures=scoreSelectionMeasures(keys),selection=s.scoreLinkInstruments===false?keys:measures.flatMap(m=>scoreInstrumentIds.map(i=>scoreCellKey(m,i)));
 const current=new Set(scoreSelection(s,t));for(const key of selection){if(mode==='remove')current.delete(key);else current.add(key);}
 const next=[...current].sort();if(JSON.stringify([...scoreSelection(s,t)].sort())===JSON.stringify(next))return;
 rememberScoreChange(s,t);t.scoreSelections[s.doc.id]=next;renderDemo();
}
function scorePoint(e,paper){const r=paper.getBoundingClientRect();return {x:Math.max(0,Math.min(1,(e.clientX-r.left)/r.width)),y:Math.max(0,Math.min(1,(e.clientY-r.top)/r.height))};}
let scoreGesture=null,ignoreScoreClickUntil=0;
function scoreGestureKeys(s,g){
 const left=Math.min(g.start.x,g.end.x),right=Math.max(g.start.x,g.end.x),top=Math.min(g.start.y,g.end.y),bottom=Math.max(g.start.y,g.end.y);
 const cells=scoreCells(s,g.page),hit=cells.filter(r=>right>=r.x&&left<=r.x+r.width&&bottom>=r.y&&top<=r.y+r.height);
 if(s.scoreLinkInstruments===false)return hit.map(c=>c.key);
 const measures=new Set(hit.map(c=>c.measure));return cells.filter(c=>measures.has(c.measure)).map(c=>c.key);
}
document.addEventListener('pointerdown',e=>{
 if(active?.id!=='partituur'||e.target.closest('.score-inline-editor'))return;
 const paper=e.target.closest('.score-paper');if(!paper||![0,2].includes(e.button)||!(e.metaKey||e.ctrlKey))return;
 if(!state().selected){toast('Create a take before making a selection.');return;}
 e.preventDefault();paper.setPointerCapture(e.pointerId);const start=scorePoint(e,paper);
 scoreGesture={paper,page:+paper.dataset.scorePage,pointer:e.pointerId,mode:e.button===2||e.altKey?'remove':'add',start,end:start,screenStart:{x:e.clientX,y:e.clientY},moved:false,all:e.shiftKey};
});
document.addEventListener('pointermove',e=>{
 if(!scoreGesture||scoreGesture.pointer!==e.pointerId)return;e.preventDefault();const g=scoreGesture;
 g.end=scorePoint(e,g.paper);g.all||=e.shiftKey;g.moved||=Math.hypot(e.clientX-g.screenStart.x,e.clientY-g.screenStart.y)>4;if(!g.moved)return;
 const box=g.paper.querySelector('.score-drag-rectangle');box.hidden=false;box.classList.toggle('is-removing',g.mode==='remove');
 Object.assign(box.style,{left:Math.min(g.start.x,g.end.x)*100+'%',top:Math.min(g.start.y,g.end.y)*100+'%',width:Math.abs(g.end.x-g.start.x)*100+'%',height:Math.abs(g.end.y-g.start.y)*100+'%'});
 const keys=new Set(scoreGestureKeys(state(),g));g.paper.querySelectorAll('[data-score-cell]').forEach(el=>el.classList.toggle('drag-cell-preview',keys.has(el.dataset.scoreCell)));
});
document.addEventListener('pointerup',e=>{
 if(!scoreGesture||scoreGesture.pointer!==e.pointerId)return;const g=scoreGesture;scoreGesture=null;
 e.preventDefault();g.end=scorePoint(e,g.paper);g.all||=e.shiftKey;state().page=g.page;
 ignoreScoreClickUntil=performance.now()+200;setTimeout(()=>{ignoreScoreClickUntil=0;},0);
 changeScoreSelection(state(),scoreGestureKeys(state(),g),g.mode);
 document.querySelectorAll('.drag-cell-preview').forEach(el=>el.classList.remove('drag-cell-preview'));document.querySelectorAll('.score-drag-rectangle').forEach(el=>el.hidden=true);
});
document.addEventListener('pointercancel',()=>{scoreGesture=null;document.querySelectorAll('.score-drag-rectangle').forEach(el=>el.hidden=true);document.querySelectorAll('.drag-cell-preview').forEach(el=>el.classList.remove('drag-cell-preview'));});
document.addEventListener('contextmenu',e=>{if(e.target.closest('.score-paper')&&(e.metaKey||e.ctrlKey||scoreGesture))e.preventDefault();});
function scoreNoteEvent(e){
 if(active?.id!=='partituur'||e.button!==0||e.metaKey||e.ctrlKey||e.target.closest('.score-inline-editor')||performance.now()<ignoreScoreClickUntil)return;
 const s=state(),noteButton=e.target.closest('[data-score-note]'),t=takeById(s,noteButton?.dataset.scoreTake||s.selected);
 if(noteButton){if(e.type==='dblclick')return;const n=t?.notes.find(n=>n.id===noteButton.dataset.scoreNote);if(s.scoreComment?.text.trim()&&s.scoreComment.editId!==n?.id){document.querySelector('#score-comment-text')?.focus({preventScroll:true});toast('Add or cancel your current note first.');return;}if(n){if(t.id!==s.selected)selectScoreTake(s,t.id,true);openScoreComment(s,n.measure,n.anchor||scoreNoteAnchor(s,n),n.page,n.instruments||scoreInstrumentIds,n);}return;}
 if(e.type!=='dblclick'&&e.detail!==0)return;
 const paper=e.target.closest('.score-paper');if(!paper)return;
 e.preventDefault();const page=+paper.dataset.scorePage;
 const targetCell=e.target.closest('[data-score-cell]'),cells=scoreCells(s,page);
 const candidate=targetCell?cells.find(c=>c.key===targetCell.dataset.scoreCell):null;
 const point=e.detail===0&&candidate?{x:candidate.x+candidate.width/2,y:candidate.y+candidate.height/2}:scorePoint(e,paper);
 const cell=cells.find(c=>point.x>=c.x&&point.x<=c.x+c.width&&point.y>=c.y&&point.y<=c.y+c.height);
 if(s.scoreComment?.text.trim()){document.querySelector('#score-comment-text')?.focus({preventScroll:true});toast('Add or cancel your current note first.');return;}
 if(!cell){openScoreComment(s,null,point,page,scoreInstrumentIds);return;}
 openScoreComment(s,cell.measure,point,page,e.shiftKey?scoreInstrumentIds:[cell.instrument]);
}
document.addEventListener('click',scoreNoteEvent);
document.addEventListener('dblclick',scoreNoteEvent);
document.addEventListener('input',e=>{
 if(active?.id!=='partituur'||!state().scoreComment)return;const c=state().scoreComment;
 if(e.target.id==='score-comment-text')c.text=e.target.value;
 if(e.target.id==='score-comment-measure'){const before=+c.measure;c.measure=e.target.value;const from=scoreCells(state(),c.page).find(r=>r.measure===before&&r.instrument===c.instruments[0]),loc=scoreLocation(c.source,c.measure);if(loc){const to=scoreCells(state(),loc.page).find(r=>r.measure===+c.measure&&r.instrument===c.instruments[0]);if(from&&to)c.anchor={x:to.x+Math.min(to.width*.8,Math.max(0,c.anchor.x-from.x)),y:to.y+Math.min(to.height*.8,Math.max(0,c.anchor.y-from.y))};c.page=loc.page;}}
});
document.addEventListener('keydown',e=>{
 if(active?.id!=='partituur')return;
 if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='z'&&!e.altKey&&!e.isComposing&&!e.target.closest('input,textarea,[contenteditable=true]')){e.preventDefault();e.stopImmediatePropagation();undoScoreChange(state(),e.shiftKey);return;}
 if(!state().scoreComment)return;
 if(e.key==='Escape'){e.preventDefault();e.stopImmediatePropagation();const s=state(),t=takeById(s,s.selected);if(t?.scoreCommentDrafts)delete t.scoreCommentDrafts[s.doc.id];s.scoreComment=null;renderDemo();return;}
 if(e.key==='Enter'&&!e.shiftKey&&!e.metaKey&&!e.ctrlKey&&!e.repeat&&!e.isComposing&&e.target.id==='score-comment-text'){e.preventDefault();saveScoreComment(state());}
},true);

function relocateScoreNote(n,value){
 const s=state(),loc=scoreLocation(n.source,value),before=scoreCells(s,n.page).find(c=>c.measure===n.measure&&c.instrument===(n.instruments?.[0]||'vln1'));
 if(!loc){n.anchor=null;return;}
 const after=scoreCells(s,loc.page).find(c=>c.measure===+value&&c.instrument===(n.instruments?.[0]||'vln1'));
 if(after)n.anchor={x:after.x+Math.max(0,Math.min(after.width*.8,n.anchor&&before?n.anchor.x-before.x:.01)),y:after.y+Math.max(0,Math.min(after.height*.8,n.anchor&&before?n.anchor.y-before.y:.01))};
}

// Drag the displayed text without changing its musical or take context.
let scoreNoteDrag=null;
function cancelScoreNoteDrag(){
 const g=scoreNoteDrag;if(!g)return;scoreNoteDrag=null;
 Object.assign(g.button.style,g.originalStyle);g.button.classList.remove('is-dragging');
 if(g.button.hasPointerCapture(g.pointer))g.button.releasePointerCapture(g.pointer);
}
document.addEventListener('pointerdown',e=>{
 if(active?.id!=='partituur'||e.button!==0||e.metaKey||e.ctrlKey||scoreNoteDrag)return;
 const button=e.target.closest('.score-text-annotation'),paper=button?.closest('.score-paper');if(!paper)return;
 const s=state(),t=takeById(s,button.dataset.scoreTake),n=t?.notes.find(n=>n.id===button.dataset.scoreNote);if(!n)return;
 if(s.scoreComment?.text.trim())return;
 const r=paper.getBoundingClientRect(),b=button.getBoundingClientRect();
 scoreNoteDrag={button,paper,pointer:e.pointerId,s,t,n,source:s.doc.id,start:{x:e.clientX,y:e.clientY},anchor:{x:(b.left-r.left)/r.width,y:(b.top-r.top)/r.height},originalStyle:{left:button.style.left,top:button.style.top},moved:false};
 button.setPointerCapture(e.pointerId);
});
document.addEventListener('pointermove',e=>{
 const g=scoreNoteDrag;if(!g||g.pointer!==e.pointerId)return;
 if(!g.button.isConnected||active?.id!=='partituur'||state()!==g.s||g.s.doc.id!==g.source){cancelScoreNoteDrag();return;}
 g.moved||=Math.hypot(e.clientX-g.start.x,e.clientY-g.start.y)>4;if(!g.moved)return;
 e.preventDefault();const r=g.paper.getBoundingClientRect(),b=g.button.getBoundingClientRect();
 g.end={x:Math.max(0,Math.min(Math.max(0,1-b.width/r.width),g.anchor.x+(e.clientX-g.start.x)/r.width)),y:Math.max(0,Math.min(Math.max(0,1-b.height/r.height),g.anchor.y+(e.clientY-g.start.y)/r.height))};
 g.button.classList.add('is-dragging');Object.assign(g.button.style,{left:g.end.x*100+'%',top:g.end.y*100+'%'});
});
document.addEventListener('pointerup',e=>{
 const g=scoreNoteDrag;if(!g||g.pointer!==e.pointerId)return;
 const valid=g.button.isConnected&&active?.id==='partituur'&&state()===g.s&&g.s.doc.id===g.source;
 cancelScoreNoteDrag();if(!g.moved||!valid)return;
 e.preventDefault();ignoreScoreClickUntil=performance.now()+200;setTimeout(()=>{ignoreScoreClickUntil=0;},0);
 if(g.end.x===g.anchor.x&&g.end.y===g.anchor.y)return;
 if(g.t.id!==g.s.selected)selectScoreTake(g.s,g.t.id,true);
 rememberScoreChange(g.s,g.t);g.n.anchor=g.end;g.n.placement='free';g.s.focusedScoreNote=g.n.id;renderDemo();
});
document.addEventListener('pointercancel',cancelScoreNoteDrag);
document.addEventListener('lostpointercapture',e=>{if(scoreNoteDrag?.pointer===e.pointerId)cancelScoreNoteDrag();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&scoreNoteDrag){e.preventDefault();e.stopImmediatePropagation();cancelScoreNoteDrag();}},true);
