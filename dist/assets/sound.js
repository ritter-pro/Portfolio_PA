(()=>{
 const en=document.documentElement.lang==='en';
 const toggle=document.createElement('button');toggle.className='sound-toggle';toggle.type='button';toggle.setAttribute('aria-pressed','false');
 let enabled=false,ctx,lastHover=0,ambient;
 function label(){toggle.textContent=(enabled?'◉ ':'◎ ')+(en?'Sound: ':'Звук: ')+(enabled?(en?'on':'вкл.'):(en?'off':'выкл.'))}
 label();document.body.append(toggle);
 function tone(freq,duration=.12,volume=.025,delay=0){if(!enabled||!ctx||document.hidden)return;const t=ctx.currentTime+delay,o=ctx.createOscillator(),g=ctx.createGain();o.type='sine';o.frequency.setValueAtTime(freq,t);o.frequency.exponentialRampToValueAtTime(freq*.65,t+duration);g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(volume,t+.008);g.gain.exponentialRampToValueAtTime(.0001,t+duration);o.connect(g);g.connect(ctx.destination);o.start(t);o.stop(t+duration+.02)}
 toggle.addEventListener('click',async()=>{try{if(!ctx){ctx=new (window.AudioContext||window.webkitAudioContext)();ambient=ctx.createGain();ambient.gain.value=0;ambient.connect(ctx.destination);[82.41,123.47].forEach(f=>{const o=ctx.createOscillator();o.frequency.value=f;o.connect(ambient);o.start()})}enabled=!enabled;if(enabled)await ctx.resume();toggle.setAttribute('aria-pressed',String(enabled));label();ambient.gain.setTargetAtTime(enabled?.006:0,ctx.currentTime,.5);if(enabled){tone(523,.2,.022);tone(784,.3,.015,.12)}}catch{enabled=false;label();toggle.disabled=true;toggle.textContent=en?'Sound unavailable':'Звук недоступен'}});
 document.addEventListener('pointerover',e=>{if(e.pointerType==='touch'||!e.target.closest('a,button')||!enabled)return;const now=performance.now();if(now-lastHover<180)return;lastHover=now;tone(600,.065,.009)});
 document.addEventListener('click',e=>{if(e.target.closest('a,button')&&!e.target.closest('.sound-toggle'))tone(440,.14,.022)});
 document.addEventListener('pa:scene',()=>{tone(330,.32,.013);tone(660,.26,.009,.09)});
 document.addEventListener('pa:model-ready',()=>{tone(440,.2,.018);tone(660,.25,.015,.1);tone(880,.4,.01,.2)});
 document.addEventListener('visibilitychange',()=>{if(!ctx)return;if(document.hidden)ctx.suspend();else if(enabled)ctx.resume().catch(()=>{})});
})();
