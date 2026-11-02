// A compact reading score uses the same source and global zoom as Comp tool.
function reviewReferenceScore(s){
 const asset=scoreAsset(s.doc.id);if(!asset)return '<p>No reference score is available for this cue.</p>';
 return `<aside class="v3-reference-score" aria-label="Reference score beside notes"><header><b>${cues[s.cue][0]} · Score</b><div><button data-review-reference-zoom="out" aria-label="Zoom reference score out">−</button><span>${Math.round(s.zoom*100)}%</span><button data-review-reference-zoom="in" aria-label="Zoom reference score in">+</button><button data-review-reference-zoom="fit">Fit</button><button data-review-open-comp>Comp tool ↗</button></div></header><div class="v3-reference-pages" tabindex="0" aria-label="Continuous reference score">${Array.from({length:s.doc.pages},(_,i)=>{const img=asset===assets.production?asset.pageImages[i]:assets.production.bookImages[asset.bookPages[i]];return `<figure style="width:${1200*s.zoom}px"><img draggable="false" src="${img}" alt="${cues[s.cue][0]}, book page ${asset.bookPages[i]}" width="1200" height="1698"><figcaption>Book p. ${asset.bookPages[i]}</figcaption></figure>`;}).join('')}</div></aside>`;
}
reviewUpdates.push(()=>{
 if(sessionReview.feature!=='score'||reviewVariant('score')!=='A'||proposalView!=='recording')return;
 const workspace=document.querySelector('.v3-cue-workspace');if(workspace){workspace.classList.add('v3-with-reference');workspace.insertAdjacentHTML('beforeend',reviewReferenceScore(state()));}
});
document.addEventListener('click',e=>{
 const zoom=e.target.closest('[data-review-reference-zoom]');if(zoom){state().zoom=zoom.dataset.reviewReferenceZoom==='fit'?Math.max(.1,Math.min(3,(document.querySelector('.v3-reference-pages').clientWidth-16)/1200)):Math.max(.1,Math.min(3,Math.round((state().zoom+(zoom.dataset.reviewReferenceZoom==='in'?.1:-.1))*100)/100));renderDemo();return;}
 if(e.target.closest('[data-review-open-comp]')){showProposalView('cutlist');return;}
});
document.addEventListener('wheel',e=>{
 if(!e.ctrlKey||!e.target.closest('.v3-reference-pages'))return;e.preventDefault();state().zoom=Math.max(.1,Math.min(3,state().zoom*Math.exp(-e.deltaY*.01)));renderDemo();
},{passive:false});
