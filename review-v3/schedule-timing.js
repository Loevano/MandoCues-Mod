// Count cue work on the same second boundaries as session work. Independently
// flooring two differently anchored stopwatches produced a false one-second lag
// every second after switching cues, and discarded fractions at every switch.
const reviewBaseWorkflowTiming=scoreWorkflowTiming;
scoreWorkflowTiming=function(s){
 const timing=reviewBaseWorkflowTiming(s);if(!s.unified)return timing;
 const clock=timing.clock,actualNow=Date.now(),now=s.sessionPausedAt??actualNow;
 const sessionTicks=Math.floor((now-clock.started)/1000);
 const cueStartTick=Math.floor((clock.cueStarted-clock.started)/1000);
 const elapsed=clock.sessionBase+sessionTicks+clock.offset;
 const cueElapsed=clock.cueBase+sessionTicks-cueStartTick+clock.offset-clock.cueOffset;
 const breakTime=(clock.breakSeconds||0)+(s.sessionPausedAt?Math.floor((actualNow-s.sessionPausedAt)/1000):0);
 clock.remaining=cues.reduce((sum,_,j)=>sum+(s.cueSettings?.[j]?.complete?0:Math.max(0,cuePlannedMinutes(j)*60-(j===s.cue?cueElapsed:clock.cueSpent[j]||0))),0);
 return {...timing,elapsed,cueElapsed,delta:elapsed+clock.remaining-clock.booked+breakTime,remaining:Math.max(0,clock.booked-elapsed-breakTime)};
};
renderDemo();
