// AI Readiness Score: six questions, two per pillar. Runs entirely in the browser; nothing is stored or sent.
(function () {
  const card = document.getElementById('score-card');
  if (!card) return;

  const SUBSCRIBE = 'https://airevolutionupdate.substack.com/subscribe';
  const PILLARS = {
    work: { name: 'Work', page: 'work.html', color: '#6a3998',
      advice: 'Start with Work: learn which of your tasks AI can take over, then put an AI assistant to work for you.' },
    housing: { name: 'Housing', page: 'housing.html', color: '#096341',
      advice: 'Start with Housing: look at what your home costs you and what your options are if your income changes.' },
    finance: { name: 'Finance', page: 'finance.html', color: '#1a2336',
      advice: 'Start with Finance: build a cushion so a change at work doesn’t turn into a crisis at home.' },
    education: { name: 'Education', page: 'education.html', color: '#57288b',
      advice: 'Start with Education: pick up one new skill this season, and look at how your family learns.' },
    healthcare: { name: 'Healthcare', page: 'healthcare.html', color: '#0b6b4a',
      advice: 'Start with Healthcare: see which of your tasks AI is taking over, and which skills to grow next.' }
  };
  const QUESTIONS = [
    { pillar: 'work', text: 'How much of your workday is repeating the same tasks?',
      options: ['Almost all of it', 'About half', 'A little', 'Almost none, every day is different'] },
    { pillar: 'work', text: 'How often do you use an AI tool like ChatGPT, Claude or Gemini to get work done?',
      options: ['Never', 'I’ve tried it once or twice', 'A few times a month', 'Every week'] },
    { pillar: 'housing', text: 'If your income dropped by a quarter, could you keep your current home?',
      options: ['No', 'For a few months', 'Probably, with some cuts', 'Yes, comfortably'] },
    { pillar: 'housing', text: 'Could your work, or work you could switch to, be done from home part of the week?',
      options: ['No', 'I’m not sure', 'Some of it', 'Yes'] },
    { pillar: 'finance', text: 'If a surprise $400 bill showed up tomorrow, how would you pay it?',
      options: ['I couldn’t, or I’d have to borrow', 'A credit card I’d carry a balance on', 'Savings, but it would hurt', 'Savings, no problem'] },
    { pillar: 'finance', text: 'How many ways do you earn money?',
      options: ['One job, no backup', 'One job, plus skills I could sell', 'One job plus a small side income', 'Two or more income streams'] },
    { pillar: 'education', text: 'When did you last learn a new work skill, through a course, certificate or training?',
      options: ['I can’t remember', 'More than a year ago', 'In the last year', 'I’m learning something now'] },
    { pillar: 'healthcare', text: 'If you work in healthcare, how much of your day is paperwork versus hands-on care?',
      options: ['Almost all paperwork', 'More paperwork than care', 'More care than paperwork', 'Almost all hands-on care'], optOut: 'I don’t work in healthcare' }
  ];

  const answers = new Array(QUESTIONS.length).fill(null);
  let step = 0;

  const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  function header() {
    return '<div class="score-head"><h2>Your AI Readiness Score</h2><span class="tag">No email required</span></div>' +
      '<div class="progress" aria-hidden="true">' +
      QUESTIONS.map((_, i) => '<span class="' + (i < step || step === QUESTIONS.length ? 'done' : (i === step ? 'done' : '')) + '"></span>').join('') +
      '</div>';
  }

  function renderQuestion() {
    const q = QUESTIONS[step];
    const last = step === QUESTIONS.length - 1;
    card.innerHTML = header() +
      '<fieldset><legend>Question ' + (step + 1) + ' of ' + QUESTIONS.length + ' · ' + PILLARS[q.pillar].name + '</legend>' +
      '<p class="q-text" id="q-text" tabindex="-1">' + esc(q.text) + '</p>' +
      q.options.map((o, i) =>
        '<label class="option"><input type="radio" name="q" value="' + i + '"' + (answers[step] === i ? ' checked' : '') + '> ' + esc(o) + '</label>'
      ).join('') +
      (q.optOut ? '<label class="option"><input type="radio" name="q" value="-1"' + (answers[step] === -1 ? ' checked' : '') + '> ' + esc(q.optOut) + '</label>' : '') +
      '</fieldset>' +
      '<div class="score-actions">' +
      (step > 0 ? '<button type="button" class="btn ghost" data-act="back">← Back</button>' : '') +
      '<button type="button" class="btn primary" data-act="next"' + (answers[step] === null ? ' disabled' : '') + '>' +
      (last ? 'See my score →' : 'Next question →') + '</button></div>' +
      '<p class="score-note">About 2 minutes. No email or sign-up required. Your answers stay on your device.</p>';
  }

  function scores() {
    const out = {};
    Object.keys(PILLARS).forEach(p => {
      const idx = QUESTIONS.map((q, i) => q.pillar === p ? i : -1).filter(i => i >= 0);
      const valid = idx.filter(i => answers[i] >= 0);
      if (!valid.length) return;
      const total = valid.reduce((s, i) => s + answers[i], 0);
      out[p] = Math.round(total / (valid.length * 3) * 100);
    });
    return out;
  }

  const label = n => n >= 70 ? 'Ahead' : n >= 40 ? 'Getting there' : 'Exposed';

  function renderResult() {
    const s = scores();
    const order = Object.keys(PILLARS).filter(p => s[p] !== undefined);
    const start = order.reduce((a, b) => s[b] < s[a] ? b : a, order[0]);
    card.innerHTML = header() +
      '<p class="q-text" tabindex="-1" id="result-title">Here’s where you stand</p>' +
      order.map(p =>
        '<div class="result-row"><div class="top"><span>' + PILLARS[p].name + '</span><span>' + s[p] + ' · ' + label(s[p]) + '</span></div>' +
        '<div class="bar" role="img" aria-label="' + PILLARS[p].name + ' score ' + s[p] + ' out of 100"><i style="width:' + Math.max(s[p], 4) + '%;background:' + PILLARS[p].color + '"></i></div></div>'
      ).join('') +
      '<div class="result-start"><span class="kicker c-home">Your best place to start</span>' +
      '<p>' + esc(PILLARS[start].advice) + '</p>' +
      '<a class="btn primary" href="' + PILLARS[start].page + '">Go to ' + PILLARS[start].name + ' →</a></div>' +
      '<form class="inline-join" action="' + SUBSCRIBE + '" method="get" target="_blank" rel="noopener">' +
      '<label class="sr-only" for="score-email">Email address</label>' +
      '<input id="score-email" type="email" name="email" placeholder="you@email.com" required>' +
      '<button class="btn primary" type="submit">Subscribe free</button></form>' +
      '<div class="score-actions"><button type="button" class="btn ghost" data-act="restart" style="flex:1!important">Retake the score</button></div>' +
      '<p class="score-note">A quick self-check, not a professional financial or career assessment.</p>';
    document.getElementById('result-title').focus();
  }

  function render() { step < QUESTIONS.length ? renderQuestion() : renderResult(); }

  card.addEventListener('change', e => {
    if (e.target.name === 'q') {
      answers[step] = Number(e.target.value);
      const next = card.querySelector('[data-act="next"]');
      if (next) next.disabled = false;
    }
  });
  card.addEventListener('click', e => {
    const act = e.target.closest('[data-act]')?.dataset.act;
    if (!act) return;
    if (act === 'next' && answers[step] !== null) step++;
    if (act === 'back' && step > 0) step--;
    if (act === 'restart') { answers.fill(null); step = 0; }
    render();
    if (act !== 'restart' && step < QUESTIONS.length) card.querySelector('#q-text')?.focus?.();
  });

  render();
})();
