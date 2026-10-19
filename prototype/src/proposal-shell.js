// Familiar application context, reconstructed from the supplied rendered HTML.
function appIcon(name){const paths={grid:'M3 3h7v7H3z M14 3h7v7h-7z M3 14h7v7H3z M14 14h7v7h-7z',music:'M9 18V5l11-2v13 M9 7l11-2 M9 18c0 4-6 4-6 1s6-4 6-1 M20 16c0 4-6 4-6 1s6-4 6-1',mic:'M9 3h6v10a3 3 0 0 1-6 0z M5 10v3a7 7 0 0 0 14 0v-3 M12 20v2',record:'M7 7a7 7 0 0 0 0 10 M17 7a7 7 0 0 1 0 10 M4 4a11 11 0 0 0 0 16 M20 4a11 11 0 0 1 0 16 M12 9v6',check:'M4 4h16v16H4z M7 11l4 4 6-8',chart:'M4 3v18h18 M8 15V9 M13 17V5 M18 17v-6',settings:'M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8 M9 3h6l1 3 3 1 2 5-2 5-3 1-1 3H9l-1-3-3-1-2-5 2-5 3-1z',sun:'M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10 M12 1v3 M12 20v3 M1 12h3 M20 12h3 M4 4l2 2 M18 18l2 2 M4 20l2-2 M18 6l2-2',exit:'M9 3H3v18h6 M10 12h11 M17 8l4 4-4 4',chat:'M3 4h18v13H8l-5 4z',pdf:'M5 2h9l5 5v15H5z M14 2v6h5 M8 15h8 M12 11v8',cup:'M4 8h13v7a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z M17 9h2a3 3 0 0 1 0 6h-2 M7 2v3 M12 2v3'};return `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="${paths[name]||paths.grid}"/></svg>`;}
function appSidebar(){return `<aside class="app-sidebar" lang="en" aria-label="Application navigation"><div class="app-brand"><span>MD</span><b>MandoCues</b></div><nav>${[['grid','Dashboard'],['music','Cues'],['mic','Sessions'],['record','Recording'],['check','Tasks'],['chart','Stats'],['settings','Settings']].map(([icon,label])=>`<button ${label==='Recording'?'aria-current="page"':'disabled'} title="${label}">${appIcon(icon)}<span>${label}</span></button>`).join('')}</nav><footer><button disabled>${appIcon('sun')}<span>Toggle theme</span></button><button disabled>${appIcon('exit')}<span>Sign out</span></button><div class="app-account"><i>F</i><div>Floris Heemskerk<small>florisheemskerk01@gmail.com</small></div></div></footer></aside>`;}
function proposalSessionHeader(s){return `<section class="proposal-session-header" aria-label="Recording session"><div class="session-choice"><label>Session<select data-session-select><option>String quartet · 20 October</option></select></label><span>20 October 2026 · 10:00 · Studio Hana</span></div><div class="session-setup"><label>Session length <span><input data-session-setting="length" type="number" min="15" max="1440" step="15" value="${s.booked}"> min <small data-session-hours>${Math.floor(s.booked/60)}h ${String(s.booked%60).padStart(2,'0')}m</small></span></label><label>Prep per cue <span><input data-session-setting="prep" type="number" min="0" max="60" value="${s.prepMinutes??3}"> min</span></label><label>Max music <span><input data-session-setting="music" type="number" min="0" max="1440" value="${s.maxMusicMinutes??60}" aria-label="Maximum minutes of music" title="Maximum total duration of music in this session"> min</span></label><div class="session-app-actions"><button data-app-action="add-cues">+ Add cues</button><button data-app-action="chat" aria-pressed="${!!s.chatOpen}">${appIcon('chat')} Chat</button><details class="session-pdf-menu"><summary>${appIcon('pdf')} PDF <span>⌄</span></summary><div><small>Export</small><button data-app-export="order">Recording order</button><button data-app-export="takes">Take sheet (for the mixer)</button></div></details></div></div></section>`;}
const proposalAvailableCues=[['1M04','Pool Flashback','01:15'],['1M08','Beach','00:47'],['1M12','Bankruptcy','01:29'],['1M19','52 Uur Eerder','02:11'],['1M25','Cave Talk','00:49'],['1M29','Harry Arrives','01:30'],['1M39','Wanted','01:55']];
function appDialog(title,content,actions=''){
 document.querySelector('.app-dialog')?.remove();const dialog=document.createElement('dialog');dialog.className='app-dialog';dialog.lang='en';dialog.innerHTML=`<header><h2>${title}</h2><button data-app-dialog-close aria-label="Close">×</button></header>${content}<footer><button data-app-dialog-close>Cancel</button>${actions}</footer>`;document.body.append(dialog);dialog.showModal();dialog.addEventListener('close',()=>dialog.remove(),{once:true});return dialog;
}
function openAddSessionCues(){
 const available=proposalAvailableCues.filter(c=>!cues.some(x=>x[0]===c[0]));
 appDialog('Add cues to this session',`<label class="add-cues-all"><input type="checkbox" data-add-cues-all> Select all (${available.length})</label><div class="add-cue-options">${available.map(c=>`<label><input type="checkbox" data-add-session-cue="${c[0]}"><b>${c[0]}</b><span>${esc(c[1])}</span><small>${c[2]}</small></label>`).join('')||'<p>All available cues are already in this session.</p>'}</div>`, '<button data-app-action="confirm-cues" disabled>Add cues</button>');
}
function renderSessionChat(){
 const s=unifiedState;document.querySelector('.session-chat')?.remove();if(!s.chatOpen)return;
 const panel=document.createElement('aside');panel.className='session-chat';panel.lang='en';panel.setAttribute('aria-label','Session chat');panel.innerHTML=`<header><b>${appIcon('chat')} Session chat</b><button data-app-action="chat" aria-label="Close session chat">×</button></header><div class="session-chat-messages">${(s.chatMessages||[]).map(m=>`<p><small>${esc(m.cue)} · ${esc(m.take)} · ${esc(m.time)}</small>${esc(m.text)}</p>`).join('')}</div><form data-session-chat-form><label>Message everyone<textarea aria-label="Session chat message" placeholder="Message everyone…"></textarea></label><button>Send</button></form>`;document.body.append(panel);
}
function openSessionExport(kind){
 document.querySelectorAll('.session-pdf-menu').forEach(el=>el.open=false);
 const body=kind==='takes'?cues.map((c,j)=>`<h3>${c[0]} ${esc(c[1])}</h3>${unifiedState.takes[j].map(t=>`<section><b>${entryLabel(t)}</b> · ${t.rating||'—'}/5${t.best?' · Best':''}<ul>${t.notes.map(n=>`<li>${esc(n.text)} · ${n.measureScope==='all'?'All':n.measure?'Bar '+n.measure:'—'} · ${noteTimeValue(n)}</li>`).join('')}</ul></section>`).join('')}`).join(''):`<table><thead><tr><th>Cue</th><th>Title</th><th>Music length</th><th>Planned (min)</th></tr></thead><tbody>${cues.map((c,j)=>`<tr><td>${c[0]}</td><td>${esc(c[1])}</td><td>${c[2]}</td><td>${cuePlannedMinutes(j)}</td></tr>`).join('')}</tbody></table>`;
 appDialog(kind==='takes'?'Take sheet':'Recording order',`<div class="session-export-preview">${body}</div>`,'<button data-app-action="print-export">Print / Save as PDF</button>');
}
document.addEventListener('click',event=>{
 const close=event.target.closest('[data-app-dialog-close]');if(close){close.closest('dialog').close();return;}
 const exp=event.target.closest('[data-app-export]');if(exp){openSessionExport(exp.dataset.appExport);return;}
 const action=event.target.closest('[data-app-action]')?.dataset.appAction;if(!action)return;
 if(action==='add-cues')openAddSessionCues();
 if(action==='chat'){unifiedState.chatOpen=!unifiedState.chatOpen;document.querySelector('[data-app-action="chat"][aria-pressed]')?.setAttribute('aria-pressed',unifiedState.chatOpen);renderSessionChat();}
 if(action==='print-export')window.print();
 if(action==='confirm-cues'){
  const selected=[...document.querySelectorAll('[data-add-session-cue]:checked')].map(el=>el.dataset.addSessionCue);
  for(const code of selected){const cue=proposalAvailableCues.find(c=>c[0]===code);if(!cue||cues.some(c=>c[0]===code))continue;cues.push([...cue]);unifiedState.takes.push([]);unifiedState.cueNotes.push([]);unifiedState.cueDrafts.push('');}
  document.querySelector('.app-dialog').close();renderDemo();
 }
});
document.addEventListener('change',event=>{
 if(event.target.matches('[data-add-cues-all]'))document.querySelectorAll('[data-add-session-cue]').forEach(el=>el.checked=event.target.checked);
 if(event.target.matches('[data-add-cues-all],[data-add-session-cue]'))document.querySelector('[data-app-action="confirm-cues"]').disabled=!document.querySelector('[data-add-session-cue]:checked');
 const key=event.target.dataset.sessionSetting;if(!key)return;const value=+event.target.value;
 if(!event.target.checkValidity()||!Number.isFinite(value))return;
 if(key==='length'){const timing=scoreWorkflowTiming(unifiedState);unifiedState.booked=value;timing.clock.booked=value*60;timing.clock.plannedEndAt=Date.now()+Math.max(0,value*60-timing.elapsed)*1000;document.querySelector('[data-session-hours]').textContent=Math.floor(value/60)+'h '+String(value%60).padStart(2,'0')+'m';}
 if(key==='prep')unifiedState.prepMinutes=value;
 if(key==='music')unifiedState.maxMusicMinutes=value;
 renderDemo();
});
document.addEventListener('submit',event=>{
 if(!event.target.matches('[data-session-chat-form]'))return;event.preventDefault();const field=event.target.querySelector('textarea'),text=field.value.trim();if(!text)return;
 const s=unifiedState,t=running(s)||takeById(s,s.selected);s.chatMessages??=[];s.chatMessages.push({text,cue:cues[s.cue][0],take:t?entryLabel(t):'',time:proposalClockTime(Date.now())});renderSessionChat();document.querySelector('[data-session-chat-form] textarea')?.focus();
});
