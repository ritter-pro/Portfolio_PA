(()=>{
 const en=document.documentElement.lang==='en',reduce=matchMedia('(prefers-reduced-motion: reduce)');
 document.querySelectorAll('.module-info').forEach(card=>{
  const b=card.querySelector('.module-expand');b.addEventListener('click',()=>{const open=card.classList.toggle('expanded');b.setAttribute('aria-expanded',String(open));b.textContent=open?(en?'Less −':'Свернуть −'):(en?'Details +':'Подробнее +')});
 });
 if(!('IntersectionObserver' in window))return;
 const nodes=[...document.querySelectorAll('.section>h2,.section-heading,.pack-story>div,.two-cols article,.timeline article,.passport-identity,.pack-index a,.module-info,.spec-panel,.contact-grid>a')];
 document.body.classList.add('cinema-ready');
 const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('cinema-visible');observer.unobserve(e.target)}}),{threshold:.07});
 nodes.forEach((node,i)=>{node.classList.add('cinema-item');node.style.setProperty('--cinema-delay',(node.matches('.module-info,.spec-panel,.contact-grid>a')?i%4*70:0)+'ms');if(reduce.matches||window.paMotion===false||node.getBoundingClientRect().top<innerHeight*.95)node.classList.add('cinema-visible');else observer.observe(node)});
 function showAll(){if(reduce.matches||window.paMotion===false)nodes.forEach(n=>{n.classList.add('cinema-visible');observer.unobserve(n)})}
 document.getElementById('motion')?.addEventListener('click',showAll);reduce.addEventListener('change',showAll);
})();
