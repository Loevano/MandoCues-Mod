function scoreAsset(source){return source===assets.production.id?assets.production:assets.production.documents.find(d=>d.id===source);}
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
 s.scoreDrafts[s.doc.id]=Object.fromEntries(allTakes(s).map(t=>[t.id,{draft:{...t.draft}}]));
 if(s.doc.url&&s.doc.url!==doc.url)URL.revokeObjectURL(s.doc.url);
 s.doc=doc;s.page=1;s.measure=null;s.zoom=1;s.scoreComment=null;
 for(const t of allTakes(s)){
  const previous=s.scoreDrafts[doc.id]?.[t.id];
  t.draft=previous?{...previous.draft}:draft();
 }
 restoreScoreView(s);
 if(redraw)renderDemo();
}
function revealScoreMeasure(){
 const s=state(),paper=document.querySelector(`.score-paper[data-score-page="${s.page}"]`),chosen=paper?.querySelector('.score-measure.chosen');
 const target=chosen||paper,canvas=paper?.closest('.score-canvas');
 if(target&&canvas)canvas.scrollTo({top:canvas.scrollTop+target.getBoundingClientRect().top-canvas.getBoundingClientRect().top-(canvas.clientHeight-target.getBoundingClientRect().height)/2,behavior:'auto'});
}
function scoreRegions(s,page=s.page){const a=scoreAsset(s.doc.id);return a?a.regions.filter(r=>r.page===page):s.doc.id==='example-v1'?Array.from({length:8},(_,n)=>({measure:17+(page-1)*8+n,page,x:(110+(n%4)*185)/900,y:(70+Math.floor(n/4)*225)/560,width:185/900,height:180/560})):[];}
function scoreNoteAnchor(s,n){
 if(n.anchor)return n.anchor;
 const ids=n.instruments||scoreInstrumentIds,cell=scoreCells(s,n.page).find(c=>c.measure===n.measure&&c.instrument===ids[0]);
 return cell?{x:cell.x+.01,y:cell.y+.01}:null;
}
function scoreZoomControls(s){
 const zoom=s.zoom||1;
 return `<div class="score-zoom-controls" role="group" aria-label="Score zoom"><button type="button" data-score-zoom="out" aria-label="Zoom out" title="Zoom out" ${zoom<=.5?'disabled':''}>−</button><output data-score-zoom-value aria-live="polite">${Math.round(zoom*100)}%</output><button type="button" data-score-zoom="in" aria-label="Zoom in" title="Zoom in" ${zoom>=3?'disabled':''}>+</button><button type="button" class="score-fit-width" data-score-zoom="fit" title="Fit score to width">Fit width</button></div>`;
}
function setScoreZoom(s,action,point=null){
 const canvas=document.querySelector('.score-canvas');if(!canvas)return;
 const viewport=canvas.getBoundingClientRect(),cx=point?.x??viewport.left+canvas.clientWidth/2,cy=point?.y??viewport.top+canvas.clientHeight/2;
 const papers=[...canvas.querySelectorAll('.score-paper')];
 const anchor=papers.find(p=>{const r=p.getBoundingClientRect();return r.top<=cy&&r.bottom>=cy;})||papers.find(p=>p.getBoundingClientRect().bottom>viewport.top)||papers[0];
 if(!anchor)return;
 const before=anchor.getBoundingClientRect(),x=Math.max(0,Math.min(1,(cx-before.left)/before.width)),y=Math.max(0,Math.min(1,(cy-before.top)/before.height));
 const requested=typeof action==='number'?action:action==='fit'?1:Math.round(((s.zoom||1)+(action==='in'?.25:-.25))*100)/100;
 s.zoom=Math.max(.5,Math.min(3,requested));
 canvas.style.setProperty('--score-zoom',s.zoom);
 refreshScoreTextPositions();
 const after=anchor.getBoundingClientRect();
 canvas.scrollTop+=after.top+after.height*y-cy;
 canvas.scrollLeft=action==='fit'?0:canvas.scrollLeft+after.left+after.width*x-cx;
 document.querySelectorAll('[data-score-zoom-value]').forEach(el=>el.textContent=Math.round(s.zoom*100)+'%');
 document.querySelectorAll('[data-score-zoom="out"]').forEach(el=>el.disabled=s.zoom<=.5);
 document.querySelectorAll('[data-score-zoom="in"]').forEach(el=>el.disabled=s.zoom>=3);
 rememberScoreView(s);
}
function scoreSettings(s){
 const settings=[
  {key:'scoreLinkInstruments',label:'Link instruments',hint:'Select bars across all instruments',icon:'<path d="M10 13a5 5 0 0 0 7 .1l3-3a5 5 0 0 0-7-7l-2 2 M14 11a5 5 0 0 0-7-.1l-3 3a5 5 0 0 0 7 7l2-2"/>'},
  {key:'scoreSeeOtherTakes',label:'See other takes',hint:'Show background selections from other takes',icon:'<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>'}
 ];
 return `<div class="score-settings" role="group" aria-label="Score settings">${active?.id==='partituur'?scoreViewSwitcher(s):''}${settings.map(({key,label,hint,icon})=>`<button type="button" data-score-setting="${key}" aria-label="${label}" aria-pressed="${s[key]!==false}" title="${label} · ${hint}"><svg viewBox="0 0 24 24" aria-hidden="true">${icon}</svg></button>`).join('')}${s.cutlistView!=='all'&&!s.doc.url?scoreZoomControls(s):''}</div>`;
}
function productionScoreView(s){
 if(active?.id==='partituur'&&s.cutlistView==='all')return scoreAllTakes(s);
 const a=scoreAsset(s.doc.id),t=takeById(s,s.selected);
 if(s.doc.url)return `<section class="score-viewer cutlist-viewer">${scoreSettings(s)}<iframe class="pdf-native" title="Custom PDF score" src="${esc(s.doc.url)}#view=FitH"></iframe></section>`;
 const selected=scoreSelection(s,t);
 return `<section class="score-viewer cutlist-viewer" style="--take-color:${scoreTakeColor(t)}">${scoreSettings(s)}<div class="score-canvas" style="--score-zoom:${s.zoom||1}">${Array.from({length:s.doc.pages},(_,index)=>{
  const page=index+1,cells=scoreCells(s,page),src=a===assets.production?assets.production.pageImages[index]:a?assets.production.bookImages[a.bookPages[index]]:null;
  const paper=a?`<img draggable="false" class="production-score-image" src="${src}" width="1200" height="1698" alt="${a.cue}, book page ${a.bookPages[index]}">`:assets.pages[index];
  const notes=t?.notes.filter(n=>n.source===s.doc.id&&n.page===page)||[];
  return `<div class="score-sheet" data-score-sheet="${page}"><div class="score-paper ${a?'production-score-paper':''}" data-score-source="${s.doc.id}" data-score-page="${page}" data-score-take="${t?.id||''}">${paper}${scoreComparisonLayers(s,page)}<div class="measure-overlays">${cells.map(c=>{
   const chosen=s.measure===c.measure&&(!s.scoreFocus||s.scoreFocus.page===page&&s.scoreFocus.instruments.includes(c.instrument));
   return `<button class="score-measure ${chosen?'chosen':''} ${selected.includes(c.key)?'in-take-selection':''}" style="left:${c.x*100}%;top:${c.y*100}%;width:${c.width*100}%;height:${c.height*100}%" data-score-measure="${c.measure}" data-score-instrument="${c.instrument}" data-score-cell="${c.key}" aria-label="Bar ${c.measure}, ${scoreInstrumentLabel([c.instrument])}" aria-pressed="${selected.includes(c.key)}"></button>`;
  }).join('')}</div><div class="score-drag-rectangle" hidden></div><div class="score-note-bar-preview" hidden aria-hidden="true"></div>${scorePageComments(s,t,page)}${scoreCommentDialog(s,page)}</div></div>`;
 }).join('')}</div></section>`;
}

// Trackpad pinch is a ctrl-wheel stream in Chromium and a gesture stream in Safari.
// Ordinary two-finger scrolling remains native and never changes zoom.
let scorePinchGesture=null;
document.addEventListener('wheel',event=>{
 const canvas=event.target.closest?.('.score-canvas');
 if(!canvas||!event.ctrlKey||active?.id!=='partituur')return;
 event.preventDefault();
 if(scorePinchGesture)return;
 const delta=event.deltaY*(event.deltaMode===1?16:event.deltaMode===2?canvas.clientHeight:1);
 setScoreZoom(state(),(state().zoom||1)*Math.exp(-Math.max(-80,Math.min(80,delta))*.01),{x:event.clientX,y:event.clientY});
},{passive:false});
document.addEventListener('gesturestart',event=>{
 const canvas=event.target.closest?.('.score-canvas');if(!canvas||active?.id!=='partituur')return;
 event.preventDefault();scorePinchGesture={canvas,zoom:state().zoom||1};
},{passive:false});
document.addEventListener('gesturechange',event=>{
 if(!scorePinchGesture)return;
 event.preventDefault();
 if(!scorePinchGesture.canvas.isConnected){scorePinchGesture=null;return;}
 if(Number.isFinite(event.scale))setScoreZoom(state(),scorePinchGesture.zoom*event.scale,{x:event.clientX,y:event.clientY});
},{passive:false});
document.addEventListener('gestureend',event=>{
 if(scorePinchGesture){event.preventDefault();scorePinchGesture=null;}
},{passive:false});
