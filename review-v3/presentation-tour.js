// A short walkthrough of the accepted workspace, in session order.
const reviewTourById=new Map(proposalTourSteps.map(step=>[step.id,step]));
const reviewPlanStep={id:'sessieplan',title:'Cues kiezen en herschikken',
 text:'Kies een cue in het sessieplan. Sleep cues om de opnamevolgorde te veranderen; de cuelijst volgt mee.',
 target:'.cue-timeline',view:'recording',parts:[{id:'cuevolgorde',title:'Gedeelde opnamevolgorde',
 prompt:'Laat cues kiezen en herschikken via zowel het sessieplan als de sleepgreep in de cuelijst. Gebruik één opnamevolgorde voor beide en voor vorige/volgende cue en de opnamevolgorde-export. Verander geen cue-, take- of note-identiteiten. Bewaar de aparte natuurlijke cue-sortering als weergavesortering; daarin is slepen uitgeschakeld. Blokkeer herschikken tijdens een lopende take.'}]};
proposalTourSelection.add('cuevolgorde');
const cueStep=reviewTourById.get('cue-aanklikken');
cueStep.text='Klik een cue om zijn takes open te klappen. Kies een take; rechts zie je de notes die daarbij horen.';
const noteStep=reviewTourById.get('noteplek');
noteStep.text='Kies een take om zijn notes te lezen en schrijven. N opent het tekstveld en legt de kloktijd vast. Enter slaat op en zet een nieuwe note klaar.';
noteStep.prepare='sticky';
noteStep.inlineHelp={title:'Bediening blijft bereikbaar',text:'Bij scrollen blijven cue en start/stop bovenaan in beeld.'};
const stickyPart=removedTransportStep?.parts.find(part=>part.id==='bereikbare-bediening');
if(stickyPart)noteStep.parts.push(stickyPart);
noteStep.parts.push({id:'note-sneltoets',title:'N om een note te beginnen',prompt:'Laat N buiten tekstvelden in Recording het noteveld voor de gekozen take focussen en de oorspronkelijke kloktijd vastleggen. Bewaar een bestaand concept en zijn tijdanker. Voeg geen letter N in en maak niet ongemerkt een nieuwe take. Enter slaat op en opent een nieuw concept. Tijdens tekstinvoer blijft N gewone tekst; bescherm modifiers, modals, slepen en IME.'});
proposalTourSelection.add('note-sneltoets');
const metadataStep=reviewTourById.get('maat-aanpassen');
metadataStep.text='Bij het typen van de eerste letter wordt de kloktijd vastgelegd; met N leg je hem eerder vast. Kies zelf de maat. ↓ vult de huidige tijd in; het klokje herstelt het oorspronkelijke schrijfmoment.';
metadataStep.inlineHelp={title:'Voor later',text:'We kunnen kijken of notes met Pro Tools-opnames te synchroniseren zijn.'};
metadataStep.parts.find(part=>part.id==='protools-sync').prompt='Idee voor later: onderzoeken of notes via hun kloktijd aan Pro Tools-opnames te koppelen zijn. De route en haalbaarheid staan nog open. Bouw in deze ronde geen DAW-, AI- of importkoppeling.';
const metadataDiscussion=discussion.find(item=>item.id==='maat-aanpassen');
if(metadataDiscussion)metadataDiscussion.text='Bewaar de oorspronkelijke schrijfinstant apart van de aanpasbare kloktijd. Leg die vast bij de eerste letter of bij N om het noteveld te openen; leegmaken en opnieuw typen verandert het anker niet. Enter bewaart de note en opent een nieuw concept. Toon vóór en na Enter dezelfde directe maatkeuze en kloktijdbewerking. Naast de tijd staat eerst ↓ voor de huidige kloktijd en daarna het klokje om de oorspronkelijke schrijfinstant te herstellen. Handmatig aanpassen, verplaatsen en undo behouden het oorspronkelijke anker. Maatnummers blijven handmatig of bewust uit de score gekozen; geen gesimuleerd maatvolgen.';
reviewTourById.get('sterren').text='Zou 1–5 sterren met een filter handig zijn? Best markeert favoriete takes; Alt markeert reservetakes.';
const scoreStep=reviewTourById.get('view-toggle');
scoreStep.text='Kies links een take. Markeer passages uit verschillende takes op de partituur om een kniplijst samen te stellen.';
scoreStep.target='.score-paper';scoreStep.relatedTargets=['.score-take-picker'];
const scoreEditPart=reviewTourById.get('score-notes').parts.find(part=>part.id==='score-notes-bewerken');
scoreEditPart.prompt=scoreEditPart.prompt.replace('Een klein klokje vult de werkelijke huidige kloktijd in, ook tijdens typen of bij een oudere take.','Een pijl omlaag vult de werkelijke huidige kloktijd in; het klokje herstelt de oorspronkelijke schrijfinstant. Dit werkt vóór en na Enter en bij oudere takes.');
const order=['cue-aanklikken','sterren','noteplek','maat-aanpassen','planning','comp-tool-overgang','view-toggle','score-selecteren','score-notes','score-vergelijk'];
proposalTourSteps.splice(0,proposalTourSteps.length,reviewPlanStep,...order.map(id=>reviewTourById.get(id)));
proposalTourSuggestions.splice(0,proposalTourSuggestions.length,...proposalTourSteps.filter(step=>!step.transition));
proposalTourParts.splice(0,proposalTourParts.length,...proposalTourSteps.flatMap(step=>step.parts));
// Keep explicit opt-outs, including the transport part moved into the note step.
try{const saved=JSON.parse(localStorage.getItem(proposalTourStorageKey)||'null');if(Array.isArray(saved?.excluded))for(const id of saved.excluded)proposalTourSelection.delete(id);}catch{}
persistTourSelection();
const reviewShortcutText=shortcutText;
shortcutText=function(text){return reviewShortcutText(text).replace(/\bN\b/g,'<kbd class="keyboard-shortcut">N</kbd>');};

let reviewTourPosition=null,reviewTourDrag=null;
const reviewPositionTour=positionProposalTour,reviewOpenTourStep=openTourStep;
function reviewPlaceTourCard(card,x,y){
 const left=Math.max(8,Math.min(innerWidth-card.offsetWidth-8,x)),top=Math.max(8,Math.min(innerHeight-card.offsetHeight-8,y));
 Object.assign(card.style,{left:left+'px',top:top+'px'});return {x:left,y:top};
}
positionProposalTour=function(){
 reviewPositionTour();
 const card=document.querySelector('.proposal-tour-card');if(card&&reviewTourPosition)reviewTourPosition=reviewPlaceTourCard(card,reviewTourPosition.x,reviewTourPosition.y);
};
openTourStep=function(index){
 reviewTourPosition=null;reviewTourDrag=null;reviewOpenTourStep(index);
 const header=document.querySelector('.proposal-tour-card header');
 if(header)header.title='Sleep om te verplaatsen';
};
document.addEventListener('pointerdown',event=>{
 const header=event.target.closest('.proposal-tour-card header');
 if(!header||event.target.closest('button')||event.button!==0)return;
 const card=header.closest('.proposal-tour-card'),r=card.getBoundingClientRect();
 event.preventDefault();header.setPointerCapture(event.pointerId);
 reviewTourDrag={pointer:event.pointerId,x:event.clientX-r.left,y:event.clientY-r.top};
});
document.addEventListener('pointermove',event=>{
 const drag=reviewTourDrag,card=document.querySelector('.proposal-tour-card');if(!drag||!card||drag.pointer!==event.pointerId)return;
 event.preventDefault();reviewTourPosition=reviewPlaceTourCard(card,event.clientX-drag.x,event.clientY-drag.y);
});
document.addEventListener('pointerup',event=>{if(reviewTourDrag?.pointer===event.pointerId)reviewTourDrag=null;});
document.addEventListener('pointercancel',()=>reviewTourDrag=null);
