(()=>{
 const data=JSON.parse(document.getElementById('pack-data').textContent),en=document.documentElement.lang==='en',base=en?'../assets/':'assets/';
 const screen=document.querySelector('.pack-screen'),stage=document.querySelector('.pack-stage'),shots=[...document.querySelectorAll('.pack-shot')],dots=[...document.querySelectorAll('[data-go]')],play=document.getElementById('pack-play'),bp=document.querySelector('.pack-blueprint');
 const reduce=matchMedia('(prefers-reduced-motion: reduce)'),fine=matchMedia('(hover:hover) and (pointer:fine)');
 let index=Math.max(0,data.findIndex(d=>d.slug===decodeURIComponent(location.hash.slice(1)))),auto=window.paMotion!==false&&!reduce.matches,hover=false,focus=false,visible=true,tapped=false,elapsed=0,last=0;
 function motion(){return window.paMotion!==false&&!reduce.matches}
 function playLabel(){const running=auto&&motion();play.setAttribute('aria-pressed',String(running));play.textContent=(running?'Ⅱ ':'▶ ')+(running?(en?'Pause':'Пауза'):(en?'Play':'Запустить'))}
 function inspect(on){stage.classList.toggle('inspecting',on)}
 function show(next,manual=false){
  index=(next+data.length)%data.length;elapsed=0;screen.style.setProperty('--slide-progress',0);tapped=false;inspect(false);const d=data[index];
  shots.forEach((s,i)=>{s.classList.toggle('current',i===index);s.classList.toggle('previous',i===(index-1+data.length)%data.length);s.classList.toggle('next',i===(index+1)%data.length);s.tabIndex=i===index?0:-1;s.setAttribute('aria-hidden',String(i!==index));if(i===index||i===(index+1)%data.length){const im=s.querySelector('img');if(im.dataset.srcset)im.srcset=im.dataset.srcset;if(im.dataset.src)im.src=im.dataset.src;im.loading='eager';delete im.dataset.src;delete im.dataset.srcset}});
  dots.forEach((d,i)=>d.setAttribute('aria-current',String(i===index)));
  screen.style.setProperty('--pack-color',d.color);bp.src=base+'packaging/'+d.slug+'-drawing.svg';
  document.getElementById('pack-brand').textContent=d.brand;
  document.getElementById('pack-name').textContent=d[en?'titleEn':'title'];document.getElementById('pack-short').textContent=d[en?'shortEn':'short'];document.getElementById('pack-description').textContent=d[en?'designEn':'design'];document.querySelector('.pack-case-link').href='pack-'+d.slug+'.html';
  document.getElementById('pack-count').textContent=String(index+1).padStart(2,'0')+' / '+String(data.length).padStart(2,'0');document.querySelector('.pack-watermark').textContent=String(index+1).padStart(2,'0');
  if(manual){history.replaceState(null,'','#'+d.slug);document.dispatchEvent(new Event('pa:scene'))}
 }
 shots.forEach((s,i)=>{s.addEventListener('pointerenter',()=>{if(fine.matches&&i===index)inspect(true)});s.addEventListener('focus',()=>inspect(true));s.addEventListener('click',()=>{if(i!==index)return;if(!fine.matches&&!tapped){tapped=true;inspect(true);return}location.href='pack-'+data[index].slug+'.html'})});
 stage.addEventListener('pointerenter',()=>hover=true);stage.addEventListener('pointerleave',()=>{hover=false;if(!tapped)inspect(false)});
 screen.addEventListener('focusin',e=>focus=stage.contains(e.target));screen.addEventListener('focusout',e=>{focus=stage.contains(e.relatedTarget)});
 document.getElementById('pack-prev').onclick=()=>show(index-1,true);document.getElementById('pack-next').onclick=()=>show(index+1,true);dots.forEach(d=>d.onclick=()=>show(+d.dataset.go,true));
 play.onclick=()=>{auto=!auto;elapsed=0;playLabel()};document.getElementById('motion')?.addEventListener('click',playLabel);
 stage.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();show(index+(e.key==='ArrowRight'?1:-1),true)}});
 let touchX=0,touchY=0,swiped=false;stage.addEventListener('touchstart',e=>{touchX=e.touches[0].clientX;touchY=e.touches[0].clientY;swiped=false},{passive:true});stage.addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-touchX,dy=e.changedTouches[0].clientY-touchY;if(Math.abs(dx)>60&&Math.abs(dx)>Math.abs(dy)*1.5){swiped=true;show(index+(dx<0?1:-1),true)}},{passive:true});stage.addEventListener('click',e=>{if(swiped){e.stopImmediatePropagation();e.preventDefault();swiped=false}},true);
 new IntersectionObserver(e=>visible=e[0].isIntersecting,{threshold:.25}).observe(screen);
 function tick(t){const dt=last?Math.min(t-last,100):0;last=t;if(auto&&motion()&&!hover&&!focus&&!tapped&&visible&&!document.hidden){elapsed+=dt;screen.style.setProperty('--slide-progress',Math.min(1,elapsed/4000));if(elapsed>=4000)show(index+1)}requestAnimationFrame(tick)}
 reduce.addEventListener('change',playLabel);show(index);playLabel();requestAnimationFrame(tick);
})();
