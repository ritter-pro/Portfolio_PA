// Local pointer light: shared by every page and both visual modes.
(()=>{
 const pointer=matchMedia('(any-hover: hover) and (any-pointer: fine)');
 const reducedMotion=matchMedia('(prefers-reduced-motion: reduce)');
 const halo=document.createElement('div');
 halo.className='cursor-halo';halo.setAttribute('aria-hidden','true');document.body.append(halo);
 let x=0,y=0,targetX=0,targetY=0,frame=0,visible=false,lastTime=0;
 const enabled=()=>pointer.matches&&!reducedMotion.matches&&window.paMotion!==false;
 function hide(){visible=false;halo.classList.remove('is-visible');cancelAnimationFrame(frame);frame=0;lastTime=0}
 function draw(time){
  frame=0;if(!visible||!enabled()){hide();return}
  const delta=lastTime?Math.min(time-lastTime,64):16;lastTime=time;
  const ease=1-Math.exp(-delta/45);x+=(targetX-x)*ease;y+=(targetY-y)*ease;
  halo.style.transform=`translate3d(${x}px,${y}px,0)`;
  halo.style.setProperty('--pointer-hue',String(175+Math.min(1,Math.max(0,x/innerWidth))*140));
  if(Math.abs(x-targetX)+Math.abs(y-targetY)>.15)frame=requestAnimationFrame(draw);else lastTime=0;
 }
 addEventListener('pointermove',event=>{
  if(event.pointerType==='touch'||!enabled()){hide();return}
  targetX=event.clientX;targetY=event.clientY;
  if(!visible){x=targetX;y=targetY;visible=true;halo.classList.add('is-visible')}
  halo.classList.toggle('over-control',!!event.target.closest('a,button,[role="button"]'));
  if(!frame)frame=requestAnimationFrame(draw);
 },{passive:true});
 document.documentElement.addEventListener('pointerleave',hide);addEventListener('blur',hide);
 document.addEventListener('visibilitychange',()=>{if(document.hidden)hide()});
 document.getElementById('motion')?.addEventListener('click',()=>{if(!enabled())hide()});
 pointer.addEventListener('change',hide);reducedMotion.addEventListener('change',hide);
})();
