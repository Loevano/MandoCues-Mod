// Score is a recording/annotation view. Comp remains intact in the preserved v3.
const v4ScoreBaseView=productionScoreView,v4ScoreBaseTakeList=scoreTakeList;
scoreComparisonLayers=function(){return '';};
scoreSettings=function(s){return `<div class="score-settings" role="group" aria-label="Score display">${!s.doc.url?scorePageLayoutMenu(s)+scoreZoomControls(s):''}</div>`;};
productionScoreView=function(s){
 s.cutlistView='score';const template=document.createElement('template');template.innerHTML=v4ScoreBaseView(s);
 template.content.querySelectorAll('.score-measure').forEach(cell=>{cell.classList.remove('in-take-selection');cell.setAttribute('aria-pressed','false');});
 return template.innerHTML;
};
// Keep the saved comp data; suppress edits and colored selection rendering only here.
changeScoreSelection=function(){return;};
document.addEventListener('pointerdown',event=>{
 if(proposalView!=='cutlist'||!(event.metaKey||event.ctrlKey)||!event.target.closest('.score-paper')||event.target.closest('.score-note-text,.score-inline-editor'))return;
 event.stopImmediatePropagation();
},true);
chooseScoreTake=function(s,id){selectScoreTake(s,id,false,true);};
scoreVisibleTakes=function(s){const t=takeById(s,s.selected);return t?[t]:[];};
scoreTakeList=function(s,options){
 const template=document.createElement('template');template.innerHTML=v4ScoreBaseTakeList(s,{...options,newButton:false});
 template.content.querySelector('.score-compare-help')?.remove();
 template.content.querySelectorAll('.score-take-row').forEach(row=>{
  const id=row.querySelector('[data-select-take]').dataset.selectTake,t=takeById(s,id);
  row.insertAdjacentHTML('beforeend',`<button class="v4-score-range" data-v4-edit-take-range="${id}" title="Edit take bars">${v4RangeLabel(t.barRange)}</button>`);
 });return template.innerHTML;
};
scoreSidebar=function(s){
 const t=takeById(s,s.selected),p=v4Forecast(s);
 return `<aside class="score-notes cutlist-sidebar v4-score-sidebar">${scoreCueOverview(s)}<div class="v4-score-timing"><span>Cue left <b data-v4-compact-cue>${(p.cueLeft<0?'−':'')+v4Duration(Math.abs(p.cueLeft))}</b></span><button data-v4-edit-cue="${s.cue}">Cue timing</button></div><div class="v4-score-next-range">${v4RangeControls(s)}</div>${scoreTakeList(s)}${t?`<section class="v4-score-composer"><header><b>${entryLabel(t)} · Notes</b><small>${shortcutText('N · Enter')}</small></header>${composer(s,t,false,'v4-score')}${scoreNoteList(s,t)}</section>`:'<p class="notes-empty">Start a take to write notes.</p>'}</aside>`;
};
const v4ScoreBaseRender=renderDemo;
renderDemo=function(){
 v4ScoreBaseRender();document.querySelectorAll('[data-proposal-view="cutlist"]').forEach(b=>{b.textContent='Score';b.setAttribute('aria-label','Score view');});
 document.querySelector('.proposal-workspace-title').textContent=proposalView==='cutlist'?'Score':'Recording';
 const title=document.querySelector('.proposal-demo-label');if(title)title.textContent='Local v4 prototype · no audio is recorded';
};
const v4ScoreBaseShow=showProposalView;
showProposalView=function(view,options={}){const target=view==='score'?'cutlist':view;v4ScoreBaseShow(target,options);if(options.navigate!==false)history.replaceState(null,'',target==='cutlist'?'#score':'#recording');};
route=function(){if(!document.querySelector('.proposal-shell'))mountProposal();showProposalView(['score','cutlist','partituur'].includes(location.hash.slice(1))?'score':'recording',{navigate:false});};
document.addEventListener('keydown',event=>{
 if(event.code!=='KeyN'||proposalView!=='cutlist'||event.metaKey||event.ctrlKey||event.altKey||event.shiftKey||event.repeat||event.isComposing||!navigationKeysAvailable(event)||state().scoreComment)return;
 const t=takeById(state(),state().selected),editor=document.querySelector('[data-draft][data-editor-place="v4-score"]');if(!t||!editor)return;
 event.preventDefault();event.stopImmediatePropagation();reviewAnchorDraft(t);editor.focus();editor.setSelectionRange(editor.value.length,editor.value.length);
},true);
// Preserve the first-letter anchor when a positioned score note is edited.
const v4SaveScoreComment=saveScoreComment;
saveScoreComment=function(s){const c=s.scoreComment,t=takeById(s,c?.take),old=t?.notes.find(n=>n.id===c?.editId),writtenAt=old?.writtenAt??c?.clockAt;v4SaveScoreComment(s);if(c&&t&&!s.scoreComment){const n=t.notes.find(n=>n.id===c.editId)||t.notes.at(-1);if(n)n.writtenAt=writtenAt??n.clockAt;}};
route();
