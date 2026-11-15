// Marketplace filters. Runs in the browser; nothing is stored or sent.
(function () {
  // Two tabs: Robots and gadgets / Home and office
  const chips = document.querySelectorAll('.mk-chip');
  const shopCards = document.querySelectorAll('#mk-grid .mk-card');
  chips.forEach(c => c.addEventListener('click', () => {
    showTab(c.dataset.f);
  }));
  const grid = document.getElementById('mk-grid');
  const area = document.getElementById('home-office');
  function showTab(f) {
    chips.forEach(x => { const on = x.dataset.f === f; x.classList.toggle('on', on); x.setAttribute('aria-pressed', on ? 'true' : 'false'); });
    // The three Home and office cards appear only on their own tab
    if (area) area.hidden = f !== 'ho';
    if (grid) grid.hidden = f === 'ho';
    shopCards.forEach(card => { card.hidden = false; });
  }

  // Home and office: products show only after a card is clicked
  const NAMES = { home: 'AI My Home', office: 'AI My Office', nowifi: 'No Wi-Fi smart home' };
  const panel = document.getElementById('ho-panel');
  const head = document.getElementById('ho-head');
  const picks = document.querySelectorAll('.ho-pick');
  function pick(sub) {
    if (!panel) return;
    picks.forEach(a => { const on = a.dataset.pick === sub; a.classList.toggle('on', on); a.setAttribute('aria-pressed', on ? 'true' : 'false'); });
    panel.querySelectorAll('.mk-card').forEach(card => { card.hidden = card.dataset.sub !== sub; });
    head.innerHTML = '<strong>' + NAMES[sub] + '</strong> picks';
    panel.hidden = false;
    panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  picks.forEach(a => a.addEventListener('click', e => { e.preventDefault(); pick(a.dataset.pick); }));

  const h = location.hash.replace('#', '');
  if (h === 'home-office') showTab('ho');
  else if (h.indexOf('pick-') === 0 && NAMES[h.slice(5)]) { showTab('ho'); pick(h.slice(5)); }
})();
