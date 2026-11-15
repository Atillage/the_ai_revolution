// Paycheck cushion calculator and copy-prompt buttons. Runs in the browser; nothing is stored or sent.
(function () {
  const form = document.getElementById('fin-calc');
  if (form) {
    const out = document.getElementById('fin-result');
    const money = v => Number(String(v).replace(/[^0-9.]/g, ''));
    const fmt = n => '$' + Math.round(n).toLocaleString('en-US');
    form.addEventListener('submit', e => {
      e.preventDefault();
      const bills = money(form.bills.value);
      const saved = money(form.saved.value) || 0;
      const sources = Number(form.sources.value);
      if (!bills || bills <= 0) {
        out.innerHTML = '<p class="calc-msg">Enter what your must-pay bills cost each month.</p>';
        return;
      }
      const months = saved / bills;
      const weeks = Math.floor(months * 52 / 12);
      let big, label, color, note;
      if (months < 1) {
        big = weeks + (weeks === 1 ? ' week' : ' weeks'); label = 'Thin cushion'; color = '#9b2c2c';
        note = 'A missed paycheck would hit right away. Building one month of bills is the first goal.';
      } else if (months < 3) {
        big = months.toFixed(1) + ' months'; label = 'Getting there'; color = '#8a5a00';
        note = 'You could handle a short gap. Aim for three months to ride out a job change.';
      } else {
        big = months.toFixed(1) + ' months'; label = 'Solid cushion'; color = '#096341';
        note = 'You have room to handle a job change. Keep it in a high-yield savings account so it grows.';
      }
      const toThree = Math.max(0, bills * 3 - saved);
      const toOne = Math.max(0, bills - saved);
      let html = '<p class="calc-big" style="color:' + color + '">' + big + '</p>' +
        '<p class="calc-label" style="color:' + color + '">' + label + '</p>' +
        '<p class="calc-msg">' + note + '</p>';
      if (toOne > 0) {
        html += '<p class="calc-msg"><strong>To reach one month:</strong> save about ' + fmt(toOne / 26) + ' a week for 6 months.</p>';
      }
      if (toThree > 0) {
        html += '<p class="calc-msg"><strong>Gap to a 3-month cushion:</strong> ' + fmt(toThree) + '.</p>';
      }
      if (sources === 1) {
        html += '<p class="calc-msg"><strong>One paycheck:</strong> your home depends on a single income. A second, smaller stream of income makes any cushion last longer.</p>';
      }
      html += '<p class="calc-msg"><a href="#help">See tools that help you build it →</a></p>';
      out.innerHTML = html;
      out.focus();
    });
  }

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

// Investment growth estimate. Runs in the browser; nothing is stored or sent.
(function () {
  const form = document.getElementById('grow-calc');
  if (!form) return;
  const out = document.getElementById('grow-result');
  const fmt = n => '$' + Math.round(n).toLocaleString('en-US');
  form.addEventListener('submit', e => {
    e.preventDefault();
    const weekly = Number(String(form.amt.value).replace(/[^0-9.]/g, ''));
    const years = Number(form.years.value);
    const rate = Number(form.rate.value) / 100;
    if (!weekly || weekly <= 0) {
      out.innerHTML = '<p class="calc-msg">Enter how much you could invest each week.</p>';
      return;
    }
    const monthly = weekly * 52 / 12, r = rate / 12, n = years * 12;
    const total = monthly * ((Math.pow(1 + r, n) - 1) / r);
    const put = monthly * n;
    out.innerHTML = '<p class="calc-big" style="color:#096341">' + fmt(total) + '</p>' +
      '<p class="calc-label" style="color:#096341">after ' + years + ' years</p>' +
      '<p class="calc-msg">You would put in <strong>' + fmt(put) + '</strong>. Growth could add about <strong>' + fmt(total - put) + '</strong>.</p>' +
      '<p class="calc-msg">The longer you stay invested, the more growth does the work.</p>';
    out.focus();
  });
})();
