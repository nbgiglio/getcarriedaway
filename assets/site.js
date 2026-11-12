// Header menu: Tools dropdown on desktop, full-screen menu on phones. Portfolio filters.
(() => {
  const btn = document.querySelector('.tools-btn');
  const menu = document.getElementById('tools-menu');
  const setTools = open => { if (!btn) return; btn.setAttribute('aria-expanded', open); menu.hidden = !open; };
  btn?.addEventListener('click', e => { e.stopPropagation(); setTools(menu.hidden); });
  document.addEventListener('click', e => { if (menu && !menu.hidden && !menu.contains(e.target)) setTools(false); });

  const mb = document.querySelector('.menu-btn');
  const setNav = open => {
    document.body.classList.toggle('nav-open', open);
    mb?.setAttribute('aria-expanded', open);
    mb?.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    mb?.querySelector('.i-open')?.toggleAttribute('hidden', open);
    mb?.querySelector('.i-close')?.toggleAttribute('hidden', !open);
  };
  mb?.addEventListener('click', () => setNav(!document.body.classList.contains('nav-open')));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { setTools(false); setNav(false); } });
  matchMedia('(min-width: 761px)').addEventListener('change', () => setNav(false));

  const chips = document.querySelectorAll('.chip');
  chips.forEach(c => c.addEventListener('click', () => {
    chips.forEach(x => x.setAttribute('aria-pressed', x === c));
    const f = c.dataset.filter;
    document.querySelectorAll('.project').forEach(p => { p.hidden = f !== 'all' && p.dataset.tag !== f; });
  }));
})();
