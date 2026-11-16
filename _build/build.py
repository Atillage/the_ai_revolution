"""Builds the ecosystem pages for theairevolution.net and updates nav/footer on existing pages."""
import re, pathlib, sys

ROOT = pathlib.Path(sys.argv[1])
SUB = "https://airevolutionupdate.substack.com/p/"
SUBSCRIBE = "https://airevolutionupdate.substack.com/subscribe"

PILLARS = [("work.html", "Work"), ("housing.html", "Housing"), ("finance.html", "Finance"),
           ("education.html", "Education"), ("healthcare.html", "Healthcare")]
OTHER = [("jobs.html", "Jobs"), ("guides.html", "Guides"), ("marketplace.html", "Marketplace"), ("understanding-ai.html", "Understanding AI"), ("about.html", "Our Mission")]
ACTIVE = {"index.html": "index.html", "work.html": "work.html", "office.html": "marketplace.html", "marketplace.html": "marketplace.html",
          "housing.html": "housing.html", "home.html": "marketplace.html", "finance.html": "finance.html",
          "education.html": "education.html", "healthcare.html": "healthcare.html",
          "guides.html": "guides.html", "understanding-ai.html": "understanding-ai.html",
          "about.html": "about.html", "jobs.html": "jobs.html"}


def nav(page, pre=""):
    act = "understanding-ai.html" if pre else ACTIVE.get(page)
    def link(href, label, cls="nav-link"):
        a = href == act
        return f'<a class="{cls}{" active" if a else ""}" href="{pre}{href}"{" aria-current=\"page\"" if a else ""}>{label}</a>'
    in_pillar = act in [h for h, _ in PILLARS]
    out = [link("index.html", "Home")]
    out.append('<div class="nav-drop"><button class="nav-link drop-btn' + (' active' if in_pillar else '') +
               '" type="button" aria-expanded="false" aria-controls="pillar-menu">Pillars <span aria-hidden="true">▾</span></button>'
               '<div class="drop-menu" id="pillar-menu">' + "".join(link(h, l, "drop-link") for h, l in PILLARS) + '</div></div>')
    out += [link(h, l) for h, l in OTHER]
    out.append(f'<a class="nav-cta" href="{pre}index.html#join">Join free</a>')
    return '<nav class="nav" id="main-nav" aria-label="Main navigation">' + "".join(out) + "</nav>"


def foot_links(pre=""):
    items = [("work.html", "Future of Work"), ("guides.html", "Guides"), ("housing.html", "Future of Housing"),
             ("understanding-ai.html", "Understanding AI"), ("finance.html", "Future of Finance"),
             ("index.html#score", "AI Readiness Score"), ("marketplace.html", "Marketplace"), ("education.html", "Future of Education"),
             ("about.html", "Our Mission"), ("healthcare.html", "Future of Healthcare Work"),
             ("jobs.html", "Find a job"), ("disclosure.html", "Disclosure &amp; privacy")]
    return '<div class="foot-links">' + "".join(f'<a href="{pre}{h}">{t}</a>' for h, t in items) + "</div>"


BRAND = ('<a class="brand" href="index.html" aria-label="The AI Revolution home"><span class="brand-mark" aria-hidden="true">'
         '<i></i><b></b></span><span><strong>The AI Revolution</strong><small>Adapt · Build · Evolve</small></span></a>')


SITE = "https://theairevolution.net/"
def head_extra(name, title, desc, pre=""):
    url = SITE + ("" if name == "index.html" else name)
    return (f'<link rel="canonical" href="{url}"><link rel="icon" href="{pre}favicon.svg" type="image/svg+xml"><link rel="icon" href="{pre}favicon.png" type="image/png"><link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="The AI Revolution"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}images/og-image.png"><meta name="twitter:card" content="summary_large_image">'
            f'<script src="{pre}analytics.js" defer></script>')

def page(name, title, desc, body, extra_js=""):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f8f7f4"><meta name="description" content="{desc}"><title>{title}</title>{head_extra(name, title, desc)}<link rel="stylesheet" href="style.css"><link rel="stylesheet" href="ecosystem.css"><script src="script.js" defer></script>{extra_js}</head><body><header class="site-header"><div class="container nav-wrap">{BRAND}<button class="menu-toggle" type="button" aria-label="Toggle navigation" aria-controls="main-nav" aria-expanded="false">☰</button>{nav(name)}</div></header><main>
{body}
</main><footer class="site-footer"><div class="container footer-grid"><div>{BRAND.replace(' aria-label="The AI Revolution home"', '')}<p>Helping working people get ahead of the AI economy in work, housing, finance, education and healthcare.</p></div>{foot_links()}</div><div class="container fineprint">© <span id="year">2026</span> The AI Revolution. Educational information, not financial, legal or career advice. Confirm compatibility, costs and features before purchasing.</div></footer></body></html>
'''


def join(topic=None, fid="join-email"):
    heading = "Adapt · Build · Evolve." if topic is None else "Stay in the loop."
    extra = "" if topic is None else f" New {topic} guides will be added to this page as they're published."
    text = ("AI Revolution Update is my free newsletter about AI and everyday life: work, home, money, learning and health care. "
            "It covers AI broadly, not only this topic." + extra)
    return f'''<section class="join" id="join"><h2>{heading}</h2><p>{text}</p><div class="join-embed"><iframe src="https://airevolutionupdate.substack.com/embed" title="Sign up for the AI Revolution Update newsletter" loading="lazy" scrolling="no"></iframe></div><small>Free. Delivered by Substack, where the newsletter lives. Unsubscribe anytime.</small></section>'''



HC_ICON = '<svg width="72" height="72" viewBox="0 0 24 24" fill="none" stroke="#8fd3b4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.6-7 10-7 10z"/><path d="M8.5 12h2l1-2 1.5 4 1-2h1.5"/></svg>'
ED_ICON = '<svg width="72" height="72" viewBox="0 0 24 24" fill="none" stroke="#c9a9ea" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/><path d="M22 9v6"/></svg>'
CHART_SVG = '<svg width="72" height="72" viewBox="0 0 24 24" fill="none" stroke="#8fd3b4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19h16"/><path d="M6 16v-4"/><path d="M10 16V9"/><path d="M14 16v-6"/><path d="M18 16V6"/></svg>'

STATS = {
    "work": ('22%', 'of jobs worldwide are expected to be disrupted by 2030: 170 million new roles created and 92 million displaced.',
             'World Economic Forum, Future of Jobs Report 2025',
             'https://www.weforum.org/press/2025/01/future-of-jobs-report-2025-78-million-new-job-opportunities-by-2030-but-urgent-upskilling-needed-to-prepare-workforces/'),
    "housing": ('1 in 4', 'U.S. paid workdays now happen at home, up from about 7% before 2020. Where you work is shaping where you can live.',
                'WFH Research (Stanford), 2026', 'https://wfhresearch.com/'),
    "finance": ('37%', 'of U.S. adults couldn\'t cover a surprise $400 expense with cash or its equivalent. Little cushion if a job changes.',
                'Federal Reserve, Economic Well-Being of U.S. Households in 2025',
                'https://www.federalreserve.gov/newsevents/pressreleases/other20260513a.htm'),
}
SCLASS = {"work": "c-work", "housing": "c-home", "finance": "c-work"}
SLABEL = {"work": "Your workday", "housing": "Your home", "finance": "Your paycheck"}


def stat(p):
    n, t, s, u = STATS[p]
    return f'<article class="stat-card"><span class="kicker {SCLASS[p]}">{SLABEL[p]}</span><p class="num {SCLASS[p]}">{n}</p><p>{t}</p><p class="src">Source: <a href="{u}" target="_blank" rel="noopener noreferrer">{s}</a></p></article>'


PRODUCTS = '''<a class="product" href="https://altillage.gumroad.com/l/mslfc" target="_blank" rel="noopener noreferrer"><span>Customer Service Rep's AI Survival Checklist</span><span class="price">$7</span></a><a class="product" href="https://altillage.gumroad.com/l/ai-playbook-workers" target="_blank" rel="noopener noreferrer"><span>AI Assistant Playbook: For Working People</span><span class="price">$19</span></a><a class="product" href="https://altillage.gumroad.com/l/ai-playbook-business" target="_blank" rel="noopener noreferrer"><span>AI Assistant Playbook: For Small Business Owners</span><span class="price">$27</span></a>'''

# ---------- Homepage ----------
home_body = f'''<section class="eco-hero"><img src="images/hero.webp" alt=""><div class="container eco-hero-grid"><div>
<span class="eyebrow">The future is being rebuilt</span>
<h1>AI is rebuilding work, school, home and money. <em>Build your future on purpose.</em></h1>
<p class="lead">A plan and a toolkit for working people who'd rather shape what's coming than wait for it.</p>
<div class="accent-rule"></div>
<p class="hint">Start with the AI Readiness Score. It takes about 2 minutes, and no email or sign-up is required.</p>
<div class="quick-start"><span>Or go straight to what you need:</span><div class="qs-row"><a href="jobs.html">Find a job</a><a href="work.html#job-check">Check my job</a><a href="finance.html#fin-calc">Protect my money</a><a href="understanding-ai.html#try-it">Learn AI basics</a></div></div>
</div>
<div class="score-card" id="score" aria-live="polite"><div id="score-card"><noscript><p>The Readiness Score needs JavaScript turned on in your browser.</p></noscript></div></div>
</div></section>

<section class="shipped" aria-label="Shipped recently"><div class="container"><strong>Shipped recently</strong>
<a href="{SUB}put-ai-to-work-while-you-sleep" target="_blank" rel="noopener noreferrer">New post: Put AI to Work While You Sleep</a><span class="dot" aria-hidden="true">·</span>
<a href="#score">New tool: the AI Readiness Score</a><span class="dot" aria-hidden="true">·</span>
<a href="#plan">The Master Plan, published</a></div></section>

<section class="eco-section" id="pillars"><div class="container">
<div class="center-head"><span class="eyebrow">Five things AI is rebuilding</span><h2>One chain reaction. Five places to act.</h2></div>
<div class="pillar-grid five">
<a class="pillar-card" href="work.html"><img src="images/office.webp" alt=""><div><span class="kicker c-work">Pillar 1</span><h3 class="c-work">The Future of Work</h3><p>Turn AI from the thing that replaces you into the assistant that works for you.</p><span class="go c-work">Explore Work →</span></div></a>
<a class="pillar-card" href="housing.html"><img src="images/housing.webp" style="object-position:50% 20%" alt="Family carrying moving boxes into their new home, holding up the keys"><div><span class="kicker c-home">Pillar 2</span><h3 class="c-home">The Future of Housing</h3><p>AI now helps decide who gets approved, what the rent is and where you can live. Know your rights and your options.</p><span class="go c-home">Explore Housing →</span></div></a>
<a class="pillar-card" href="finance.html"><img src="images/finance.webp" alt="Kitchen table with a budget planner, a tablet showing bills and savings, and a coffee mug"><div><span class="kicker c-work">Pillar 3</span><h3 class="c-work">The Future of Finance</h3><p>AI is changing how we earn, pay and save. See what's shifting and how to protect your money.</p><span class="go c-work">Explore Finance →</span></div></a>
<a class="pillar-card" href="education.html"><img src="images/education.webp" alt="Laptop on a desk showing an online biology lesson with a teacher on video"><div><span class="kicker c-work">Pillar 4</span><h3 class="c-work">The Future of Education</h3><p>Skills are starting to count as much as diplomas. See how you'll keep learning, and how your kids will learn, with AI.</p><span class="go c-work">Explore Education →</span></div></a>
<a class="pillar-card" href="healthcare.html"><img src="images/healthcare.webp" style="object-position:50% 12%" alt="Nurse in scrubs reviewing a tablet in a sunny hospital hallway"><div><span class="kicker c-home">Pillar 5</span><h3 class="c-home">The Future of Healthcare Work</h3><p>Healthcare keeps hiring while AI takes over the paperwork. See which tasks are changing in your job.</p><span class="go c-home">Explore Healthcare →</span></div></a>
</div></div></section>

<section class="plan-band" id="plan"><div class="container">
<div class="center-head"><span class="eyebrow">The Master Plan</span><h2>Help working people stay ahead of the AI economy by changing how they earn, learn, live and build wealth.</h2><p>Three phases, built in public. Watch each one happen and help shape it.</p></div>
<div class="plan-grid">
<div><span class="kicker k-now">Phase 1 · Now</span><h3>Learn</h3><p>A free newsletter and step-by-step guides on using AI in your work, learning, home and money.</p></div>
<div><span class="kicker k-next">Phase 2 · Started</span><h3>Tools</h3><p>The Readiness Score is live. Next: simple calculators for job risk, relocation and a paycheck buffer.</p></div>
<div><span class="kicker k-later">Phase 3 · Later</span><h3>Community</h3><p>Working people rebuilding their careers, homes and finances together, starting with newsletter subscribers.</p></div>
</div></div></section>

<section class="eco-section"><div class="container">
<div class="center-head"><span class="eyebrow">The data behind the shift</span><h2>Why the time to act is now.</h2></div>
<div class="stat-grid">{stat("work")}{stat("housing")}{stat("finance")}</div>
</div></section>

<section class="soft-band" id="guides"><div class="container">
<div class="row-head"><div><span class="eyebrow" style="color:var(--purple)">Get started</span><h2>Guides to get you moving today</h2></div><a href="guides.html">Browse all guides →</a></div>
<div class="product-row">{PRODUCTS}</div>
</div></section>

{join()}'''

# ---------- Work ----------
def posts(items):
    return '<div class="post-list">' + "".join(
        f'<a href="{u}"{" target=\"_blank\" rel=\"noopener noreferrer\"" if u.startswith("http") else ""}><b>{t}</b><span>{d}</span></a>' for t, d, u in items) + "</div>"




# ---------- Housing ----------
def shift(n, title, color, fact, src_name, src_url, action):
    return (f'<article class="shift-card"><div class="shift-top"><span class="n" style="color:{color}">{n}</span><h3>{title}</h3></div>'
            f'<p>{fact}</p><p class="src">Source: <a href="{src_url}" target="_blank" rel="noopener noreferrer">{src_name}</a></p>'
            f'<div class="do"><span class="kicker c-home">What you can do</span><ul>{"".join(f"<li>{a}</li>" for a in action)}</ul></div></article>')

HS_STRIP = '''<section class="steps-band"><div class="container"><div class="center-head"><span class="eyebrow">Start here</span><h2>Three ways to protect your home</h2></div>
<div class="plp-grid">
<a class="plp-card" href="#shifts"><span class="n">1</span><h3>Know your rights</h3><p>How AI screens renters and sets rent, and what you can do about it.</p><span class="go">See the 4 shifts →</span></a>
<a class="plp-card" href="#safety-net"><span class="n">2</span><h3>Build a safety net</h3><p>Check your housing number and plan ahead in case your income changes.</p><span class="go">Know my number →</span></a>
<a class="plp-card" href="#ai-at-work"><span class="n">3</span><h3>Put AI on your side</h3><p>Copy-ready prompts to dispute a report, push back on rent and read a lease.</p><span class="go">Get the prompts →</span></a>
</div></div></section>

'''

HS_NEXT = '''<div class="next-wave"><span class="eyebrow" style="color:#c9a9ea">What's coming next</span><h3>Your AI agent vs. their AI agent</h3><p>Landlords and lenders already use AI to screen, price and approve. Next, renters and buyers will have AI agents of their own that search listings, compare the true monthly cost, flag unusual lease terms and draft offers or negotiation emails. Homes themselves are starting to be built faster by robots and factory methods. The people who come out ahead will be the ones who know their numbers and their rights, and use AI to check the other side's math.</p><p class="next-do"><strong>What to do now:</strong> start using AI for the paperwork side of housing. The prompts below are a good place to start.</p></div>'''

HS_SAFETY = '''<section class="soft-band" id="safety-net"><div class="container">
<div class="center-head"><span class="eyebrow" style="color:var(--purple)">Your home as a safety net</span><h2>Make your housing work when income is uncertain</h2><p style="margin:12px auto 0;max-width:640px">If AI changes your job, your housing costs are usually the biggest bill you can't skip. These moves give you room to adjust.</p></div>
<div class="three">
<article class="step-card"><span class="n">01</span><h3>Know your number</h3><p>If housing takes more than 30% of your income, the government counts you as cost-burdened, and a job change would hit hard.</p><form class="calc" id="housing-calc" novalidate><label for="hc-income">Monthly income before taxes</label><div class="calc-in"><span aria-hidden="true">$</span><input id="hc-income" name="income" inputmode="decimal" placeholder="4,500" autocomplete="off"></div><label for="hc-cost">Monthly housing costs</label><div class="calc-in"><span aria-hidden="true">$</span><input id="hc-cost" name="cost" inputmode="decimal" placeholder="1,400" autocomplete="off"></div><small>Rent or mortgage, plus utilities, insurance and any HOA fees.</small><button class="btn primary" type="submit">Show my number</button><div id="housing-result" class="calc-result" aria-live="polite" tabindex="-1"></div><small>No email required. Your numbers stay on your device.</small></form></article>
<article class="step-card"><span class="n">02</span><h3>Have a plan B before you need it</h3><p>Decide now what you'd do if your income dropped, so you're not deciding in a panic.</p><ul class="scam-list"><li><strong>List your options:</strong> a roommate, a cheaper unit, moving in with family, or renting out space.</li><li><strong>Talk to your landlord or lender early.</strong> Payment plans are easier to get before you fall behind.</li><li><strong>Get free expert help.</strong> A <a href="https://www.consumerfinance.gov/find-a-housing-counselor/" target="_blank" rel="noopener noreferrer" style="color:var(--green);font-weight:700">HUD-approved housing counselor</a> can help with renting, buying, credit and avoiding foreclosure.</li></ul></article>
<article class="step-card"><span class="n">03</span><h3>Make your home earn or save</h3><p>Small changes can take real pressure off your budget.</p><ul class="scam-list"><li><strong>Rent a spare room</strong> for a month or more, for example to traveling nurses (see partners below).</li><li><strong>Check the rules first:</strong> your lease, HOA and city may limit rentals, and rental income is taxable.</li><li><strong>Cut the bills you control.</strong> Ask your utility about a free or low-cost energy audit and budget billing.</li></ul></article>
</div></div></section>

'''

hs_prompts = [
 ("Dispute a tenant screening report", "Help me write a short, polite letter to [screening company] disputing errors on my tenant screening report. The errors are: [list them]. Ask them to correct or remove these items and send me an updated copy. Keep it under 200 words."),
 ("Push back on a rent increase", "My rent is going up from $[current] to $[new]. Similar units nearby list for [prices]. I've paid on time for [number] years. Write a polite email to my landlord asking for a smaller increase or a longer lease at today's rate."),
 ("Explain my lease in plain English", "Explain this lease in plain English. List every fee, penalty and renewal term, and flag anything unusual I should ask about before signing: [paste the lease, with names and account numbers removed]."),
 ("Check the math on a remote-work move", "I work remotely and earn $[amount] a year. Compare living in [current city] and [new city]: rent, state and local taxes, insurance, utilities and [number] trips back to the office a year. Show monthly totals in a table and tell me what to double-check."),
]
hs_prompt_html = "".join(f'<details class="prompt"><summary>{t}</summary><p class="prompt-text">{p}</p><button class="copy-btn" type="button">Copy prompt</button></details>' for t,p in hs_prompts)

HS_PROMPTS = f'''<section class="eco-section" id="ai-at-work"><div class="container">
<div class="center-head"><span class="eyebrow">Put AI on your side</span><h2>AI prompts for renters and owners</h2><p style="margin:12px auto 0;max-width:660px">Copy a prompt into any AI assistant, such as ChatGPT, Claude or Gemini, and fill in the blanks. Remove names, account numbers and Social Security numbers before you paste any document.</p></div>
<div class="tip-row"><article class="tip-box"><h3>Four prompts for housing paperwork</h3><div class="prompt-list">{hs_prompt_html}</div></article>
<article class="tip-box"><h3>Before you send anything</h3><ul class="scam-list"><li><strong>Check every fact.</strong> AI can get laws and numbers wrong. Your state or city rules are what count.</li><li><strong>Keep it polite and in writing.</strong> Email or letters create a record if you need it later.</li><li><strong>Know when to get help.</strong> For an eviction notice or foreclosure, contact a <a href="https://www.consumerfinance.gov/find-a-housing-counselor/" target="_blank" rel="noopener noreferrer" style="color:var(--green);font-weight:700">housing counselor</a> or local legal aid right away.</li></ul></article></div>
</div></section>

'''

def hcard(kicker, name, url, what, note, kc="c-home"):
    return f'<article class="partner-card"><span class="kicker {kc}">{kicker}</span><h3><a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a></h3><p>{what}</p><p class="note">{note}</p><a class="go" href="{url}" target="_blank" rel="noopener noreferrer">Visit {name} →</a></article>'

HS_HELP = f'''<section class="eco-section soft" id="help"><div class="container"><div class="center-head"><span class="eyebrow">Where to get help</span><h2>Services that protect your home</h2><p style="margin:12px auto 0;max-width:660px">Matched to the moves above: protecting what you own, building credit with the rent you already pay, and earning from a spare room. A free option is listed too.</p></div><div class="partner-grid four">
{hcard("Renter's insurance", "Lemonade", "https://www.lemonade.com/renters", "Renter's and homeowner's insurance you can buy and manage in an app, with claims handled online.", "Compare quotes from your car insurer too; bundling can be cheaper.")}
{hcard("Build credit with rent", "Boom", "https://www.boompay.app", "Reports your on-time rent payments to all three credit bureaus, which can help if you have little credit history.", "A small monthly fee. Helps most if your credit file is thin.")}
{hcard("Rent out a room", "Furnished Finder", "https://www.furnishedfinder.com", "A marketplace for monthly furnished rentals, built for traveling nurses and other healthcare workers on 13-week assignments.", "Landlords pay to list; travelers book directly. Check your lease and local rules first.")}
<article class="partner-card free"><span class="kicker c-home">Free option</span><h3>HUD-approved housing counselor</h3><p>Free or low-cost help from a trained counselor on renting, buying, credit and avoiding foreclosure. <a href="https://www.consumerfinance.gov/find-a-housing-counselor/" target="_blank" rel="noopener noreferrer">Find one near you</a>.</p><p class="note">Avoid for-profit "foreclosure rescue" companies that charge fees.</p></article>
</div><p class="partner-foot">We list services we would recommend to a friend. Some links may earn us a commission at no cost to you; any paid link is labeled.</p>
<p style="text-align:center;margin:18px 0 0;font-size:.85rem">This page is general information, not legal or financial advice. Rules vary by state and city.</p></div></section>
'''

housing_body = f'''<section class="pillar-hero"><div class="container pillar-hero-grid"><div>
<span class="eyebrow">Pillar 2 · The Future of Housing</span>
<h1>AI is already deciding parts of <em style="font-style:normal;color:var(--green)">where you live.</em></h1>
<p class="big-q">Where and how do I live when work is remote, uncertain or automated?</p>
<p class="updated">Updated November 2026</p>
<p class="lead">Algorithms now help decide who gets approved for an apartment or a mortgage, what the rent is, and even how homes are built. Here's what's changing, and what you can do about it.</p>
</div><img src="images/hero.webp" alt="Sunlit modern living room and kitchen"></div></section>

{HS_STRIP}<section class="eco-section" id="shifts"><div class="container">
<div class="center-head"><span class="eyebrow">What's happening now</span><h2>4 ways AI is already shaping your housing</h2></div>
<div class="shift-grid">
{shift("01", "It decides who gets approved", "var(--purple)",
 "Many rental applications are scored by software before a person looks at them. In a landmark case, SafeRent settled a lawsuit claiming its scores unfairly marked down Black and Hispanic applicants and people using housing vouchers, and agreed to stop scoring voucher holders. Mortgage lenders are adding AI to underwriting and home valuations too, and 46% of homebuyers say lenders shouldn't run automated valuations without their approval.",
 "AP via Fortune (SafeRent, 2024); Cotality homebuyer survey (2026)",
 "https://fortune.com/2024/11/21/renter-scoring-saferent-million-settle-case-algorithm-discriminating-race-income/",
 ["Turned down for an apartment because of a screening report? The landlord has to tell you which company made it, and you can get a free copy from that company within 60 days.",
  "Dispute anything wrong in the report directly with the screening company.",
  "Ask whether a person can review your application, especially if you use a housing voucher.",
  "Buying? You have the right to a copy of every appraisal and valuation your lender used."])}
{shift("02", "It helps set your rent", "var(--green)",
 "Rent-pricing software from RealPage was at the center of a federal antitrust case over landlords allegedly using shared data to push rents up. RealPage settled with the Justice Department without admitting wrongdoing, and in October 2026 a court approved nearly $360 million in settlements involving 41 defendants. More than 22 states have introduced bills on algorithmic rent pricing.",
 "The Close (Oct 2026); Private Equity Stakeholder Project (Jan 2026)",
 "https://theclose.com/news/news-ai-rent-pricing-settlements-realpage/",
 ["Ask the leasing office how rent is set, and compare your renewal offer with nearby listings before you sign.",
  "If you rented from a large property company, check whether it's part of a rent-pricing settlement. Use only the official court-approved claims site, and never pay anyone to file for you.",
  "Check whether your state or city has passed rules on rent-pricing software."])}
{shift("03", "It changes where you can live", "var(--navy)",
 "About 1 in 4 paid workdays in the U.S. now happen at home, up from roughly 7% before 2020. For many people, the job no longer decides the zip code, but moving only pays off if the math works.",
 "WFH Research (Stanford), 2026", "https://wfhresearch.com/",
 ["Before moving somewhere cheaper, add up the full picture: rent or mortgage, taxes, insurance, commute days, and travel back to the office.",
  "Get your remote or hybrid arrangement in writing before you move.",
  "Ask: if I had to go back to the office full time, would this still work?"])}
{shift("04", "It's changing how homes get built", "var(--purple)",
 "Robotic 3D printers built Wolf Ranch in Texas, a 100-home neighborhood by ICON and Lennar that became Lennar's top-selling community in Central Texas. The homes start just under $400,000. It's a real step toward building faster, but it isn't low-cost housing yet.",
 "Builder magazine; CNBC via NBC Miami",
 "https://www.builderonline.com/design/technology/icons-next-phase-building-a-scalable-platform-for-3d-printed-housing/",
 ["Treat new building tech as a long-term trend, not a reason to wait to buy or rent.",
  "If you look at a 3D-printed or factory-built home, compare it like any other home: price per square foot, insurance, warranty and resale.",
  "Follow local zoning news. Rules on smaller homes and rental units shape what gets built near you."])}
</div>
{HS_NEXT}
</div></section>

{HS_SAFETY}{HS_PROMPTS}{HS_HELP}{join("Housing", "housing-email")}'''

# ---------- Finance ----------
def pcard(kicker, name, url, what, note, kc="c-work"):
    title = f'<a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a>' if url else name
    go = f'<a class="go" href="{url}" target="_blank" rel="noopener noreferrer">Visit {name} →</a>' if url else ''
    return f'<article class="partner-card"><span class="kicker {kc}">{kicker}</span><h3>{title}</h3><p>{what}</p><p class="note">{note}</p>{go}</article>'

finance_body = f'''<section class="pillar-hero"><div class="container pillar-hero-grid"><div>
<span class="eyebrow" style="color:var(--purple)">Pillar 3 · The Future of Finance</span>
<h1>AI is rebuilding <em style="font-style:normal;color:var(--green)">how money works.</em></h1>
<p class="big-q" style="border-color:var(--purple)">What happens to my money when AI changes how we earn, pay and save?</p>
<p class="lead">AI agents are starting to shop and pay for people. Money is moving into apps. The government is opening investment accounts for babies. And paychecks may get less predictable. Here's what's changing, how to get ready, and how to start investing.</p>
<a class="btn primary" href="#shifts">See the 4 shifts →</a> <a class="btn secondary" href="#invest">Learn to invest →</a>
</div>{stat("finance")}</div></section>

<section class="eco-section" id="shifts"><div class="container">
<div class="center-head"><span class="eyebrow">What's happening now</span><h2>4 ways AI is reshaping your money</h2></div>
<div class="shift-grid">
{shift("01", "AI will spend money for you", "var(--purple)",
 "Visa, Mastercard and PayPal have built systems that let AI assistants shop and pay on your behalf, inside tools like ChatGPT and Gemini. You set the limits and the AI completes the purchase. Visa predicts millions of people will use AI agents to buy things by the 2026 holiday season.",
 "Visa (Dec 2025)",
 "https://corporate.visa.com/en/sites/visa-perspectives/newsroom/visa-partners-complete-secure-agentic-transactions.html",
 ["Before you let an AI buy anything, set a spending limit and require your approval for every purchase.",
  "Turn on instant purchase alerts on every card you connect to an AI tool.",
  "Use one card for AI shopping, ideally a credit card or a virtual card number, not your main debit card.",
  "Check your statements weekly. If an AI makes a purchase you didn't approve, dispute it with your card company right away."])}
{shift("02", "Your money is moving into apps", "var(--green)",
 "Elon Musk's X launched X Money for U.S. Premium subscribers in July 2026, with the goal of making X a place to hold, send and spend money. Payment apps, AI budgeting tools and app-based banks all want to hold your paycheck. Not all of them work like a bank, and not all of them protect your money the same way.",
 "Digital Trends (July 2026)",
 "https://www.digitaltrends.com/?p=5993504",
 ["Before you keep money in any app, find out if it's FDIC-insured, and up to how much.",
  "Keep your emergency cushion in an insured bank or savings account, not in a payment app balance.",
  "Turn on two-factor sign-in for every money app, and use a different password for each.",
  "Read what the app does with your data before you connect your bank account."])}
{shift("03", "Investing now starts at birth", "var(--navy)",
 "Trump Accounts launched on July 4, 2026. Parents can open an investment account for any child, and children born during President Trump's second term get $1,000 from the government. The money is invested in U.S. stock index funds and locked until age 18, then can be used for things like school or a first home. Some employers and donors are adding money too.",
 "AP via KPRC (July 2026)",
 "https://www.click2houston.com/news/local/2026/07/07/trump-accounts-launched-on-july-4-giving-newborns-1000-heres-what-to-know/",
 ["Had a baby since 2025? Open an account at <a href='https://trumpaccounts.gov' target='_blank' rel='noopener noreferrer'>trumpaccounts.gov</a> to claim the $1,000.",
  "Older children can have an account too, even without the $1,000.",
  "Ask your employer whether it adds money to employees' children's accounts.",
  "Ask grandparents and relatives to give to the account instead of buying another toy."])}
{shift("04", "Paychecks may get less predictable", "var(--purple)",
 "Elon Musk says AI and robots could make work optional in 10 to 20 years, with a 'universal high income' paid by the government. Critics say no government could afford it, and nothing like it exists today. Meanwhile, 37% of adults couldn't cover a surprise $400 expense with cash.",
 "Fox Business (Musk); Federal Reserve (2025)",
 "https://foxbusiness.com/economy/musk-predicts-ai-create-universal-high-income-make-saving-money-unnecessary",
 ["Don't plan around a future check. Build a cushion of at least one month of bills, then three.",
  "Add a second, smaller source of income that uses human skills: care, trades, teaching or local services.",
  "If you earn side income, set aside money for taxes every time you're paid.",
  "Use the cushion calculator below to see where you stand."])}
</div></div></section>

<section class="eco-section soft" id="tools"><div class="container">
<div class="center-head"><span class="eyebrow">Get ready now</span><h2>Tools for the new money world</h2><p style="margin:12px auto 0;max-width:620px">No email, no sign-up, nothing to buy. Your answers stay on your device.</p></div>
<div class="three">
<article class="step-card"><span class="n">01</span><h3>Know your cushion</h3><p>If your paycheck stopped tomorrow, how long could you cover the bills? Find out in 30 seconds.</p><form class="calc" id="fin-calc" novalidate><label for="fc-bills">Must-pay bills each month</label><div class="calc-in"><span aria-hidden="true">$</span><input id="fc-bills" name="bills" inputmode="decimal" placeholder="2,800" autocomplete="off"></div><small>Rent or mortgage, utilities, phone, insurance, car, food and minimum debt payments.</small><label for="fc-saved">Savings you could use</label><div class="calc-in"><span aria-hidden="true">$</span><input id="fc-saved" name="saved" inputmode="decimal" placeholder="1,500" autocomplete="off"></div><label for="fc-sources">Sources of income in your home</label><select id="fc-sources" name="sources"><option value="1">One paycheck</option><option value="2">Two</option><option value="3">Three or more</option></select><button class="btn primary" type="submit">Show my cushion</button><div id="fin-result" class="calc-result" aria-live="polite" tabindex="-1"></div><small>No email required. Your numbers stay on your device.</small></form></article>
<article class="step-card"><span class="n">02</span><h3>Let AI do your money chores</h3><p>Copy a prompt into any free AI assistant, such as ChatGPT, Claude or Gemini, and fill in the blanks.</p><div class="prompt-list">
<details class="prompt"><summary>Find forgotten subscriptions</summary><p class="prompt-text">Here are the charges from my last two months of bank and card statements (descriptions and amounts only): [paste here]. List every charge that repeats, how often it bills and what it costs per year. Flag any that look like ones I may have forgotten about.</p><button class="copy-btn" type="button">Copy prompt</button></details>
<details class="prompt"><summary>Build a bill calendar</summary><p class="prompt-text">Here are my monthly bills with due dates and amounts: [list]. I get paid on [dates] and take home about $[amount] each time. Show which paycheck should cover which bills, and warn me about any weeks that will be tight.</p><button class="copy-btn" type="button">Copy prompt</button></details>
<details class="prompt"><summary>Make a 30-day cushion plan</summary><p class="prompt-text">My must-pay bills are about $[amount] a month and I have $[amount] saved. Suggest 5 realistic ways to free up $25 to $50 a week without cutting groceries or medicine, then turn them into a simple 30-day plan with one small step each week.</p><button class="copy-btn" type="button">Copy prompt</button></details>
</div><p class="safe-note"><strong>Stay safe:</strong> never paste account numbers, passwords or your Social Security number into an AI tool.</p></article>
<article class="step-card"><span class="n">03</span><h3>Spot AI money scams</h3><p>Scammers now use AI to copy voices, faces and bank messages. Know the warning signs before they call.</p><ul class="scam-list">
<li><strong>A loved one's voice asking for money fast.</strong> AI can copy a voice from a short clip. Hang up and call them back on a number you know.</li>
<li><strong>A "can't-lose" AI trading bot or crypto deal,</strong> often in a video with a famous face. Guaranteed returns are a scam.</li>
<li><strong>Pay by gift card, wire, crypto or payment app.</strong> Real banks, agencies and family emergencies don't demand these.</li>
<li><strong>A text or email from "your bank" asking you to verify.</strong> Don't click. Open your bank's app yourself.</li>
<li><strong>Set a family code word</strong> that a caller has to know before anyone sends money.</li>
</ul><a href="https://consumer.ftc.gov/consumer-alerts/2023/03/scammers-use-ai-enhance-their-family-emergency-schemes" target="_blank" rel="noopener noreferrer">Read the FTC's warning →</a><p class="safe-note">Got scammed or targeted? Report it at <a href="https://reportfraud.ftc.gov" target="_blank" rel="noopener noreferrer">ReportFraud.ftc.gov</a>.</p></article>
</div></div></section>

<section class="eco-section" id="invest"><div class="container">
<div class="center-head"><span class="eyebrow">Learn to invest</span><h2>How to start investing in stocks</h2><p style="margin:12px auto 0;max-width:680px">AI may change who earns a paycheck, but owning a small piece of the companies doing the work is open to everyone. You don't need a lot of money. You need a plan and time.</p></div>
<div class="invest-grid">
<ol class="invest-steps">
<li><h3>Build your cushion first</h3><p>Money you might need in the next few years belongs in savings, not stocks. Pay off high-interest credit cards too: it's a guaranteed return.</p></li>
<li><h3>Grab any free money</h3><p>If your job has a 401(k) or 403(b) with an employer match, put in at least enough to get the full match. That's free money.</p></li>
<li><h3>Pick the right account</h3><p>No match at work? A Roth IRA lets your investments grow tax-free for retirement. For goals that aren't retirement, use a regular brokerage account.</p></li>
<li><h3>Start with a low-cost index fund</h3><p>An index fund buys a little of hundreds of companies at once. An S&amp;P 500 index fund owns about 500 of the largest U.S. companies, including many building AI. Look for a fee (expense ratio) of 0.10% or less.</p></li>
<li><h3>Put it on autopilot</h3><p>Set up an automatic weekly or monthly deposit, even $10 or $25. Many apps let you buy fractions of a share, so small amounts work.</p></li>
<li><h3>Stay in for the long run</h3><p>Stocks go up and down, sometimes a lot. Plan to leave the money for 5 years or more, and don't sell in a panic when the market drops.</p></li>
</ol>
<article class="step-card"><span class="n">$</span><h3>See what small amounts can grow into</h3><form class="calc" id="grow-calc" novalidate><label for="gc-amt">Amount you could invest each week</label><div class="calc-in"><span aria-hidden="true">$</span><input id="gc-amt" name="amt" inputmode="decimal" placeholder="25" autocomplete="off"></div><label for="gc-years">For how many years</label><select id="gc-years" name="years"><option value="5">5 years</option><option value="10">10 years</option><option value="20" selected>20 years</option><option value="30">30 years</option></select><label for="gc-rate">Average yearly return</label><select id="gc-rate" name="rate"><option value="5">5% (cautious)</option><option value="7" selected>7% (middle)</option><option value="9">9% (hopeful)</option></select><button class="btn primary" type="submit">Show my growth</button><div id="grow-result" class="calc-result" aria-live="polite" tabindex="-1"></div><small>An estimate, not a promise. Stock returns aren't guaranteed and some years lose money. No email required. Your numbers stay on your device.</small></form></article>
</div>
<div class="center-head" style="margin-top:48px"><h3 style="font-family:'Playfair Display',serif;font-weight:500;font-size:1.7rem">Where to open an account</h3></div>
<div class="partner-grid">
{pcard("Our top pick · do it yourself", "Fidelity", "https://www.fidelity.com", "A large, long-established broker with no account fees, fractional shares, IRAs and its own very low-cost index funds. A good home for your first index fund.", "Best if you're willing to pick one or two index funds yourself and leave them alone.")}
{pcard("Hands-off · automated investing", "Betterment", "https://www.betterment.com", "A robo-advisor: software picks a mix of low-cost funds for your goal, rebalances it and reinvests for you. Good if you want to set it and forget it.", "Charges a yearly fee based on your balance. Offers IRAs and regular accounts.")}
{pcard("Small amounts · simple app", "Robinhood", "https://robinhood.com", "A simple app for buying stocks and index funds, including fractions of a share for as little as $1. Offers IRAs too.", "Stick to index funds and long-term investing. Skip options, day trading and crypto, which the app also offers.")}
</div></div></section>

<section class="eco-section soft" id="help"><div class="container"><div class="center-head"><span class="eyebrow">Where to get help</span><h2>Services built for what's coming</h2><p style="margin:12px auto 0;max-width:660px">Matched to the shifts above: protection from AI scams, a safe home for your cushion, and tools for side income. Free options are listed too.</p></div><div class="partner-grid">
{pcard("Protect · AI scams and identity theft", "Aura", "https://www.aura.com", "Identity theft protection, credit and bank monitoring, a VPN, antivirus and a password manager in one app. Covers the whole family.", "Paid subscription. Compare plans, and check whether your bank or employer already offers ID protection free.")}
{pcard("Cushion · where your safety net lives", "Wealthfront Cash Account", "https://www.wealthfront.com", "Earns like a high-yield savings account and works like a checking account, with no account fees and FDIC insurance through partner banks.", "Rates change. Compare with at least one other high-yield savings account before you move money.")}
{pcard("Budget · see where it all goes", "Monarch Money", "https://www.monarchmoney.com", "Connects your bank, card and investment accounts in one place, with budgets, goals and spending tracking.", "Costs $99.99 a year or $14.99 a month after a 7-day free trial.")}
{pcard("Side income · AI tax help", "Keeper", "https://www.keepertax.com", "Uses AI to scan your purchases for tax write-offs and helps freelancers and gig workers file, with tax pros reviewing returns.", "Paid plans. Most useful once you have 1099 or side-hustle income.")}
{pcard("Side income · banking", "Found", "https://found.com", "Banking built for freelancers and side hustlers, with bookkeeping, invoicing and built-in tax estimates.", "Free account with an optional paid upgrade. Keep side income separate from your personal account.")}
{pcard("Credit · build it from scratch", "Self", "https://www.self.inc", "A credit builder account: you make small monthly payments into savings, which builds payment history with the credit bureaus. No hard credit check.", "It's a small loan. You get your savings back at the end, minus interest and fees.")}
</div>
<article class="partner-card free" style="margin-top:20px"><span class="kicker c-home">Free options</span><h3>Free help</h3><p>Claim a child's $1,000 at <a href="https://trumpaccounts.gov" target="_blank" rel="noopener noreferrer">trumpaccounts.gov</a>. Use your bank's own budgeting tools or a simple spreadsheet. If debt is the problem, get nonprofit credit counseling through the <a href="https://www.nfcc.org" target="_blank" rel="noopener noreferrer">National Foundation for Credit Counseling</a>. Report scams at <a href="https://reportfraud.ftc.gov" target="_blank" rel="noopener noreferrer">ReportFraud.ftc.gov</a>.</p></article>
<p class="partner-foot">We list services we would recommend to a friend. Some links may earn us a commission at no cost to you; any paid link is labeled. This is general information, not financial advice.</p></div></section>

<section class="soft-band"><div class="container">
<div class="center-head"><span class="eyebrow" style="color:var(--purple)">Coming in the Finance series</span><h2>What we'll cover next</h2></div>
<div class="three">
<article class="topic-card"><h3>Letting AI pay your bills safely</h3><p>How AI shopping agents work, which settings to turn on, and what to never hand over.</p></article>
<article class="topic-card"><h3>Trump Accounts, step by step</h3><p>Who qualifies, how to claim the $1,000, and how family and employers can add to it.</p></article>
<article class="topic-card"><h3>Your first index fund, step by step</h3><p>How to open an account, pick a low-cost fund and set it on autopilot.</p></article>
</div></div></section>
{join("Finance", "finance-email")}'''


# ---------- Healthcare ----------

def big_stat(kicker, cls, num, text, src, url):
    return (f'<article class="stat-card"><span class="kicker {cls}">{kicker}</span><p class="num {cls}">{num}</p><p>{text}</p>'
            f'<p class="src">Source: <a href="{url}" target="_blank" rel="noopener noreferrer">{src}</a></p></article>')

HC_TASKS = [
 ("doc", "Writing notes, reports or charting"),
 ("code", "Coding, billing or insurance claims"),
 ("sched", "Scheduling, prior authorizations or phones"),
 ("trans", "Transcribing dictation"),
 ("img", "Reviewing images, scans or test results"),
 ("msg", "Answering patient messages and questions"),
 ("hands", "Hands-on patient care or procedures"),
 ("teach", "Teaching patients and families"),
 ("team", "Coordinating a care team or unit"),
 ("comfort", "Calming, comforting or advocating for patients"),
]
hc_checks = "".join(f'<label class="option"><input type="checkbox" name="task" value="{v}"> {t}</label>' for v, t in HC_TASKS)

HC_STRIP = '''<section class="steps-band"><div class="container"><div class="center-head"><span class="eyebrow">Start here</span><h2>Three ways to stay ahead in healthcare</h2></div>
<div class="plp-grid">
<a class="plp-card" href="#task-check"><span class="n">1</span><h3>Protect</h3><p>See which parts of your job AI is taking over, and which stay human.</p><span class="go">Check my tasks →</span></a>
<a class="plp-card" href="#ladders"><span class="n">2</span><h3>Move up</h3><p>See the career ladders, the pay at each step, and how to climb.</p><span class="go">See career ladders →</span></a>
<a class="plp-card" href="#ai-at-work"><span class="n">3</span><h3>Lead the change</h3><p>Become the person your team asks when the new AI tools arrive.</p><span class="go">Start with AI prompts →</span></a>
</div></div></section>

<section class="eco-section soft" id="from-alaina"><div class="container"><div class="founder-note">
<span class="eyebrow" style="color:var(--green)">From someone who's lived it</span>
<p>I've spent more than 30 years in healthcare, in diagnostic radiology, CT and interventional cardiovascular work. I watched film turn into digital images, paper charts turn into electronic records, and now I'm watching AI arrive in the reading room and the exam room.</p>
<p>Every one of those changes was supposed to replace people. None of them did. What they changed was which skills mattered. The people who came out ahead learned the new system early, became the person everyone else asked for help, and never lost sight of the patient. As a clinical applications super user, that's the role I took on, and it shaped the rest of my career.</p>
<p>That's what this page is for: protecting the career you've built, seeing where you can move up, and helping lead the change instead of having it happen to you.</p>
<p class="sig">Alaina Tillage, CIIP, RT(R)(CT)(CI)</p>
</div></div></section>

'''

HC_NEXT = '''<div class="next-wave"><span class="eyebrow" style="color:#c9a9ea">What's coming next</span><h3>From AI that drafts to AI that runs whole processes</h3><p>Today, most healthcare AI drafts notes or flags images for a person to review. The next step is AI that handles whole processes, like prior authorizations. In January 2026, Medicare began testing AI-assisted prior authorization review for certain services in six states: Arizona, New Jersey, Ohio, Oklahoma, Texas and Washington. CMS says licensed clinicians make any recommendation to deny payment, and some members of Congress have criticized the program as a risk to timely care.</p><p class="next-do"><strong>What to do now:</strong> strong documentation matters more than ever when software reads it first. Learn how AI decisions are made and appealed where you work, and be the person who can explain them to patients and coworkers.</p></div>'''

def rung(title, pay, note=""):
    p = f'<span class="pay">{pay}</span>' if pay else ''
    n = f'<span class="rnote">{note}</span>' if note else ''
    return f'<li><strong>{title}</strong>{p}{n}</li>'

LADDERS = [
 ("Bedside care", "c-home", [rung("Nursing assistant","$42,260","State-approved program"), rung("Licensed practical nurse","$64,400","About a 1-year program"), rung("Registered nurse","$97,550","Associate's or bachelor's degree"), rung("Nurse practitioner","$132,300","Master's degree; jobs projected to grow 41% by 2035")], "https://www.bls.gov/ooh/healthcare/registered-nurses.htm"),
 ("Imaging", "c-work", [rung("Radiologic technologist","$80,110","Associate's degree"), rung("CT or MRI technologist","$95,480 (MRI)","Advanced certification on top of your rad tech license"), rung("Imaging informatics","","PACS and imaging IT roles. The CIIP certification combines clinical and IT skills")], "https://www.bls.gov/ooh/healthcare/radiologic-technologists.htm"),
 ("Health information", "c-work", [rung("Medical records specialist","$51,140","Postsecondary certificate"), rung("Health information technologist","$68,020","Associate's degree"), rung("Coding auditor or compliance","","Checking and correcting AI-coded claims is a growing need")], "https://www.bls.gov/ooh/healthcare/"),
]
ladder_html = "".join(f'<article class="ladder"><span class="kicker {k}">{t} ladder</span><ol>{"".join(r)}</ol><a class="go" href="{u}" target="_blank" rel="noopener noreferrer">Training and pay details ↗</a></article>' for t,k,r,u in LADDERS)

HC_LADDERS = f'''<section class="eco-section" id="ladders"><div class="container">
<div class="center-head"><span class="eyebrow" style="color:var(--green)">Move up</span><h2>Healthcare career ladders</h2><p style="margin:12px auto 0;max-width:680px">Each step builds on the one before it, and many employers help pay for the next one. The higher rungs mix hands-on care or clinical skill with judgment, the work AI is least able to take over.</p></div>
<div class="ladder-grid">{ladder_html}</div>
<div class="tip-row" style="margin-top:22px"><article class="tip-box"><h3>How to climb without starting over</h3><ul class="scam-list"><li><strong>Ask about tuition help first.</strong> Many hospitals pay for the next credential, sometimes in exchange for a work commitment.</li><li><strong>Look for "bridge" programs</strong> like LPN-to-RN or RN-to-BSN that count what you already know.</li><li><strong>Become a super user.</strong> Volunteering to learn a new system first is one of the fastest ways to get noticed for informatics and leadership roles.</li></ul></article>
<article class="tip-box"><h3>Not in healthcare yet?</h3><p>Nursing assistant and medical records programs are short, and both are first rungs on a ladder. See more hands-on careers on the Work page.</p><a class="btn primary" href="work.html#hands-on">Hands-on careers →</a></article></div>
<p class="safe-note" style="margin-top:18px">Pay: <a href="https://www.bls.gov/ooh/healthcare/" target="_blank" rel="noopener noreferrer">U.S. Bureau of Labor Statistics, Occupational Outlook Handbook</a>, 2025 median pay. Pay varies by state, setting and experience.</p>
</div></section>

'''

hc_prompts = [
 ("Study for a certification", "Quiz me on [topic] for the [certification name] exam. Ask one question at a time, wait for my answer, then explain why it's right or wrong. Get harder as I improve."),
 ("Explain a new policy simply", "Explain this policy or procedure in simple, everyday words, then list the three things that change for me day to day: [paste the policy, with no patient information]."),
 ("Write a patient handout", "Write a one-page handout explaining [procedure or condition] at a 6th-grade reading level. Use short sentences and a 'What to expect' section. I will check it for accuracy before using it."),
 ("Make a tip sheet for your team", "I'm the go-to person for [new system or feature]. Write a one-page tip sheet for coworkers: the five things they'll use most, common mistakes, and who to ask for help."),
]
hc_prompt_html = "".join(f'<details class="prompt"><summary>{t}</summary><p class="prompt-text">{p}</p><button class="copy-btn" type="button">Copy prompt</button></details>' for t,p in hc_prompts)

HC_PROMPTS = f'''<section class="eco-section soft" id="ai-at-work"><div class="container">
<div class="center-head"><span class="eyebrow">Lead the change</span><h2>AI prompts for healthcare workers</h2><p style="margin:12px auto 0;max-width:660px">Copy a prompt into any AI assistant and fill in the blanks. <strong>Never paste patient names, dates of birth, record numbers or any other patient information</strong> into a public AI tool, and follow your organization's AI policy.</p></div>
<div class="tip-row"><article class="tip-box"><h3>Four prompts to start with</h3><div class="prompt-list">{hc_prompt_html}</div></article>
<article class="tip-box course-box"><span class="kicker c-work">Coming soon</span><h3>AI for Healthcare Workers</h3><p>A short, practical course from someone who's worked in imaging and cardiovascular care for 30 years: how AI tools work in clinical settings, what to trust and what to check, and how to become the go-to person when they arrive.</p><a class="btn primary" href="#join">Get notified when it opens →</a><p class="safe-note" style="margin-top:14px">Join the free newsletter and you'll hear first.</p></article></div>
</div></section>

'''

healthcare_body = f'''<section class="pillar-hero"><div class="container pillar-hero-grid"><div>
<span class="eyebrow">Pillar 5 · The Future of Healthcare Work</span>
<h1>Healthcare is hiring. AI is changing <em style="font-style:normal;color:var(--green)">what the work looks like.</em></h1>
<p class="big-q">How do I build a lasting healthcare career when AI is taking over the paperwork?</p>
<p class="updated">Updated November 2026</p>
<p class="lead">Healthcare is still the country's biggest job engine. The change isn't fewer jobs overall. It's which tasks people do, which roles grow, and which skills employers pay for.</p>
</div>{big_stat("Healthcare jobs", "c-home", "~2 million", "new healthcare and social assistance jobs projected from 2024 to 2034, the fastest-growing sector at 8.4%.", "U.S. Bureau of Labor Statistics, 2024–34 projections", "https://fraser.stlouisfed.org/files/docs/publications/bls_mlr/bls_mlr_20260108.pdf")}</div></section>

{HC_STRIP}<section class="eco-section" id="shifts"><div class="container">
<div class="center-head"><span class="eyebrow">What's happening now</span><h2>4 ways AI is reshaping healthcare work</h2></div>
<div class="shift-grid">
{shift("01", "Care jobs keep growing", "var(--green)",
 "An aging population keeps demand rising. Nurse practitioners are projected to be the fastest-growing healthcare occupation, up about 40% from 2024 to 2034, with medical and health services managers, physical therapist assistants and physician assistants close behind.",
 "BLS via Becker's Hospital Review", "https://www.beckershospitalreview.com/workforce/12-fastest-growing-healthcare-jobs-by-2034",
 ["Look at the growing roles one step up from yours, and what training they take.",
  "Ask your employer about tuition help or career ladders before paying on your own.",
  "Roles that combine hands-on care with judgment are growing fastest."])}
{shift("02", "AI is taking over the paperwork", "var(--purple)",
 "81% of physicians now use AI at work, up from 38% in 2023, mostly for documentation and research summaries. Some say AI scribes save 15 to 60 minutes a day, but in one 2026 poll 42% of users reported no time saved, so results depend on the tool and how it's set up.",
 "AMA 2026 survey via Health Data Management; AMA; Medical Economics",
 "https://healthdatamanagement.com/articles/clinicians-increasingly-turn-to-ai-as-timely-relief-for-burdensome-tasks/",
 ["Learn the AI documentation tool your organization uses, and become the person others ask.",
  "Always review AI-drafted notes before signing. You are still responsible for what's in the chart.",
  "Speak up during rollouts. Physicians and staff want a say in how these tools are chosen."])}
{shift("03", "Imaging is the front line", "var(--navy)",
 "Of the 1,524 AI-enabled devices the FDA had authorized through March 2026, 1,163 were for radiology, about 76% of the total. Imaging is where clinical AI is most established, so imaging staff see the change first.",
 "Radiology Business, June 2026",
 "https://radiologybusiness.com/topics/artificial-intelligence/radiology-gets-68-new-fda-cleared-algorithms",
 ["Learn how AI triage and detection tools fit into your department's workflow.",
  "Know the limits: AI flags findings, but people still make the call and talk to patients.",
  "Skills that connect clinical work and IT, like PACS and imaging informatics, are in demand."])}
{shift("04", "Admin and transcription jobs are shrinking", "var(--purple)",
 "Medical transcriptionist jobs are projected to decline 5% from 2024 to 2034 as speech recognition takes over first drafts. In coding, billing and claims, AI is speeding up the work, but staffing firms say it raises the need for people who check and audit it.",
 "BLS Occupational Outlook Handbook; Addison Group 2026 guide",
 "https://www.bls.gov/ooh/Healthcare/Medical-transcriptionists.htm",
 ["If you work in transcription, coding or billing, move toward auditing, compliance or editing AI output.",
  "Add a credential in a growing area, such as health information or revenue cycle management.",
  "Consider bridging into a patient-facing role if you enjoy working with people."])}
</div>
{HC_NEXT}
</div></section>

<section class="soft-band" id="task-check"><div class="container">
<div class="center-head"><span class="eyebrow" style="color:var(--purple)">Task check</span><h2>Which parts of your job is AI changing?</h2><p style="margin:12px auto 0;max-width:640px">Pick the tasks that take up most of your workday. You'll see which ones AI is already handling, which it helps with, and which stay human.</p></div>
<form class="calc task-check" id="hc-check" novalidate>
<fieldset><legend class="sr-only">Your main tasks</legend><div class="task-grid">{hc_checks}</div></fieldset>
<button class="btn primary" type="submit">Show my results</button>
<div id="hc-result" class="calc-result" aria-live="polite" tabindex="-1"></div>
<small>A general guide based on where AI is being used today, not a prediction about your specific job. No email required. Your answers stay on your device.</small>
</form></div></details></div>
</div></section>

{HC_LADDERS}{HC_PROMPTS}<section class="eco-section" id="help"><div class="container"><div class="center-head"><span class="eyebrow">Where to get help</span><h2>Build skills and move up</h2><p style="margin:12px auto 0;max-width:660px">Continuing education, certification prep and job tools for healthcare workers, matched to the shifts above.</p></div><div class="partner-grid"><article class="partner-card"><span class="kicker c-work">Nurses · continuing education</span><h3><a href="https://www.nurse.com" target="_blank" rel="noopener noreferrer">Nurse.com</a></h3><p>More than 1,000 ANCC-accredited CE courses, state renewal packages and certification prep, all online.</p><p class="note">Check your state board of nursing's CE requirements before you buy a package.</p><a class="go" href="https://www.nurse.com" target="_blank" rel="noopener noreferrer">Visit Nurse.com →</a></article><article class="partner-card"><span class="kicker c-work">All healthcare workers · AI skills</span><h3><a href="https://www.coursera.org/courses?query=ai%20in%20healthcare" target="_blank" rel="noopener noreferrer">Coursera</a></h3><p>University and industry courses on AI in healthcare, data and health informatics. Many are free to audit.</p><p class="note">Good for building skills that connect clinical work and technology.</p><a class="go" href="https://www.coursera.org/courses?query=ai%20in%20healthcare" target="_blank" rel="noopener noreferrer">Visit Coursera →</a></article><article class="partner-card"><span class="kicker c-work">Certification prep</span><h3><a href="https://www.mometrix.com" target="_blank" rel="noopener noreferrer">Mometrix</a></h3><p>Study guides, flashcards and practice tests for nursing specialty certifications and nurse practitioner exams.</p><p class="note">Certifications are one of the clearest ways to move into a growing role.</p><a class="go" href="https://www.mometrix.com" target="_blank" rel="noopener noreferrer">Visit Mometrix →</a></article><article class="partner-card"><span class="kicker c-work">NPs, PAs and physicians · board prep</span><h3><a href="https://www.boardvitals.com" target="_blank" rel="noopener noreferrer">BoardVitals</a></h3><p>Online question banks for board exams and recertification.</p><p class="note">Best for clinicians studying for a specific board exam.</p><a class="go" href="https://www.boardvitals.com" target="_blank" rel="noopener noreferrer">Visit BoardVitals →</a></article><article class="partner-card free"><span class="kicker c-home">Free option</span><h3><a href="https://www.incrediblehealth.com" target="_blank" rel="noopener noreferrer">Incredible Health</a></h3><p>A free job marketplace for nurses where hospitals apply to you, plus free career tools.</p><p class="note">Free for nurses; hospitals pay to use it.</p><a class="go" href="https://www.incrediblehealth.com" target="_blank" rel="noopener noreferrer">Visit Incredible Health →</a></article></div><p class="partner-foot">We list services we would recommend to a colleague. Some links may earn us a commission at no cost to you; any paid link is labeled.</p></div></section>
<p style="text-align:center;margin:-40px 0 50px;font-size:.85rem">General career information, not medical, legal or employment advice.</p>
{join("Healthcare Work", "hc-email")}'''

# ---------- Education ----------
SHOWCASE_FORM = ""  # paste the Google Form / Tally link here
SHOWCASE_CTA_HTML = (f'<a class="btn primary" href="{SHOWCASE_FORM}" target="_blank" rel="noopener noreferrer">I want to present →</a> <a class="btn secondary" href="{SHOWCASE_FORM}" target="_blank" rel="noopener noreferrer">I\'m hiring →</a>' if SHOWCASE_FORM else '<p class="soon">The interest list opens soon.</p>')

SHOWCASE_ON = True  # set True once the interest form link is in SHOWCASE_FORM
SHOWCASE_BLOCK = ('''<div class="showcase"><div><span class="eyebrow" style="color:#c9a9ea">Coming soon</span><h3>Skills Showcase</h3><p>Online events where working people show what they can do in five minutes, and local businesses come looking for talent. No degree required to present.</p></div><div class="showcase-cta">'''+SHOWCASE_CTA_HTML+'''</div></div>''') if SHOWCASE_ON else ''

education_body = f'''<section class="pillar-hero"><div class="container pillar-hero-grid"><div>
<span class="eyebrow" style="color:var(--purple)">Pillar 4 · The Future of Education</span>
<h1>How we learn is changing. <em style="font-style:normal;color:var(--purple)">For you and your kids.</em></h1>
<p class="big-q" style="border-color:var(--purple)">How will I keep learning, and how will my kids learn, when AI can teach almost anything?</p>
<p class="lead">Employers are starting to care more about what you can do than where you went to school. AI tutors are arriving for everyone. Work skills need updating every few years. And more families are learning outside the classroom. Here's what's changing, and how to keep up.</p>
<a class="btn primary" href="#skills">Learning for you →</a> <a class="btn secondary" href="#kids">How your kids will learn →</a>
</div>{big_stat("Your skills", "c-work", "39%", "of workers' core skills are expected to change by 2030, according to employers worldwide.", "World Economic Forum, Future of Jobs Report 2025", "https://www.weforum.org/publications/the-future-of-jobs-report-2025/in-full/3-skills-outlook/")}</div></section>

<section class="steps-band"><div class="container"><div class="center-head"><span class="eyebrow">Start here</span><h2>Plan, learn, prove it</h2></div>
<div class="plp-grid">
<a class="plp-card" href="#learn-first" data-open="learn-first"><span class="n">1</span><h3>Plan</h3><p>Answer four questions and see which skills to learn first.</p><span class="go">Get my starting plan →</span></a>
<a class="plp-card" href="#tutor-prompt"><span class="n">2</span><h3>Learn</h3><p>Turn any AI assistant into a patient tutor with one prompt.</p><span class="go">Get the tutor prompt →</span></a>
<a class="plp-card" href="#passport" data-open="passport"><span class="n">3</span><h3>Prove it</h3><p>Build a one-page Skills Passport to show employers what you can do.</p><span class="go">Build my passport →</span></a>
</div></div></section>

<section class="eco-section" id="shifts"><div class="container">
<div class="center-head"><span class="eyebrow">What's happening now</span><h2>4 ways education is changing</h2></div>
<div class="shift-grid">
{shift("01", "Proof of skills is starting to count as much as a diploma", "var(--purple)",
 "Employers have opened almost 600,000 jobs to workers without a four-year degree, and 33 states have dropped degree requirements for many government jobs. But a Harvard study found 45% of companies that dropped the requirement changed only the job post, not who they hired. People who can show what they've done have the edge.",
 "Opportunity@Work (2026); Harvard Business School and Burning Glass Institute (2024)", "https://www.opportunityatwork.org/about/press-release/opportunity-work-names-lafawn-davis-to-board-of-directors-as-skills-first-movement-gains-ground-in-the-ai-economy",
 ["Keep a simple record of projects you finish and what they achieved.",
  "Earn a short certificate in a skill employers are asking for.",
  "See where the skills-first jobs are in the section below."])}
{shift("02", "Everyone is getting a personal AI tutor", "var(--green)",
 "Elon Musk posted that \"it's AI tutors or the slow death of civilization,\" and in 2026 his company xAI began rolling out its Grok chatbot as a nationwide tutor in El Salvador. But a two-year trial in 18 Tennessee middle schools found most students stopped using the Khanmigo AI tutor once it refused to just give answers. AI tutors help when people actually use them to learn.",
 "Mother Jones (Musk); FutureEd and NBER (Khanmigo, 2026)", "https://www.future-ed.org/students-tried-khanmigos-ai-tutor-most-didnt-want-its-help/",
 ["Use AI to explain, quiz and coach you, not to do the work for you (copy the prompts on this page).",
  "Choose kids' tools that give hints and questions, not answers, and check their age rules.",
  "Sit with younger kids for the first sessions.",
  "Keep real teachers, classmates and study partners in the picture. AI can't replace them."])}
{shift("03", "Learning doesn't stop at graduation anymore", "var(--navy)",
 "That 39% figure at the top of the page means a degree earned 10 or 20 years ago won't carry anyone through a whole career anymore. AI, data and technology skills are growing fastest. Learning is becoming something adults do all their lives, not just in school.",
 "World Economic Forum, Future of Jobs Report 2025", "https://www.weforum.org/publications/the-future-of-jobs-report-2025/in-full/3-skills-outlook/",
 ["Plan to learn one new work skill every year.",
  "Set aside an hour a week for learning, like you would for exercise.",
  "Ask your employer what training or tuition help it offers. Many companies pay for it.",
  "Teach your kids that learning doesn't end at graduation, by letting them see you do it."])}
{shift("04", "School is moving out of the classroom", "var(--purple)",
 "Homeschooling grew an average of 5.4% across reporting states in 2024–25, and homeschoolers are now about 6% of U.S. students, up from about 3% before the pandemic. In 18 states, education savings accounts let some families use public education money on tutoring, classes or materials. Starting January 1, 2027, a new federal Education Freedom Tax Credit will fund K–12 scholarships through donations, but only in states whose governors opt in. Supporters call it the biggest expansion of school choice yet; groups including the National Education Association oppose it as a voucher program.",
 "Johns Hopkins Homeschool Hub via Reason (2025); EdChoice (2026); U.S. Treasury (2026)", "https://reason.com/2025/11/19/homeschooling-hits-record-numbers",
 ["Look up your state's homeschool and education savings account rules on official state websites.",
  "Check whether your state has opted in to the federal Education Freedom Tax Credit before 2027 (<a href='https://content.govdelivery.com/accounts/USTREAS/bulletins/42d50e4' target='_blank' rel='noopener noreferrer'>Treasury announcement</a>).",
  "Ask about free public virtual schools if you want structure without a classroom.",
  "Find a co-op or group class so neither you nor your child learns alone."])}
</div></div></section>

<section class="eco-section" id="skills"><div class="container">
<div class="center-head"><span class="eyebrow" style="color:var(--purple)">For you</span><h2>Learning for you: build skills, then prove them</h2><p style="margin:12px auto 0;max-width:680px">Start with a personal plan for what to learn, use AI as your tutor, then find the employers who hire for skills and show them what you can do.</p></div>
<div class="tip-row" style="margin:0 0 22px">
<article class="tip-box" id="learn-first"><h3>Not sure what to learn first?</h3><p>Answer four quick questions and get a personal starting plan: which skills to learn first and where to learn them.</p><details class="tool-toggle"><summary class="btn primary">Get my starting plan →</summary><form class="calc path-form compact" id="learn-finder" novalidate><fieldset><legend>What's your goal?</legend><label class="option"><input type="radio" name="goal" value="keep"> Keep my current job safe</label><label class="option"><input type="radio" name="goal" value="promote"> Get promoted</label><label class="option"><input type="radio" name="goal" value="change"> Change careers</label><label class="option"><input type="radio" name="goal" value="side"> Start a side business</label></fieldset><fieldset><legend>What kind of work do you do?</legend><label class="option"><input type="radio" name="work" value="office"> Office or admin</label><label class="option"><input type="radio" name="work" value="health"> Health care</label><label class="option"><input type="radio" name="work" value="trades"> Trades or hands-on work</label><label class="option"><input type="radio" name="work" value="customer"> Customer service or sales</label><label class="option"><input type="radio" name="work" value="other"> Something else</label></fieldset><fieldset><legend>How comfortable are you with AI tools?</legend><label class="option"><input type="radio" name="comfort" value="0"> Never used them</label><label class="option"><input type="radio" name="comfort" value="1"> Tried a few times</label><label class="option"><input type="radio" name="comfort" value="2"> Use them often</label></fieldset><fieldset><legend>How much time do you have each week?</legend><label class="option"><input type="radio" name="time" value="1"> About 1 hour</label><label class="option"><input type="radio" name="time" value="2"> 2–4 hours</label><label class="option"><input type="radio" name="time" value="3"> 5 hours or more</label></fieldset><button class="btn primary" type="submit">Show my starting plan</button><div id="learn-result" class="calc-result" aria-live="polite" tabindex="-1"></div><small>No email required. Your answers stay on your device.</small></form></details></article>
<article class="tip-box" id="tutor-prompt"><h3>Prompt: make AI your tutor</h3><p>Paste this into ChatGPT, Claude or Gemini and fill in the blanks.</p>
<details class="prompt" open><summary>Personal tutor prompt</summary><p class="prompt-text">Teach me [topic] as if I'm a beginner. My goal is [why I want to learn it]. Explain one small step at a time with an everyday example. After each step, ask me one question to check I understood. If I get it wrong, explain it a different way. Don't move on until I get it right.</p><button class="copy-btn" type="button">Copy prompt</button></details></article>
</div>
<div class="center-head" style="margin-top:44px"><h3 style="font-family:'Playfair Display',serif;font-weight:500;font-size:1.7rem">No degree? Here's where the doors are opening</h3></div>
<div class="three four">
<article class="step-card"><span class="n">01</span><h3>State government jobs</h3><p>Many states now hire for skills and experience instead of a diploma.</p><p class="how-to"><strong>How to look:</strong> search "[your state] state jobs," then look for postings that say "or equivalent experience."</p></article>
<article class="step-card"><span class="n">02</span><h3>Paid apprenticeships</h3><p>Earn a paycheck while you train, in fields from IT and health care to construction and manufacturing. No degree needed.</p><a href="https://www.apprenticeship.gov/apprenticeship-job-finder" target="_blank" rel="noopener noreferrer">Search Apprenticeship.gov →</a></article>
<article class="step-card"><span class="n">03</span><h3>Skills-first employers</h3><p>Companies such as Accenture, Google, IBM, LinkedIn and Walmart have joined the Tear the Paper Ceiling coalition to hire workers skilled through other routes.</p><a href="https://tearthepaperceiling.org" target="_blank" rel="noopener noreferrer">Visit Tear the Paper Ceiling →</a></article>
<article class="step-card"><span class="n">04</span><h3>Career certificates</h3><p>Professional certificates from Google, IBM and others in AI, data, IT support and more. Many courses can be audited for free, and financial aid is available.</p><a href="https://www.coursera.org/professional-certificates" target="_blank" rel="noopener noreferrer">Browse certificates on Coursera →</a></article>
</div>
<div class="tip-row one">
<article class="tip-box"><h3>How to spot an employer that really hires for skills</h3><p>A Harvard and Burning Glass Institute study found that 45% of companies that dropped degree requirements changed the job post but not who they actually hired. Look for these signs:</p><ul class="scam-list"><li><strong>The post says "or equivalent experience"</strong> and lists skills, not just schools.</li><li><strong>They test skills</strong> with a work sample, skills test or trial project.</li><li><strong>They run apprenticeships</strong> or paid training programs.</li><li><strong>People in that job don't all have degrees.</strong> Check current employees' profiles on LinkedIn.</li></ul><p class="src" style="font-size:.8rem">Source: <a href="https://gof.mit.edu/when-firms-drop-college-degree-requirements-does-hiring-change-a-new-study-gives-stark-answers" target="_blank" rel="noopener noreferrer">Harvard Business School and Burning Glass Institute (2024)</a></p></article>
<article class="tip-box" id="passport"><h3>Build your Skills Passport</h3><p>Show up with proof. Turn three things you've done into a one-page summary of your skills, then print it or save it as a PDF to share with employers.</p>
<details class="tool-toggle"><summary class="btn primary">Build my passport →</summary>
<form class="calc passport-form" id="pp-form" novalidate>
<div class="pp-grid"><div><label for="pp-name">Your name</label><input id="pp-name" name="name" autocomplete="off"></div><div><label for="pp-goal">The job you're aiming for</label><input id="pp-goal" name="goal" placeholder="Medical office coordinator"></div><div><label for="pp-contact">How to reach you (email or phone)</label><input id="pp-contact" name="contact" autocomplete="off"></div><div><label for="pp-skills">Your top skills, separated by commas</label><input id="pp-skills" name="skills" placeholder="Scheduling, Excel, calming upset customers"></div></div>
<div class="pp-grid three"><fieldset class="pp-proj"><legend>Project 1</legend><label for="pp-t1">Short title</label><input id="pp-t1" name="t1" placeholder="Cut patient check-in time"><label for="pp-d1">What you did and the problem it solved</label><textarea id="pp-d1" name="d1" rows="2"></textarea><label for="pp-r1">The result (use a number if you can)</label><input id="pp-r1" name="r1" placeholder="Wait times dropped from 20 to 8 minutes"></fieldset><fieldset class="pp-proj"><legend>Project 2</legend><label for="pp-t2">Short title</label><input id="pp-t2" name="t2" placeholder="Organized the parts inventory"><label for="pp-d2">What you did and the problem it solved</label><textarea id="pp-d2" name="d2" rows="2"></textarea><label for="pp-r2">The result (use a number if you can)</label><input id="pp-r2" name="r2" placeholder="Found $2,000 in lost stock"></fieldset><fieldset class="pp-proj"><legend>Project 3</legend><label for="pp-t3">Short title</label><input id="pp-t3" name="t3" placeholder="Trained three new coworkers"><label for="pp-d3">What you did and the problem it solved</label><textarea id="pp-d3" name="d3" rows="2"></textarea><label for="pp-r3">The result (use a number if you can)</label><input id="pp-r3" name="r3" placeholder="All three passed training in 2 weeks"></fieldset></div>
<label for="pp-learn">Training, certificates or courses (optional)</label><input id="pp-learn" name="learn" placeholder="Google Data Analytics Certificate (in progress)">
<button class="btn primary" type="submit">Create my Skills Passport</button>
<small>No email required. Nothing you type leaves your device. Leave out your home address and other private details.</small>
</form></details>
<div id="pp-out" aria-live="polite" tabindex="-1"></div>
<details class="prompt"><summary>Stuck on wording? Use this AI prompt</summary><p class="prompt-text">Help me write a one-page skills portfolio. The job I'm aiming for: [job]. Here are three things I've done: 1) [what I did, the problem it solved, the result]. 2) [same]. 3) [same]. For each one, write a short title, two sentences on what I did, and the skills it shows. Use plain words and real numbers where I gave them. Don't invent anything I didn't tell you.</p><button class="copy-btn" type="button">Copy prompt</button></details>
</article>
</div>
{SHOWCASE_BLOCK}
</div></section>

<section class="kids-band" id="kids"><div class="container"><div class="center-head"><span class="eyebrow" style="color:#c9a9ea">For your kids</span><h2>How children will learn</h2><p>Kids growing up now will use AI their whole lives. The goal isn't to keep them away from it. It's to help them think, solve problems and work with people, with AI as a helper. Here are projects to try at home, and how to use AI as their coach.</p></div></div></section>
<section class="eco-section" id="problem"><div class="container">
<div class="center-head"><span class="eyebrow">Learn by doing</span><h2>Teach the problem, not the tools</h2><p style="margin:12px auto 0;max-width:700px">When Elon Musk started his own school, Ad Astra, he used a simple idea: don't start with lessons on screwdrivers and wrenches. Give kids an engine and let them take it apart, and they'll see why the tools matter. His school also grouped kids by ability, not age. You can do both at home.</p></div>
<div class="project-grid">
<article class="project-card"><span class="kicker c-work">Ages 6+ · science</span><h3>Take apart an old gadget</h3><p>An old toaster, keyboard or remote (unplugged, batteries out, adult nearby). Guess what each part does, then look it up.</p><p class="learn"><strong>They learn:</strong> how machines work, using tools safely, asking good questions.</p></article>
<article class="project-card"><span class="kicker c-home">Ages 8+ · math</span><h3>Plan the family's groceries</h3><p>Give them a real budget and a week of meals to plan. Compare prices, add it up, and see if it fits.</p><p class="learn"><strong>They learn:</strong> math, money, trade-offs and planning.</p></article>
<article class="project-card"><span class="kicker c-work">Ages 9+ · technology</span><h3>Build a simple game or website</h3><p>Pick something they love and make a page or game about it with a free beginner tool like Scratch.</p><p class="learn"><strong>They learn:</strong> logic, design, and fixing what breaks.</p></article>
<article class="project-card"><span class="kicker c-home">Ages 10+ · business</span><h3>Run a tiny business</h3><p>A bake sale, pet-sitting or yard work. Set a price, track costs and count the profit.</p><p class="learn"><strong>They learn:</strong> math, people skills and responsibility.</p></article>
<article class="project-card"><span class="kicker c-work">Ages 10+ · research</span><h3>Investigate a real question</h3><p>"Why is our electric bill higher in summer?" Gather clues, test ideas and present what they found to the family.</p><p class="learn"><strong>They learn:</strong> research, reading, and checking whether a source is right.</p></article>
<article class="project-card"><span class="kicker c-home">Any age · life skills</span><h3>Fix something together</h3><p>A wobbly chair, a leaky faucet, a flat bike tire. Watch a how-to video, then do it.</p><p class="learn"><strong>They learn:</strong> patience, following steps, and that they can fix things.</p></article>
<article class="project-card wide"><span class="kicker c-work">Grades K–12 · AI</span><h3>Enter the Presidential AI Challenge</h3><p>A national contest where student teams, with an adult mentor, build an AI project that solves a problem in their community. Registration for 2026 has closed; watch for the next round.</p><p class="learn"><strong>They learn:</strong> AI basics, teamwork and solving real problems. <a href="https://www.ai.gov/initiatives/presidential-challenge" target="_blank" rel="noopener noreferrer" style="color:var(--green);font-weight:700">Challenge website →</a></p></article>
</div>
<div class="tip-row">
<article class="tip-box"><h3>Use AI as the coach, not the answer key</h3><p>Paste this into ChatGPT, Claude or Gemini before your child starts a project, so the AI asks questions instead of doing the work.</p>
<details class="prompt" open><summary>Coach prompt for kids</summary><p class="prompt-text">You are a patient tutor for a [age]-year-old who is working on [project]. Do not give the answer or do the work. Ask one question at a time to help them figure it out. Give a small hint only if they are stuck after two tries. Use simple words, and cheer them on when they get something right.</p><button class="copy-btn" type="button">Copy prompt</button></details>
<p class="safe-note"><strong>Stay safe:</strong> check each AI tool's age rules, and sit with younger kids while they use it.</p></article>
<article class="tip-box"><h3>Learn at their level, not their grade</h3><p>A 9-year-old might read like a 12-year-old and do math like an 8-year-old. That's normal. Let them move ahead where they're strong and slow down where they need it.</p><p>Practice tools like IXL adjust to your child's level automatically, and live classes on Outschool are grouped by interest and ability.</p><h3 style="margin-top:18px">Don't skip the people part</h3><p>Projects are better with others. Co-ops, library programs, sports and group classes give kids the teamwork and friendships that no AI can.</p></article>
</div>
</div></section>

<section class="eco-section" id="help"><div class="container"><div class="center-head"><span class="eyebrow">Where to get help</span><h2>Where to learn: for you and your kids</h2><p style="margin:12px auto 0;max-width:660px">Career skills for you, and practice and live classes for your kids, with the trade-offs people mention most. Free options are listed too.</p></div><div class="partner-grid four"><article class="partner-card"><span class="kicker c-work">For you · career skills</span><h3><a href="https://www.coursera.org" target="_blank" rel="noopener noreferrer">Coursera</a></h3><p>Courses and certificates from Google, IBM and universities, including AI basics. Many courses are free to audit.</p><p class="note">Look for financial aid on paid certificates.</p><a class="go" href="https://www.coursera.org" target="_blank" rel="noopener noreferrer">Visit Coursera →</a></article><article class="partner-card"><span class="kicker c-work">For your kids · live group classes, ages 3–18</span><h3><a href="https://outschool.com" target="_blank" rel="noopener noreferrer">Outschool</a></h3><p>Live small-group classes taught online, on almost any subject. Good for core subjects, interests and time with other kids.</p><p class="note">Parents praise the teachers. Common complaints are about the monthly credit membership, so check the renewal terms before you subscribe.</p><a class="go" href="https://outschool.com" target="_blank" rel="noopener noreferrer">Visit Outschool →</a></article><article class="partner-card"><span class="kicker c-work">For your kids · practice, K–12</span><h3><a href="https://www.ixl.com" target="_blank" rel="noopener noreferrer">IXL</a></h3><p>Skill-by-skill practice in math, reading, science and more. Works alongside any school or homeschool path.</p><p class="note">Best as a supplement, not a full curriculum.</p><a class="go" href="https://www.ixl.com" target="_blank" rel="noopener noreferrer">Visit IXL →</a></article><article class="partner-card free"><span class="kicker c-home">Free options</span><h3>Free places to start</h3><p>Khan Academy for practice, your public library for books and online classes, and your state's free public virtual school if you want full online school.</p><p class="note">Start free, then pay only for what fills a real gap.</p></article></div><p class="partner-foot">We list services we would recommend to a friend. Some links may earn us a commission at no cost to you; any paid link is labeled.</p><p style="text-align:center;margin:18px 0 0;font-size:.82rem">General information, not legal or educational advice. School and school-choice rules vary by state.</p></div></section>
{join("Education", "ed-email")}'''

# ---------- Guides, About, Disclosure (generated) ----------


about_body = '''<section class="page-hero"><div class="container"><span class="pill">OUR MISSION</span><h1>Adapt. Build. <span class="gradient-text">Evolve.</span></h1><p>The future isn't something that happens to us. It's something we build.</p></div></section>
<section class="section"><div class="container article-width">
<h2>Why we exist</h2>
<p>AI is not coming. It is here, and it is changing what it means to work, earn, live and belong.</p>
<p>For the first time in history, machines can do much of the thinking work that people have been paid to do. Jobs that took years to learn can be automated in months. Decisions about our rent, our loans, our health and our hiring are already being made by software we never see.</p>
<p>This is bigger than technology. It is about whether ordinary people still have a place, a purpose and a paycheck in the world that is coming. It is about the future of the human race.</p>
<p>We believe that future is not decided yet. Adapt Build Evolve exists so that working people help decide it, instead of having it decided for them.</p>
<h2>What we believe</h2>
<ol>
<li><strong>Humans come first.</strong> Technology should serve people, not replace their worth. A person is more than the tasks they do for a paycheck.</li>
<li><strong>No one should be left behind.</strong> The AI economy will create winners. We want working families to be among them, not just the people who own the machines.</li>
<li><strong>Surviving comes before thriving.</strong> First we protect our income, our homes and our families. Then we build something new.</li>
<li><strong>Ownership is freedom.</strong> People who own skills, businesses, homes and savings are harder to knock down than people who only own a job.</li>
<li><strong>The human things matter more now.</strong> Care, trust, hands-on skill, judgment and community are what machines cannot replace. We double down on them.</li>
<li><strong>We are stronger together.</strong> No one gets through a revolution alone. We share what works, warn each other about what doesn't, and lift each other up.</li>
<li><strong>Fear is not a plan.</strong> We look at the truth about AI clearly, then we act.</li>
</ol>
<h2>Adapt. Build. Evolve.</h2>
<p>Three words, three stages of getting through what is coming.</p>
<p><strong>Adapt: protect what you have.</strong> See the changes before they hit you. Know which parts of your job are at risk. Build a cash cushion, a backup plan and a list of people you can call. Know your rights when software decides your rent, your loan or your hiring.</p>
<p><strong>Build: create what can't be taken.</strong> Grow skills that need a human. Start a second income. Learn a trade, start a business, or buy one. Put your money where it grows. Own something.</p>
<p><strong>Evolve: become who the future needs.</strong> Keep learning for life. Teach your children to think, create and work alongside machines. Help shape the rules. Bring others with you, because a movement that grows is how people keep their power.</p>
<h2>Who this is for</h2>
<p>This movement is for the people who keep the world running and are rarely asked what they think about its future:</p>
<ul>
<li>Workers who wonder if their job will exist in five years</li>
<li>People who just lost a job, or feel one coming</li>
<li>Parents worried about what their children should learn</li>
<li>People without a degree who are told the door is closing</li>
<li>Anyone who has ever been treated like a number by a system</li>
<li>Anyone ready to stop worrying and start building</li>
</ul>
<p>You don't need to be technical. You don't need money to start. You just need to decide you will not be left behind.</p>
<h2>What we will do together</h2>
<p>We focus on the five things every family needs to get through the AI era.</p>
<ul>
<li><a href="work.html"><strong>Work</strong></a>: Will I still have a way to earn? Spot the risk early, move toward work that needs a person, build a second paycheck.</li>
<li><a href="housing.html"><strong>Housing</strong></a>: Will I keep a roof over my head? Know our rights, build a safety net, make our homes work for us.</li>
<li><a href="finance.html"><strong>Money</strong></a>: Will my money last and grow? Build a cushion, avoid AI scams, invest for the long run, own assets.</li>
<li><a href="education.html"><strong>Learning</strong></a>: Will my family have the skills that matter? Learn for life, prove skills over degrees, raise children ready for what's next.</li>
<li><a href="healthcare.html"><strong>Health</strong></a>: Will we be cared for by people, not just systems? Know how AI is used in our care, speak up, protect the human side of health.</li>
</ul>
<p>And we do it as a community: sharing leads, swapping skills, meeting in person and online, and showing each other what is working.</p>
<h2>Why I started this</h2>
<p>I spent more than 30 years in hospitals, in radiology, CT and the cardiac cath lab. I watched technology change the work over and over. Machines got smarter, and every time, some people adapted and some people got left behind. The difference was rarely talent. It was whether someone saw it coming and had help.</p>
<p>When AI arrived, I saw the same wave coming, only bigger and faster, and headed for almost every kind of job. So I did what I want everyone to be able to do. I adapted. I learned. I built a business, a newsletter and a website, on my own terms.</p>
<p>I'm not a tech billionaire. I'm a working person who decided not to wait. Adapt Build Evolve is how I share the path, so you don't have to walk it alone.</p>
<p><em>— Alaina Tillage, founder</em></p>
<h2>Our promise, and your invitation</h2>
<p>We promise to tell the truth about AI, even when it's uncomfortable. We promise to point you to real help, not hype. We promise to put people before profit, and to tell you plainly when we earn money from a recommendation. Read the full <a href="disclosure.html">disclosure</a>.</p>
<p>The future isn't something that happens to us. It's something we build.</p>
<p><strong>Join us. Adapt. Build. Evolve.</strong></p>
</div></section>
''' + join()

disclosure_body = '''<section class="page-hero"><div class="container"><span class="pill">TRANSPARENCY &amp; PRIVACY</span><h1>Disclosure and <span class="gradient-text">privacy</span></h1><p>How this site earns money, what it collects and what it doesn't. Last updated November 2026.</p></div></section>
<section class="section"><div class="container article-width">
<h2>Paid links</h2>
<p>Some links on this site are paid (affiliate) links. They're marked "Paid link" next to the link. If you click one and sign up or buy, The AI Revolution may earn a commission. It doesn't change the price you pay.</p>
<p>A commission never decides whether something is listed. Each partner section also includes free or low-cost options, and some services are listed without any paid link at all.</p>
<h2>My own products</h2>
<p>The guides sold on Gumroad are my own products. Buying one supports the site directly.</p>
<h2>Newsletter signups</h2>
<p>Email forms on this site send you to Substack to finish subscribing to AI Revolution Update, my free newsletter about AI and everyday life. Your email is handled by Substack under <a href="https://substack.com/privacy" target="_blank" rel="noopener noreferrer">its privacy policy</a>. This site doesn't store your email address.</p>
<h2>Calculators and quizzes</h2>
<p>The AI Readiness Score, the calculators, the learning path finder and the healthcare task check run entirely in your browser. You don't need to give an email or sign up to use them, there's nothing to buy at the end, and your answers aren't sent to or saved by this site.</p>
<h2>Visitor statistics</h2>
<p>This site may use Cloudflare Web Analytics to count visits and see which pages are useful. It doesn't use cookies or track you across other sites. Affiliate networks may also count clicks on paid links, and the sites you visit through any outside link use their own cookies and privacy policies.</p>
<h2>Accounts and payments</h2>
<p>This site has no accounts, no comments and no shopping cart. Purchases happen on the seller's own site.</p>
<h2>General information only</h2>
<p>Content on this site is general educational information, not medical, financial, legal or career advice. Programs, prices and offers change, so confirm details with the provider before you sign up or buy.</p>
</div></section>'''

# ---------- Guides (futurist toolkit) ----------
def tcard(name, what, href, cta, tag=""):
    t = f'<span class="tk-tag">{tag}</span>' if tag else ''
    return f'<a class="tk-tool" href="{href}">{t}<strong>{name}</strong><span>{what}</span><em>{cta} →</em></a>'

TK_PILLARS = [
 ("Work", [tcard("Job task check", "Which of your tasks AI is taking on, which it helps with, and which stay human.", "work.html#job-check", "Check my job")]),
 ("Healthcare", [tcard("Healthcare task check", "See which parts of your health care job AI is changing.", "healthcare.html#task-check", "Check my tasks")]),
 ("Money", [tcard("Paycheck cushion", "How long your savings would cover your bills if your pay stopped.", "finance.html#fin-calc", "Find my cushion"), tcard("Investment growth", "What a small weekly amount could grow into.", "finance.html#grow-calc", "Try it")]),
 ("Housing", [tcard("Housing safety net", "Your housing cost share, and what happens if your pay drops.", "housing.html#housing-calc", "Know my number")]),
 ("Learning", [tcard("What should I learn first?", "Four questions, one personal starting plan.", "education.html#learn-first", "Get my plan"), tcard("Skills Passport", "A one-page summary of your skills to print or save as a PDF.", "education.html#passport", "Build my passport")]),
 ("AI basics", [tcard("Real or AI scam? quiz", "Six real-life situations. Could you spot the AI scam?", "understanding-ai.html#scam-quiz", "Take the quiz"), tcard("Try AI in 2 minutes", "Your first AI conversation, with a prompt to copy.", "understanding-ai.html#try-it", "Try it")]),
]
TOOL_COUNT = 1 + sum(len(t) for _, t in TK_PILLARS)
tk_pillar_html = "".join(f'<div class="tk-col"><p class="tk-col-h">{n}</p>{"".join(tools)}</div>' for n,tools in TK_PILLARS)

PROMPT_LIB = [
 ("Work", 4, "Draft a hard email · Meeting notes into action items · Weekly update in 5 minutes · Messy process into a checklist", "work.html#ai-at-work"),
 ("Healthcare", 4, "Study for a certification · Explain a new policy simply · Write a patient handout · Tip sheet for your team", "healthcare.html#ai-at-work"),
 ("Housing", 4, "Dispute a screening report · Push back on rent · Explain my lease · Remote-move math", "housing.html#ai-at-work"),
 ("Money", 3, "Find forgotten subscriptions · Build a bill calendar · 30-day cushion plan", "finance.html#tools"),
 ("Learning", 3, "Personal AI tutor · Help with Skills Passport wording · Coach prompt for kids", "education.html#tutor-prompt"),
]
PROMPT_COUNT = sum(n for _, n, _, _ in PROMPT_LIB)
prompt_lib_html = "".join(f'<a class="pl-card" href="{u}"><span class="pl-k">{k}</span><span class="pl-n">{n} prompts</span><span class="pl-x">{x.split(" · ")[0]} + {n-1} more</span><em>Open →</em></a>' for k,n,x,u in PROMPT_LIB)

guides_body = f'''<section class="pillar-hero"><div class="container pillar-hero-grid"><div>
<span class="eyebrow" style="color:var(--purple)">Free tools and guides</span>
<h1>Every free tool, <em style="font-style:normal;color:var(--purple)">in one place.</em></h1>
<p class="lead">Quick tools, copy-ready AI prompts and career maps. No email, no sign-up, and your answers stay on your device.</p>
</div><a class="stat-card start-card" href="index.html#score"><span class="kicker c-work">Start here · 2 minutes</span><p class="num" style="color:var(--purple)">AI Readiness Score</p><p>Eight quick questions across work, housing, money, learning and health care. See where you're strong and where to start.</p><span class="go">Take the score →</span></a></div></section>

<section class="eco-section" id="tools"><div class="container">
<div class="center-head"><span class="eyebrow">Tools</span><h2>Check where you stand</h2><p style="margin:12px auto 0;max-width:600px">Each one takes a few minutes. Nothing you enter leaves your device.</p></div>
<div class="tk-grid">{tk_pillar_html}</div>
</div></section>

<section class="eco-section soft" id="prompts"><div class="container">
<div class="center-head"><span class="eyebrow">AI prompt library</span><h2>{PROMPT_COUNT} prompts you can copy and use today</h2><p style="margin:12px auto 0;max-width:660px">Paste one into ChatGPT, Claude or Gemini, fill in the blanks, and let AI handle the busywork. Never paste private customer, patient or account information.</p></div>
<div class="pl-grid">{prompt_lib_html}</div>
</div></section>

<section class="eco-section" id="careers"><div class="container">
<div class="center-head"><span class="eyebrow">Career maps</span><h2>See your next move</h2></div>
<div class="cm-grid">
<a class="cm-card" href="jobs.html"><span class="cm-ic" aria-hidden="true">✦</span><strong>Find a job</strong><span>The best free job boards, jobs that don't need a degree, and a first-week checklist.</span><em>Open →</em></a>
<a class="cm-card" href="healthcare.html#ladders"><span class="cm-ic" aria-hidden="true">↗</span><strong>Healthcare career ladders</strong><span>Bedside care, imaging and health information, with the pay at each step.</span><em>Open →</em></a>
<a class="cm-card" href="work.html#hands-on"><span class="cm-ic" aria-hidden="true">⚒</span><strong>Careers that need a person on site</strong><span>Electricians, HVAC, plumbers, wind techs and more, with pay and outlook.</span><em>Open →</em></a>
<a class="cm-card" href="work.html#skills-first"><span class="cm-ic" aria-hidden="true">◇</span><strong>Where hiring is opening up</strong><span>Employers and governments hiring for skills instead of degrees.</span><em>Open →</em></a>
<a class="cm-card" href="work.html#second-paycheck"><span class="cm-ic" aria-hidden="true">＋</span><strong>Build a second paycheck</strong><span>Four realistic ways to earn on the side, with AI doing the admin.</span><em>Open →</em></a>
</div>
</div></section>

<section class="eco-section soft"><div class="container">
<a class="mk-teaser lt" href="marketplace.html"><div><span class="eyebrow">Marketplace</span><h2>Robots, AI gadgets, and smart home and office gear</h2><p>The gadgets of the AI revolution, rated from "ready now" to "moonshot," with an honest note on each.</p><em>Explore the Marketplace →</em></div><span class="mk-orb" aria-hidden="true"></span></a>
</div></section>

<section class="eco-section" id="playbooks"><div class="container">
<div class="center-head"><span class="eyebrow">Playbooks</span><h2>Want to go deeper?</h2><p style="margin:12px auto 0;max-width:640px">Step-by-step guides I wrote, sold on Gumroad. Everything above stays free.</p></div>
<div class="product-row">{PRODUCTS}</div>
<p style="text-align:center;margin:26px 0 0;font-size:.85rem">Tools and prompts are general information, not medical, financial, legal or career advice.</p>
</div></section>'''

# ---------- Marketplace ----------
def svg(inner):
    return f'<svg viewBox="0 0 120 90" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'

ART = {
 "humanoid": svg('<rect x="47" y="8" width="26" height="20" rx="7"/><circle cx="55" cy="18" r="2.2" fill="currentColor"/><circle cx="65" cy="18" r="2.2" fill="currentColor"/><path d="M60 28v4"/><rect x="44" y="32" width="32" height="30" rx="8"/><path d="M44 38l-12 16M76 38l12 16"/><path d="M52 62v20M68 62v20"/><path d="M48 82h8M64 82h8"/>'),
 "vacuum": svg('<ellipse cx="46" cy="64" rx="30" ry="12"/><path d="M16 64v-6c0-6 13-11 30-11s30 5 30 11v6"/><circle cx="46" cy="52" r="3"/><path d="M62 50l14-22 16 8"/><path d="M92 36l6-4M92 36l5 6"/><path d="M96 70c3-4 9-4 12 0l-4 6h-6z"/>'),
 "dog": svg('<rect x="30" y="34" width="50" height="20" rx="8"/><path d="M80 38l12-10h10v14l-10 4"/><circle cx="98" cy="35" r="1.8" fill="currentColor"/><path d="M36 54l-4 14 6 10M50 54v24M62 54v24M74 54l4 14-6 10"/><path d="M30 40l-10-6"/>'),
 "mower": svg('<path d="M24 58l10-22h44l14 22z"/><circle cx="36" cy="64" r="8"/><circle cx="82" cy="64" r="8"/><path d="M48 36l6-10h14"/><circle cx="72" cy="26" r="3"/><path d="M10 80l4-8 4 8 4-8 4 8M94 80l4-8 4 8 4-8 4 8"/>'),
 "glasses": svg('<rect x="14" y="32" width="38" height="28" rx="12"/><rect x="68" y="32" width="38" height="28" rx="12"/><path d="M52 42c4-4 12-4 16 0"/><path d="M14 40H6M106 40h8"/><circle cx="22" cy="28" r="3" fill="currentColor"/><path d="M84 18l4-6M92 20l6-4M96 26h6"/>'),
 "display": svg('<rect x="14" y="32" width="38" height="28" rx="12"/><rect x="68" y="32" width="38" height="28" rx="12"/><path d="M52 42c4-4 12-4 16 0"/><path d="M14 40H6M106 40h8"/><path d="M76 42h20M76 48h14M76 54h18"/>'),
 "pin": svg('<rect x="44" y="18" width="24" height="54" rx="12"/><circle cx="56" cy="38" r="5"/><path d="M80 34c4 4 4 12 0 16M88 28c8 8 8 20 0 28M32 34c-4 4-4 12 0 16M24 28c-8 8-8 20 0 28"/>'),
 "ikea": svg('<path d="M30 52c-8-5-10-14-10-20a16 16 0 0 1 32 0c0 6-2 15-10 20z"/><path d="M30 52h12v8H30zM32 66h8"/><rect x="72" y="34" width="30" height="30" rx="7"/><circle cx="87" cy="44" r="4"/><circle cx="87" cy="56" r="4"/><path d="M58 30c4-4 8-4 10 0M54 24c7-7 15-7 18 0"/>'),
 "hue": svg('<path d="M40 56c-10-6-13-17-13-24a20 20 0 0 1 40 0c0 7-3 18-13 24z"/><path d="M40 56h14v9H40zM42 71h10"/><path d="M84 30l12 10-12 10V22l12 10-12 10"/>'),
 "lutron": svg('<rect x="18" y="16" width="36" height="58" rx="5"/><rect x="28" y="26" width="16" height="38" rx="3"/><path d="M36 34v8"/><rect x="74" y="28" width="22" height="40" rx="6"/><circle cx="85" cy="38" r="3"/><circle cx="85" cy="48" r="3"/><circle cx="85" cy="58" r="3"/><path d="M60 40c3-3 6-3 8 0"/>'),
 "card": svg('<rect x="28" y="16" width="64" height="58" rx="8"/><path d="M40 46v-2M46 50v-10M52 54v-18M58 50v-10M64 52v-14M70 48v-6M76 46v-2"/><circle cx="60" cy="24" r="2" fill="currentColor"/>'),
 "chat": svg('<path d="M14 22h52a8 8 0 0 1 8 8v20a8 8 0 0 1-8 8H36l-12 10v-10h-10a8 8 0 0 1-8-8V30a8 8 0 0 1 8-8z"/><path d="M60 40h40a8 8 0 0 1 8 8v14a8 8 0 0 1-8 8h-4v8l-10-8H60"/><path d="M24 36h28M24 44h18"/><path d="M96 14l2 5 5 2-5 2-2 5-2-5-5-2 5-2z" fill="currentColor"/>'),
}

def mk(shelf, level, art, name, price, what, note, url, cta="See it"):
    lv = {"now":"Ready now","early":"Early adopter","moon":"Moonshot"}[level]
    shelf, _, sub = shelf.partition(":")
    return (f'<article class="mk-card" data-shelf="{shelf}" data-sub="{sub}">'
            f'<div class="mk-body"><div class="mk-meta"><span class="mk-lv {level}">{lv}</span><span class="mk-price">{price}</span></div><h3>{name}</h3><p>{what}</p><p class="mk-note">{note}</p>'
            f'<a class="mk-go" href="{url}" target="_blank" rel="noopener noreferrer">{cta} ↗</a></div></article>')

MK_ITEMS = [
 mk("robots","moon","humanoid","1X NEO home robot","$20,000 or $499/mo","A 5-foot-6 humanoid built for chores like folding laundry, tidying shelves and fetching things. The first US deliveries are planned for 2026.","Early units can be remotely guided by human operators who see inside your home, so weigh the privacy trade-off.","https://www.1x.tech"),
 mk("robots","early","vacuum","Roborock Saros Z70","List $2,599; often on sale","A robot vacuum and mop with a folding arm that picks up socks and small items before it cleans.","Reviewers say the arm works about half the time. Great cleaner, first-generation arm.","https://us.roborock.com"),
 mk("robots","moon","dog","Unitree Go2 robot dog","From about $1,600 + shipping","A walking, climbing robot dog with obstacle avoidance and app control. Pure future, today.","More conversation piece than helper. Shipping from the maker adds hundreds of dollars.","https://www.unitree.com/go2"),
 mk("robots","now","mower","Segway Navimow i105N","About $680","A robot lawn mower for small yards that maps your lawn with GPS and cameras. No buried wire.","Best for smaller lawns; bigger or steeper yards need a pricier model.","https://navimow.segway.com"),
 mk("gadgets","now","glasses","Ray-Ban Meta glasses (Gen 2)","About $379","Glasses with a camera, open-ear speakers and Meta AI. Ask about what you're looking at, translate, take calls, capture video.","A camera on your face: be respectful where people expect privacy.","https://www.meta.com/ai-glasses/"),
 mk("gadgets","early","display","Even Realities G2","About $599","Display glasses that show text, directions and notes in the lens. No camera, two-day battery.","A small monochrome display, and its assistant is simpler than Meta's.","https://www.evenrealities.com"),
 mk("gadgets","now","pin","Plaud NotePin S","$179","A wearable recorder about the weight of a AA battery. It records, transcribes and summarizes conversations, with 300 free transcription minutes a month.","Always get permission before recording. Some states require everyone's consent.","https://www.plaud.ai/collections/plaud-notepin-s"),
 mk("home:nowifi","now","ikea","IKEA KAJPLATS bulbs + BILRESA remote","Low cost","IKEA's new smart bulbs and two-button remote. Pair them and turn a whole set of lights on or off with one click.","Works with no app, no hub and no Wi-Fi. The new bulbs also work with older IKEA remotes.","https://www.ikea.com/us/en/search/?q=kajplats"),
 mk("home:nowifi","now","hue","Philips Hue Bluetooth bulbs","Check current price","Hue bulbs that connect straight to your phone by Bluetooth, or pair directly with a Hue dimmer switch.","Up to 10 lights without the Hue Bridge. Add the bridge later for away-from-home control.","https://www.philips-hue.com/en-us/explore-hue/faq/controls/how-to-connect-philips-hue-without-a-bridge"),
 mk("home:nowifi","now","lutron","Lutron Caséta dimmer + Pico remote","About $75","A wall dimmer plus a battery remote you can stick anywhere as a second switch. No neutral wire needed.","Never uses your Wi-Fi. The Pico has a 10-year battery and controls up to 10 Caséta devices without a hub.","https://www.casetawireless.com"),
 mk("home:home","now","hub","Amazon Echo Hub","About $180","Smart hub · An 8-inch wall-mount touchscreen that controls your lights, locks, cameras and thermostat in one place, with Alexa built in.","Best if your home already uses Alexa or Ring.","https://www.amazon.com/s?k=Amazon+Echo+Hub"),
 mk("home:home","now","hub","Samsung SmartThings Station","Check current price","Smart hub · A small hub with no screen that connects devices from many brands, so you don't need a separate bridge for each one. Doubles as a phone charger.","You control everything from the SmartThings app. Works with Alexa and Google too.","https://www.samsung.com/us/smartthings/"),
 mk("home:home","now","hub","Apple HomePod mini","About $99","Smart hub · A small speaker that also runs your Apple Home devices, so you can control them with Siri, even when you're away.","Best for homes where everyone has an iPhone.","https://www.apple.com/homepod-mini/"),
 mk("home:home","now","hue","Philips Hue White and Color starter kit","Check current price","Smart lighting · Color bulbs plus the Hue Bridge. Schedules, scenes, away-from-home control and the widest choice of lamps and light strips.","Pricier than other brands, but the most reliable whole-home lighting system.","https://www.philips-hue.com/en-us"),
 mk("home:home","now","hue","Nanoleaf Essentials bulbs","Check current price","Smart lighting · Color bulbs that work without a bridge and connect to Apple Home, Google Home or Alexa through Matter.","A lower-cost way to start; the app is less polished than Hue's.","https://nanoleaf.me/en-US/"),
 mk("home:home","now","hue","LIFX color bulbs","About $30 a bulb","Smart lighting · Bright color bulbs that connect straight to your Wi-Fi. No hub needed.","Uses Wi-Fi, so each bulb adds a device to your network.","https://www.lifx.com"),
 mk("home:home","now","speaker","Amazon Echo smart speaker","Check current price","Smart speaker · A speaker you talk to for timers, reminders, music and turning compatible lights and plugs on and off.","It's always listening for its wake word. Use the mute button when you want privacy.","https://www.amazon.com/echo"),
 mk("home:home","now","thermo","Google Nest thermostat","Check current price","Thermostat · Set heating and cooling from your phone, on a schedule, or let it learn your routine.","Check that it works with your heating system and wiring before you buy.","https://store.google.com/category/connected_home?hl=en-US"),
 mk("home:office","now","card","Plaud Note Pro","$189","A card-thin AI recorder for meetings and calls that turns them into transcripts and summaries.","The free plan has monthly limits; heavy users pay for a yearly plan.","https://www.plaud.ai"),
 mk("home:office","now","chat","Free AI assistants","Free to start","ChatGPT, Claude, Gemini and Microsoft Copilot all have free versions for writing, planning and research.","Start with our copy-ready work prompts. Follow your employer's AI rules.","guides.html#prompts","Get the prompts"),
 mk("home:office","now","card","Canva","Free plan","Make flyers, slides and social posts, with AI features that help with design and wording.","The free plan covers most needs; some AI features need a paid plan.","https://www.canva.com"),
]

MK_SHOP = [x for x in MK_ITEMS if 'data-shelf="home"' not in x]
MK_HO = [x for x in MK_ITEMS if 'data-shelf="home"' in x]
SHELVES = [("tech","Robots and gadgets"),("ho","Home and office")]
mk_chips = "".join(f'<button type="button" class="mk-chip{" on" if k=="tech" else ""}" data-f="{k}" aria-pressed="{"true" if k=="tech" else "false"}">{l}</button>' for k,l in SHELVES)

hero_tiles = "".join(f'<div class="mk-tile s-{s}">{ART[a]}</div>' for s,a in [("robots","humanoid"),("gadgets","glasses"),("nowifi","ikea"),("robots","dog")])

market_body = f'''<section class="pillar-hero mk-hero-light"><div class="container"><div>
<span class="eyebrow" style="color:var(--purple)">The AI Revolution Marketplace</span>
<h1>The future, <em style="font-style:normal;color:var(--purple)">on sale now.</em></h1>
<p class="big-q" style="border-color:var(--purple)">What AI gadgets are actually worth buying?</p>
<p class="updated">Updated November 2026</p>
<p class="lead">Home robots, AI glasses, smart home and office gear, and lights that work with no Wi-Fi at all. Every pick is rated from "ready now" to "moonshot," with an honest note on each.</p>
<div class="mk-legend"><span><i class="mk-lv now">Ready now</i> works well today</span><span><i class="mk-lv early">Early adopter</i> impressive, still rough</span><span><i class="mk-lv moon">Moonshot</i> pure future, high price</span></div>
</div></div></section>

<section class="eco-section" id="shop"><div class="container">
<div class="center-head"><span class="eyebrow">Shop the Marketplace</span><h2>Picks from the AI revolution</h2></div>
<div class="mk-chips" role="group" aria-label="Marketplace sections">{mk_chips}</div>
<div class="mk-grid" id="mk-grid">{"".join(MK_SHOP)}</div>
<div class="ho-area" id="home-office" hidden>
<p class="ho-intro">Click a card to see the products.</p>
<div class="ho-grid">
<a class="pillar-card ho-pick" href="#shop" data-pick="home"><span class="ho-img"><img src="images/home.webp" alt="Comfortable living room with a smart speaker" loading="lazy"></span><div><span class="kicker c-home">AI My Home</span><h3>A smarter home</h3><p>Smart hubs, lighting, speakers and thermostats that make home life easier.</p><span class="go c-home">See home picks →</span></div></a>
<a class="pillar-card ho-pick" href="#shop" data-pick="office"><span class="ho-img"><img src="images/office.webp" alt="Bright workspace with a laptop" loading="lazy"></span><div><span class="kicker c-home">AI My Office</span><h3>Work smarter, not harder</h3><p>AI note-takers and tools for writing, planning and design.</p><span class="go c-home">See office picks →</span></div></a>
<a class="pillar-card ho-pick" href="#shop" data-pick="nowifi"><span class="ho-img"><img src="images/nowifi.webp" alt="Cozy living room with two lamps lit and a small white battery remote on a side table" loading="lazy"></span><div><span class="kicker c-home">No Wi-Fi smart home</span><h3>One click, every light</h3><p>Bulbs and battery remotes that talk to each other. No app, no hub, no Wi-Fi.</p><span class="go c-home">See no Wi-Fi picks →</span></div></a>
</div>
<div class="ho-panel" id="ho-panel" hidden><p class="ho-panel-head" id="ho-head" tabindex="-1"></p><div class="mk-grid">{"".join(MK_HO)}</div></div>
</div>

<p class="mk-fine">Prices are approximate as of November 2026 and change often, especially on sale days. Check the current price before you buy. Links go to each maker's site.</p>
</div></section>

<section class="steps-band" id="no-wifi"><div class="container">
<div class="center-head"><span class="eyebrow">No Wi-Fi smart home</span><h2>One click, every light</h2><p style="margin:12px auto 0;max-width:640px">You don't need an app, a hub or Wi-Fi for a smart home. Bulbs and battery remotes can talk to each other directly.</p></div>
<div class="three four">
<article class="step-card"><span class="n">01</span><h3>Pick one system</h3><p>IKEA, Philips Hue or Lutron Caséta. Stay with one brand to start.</p></article>
<article class="step-card"><span class="n">02</span><h3>Pair the remote</h3><p>Follow the pairing steps in the box. It usually takes a minute per bulb or switch.</p></article>
<article class="step-card"><span class="n">03</span><h3>Put it where you need it</h3><p>Battery remotes mount anywhere: by the bed, the couch or the door.</p></article>
<article class="step-card"><span class="n">04</span><h3>Add an app later, if ever</h3><p>A hub adds schedules and away-from-home control. It's optional.</p></article>
</div></div></section>

<section class="eco-section soft" id="before-you-buy"><div class="container">
<div class="center-head"><span class="eyebrow">Before you buy</span><h2>Five questions to ask about any AI gadget</h2></div>
<div class="tip-row"><article class="tip-box"><ul class="scam-list">
<li><strong>Does it have a camera or microphone?</strong> Know who can see and hear what it records, and where that goes.</li>
<li><strong>Is there a subscription?</strong> Many AI gadgets need a monthly plan for the smart features.</li>
<li><strong>Is it first-generation?</strong> First versions are exciting and rough. Waiting a year often means better and cheaper.</li>
</ul></article><article class="tip-box"><ul class="scam-list">
<li><strong>Does it work with what you have?</strong> Look for the Matter logo if you want it to work across Apple, Google, Amazon and Samsung.</li>
<li><strong>What's the return window?</strong> Buy from a store with an easy return policy, and test it in the first week.</li>
</ul><p class="safe-note" style="margin-top:14px">Recording people? Always ask first. Some states require everyone's consent.</p></article></div>
<p class="partner-foot">We list products we would recommend to a friend, with honest notes. Some links may earn us a commission in the future at no cost to you; any paid link will be labeled.</p>
</div></section>'''


# ---------- Understanding AI ----------
import json as _json
FAQ = [
 ("Will AI take my job?", "AI is taking over tasks faster than whole jobs. The World Economic Forum expects 170 million new jobs and 92 million lost by 2030, so the bigger risk is standing still. Check which of your tasks are changing and plan your next skill.", "work.html#job-check", "Check your job"),
 ("Is ChatGPT safe to use?", "For everyday tasks like drafting emails or explaining a topic, it's generally safe if you're careful. Never paste private information such as passwords, account numbers or patient and customer details, and double-check facts, because AI can sound confident and still be wrong. Follow your employer's rules at work.", "guides.html#prompts", "Try safe, copy-ready prompts"),
 ("What is an AI agent?", "An AI agent is AI that carries out a chain of steps on its own, like comparing prices, filling in a form and sending a confirmation, instead of answering one question at a time. Agents are the next big shift at work and at home.", "https://airevolutionupdate.substack.com/p/part-4-what-are-ai-agents-and-what", "Read Part 4 of the beginner series"),
 ("Which AI assistant should I use?", "ChatGPT, Claude, Gemini and Microsoft Copilot all have free versions and handle everyday tasks well. Pick one, use it for a week on real tasks, and switch only if it doesn't fit.", "https://airevolutionupdate.substack.com/p/who-are-the-big-ai-players-and-which", "Compare the big AI players"),
 ("Do I still need a degree to get a good job?", "Less than before. Governors in more than 30 states have acted to remove degree requirements from state jobs, and federal hiring is shifting toward tests of real skills. Apprenticeships and certificates are real paths in.", "work.html#skills-first", "See where hiring is opening up"),
 ("How is AI changing health care jobs?", "AI is taking over paperwork like notes, coding and prior authorizations, and imaging is where clinical AI is most established. Hands-on care keeps growing, so the safest moves combine patient care or clinical skill with judgment.", "healthcare.html", "See healthcare career ladders"),
 ("How do I spot an AI scam?", "Scammers now use AI to clone voices, fake videos and write convincing messages. Be suspicious of any urgent request for money or codes, even from a familiar voice, and confirm by calling back on a number you already know.", "finance.html#tools", "See the AI scam warning signs"),
]
faq_html = "".join(f'<details class="faq"><summary>{q}</summary><div><p>{a}</p><a href="{u}"{" target=\'_blank\' rel=\'noopener noreferrer\'" if u.startswith("http") else ""}>{c} →</a></div></details>' for q,a,u,c in FAQ)
faq_ld = '<script type="application/ld+json">' + _json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a,_,_ in FAQ]}) + '</script>'

GLOSSARY = [
 ("Artificial intelligence (AI)", "Computer systems that do things that normally take human thinking, like understanding language, spotting patterns or making predictions."),
 ("Algorithm", "A set of step-by-step rules a computer follows. Apps use them to decide what to show you, from search results to rent prices."),
 ("Machine learning", "A way of building AI where the computer learns patterns from lots of examples instead of being given every rule."),
 ("AI model", "The trained \"brain\" behind an AI tool. ChatGPT, Claude and Gemini each run on their own models."),
 ("Large language model (LLM)", "An AI model trained on huge amounts of text so it can read, write and answer questions in everyday language."),
 ("Generative AI", "AI that creates something new: text, images, music, video or code."),
 ("Chatbot", "A program you talk to by typing or speaking. Today's AI chatbots can hold a real back-and-forth conversation."),
 ("AI assistant", "A chatbot built to help with tasks, such as drafting, planning, summarizing or answering questions."),
 ("Prompt", "What you type or say to an AI tool. Clear prompts with context get much better answers."),
 ("AI agent", "AI that carries out a chain of steps on its own, not just one answer at a time."),
 ("Hallucination", "When AI states something false with full confidence. It's why you always check important facts."),
 ("Training data", "The examples an AI model learned from. Gaps or slants in the data show up in the answers."),
 ("Bias", "When an AI system treats some people or groups unfairly, often because of its training data."),
 ("Multimodal", "AI that works with more than one kind of input, like text, photos, voice and video together."),
 ("Computer vision", "AI that understands images and video. It's how robot vacuums dodge socks and how scans get flagged."),
 ("Speech recognition", "AI that turns spoken words into text, used in voice assistants and medical transcription."),
 ("Deepfake", "A fake video, photo or voice made with AI to look or sound like a real person."),
 ("Automation", "Using technology to do a task with little or no human effort. AI makes far more tasks automatable."),
 ("On-device AI", "AI that runs on your phone or gadget instead of in the cloud, which can be faster and more private."),
 ("Humanoid robot", "A robot shaped roughly like a person, with arms and legs, built to work in spaces designed for people."),
]
import re as _re
def _slug(t): return "what-is-" + _re.sub(r"[^a-z0-9]+", "-", _re.sub(r"\s*\(.*?\)", "", t).lower()).strip("-")
glossary_html = "".join(f'<div class="gl-item" id="{_slug(t)}"><dt>{t}</dt><dd>{d}</dd><button class="gl-share" type="button" data-id="{_slug(t)}" aria-label="Copy a link to {t}">Share this word</button></div>' for t,d in GLOSSARY)

PILLAR_LINKS = [
 ("work.html", "Work", "Will AI change my job?", "Check your job, use AI at work and find where hiring is opening up."),
 ("healthcare.html", "Healthcare Work", "What does AI mean for health care jobs?", "Task check, career ladders and AI prompts for people in health care."),
 ("housing.html", "Housing", "Is AI setting my rent?", "Know your rights, build a safety net and put AI on your side."),
 ("finance.html", "Money", "How do I protect my money?", "A paycheck cushion, AI scam warnings and investing basics."),
 ("education.html", "Education", "What should I learn next?", "Find your next skill, an AI tutor and a Skills Passport."),
]
pillar_links_html = "".join(f'<a class="pl-link" href="{u}"><span class="kicker c-work">{k}</span><h3>{q}</h3><p>{d}</p><span class="go">Go to {k} →</span></a>' for u,k,q,d in PILLAR_LINKS)

TRY_PROMPT = "I'm new to AI. My job is [your job] and in my free time I [one thing you do]. In five short, simple sentences, tell me how you could help me this week. Then ask me one question to find out what I need most."
try_html = f'''<section class="eco-section" id="try-it"><div class="container"><div class="try-box">
<div><span class="eyebrow">Try it in 2 minutes</span><h2>Have your first AI conversation</h2>
<ol class="try-steps"><li><strong>Open a free AI assistant.</strong> Any of these works. All have a free version.</li><li><strong>Copy this prompt</strong>, fill in the brackets and paste it in.</li><li><strong>Answer its question</strong> and keep going. Ask it to explain anything that doesn't make sense.</li></ol>
<div class="try-apps"><a href="https://chatgpt.com" target="_blank" rel="noopener noreferrer">ChatGPT ↗</a><a href="https://claude.ai" target="_blank" rel="noopener noreferrer">Claude ↗</a><a href="https://gemini.google.com" target="_blank" rel="noopener noreferrer">Gemini ↗</a><a href="https://copilot.microsoft.com" target="_blank" rel="noopener noreferrer">Copilot ↗</a></div></div>
<div class="try-prompt"><p class="prompt-text">{TRY_PROMPT}</p><button class="copy-btn" type="button">Copy prompt</button>
<p class="try-note"><strong>Two rules from day one:</strong> don't paste in passwords, account numbers or private health details, and double-check any fact that matters. AI can sound sure and still be wrong.</p></div>
</div></div></section>'''

quiz_html = '''<section class="eco-section soft" id="scam-quiz"><div class="container">
<div class="center-head"><span class="eyebrow">Real or AI scam?</span><h2>Could you spot an AI scam?</h2><p style="margin:12px auto 0;max-width:640px">AI can copy a voice, fake a video and write a perfect email. Six quick situations. Pick an answer to see the tip.</p></div>
<div class="quiz" id="quiz"></div>
<p class="quiz-score" id="quizScore" role="status" aria-live="polite"></p>
</div></section>'''


NOW = [
 ("Health care", "Medicare is testing AI for prior authorizations", "Since January 2026, AI-assisted review has been part of prior authorization for certain services in six states. Critics in Congress worry it could delay care.", "healthcare.html", "https://samacare.com/resources/wiser-ai-and-patient-access-what-cmss-new-model-could-mean-for-care----and-why-patient-advocates-are-worried"),
 ("Robots", "Home humanoids are in production", "1X has started building its NEO home robot at a factory in Hayward, California, with first deliveries to private customers planned by the end of 2026.", "marketplace.html", "https://heise.de/-11287205"),
 ("Smart home", "IKEA rebuilt its smart home on Matter", "IKEA released 21 new devices, including bulbs and remotes, that work across Apple, Google, Amazon and Samsung, and even without its hub.", "marketplace.html#no-wifi", "https://www.matteralpha.com/news/ikea-launches-21-new-smart-home-devices-with-native-matter-support"),
 ("Hiring", "Federal jobs move to skills tests", "The federal personnel office published its 2026 plan to move hiring toward hands-on skills assessments instead of self-ratings and degrees.", "work.html#skills-first", "https://www.opm.gov/about-us/reports-publications/agency-reports/chance-to-compete-act-of-2024-governmentwide-implementation-plan-for-transition-to-technical-assessments-report-to-congress.pdf"),
]
now_html = "".join(f'<article class="now-card"><span class="kicker c-work">{k}</span><h3>{t}</h3><p>{d}</p><div class="now-links"><a href="{u}">What it means for you →</a><a class="src" href="{s}" target="_blank" rel="noopener noreferrer">Source ↗</a></div></article>' for k,t,d,u,s in NOW)

understanding_body = f'''<section class="pillar-hero"><div class="container pillar-hero-grid"><div>
<span class="eyebrow" style="color:var(--purple)">Understanding AI</span>
<h1>AI, explained <em style="font-style:normal;color:var(--purple)">for everyone.</em></h1>
<p class="big-q" style="border-color:var(--purple)">What is AI, and what does it mean for my life?</p>
<p class="updated">Updated November 2026</p>
<p class="lead">Start from zero, get straight answers to the questions people ask most, learn the words everyone's using, and catch up on what's happening right now.</p>
</div><a class="stat-card start-card" href="#start"><span class="kicker c-work">Start here</span><p class="num c-work" style="color:var(--purple)">5 parts</p><p>A Beginner's Guide to AI. Short reads, in order, from "What is AI?" to using it safely.</p><span class="go">Start Part 1 →</span></a></div></section>

<section class="steps-band"><div class="container"><div class="center-head"><span class="eyebrow">Start here</span><h2>Three ways to get up to speed</h2></div>
<div class="plp-grid">
<a class="plp-card" href="#start"><span class="n">1</span><h3>Start from zero</h3><p>The 5-part Beginner's Guide to AI, in order.</p><span class="go">Read the series →</span></a>
<a class="plp-card" href="#questions"><span class="n">2</span><h3>Get answers</h3><p>Straight answers to the questions people ask most.</p><span class="go">See the questions →</span></a>
<a class="plp-card" href="#glossary"><span class="n">3</span><h3>Learn the words</h3><p>20 AI terms explained in everyday language.</p><span class="go">See the words →</span></a>
</div></div></section>

{try_html}

<section class="eco-section soft" id="right-now"><div class="container">
<div class="center-head"><span class="eyebrow">Right now in AI</span><h2>What's happening, and why it matters</h2><p style="margin:12px auto 0;max-width:640px">Four developments that affect everyday people this year, each linked to what you can do about it.</p></div>
<div class="now-grid">{now_html}</div>
</div></section>

<section class="eco-section" id="start"><div class="container">
<div class="center-head"><span class="eyebrow">Start from zero</span><h2>A Beginner's Guide to AI</h2><p style="margin:12px auto 0;max-width:600px">Five short parts on Substack. Read them in order.</p></div>
<div class="series-grid" id="series"></div>
<p class="series-progress" id="seriesProgress" role="status" aria-live="polite"></p>
</div></section>

<section class="eco-section soft" id="questions"><div class="container">
<div class="center-head"><span class="eyebrow">Your AI questions, answered</span><h2>The questions people ask most</h2></div>
<div class="faq-list">{faq_html}</div>
</div></section>

{quiz_html}

<section class="eco-section" id="glossary"><div class="container">
<div class="center-head"><span class="eyebrow">AI words, explained</span><h2>20 words everyone's using</h2><p style="margin:12px auto 0;max-width:600px">Tap "Share this word" to copy a link you can text to a friend.</p></div>
<dl class="gl-grid">{glossary_html}</dl>
</div></section>

<section class="eco-section soft" id="for-you"><div class="container">
<div class="center-head"><span class="eyebrow">What AI means for you</span><h2>Now put it to work in your life</h2><p style="margin:12px auto 0;max-width:600px">Each page has free tools, AI prompts and real places to get help.</p></div>
<div class="pl-links">{pillar_links_html}</div>
</div></section>

<section class="eco-section" id="library"><div class="container">
<div class="center-head"><span class="eyebrow">The library</span><h2>Every article in one place</h2></div>
<div id="featured"></div>
<div class="lib-controls"><input class="lib-search" id="search" type="search" placeholder="Search articles…" aria-label="Search articles"><div class="mk-chips" id="chips" role="group" aria-label="Filter by topic"></div></div>
<p class="lib-count" id="resultCount" role="status" aria-live="polite"></p>
<div class="lib-grid" id="grid"></div>
<p class="lib-empty" id="empty" hidden>Nothing matches that yet. Try another word.</p>
<p class="lib-more">Want step-by-step playbooks? <a href="guides.html#playbooks">See my guides →</a></p>
</div></section>
{faq_ld}
{join("AI")}'''

# ---------- Jobs ----------
def wcard(kicker, name, url, what, note, kc="c-work"):
    title = f'<a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a>' if url else name
    go = f'<a class="go" href="{url}" target="_blank" rel="noopener noreferrer">Visit {name} →</a>' if url else ''
    return f'<article class="partner-card"><span class="kicker {kc}">{kicker}</span><h3>{title}</h3><p>{what}</p><p class="note">{note}</p>{go}</article>'

def jcheck(i, title, text, link=""):
    return f'<li class="jc-item"><label><input type="checkbox" data-k="{i}"><span class="jc-box" aria-hidden="true"></span><span class="jc-text"><strong>{title}</strong> {text}</span></label>{link}</li>'

def ext(url, label):
    return f'<a class="jc-link" href="{url}" target="_blank" rel="noopener noreferrer">{label} ↗</a>'

FIRST_WEEK = [
 ("File for unemployment right away.", "Apply in the state where you worked, even if you're not sure you qualify. Each state has its own rules, so don't wait.", ext("https://www.careeronestop.org/LocalHelp/local-help.aspx", "Find your state's unemployment office")),
 ("Sort out health coverage.", "You have 60 days after losing job-based coverage to sign up for a Marketplace plan. COBRA keeps your same plan, but you pay the full cost, so compare both.", ext("https://www.healthcare.gov/unemployed/cobra-coverage/", "Compare COBRA and Marketplace plans")),
 ("Get the details in writing.", "Your final paycheck, unused vacation pay, severance, and the date your benefits end. Ask for time to read any severance agreement before you sign it.", ""),
 ("Don't cash out your 401(k).", "Leaving it where it is or rolling it over avoids taxes and early-withdrawal penalties.", ""),
 ("Make a bare-bones budget.", "Know how many weeks your savings can cover. If a bill will be late, call the company early and ask about hardship programs.", '<a class="jc-link" href="finance.html#fin-calc">Use the paycheck cushion tool →</a>'),
 ("Tell people you're looking.", "Former coworkers, friends, neighbors, your church or community group. Many jobs are filled through someone who knows you.", ""),
 ("Visit your American Job Center.", "Free career counselors, job search workshops, free computer access and help paying for training. Or call 1-877-US-2JOBS.", ext("https://www.careeronestop.org/LocalHelp/local-help.aspx", "Find one near you")),
 ("Update your resume with AI.", "Use the prompts below to match your resume to each job and practice for interviews.", '<a class="jc-link" href="#get-hired">See the prompts →</a>'),
]
first_week_html = "".join(jcheck(i, t, d, l) for i, (t, d, l) in enumerate(FIRST_WEEK))

def board(kicker, title, text, url, label, outside=True):
    tgt = ' target="_blank" rel="noopener noreferrer"' if outside else ''
    arrow = "↗" if outside else "→"
    return f'<article class="jb-card"><span class="kicker c-work">{kicker}</span><h3>{title}</h3><p>{text}</p><a href="{url}"{tgt}>{label} {arrow}</a></article>'

BOARDS = "".join([
 board("All jobs", "CareerOneStop Job Finder", "A free U.S. Department of Labor job search that pulls listings from several job sites, updated daily.", "https://www.careeronestop.org/JobSearch/job-search.aspx", "Search jobs near you"),
 board("Your state", "Your state's job bank", "Every state runs a free job site, often tied to your unemployment account. Search \"[your state] job bank.\" Many state government jobs no longer require a degree.", "https://www.careeronestop.org/LocalHelp/local-help.aspx", "Find your state's job services"),
 board("Government", "USAJOBS", "Federal jobs across the country. Federal hiring is moving away from degree requirements toward tests of real job skills.", "https://www.usajobs.gov", "Search federal jobs"),
 board("Earn while you learn", "Paid apprenticeships", "Get a paycheck while you train in the trades, IT, health care and more. No experience needed for many programs.", "https://www.apprenticeship.gov/apprenticeship-job-finder", "Search Apprenticeship.gov"),
 board("No degree needed", "Skills-first employers", "Companies in the Tear the Paper Ceiling campaign have committed to hiring for skills, not just degrees.", "https://tearthepaperceiling.org", "See the employers"),
 board("Health care", "Hospital and clinic jobs", "Many entry jobs train you on the job: patient transport, sterile processing, unit secretary, nursing assistant. Check local hospital career pages.", "healthcare.html#ladders", "See health care career ladders", False),
 board("Hands-on", "Skilled trades", "Electricians, HVAC, plumbers, welders and wind techs are in demand and hard for AI to replace.", "work.html#hands-on", "See the careers and pay", False),
 board("Remote", "Work from home", "Use the \"remote\" filter on any job site. FlexJobs screens remote jobs by hand to filter out scams (paid).", "https://www.flexjobs.com", "Browse FlexJobs"),
])

NO_DEGREE = [
 ("Electrician, HVAC tech, plumber", "Paid apprenticeship or trade school", "work.html#hands-on"),
 ("Nursing assistant (CNA)", "State-approved program, often a few weeks", "healthcare.html#ladders"),
 ("Medical assistant, phlebotomist, pharmacy tech", "Certificate program, usually a few months", "healthcare.html#ladders"),
 ("Sterile processing tech", "Certificate program; many hospitals train on the job", "healthcare.html#ladders"),
 ("IT support specialist", "Google IT Support or CompTIA A+ certificate, a few months", "https://www.coursera.org/professional-certificates"),
 ("Truck driver (CDL)", "CDL training, often a few weeks; some companies pay for it", "https://www.careeronestop.org/JobSearch/job-search.aspx"),
 ("Wind turbine technician", "Technical program at a community college", "work.html#hands-on"),
 ("Customer success, sales, office admin", "Your people skills and experience; AI skills set you apart", "#get-hired"),
]
def nd_row(job, how, url):
    tgt = ' target="_blank" rel="noopener noreferrer"' if url.startswith("http") else ''
    return f'<tr><th scope="row">{job}</th><td>{how}</td><td><a href="{url}"{tgt}>Learn more</a></td></tr>'
no_degree_html = "".join(nd_row(*r) for r in NO_DEGREE)

JOB_PROMPTS = [
 ("Match my resume to this job", "Here is my resume: [paste]. Here is the job post: [paste]. Rewrite my summary and bullet points to match this job, using only experience I really have. Then list any skills from the post that I'm missing."),
 ("Explain a layoff or a gap", "I was laid off from my job as a [job] in [month] because [reason, like company cutbacks]. Write two calm, positive sentences I can say in an interview about it, then one sentence that turns to what I can do for them."),
 ("Practice an interview", "Act as a hiring manager for a [job title] job. Ask me one interview question at a time. After each answer, tell me what was strong and how to make it better."),
 ("Find jobs my skills fit", "I worked as a [job] for [years] years. List the skills I built that other employers want, in the words they use, and suggest 5 job titles I could apply for without a four-year degree."),
 ("Write a thank-you email", "Write a short thank-you email after my interview for the [job] position at [company] with [name]. Mention [something we talked about]. Keep it under 120 words."),
]
job_prompts_html = "".join(f'<details class="prompt"><summary>{t}</summary><p class="prompt-text">{p}</p><button class="copy-btn" type="button">Copy prompt</button></details>' for t, p in JOB_PROMPTS)

jobs_body = f'''<section class="pillar-hero"><div class="container pillar-hero-grid"><div>
<span class="eyebrow" style="color:var(--purple)">Jobs</span>
<h1>Find work that pays, <em style="font-style:normal;color:var(--purple)">with or without a degree.</em></h1>
<p class="big-q" style="border-color:var(--purple)">Where are the jobs?</p>
<p class="updated">Updated November 2026</p>
<p class="lead">Where to look, who's hiring for skills instead of degrees, and how to get hired faster with AI. Every link here is free unless it says otherwise.</p>
</div><a class="stat-card start-card" href="#first-week"><span class="kicker c-work">Just lost your job?</span><p class="num" style="color:var(--purple)">Your first 7 days</p><p>A simple checklist: unemployment, health coverage, money and your job search.</p><span class="go">Start the checklist →</span></a></div></section>

<section class="steps-band"><div class="container"><div class="center-head"><span class="eyebrow">Start here</span><h2>Three ways in</h2></div>
<div class="plp-grid">
<a class="plp-card" href="#first-week"><span class="n">1</span><h3>I just lost my job</h3><p>What to do this week, in order.</p><span class="go">See the checklist →</span></a>
<a class="plp-card" href="#where"><span class="n">2</span><h3>Show me the jobs</h3><p>The best free places to search, by type of job.</p><span class="go">Find jobs →</span></a>
<a class="plp-card" href="#get-hired"><span class="n">3</span><h3>Help me get hired</h3><p>AI prompts for your resume, interviews and follow-ups.</p><span class="go">Get the prompts →</span></a>
</div></div></section>

<section class="eco-section" id="first-week"><div class="container">
<div class="center-head"><span class="eyebrow">Just lost your job?</span><h2>Your first 7 days</h2><p style="margin:12px auto 0;max-width:640px">Losing a job is hard, and it's not a measure of your worth. Take it one step at a time. Check things off as you go; your progress is saved on this device.</p></div>
<ol class="jc-list" id="jc-list">{first_week_html}</ol>
<p class="jc-progress" id="jc-progress" role="status" aria-live="polite"></p>
<p class="safe-note" style="max-width:760px;margin:18px auto 0;text-align:center">Need help with food, rent or utilities right now? Call or text <strong>211</strong>, or visit <a href="https://www.211.org" target="_blank" rel="noopener noreferrer">211.org</a>, to reach local help.</p>
</div></section>

<section class="eco-section soft" id="where"><div class="container">
<div class="center-head"><span class="eyebrow">Where the jobs are</span><h2>The best free places to look</h2></div>
<div class="jb-grid">{BOARDS}</div>
<div class="tip-row one"><article class="tip-box"><h3>Search smarter</h3><ul class="scam-list">
<li><strong>Add "no degree" or "or equivalent experience"</strong> to any job search to find jobs that hire for skills.</li>
<li><strong>Set up job alerts</strong> and apply in the first few days a job is posted.</li>
<li><strong>Watch for scams.</strong> A real employer will never ask you to pay to apply, buy equipment up front or deposit a check for them.</li>
</ul><p style="margin:10px 0 0"><a href="understanding-ai.html#scam-quiz" style="color:var(--green);font-weight:700">Take the AI scam quiz →</a></p></article></div>
</div></section>

<section class="eco-section" id="no-degree"><div class="container">
<div class="center-head"><span class="eyebrow">No four-year degree needed</span><h2>Good jobs you can train for fast</h2><p style="margin:12px auto 0;max-width:640px">These jobs are in demand, and people get into them through short training, apprenticeships or on-the-job learning.</p></div>
<div class="nd-wrap"><table class="nd-table"><thead><tr><th scope="col">Job</th><th scope="col">How people get started</th><th scope="col"><span class="sr-only">Link</span></th></tr></thead><tbody>{no_degree_html}</tbody></table></div>
<p class="safe-note" style="text-align:center;margin:16px auto 0;max-width:900px">An American Job Center may be able to help pay for training. Build a <a href="education.html#passport" style="color:var(--green);font-weight:700">Skills Passport</a> to show employers what you can do.</p>
</div></section>

<section class="eco-section soft" id="get-hired"><div class="container">
<div class="center-head"><span class="eyebrow">Get hired faster with AI</span><h2>Five prompts for your job search</h2><p style="margin:12px auto 0;max-width:660px">Paste one into ChatGPT, Claude or Gemini and fill in the brackets. Always read the result and make it sound like you. Never paste your Social Security number or bank details.</p></div>
<div class="tip-row one"><article class="tip-box"><div class="prompt-list">{job_prompts_html}</div>
<p style="margin:6px 0 0">Many employers use software to screen resumes. <a href="https://www.jobscan.co" target="_blank" rel="noopener noreferrer" style="color:var(--green);font-weight:700">Jobscan</a> shows how yours scores against a job post (free scans, paid plan for more).</p></article></div>
</div></section>

<section class="eco-section" id="bridge"><div class="container">
<div class="center-head"><span class="eyebrow">Money while you search</span><h2>Keep something coming in</h2></div>
<div class="jb-grid three">
{board("Fast", "Temp and staffing agencies", "Many pay weekly, and some temp jobs turn into permanent ones. Look for local agencies in health care, warehouses and offices.", "https://www.careeronestop.org/JobSearch/job-search.aspx", "Search temp jobs")}
{board("Flexible", "Part-time and seasonal work", "Retail, delivery and seasonal jobs can cover the gap while you look for the right full-time job.", "https://www.careeronestop.org/JobSearch/job-search.aspx", "Search part-time jobs")}
{board("Your skills", "Build a second paycheck", "Four realistic ways to earn on your own, with AI handling the paperwork.", "work.html#second-paycheck", "See the options", False)}
</div>
</div></section>

<section class="eco-section soft" id="help"><div class="container">
<div class="center-head"><span class="eyebrow">Tools worth knowing</span><h2>Free first, paid only if it helps</h2></div>
<div class="partner-grid four">
<article class="partner-card free"><span class="kicker c-work">Free</span><h3>American Job Center</h3><p>Free career counselors, workshops, computers and help paying for training. About 2,300 centers nationwide.</p><p class="note">Call 1-877-US-2JOBS or search by ZIP code.</p><a class="go" href="https://www.careeronestop.org/LocalHelp/local-help.aspx" target="_blank" rel="noopener noreferrer">Find one near you →</a></article>
{wcard("Resume check", "Jobscan", "https://www.jobscan.co", "Compares your resume to a job post the way hiring software does, and shows which keywords are missing.", "Free scans; paid plan for more.")}
{wcard("Remote jobs", "FlexJobs", "https://www.flexjobs.com", "Remote, part-time and flexible jobs screened by hand to filter out scams.", "Paid subscription. Worth it if you're focused on remote work.")}
{wcard("New skills", "Coursera", "https://www.coursera.org/professional-certificates", "Career certificates from Google, IBM and others in IT support, data and project management.", "Many courses can be audited free; financial aid is available.")}
</div>
<p class="partner-foot">We list services we would recommend to a friend. Some links may earn us a commission at no cost to you; any paid link will be labeled.</p>
</div></section>
{join("job search")}'''

pages_more = {
    "jobs.html": ("Find a Job, With or Without a Degree | The AI Revolution", "Where to find jobs, who hires for skills instead of degrees, a first-week checklist if you lost your job, and AI prompts to get hired faster.", jobs_body, '<script src="jobs.js" defer></script>'),
    "guides.html": ("Free AI Career Tools and Prompts, No Email Required | The AI Revolution", "Every free tool in one place: AI readiness score, job task check, money and housing calculators, skill finder, Skills Passport, AI scam quiz, 18 AI prompts and career maps.", guides_body, ""),
    "marketplace.html": ("AI Gadgets, Home Robots and Smart Home Without Wi-Fi | The AI Revolution", "Home robots, AI glasses, wearable AI recorders and smart lights that work without Wi-Fi, each rated from ready now to moonshot, with honest notes.", market_body, '<script src="market.js" defer></script>'),
    "understanding-ai.html": ("AI Explained: Questions, Words and a Beginner's Guide | The AI Revolution", "What is AI and what does it mean for you? A 5-part beginner's guide, answers to common AI questions, 20 AI words explained, and every article in one place.", understanding_body, '<script src="learn.js" defer></script>'),
    "about.html": ("Our Mission | The AI Revolution", "Adapt Build Evolve: our mission to help working people survive and thrive in the AI era, and why we started.", about_body, ""),
    "disclosure.html": ("Disclosure & Privacy | The AI Revolution", "How The AI Revolution earns money, labels paid links and handles your information.", disclosure_body, ""),
}

WT = [
 ("auto","email","Writing routine emails, letters or reports"),
 ("auto","data","Entering, copying or checking data"),
 ("auto","faq","Answering the same customer questions"),
 ("auto","sched","Scheduling, booking and reminders"),
 ("auto","summ","Summarizing documents, calls or meetings"),
 ("auto","look","Looking up information"),
 ("assist","numbers","Working with numbers or spreadsheets"),
 ("assist","sell","Selling or persuading customers"),
 ("assist","plan","Planning projects or schedules for a team"),
 ("assist","create","Writing marketing or creative content"),
 ("human","hands","Hands-on physical work, building or repairs"),
 ("human","care","Caring for people face to face"),
 ("human","lead","Leading, training or coaching people"),
 ("human","fix","Solving unusual problems on the spot"),
 ("human","calm","Calming upset customers, patients or coworkers"),
 ("human","equip","Operating vehicles, machines or equipment"),
]
wt_checks = "".join(f'<label class="option"><input type="checkbox" name="task" value="{k}" data-group="{g}"> {t}</label>' for g,k,t in WT)

work_prompts = [
 ("Draft a hard email", "Help me write a clear, polite email to [person] about [situation]. I want to [goal]. Keep it under 150 words and calm in tone."),
 ("Turn meeting notes into action items", "Here are my notes from a meeting (no private customer or patient details): [paste]. List the decisions, the action items with who owns each one, and any open questions."),
 ("Write your weekly update in 5 minutes", "Here's what I worked on this week: [list]. Turn it into a short update for my manager: wins, what's in progress, and anything I need help with."),
 ("Turn a messy process into a checklist", "Here's how I do [task] at work: [describe]. Turn it into a clear numbered checklist a new coworker could follow."),
]
work_prompt_html = "".join(f'<details class="prompt"><summary>{t}</summary><p class="prompt-text">{p}</p><button class="copy-btn" type="button">Copy prompt</button></details>' for t,p in work_prompts)

def wcard(kicker, name, url, what, note, kc="c-work"):
    title = f'<a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a>' if url else name
    go = f'<a class="go" href="{url}" target="_blank" rel="noopener noreferrer">Visit {name} →</a>' if url else ''
    return f'<article class="partner-card"><span class="kicker {kc}">{kicker}</span><h3>{title}</h3><p>{what}</p><p class="note">{note}</p>{go}</article>'

work_body = f'''<section class="pillar-hero"><div class="container pillar-hero-grid"><div>
<span class="eyebrow" style="color:var(--purple)">Pillar 1 · The Future of Work</span>
<h1>Make AI work <em style="font-style:normal;color:var(--purple)">for</em> you, not instead of you.</h1>
<p class="big-q" style="border-color:var(--purple)">How do I keep earning when AI can do parts of my job?</p>
<p class="updated">Updated November 2026</p>
<p class="lead">AI is taking over tasks faster than whole jobs. Desk work is changing first, AI now reads job applications before people do, and more workers are adding a second paycheck. Here's what's changing, and how to stay ahead.</p>
</div>{stat("work")}</div></section>

<section class="steps-band"><div class="container"><div class="center-head"><span class="eyebrow">Start here</span><h2>Three ways to stay ahead</h2></div>
<div class="plp-grid">
<a class="plp-card" href="#job-check" data-open="job-check"><span class="n">1</span><h3>Protect</h3><p>See which parts of your job AI is changing, and let AI handle the busywork.</p><span class="go">Check my job →</span></a>
<a class="plp-card" href="#skills-first"><span class="n">2</span><h3>Move up</h3><p>Find employers hiring for skills, hands-on careers, and tools to get hired.</p><span class="go">See where hiring is opening →</span></a>
<a class="plp-card" href="#second-paycheck"><span class="n">3</span><h3>Earn more</h3><p>Add a second paycheck with a skill you already have, a few hours a week.</p><span class="go">Build a second paycheck →</span></a>
</div></div></section>

<section class="soft-band" id="job-check"><div class="container">
<div class="center-head"><span class="eyebrow" style="color:var(--purple)">Job check</span><h2>Which parts of your job is AI changing?</h2><p style="margin:12px auto 0;max-width:640px">Pick your main tasks and see which ones AI is taking on, which it helps with, and which stay human. Takes about a minute. No email required.</p></div>
<div style="text-align:center"><details class="tool-toggle"><summary class="btn primary">Check my job →</summary><div style="text-align:left"><form class="calc task-check" id="job-check-form" novalidate>
<fieldset><legend class="sr-only">Your main tasks</legend><div class="task-grid">{wt_checks}</div></fieldset>
<button class="btn primary" type="submit">Show my results</button>
<div id="job-result" class="calc-result" aria-live="polite" tabindex="-1"></div>
<small>A general guide based on where AI is being used today, not a prediction about your specific job. Work in health care? Try the <a href="healthcare.html#task-check" style="color:var(--green);font-weight:700">healthcare task check</a>. No email required. Your answers stay on your device.</small>
</form>
</div></section>

<section class="eco-section" id="shifts"><div class="container">
<div class="center-head"><span class="eyebrow">What's happening now</span><h2>4 ways AI is changing work</h2></div>
<div class="shift-grid">
{shift("01", "AI changes tasks before whole jobs", "var(--purple)",
 "Microsoft researchers studied how people use its Copilot AI assistant at work and found it helps most with researching, writing and communicating. The lead researcher said the work “does not indicate it can fully perform any single occupation.” The World Economic Forum expects 170 million new jobs and 92 million lost by 2030.",
 "World Economic Forum, Future of Jobs Report 2025; Microsoft Research (2025)", "https://www.weforum.org/press/2025/01/future-of-jobs-report-2025-78-million-new-job-opportunities-by-2030-but-urgent-upskilling-needed-to-prepare-workforces/",
 ["List the five tasks that take up most of your week.",
  "Use the job check above to see which ones AI is taking on.",
  "Get good at using AI for those tasks before someone else does it for you."])}
{shift("02", "Desk work is changing first; hands-on work lasts longer", "var(--green)",
 "The jobs that overlap most with AI involve knowledge work: writers, translators, sales and customer service. The least affected include nursing assistants, phlebotomists and hazardous materials workers. Elon Musk calls AI a “supersonic tsunami” for digital jobs, and an April 2025 executive order set a goal of one million new apprenticeships a year.",
 "Microsoft Research via Fortune (2025)", "https://fortune.com/article/what-are-the-jobs-most-exposed-to-ai-microsoft-researchers-list/?rand=8593",
 ["If your job is mostly screen work, add a people skill or hands-on skill AI can't easily do.",
  "Consider a paid apprenticeship in a trade, health care or IT (see Education).",
  "If your job is hands-on, learn the digital tools around it: quotes, scheduling, records."])}
{shift("03", "AI reads your application before a person does", "var(--navy)",
 "87% of hiring managers say their company uses AI in at least one part of hiring, and 58% use it to screen resumes and applications.",
 "Resume Genius 2026 Hiring Trends Report (survey of 1,000 U.S. hiring managers)", "https://resumegenius.com/blog/job-hunting/hiring-trends-report-2026",
 ["Use the exact words from the job post for skills you really have.",
  "Keep your resume format simple: plain headings, no tables or graphics.",
  "Use AI to tailor your resume, then rewrite it in your own voice. Never let it invent experience.",
  "Ask someone inside the company to refer you. A person still beats the filter."])}
{shift("04", "One paycheck may not be enough", "var(--purple)",
 "35% of U.S. workers now have a side hustle or more than one job, according to a 2026 ZipRecruiter survey. Side hustlers report earning an average of $1,242 a month. AI makes it easier to start: it can write your listings, quotes and follow-ups.",
 "ZipRecruiter (2026); LendingTree (2026)", "https://www.ziprecruiter-research.org/economic-insights-research/more-than-a-third-have-side-hustles",
 ["Start small: 3 to 5 hours a week with a skill you already use.",
  "See the four paths in “Build a second paycheck” below.",
  "Check your employer's rules on outside work before you start."])}
</div>
<div class="next-wave"><span class="eyebrow" style="color:#c9a9ea">What's coming next</span><h3>From AI helpers to AI agents</h3><p>So far, most people use AI to help with one task at a time: write this email, summarize that report. The next wave is AI "agents" that carry out whole chains of work on their own, like finding a supplier, comparing prices, placing the order and updating the spreadsheet. As that spreads, the most valuable workers will be the ones who can set up, check and steer those agents, and who handle the people, judgment and hands-on work they can't.</p><p class="next-do"><strong>What to do now:</strong> get comfortable handing AI a multi-step task and checking its work. The prompts below are a good place to start.</p></div>
</div></section>

<section class="eco-section soft" id="ai-at-work"><div class="container">
<div class="center-head"><span class="eyebrow">Put AI to work for you</span><h2>Let AI handle the busywork</h2><p style="margin:12px auto 0;max-width:640px">Copy a prompt into any AI assistant, such as ChatGPT, Claude or Gemini, and fill in the blanks. Follow your employer's rules on AI tools, and never paste private customer, patient or company information.</p></div>
<div class="tip-row"><article class="tip-box"><h3>Four prompts for everyday work</h3><div class="prompt-list">{work_prompt_html}</div></article>
<article class="tip-box"><h3>Want AI to do this every week?</h3><p>My AI Assistant Playbook walks you through setting up an AI assistant that handles your recurring tasks automatically, step by step.</p><div class="product-row" style="grid-template-columns:1fr">{PRODUCTS}</div><p class="safe-note" style="margin-top:14px">These are my own guides, sold on Gumroad.</p></article></div>
</div></section>

<section class="eco-section" id="skills-first"><div class="container">
<div class="center-head"><span class="eyebrow" style="color:var(--purple)">Skills over degrees</span><h2>Where hiring is opening up</h2><p style="margin:12px auto 0;max-width:680px">More than 70 million U.S. workers, about half the workforce, built their skills through work, the military, community college or training instead of a four-year degree. Employers and governments are starting to hire for those skills.</p></div>
<div class="three four">
<article class="step-card"><span class="n">01</span><h3>Tear the Paper Ceiling employers</h3><p>A national campaign led by Opportunity@Work and the Ad Council. Employers that join commit to looking past degree screens to hire skilled workers.</p><a href="https://tearthepaperceiling.org" target="_blank" rel="noopener noreferrer">See the campaign ↗</a></article>
<article class="step-card"><span class="n">02</span><h3>Federal jobs</h3><p>The Chance to Compete Act of 2024 and the 2025 Merit Hiring Plan move federal hiring away from degree requirements and toward tests of real job skills.</p><a href="https://www.usajobs.gov" target="_blank" rel="noopener noreferrer">Search USAJOBS ↗</a></article>
<article class="step-card"><span class="n">03</span><h3>State jobs</h3><p>Governors in more than 30 states have acted to remove degree requirements from state government jobs. Maryland was the first, in 2022.</p><p class="how-to"><strong>How to look:</strong> search "[your state] state jobs" and look for "or equivalent experience."</p></article>
<article class="step-card"><span class="n">04</span><h3>Paid apprenticeships</h3><p>A 2025 executive order set a goal of one million new apprenticeships a year. You earn a paycheck while you train in IT, health care, the trades and more.</p><a href="https://www.apprenticeship.gov/apprenticeship-job-finder" target="_blank" rel="noopener noreferrer">Search Apprenticeship.gov ↗</a></article>
</div>
<p class="safe-note" style="margin-top:20px">Sources: <a href="https://tearthepaperceiling.org" target="_blank" rel="noopener noreferrer">Tear the Paper Ceiling</a>; <a href="https://www.opm.gov/policy-data-oversight/hiring-information/merit-hiring-plan-resources/merit-hiring-plan-overview-guidance" target="_blank" rel="noopener noreferrer">U.S. Office of Personnel Management</a>; <a href="https://www.nga.org/news/press-releases/national-governors-association-and-walmart-partner-to-advance-skills-first-hiring-and-workforce-development-in-states/" target="_blank" rel="noopener noreferrer">National Governors Association</a>. Next step: build a <a href="education.html#passport" style="color:var(--green);font-weight:700">Skills Passport</a> to show employers what you can do.</p>
<p class="jobs-cta">Ready to apply? <a href="jobs.html">See the best free places to find jobs →</a></p>
{SHOWCASE_BLOCK}
</div></section>

<section class="eco-section soft" id="hands-on"><div class="container">
<div class="center-head"><span class="eyebrow" style="color:var(--green)">Hands-on careers</span><h2>Careers that need a person on site</h2><p style="margin:12px auto 0;max-width:680px">These careers need a person on site. Most start with paid on-the-job training or a short certificate, not a four-year degree.</p></div>
<div class="partner-grid three-col"><article class="partner-card"><span class="kicker c-home">Apprenticeship</span><h3>Electricians</h3><p>Wire homes, businesses, factories and power systems. Needed in nearly every building, plus solar and wind hookups.</p><p class="note"><strong>Median pay:</strong> $63,190 a year<br><strong>Outlook:</strong> 9% growth by 2035, much faster than average</p><a class="go" href="https://www.bls.gov/ooh/construction-and-extraction/electricians.htm" target="_blank" rel="noopener noreferrer">Pay and training details ↗</a></article><article class="partner-card"><span class="kicker c-home">Training program</span><h3>HVAC technicians</h3><p>Install and repair heating, cooling and refrigeration systems in homes and buildings.</p><p class="note"><strong>Median pay:</strong> $61,010 a year<br><strong>Outlook:</strong> 11% growth by 2035, much faster than average</p><a class="go" href="https://www.bls.gov/ooh/installation-maintenance-and-repair/heating-air-conditioning-and-refrigeration-mechanics-and-installers.htm" target="_blank" rel="noopener noreferrer">Pay and training details ↗</a></article><article class="partner-card"><span class="kicker c-home">Apprenticeship</span><h3>Plumbers and pipefitters</h3><p>Install and repair water, gas and piping systems in homes, businesses and power plants.</p><p class="note"><strong>Median pay:</strong> $63,800 a year<br><strong>Outlook:</strong> 7% growth by 2035, much faster than average</p><a class="go" href="https://www.bls.gov/ooh/construction-and-extraction/plumbers-pipefitters-and-steamfitters.htm" target="_blank" rel="noopener noreferrer">Pay and training details ↗</a></article><article class="partner-card"><span class="kicker c-home">Certificate</span><h3>Wind turbine technicians</h3><p>Climb, maintain and repair wind turbines. Among the fastest-growing jobs in the country.</p><p class="note"><strong>Median pay:</strong> $64,120 a year<br><strong>Outlook:</strong> 30% growth by 2035, much faster than average</p><a class="go" href="https://www.bls.gov/ooh/installation-maintenance-and-repair/wind-turbine-technicians.htm" target="_blank" rel="noopener noreferrer">Pay and training details ↗</a></article><article class="partner-card"><span class="kicker c-home">Training program</span><h3>Welders</h3><p>Join and cut metal for buildings, ships, pipelines and manufacturing. Usually a high school diploma plus training.</p><p class="note"><strong>Median pay:</strong> $53,750 a year<br><strong>Outlook:</strong> Steady demand, slower growth than average</p><a class="go" href="https://www.bls.gov/ooh/production/welders-cutters-solderers-and-brazers.htm" target="_blank" rel="noopener noreferrer">Pay and training details ↗</a></article><article class="partner-card"><span class="kicker c-home">State-approved program</span><h3>Nursing assistants</h3><p>Care for patients face to face in hospitals and nursing homes. About 203,000 openings a year.</p><p class="note"><strong>Median pay:</strong> $42,260 a year<br><strong>Outlook:</strong> 3% growth by 2035, about average</p><a class="go" href="https://www.bls.gov/ooh/healthcare/nursing-assistants.htm" target="_blank" rel="noopener noreferrer">Pay and training details ↗</a></article></div>
<div class="tip-row" style="margin-top:22px"><article class="tip-box"><h3>How to get started</h3><ul class="scam-list"><li><strong>Earn while you train.</strong> Search paid apprenticeships near you at <a href="https://www.apprenticeship.gov/apprenticeship-job-finder" target="_blank" rel="noopener noreferrer" style="color:var(--green);font-weight:700">Apprenticeship.gov</a>.</li><li><strong>Ask about free training money.</strong> Your local <a href="https://www.careeronestop.org/LocalHelp/AmericanJobCenters/find-american-job-centers.aspx" target="_blank" rel="noopener noreferrer" style="color:var(--green);font-weight:700">American Job Center</a> can help pay for training in many trades.</li><li><strong>Check your community college</strong> for short certificate programs in HVAC, welding and nursing assistant training.</li></ul></article>
<article class="tip-box"><h3>Already in health care?</h3><p>Hands-on patient care is one of the safest places to be as AI grows. See how AI is changing health care jobs and which tasks stay human.</p><a class="btn primary" href="healthcare.html">Future of Healthcare Work →</a></article></div>
<p class="safe-note" style="margin-top:18px">Pay and outlook: <a href="https://www.bls.gov/ooh/" target="_blank" rel="noopener noreferrer">U.S. Bureau of Labor Statistics, Occupational Outlook Handbook</a> (2025 median pay; projected growth 2025–2035). Pay varies by state and experience.</p>
</div></section>

<section class="eco-section" id="help"><div class="container"><div class="center-head"><span class="eyebrow">Where to get help</span><h2>Tools to get hired and move up</h2><p style="margin:12px auto 0;max-width:660px">Matched to the shifts above: getting past AI resume screening, protecting the job you have, changing careers, and finding flexible work. Free options are listed too.</p></div><div class="partner-grid four">
{wcard("Get past AI screening", "Jobscan", "https://www.jobscan.co", "Compares your resume to a job post the way hiring software does, and shows which skills and keywords are missing.", "Free scans to start, then a paid plan. Use it to tailor, not to stuff in keywords you can't back up.")}
{wcard("Keep your job safe", "LinkedIn Learning", "https://www.linkedin.com/learning", "Short video courses on AI tools, Excel, leadership and more. Finished courses show on your LinkedIn profile, where employers and recruiters can see them.", "Free trial to start, then a monthly subscription. Some libraries and employers give free access, so check yours first.")}
{wcard("Change careers", "Coursera", "https://www.coursera.org/professional-certificates", "Professional certificates from Google, IBM and others in AI, data, IT support and project management.", "Many courses can be audited for free; financial aid is available.")}
{wcard("Remote and flexible jobs", "FlexJobs", "https://www.flexjobs.com", "Remote, part-time and flexible jobs that are screened by hand to filter out scams.", "Paid subscription. Worth it if you're serious about remote or part-time work.")}
</div>
<article class="partner-card free" style="margin-top:20px"><span class="kicker c-home">Free options</span><h3>Free help</h3><p>Your local <a href="https://www.careeronestop.org/LocalHelp/AmericanJobCenters/find-american-job-centers.aspx" target="_blank" rel="noopener noreferrer">American Job Center</a> offers free job search help and training funds. Search paid apprenticeships at <a href="https://www.apprenticeship.gov/apprenticeship-job-finder" target="_blank" rel="noopener noreferrer">Apprenticeship.gov</a>. Upwork and Fiverr are free to join for side work.</p></article>
<p class="partner-foot">We list services we would recommend to a friend. Some links may earn us a commission at no cost to you; any paid link is labeled. General career information, not legal or employment advice.</p></div></section>

<section class="eco-section soft" id="second-paycheck"><div class="container">
<div class="center-head"><span class="eyebrow">Build a second paycheck</span><h2>Four realistic ways to earn on the side</h2><p style="margin:12px auto 0;max-width:660px">You don't need a big idea. Most side income starts with a skill you already use, a few hours a week, and AI to handle the writing and admin.</p></div>
<div class="three four">
<article class="project-card"><span class="kicker c-work">Easiest start</span><h3>Sell a skill you use at work</h3><p>Scheduling, bookkeeping, data entry, writing, customer follow-up. Offer it to small businesses or on freelance sites like Upwork or Fiverr.</p><p class="learn"><strong>AI helps:</strong> write your profile, proposals and quotes.</p></article>
<article class="project-card"><span class="kicker c-home">Hard for AI to replace</span><h3>Local hands-on services</h3><p>Handyman work, cleaning, pet care, moving help, yard work. Neighbors and apps like Nextdoor bring steady local customers.</p><p class="learn"><strong>AI helps:</strong> price jobs, answer messages and post ads.</p></article>
<article class="project-card"><span class="kicker c-work">Uses what you know</span><h3>Teach or tutor</h3><p>Tutor students, train new hires in your field, or turn what you know into a short guide or class you sell online.</p><p class="learn"><strong>AI helps:</strong> build lesson plans, worksheets and quizzes.</p></article>
<article class="project-card"><span class="kicker c-home">Steadier hours</span><h3>Part-time remote work</h3><p>Part-time remote roles in customer support, admin, scheduling and data. Use screened job boards to avoid scams.</p><p class="learn"><strong>AI helps:</strong> tailor your resume and practice interviews.</p></article>
</div>
<div class="tip-row" style="margin-top:22px"><article class="tip-box"><h3>Before you start</h3><ul class="scam-list"><li><strong>Keep it separate.</strong> Open a separate bank account for side income so taxes and records stay simple (see <a href="finance.html#help" style="color:var(--green);font-weight:700">banking and tax help</a>).</li><li><strong>Save for taxes.</strong> Side income usually has no taxes taken out. Set some aside from every payment; a tax tool or tax pro can tell you how much.</li><li><strong>Watch for scams.</strong> Real jobs never ask you to pay to start, buy equipment up front, or deposit a check and send money back.</li><li><strong>Check your job's rules</strong> on outside work and conflicts of interest.</li></ul></article>
<article class="tip-box"><h3>Show clients what you can do</h3><p>Build a one-page Skills Passport with three projects and results. It works for side clients the same way it works for employers.</p><a class="btn primary" href="education.html#passport">Build my Skills Passport →</a><p style="margin-top:16px">Need a skill first? Get a personal starting plan with the <a href="education.html#learn-first" style="color:var(--green);font-weight:700">skill finder</a>.</p></article></div>
</div></section>

<section class="soft-band"><div class="container">
<div class="row-head"><div><span class="eyebrow">Read more</span><h2>From the newsletter</h2></div><a href="understanding-ai.html">All articles →</a></div>
{posts([
 ("The Jobs AI Is Changing Right Now", "Which jobs are shifting, and what that means for you.", SUB+"the-jobs-ai-is-changing-right-now"),
 ("How AI Screens Resumes — and How to Prepare", "Get your resume past AI screening software.", SUB+"how-ai-screens-resumes-and-how-to"),
 ("Put AI to Work While You Sleep", "The one AI skill that saves hours every week.", SUB+"put-ai-to-work-while-you-sleep"),
])}
<p style="margin-top:22px">No degree? See where employers are <a href="education.html#skills" style="color:var(--green);font-weight:700">hiring for skills instead</a>.</p>
</div></section>

{join("Work", "work-email")}'''

pages = {
    "index.html": ("Stay Ahead of AI at Work, Home and Money | The AI Revolution", "Will AI take your job? Free tools and easy guides to protect your job, move up, and build income as AI changes work, housing, money and health care.", home_body, '<script src="score.js" defer></script>'),
    "work.html": ("Will AI Take My Job? Check Your Tasks | The AI Revolution", "See which parts of your job AI is changing, get past AI resume screening, find skills-first employers and hands-on careers, and build a second paycheck.", work_body, '<script src="work-tools.js" defer></script>'),
    "housing.html": ("AI Tenant Screening and Rent Software: Your Rights | The AI Revolution", "How AI screens renters and sets rent, what you can do about it, a housing cost calculator, and free AI prompts to dispute a report or push back on rent.", housing_body, '<script src="housing-calc.js" defer></script>'),
    "finance.html": ("How AI Is Changing Money, and How to Start Investing | The AI Revolution", "How AI is changing how we earn, pay and save, a paycheck cushion calculator, AI money scams to watch for, and a simple guide to start investing.", finance_body, '<script src="finance-calc.js" defer></script>'),
    "education.html": ("Skills Over Degrees: Learning in the AI Era | The AI Revolution", "How adults can keep learning as AI changes work, where employers hire for skills instead of degrees, a free skill finder, and how children will learn.", education_body, '<script src="education-path.js" defer></script><script src="passport.js" defer></script>'),
    "healthcare.html": ("How AI Is Changing Healthcare Jobs: Career Ladders and Pay | The AI Revolution", "Which healthcare tasks AI is taking over, career ladders with pay for nursing, imaging and health information, and AI prompts for healthcare workers.", healthcare_body, '<script src="healthcare-check.js" defer></script>'),
}
pages.update(pages_more)
for name, (title, desc, body, js) in pages.items():
    (ROOT / name).write_text(page(name, title, desc, body, js))

# ---------- Update nav + footer on existing pages ----------
NAV_RE = re.compile(r'<nav class="nav" id="main-nav"[^>]*>.*?</nav>', re.S)
FOOT_RE = re.compile(r'<div class="foot-links">.*?</div>', re.S)
for f in sorted(ROOT.rglob("*.html")):
    rel = f.relative_to(ROOT).as_posix()
    if rel in pages:
        continue
    pre = "../" if "/" in rel else ""
    s = f.read_text()
    n1 = len(NAV_RE.findall(s)); n2 = len(FOOT_RE.findall(s))
    s = NAV_RE.sub(lambda m: nav(f.name, pre), s)
    s = FOOT_RE.sub(lambda m: foot_links(pre), s)
    if 'ecosystem.css' not in s and n1:
        s = s.replace(f'<link rel="stylesheet" href="{pre}style.css">', f'<link rel="stylesheet" href="{pre}style.css"><link rel="stylesheet" href="{pre}ecosystem.css">', 1)
    if 'analytics.js' not in s:
        tm = re.search(r'<title>(.*?)</title>', s); dm = re.search(r'<meta name="description" content="([^"]*)"', s)
        t = tm.group(1) if tm else "The AI Revolution"; d = dm.group(1) if dm else ""
        s = s.replace(tm.group(0), tm.group(0) + head_extra(rel, t, d, pre), 1)
    f.write_text(s)
    print(rel, "nav", n1, "footer", n2)

# ---------- Old pages now point to the Marketplace ----------
REDIRECT = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=marketplace.html#home-office"><link rel="canonical" href="https://theairevolution.net/marketplace.html"><title>Moved to the Marketplace | The AI Revolution</title></head><body><p>This page has moved to the <a href="marketplace.html">AI Revolution Marketplace</a>.</p></body></html>'''
(ROOT / "lab.html").write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=understanding-ai.html"><link rel="canonical" href="https://theairevolution.net/understanding-ai.html"><title>Moved to Understanding AI | The AI Revolution</title></head><body><p>This page has moved to <a href="understanding-ai.html">Understanding AI</a>.</p></body></html>''')
for old, tag in [("home.html", "pick-home"), ("office.html", "pick-office")]:
    (ROOT / old).write_text(REDIRECT.replace("marketplace.html#home-office", "marketplace.html#" + tag))

# ---------- Google Search Console verification (do not remove) ----------
GSC = '<meta name="google-site-verification" content="yyV0nYsBCZVySPGIf4YILyVlVIKkFei4jze9mTq1eWg" />'
for f in list(ROOT.glob("*.html")) + list(ROOT.glob("blog/*.html")):
    s = f.read_text()
    if "google-site-verification" not in s and '<meta charset="utf-8">' in s:
        f.write_text(s.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + GSC, 1))

# ---------- Cache busting: tag local .js/.css links with a short hash of the file ----------
import hashlib as _hl, re as _re2
def _ver(path):
    try: return _hl.md5(path.read_bytes()).hexdigest()[:8]
    except FileNotFoundError: return None
for f in list(ROOT.glob("*.html")) + list(ROOT.glob("blog/*.html")):
    s = f.read_text()
    def _tag(m):
        attr, url = m.group(1), m.group(2)
        if url.startswith(("http", "//")): return m.group(0)
        clean = url.split("?")[0]
        v = _ver((f.parent / clean).resolve())
        return f'{attr}="{clean}?v={v}"' if v else m.group(0)
    s2 = _re2.sub(r'(src|href)="([^"]+\.(?:js|css)(?:\?v=[0-9a-f]+)?)"', _tag, s)
    if s2 != s: f.write_text(s2)
