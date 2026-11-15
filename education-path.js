// Education path finder: suggests a starting point from four answers. Runs in the browser; nothing is stored or sent.
(function () {
  const form = document.getElementById('ed-path');
  if (!form) return;
  const out = document.getElementById('ed-result');
  const PATHS = {
    online: { name: 'Online school', why: 'It gives your child teachers, a schedule and grades without needing an adult to teach all day. Many states offer free public virtual schools.' },
    stay: { name: 'Stay in school, add support at home', why: 'Your child is doing fine and time is tight. Add a coaching-style AI tutor or a weekend class for extra practice.' },
    home: { name: 'Homeschooling with a curriculum', why: 'You have time to guide learning and your child likes some structure. A curriculum plus a co-op or outside classes is a common setup.' },
    unschool: { name: 'Deschooling, then unschooling', why: 'Your child learns best following their interests, and you have time to guide. Start with a deschooling break, then build learning around projects and curiosity.' },
    hybrid: { name: 'A hybrid or co-op model', why: 'Combining a few days of classes or a co-op with learning at home can give your child a fresh start while sharing the load.' }
  };

  form.addEventListener('submit', e => {
    e.preventDefault();
    const v = n => { const c = form.querySelector('input[name="' + n + '"]:checked'); return c ? Number(c.value) : null; };
    const time = v('time'), structure = v('structure'), budget = v('budget'), feel = v('feel');
    if ([time, structure, budget, feel].includes(null)) {
      out.innerHTML = '<p class="calc-msg">Answer all four questions to see a starting point.</p>';
      out.focus();
      return;
    }
    let key;
    if (time === 0) key = feel === 0 ? 'stay' : 'online';
    else if (feel === 2 && time >= 1) key = structure === 0 && time === 2 ? 'unschool' : 'hybrid';
    else if (structure === 0 && time === 2) key = 'unschool';
    else if (time === 2) key = 'home';
    else key = feel === 0 ? 'stay' : 'hybrid';
    const p = PATHS[key];
    const money = budget === 0
      ? 'On a tight budget, look at free public virtual schools, your library, and free courses like Khan Academy. Some states also offer education savings accounts.'
      : 'Check whether your state offers an education savings account, which can help cover classes and materials.';
    out.innerHTML = '<p class="calc-label" style="color:#6a3998">Starting point: ' + p.name + '</p>' +
      '<p class="calc-msg">' + p.why + '</p><p class="calc-msg">' + money + '</p>' +
      '<p class="calc-msg">Before you change anything, check your state department of education’s rules for homeschooling or virtual school.</p>';
    out.focus();
  });
})();

// Copy-prompt buttons. Nothing is stored or sent.
document.querySelectorAll('.copy-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const text = btn.parentElement.querySelector('.prompt-text').textContent;
    const done = () => { btn.textContent = 'Copied ✓'; setTimeout(() => { btn.textContent = 'Copy prompt'; }, 2000); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, () => {});
    }
  });
});

// "What should I learn first?" skill finder. Runs in the browser; nothing is stored or sent.
(function () {
  const form = document.getElementById('learn-finder');
  if (!form) return;
  const out = document.getElementById('learn-result');
  const C = q => 'https://www.coursera.org/search?query=' + encodeURIComponent(q);
  const link = (url, text, ext) => '<a href="' + url + '"' + (ext ? ' target="_blank" rel="noopener noreferrer"' : '') + '>' + text + (ext ? ' ↗' : ' →') + '</a>';
  const AI_BASICS = { name: 'AI basics', why: 'Learn what AI assistants can and can\'t do, and how to use one safely at work and home.',
    where: link('https://airevolutionupdate.substack.com/p/what-is-ai-really-and-why-it-suddenly', 'Start the AI basics series', true) + '<br>' + link('#tutor-prompt', 'Use the AI tutor prompt') };
  const FIELD = {
    office: { name: 'Spreadsheets and data basics', why: 'Office jobs that grow are the ones that can sort, check and explain numbers, often with AI doing the first draft.', where: link(C('data analytics beginner'), 'Beginner data courses on Coursera', true) },
    health: { name: 'AI and health care technology', why: 'Health care keeps hiring, and the people who understand the new software, records and AI tools become the go-to person on the unit.', where: link(C('healthcare informatics'), 'Health informatics courses on Coursera', true) + '<br>' + link('healthcare.html#task-check', 'Check which of your tasks are changing') },
    trades: { name: 'Digital tools for your trade', why: 'Hands-on work is hard to automate. Using AI for quotes, scheduling and customer messages lets you take on more work.', where: link('https://www.apprenticeship.gov/apprenticeship-job-finder', 'Find a paid apprenticeship', true) + '<br>' + link(C('small business AI tools'), 'AI tools for small business on Coursera', true) },
    customer: { name: 'Working alongside AI with customers', why: 'Chatbots now handle simple questions. People who can solve the hard problems, and use AI to draft and look things up faster, stay valuable.', where: link(C('customer success'), 'Customer success courses on Coursera', true) + '<br>' + link('work.html', 'See the Work pillar') },
    other: { name: 'Digital and data basics', why: 'Almost every job now uses data and software. A solid foundation makes every other skill easier to add.', where: link(C('digital skills beginner'), 'Beginner digital skills on Coursera', true) }
  };
  const GOAL = {
    keep: { name: 'Automate one task you repeat every week', why: 'Showing your boss you saved hours with AI is one of the best ways to protect your job.', where: link('work.html', 'Ideas on the Work pillar') },
    promote: { name: 'Leading projects and people', why: 'AI handles more routine work, so the people who organize work and lead teams move up.', where: link(C('project management certificate'), 'Project management courses on Coursera', true) },
    change: { name: 'A career certificate in a growing field', why: 'A focused certificate plus a small portfolio is a faster path into a new field than starting a degree.', where: link('https://www.coursera.org/professional-certificates', 'Browse career certificates on Coursera', true) + '<br>' + link('https://www.apprenticeship.gov/apprenticeship-job-finder', 'Or find a paid apprenticeship', true) },
    side: { name: 'Marketing and selling online', why: 'AI makes it cheaper to start a small business. Finding customers is the skill that decides whether it works.', where: link(C('digital marketing beginner'), 'Digital marketing courses on Coursera', true) + '<br>' + link('finance.html#help', 'Banking and tax help for side income') }
  };
  const PACE = {
    1: 'With about an hour a week, focus on one skill at a time. Start with the first one on your list.',
    2: 'With 2–4 hours a week, you can work on two skills side by side. Start with the first two.',
    3: 'With 5 or more hours a week, you have time for a full certificate. Pick one and set a weekly schedule.'
  };
  form.addEventListener('submit', e => {
    e.preventDefault();
    const v = n => (form.querySelector('input[name="' + n + '"]:checked') || {}).value;
    const goal = v('goal'), work = v('work'), comfort = v('comfort'), time = v('time');
    if (!goal || !work || !comfort || !time) {
      out.innerHTML = '<p class="calc-msg">Please answer all four questions.</p>';
      return;
    }
    const list = [];
    if (comfort === '0') list.push(AI_BASICS);
    list.push(FIELD[work]);
    list.push(GOAL[goal]);
    let html = '<p class="calc-label" style="color:#57288b">Your starting plan</p><ol class="learn-list">';
    list.forEach(s => { html += '<li><strong>' + s.name + '</strong><span>' + s.why + '</span><span class="where">' + s.where + '</span></li>'; });
    html += '</ol><p class="calc-msg">' + PACE[time] + '</p>';
    if (comfort === '2') html += '<p class="calc-msg">You already use AI often. Use it as your tutor and practice partner for each skill above.</p>';
    html += '<p class="calc-msg"><strong>Next:</strong> ' + link('#skills', 'See where the skills-first jobs are') + '</p>';
    out.innerHTML = html;
    out.focus();
  });
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
