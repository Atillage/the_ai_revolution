// Healthcare task check: sorts the tasks a person picks into three groups. Runs in the browser; nothing is stored or sent.
(function () {
  const form = document.getElementById('hc-check');
  if (!form) return;
  const out = document.getElementById('hc-result');
  const GROUPS = {
    auto: { title: 'AI is already handling much of this', color: '#6a3998',
      tip: 'Move toward checking, editing and auditing what AI produces, or toward a role that adds judgment.',
      tasks: ['doc', 'code', 'sched', 'trans'] },
    assist: { title: 'AI helps, but you make the call', color: '#1a2336',
      tip: 'Learn the tools well. People who use AI wisely in these tasks become more valuable.',
      tasks: ['img', 'msg'] },
    human: { title: 'Mostly human for the foreseeable future', color: '#096341',
      tip: 'These are your strongest skills to grow. Lean into them as AI takes over paperwork.',
      tasks: ['hands', 'teach', 'team', 'comfort'] }
  };
  const LABELS = {};
  form.querySelectorAll('input[name="task"]').forEach(i => { LABELS[i.value] = i.parentElement.textContent.trim(); });

  form.addEventListener('submit', e => {
    e.preventDefault();
    const picked = [...form.querySelectorAll('input[name="task"]:checked')].map(i => i.value);
    if (!picked.length) {
      out.innerHTML = '<p class="calc-msg">Pick at least one task.</p>';
      out.focus();
      return;
    }
    let html = '';
    Object.values(GROUPS).forEach(g => {
      const mine = picked.filter(t => g.tasks.includes(t));
      if (!mine.length) return;
      html += '<div class="hc-group" style="border-color:' + g.color + '"><p class="calc-label" style="color:' + g.color + '">' + g.title + '</p>' +
        '<ul>' + mine.map(t => '<li>' + LABELS[t] + '</li>').join('') + '</ul><p class="calc-msg">' + g.tip + '</p></div>';
    });
    const autoShare = picked.filter(t => GROUPS.auto.tasks.includes(t)).length / picked.length;
    const summary = autoShare >= 0.5
      ? 'Most of the tasks you picked are ones AI is taking over. Now is a good time to plan your next skill.'
      : 'Most of the tasks you picked still need a person. Your hands-on and people skills are your advantage.';
    out.innerHTML = '<p class="calc-msg"><strong>' + summary + '</strong></p>' + html;
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
