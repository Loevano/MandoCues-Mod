// Comparison never changes the live take. Only the primary take is edited.
function scoreVisibleTakes(s){const ids=s.scoreCompared?.[s.cue]||[s.selected];return [...new Set([s.selected,...ids])].map(id=>takeById(s,id)).filter(t=>t&&t.cue===s.cue);}
function toggleScoreComparison(s,id){
 const t=takeById(s,id);if(!t||t.cue!==s.cue)return;
 s.scoreRangeAnchor??={};s.scoreRangeAnchor[s.cue]=id;
 const ids=scoreVisibleTakes(s).map(t=>t.id),on=ids.includes(id);
 if(on&&ids.length===1)return;
 const next=on?ids.filter(x=>x!==id):[...ids,id];s.scoreCompared??={};s.scoreCompared[s.cue]=next;
 const primary=on?(id===s.selected?next.at(-1):s.selected):id;
 if(primary!==s.selected)selectScoreTake(s,primary,true,true);else renderDemo();
}
function selectScoreRange(s,id,add=false){
 const takes=s.takes[s.cue],end=takes.findIndex(t=>t.id===id);if(end<0)return;
 const anchor=s.scoreRangeAnchor?.[s.cue]||s.selected,start=Math.max(0,takes.findIndex(t=>t.id===anchor));
 s.scoreRangeAnchor??={};s.scoreRangeAnchor[s.cue]=takes[start].id;
 const range=takes.slice(Math.min(start,end),Math.max(start,end)+1).map(t=>t.id);
 s.scoreCompared??={};s.scoreCompared[s.cue]=add?[...new Set([...scoreVisibleTakes(s).map(t=>t.id),...range])]:range;
 selectScoreTake(s,id,true,true);
}
function chooseScoreTake(s,id,event){
 if(event?.shiftKey)selectScoreRange(s,id,!!(event.metaKey||event.ctrlKey));
 else if(event?.metaKey||event?.ctrlKey)toggleScoreComparison(s,id);
 else selectScoreTake(s,id);
}
function scoreComparisonLayers(s,page){
 const visible=new Set(scoreVisibleTakes(s).map(t=>t.id));
 const layers=s.takes[s.cue].filter(t=>visible.has(t.id)||s.scoreSeeOtherTakes!==false).map(t=>({t,selection:new Set(scoreSelection(s,t))}));
 const regions=scoreRegions(s,page).flatMap(r=>{
  const partial=layers.some(l=>{const count=scoreInstrumentIds.filter(i=>l.selection.has(scoreCellKey(r.measure,i))).length;return count>0&&count<scoreInstrumentIds.length;});
  return partial?scoreCells(s,page).filter(c=>c.measure===r.measure):[r];
 });
 return `<div class="score-comparison-layer" aria-hidden="true">${regions.map(r=>{
  const explicit=layers.filter(l=>visible.has(l.t.id)&&l.selection.has(scoreCellKey(r.measure,r.instrument||scoreInstrumentIds[0]))),ghosts=layers.filter(l=>!visible.has(l.t.id)&&l.selection.has(scoreCellKey(r.measure,r.instrument||scoreInstrumentIds[0])));
  const shown=[...explicit,...ghosts];if(!shown.length)return '';
  const colours=shown.map(l=>`color-mix(in srgb,${scoreTakeColor(l.t)} ${visible.has(l.t.id)?34:23}%,transparent)`);
  const background=colours.length===1?colours[0]:`repeating-linear-gradient(135deg,${colours.map((c,i)=>`${c} ${i*10}px ${(i+1)*10}px`).join(',')})`;
  return `<div class="score-cut-range ${explicit.length?'compared-range':'ghost-range'} ${shown.length>1?'has-overlap':''}" data-cut-measure="${r.measure}" data-cut-takes="${shown.map(l=>l.t.id).join(' ')}" style="left:${r.x*100}%;top:${r.y*100}%;width:${r.width*100}%;height:${r.height*100}%;--range-color:${scoreTakeColor(shown[0].t)};background:${background}">${shown.map((l,i)=>`<i class="score-take-band ${visible.has(l.t.id)?'':'is-reference'}" data-range-take="${l.t.id}" style="top:${i*3}px;border-color:${scoreTakeColor(l.t)}"></i>`).join('')}</div>`;
 }).join('')}</div>`;
}
// Small image occupancy maps help keep added text out of existing printed marks.
const scoreInkMaps=new Map();
function scoreInkMap(image){
 if(!image?.complete||!image.naturalWidth)return null;const key=image.src;
 if(scoreInkMaps.has(key))return scoreInkMaps.get(key);
 const canvas=document.createElement('canvas');canvas.width=600;canvas.height=Math.round(600*image.naturalHeight/image.naturalWidth);
 const ctx=canvas.getContext('2d',{willReadFrequently:true});ctx.drawImage(image,0,0,canvas.width,canvas.height);
 const {width:w,height:h}=canvas,pixels=ctx.getImageData(0,0,w,h).data,prefix=new Uint32Array((w+1)*(h+1));
 for(let y=0;y<h;y++){let row=0;for(let x=0;x<w;x++){const p=(y*w+x)*4;row+=pixels[p]+pixels[p+1]+pixels[p+2]<600&&pixels[p+3]>128?1:0;prefix[(y+1)*(w+1)+x+1]=prefix[y*(w+1)+x+1]+row;}}
 const map={w,h,prefix};if(scoreInkMaps.size>12)scoreInkMaps.delete(scoreInkMaps.keys().next().value);scoreInkMaps.set(key,map);return map;
}
function scoreInkFraction(map,x,y,width,height){
 if(!map)return 0;const {w,h,prefix:p}=map,stride=w+1;
 const l=Math.max(0,Math.floor(x*w)),r=Math.min(w,Math.ceil((x+width)*w)),top=Math.max(0,Math.floor(y*h)),bottom=Math.min(h,Math.ceil((y+height)*h));
 return (p[bottom*stride+r]-p[top*stride+r]-p[bottom*stride+l]+p[top*stride+l])/Math.max(1,(r-l)*(bottom-top));
}
function scoreTextPlacements(s,page){
 const result=new Map(),placed=[],cells=scoreCells(s,page),a=scoreAsset(s.doc.id),labels=assets.production.staffLabels.find(p=>p.bookPage===a?.bookPages[page-1])?.labels||[];
 const image=document.querySelector(`.score-paper[data-score-source="${s.doc.id}"][data-score-page="${page}"] .production-score-image`),map=scoreInkMap(image);
 const measureCanvas=document.createElement('canvas').getContext('2d');measureCanvas.font='17px sans-serif';
 for(const t of scoreVisibleTakes(s))for(const n of t.notes.filter(n=>n.source===s.doc.id&&n.page===page)){
  const id=n.instruments?.length===4?'vln1':n.instruments?.[0]||'vln1',cell=cells.find(c=>c.measure===n.measure&&c.instrument===id);
  const anchor=n.anchor||cell&&{x:cell.x+.01,y:cell.y+.01};if(!anchor)continue;
  if(n.placement==='free'||!cell){result.set(t.id+':'+n.id,anchor);continue;}
  const label=labels.find(l=>l.instrument===id&&l.y>=cell.y-.005&&l.y<=cell.y+cell.height+.005),center=label?.y??cell.y+cell.height/2;
  const below=n.placement==='below',x=Math.max(cell.x+.003,Math.min(anchor.x,cell.x+cell.width-.015));
  const width=Math.min(.23,Math.max(.025,measureCanvas.measureText(n.text).width/1200)),height=Math.max(.012,Math.ceil(measureCanvas.measureText(n.text).width/(1200*.23))*.013);
  const preferred=below?center+.029:center-.032;
  let best={x,y:Math.max(.005,preferred)},bestScore=Infinity;
  for(let step=0;step<18;step++){
   const y=preferred+(below?1:-1)*step*.0035;
   if(y<Math.max(.005,cell.y-.022)||y+height>Math.min(.99,cell.y+cell.height+.015))continue;
   const blocked=placed.some(p=>x<p.x+p.width&&x+width>p.x&&y<p.y+p.height+.003&&y+height+.003>p.y);
   const score=scoreInkFraction(map,x,y,width,height)+(blocked?2:0)+step*.0007;
   if(score<bestScore){best={x,y};bestScore=score;}
   if(score<.004)break;
  }
  placed.push({...best,width,height});result.set(t.id+':'+n.id,best);
 }
 return result;
}
function refreshScoreTextPositions(){
 if(active?.id!=='partituur')return;
 const s=state();document.querySelectorAll('.score-paper').forEach(paper=>{
  const positions=scoreTextPlacements(s,+paper.dataset.scorePage);
  paper.querySelectorAll('.score-text-annotation').forEach(el=>{const a=positions.get(el.dataset.scoreTake+':'+el.dataset.scoreNote);if(a){el.style.left=a.x*100+'%';el.style.top=a.y*100+'%';}});
 });
}
document.addEventListener('load',e=>{if(e.target.matches?.('.production-score-image'))refreshScoreTextPositions();},true);
document.addEventListener('change',e=>{
 if(active?.id!=='partituur'||!state().scoreComment)return;const c=state().scoreComment;
 if(e.target.id==='score-comment-instrument'){c.instruments=e.target.value==='all'?[...scoreInstrumentIds]:[e.target.value];renderDemo();}
 if(e.target.id==='score-comment-placement'){c.placement=e.target.value;renderDemo();}
});
