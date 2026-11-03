/* Pure planning functions: no browser, clock, transport or note dependencies. */
const V4Planning=(()=>{
 const weights={Easy:.7,Medium:1,Hard:1.5};
 const clamp=(n,min,max)=>Math.max(min,Math.min(max,n));
 const positive=n=>Number.isFinite(n)?Math.max(0,n):0;
 function workload(cue){return positive(cue.musicSeconds)*(weights[cue.complexity]??1);}
 function initialRate(cues,seconds,prep){
  const total=cues.reduce((sum,cue)=>sum+workload(cue),0);
  return total?Math.max(0,seconds-prep*cues.filter(c=>c.musicSeconds>0).length)/total:0;
 }
 function learning(cues,rate,prep,complexity=null){
  const samples=cues.filter(c=>c.done&&c.include!==false&&c.workedSeconds>0&&workload(c)>0&&rate>0);
  let sum=0,weight=0;
  for(const cue of samples){
   const ratio=clamp((cue.workedSeconds-prep)/(rate*workload(cue)),.25,4);
   const w=Math.min(1,cue.musicSeconds/60)*(complexity&&complexity!==cue.complexity?.toString()? .5:1);
   sum+=Math.log(ratio)*w;weight+=w;
  }
  // Three cue-equivalents of prior evidence keep one unusual cue from dominating.
  return {factor:Math.exp(sum/(3+weight)),samples:samples.length,weight};
 }
 function forecast(cues,{rate,prepSeconds,availableSeconds}){
  const learned=learning(cues,rate,prepSeconds);
  const rows=cues.map(cue=>{
   const factor=learning(cues,rate,prepSeconds,cue.complexity).factor;
   const estimate=cue.musicSeconds>0?prepSeconds+rate*workload(cue)*factor:0;
   const reserve=cue.musicSeconds>0?Math.max(30,Math.min(prepSeconds,estimate*.1)):0;
   const remaining=cue.done?0:cue.remainingOverride!=null?positive(cue.remainingOverride):Math.max(reserve,estimate-positive(cue.workedSeconds));
   return {...cue,estimate,remaining,reserve,factor};
  });
  const remaining=rows.reduce((sum,row)=>sum+row.remaining,0);
  // A budget is what fits; an estimate is what we expect. Never collapse the two.
  const budget=Math.max(0,availableSeconds);
  for(const row of rows)row.suggestedBudget=remaining?budget*row.remaining/remaining:0;
  return {rows,remaining,delta:Math.round(remaining-availableSeconds),...learned};
 }
 return {weights,workload,initialRate,learning,forecast};
})();
if(typeof module!=='undefined')module.exports=V4Planning;
