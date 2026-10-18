function scoreAsset(source){return source===assets.production.id?assets.production:assets.production.documents.find(d=>d.id===source);}
function canFollowMeasure(s,t){return s.doc.id==='example-v1'&&t.cue===0&&t.kind!=='overdub';}
function measureSourceHint(s,t){if(scoreAsset(s.doc.id))return 'No take timing anchors · choose a bar on the right';return measureSuggestion(s,t,t.draft.at??position(t))?'Demo mapping · bar remains editable':'No bar mapping · enter manually';}
function productionScoreDoc(cue='1M02'){
 const code=['1M09A','1M09B'].includes(cue)?'1M09AB':cue;
 const a=code==='1M02'?assets.production:assets.production.documents.find(d=>d.cue===code);
 return {id:a.id,name:a.name,url:null,pages:a.pages,production:true};
}
function schematicScoreDoc(){return {id:'example-v1',name:'Schematic demo score',url:null,pages:2};}
function scoreLocation(source,measure){
 const a=scoreAsset(source);
 if(a)return a.regions.find(r=>r.measure===+measure)||null;
 if(source==='example-v1'&&measure>=17&&measure<=32)return {page:Math.floor((measure-17)/8)+1};
 return null;
}
function syncSavedScorePage(n){
 if(scoreAsset(n.source)||n.source==='example-v1'){
  const loc=scoreLocation(n.source,n.measure);
  n.page=loc?.page??(n.anchor?n.page:null);n.bookPage=loc?.bookPage??null;
 }
}
function scoreSourceReference(n){const a=scoreAsset(n.source);return a&&n.page?`<small class="score-page-reference">Book p. ${a.bookPages[n.page-1]}</small>`:'';}
function switchScoreDocument(s,doc,redraw=true){
 rememberScoreView(s);
 s.scoreDrafts??={};
 s.scoreDrafts[s.doc.id]=Object.fromEntries(allTakes(s).map(t=>[t.id,{draft:{...t.draft},followMeasure:t.followMeasure}]));
 if(s.doc.url&&s.doc.url!==doc.url)URL.revokeObjectURL(s.doc.url);
 s.doc=doc;s.page=1;s.measure=null;s.zoom=1;s.scoreComment=null;
 for(const t of allTakes(s)){
  const previous=s.scoreDrafts[doc.id]?.[t.id];
  t.draft=previous?{...previous.draft}:draft();t.followMeasure=previous?.followMeasure??true;
 }
 restoreScoreView(s);
 if(redraw)renderDemo();
}
function revealScoreMeasure(){
 const s=state(),paper=document.querySelector(`.score-paper[data-score-page="${s.page}"]`),chosen=paper?.querySelector('.score-measure.chosen');
 (chosen||paper)?.scrollIntoView({block:'center',inline:'nearest',behavior:'auto'});
}
function scoreRegions(s,page=s.page){const a=scoreAsset(s.doc.id);return a?a.regions.filter(r=>r.page===page):s.doc.id==='example-v1'?Array.from({length:8},(_,n)=>({measure:17+(page-1)*8+n,page,x:(110+(n%4)*185)/900,y:(70+Math.floor(n/4)*225)/560,width:185/900,height:180/560})):[];}
function scoreNoteAnchor(s,n){
 if(n.anchor)return n.anchor;
 const ids=n.instruments||scoreInstrumentIds,cell=scoreCells(s,n.page).find(c=>c.measure===n.measure&&c.instrument===ids[0]);
 return cell?{x:cell.x+.01,y:cell.y+.01}:null;
}
function scoreSettings(s){
 const settings=[
  {key:'scoreLinkInstruments',label:'Link instruments',hint:'Select bars across all instruments',icon:'<path d="M10 13a5 5 0 0 0 7 .1l3-3a5 5 0 0 0-7-7l-2 2 M14 11a5 5 0 0 0-7-.1l-3 3a5 5 0 0 0 7 7l2-2"/>'},
  {key:'scoreSeeOtherTakes',label:'See other takes',hint:'Show background selections from other takes',icon:'<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>'}
 ];
 return `<div class="score-settings" role="group" aria-label="Score settings">${settings.map(({key,label,hint,icon})=>`<button type="button" data-score-setting="${key}" aria-label="${label}" aria-pressed="${s[key]!==false}" title="${label} · ${hint}"><svg viewBox="0 0 24 24" aria-hidden="true">${icon}</svg></button>`).join('')}</div>`;
}
function productionScoreView(s){
 const a=scoreAsset(s.doc.id),t=takeById(s,s.selected);
 if(s.doc.url)return `<section class="score-viewer cutlist-viewer">${scoreSettings(s)}<iframe class="pdf-native" title="Custom PDF score" src="${esc(s.doc.url)}#view=FitH"></iframe><p>No bar and staff regions have been mapped for this PDF.</p></section>`;
 const selected=scoreSelection(s,t);
 return `<section class="score-viewer cutlist-viewer" style="--take-color:${scoreTakeColor(t)}">${scoreSettings(s)}<div class="score-canvas">${Array.from({length:s.doc.pages},(_,index)=>{
  const page=index+1,cells=scoreCells(s,page),src=a===assets.production?assets.production.pageImages[index]:a?assets.production.bookImages[a.bookPages[index]]:null;
  const paper=a?`<img draggable="false" class="production-score-image" src="${src}" width="1200" height="1698" alt="${a.cue}, book page ${a.bookPages[index]}">`:assets.pages[index];
  const notes=t?.notes.filter(n=>n.source===s.doc.id&&n.page===page)||[];
  return `<div class="score-sheet" data-score-sheet="${page}"><div class="score-paper ${a?'production-score-paper':''}" data-score-source="${s.doc.id}" data-score-page="${page}" data-score-take="${t?.id||''}">${paper}${scoreComparisonLayers(s,page)}<div class="measure-overlays">${cells.map(c=>{
   const chosen=s.measure===c.measure&&(!s.scoreFocus||s.scoreFocus.page===page&&s.scoreFocus.instruments.includes(c.instrument));
   return `<button class="score-measure ${chosen?'chosen':''} ${selected.includes(c.key)?'in-take-selection':''}" style="left:${c.x*100}%;top:${c.y*100}%;width:${c.width*100}%;height:${c.height*100}%" data-score-measure="${c.measure}" data-score-instrument="${c.instrument}" data-score-cell="${c.key}" aria-label="Bar ${c.measure}, ${scoreInstrumentLabel([c.instrument])}" aria-pressed="${selected.includes(c.key)}"></button>`;
  }).join('')}</div><div class="score-drag-rectangle" hidden></div>${scorePageComments(s,t,page)}${scoreCommentDialog(s,page)}</div></div>`;
 }).join('')}</div><div class="cutlist-how"><p><b>Select a take on the left.</b> Each take has its own colour, bars and notes.</p><p><b>Cmd+left-click:</b> add bars. <b>Cmd+right-click:</b> remove bars. Dragging also works. ${s.scoreLinkInstruments===false?'Select bars per instrument.':'Linked instruments: selections cover all instruments.'}</p><p><b>Double-click:</b> write a note, then press Enter to place the text at that bar. Above the staff, or above the top staff for all instruments. Click a note to edit it. <b>Cmd+Z:</b> undo. Windows: Ctrl.</p></div><small class="cutlist-mapping-hint">${a===assets.production?'Arrival: checked bar regions.':a?'Bar regions are approximate; check the mapping.':'Schematic demo.'} Notes appear as text at their score position.</small></section>`;
}
