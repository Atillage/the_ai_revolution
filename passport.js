// Skills Passport builder. Runs in the browser; nothing is stored or sent.
(function () {
  const form = document.getElementById('pp-form');
  if (!form) return;
  const out = document.getElementById('pp-out');
  const esc = v => String(v || '').trim().replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const val = n => esc(form.elements[n] ? form.elements[n].value : '');

  function build() {
    const name = val('name'), goal = val('goal'), contact = val('contact'), learn = val('learn');
    const skills = (form.elements.skills.value || '').split(',').map(x => esc(x)).filter(Boolean);
    const projects = [1, 2, 3].map(n => ({ t: val('t' + n), d: val('d' + n), r: val('r' + n) })).filter(p => p.t || p.d || p.r);
    if (!name || !goal || !projects.length) {
      out.innerHTML = '<p class="calc-msg">Add your name, the job you\'re aiming for and at least one project.</p>';
      return null;
    }
    let h = '<div class="passport-sheet" id="pp-sheet"><div class="pp-head"><div><span class="pp-kicker">Skills Passport</span><h3>' + name + '</h3><p class="pp-goal">Aiming for: ' + goal + '</p></div>' +
      (contact ? '<p class="pp-contact">' + contact + '</p>' : '') + '</div>';
    if (skills.length) h += '<div class="pp-skills">' + skills.map(x => '<span>' + x + '</span>').join('') + '</div>';
    h += '<h4>What I\'ve done</h4><ol class="pp-projects">' + projects.map(p =>
      '<li><strong>' + (p.t || 'Project') + '</strong>' + (p.d ? '<p>' + p.d + '</p>' : '') + (p.r ? '<p class="pp-result">Result: ' + p.r + '</p>' : '') + '</li>').join('') + '</ol>';
    if (learn) h += '<h4>Training and certificates</h4><p>' + learn + '</p>';
    h += '<p class="pp-foot">Skilled through experience. Made with the Skills Passport at theairevolution.net</p></div>' +
      '<div class="pp-actions"><button class="btn primary" type="button" id="pp-print">Print or save as PDF</button> <button class="btn secondary" type="button" id="pp-edit">Edit my answers</button></div>' +
      '<p class="calc-msg" style="font-size:.82rem">To save a PDF, choose "Save as PDF" as the printer.</p>';
    return h;
  }

  form.addEventListener('submit', e => {
    e.preventDefault();
    const h = build();
    if (!h) return;
    out.innerHTML = h;
    document.getElementById('pp-print').addEventListener('click', () => {
      let root = document.getElementById('pp-print-root');
      if (!root) { root = document.createElement('div'); root.id = 'pp-print-root'; document.body.appendChild(root); }
      root.innerHTML = '';
      root.appendChild(document.getElementById('pp-sheet').cloneNode(true));
      document.body.classList.add('printing-passport');
      window.print();
      setTimeout(() => document.body.classList.remove('printing-passport'), 500);
    });
    document.getElementById('pp-edit').addEventListener('click', () => form.scrollIntoView({ behavior: 'smooth' }));
    out.focus();
    out.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
  window.addEventListener('afterprint', () => document.body.classList.remove('printing-passport'));
})();
