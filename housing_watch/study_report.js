(() => {
  'use strict';
  const root = document.querySelector('.study-reader');
  const bar = root.querySelector('.study-toolbar');
  const menu = root.querySelector('#document-menu');
  const back = root.querySelector('#document-back');
  const chapters = [...root.querySelectorAll('.study-chapter[id^="chapter-"]')];
  const links = [...root.querySelectorAll('[data-section-link]')];
  const sameDocument = () => location.href.split('#')[0];
  const canBack = () => typeof window.navigation?.canGoBack === 'boolean' ? navigation.canGoBack : history.length > 1;
  function backState() {
    back.textContent = canBack() ? '← 뒤로' : '← 리서치 목록';
    back.setAttribute('aria-label', canBack() ? '이전 페이지 또는 읽기 위치로 돌아가기' : '리서치 목록으로 이동');
  }
  back.addEventListener('click', e => {
    if (e.button || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || !canBack()) return;
    e.preventDefault(); menu.open = false; history.back();
  });
  root.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    if (e.button || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
    history.replaceState({...history.state, studyPosition: {url:sameDocument(),y:scrollY}},'');
    menu.open = false;
    const target = document.getElementById(a.hash.slice(1));
    if (!target) return;
    for (let p=target.parentElement;p;p=p.parentElement) if (p.tagName==='DETAILS') p.open=true;
    const focus = target.querySelector('h2,h3') || target;
    requestAnimationFrame(() => {focus.setAttribute('tabindex','-1');focus.focus({preventScroll:true});});
  }));
  document.addEventListener('click',e=>{if(menu.open&&!menu.contains(e.target))menu.open=false;});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.open){e.stopImmediatePropagation();menu.open=false;menu.querySelector('summary').focus({preventScroll:true});}});
  let frame=false;
  function current(){
    frame=false;let active=null;const line=bar.getBoundingClientRect().height+38;
    for(const ch of chapters)if(ch.getBoundingClientRect().top<=line)active=ch.id;
    for(const a of links){const on=a.hash==='#'+active;a.classList.toggle('active',on);if(on)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');}
    root.querySelector('#document-current').textContent=active ? chapters.find(c=>c.id===active).querySelector('h2').textContent : '';
  }
  function schedule(){if(!frame){frame=true;requestAnimationFrame(current);}}
  addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule);
  for(const name of ['popstate','hashchange','pageshow'])addEventListener(name,()=>{menu.open=false;backState();schedule();});
  addEventListener('popstate',e=>{const pos=e.state?.studyPosition;if(pos?.url===sameDocument()&&Number.isFinite(pos.y))requestAnimationFrame(()=>requestAnimationFrame(()=>scrollTo({top:pos.y,behavior:'instant'})));});
  backState();schedule();
  root.querySelector('#study-print').addEventListener('click',()=>window.print());
  let openBeforePrint=[];
  addEventListener('beforeprint',()=>{openBeforePrint=[...root.querySelectorAll('details')].map(d=>[d,d.open]);openBeforePrint.forEach(([d])=>{if(d!==menu)d.open=true;});});
  addEventListener('afterprint',()=>openBeforePrint.forEach(([d,open])=>d.open=open));

  const tools=JSON.parse(root.parentElement.querySelector('#study-tools').textContent);
  if(!tools.length)return;
  const byId=new Map(tools.map(t=>[t.id,t]));
  const controls=root.querySelector('.catalog-controls');controls.hidden=false;
  root.querySelector('.catalog-help').hidden=false;
  const cards=[...root.querySelectorAll('.tool')];
  const query=root.querySelector('#tool-search'),field=root.querySelector('#tool-field'),tier=root.querySelector('#tool-tier');
  const selected=new Set();
  root.querySelectorAll('.tool-select').forEach(label=>label.hidden=false);
  function filter(){
    const words=query.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);let total=0;
    for(const card of cards){card.hidden=!words.every(w=>card.dataset.search.includes(w))||(field.value&&field.value!==card.dataset.field)||(tier.value&&tier.value!==card.dataset.tier);if(!card.hidden)total++;}
    root.querySelector('#tool-count').textContent=`${total}개 기술 / 전체 ${cards.length}개`;
    root.querySelector('#tool-empty').hidden=total!==0;
  }
  query.addEventListener('input',filter);field.addEventListener('change',filter);tier.addEventListener('change',filter);
  root.querySelector('#tool-reset').addEventListener('click',()=>{query.value=field.value=tier.value='';filter();query.focus({preventScroll:true});});
  function compare(){
    const section=root.querySelector('#tool-comparison');section.hidden=selected.size<2;
    const body=section.querySelector('tbody');body.replaceChildren();
    for(const id of selected){const t=byId.get(id),tr=document.createElement('tr');for(const [i,key] of ['name','reuse','jenkins','limits','license'].entries()){const td=document.createElement(i?'td':'th');if(!i)td.scope='row';td.textContent=t[key];tr.append(td);}body.append(tr);}
  }
  root.querySelectorAll('.tool-select input').forEach(box=>box.addEventListener('change',()=>{if(box.checked)selected.add(box.value);else selected.delete(box.value);compare();}));
  root.querySelector('#clear-comparison').addEventListener('click',()=>{selected.clear();root.querySelectorAll('.tool-select input').forEach(box=>box.checked=false);compare();});
  filter();
})();
