// Best is independent per take, just like Alt and ratings.
document.addEventListener('click',event=>{
 const button=event.target.closest('[data-take-best]');if(!button||button.disabled)return;
 event.preventDefault();event.stopImmediatePropagation();
 const t=takeById(state(),button.dataset.takeBest);if(!t)return;
 t.best=!t.best;renderDemo();
},true);
const reviewBestDiscussion=discussion.find(item=>item.id==='alt-best');
if(reviewBestDiscussion){
 reviewBestDiscussion.title='Best en Alt per take';
 reviewBestDiscussion.bullet='Best voor favoriete takes; Alt voor reservetakes, los van de sterren.';
 reviewBestDiscussion.text=reviewBestDiscussion.text.replace('Maak Beste een toggle met maximaal één Beste per cue; een nieuwe Beste heft de vorige binnen die cue op.','Maak Best een onafhankelijke toggle per take; meerdere takes binnen dezelfde cue mogen Best zijn.');
}
