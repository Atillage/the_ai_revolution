// Job task check and copy-prompt buttons for the Work page. Runs in the browser; nothing is stored or sent.
(function () {
  const form = document.getElementById('job-check-form');
  if (form) {
    const out = document.getElementById('job-result');
    const GROUPS = {
      auto: { title: 'AI is taking on much of this', color: '#6a3998',
        tip: 'Learn to do these tasks with AI so you become the person who checks and improves its work, not the person it replaces.' },
      assist: { title: 'AI helps, but you make the call', color: '#1a2336',
        tip: 'Get good at the AI tools for these tasks. People who use them well get more done and stand out.' },
      human: { title: 'Mostly human for the foreseeable future', color: '#096341',
        tip: 'These are your strongest skills. Put them first on your resume and grow them.' }
    };
    const boxes = [...form.querySelectorAll('input[name="task"]')];
    form.addEventListener('submit', e => {
      e.preventDefault();
      const picked = boxes.filter(i => i.checked);
      if (!picked.length) { out.innerHTML = '<p class="calc-msg">Pick at least one task.</p>'; out.focus(); return; }
      let html = '';
      Object.keys(GROUPS).forEach(k => {
        const g = GROUPS[k];
        const mine = picked.filter(i => i.dataset.group === k);
        if (!mine.length) return;
        html += '<div class="hc-group" style="border-color:' + g.color + '"><p class="calc-label" style="color:' + g.color + '">' + g.title + '</p><ul>' +
          mine.map(i => '<li>' + i.parentElement.textContent.trim() + '</li>').join('') + '</ul><p class="calc-msg">' + g.tip + '</p></div>';
      });
      const share = picked.filter(i => i.dataset.group === 'auto').length / picked.length;
      const summary = share >= 0.5
        ? 'Most of the tasks you picked are ones AI is taking on. Now is a good time to add a new skill.'
        : 'Most of the tasks you picked still need a person, or a person working with AI. Build on those strengths.';
      const next = share >= 0.5
        ? '<a href="education.html#learn-first">Find your next skill →</a> <a href="#ai-at-work">Start using AI for these tasks →</a>'
        : '<a href="#ai-at-work">Use AI for the busywork →</a> <a href="#second-paycheck">Turn your skills into a second paycheck →</a>';
      out.innerHTML = '<p class="calc-msg"><strong>' + summary + '</strong></p>' + html + '<p class="calc-next">' + next + '</p>';
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
// Open a collapsed tool when someone jumps to it.
(function () {
  function openFor(id) {
    const box = document.getElementById(id);
    const d = box && box.querySelector('details.tool-toggle');
    if (d) d.open = true;
  }
  document.querySelectorAll('[data-open]').forEach(a => a.addEventListener('click', () => openFor(a.dataset.open)));
  if (location.hash) openFor(location.hash.slice(1));
  window.addEventListener('hashchange', () => openFor(location.hash.slice(1)));
})();
