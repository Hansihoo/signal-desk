/* Navigation and document rendering; source data is inserted as text only. */
(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('briefing-data').textContent);
  const $ = id => document.getElementById(id);
  const topics = data.topics || [];
  const items = data.items || [];
  const params = new URLSearchParams(window.location.search);
  const requestedReport = params.get('report');
  const report = requestedReport ? items.find(item => item.id === requestedReport) : null;
  const topicOf = item => topics.find(topic => item.topic_id ? topic.id === item.topic_id : topic.name === item.topic);
  const topicId = report ? topicOf(report)?.id : (data.selected_topic || params.get('topic') || '');
  const selectedTopic = topics.find(topic => topic.id === topicId);
  const categoryOf = item => item.category || '기타';
  const section = report ? categoryOf(report) : (selectedTopic ? params.get('section') || '' : '');
  const topicItems = topic => items.filter(item => topicOf(item)?.id === topic.id);
  const groups = topic => [...new Set(topicItems(topic).map(categoryOf))].map(name => ({
    name, items: topicItems(topic).filter(item => categoryOf(item) === name)
  })).sort((a, b) => b.items.length - a.items.length || a.name.localeCompare(b.name, 'ko'));
  const sortRecent = rows => [...rows].sort((a, b) =>
    String(b.published_at || b.first_seen_at).localeCompare(String(a.published_at || a.first_seen_at)) || b.score - a.score);
  const homeUrl = data.archived ? 'index.html' : data.prefix + 'index.html';
  const route = (topic, category = '', record = '') => {
    const query = new URLSearchParams();
    if (data.archived && topic) query.set('topic', topic.id);
    if (category) query.set('section', category);
    if (record) query.set('report', record);
    const base = data.archived ? 'index.html' : topic ? data.prefix + 'research/' + encodeURIComponent(topic.id) + '/index.html' : homeUrl;
    return base + (query.size ? '?' + query.toString() : '');
  };
  const recordUrl = item => route(topicOf(item), categoryOf(item), item.id);
  const safeUrl = value => {
    try { const url = new URL(value); return ['http:', 'https:'].includes(url.protocol) && !url.username && !url.password ? url.href : ''; }
    catch { return ''; }
  };
  const date = value => value ? String(value).slice(0, 10) : '미상';
  const timestamp = value => {
    const parsed = new Date(value);
    return Number.isNaN(parsed.getTime()) ? '미상' : parsed.toLocaleString('ko-KR', {timeZone: 'Asia/Seoul'}) + ' KST';
  };
  function node(tag, text = '', className = '') {
    const element = document.createElement(tag);
    element.textContent = text;
    if (className) element.className = className;
    return element;
  }
  function link(text, href, current = false, className = '') {
    const element = node('a', text, className);
    element.href = href;
    if (current) element.setAttribute('aria-current', 'page');
    return element;
  }
  function crumb(text, href) {
    if ($('breadcrumbs').childElementCount) $('breadcrumbs').append(node('span', '/'));
    const element = href ? link(text, href) : node('span', text, 'crumb-current');
    if (!href) element.setAttribute('aria-current', 'page');
    $('breadcrumbs').append(element);
  }
  function renderTree() {
    const root = node('ul');
    const home = node('li');
    home.append(link(data.archived ? '보관된 브리핑 메인' : '리서치 메인', homeUrl, !topicId && !requestedReport, 'tree-home'));
    root.append(home);
    for (const [index, topic] of topics.entries()) {
      const row = node('li'), branch = node('details', '', 'tree-topic'), heading = node('summary', topic.name);
      branch.open = topic.id === topicId || (!topicId && index === 0);
      heading.append(node('span', String(topic.count ?? topicItems(topic).length), 'tree-count'));
      const children = node('ul', '', 'tree-children'), overview = node('li');
      overview.append(link(topic.name + ' 전체 보기', route(topic), topic.id === topicId && !section && !requestedReport, 'tree-topic-link'));
      children.append(overview);
      for (const group of groups(topic)) {
        const subrow = node('li'), subbranch = node('details', '', 'tree-section'), subheading = node('summary', group.name);
        subheading.append(node('span', String(group.items.length), 'tree-count'));
        subbranch.open = topic.id === topicId && group.name === section;
        const records = node('ul', '', 'tree-records');
        const all = node('li');
        all.append(link(group.name + ' 기록 목록', route(topic, group.name), topic.id === topicId && section === group.name && !requestedReport, 'tree-all'));
        records.append(all);
        const leaves = sortRecent(group.items).slice(0, 4);
        if (report && group.items.includes(report) && !leaves.includes(report)) leaves.push(report);
        for (const item of leaves) {
          const leaf = node('li'), anchor = link('', recordUrl(item), item.id === requestedReport);
          anchor.append(node('span', item.title, 'tree-record-title'));
          leaf.append(anchor); records.append(leaf);
        }
        if (group.items.length > leaves.length) {
          const more = node('li');
          more.append(link('전체 ' + group.items.length + '건 보기', route(topic, group.name), false, 'tree-all')); records.append(more);
        }
        subbranch.append(subheading, records); subrow.append(subbranch); children.append(subrow);
      }
      branch.append(heading, children); row.append(branch); root.append(row);
    }
    $('research-tree').append(root);
    const mobile = window.matchMedia('(max-width: 900px)');
    $('tree-panel').open = !mobile.matches;
    mobile.addEventListener('change', event => { $('tree-panel').open = !event.matches; });
  }
  function directoryRow(index, title, description, href, count) {
    const row = node('div', '', 'directory-row'), body = node('div'), heading = node('h3');
    heading.append(link(title, href)); body.append(heading);
    if (description) body.append(node('p', description));
    row.append(node('span', String(index + 1).padStart(2, '0'), 'directory-number'), body, node('span', count + '건', 'directory-size'));
    return row;
  }
  function renderDirectory() {
    if (section || requestedReport) { $('directory').hidden = true; return; }
    if (selectedTopic) {
      const sections = groups(selectedTopic);
      $('directory-title').textContent = '하위 주제';
      $('directory-count').textContent = sections.length + '개 주제';
      for (const [index, group] of sections.entries()) {
        $('directory-list').append(directoryRow(index, group.name, '', route(selectedTopic, group.name), group.items.length));
      }
      if (!sections.length) $('directory-list').append(node('p', '아직 수집된 기록이 없습니다.', 'empty'));
    } else {
      $('directory-count').textContent = topics.length + '개 분야';
      for (const [index, topic] of topics.entries()) {
        $('directory-list').append(directoryRow(index, topic.name + ' 리서치', topic.description || '', route(topic), topic.count || 0));
      }
    }
  }
  function renderHealth() {
    const health = (data.health || []).filter(entry => !selectedTopic || entry.topic_id === selectedTopic.id);
    const warnings = health.filter(entry => !entry.ok || entry.warnings?.length);
    if (!warnings.length) return;
    const notice = node('details', '', 'notice');
    notice.append(node('summary', warnings.length + '개 출처에 수집 참고 사항이 있습니다'));
    for (const entry of warnings) notice.append(node('p', entry.source + ' · ' + (entry.ok ? entry.warnings.join(' / ') : entry.message)));
    $('health').append(notice);
  }
  function renderReport() {
    $('library').hidden = true; $('archive').hidden = true;
    if (!report) {
      $('not-found').hidden = false;
      $('page-title').textContent = '기록을 찾을 수 없습니다';
      $('description').textContent = data.archived ? '이 날짜의 보관본에 없는 기록입니다.' : '현재 분야에 없는 기록입니다.';
      return;
    }
    $('report').hidden = false;
    $('eyebrow').textContent = 'SOURCE NOTE / 수집 기록';
    $('page-title').textContent = report.title;
    $('description').textContent = [selectedTopic?.name, categoryOf(report)].filter(Boolean).join(' · ');
    const fields = [['출처', report.source], ['발행일', date(report.published_at)], ['자료 유형', report.basis || '원문 링크'], ['최초 수집', timestamp(report.first_seen_at)]];
    if (report.status) fields.push(['공고 상태', report.status]);
    for (const [label, value] of fields) {
      const field = node('div'); field.append(node('dt', label), node('dd', value)); $('report-meta').append(field);
    }
    $('report-summary').textContent = report.summary || '수집된 요약문이 없습니다. 아래 원문에서 내용을 확인해 주세요.';
    $('report-evidence').append(node('p', report.source + ' · ' + (report.basis || '원문 링크')));
    const url = safeUrl(report.url);
    if (url) {
      const source = link('원문 자료 열기 ↗', url);
      source.target = '_blank'; source.rel = 'noopener noreferrer'; $('report-evidence').append(source);
    }
    $('report-back').href = route(selectedTopic, categoryOf(report));
  }
  let mode = selectedTopic || data.archived ? 'all' : 'recent';
  let shown = 12;
  const cutoff = Date.parse(data.created_at) - 7 * 86400000;
  const isRecent = item => Date.parse(item.published_at || item.first_seen_at) >= cutoff;
  function renderRecords() {
    const keyword = $('search').value.trim().toLocaleLowerCase('ko-KR');
    const filterTopic = $('topic').value;
    const rows = sortRecent(items.filter(item =>
      (!filterTopic || topicOf(item)?.id === filterTopic) && (!section || categoryOf(item) === section) &&
      (mode === 'all' || isRecent(item)) && [item.title, item.summary, item.source, item.topic, item.category].join(' ').toLocaleLowerCase('ko-KR').includes(keyword)));
    $('items').replaceChildren();
    $('list-title').textContent = selectedTopic ? (section ? '주제의 기록' : '수집 기록') : mode === 'recent' ? '최근 기록' : '전체 기록';
    $('count').textContent = rows.length + '건';
    $('recent').setAttribute('aria-pressed', String(mode === 'recent'));
    $('all').setAttribute('aria-pressed', String(mode === 'all'));
    for (const item of rows.slice(0, shown)) {
      const row = node('article', '', 'record-row'), kicker = node('div', '', 'record-kicker'), heading = node('h3');
      kicker.append(node('span', item.topic + ' / ' + categoryOf(item), 'record-topic'), node('span', date(item.published_at || item.first_seen_at)), node('span', item.source));
      heading.append(link(item.title, recordUrl(item))); row.append(kicker, heading); $('items').append(row);
    }
    if (!rows.length) $('items').append(node('p', '조건에 맞는 기록이 없습니다. 검색어 또는 자료 범위를 바꿔 주세요.', 'empty'));
    $('more').hidden = rows.length <= shown;
  }

  $('brand-link').href = data.prefix + 'index.html';
  $('home-link').href = data.prefix + 'index.html';
  $('archive-link').href = requestedReport ? homeUrl + '#archive' : '#archive';
  $('updated').textContent = (data.archived ? '보관된 브리핑 · ' : '마지막 갱신 · ') + timestamp(data.created_at) + ' · ' + items.length + '건의 기록';
  if (topicId || requestedReport) crumb(data.archived ? '보관 메인' : '리서치 메인', homeUrl);
  else crumb(data.archived ? '보관된 브리핑' : '리서치 메인');
  if (selectedTopic) crumb(selectedTopic.name, section || requestedReport ? route(selectedTopic) : '');
  if (section) crumb(section, requestedReport ? route(selectedTopic, section) : '');
  if (requestedReport) crumb('개별 기록');
  if (selectedTopic && !requestedReport) {
    $('eyebrow').textContent = section ? 'RESEARCH SUBJECT' : 'RESEARCH TOPIC';
    $('page-title').textContent = section || selectedTopic.name + ' 리서치';
    $('description').textContent = section ? selectedTopic.name + ' 분야의 ' + section + ' 자료를 모읍니다.' : selectedTopic.description || '이 분야의 수집 기록을 모읍니다.';
  } else if (!requestedReport) {
    $('page-title').textContent = data.archived ? data.date + ' 브리핑' : '리서치 메인';
    $('description').textContent = '분야별 자료를 모으고, 주제를 따라 기록을 읽는 리서치 아카이브입니다.';
  }
  renderTree(); renderDirectory(); renderHealth();
  const invalidTopic = Boolean(topicId && !selectedTopic);
  const invalidSection = Boolean(section && selectedTopic && !groups(selectedTopic).some(group => group.name === section));
  if (requestedReport) renderReport();
  else if (invalidTopic || invalidSection) {
    $('directory').hidden = true; $('library').hidden = true; $('not-found').hidden = false;
    $('page-title').textContent = '주제를 찾을 수 없습니다';
  } else {
    for (const topic of topics.filter(topic => !data.selected_topic || topic.id === data.selected_topic)) {
      const option = node('option', topic.name); option.value = topic.id; $('topic').append(option);
    }
    $('topic').value = selectedTopic?.id || '';
    if (selectedTopic) $('topic').hidden = true;
    $('search').addEventListener('input', () => { shown = 12; renderRecords(); });
    $('topic').addEventListener('change', () => { shown = 12; renderRecords(); });
    for (const name of ['recent', 'all']) $(name).addEventListener('click', () => { mode = name; shown = 12; renderRecords(); });
    $('more').addEventListener('click', () => { shown += 12; renderRecords(); });
    renderRecords();
  }
  for (const entry of data.history || []) $('archive-list').append(link(entry.date + ' · ' + entry.count + '건', data.prefix + 'archive/' + entry.date + '/index.html'));
  document.title = 'Signal Desk · ' + $('page-title').textContent;
})();
