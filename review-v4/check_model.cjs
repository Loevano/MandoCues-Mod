const assert=require('node:assert/strict');
const M=require('./planning-model.js');
const cue=(id,musicSeconds=60,complexity='Medium',extra={})=>({id,musicSeconds,complexity,workedSeconds:0,done:false,...extra});
const input=[cue(0),cue(1,120),cue(2,60,'Hard')],prep=60,available=1800,rate=M.initialRate(input,available,prep);
const plan=(cues,availableSeconds=available)=>M.forecast(cues,{rate,prepSeconds:prep,availableSeconds});
let p=plan(input);
assert(Math.abs(p.remaining-available)<.001);
assert(p.rows[2].estimate>p.rows[0].estimate);
assert(p.rows[1].estimate>p.rows[2].estimate);
assert(Math.abs(p.rows.reduce((n,r)=>n+r.suggestedBudget,0)-available)<.001);
const done={...input[0],done:true,workedSeconds:p.rows[0].estimate*2};
const learned=plan([done,...input.slice(1)]);
assert(learned.factor>1&&learned.factor<2);
assert.equal(learned.samples,1);
assert(learned.rows[1].estimate>p.rows[1].estimate);
assert.equal(learned.rows[0].remaining,0);
assert.equal(plan([{...done,include:false},...input.slice(1)]).factor,1);
assert.equal(plan([{...done,done:false},...input.slice(1)]).factor,1);
// Changing a deadline reallocates available time without changing work estimates.
assert.equal(plan(input,900).remaining,p.remaining);
assert.equal(plan(input,2400).remaining,p.remaining);
assert(plan(input,900).delta>0);assert(plan(input,2400).delta<0);
// An unfinished cue cannot magically become complete at its forecast boundary.
assert(plan([cue(0,60,'Medium',{workedSeconds:100000})]).remaining>=30);
assert.equal(plan([cue(0,60,'Medium',{remainingOverride:0})]).remaining,0);
assert.equal(plan([cue(0,0)]).remaining,0);
assert.equal(plan([cue(0,60,'Medium',{done:true})]).remaining,0);
// A completed cue that was genuinely 1.5x slower at Hard normalizes as expected.
const hard=cue(1,60,'Hard',{done:true,workedSeconds:prep+rate*60*1.5});
assert(Math.abs(plan([hard, input[0]]).factor-1)<1e-10);
assert(plan([cue(0,60,'Medium',{done:true,workedSeconds:1e9}),...input.slice(1)]).factor<1.5);
assert(Number.isFinite(M.initialRate([],0,prep)));
assert.equal(plan([],0).delta,0);
assert.equal(plan(input,-300).delta,Math.round(p.remaining+300));
console.log('PASS workload/complexity, conserved allocation, shrunk completed-cue learning, exclusions, deadline independence and unfinished reserve');
