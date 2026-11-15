document.querySelectorAll('#year').forEach(el=>el.textContent=new Date().getFullYear());
const menuButton=document.querySelector('.menu-toggle');
const nav=document.querySelector('.nav');
menuButton?.addEventListener('click',()=>{const open=nav.classList.toggle('open');menuButton.setAttribute('aria-expanded',String(open));menuButton.textContent=open?'✕':'☰';});
nav?.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{nav.classList.remove('open');menuButton?.setAttribute('aria-expanded','false');}));
document.querySelectorAll('.nav-drop').forEach(d=>{const b=d.querySelector('.drop-btn');b?.addEventListener('click',()=>{const o=d.classList.toggle('open');b.setAttribute('aria-expanded',String(o));});d.addEventListener('keydown',e=>{if(e.key==='Escape'){d.classList.remove('open');b?.setAttribute('aria-expanded','false');b?.focus();}});});
document.addEventListener('click',e=>{document.querySelectorAll('.nav-drop.open').forEach(d=>{if(!d.contains(e.target)){d.classList.remove('open');d.querySelector('.drop-btn')?.setAttribute('aria-expanded','false');}});});

// "Keep your results" box under each tool. Runs in the browser; nothing is stored or sent by this site.
(function(){
  const SUB='https://airevolutionupdate.substack.com/subscribe';
  function textOf(el){return (el.innerText||el.textContent||'').replace(/\n{3,}/g,'\n\n').trim();}
  function makeBox(getText,label){
    const box=document.createElement('div');box.className='keep-box';
    box.innerHTML='<p class="keep-title">Keep your results</p>'+
      '<div class="keep-actions"><button type="button" class="btn secondary keep-copy">Copy my results</button></div>'+
      '<div class="keep-join"><p>Get my free newsletter on how AI is changing work, money and health care, and what you can do about it.</p><a class="btn primary" href="'+SUB+'" target="_blank" rel="noopener">Get my free newsletter →</a><small>Opens Substack, where the newsletter lives. Unsubscribe anytime.</small></div>';
    const cb=box.querySelector('.keep-copy');
    cb.addEventListener('click',()=>{
      const t=getText(); const done=()=>{cb.textContent='Copied ✓';setTimeout(()=>{cb.textContent='Copy my results';},2000);};
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,()=>{});}
    });
    return box;
  }
  document.querySelectorAll('.calc-result').forEach((el,i)=>{
    const watch=()=>{ if(textOf(el) && !el.querySelector('.calc-msg:only-child') && !el.nextElementSibling?.classList.contains('keep-box')){
      const card=el.closest('.step-card');
      const head=card?.querySelector('h3')?textOf(card.querySelector('h3'))+'\n\n':'';
      el.after(makeBox(()=>head+textOf(el),'r'+i)); } };
    new MutationObserver(watch).observe(el,{childList:true,subtree:true});
  });
  const sc=document.getElementById('score-card');
  if(sc){ new MutationObserver(()=>{ if(sc.querySelector('.result-start') && !sc.querySelector('.keep-box')){ sc.appendChild(makeBox(()=>{const c=sc.cloneNode(true);c.querySelector('.keep-box')?.remove();c.querySelectorAll('button,a.btn').forEach(b=>b.remove());return textOf(c);},'score')); } }).observe(sc,{childList:true}); }
})();

// Newsletter forms: clear feedback when the email is missing, and a backup link in case the new tab is blocked.
document.addEventListener('submit',e=>{
  const f=e.target; if(!f.matches('.keep-join,.join-form')) return;
  const inp=f.querySelector('input[type=email]');
  let msg=f.querySelector('.form-msg'); if(!msg){msg=document.createElement('p');msg.className='form-msg';msg.setAttribute('aria-live','polite');f.appendChild(msg);}
  const url=f.action+'?email='+encodeURIComponent(inp.value.trim());
  msg.innerHTML='Opening Substack in a new tab to finish signing up. If nothing opens, <a href="'+url+'" target="_blank" rel="noopener">click here</a>.';
},true);
document.addEventListener('invalid',e=>{
  const f=e.target.closest('.keep-join,.join-form'); if(!f) return;
  let msg=f.querySelector('.form-msg'); if(!msg){msg=document.createElement('p');msg.className='form-msg';msg.setAttribute('aria-live','polite');f.appendChild(msg);}
  msg.textContent='Please type your email address first.';
},true);

// Handle newsletter buttons by click too, so they still respond where form submission is blocked (for example, inside some previews).
document.addEventListener('click',e=>{
  const btn=e.target.closest('.keep-join button[type=submit],.join-form button[type=submit]'); if(!btn) return;
  const f=btn.closest('form'); const inp=f.querySelector('input[type=email]');
  let msg=f.querySelector('.form-msg'); if(!msg){msg=document.createElement('p');msg.className='form-msg';msg.setAttribute('aria-live','polite');f.appendChild(msg);}
  e.preventDefault();
  if(!inp.value.trim()||!inp.checkValidity()){msg.textContent='Please type your email address first.';inp.focus();return;}
  const url=f.action+'?email='+encodeURIComponent(inp.value.trim());
  let w=null; try{w=window.open(url,'_blank','noopener');}catch(err){}
  msg.innerHTML='Opening Substack to finish signing up. If a new tab didn\u2019t open, <a href="'+url+'" target="_blank" rel="noopener">click here to sign up</a>.';
},true);
