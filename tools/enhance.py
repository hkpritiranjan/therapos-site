#!/usr/bin/env python3
"""Idempotent page chrome for every docs page: heading ids, sidebar, breadcrumbs,
skip link, search button, purpose strip, legends, table regions, journey nav.
Run:  python3 tools/enhance.py   (then tools/build.py, then tools/check.py)"""
import re, json, glob, html, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
P = json.load(open('data/pages.json'))
FILES = sorted(glob.glob('docs/*.html'))
slug_of = lambda f: os.path.basename(f)[:-5]

def strip(t): return html.unescape(re.sub(r'<[^>]+>', '', t)).strip()
def slugs(text):
    raw = re.sub(r'[^a-z0-9\s-]', '', text.lower().replace('\u2013', '-'))
    t = raw.strip()
    return [re.sub(r'\s+', '-', t), t.replace(' ', '-'), raw.replace(' ', '-'), re.sub(r'\s+', '-', raw)]

# anchors referenced anywhere, per target page
refs = {}
for f in FILES + ['index.html']:
    s = open(f).read()
    for h in re.findall(r'href="([^"]*#[^"]+)"', s):
        p, _, a = h.partition('#')
        tgt = slug_of(f) if not p else os.path.basename(p).replace('.html', '')
        refs.setdefault(tgt, set()).add(a)

def add_ids(s, page):
    used = set(re.findall(r'id="([^"]+)"', s)); want = refs.get(page, set())
    def r(m):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        if 'id=' in attrs: return m.group(0)
        cs = slugs(strip(inner)); cand = [x for x in cs if x in want] or [cs[0]]
        i = cand[0]
        if i in used: return m.group(0)
        used.add(i); return f'<{tag}{attrs} id="{i}">{inner}</{tag}>'
    return re.sub(r'<(h[23])([^>]*)>(.*?)</\1>', r, s, flags=re.S)

def alias_anchors(s, page):
    """For referenced fragments with no target, drop an invisible anchor on the best-matching heading
    (exact normalised match first, then prefix). Idempotent: skips fragments that already resolve."""
    have = set(re.findall(r'\sid="([^"]+)"', s)); norm = lambda x: re.sub(r'[^a-z0-9]', '', x.lower())
    for frag in sorted(refs.get(page, set()) - have):
        cands = [(m.start(), m.end(), norm(strip(m.group(3))), norm(m.group(2) or '')) for m in re.finditer(r'<(h[234]|div class="tl-label")( [^>]*)?>(.*?)</(?:h[234]|div)>', s, flags=re.S)]
        n = norm(frag)
        pick = next((c for c in cands if c[2] == n or c[2].rstrip('abcdefghijklmnopqrstuvwxyz') == n and False), None) or next((c for c in cands if c[2].startswith(n) and n), None)
        if not pick and frag.endswith('-'):   # schema model blocks inside <pre>
            nm = frag.rstrip('-').replace('-', ' ')
            m = re.search(rf'(model {nm.replace(" ", "")} \{{|// ── {nm} )', s, flags=re.I)
            if m: s = s[:m.start()] + f'<span id="{frag}"></span>' + s[m.start():]
            continue
        if pick:
            tag_end = s.index('>', pick[0]) + 1
            s = s[:tag_end] + f'<span id="{frag}"></span>' + s[tag_end:]
    return s

def sidebar(active):
    out = ['  <nav class="docs-sidebar" aria-label="Documentation">']
    for g, items in P['groups']:
        out.append(f'    <div class="group">{g}</div>')
        for sl, label in items:
            cur = ' class="active" aria-current="page"' if sl == active else ''
            out.append(f'    <a href="/docs/{sl}.html"{cur}>{label}</a>')
    out.append('  </nav>'); return '\n'.join(out)

def mobile_nav(active):
    out = ['<details class="mobile-nav"><summary>Documentation menu</summary>']
    for g, items in P['groups']:
        out.append(f'<div class="group">{g}</div>')
        for sl, label in items:
            cur = ' aria-current="page"' if sl == active else ''
            out.append(f'<a href="/docs/{sl}.html"{cur}>{label}</a>')
    out.append('</details>'); return ''.join(out)

def group_of(sl):
    for g, items in P['groups']:
        if any(x == sl for x, _ in items): return g
    return 'Docs'

def crumbs(sl, title):
    g = group_of(sl)
    mid = '' if sl == 'index' else f'<span class="sep" aria-hidden="true">/</span><span>{g}</span>'
    here = f'<span class="sep" aria-hidden="true">/</span><span aria-current="page">{title}</span>' if sl != 'index' else ''
    return f'<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span class="sep" aria-hidden="true">/</span><a href="/docs/index.html">Docs</a>{mid}{here}</nav>'

EV = '<div class="legend" role="note" aria-label="Evidence labels"><p class="legend-title">Evidence labels</p>' \
 '<div><span class="ev ev-verified">Verified</span> primary source or documented implementation</div>' \
 '<div><span class="ev ev-reported">Reported</span> secondary or third-party source</div>' \
 '<div><span class="ev ev-inferred">Inferred</span> our reasoning from evidence</div>' \
 '<div><span class="ev ev-hypothesis">Hypothesis</span> assumption needing validation</div>' \
 '<div><span class="ev ev-unknown">Unknown</span> not found or inconclusive</div></div>'
ST = '<div class="legend" role="note" aria-label="Product status labels"><p class="legend-title">Product status</p>' \
 '<div><span class="st st-built">Built</span> implemented and verified</div>' \
 '<div><span class="st st-in-progress">In progress</span> partly implemented</div>' \
 '<div><span class="st st-planned">Planned</span> accepted, not built</div>' \
 '<div><span class="st st-exploratory">Exploratory</span> under consideration</div>' \
 '<div><span class="st st-deferred">Deferred</span> intentionally postponed</div>' \
 '<div><span class="st st-rejected">Rejected</span> evaluated and declined</div></div>'
LEG = {'plan': EV + ST, 'research': EV, 'competitors': EV, 'case-study': ST + EV}

def purpose(sl):
    p = P['purpose'].get(sl)
    if not p: return ''
    rel = ', '.join(f'<a href="/docs/{r}.html">{P["titles"][r]}</a>' for r in p['related'])
    return (f'<div class="purpose"><div><b>Role</b>{p["role"]}</div><div><b>Audience</b>{p["audience"]}</div>'
            f'<div><b>Last reviewed</b><time datetime="{P["updated"]}">{P["updated"]}</time></div><div><b>Related</b>{rel}</div></div>'
            f'<p class="sr-only" style="position:absolute;left:-999px">{p["purpose"]}</p>' + LEG.get(sl, ''))

def journey_nav(sl):
    j = P['journey']
    if sl not in j or sl == 'index': return None
    i = j.index(sl); pv, nx = j[i-1], j[(i+1) % len(j)] if i+1 < len(j) else None
    def btn(t, lab, cls=''):
        return f'<a href="/docs/{t}.html" class="doc-nav-btn{cls}"><span class="doc-nav-label">{lab}</span><span class="doc-nav-title">{P["titles"][t]}</span></a>'
    inner = btn(pv, '← Previous') + (btn(nx, 'Next →', ' next') if nx else '')
    return f'<div class="doc-nav">\n      {inner}\n    </div>'

def wrap(s, key, content, before):
    """Insert/replace a marked block placed before the given regex."""
    blk = f'<!--enh:{key}-->{content}<!--/enh:{key}-->'
    if f'<!--enh:{key}-->' in s:
        return re.sub(rf'<!--enh:{key}-->.*?<!--/enh:{key}-->', lambda m: blk, s, flags=re.S)
    return re.sub(before, lambda m: blk + '\n    ' + m.group(0), s, count=1)

CONV = [('Confirmed', 'verified', 'Verified'), ('Verified', 'verified', 'Verified'), ('Reported', 'reported', 'Reported'),
        ('Inferred', 'inferred', 'Inferred'), ('Unknown', 'unknown', 'Unknown'), ('Unverified', 'hypothesis', 'Hypothesis')]
def normalise_labels(s):
    for old, cls, new in CONV:
        s = re.sub(rf'<span class="badge badge-(?:green|yellow|red|blue|muted)">{old}</span>', f'<span class="ev ev-{cls}">{new}</span>', s)
    s = s.replace('<strong>Confirmed</strong>', '<strong>Verified</strong>')
    return s

for f in FILES:
    sl = slug_of(f); s = open(f).read()
    title = P['titles'].get(sl) or strip(re.search(r'<title>(.*?) — TherapOS', s).group(1))
    s = re.sub(r'(<(?:div|a)\b[^>]*class="card[^"]*"[^>]*>\s*<h4) id="[^"]*"', r'\1', s)
    s = add_ids(s, sl)
    s = alias_anchors(s, sl)
    s = normalise_labels(s)
    s = re.sub(r'<nav class="docs-sidebar">.*?</nav>|<nav class="docs-sidebar" aria-label="Documentation">.*?</nav>', lambda m: sidebar(sl), s, count=1, flags=re.S)
    if 'class="skip-link"' not in s:
        s = s.replace('<body>', '<body>\n<a class="skip-link" href="#main">Skip to content</a>', 1)
    s = s.replace('<main class="docs-content">', '<main class="docs-content" id="main">')
    if 'class="nav-search"' not in s:
        s = s.replace('<a href="../index.html#pricing" class="nav-cta">', '<button type="button" class="nav-search" aria-label="Search documentation">Search<kbd>/</kbd></button>\n    <a href="../index.html#pricing" class="nav-cta">', 1)
    s = s.replace('href="../index.html#', 'href="/index.html#')
    s = wrap(s, 'mnav', mobile_nav(sl), r'<nav class="crumbs"|<!--enh:crumbs-->')
    s = wrap(s, 'crumbs', crumbs(sl, title), r'<span class="eyebrow">')
    s = wrap(s, 'purpose', purpose(sl), r'(?:<h2|<div class="callout|<div class="grid|<p><strong>)') if sl in P['purpose'] else s
    jn = journey_nav(sl)
    if jn and sl in P['purpose']:
        s = re.sub(r'<div class="doc-nav">.*?</div>\s*(?=</main>)', lambda m: jn + '\n  ', s, count=1, flags=re.S)
    # table regions
    def tw(m):
        pre = s[:m.start()]; hs = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', pre, flags=re.S)
        lab = strip(hs[-1]) if hs else 'Data'
        return f'<div class="table-wrap" role="region" tabindex="0" aria-label="Table: {html.escape(lab, quote=True)}">'
    s = re.sub(r'<div class="table-wrap"(?: role="region" tabindex="0" aria-label="[^"]*")?>', tw, s)
    if 'scripts/docs.js' not in s:
        s = s.replace('</body>', '<script src="/scripts/docs.js" defer></script>\n</body>', 1)
    open(f, 'w').write(s)
print('enhanced', len(FILES), 'pages')
