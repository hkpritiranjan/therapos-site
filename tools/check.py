#!/usr/bin/env python3
"""Site checks: internal links, anchors, duplicate ids, heading order, label vocabulary,
source-register references, generated-block markers. Exit 1 on any failure."""
import re, glob, os, json, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
files = sorted(glob.glob('docs/*.html')) + ['index.html']
src = {x['id'] for x in json.load(open('data/sources.json'))}
st = json.load(open('data/status.json'))
ids = {f: re.findall(r'\sid="([^"]+)"', open(f).read()) for f in files}
errs = []; warns = []
def resolve(f, h):
    p, _, a = h.partition('#')
    if p.startswith('/'): t = p[1:]
    elif p: t = os.path.normpath(os.path.join(os.path.dirname(f), p))
    else: t = f
    if t in ('', '/'): t = 'index.html'
    if t == 'docs': t = 'docs/index.html'
    for c in (t, t + '.html'):
        if os.path.isfile(c): return c, a
    return None, a
for f in files:
    s = open(f).read()
    dup = {i for i in ids[f] if ids[f].count(i) > 1}
    if dup: errs.append(f'{f}: duplicate ids {sorted(dup)[:5]}')
    for h in re.findall(r'<a [^>]*href="([^"]*)"', s):
        if h.startswith(('http', 'mailto:', 'data:', 'tel:')) or h in ('#',): continue
        t, a = resolve(f, h)
        if t is None: errs.append(f'{f}: broken link {h}')
        elif a and a not in ids[t]: errs.append(f'{f}: broken anchor {h}')
    if re.search(r'<a [^>]*href="#"', s): warns.append(f'{f}: {len(re.findall(chr(60)+"a [^>]*href="+chr(34)+"#"+chr(34), s))} placeholder href="#" (waitlist URL not set)')
    s2 = re.sub(r'(<(?:div|a)\b[^>]*class="card[^>]*>\s*)<h4[^>]*>.*?</h4>', r'\1', s, flags=re.S)
    lv = [int(x) for x in re.findall(r'<h([1-6])[ >]', s2)]
    for a, b in zip(lv, lv[1:]):
        if b > a + 1: errs.append(f'{f}: heading jump h{a}->h{b}'); break
    if lv.count(1) != 1 and f != 'index.html': errs.append(f'{f}: {lv.count(1)} h1 elements')
    for old in ('badge badge-green">Confirmed', 'badge badge-red">Unverified'):
        if old in s: errs.append(f'{f}: legacy label {old}')
    for r in re.findall(r'data-src="([^"]+)"', s):
        for x in r.split(','):
            if x not in src: errs.append(f'{f}: unknown source id {x}')
    for m in re.findall(r'<!--gen:([a-z-]+)-->', s):
        if f'<!--/gen:{m}-->' not in s: errs.append(f'{f}: unclosed gen block {m}')
    if f.startswith('docs/') and 'id="main"' not in s: errs.append(f'{f}: no #main landmark')
    for tag in re.findall(r'<img [^>]*>', s):
        if 'alt=' not in tag: errs.append(f'{f}: img without alt')
for d in st['decisions']:
    for x in d.get('src', []):
        if x not in src: errs.append(f'decision {d["id"]}: unknown source {x}')
for b in st['bets']:
    for x in b['evidence']:
        if x not in src: errs.append(f'bet {b["id"]}: unknown source {x}')
print(f'{len(files)} pages checked, {len(errs)} problem(s)')
for e in errs[:80]: print(' -', e)
for w in warns: print(' WARN', w)
sys.exit(1 if errs else 0)
