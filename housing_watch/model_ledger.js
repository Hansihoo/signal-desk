(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('model-ledger-data').textContent);
  const $ = id => document.getElementById(id);
  const columns = [
    ['model','모델 / 설정'],['provider','개발사'],['kind','자료 구분'],['effort','추론 설정'],['release','출시'],['status','제공 상태'],['access','이용 방식'],
    ['context','Context (토큰)'],['parameters','총 Params'],['active_parameters','활성 Params (B)'],['harness','Agent / Harness'],['harness_version','Harness 버전'],
    ['agent_index','Coding Agent Index ↑'],['deep_swe','DeepSWE (%) ↑'],['agent_terminal','Agent Terminal (%) ↑'],['swe_atlas','SWE-Atlas-QnA (%) ↑'],
    ['agent_tokens','Agent 토큰 / task'],['agent_minutes','Agent 분 / task'],['agent_turns','Agent Turns / task'],['agent_cost','Agent USD / task'],
    ['intelligence','AA Intelligence ↑'],['briefcase','AA-Briefcase (Elo) ↑'],['automation','Automation (%) ↑'],['model_terminal','AA Terminal (%) ↑'],['scicode','SciCode (%) ↑'],
    ['model_cost','AA USD / task'],['lcr','AA-LCR (%) ↑'],['cursor_score','CursorBench (%) ↑'],['cursor_cost','Cursor USD / task'],['cursor_tokens','Cursor 토큰 / task'],['cursor_steps','Cursor Steps / task'],
    ['public_coding','공개 코딩 실측'],['q4_load','Q4 모델 로드'],['q4_ram','Q4 권장 RAM'],['q8_load','Q8 모델 로드'],['fp16_load','FP16/BF16 로드'],
    ['unassisted','무개입 완료율 (%)'],['regression_free','회귀 없는 성공률 (%)'],['success_cost','성공당 총비용 (USD)'],['condition','평가 조건'],['checked_on','원자료 날짜'],['note','설명 / 주의'],['suite','평가판'],['basis','근거 수준'],['tier','원본 상대 구간']
  ];
  const labels = Object.fromEntries(columns);
  Object.assign(labels, {benchmark_versions:'평가 항목별 버전',harness_versions:'평가별 Harness 버전 범위',
    estimated_intelligence:'추정 AA Intelligence · 실측 제외',fallback_models:'대체 모델 (fallback)',retained_attempts:'평가 시도 수'});
  const presets = {
    integrated: ['model','provider','kind','effort','context','harness','intelligence','agent_index','cursor_score','condition','checked_on'],
    spec: ['model','provider','release','kind','status','access','parameters','context','q4_load','q4_ram','q8_load','fp16_load','note','checked_on'],
    model: ['model','provider','effort','context','intelligence','briefcase','automation','model_terminal','scicode','model_cost','lcr','condition','checked_on'],
    agent: ['model','provider','effort','harness','agent_index','deep_swe','agent_terminal','swe_atlas','agent_tokens','agent_minutes','agent_turns','agent_cost','condition','checked_on'],
    cursor: ['model','provider','effort','cursor_score','cursor_cost','cursor_tokens','cursor_steps','condition','checked_on']
  };
  const numeric = new Set(['agent_index','deep_swe','agent_terminal','swe_atlas','agent_tokens','agent_minutes','agent_turns','agent_cost','intelligence','briefcase','automation','model_terminal','scicode','model_cost','lcr','cursor_score','cursor_cost','cursor_tokens','cursor_steps','unassisted','regression_free','success_cost']);
  const percent = new Set(['deep_swe','agent_terminal','swe_atlas','automation','model_terminal','scicode','lcr','cursor_score','unassisted','regression_free']);
  const costs = new Set(['agent_cost','model_cost','cursor_cost','success_cost']);
  const searchFields = ['label','kind','effort','harness','condition','suite','note','access','status','fallback_models'];
  let visible = new Set(presets.integrated), page = 1, sortKey = 'model', direction = 1, filtered = [];
  const pageSize = 25;
  const records = data.records;
  const harnessName = value => ({codex:'Codex','claude-code':'Claude Code'}[value] || value);
  const modelLabel = row => row.fields.label || row.model + (row.fields.effort?' ('+row.fields.effort+')':'');
  const get = (row,key) => ['model','provider','checked_on'].includes(key) ? row[key] : key==='modelLabel' ? modelLabel(row) : key==='harness' ? harnessName(row.fields.harness) : key==='effort' ? row.fields.effort?.toLowerCase() : row.fields[key];
  const missing = value => value == null || value === '' || /^(—|미확인|미측정|미공개)$/.test(String(value));
  function display(value, key) {
    if (missing(value)) return value && value !== '—' ? value : '—';
    if (key==='harness') value=harnessName(value);
    if (Array.isArray(value)) return value.join(', ') || '없음';
    if (typeof value === 'object') return JSON.stringify(value);
    if (typeof value !== 'number') return String(value);
    if (key==='context' || key.includes('tokens')) return value.toLocaleString('en-US',{maximumFractionDigits:0});
    if (key==='parameters' || key==='active_parameters') return value.toLocaleString('en-US') + 'B';
    return (costs.has(key)?'$':'') + value.toLocaleString('en-US',{maximumFractionDigits:2}) + (percent.has(key)?'%':'');
  }
  function node(tag, text, className) {
    const item = document.createElement(tag);
    if (text != null) item.textContent = text;
    if (className) item.className = className;
    return item;
  }
  function link(url,text) {
    const a=node('a',text); a.href=url; a.rel='noopener'; a.target='_blank'; return a;
  }
  function options(id, values) {
    [...new Set(values.filter(Boolean))].sort((a,b)=>String(a).localeCompare(String(b))).forEach(value=> {
      const option=node('option',value); option.value=value; $(id).append(option);
    });
  }
  options('model-provider',records.map(r=>r.provider));
  options('model-effort',records.map(r=>get(r,'effort')));
  options('model-harness',records.map(r=>get(r,'harness')));
  options('model-access',records.map(r=>r.fields.access));
  options('model-state',records.map(r=>r.fields.status));
  options('model-tier',records.map(r=>r.fields.tier));
  function renderColumns() {
    const box=$('model-columns'); box.replaceChildren(node('legend','모델 이름은 항상 표시합니다.'));
    columns.filter(([key])=>key!=='model').forEach(([key,label])=> {
      const wrapper=node('label'), input=node('input'); input.type='checkbox';input.checked=visible.has(key);input.value=key;
      input.addEventListener('change',()=> {input.checked?visible.add(key):visible.delete(key);renderTable();});
      wrapper.append(input,node('span',label));box.append(wrapper);
    });
  }
  function filter() {
    const terms=$('model-query').value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    const provider=$('model-provider').value, effort=$('model-effort').value, harness=$('model-harness').value, kind=$('model-kind').value, older=$('model-older').checked;
    const access=$('model-access').value, status=$('model-state').value, tier=$('model-tier').value;
    const local=$('model-local').checked, aa=$('model-aa').checked;
    filtered=records.filter(row=> {
      const legacy=row.source_kind.startsWith('legacy');
      return (older || (!legacy && !row.retained)) && (!provider || row.provider===provider) && (!effort || get(row,'effort')===effort) &&
        (!harness || get(row,'harness')===harness) && (!kind || (kind==='legacy'?legacy:kind===row.source_kind)) &&
        (!access || row.fields.access===access) && (!status || row.fields.status===status) && (!tier || row.fields.tier===tier) &&
        (!local || row.original?.attributes?.['data-local']==='1' || row.fields.local===true) &&
        (!aa || row.original?.attributes?.['data-aa']==='1' || ['model','agent','legacy-model','legacy-agent','legacy-agent-guide'].includes(row.source_kind)) &&
        terms.every(term=>(row.model+' '+row.provider+' '+searchFields.map(key=>row.fields[key]||'').flat().join(' ')).toLowerCase().includes(term));
    });
    page=1;renderTable();
  }
  function sortValue(row,key) {
    let value=get(row,key);
    if (key==='model') return get(row,'modelLabel');
    if (missing(value)) return null;
    if (numeric.has(key) && typeof value==='string') {
      const match=value.replace(/,/g,'').match(/[-+]?\d*\.?\d+/);
      if (!match) return null;
      value=Number(match[0]);
      if (key==='agent_tokens' && /M/.test(get(row,key))) value*=1e6;
    }
    return value;
  }
  function orderedColumns() { return columns.filter(([key])=>visible.has(key)); }
  function renderTable() {
    filtered.sort((a,b)=> {
      const av=sortValue(a,sortKey),bv=sortValue(b,sortKey);
      if (av==null || bv==null) return av==null?(bv==null?0:1):-1;
      const result=typeof av==='number'&&typeof bv==='number'?av-bv:String(av).localeCompare(String(bv),'ko',{numeric:true});
      return result*direction || a.model.localeCompare(b.model);
    });
    const selected=orderedColumns(), pages=Math.max(1,Math.ceil(filtered.length/pageSize));page=Math.min(page,pages);
    $('model-column-count').textContent='· '+selected.length+'개';
    $('model-count').textContent=filtered.length.toLocaleString()+'개 기록 / 누적 '+records.length.toLocaleString()+'개';
    const head=node('tr');
    selected.forEach(([key,label])=> {
      const th=node('th'),button=node('button',label+(sortKey===key?(direction===1?' ↑':' ↓'):''));button.type='button';th.scope='col';
      th.setAttribute('aria-sort',sortKey===key?(direction===1?'ascending':'descending'):'none');
      button.addEventListener('click',()=> {direction=sortKey===key?-direction:1;sortKey=key;renderTable();});th.append(button);head.append(th);
    });
    $('model-table').tHead.replaceChildren(head);
    const body=$('model-table').tBodies[0];body.replaceChildren();
    filtered.slice((page-1)*pageSize,page*pageSize).forEach(row=> {
      const tr=node('tr');tr.dataset.recordId=row.id;
      selected.forEach(([key])=> {
        const cell=node('td');cell.dataset.key=key;
        if (key==='model') {
          const button=node('button',get(row,'modelLabel'),'model-name');button.type='button';button.addEventListener('click',()=>detail(row));
          cell.append(button,node('small',row.fields.suite || row.fields.kind));
          if(row.retained)cell.append(node('small','원본에서 빠짐 · 이전 정보 보존','model-retained'));
        } else cell.textContent=display(get(row,key),key);
        if(row.tips[key])cell.title=row.tips[key];
        tr.append(cell);
      });body.append(tr);
    });
    $('model-empty').hidden=filtered.length>0;
    $('model-page').textContent=page+' / '+pages;
    $('model-prev').disabled=page<=1;$('model-next').disabled=page>=pages;$('model-csv').disabled=!filtered.length;
  }
  function detail(row) {
    $('model-detail-title').textContent=get(row,'modelLabel');
    const box=$('model-detail-body');box.replaceChildren();
    const dateLabel=row.source_kind==='legacy-model'?'원문 기준일':row.source_kind==='workload'?'측정일':'원문 확인일';
    box.append(node('p',row.fields.kind+' · '+(row.checked_on?dateLabel+' '+row.checked_on:'행별 확인일 미명시')+' · '+row.revision+'차 기록'));
    const evidence=node('div',null,'model-evidence');evidence.append(link(row.source_url,'자료 원문'));
    (row.fields.references || []).forEach((url,index)=>evidence.append(link(url,'근거 '+(index+1))));box.append(evidence);
    const fields=node('dl',null,'model-detail-fields');
    Object.entries(row.fields).filter(([key])=>key!=='references'&&key!=='label').forEach(([key,value])=> {
      fields.append(node('dt',labels[key] || key),node('dd',display(value,key)));
    });box.append(fields);
    const history=node('div',null,'model-detail-history');history.append(node('h3','이 모델·설정의 변경 기록'));
    const editions=data.history.filter(item=>item.id===row.id).sort((a,b)=>b.revision-a.revision);
    editions.forEach(item=> {
      const article=node('article');article.append(node('strong',item.revision+'차 · '+item.saved_at.replace('T',' ').replace('Z',' UTC')));
      article.append(node('p',item.revision===1?'최초 저장':(item.changed_fields.map(key=>labels[key]||key).join(', ') || '출처·원본 확인일 변경')));
      const previous=editions.find(entry=>entry.revision===item.revision-1);
      if(previous) {
        const changes=node('dl',null,'model-detail-fields');
        item.changed_fields.forEach(key=>changes.append(node('dt',labels[key]||key),node('dd',display(previous.fields[key],key)+' → '+display(item.fields[key],key))));
        if(previous.checked_on!==item.checked_on)changes.append(node('dt','원본 확인일'),node('dd',(previous.checked_on||'미명시')+' → '+(item.checked_on||'미명시')));
        article.append(changes);
      }
      const disclosure=node('details'),pre=node('pre',JSON.stringify(item.original,null,2),'model-detail-raw');
      disclosure.append(node('summary','이 판의 원본 값'),pre);article.append(disclosure);history.append(article);
    });box.append(history);
    $('model-detail').showModal();
  }
  $('model-detail-close').addEventListener('click',()=>$('model-detail').close());
  $('model-filters').addEventListener('submit',event=>event.preventDefault());
  $('model-query').addEventListener('input',filter);
  ['model-provider','model-effort','model-harness','model-kind','model-older','model-access','model-state','model-tier','model-local','model-aa'].forEach(id=>$(id).addEventListener('change',()=> {
    if($('model-kind').value==='legacy')$('model-older').checked=true;filter();
  }));
  function preset(name) {
    visible=new Set(presets[name]);
    document.querySelectorAll('[data-preset]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.preset===name)));
    $('model-kind').value=['model','agent','cursor'].includes(name)?name:'';
    if(name==='spec')$('model-kind').value='spec';
    renderColumns();filter();
  }
  document.querySelectorAll('[data-preset]').forEach(button=>button.addEventListener('click',()=>preset(button.dataset.preset)));
  $('model-reset').addEventListener('click',()=> {$('model-filters').reset();document.querySelector('.model-columns').open=false;sortKey='model';direction=1;preset('integrated');});
  $('model-prev').addEventListener('click',()=>{page--;renderTable();});
  $('model-next').addEventListener('click',()=>{page++;renderTable();});
  $('model-csv').addEventListener('click',()=> {
    const selected=orderedColumns();
    const csvCell=value=> '"'+String(value).replace(/^[=+@-]/,"'$&").replaceAll('"','""')+'"';
    const rows=[selected.map(([,label])=>label),...filtered.map(row=>selected.map(([key])=>display(get(row,key==='model'?'modelLabel':key),key)))];
    const url=URL.createObjectURL(new Blob(['\ufeff'+rows.map(row=>row.map(csvCell).join(',')).join('\r\n')],{type:'text/csv;charset=utf-8'}));
    const a=node('a');a.href=url;a.download='llm-models.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  const latest=data.runs[0], successful=data.runs.find(run=>run.ok), status=$('model-status');
  if(successful) {
    const stats=successful.summary;status.append(node('strong','누적 '+records.length.toLocaleString()+'개 모델·설정 기록'));
    status.append(node('span',' · 마지막 동기화 '+successful.checked_at.replace('T',' ').replace('Z',' UTC')));
    status.append(node('div','이번 갱신: 신규 '+stats.inserted+' · 변경 '+stats.updated+' · 동일 '+stats.unchanged+' · 원본에서 빠진 기록 '+stats.retained+'개 보존'));
  }else status.append(node('span',records.length?'누적 '+records.length+'개 기록 · 원본 동기화 기록은 아직 없습니다.':'아직 가져온 모델 자료가 없습니다.'));
  if(latest && !latest.ok) {status.dataset.failed='true';status.append(node('div','최근 갱신 실패 · 이전 비교표를 유지하고 있습니다.'));}
  const initial=data.history.length?data.history.map(row=>row.saved_at).sort()[0]:null;
  const updates=data.history.filter(row=>row.revision>1 || row.saved_at!==initial).slice(0,30),changeBox=$('model-change-list');
  if(!updates.length)changeBox.append(node('p',records.length?'기준 자료를 저장했습니다. 이후 새 모델·변경 내용이 생기면 표시합니다.':'아직 변경 기록이 없습니다.'));
  const eventList=node('ul',null,'model-events');
  updates.forEach(row=> {
    const li=node('li'),button=node('button',(row.revision===1?'신규 · ':'변경 · ')+modelLabel(row));button.type='button';
    button.addEventListener('click',()=>detail(records.find(record=>record.id===row.id)));
    li.append(node('time',row.saved_at.replace('T',' ').replace('Z',' UTC')),button,node('p',row.fields.suite+' · '+(row.changed_fields.map(key=>labels[key]||key).join(', ')||'출처·확인일')));eventList.append(li);
  });changeBox.append(eventList);
  const runs=node('details',null,'model-sync-details'),runList=node('ul');runs.append(node('summary','최근 수집 상태'));
  data.runs.forEach(run=>runList.append(node('li',run.checked_at+' · '+(run.ok?'성공 · 신규 '+run.summary.inserted+' / 변경 '+run.summary.updated:'실패 · '+run.error))));runs.append(runList);changeBox.append(runs);
  const candidateBox=$('model-candidate-list'),candidates=node('ul',null,'model-candidate-rows');
  if(!data.candidates.length)candidateBox.append(node('p','수집된 새 모델 소식이 없습니다.'));
  data.candidates.forEach(item=> {
    const li=node('li');li.append(node('time',(item.published_at||'발표일 미표기')+' · '+item.source),link(item.url,item.title),node('p',item.summary));candidates.append(li);
  });candidateBox.append(candidates);
  renderColumns();filter();
})();
