#!/usr/bin/env python3
"""Render generated blocks and pages from data/*.json.
  gen blocks   <!--gen:NAME-->…<!--/gen:NAME-->  always regenerated
  seed blocks  <!--seed:NAME-->…<!--/seed:NAME-->  inserted once from tools/seeds.py, then hand-edit freely
Pipeline: python3 tools/enhance.py && python3 tools/build.py && python3 tools/enhance.py && python3 tools/check.py"""
import re, json, os, html, datetime, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
import sys; sys.path.insert(0, 'tools')
from seeds import SEEDS
SRC = json.load(open('data/sources.json')); D = json.load(open('data/status.json')); PG = json.load(open('data/pages.json'))
CAD = {'volatile': 30, 'legal': 90, 'stable': 180}
for x in SRC:
    v = datetime.date.fromisoformat(x['verified']); x['next'] = (v + datetime.timedelta(days=CAD[x['cadence']])).isoformat()
SBY = {x['id']: x for x in SRC}
esc = lambda t: html.escape(t, quote=True)
cls = lambda s: s.lower().replace(' ', '-')
ev = lambda l: f'<span class="ev ev-{cls(l)}">{l}</span>'
st = lambda l: f'<span class="st st-{cls(l)}">{l}</span>'
def src_links(ids): return ', '.join(f'<a href="/docs/sources.html#{i.lower()}">{i}</a>' for i in ids)
def table(head, rows, extra=''):
    h = ''.join(f'<th scope="col">{x}</th>' for x in head)
    r = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>' for row in rows)
    return f'<div class="table-wrap"><table{extra}><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table></div>'

# ---------- generated blocks ----------
def g_status(compact=False):
    rows = []
    for x in D['status']:
        rows.append([esc(x['item']), st(x['status']), x['area'], esc(x['note'])])
    return table(['Item', 'Status', 'Area', 'Notes and evidence'], rows)
def g_counts():
    order = ['Built', 'In progress', 'Planned', 'Exploratory', 'Deferred', 'Rejected']
    n = {k: sum(1 for x in D['status'] if x['status'] == k) for k in order}
    return ' '.join(f'{st(k)} <b>{n[k]}</b>' for k in order if n[k]), n
def g_decisions():
    rows = []
    for d in sorted(D['decisions'], key=lambda d: d['date'], reverse=True):
        links = ' · '.join(f'<a href="/docs/{u}">{esc(t)}</a>' for u, t in d['links'])
        rows.append([f'<b id="{d["id"].lower()}">{d["id"]}</b>', f'<time datetime="{d["date"]}">{d["date"]}</time>', esc(d['title']), st(d['status']), esc(d['why']), links + (' · ' + src_links(d['src']) if d.get('src') else '')])
    return table(['ID', 'Date', 'Decision', 'Status', 'Why', 'Evidence and detail'], rows, ' class="trace"')
def g_timeline():
    items = ''.join(f'<li><time datetime="{d["date"]}">{d["date"]}</time><b>{d["id"]}</b> {esc(d["title"])} {st(d["status"])}</li>' for d in sorted(D['decisions'], key=lambda d: d['date']))
    return f'<ol class="timeline" aria-label="Decision timeline">{items}</ol>'
def g_bets():
    rows = []
    for b in D['bets']:
        rows.append([f'<b>{b["id"]}</b> {esc(b["name"])}<br>{st(b["status"])}', esc(b['problem']), src_links(b['evidence']), esc(b['hypothesis']), esc(b['action']), esc(b['metric']), esc(b['threshold']), esc(b['review']), st('Not started') if b['outcome'] == 'Untested' else b['outcome']])
    return table(['Bet', 'Problem', 'Evidence', 'Hypothesis', 'Action', 'Success metric', 'Decision threshold', 'Next review', 'Outcome'], rows, ' class="trace"') + '<p class="axis-note">Every metric and threshold is a proposed hypothesis, not an industry benchmark. Outcomes stay "Not started" until real data exists.</p>'
def g_dashboard():
    counts, n = g_counts(); tot = len(D['status'])
    ver = max(x['verified'] for x in SRC); vol = [x for x in SRC if x['cadence'] == 'volatile']
    nextv = min(x['next'] for x in SRC); cv = max(x['verified'] for x in vol)
    due = [x for x in SRC if x['next'] <= datetime.date.today().isoformat()]
    decided = [d for d in D['decisions'] if d['status'] == 'Decided']; prop = [d for d in D['decisions'] if d['status'] == 'Proposed']
    last = max(decided, key=lambda d: (d['date'], d['id']))
    ms = ''.join(f'<li><a href="/docs/{m["link"]}">{esc(m["title"])}</a> {st(m["state"])}</li>' for m in D['milestones'])
    od = ''.join(f'<li><a href="/docs/{u}">{esc(t)}</a></li>' for t, u in D['open_decisions'])
    rk = ''.join(f'<li>{esc(a)}: <em>{esc(b)}</em></li>' for a, b in D['risks'])
    return f'''<section aria-labelledby="dash-h"><h2 id="dash-h">Founder dashboard</h2>
<p>Only facts with documented evidence are shown. Status as of <time datetime="{PG['updated']}">{PG['updated']}</time>. Source: <code>data/status.json</code> and <code>data/sources.json</code>.</p>
<div class="dash">
<div class="card"><h4>What TherapOS is</h4><p>An AI documentation and patient-memory tool for independent therapists. AI output is always a draft the clinician edits. <a href="/docs/plan.html#strategy">Strategy at a glance</a></p></div>
<div class="card"><h4>Initial customer {st('Proposed')}</h4><p>US independent therapists who already use AI and keep their own EHR. India deferred. <a href="/docs/competitors.html#s2">Why</a></p></div>
<div class="card"><h4>Product maturity</h4><div class="big">{n.get('Built',0)} of {tot} built</div><div class="counts">{counts}</div><p style="font-size:.8rem;margin-top:.6rem"><a href="/docs/case-study.html#status">Full status table</a></p></div>
<div class="card"><h4>Key hypothesis {ev('Hypothesis')}</h4><p>Source-linked, editable patient memory plus a strict no-retention posture earns repeat use and payment where AI notes alone do not. <a href="/docs/plan.html#bets">Bets</a></p></div>
<div class="card"><h4>Validated so far</h4><ul><li>Technical: draft parser has 7 passing unit tests {ev('Verified')}</li><li>Competitor scan, US and India, 26 Oct 2026 {ev('Verified')}</li><li><b>With users: nothing.</b></li></ul></div>
<div class="card"><h4>Unproven</h4><ul><li>Willingness to pay</li><li>Time saved per note</li><li>Clinician trust in summaries</li><li>Patient appetite for activities</li></ul></div>
<div class="card"><h4>Research freshness</h4><p>Latest verification <time datetime="{ver}">{ver}</time> across {len(SRC)} records; next check due <time datetime="{nextv}">{nextv}</time>{'' if not due else f' <span class="due">{len(due)} due</span>'}. <a href="/docs/sources.html">Source register</a></p></div>
<div class="card"><h4>Competitive review</h4><p>Prices and features last verified <time datetime="{cv}">{cv}</time>; volatile claims are re-checked every 30 days. <a href="/docs/competitors.html#s3">Competitors</a></p></div>
<div class="card"><h4>Customer discovery</h4><div class="big">{st('Not started')}</div><p style="font-size:.8rem;margin-top:.5rem">No interviews, pilots or willingness-to-pay data exist yet. <a href="/docs/competitors.html#s13">30-day plan</a></p></div>
<div class="card"><h4>Critical risks</h4><ul>{rk}</ul></div>
<div class="card"><h4>Next three milestones</h4><ul>{ms}</ul></div>
<div class="card"><h4>Decisions awaiting the founder</h4><ul>{od}</ul></div>
<div class="card"><h4>Last decision</h4><p><b>{last['id']}</b> {esc(last['title'])} <time datetime="{last['date']}">{last['date']}</time></p><p style="font-size:.8rem">{len(prop)} further proposals await confirmation. <a href="/docs/plan.html#decision-log">Decision log</a></p></div>
</div></section>
<h3>How to read these docs</h3>
<nav class="journey" aria-label="Reading order"><a href="/docs/plan.html">1 Product plan</a><span class="arrow" aria-hidden="true">→</span><a href="/docs/research.html">2 Market evidence</a><span class="arrow" aria-hidden="true">→</span><a href="/docs/competitors.html">3 Competitors</a><span class="arrow" aria-hidden="true">→</span><a href="/docs/case-study.html">4 Build evidence</a><span class="arrow" aria-hidden="true">→</span><a href="/docs/roadmap.html">5 Roadmap</a><span class="arrow" aria-hidden="true">→</span><a href="/docs/architecture.html">6 Technical</a></nav>
<div class="table-wrap" role="region" tabindex="0" aria-label="Where to start by audience"><table><thead><tr><th scope="col">If you are…</th><th scope="col">Start here</th></tr></thead><tbody>
<tr><td>Founder</td><td><a href="#dash-h">Dashboard</a> → <a href="/docs/plan.html#decision-log">Decision log</a> → <a href="/docs/competitors.html#s21">Decision memo</a></td></tr>
<tr><td>Engineer</td><td><a href="/docs/architecture.html">Architecture</a> → <a href="/docs/schema.html">Schema</a> → <a href="/docs/case-study.html#status">Honest status</a></td></tr>
<tr><td>Clinical advisor</td><td><a href="/docs/competitors.html#s10">Activities and safeguards</a> → <a href="/docs/research.html#regulation">Regulation</a> → <a href="/docs/ai.html">AI behavioural contract</a></td></tr>
<tr><td>Investor or partner</td><td><a href="/docs/competitors.html#s1">Executive summary</a> → <a href="/docs/competitors.html#s12">Market scenarios</a> → <a href="/docs/sources.html">Source register</a>. Nothing here is traction.</td></tr>
</tbody></table></div>'''
def g_compfresh():
    rows = [[x['id'], esc(x['claim'][:90]) + ('…' if len(x['claim']) > 90 else ''), x['verified'], f'<span data-next-verify="{x["next"]}">{x["next"]}</span>'] for x in SRC if x['id'].startswith('C-')]
    return table(['Record', 'Claim', 'Last verified', 'Next check'], rows) + '<p class="axis-note">Full records, URLs and limitations: <a href="/docs/sources.html">Source Register</a>. Re-check prices on each vendor page before quoting.</p>'
def g_researchfresh():
    c = {}
    for x in SRC: c[x['label']] = c.get(x['label'], 0) + 1
    chips = ' '.join(f'{ev(k)} <b>{v}</b>' for k, v in sorted(c.items()))
    return f'<p>{len(SRC)} tracked records: {chips}. Latest verification {max(x["verified"] for x in SRC)}. Legal records are re-checked every 90 days, competitor prices every 30, market statistics every 180. See the <a href="/docs/sources.html">Source Register</a>.</p>'
GEN = dict(counts=lambda: g_counts()[0], status=g_status, decisions=g_decisions, timeline=g_timeline, bets=g_bets, dashboard=g_dashboard, compfresh=g_compfresh, researchfresh=g_researchfresh)

def fill(s, name, content):
    pat = rf'<!--gen:{name}-->.*?<!--/gen:{name}-->'
    return re.sub(pat, lambda m: f'<!--gen:{name}-->{content}<!--/gen:{name}-->', s, flags=re.S)

# ---------- seeds (insert once) ----------
def apply_seeds():
    for page, name, where, pos, html_ in SEEDS:
        f = f'docs/{page}.html'; s = open(f).read()
        if f'<!--seed:{name}-->' in s: continue
        blk = f'<!--seed:{name}-->{html_}<!--/seed:{name}-->\n'
        m = re.search(where, s, flags=re.S)
        if not m: raise SystemExit(f'seed anchor not found: {page}/{name}: {where}')
        i = m.start() if pos == 'before' else m.end()
        s = s[:i] + blk + s[i:]
        open(f, 'w').write(s)

def toc_add(page, entries):
    f = f'docs/{page}.html'; s = open(f).read()
    for i, (aid, label, after) in enumerate(entries):
        if f'href="#{aid}"' in s.split('class="page-toc"')[-1]: continue
        link = f'    <a href="#{aid}">{label}</a>\n'
        if after and f'href="#{after}"' in s:
            s = re.sub(rf'(    <a href="#{after}"[^>]*>[^<]*</a>\n)', lambda m: m.group(1) + link, s, count=1)
        else:
            s = s.replace('<span class="toc-label">On this page</span>\n', '<span class="toc-label">On this page</span>\n' + link, 1)
    open(f, 'w').write(s)

# ---------- Source register page ----------
def sources_page():
    base = open('docs/competitors.html').read()
    pre = base[:base.index('<main')]; post = base[base.index('</main>') + 7:]
    pre = re.sub(r'<title>.*?</title>', '<title>Source Register — TherapOS Docs</title>', pre)
    pre = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="Every evidence record behind the TherapOS docs: source, dates, evidence label, limitations and next verification date.">', pre)
    groups = [('Competitors (verify every 30 days)', 'C-'), ('Market size and demand (180 days)', 'M-'), ('Regulation (90 days; counsel review required)', 'R-'), ('Research evidence', 'E-')]
    parts = []
    for title, pf in groups:
        rows = []
        for x in [y for y in SRC if y['id'].startswith(pf)]:
            aff = ' '.join(f'<a href="/docs/plan.html#{d.lower()}">{d}</a>' for d in x['decision']) or '—'
            rows.append([f'<b id="{x["id"].lower()}">{x["id"]}</b>', esc(x['claim']), f'<a href="{esc(x["url"])}">{esc(x["type"])}</a>', x['published'], f'<time datetime="{x["verified"]}">{x["verified"]}</time>', ev(x['label']), x['scope'], esc(x['limits']), aff, f'<span data-next-verify="{x["next"]}"><time datetime="{x["next"]}">{x["next"]}</time></span>'])
        parts.append(f'<h2 id="{pf.lower().strip("-")}-records">{title}</h2>' + table(['ID', 'Claim or finding', 'Source', 'Published', 'Last verified', 'Evidence', 'Scope', 'Limitations', 'Affects', 'Next check'], rows))
    body = f'''
    <span class="eyebrow">Evidence</span>
    <h1>Source Register</h1>
    <p class="page-desc">One maintained record for every market, competitor and regulatory claim the docs rely on. Pages cite records by ID, so a price or legal fact is updated in one place: <code>data/sources.json</code>.</p>
    <div class="callout callout-info"><div class="callout-icon">ℹ</div><div class="callout-body"><div class="callout-label">How this stays current</div>
    <p>Each record carries a cadence: <b>competitor prices and features every 30 days</b>, <b>legal and regulatory items every 90 days</b>, <b>market statistics every 180 days</b>. A "Review due" flag appears in your browser when a next-check date has passed. <b>Nothing monitors sources automatically.</b> Updating means: open the URL, confirm or correct the claim, change <code>verified</code> in the JSON, rerun <code>python3 tools/enhance.py &amp;&amp; python3 tools/build.py &amp;&amp; python3 tools/enhance.py &amp;&amp; python3 tools/check.py</code>.</p></div></div>
    <div class="legend" role="note" aria-label="Evidence labels"><p class="legend-title">Evidence labels</p><div>{ev('Verified')} primary source or documented implementation</div><div>{ev('Reported')} secondary or third-party</div><div>{ev('Inferred')} our reasoning</div><div>{ev('Hypothesis')} needs validation</div><div>{ev('Unknown')} not found</div></div>
    <p>Legal items are not legal advice. Records marked for counsel need professional review before any patient-facing release (<a href="/docs/plan.html#d13">D13</a>).</p>
    {''.join(parts)}
    <h2 id="gaps">Known research gaps</h2>
    <ul><li>No published time-per-note figure for therapists (<a href="#e-time">E-TIME</a>).</li><li>Private-practice share by profession; BLS excludes many self-employed.</li><li>TherapyNotes and several SimplePractice pages returned 403 to our fetch; those claims are Reported.</li><li>Upheal, Blueprint and Mentalyc client-facing features not tested hands-on.</li><li>India counts conflict; MyKaya, Cognixa, PsychDesk and PractiPal were not verifiable.</li><li>All statute texts for state AI laws were read through summaries, not the statutes.</li></ul>
    <div class="doc-nav"><a href="/docs/case-study.html" class="doc-nav-btn"><span class="doc-nav-label">← Previous</span><span class="doc-nav-title">Case Study</span></a><a href="/docs/index.html" class="doc-nav-btn next"><span class="doc-nav-label">Next →</span><span class="doc-nav-title">Overview</span></a></div>
  '''
    toc = ''.join(f'    <a href="#{p.lower().strip("-")}-records">{t.split(" (")[0]}</a>\n' for t, p in groups) + '    <a href="#gaps">Known research gaps</a>\n'
    open('docs/sources.html', 'w').write(pre + f'<main class="docs-content" id="main">\n{body}</main>\n\n  <aside class="page-toc">\n    <span class="toc-label">On this page</span>\n{toc}  </aside>\n</div>' + post[post.index('<footer'):] if '<footer' in post else pre + body + post)

def search_index():
    out = []
    for f in sorted(glob.glob('docs/*.html')):
        s = open(f).read(); sl = os.path.basename(f)[:-5]; title = html.unescape(re.sub(r'<[^>]+>', '', PG['titles'].get(sl, sl)))
        m = re.search(r'<main.*?</main>', s, flags=re.S); main = m.group(0) if m else s
        main = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', main, flags=re.S)
        parts = re.split(r'(<h[23][^>]*>.*?</h[23]>)', main, flags=re.S)
        out.append(dict(u=f'/docs/{sl}.html', t=title, h='', x=re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', parts[0])))[:600]))
        for i in range(1, len(parts), 2):
            h = parts[i]; idm = re.search(r'id="([^"]+)"', h)
            if not idm: continue
            txt = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', parts[i + 1] if i + 1 < len(parts) else '')))
            out.append(dict(u=f'/docs/{sl}.html#{idm.group(1)}', t=title, h=html.unescape(re.sub(r'<[^>]+>', '', h)).strip(), x=txt[:1600]))
    json.dump(out, open('search-index.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    return len(out)

if __name__ == '__main__':
    sources_page()
    apply_seeds()
    for f in sorted(glob.glob('docs/*.html')):
        s = open(f).read(); o = s
        for name, fn in GEN.items():
            if f'<!--gen:{name}-->' in s: s = fill(s, name, fn())
        if s != o: open(f, 'w').write(s)
    from seeds import TOC
    for page, entries in TOC.items(): toc_add(page, entries)
    print('sources:', len(SRC), '| search entries:', search_index())
