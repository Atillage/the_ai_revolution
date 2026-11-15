// "Know your number" housing cost check. Runs in the browser; nothing is stored or sent.
(function () {
  const form = document.getElementById('housing-calc');
  if (!form) return;
  const out = document.getElementById('housing-result');
  const money = v => Number(String(v).replace(/[^0-9.]/g, ''));

  function verdict(p) {
    if (p > 50) return { label: 'Severely cost-burdened', note: 'More than half your income goes to housing. A drop in pay would leave very little room. Your plan B matters most.', color: '#9b2c2c' };
    if (p > 30) return { label: 'Cost-burdened', note: 'You’re over the 30% line. A change at work would squeeze your budget quickly.', color: '#8a5a00' };
    return { label: 'Within the 30% guideline', note: 'Your housing costs leave some room to absorb a change in income.', color: '#096341' };
  }

  form.addEventListener('submit', e => {
    e.preventDefault();
    const income = money(form.income.value);
    const cost = money(form.cost.value);
    if (!income || income <= 0 || !cost || cost < 0) {
      out.innerHTML = '<p class="calc-msg">Enter your monthly income and your monthly housing costs.</p>';
      return;
    }
    const pct = Math.round(cost / income * 100);
    const drop = Math.round(cost / (income * 0.75) * 100);
    const v = verdict(pct);
    const dv = verdict(drop);
    out.innerHTML =
      '<p class="calc-big" style="color:' + v.color + '">' + pct + '%</p>' +
      '<p class="calc-label" style="color:' + v.color + '">' + v.label + '</p>' +
      '<p class="calc-msg">' + v.note + '</p>' +
      '<p class="calc-msg"><strong>If your income dropped by a quarter:</strong> ' + drop + '% (' + dv.label.toLowerCase() + ').</p>';
    out.focus();
  });
})();

// Copy-prompt buttons.
(function () {
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const text = btn.parentElement.querySelector('.prompt-text').textContent;
      const done = () => { btn.textContent = 'Copied ✓'; setTimeout(() => { btn.textContent = 'Copy prompt'; }, 2000); };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, () => fallback(text, done));
      } else { fallback(text, done); }
    });
  });
  function fallback(text, done) {
    try {
      const t = document.createElement('textarea');
      t.value = text; t.setAttribute('readonly', ''); t.style.position = 'absolute'; t.style.left = '-9999px';
      document.body.appendChild(t); t.select(); document.execCommand('copy'); document.body.removeChild(t); done();
    } catch (e) { /* select the text manually */ }
  }

})();
