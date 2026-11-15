/* =========================================================
   UNDERSTANDING AI: EDIT YOUR CONTENT HERE
   New Substack post? Copy one line in ARTICLES (newest at the top) and change it.
   topic: one of the TOPICS names below.
   ========================================================= */
const TOPICS = ["Work & careers", "AI tools & how-to", "AI news", "Beginner's guide", "Learning"];
const SUB = "https://airevolutionupdate.substack.com/p/";
const ARTICLES = [
  { title:"Put AI to Work While You Sleep", desc:"The one AI skill that saves hours every week, and how to set it up yourself.", url:SUB+"put-ai-to-work-while-you-sleep", date:"2026-10-09", topic:"Work & careers" },
  { title:"What Is Claude Code, and Should You Care?", desc:"What Claude Code is, and whether it matters if you're not a programmer.", url:SUB+"what-is-claude-code-and-should-you", date:"2026-09-08", topic:"AI tools & how-to" },
  { title:"You Saw a \"More Models\" Button in Claude. Here's What It Means", desc:"What Claude's model picker does and which option to choose.", url:SUB+"you-saw-a-more-models-button-in-claudeheres", date:"2026-08-08", topic:"AI tools & how-to" },
  { title:"The Pope, the Paycheck, and the Personal AI Agent", desc:"A week of AI news, including Google's biggest AI event of the year.", url:SUB+"the-pope-the-paycheck-and-the-personal", date:"2026-06-01", topic:"AI news" },
  { title:"Google and AI Are Sprinting. Do You Know What They're Racing Toward?", desc:"What the fast pace of AI announcements means for everyday people.", url:SUB+"google-and-ai-are-sprinting-do-you", date:"2026-05-18", topic:"AI news" },
  { title:"Turn a Photo Into a Caricature, Cartoon, or Professional Avatar", desc:"Step by step: use AI to transform your own photos.", url:SUB+"how-to-turn-a-photo-into-a-caricature", date:"2026-03-05", topic:"AI tools & how-to" },
  { title:"Can Humans Survive the AI and Robot Takeover?", desc:"A look at the numbers behind the automation headlines.", url:SUB+"can-humans-survive-the-ai-and-robot", date:"2026-02-23", topic:"Work & careers" },
  { title:"The Jobs AI Is Changing Right Now", desc:"Which jobs are shifting, and what that actually means for you.", url:SUB+"the-jobs-ai-is-changing-right-now", date:"2026-02-15", topic:"Work & careers" },
  { title:"How AI Screens Resumes, and How to Prepare", desc:"Get your resume past AI screening software.", url:SUB+"how-ai-screens-resumes-and-how-to", date:"2026-02-08", topic:"Work & careers" },
  { title:"Who Are the Big AI Players (and Which One Should You Use?)", desc:"ChatGPT, Claude, Gemini and more, sorted out.", url:SUB+"who-are-the-big-ai-players-and-which", date:"2026-01-31", topic:"AI tools & how-to" },
  { title:"When to Use AI (and When Google Is Enough)", desc:"A simple way to decide which tool fits the question.", url:SUB+"when-to-use-ai-and-when-google-is", date:"2026-01-22", topic:"AI tools & how-to" },
  { title:"Part 5: How to Start Using AI Safely and Intentionally", desc:"Beginner's Guide to AI, part 5 of 5.", url:SUB+"part-5-how-to-start-using-ai-safely", date:"2026-01-17", topic:"Beginner's guide", part:5 },
  { title:"Part 4: What Are AI Agents (and What Are They Doing?)", desc:"Beginner's Guide to AI, part 4 of 5.", url:SUB+"part-4-what-are-ai-agents-and-what", date:"2026-01-10", topic:"Beginner's guide", part:4 },
  { title:"Part 3: How AI Is Reshaping the Way We Work", desc:"Beginner's Guide to AI, part 3 of 5.", url:SUB+"part-3-how-ai-is-reshaping-the-way", date:"2025-12-29", topic:"Beginner's guide", part:3 },
  { title:"Part 2: What AI Can (and Can't) Do at Work", desc:"Beginner's Guide to AI, part 2 of 5.", url:SUB+"what-ai-can-and-cant-do-at-work-beginners", date:"2025-12-17", topic:"Beginner's guide", part:2 },
  { title:"Part 1: What Is AI, Really?", desc:"Beginner's Guide to AI, part 1 of 5: why it suddenly feels everywhere.", url:SUB+"what-is-ai-really-and-why-it-suddenly", date:"2025-12-14", topic:"Beginner's guide", part:1 },
  { title:"Welcome to the AI Revolution", desc:"Where this newsletter starts: a practical guide for everyday people.", url:SUB+"welcome-to-the-ai-revolution-a-practical", date:"2025-11-30", topic:"AI news" },
  /* Older articles on this website (shown last) */
  { title:"AI is here. What does that mean for us?", desc:"Where AI can help in everyday life, and when to be cautious.", url:"blog/ai-is-here.html", date:"", topic:"Beginner's guide", local:true },
  { title:"Is AI replacing jobs?", desc:"Which tasks are changing, which skills stay valuable, and where new opportunities appear.", url:"blog/ai-jobs.html", date:"", topic:"Work & careers", local:true },
  { title:"AI: fact versus fear", desc:"Thoughtful questions about AI, not blind trust or constant fear.", url:"blog/fact-vs-fear.html", date:"", topic:"Beginner's guide", local:true },
  { title:"What human skills matter in an AI world?", desc:"Combining useful tools with distinctly human strengths.", url:"blog/human-skills.html", date:"", topic:"Learning", local:true }
];
/* ================= end of editable content ================= */

(function () {
  const $ = id => document.getElementById(id);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const fmt = d => new Date(d + "T12:00:00").toLocaleDateString("en-US", {month:"short", day:"numeric", year:"numeric"});
  const ext = a => a.local ? "" : ' target="_blank" rel="noopener noreferrer"';
  const dated = ARTICLES.filter(a => a.date).sort((a, b) => b.date.localeCompare(a.date));

  // Beginner series
  const s = $("series");
  if (s) s.innerHTML = ARTICLES.filter(a => a.part).sort((a, b) => a.part - b.part).map(a =>
    `<a class="series-card" href="${a.url}"${ext(a)}><span class="n">${a.part}</span><h3>${esc(a.title.replace(/^Part \d+: /, ""))}</h3><span class="go">Read part ${a.part} ↗</span></a>`).join("");

  // Featured newest post
  const f = $("featured"), top = dated[0];
  if (f && top) f.innerHTML = `<a class="feat-post" href="${top.url}"${ext(top)}><span class="feat-k">Newest · ${fmt(top.date)}</span><h3>${esc(top.title)}</h3><p>${esc(top.desc)}</p><span class="go">Read on Substack ↗</span></a>`;

  // Library
  let topic = "All";
  const used = TOPICS.filter(t => ARTICLES.some(a => a.topic === t));
  const chips = $("chips");
  chips.innerHTML = ["All", ...used].map(t => `<button class="mk-chip lib-chip${t === "All" ? " on" : ""}" type="button" aria-pressed="${t === "All"}" data-t="${esc(t)}">${esc(t)}</button>`).join("");
  chips.addEventListener("click", e => {
    const b = e.target.closest(".lib-chip"); if (!b) return;
    topic = b.dataset.t;
    chips.querySelectorAll(".lib-chip").forEach(x => { x.classList.toggle("on", x === b); x.setAttribute("aria-pressed", String(x === b)); });
    render();
  });
  $("search").addEventListener("input", render);
  function render() {
    const q = $("search").value.trim().toLowerCase();
    const list = ARTICLES
      .filter(a => !(top && a === top) || q || topic !== "All")
      .filter(a => topic === "All" || a.topic === topic)
      .filter(a => !q || (a.title + " " + a.desc).toLowerCase().includes(q))
      .sort((a, b) => (b.date || "0").localeCompare(a.date || "0"));
    $("resultCount").textContent = list.length + (list.length === 1 ? " article" : " articles");
    $("grid").innerHTML = list.map(a => `<a class="lib-card" href="${a.url}"${ext(a)}><span class="lib-meta">${esc(a.topic)} · ${a.date ? fmt(a.date) : "Older article"}</span><h3>${esc(a.title)}</h3><p>${esc(a.desc)}</p><span class="go">${a.local ? "Read here →" : "Read on Substack ↗"}</span></a>`).join("");
    $("empty").hidden = list.length > 0;
  }
  render();
})();

// ---- Extras: copy prompt, series check marks, share a word, scam quiz ----
(function () {
  const $ = id => document.getElementById(id);
  function copy(text, done) {
    const fb = () => { try { const t = document.createElement("textarea"); t.value = text; t.setAttribute("readonly", ""); t.style.position = "absolute"; t.style.left = "-9999px"; document.body.appendChild(t); t.select(); document.execCommand("copy"); t.remove(); done(); } catch (e) {} };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, fb); else fb();
  }

  // Copy the "Try it" prompt
  document.querySelectorAll("#try-it .copy-btn").forEach(btn => btn.addEventListener("click", () => {
    copy(btn.parentElement.querySelector(".prompt-text").textContent, () => { btn.textContent = "Copied ✓"; setTimeout(() => { btn.textContent = "Copy prompt"; }, 2000); });
  }));

  // Series check marks (saved in this browser only)
  const KEY = "air-series-read";
  const load = () => { try { return JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { return []; } };
  const save = v => { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {} };
  let read = load();
  function paint() {
    const cards = document.querySelectorAll("#series .series-card");
    cards.forEach(c => {
      const n = c.querySelector(".n").textContent.replace("✓", "").trim() || c.dataset.part;
      c.dataset.part = n;
      const done = read.includes(n);
      c.classList.toggle("done", done);
      c.querySelector(".n").textContent = done ? "✓" : n;
    });
    const p = $("seriesProgress");
    if (p && cards.length) p.textContent = read.length === 0 ? "Your progress is saved on this device as you read."
      : read.length >= cards.length ? "You've read all 5 parts. Nice work! Next: try the scam quiz below."
      : `You've read ${read.length} of ${cards.length} parts.`;
  }
  const series = $("series");
  if (series) {
    paint();
    series.addEventListener("click", e => {
      const c = e.target.closest(".series-card"); if (!c) return;
      if (!read.includes(c.dataset.part)) { read.push(c.dataset.part); save(read); }
      setTimeout(paint, 50);
    });
  }

  // Share a glossary word
  document.querySelectorAll(".gl-share").forEach(btn => btn.addEventListener("click", () => {
    const url = location.href.split("#")[0] + "#" + btn.dataset.id;
    copy(url, () => { btn.textContent = "Link copied ✓"; setTimeout(() => { btn.textContent = "Share this word"; }, 2000); });
  }));

  // Real or AI scam? quiz
  const QUIZ = [
    { q: "Your grandson calls. It's his voice, crying. He says he's in jail and needs bail money sent by gift card right now, and not to tell his parents.",
      a: "scam", tip: "AI can copy a voice from a few seconds of video. Hang up and call him or his parents on a number you already have. Set up a family code word that only you know." },
    { q: "A video shows a famous billionaire promoting a new AI trading app that \"guarantees\" you'll double your money in a month.",
      a: "scam", tip: "Fake celebrity videos are one of the most common AI scams. No real investment guarantees returns. Don't click; look the company up on your own." },
    { q: "Your pharmacy texts: \"Your prescription is ready for pickup.\" No link, and it doesn't ask you for anything.",
      a: "real", tip: "It doesn't ask for money, a password or a click. Still, if anything feels off, call the pharmacy using the number on your bottle." },
    { q: "An email from \"your bank\" with perfect spelling and your name asks you to click a link to confirm your login after \"unusual activity.\"",
      a: "scam", tip: "Perfect grammar no longer means it's real, because AI writes flawless emails. Never log in from a link. Open your bank's app or type its address yourself." },
    { q: "Your boss texts from a new number: \"In a meeting, can't talk. Need you to buy 5 gift cards for a client. I'll pay you back today.\"",
      a: "scam", tip: "Urgent + secret + gift cards = scam, every time. Check with your boss another way, like their usual number or in person." },
    { q: "After a text-only \"interview,\" you're offered a remote job, but first you have to pay $300 for equipment and they'll reimburse you.",
      a: "scam", tip: "Real employers don't make you pay to start. AI makes fake recruiters and job posts look polished. Check the company's own careers page." },
  ];
  const quiz = $("quiz");
  if (quiz) {
    let right = 0, answered = 0;
    quiz.innerHTML = QUIZ.map((x, i) => `<article class="quiz-card" data-i="${i}"><span class="quiz-n">${i + 1} of ${QUIZ.length}</span><p class="quiz-q">${x.q}</p><div class="quiz-btns"><button type="button" data-v="real">Looks real</button><button type="button" data-v="scam">Likely a scam</button></div><p class="quiz-tip" hidden></p></article>`).join("");
    quiz.addEventListener("click", e => {
      const b = e.target.closest(".quiz-btns button"); if (!b) return;
      const card = b.closest(".quiz-card"); if (card.classList.contains("answered")) return;
      const x = QUIZ[+card.dataset.i], ok = b.dataset.v === x.a;
      card.classList.add("answered", ok ? "ok" : "miss");
      b.classList.add("picked");
      card.querySelectorAll(".quiz-btns button").forEach(z => { z.disabled = true; if (z.dataset.v === x.a) z.classList.add("correct"); });
      const tip = card.querySelector(".quiz-tip");
      tip.innerHTML = `<strong>${ok ? "Right." : "Not quite."} ${x.a === "scam" ? "This is likely a scam." : "This one is likely real."}</strong> ${x.tip}`;
      tip.hidden = false;
      answered++; if (ok) right++;
      if (answered === QUIZ.length) $("quizScore").innerHTML = `You got <strong>${right} of ${QUIZ.length}</strong>. ${right === QUIZ.length ? "You're hard to fool." : "Scammers count on people being rushed."} Share this quiz with someone you love, and see <a href="finance.html">more ways to protect your money →</a>`;
    });
  }
})();
