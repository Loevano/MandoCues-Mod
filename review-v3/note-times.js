// Keep the original writing instant separate from an editable note timestamp.
const reviewBaseNoteTime=noteTime,reviewBaseAddNote=addNote;
function reviewWrittenAt(n){
 if(n.id!=='draft')n.writtenAt??=n.clockAt??n.createdAt??null;
 return n.writtenAt;
}
noteTime=function(s,t,n,place){
 const original=reviewWrittenAt(n),template=document.createElement('template');
 template.innerHTML=reviewBaseNoteTime(s,t,n,place);
 const now=template.content.querySelector('[data-reset-note-time]'),restore=now.cloneNode(true);
 now.innerHTML='<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2v11M3 8l5 5 5-5"/></svg>';
 restore.removeAttribute('data-reset-note-time');restore.dataset.restoreNoteTime=n.id;
 restore.title='Restore original writing time';restore.setAttribute('aria-label','Restore original writing time for note: '+n.text);
 restore.disabled=original==null;now.after(restore);
 return template.innerHTML;
};
function reviewAnchorDraft(t){
 t.draft.writtenAt??=Date.now();t.draft.clockAt??=t.draft.writtenAt;
 document.querySelectorAll(`[data-restore-note-time="draft"][data-take="${t.id}"]`).forEach(button=>button.disabled=false);
}
document.addEventListener('input',event=>{
 const id=event.target.dataset.draft;if(!id||!event.target.value.trim())return;
 const t=takeById(state(),id);if(t)reviewAnchorDraft(t);
},true);
// Quick notes start writing too; capture their anchor before the original handler renders.
document.addEventListener('click',event=>{
 const button=event.target.closest('[data-quick-note]');if(button){const t=takeById(state(),button.dataset.take);if(t)reviewAnchorDraft(t);}
},true);
addNote=function(id,place){
 const s=state(),t=takeById(s,id),original=t?.draft.writtenAt??t?.draft.clockAt,serial=s.noteSerial;
 reviewBaseAddNote(id,place);
 if(t&&s.noteSerial!==serial)t.notes.at(-1).writtenAt=original??t.notes.at(-1).createdAt;
};
document.addEventListener('click',event=>{
 const button=event.target.closest('[data-restore-note-time]');if(!button)return;
 event.preventDefault();event.stopImmediatePropagation();
 const s=state(),t=takeById(s,button.dataset.take),n=t&&metadataNote(t,button.dataset.restoreNoteTime);
 if(!n||reviewWrittenAt(n)==null)return;
 if(n.id!=='draft')rememberScoreChange(s,t);
 n.clockAt=n.writtenAt;n.useTime=true;renderDemo();
 document.querySelector(`[data-restore-note-time="${n.id}"][data-take="${t.id}"][data-editor-place="${button.dataset.editorPlace}"]`)?.focus({preventScroll:true});
},true);
document.addEventListener('keydown',event=>{
 if(event.code!=='KeyN'||event.altKey||event.metaKey||event.ctrlKey||event.shiftKey||event.repeat||event.isComposing||proposalView!=='recording'||!navigationKeysAvailable(event)||reviewCueDrag)return;
 const t=takeById(state(),state().selected);if(!t)return;
 const editor=document.querySelector(`.calm-notes [data-draft="${t.id}"]`);if(!editor)return;
 event.preventDefault();event.stopImmediatePropagation();reviewAnchorDraft(t);
 document.querySelectorAll(`[data-draft-clock="${t.id}"]`).forEach(el=>setNoteTimeValue(el,noteTimeValue(t.draft)));
 editor.focus();editor.setSelectionRange(editor.value.length,editor.value.length);
},true);
renderDemo();
