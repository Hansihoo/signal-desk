/* Editorial adaptation: native menu and a progressively enhanced report board. */
(() => {
  const sidebar = document.getElementById('sidebar');
  const toggle = sidebar.querySelector('.toggle');
  const narrow = matchMedia('(max-width: 1280px)');
  function menu(open) {
    sidebar.classList.toggle('inactive', !open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? '목차 닫기' : '목차 열기');
    sidebar.querySelector('.inner').inert = !open;
  }
  menu(!narrow.matches);
  narrow.addEventListener('change', () => menu(!narrow.matches));
  toggle.addEventListener('click', () => menu(sidebar.classList.contains('inactive')));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && !sidebar.classList.contains('inactive')) { menu(false); toggle.focus(); }
  });
  document.addEventListener('click', e => {
    if (narrow.matches && !sidebar.contains(e.target)) menu(false);
  });
  document.querySelectorAll('.citation').forEach(link => link.addEventListener('click', () => {
    const target = document.getElementById(link.hash.slice(1));
    if (target) { target.setAttribute('tabindex', '-1'); requestAnimationFrame(() => target.focus({preventScroll: true})); }
  }));
  const board = document.getElementById('board');
  if (!board) return;
  const rows = [...board.querySelectorAll('.research-post')];
  const query = board.querySelector('[name="q"]');
  const topic = board.querySelector('[name="topic"]');
  const pagination = board.querySelector('.board-pagination');
  const total = board.querySelector('.record-total');
  const size = 8;
  let page = 1;
  const params = new URLSearchParams(location.search);
  query.value = params.get('q') || '';
  topic.value = [...topic.options].some(o => o.value === params.get('topic')) ? params.get('topic') : '';
  page = Math.max(1, parseInt(params.get('page'), 10) || 1);
  function render(updateUrl = false) {
    const words = query.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    const matches = rows.filter(row => (!topic.value || row.dataset.topic === topic.value || row.dataset.path === topic.value) && words.every(word => row.dataset.search.includes(word)));
    const pages = Math.max(1, Math.ceil(matches.length / size));
    page = Math.min(page, pages);
    rows.forEach(row => row.hidden = true);
    matches.slice((page - 1) * size, page * size).forEach(row => row.hidden = false);
    total.textContent = `${matches.length}건`;
    board.querySelector('.board-empty').hidden = matches.length > 0;
    pagination.hidden = matches.length <= size;
    pagination.querySelector('.page-status').textContent = `${page} / ${pages}`;
    pagination.querySelector('[data-page="previous"]').disabled = page === 1;
    pagination.querySelector('[data-page="next"]').disabled = page === pages;
    if (updateUrl) {
      const url = new URL(location.href);
      ['q', 'topic', 'page'].forEach(key => url.searchParams.delete(key));
      if (query.value.trim()) url.searchParams.set('q', query.value.trim());
      if (topic.value) url.searchParams.set('topic', topic.value);
      if (page > 1) url.searchParams.set('page', page);
      history.replaceState(null, '', url);
    }
  }
  query.addEventListener('input', () => { page = 1; render(true); });
  topic.addEventListener('change', () => { page = 1; render(true); });
  board.querySelector('form').addEventListener('submit', e => { e.preventDefault(); page = 1; render(true); });
  pagination.querySelectorAll('button').forEach(button => button.addEventListener('click', () => {
    page += button.dataset.page === 'next' ? 1 : -1;
    render(true);
    board.scrollIntoView({block: 'start'});
  }));
  window.addEventListener('popstate', () => {
    const state = new URLSearchParams(location.search);
    query.value = state.get('q') || ''; topic.value = state.get('topic') || '';
    page = Math.max(1, parseInt(state.get('page'), 10) || 1); render();
  });
  render();
})();
