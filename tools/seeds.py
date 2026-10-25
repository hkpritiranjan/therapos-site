"""One-time seed content. build.py inserts each block once (by marker); after that, edit it in the page itself.
Generated blocks (<!--gen:NAME-->) inside seeds are re-rendered from data/*.json on every build."""
EV = lambda l: f'<span class="ev ev-{l.lower()}">{l}</span>'
ST = lambda l: f'<span class="st st-{l.lower().replace(" ", "-")}">{l}</span>'

PLAN_TOP = f'''<h2 id="strategy">Strategy at a glance</h2>
<p>A one-screen summary. Strategic intent is labelled separately from validated fact; nothing in this block is validated with users yet.</p>
<div class="strategy-grid">
<div class="card"><h4>Customer problem {EV('Inferred')}</h4><p>Independent therapists write progress notes and re-read old notes before sessions, with little continuity between sessions. How much time this costs is unmeasured.</p></div>
<div class="card"><h4>Initial segment {ST('Proposed')}</h4><p>US independent therapists (LCSW, LMFT, LPC, counselling psychologists) who already use AI and keep their own EHR. India is deferred. <a href="/docs/competitors.html#s2">Rationale</a></p></div>
<div class="card"><h4>Core workflow {ST('Built')}</h4><p>Type or dictate raw notes, receive an editable SOAP, DAP or BIRP draft, edit and finalise, and the client summary updates for the next session's prep brief. Sessions are never recorded.</p></div>
<div class="card"><h4>Proposed differentiation {EV('Hypothesis')}</h4><p>Inspectable, source-linked client memory with a strict no-retention posture. Not price, not "AI notes": both are commodity. <a href="/docs/competitors.html#s7">Assessment</a></p></div>
<div class="card"><h4>Business model {EV('Hypothesis')}</h4><p>Solo plan $29 per month (200 AI notes, 30-day trial); clinic plan $49 per seat later. Scenario ARR $63k to $1.6M. <a href="/docs/competitors.html#s12">Model</a>, <a href="/docs/pricing.html">pricing</a></p></div>
<div class="card"><h4>Most important assumptions</h4><p>Therapists will pay for memory and prep beyond free note tools; they will trust a new vendor with client data; text-first matters to buyers; patient-facing features are legally viable.</p></div>
<div class="card"><h4>Next decision for the founder</h4><p>Confirm the first segment and approve the 30-day discovery sprint (<a href="/docs/plan.html#d09">D09</a>). Then choose the BAA route (<a href="/docs/plan.html#d14">D14</a>).</p></div>
</div>
<h2 id="status-glance">Product status at a glance</h2>
<p><!--gen:counts--><!--/gen:counts--> The complete, evidence-referenced table is in the <a href="/docs/case-study.html#status">Case Study</a>. Anything not marked Built is not in the product today.</p>
<h2 id="roadmap-glance">Roadmap at a glance</h2>
<ol class="timeline" aria-label="Roadmap horizons">
<li><time>Months 0 to 3</time><b>Validate the foundation</b> {ST('Planned')} login and register, pseudonymised AI calls, BAA path, 30-day discovery sprint, 10-clinician pilot.</li>
<li><time>Months 4 to 6</time><b>Retention and workflow fit</b> {ST('Planned')} source-linked summaries, copy-to-EHR export, addenda, minimal goal tracking, search.</li>
<li><time>Months 7 to 12</time><b>Clinician–patient collaboration</b> {ST('Exploratory')} secure-link activities and reflections, only if discovery, counsel opinion and BAA path allow.</li>
<li><time>Months 13 to 24</time><b>Selective expansion</b> {ST('Deferred')} clinic accounts, SOC 2 readiness, India on pull.</li>
</ol>
<p>Detail, entry conditions and feature table: <a href="/docs/competitors.html#s15">Competitors §15</a>. Public roadmap: <a href="/docs/roadmap.html">Roadmap</a>.</p>
<h2 id="bets">Strategic bets and traceability</h2>
<p>Each bet traces from evidence (source-register IDs) to a hypothesis, action, metric, threshold and review date. All are untested.</p>
<!--gen:bets--><!--/gen:bets-->
'''
PLAN_LOG = '''<h2 id="decision-log">Decision log</h2>
<p>Newest first. <b>Decided</b> means the founder accepted it; <b>Proposed</b> means it is our recommendation, awaiting confirmation. Evidence IDs link to the <a href="/docs/sources.html">Source Register</a>.</p>
<!--gen:decisions--><!--/gen:decisions-->
'''
RESEARCH_EXEC = f'''<h2 id="exec">Research executive summary</h2>
<ul>
<li><b>Demand is rising, but evidence is thin.</b> APA reports 56% of psychologists used AI at least once in the past year and 29% monthly {EV('Reported')} (<a href="/docs/sources.html#m-apa25">M-APA25</a>); this covers psychologists only.</li>
<li><b>The documentation-burden statistics were removed.</b> No reliable per-note time figure was found {EV('Unknown')} (<a href="/docs/sources.html#e-time">E-TIME</a>).</li>
<li><b>The market supports a small business.</b> 150,000 to 400,000 independent therapy clinicians is our own range {EV('Hypothesis')} (<a href="/docs/sources.html#m-ind">M-IND</a>).</li>
<li><b>Regulation constrains patient-facing AI.</b> Illinois and Nevada restrict AI delivering care; none of it is legal advice (<a href="/docs/sources.html#r-il">R-IL</a>, <a href="/docs/sources.html#r-nv">R-NV</a>).</li>
<li><b>TherapOS holds no compliance attestations.</b> No BAAs, SOC 2 or HIPAA/DPDP compliance claims are made or supported {EV('Verified')} (<a href="/docs/sources.html#r-baa">R-BAA</a>).</li>
</ul>
<!--gen:researchfresh--><!--/gen:researchfresh-->
<h3 id="evidence-decisions">How evidence feeds decisions</h3>
<div class="table-wrap" role="region" tabindex="0" aria-label="Table: How evidence feeds decisions"><table><thead><tr><th scope="col">Finding</th><th scope="col">Evidence</th><th scope="col">Decision it affects</th></tr></thead><tbody>
<tr><td>Competitors have cross-session features; AI notes are free or cheap</td><td><a href="/docs/sources.html#c-uph">C-UPH</a>, <a href="/docs/sources.html#c-men">C-MEN</a>, <a href="/docs/sources.html#c-car">C-CAR</a></td><td><a href="/docs/plan.html#d04">D04</a>, <a href="/docs/plan.html#d12">D12</a></td></tr>
<tr><td>Therapists already adopting AI</td><td><a href="/docs/sources.html#m-apa25">M-APA25</a></td><td><a href="/docs/plan.html#d09">D09</a></td></tr>
<tr><td>Small independent pool; India pool uncountable</td><td><a href="/docs/sources.html#m-ind">M-IND</a>, <a href="/docs/sources.html#m-rci">M-RCI</a></td><td><a href="/docs/plan.html#d09">D09</a></td></tr>
<tr><td>State laws limit AI in therapy; Woebot consumer app closed</td><td><a href="/docs/sources.html#r-il">R-IL</a>, <a href="/docs/sources.html#r-nv">R-NV</a>, <a href="/docs/sources.html#e-woe">E-WOE</a></td><td><a href="/docs/plan.html#d10">D10</a>, <a href="/docs/plan.html#d13">D13</a></td></tr>
<tr><td>Homework evidence is correlational</td><td><a href="/docs/sources.html#e-hw">E-HW</a></td><td><a href="/docs/plan.html#d10">D10</a></td></tr>
<tr><td>No BAAs; vendor BAAs need zero-retention eligibility</td><td><a href="/docs/sources.html#r-baa">R-BAA</a></td><td><a href="/docs/plan.html#d05">D05</a>, <a href="/docs/plan.html#d14">D14</a></td></tr>
</tbody></table></div>
'''
RESEARCH_REQ = f'''<h3 id="requirement-types">What kind of statement is each item?</h3>
<p>Do not read recommendations as legal requirements. Items marked for counsel need professional review.</p>
<div class="table-wrap" role="region" tabindex="0" aria-label="Table: Requirement types"><table><thead><tr><th scope="col">Item</th><th scope="col">Type</th><th scope="col">Jurisdiction</th><th scope="col">Source</th></tr></thead><tbody>
<tr><td>Business associate agreement with vendors handling PHI</td><td>Legal requirement (HIPAA) for covered entities and business associates</td><td>US</td><td><a href="/docs/sources.html#r-baa">R-BAA</a></td></tr>
<tr><td>Psychotherapy notes defined and excluded from patient access</td><td>Legal requirement; application to our features needs counsel</td><td>US</td><td><a href="/docs/sources.html#r-hip">R-HIP</a></td></tr>
<tr><td>Limits on AI delivering therapy; written consent to record</td><td>Legal requirement in Illinois and Nevada; scope needs counsel</td><td>US-IL, US-NV</td><td><a href="/docs/sources.html#r-il">R-IL</a>, <a href="/docs/sources.html#r-nv">R-NV</a></td></tr>
<tr><td>DPDP Rules obligations from 13 May 2027</td><td>Legal requirement</td><td>India</td><td><a href="/docs/sources.html#r-dpdp">R-DPDP</a></td></tr>
<tr><td>Confidentiality and client access to records</td><td>Legal requirement (Mental Healthcare Act); AI application unclear</td><td>India</td><td><a href="/docs/sources.html#r-mhca">R-MHCA</a></td></tr>
<tr><td>Pseudonymise names before AI calls</td><td>Recommended practice and our design decision {ST('Planned')}</td><td>Both</td><td><a href="/docs/plan.html#d14">D14</a></td></tr>
<tr><td>SOC 2 attestation</td><td>Voluntary market expectation, not a legal requirement</td><td>US</td><td>{EV('Inferred')}</td></tr>
<tr><td>Zero-retention AI endpoints</td><td>Vendor condition for a BAA</td><td>US</td><td><a href="/docs/sources.html#r-baa">R-BAA</a></td></tr>
<tr><td>Patient-facing activity features are lawful</td><td>Open question requiring counsel; not asserted</td><td>US states</td><td><a href="/docs/plan.html#d13">D13</a></td></tr>
</tbody></table></div>
'''
COMP_FRESH = '''<details class="evidence"><summary>Verification dates for every competitor record (expand)</summary>
<p>Prices and features were last verified on 26 October 2026. Re-verify before quoting; volatile claims are due every 30 days.</p>
<!--gen:compfresh--><!--/gen:compfresh--></details>
'''
COMP_QUAD = f'''<h3 id="positioning-map">Positioning map (qualitative)</h3>
<p>Placement is drawn from vendor marketing pages, not scored or measured. Products appear only where their own pages support the placement.</p>
<figure class="chart" role="group" aria-labelledby="quad-cap">
<div class="quad">
<div><div class="quad-title">Documentation-led · recording-led</div>Freed, Heidi, JotPsych, Eleos, SimplePractice Note Taker, Carepatron scribe</div>
<div><div class="quad-title">Documentation-led · accepts typed input (none leads with it)</div>Upheal free tier, Mentalyc, Twofold accept typed or dictated input<div class="me"><b>TherapOS today</b></div></div>
<div><div class="quad-title">Longitudinal · recording-based</div>Blueprint, Upheal, Mentalyc, Berries (memory or prep claims); Nextvisit (psychiatry timeline); SimplePractice Care Aide and TherapyNotes Session Assist (EHR-locked)</div>
<div class="me"><div class="quad-title">Longitudinal · text-first</div>No vendor found leading with this. <b>TherapOS target.</b></div>
</div>
<figcaption id="quad-cap">Rows: documentation-led (top) versus longitudinal care (bottom). Columns: recording-led (left) versus text-first (right). An empty quadrant can mean nobody wants it. Text equivalent: <a href="#s6">section 6 table</a>.</figcaption></figure>
'''
COMP_VULN = f'''<h2 id="vulnerabilities">TherapOS's own weaknesses</h2>
<p>Where we are exposed, stated plainly. Status labels refer to the <a href="/docs/case-study.html#status">status table</a>.</p>
<div class="table-wrap" role="region" tabindex="0" aria-label="Table: TherapOS weaknesses"><table><thead><tr><th scope="col">Weakness</th><th scope="col">Evidence</th><th scope="col">Status</th><th scope="col">Mitigation</th></tr></thead><tbody>
<tr><td>No BAAs, SOC 2 or MFA; rivals publish SOC 2 and sign BAAs at signup</td><td>Own status {EV('Verified')}; <a href="/docs/sources.html#c-men">C-MEN</a>, <a href="/docs/sources.html#c-uph">C-UPH</a></td><td>{ST('Planned')}</td><td>BAA route (<a href="/docs/plan.html#d14">D14</a>), then SOC 2 readiness</td></tr>
<tr><td>Client names are sent to the AI model without pseudonymisation</td><td>Own status {EV('Verified')}</td><td>{ST('Planned')}</td><td>Pseudonymise before pilot</td></tr>
<tr><td>Web app has no login page or production token handling</td><td>Own status {EV('Verified')}</td><td>{ST('In progress')}</td><td>Build before any pilot</td></tr>
<tr><td>No EHR export; notes must be re-typed or copied by hand</td><td>Own status {EV('Verified')}</td><td>{ST('Planned')}</td><td>Copy-to-EHR (bet B3)</td></tr>
<tr><td>Memory and search are partial; no provenance links</td><td>Own status {EV('Verified')}</td><td>{ST('In progress')}</td><td>Source-linked summaries (bet B1)</td></tr>
<tr><td>Audit table exists but nothing writes to it</td><td>Own status {EV('Verified')}</td><td>{ST('Planned')}</td><td>Write audit events before pilot</td></tr>
<tr><td>Tests cover only the draft parser; no isolation or note-locking tests</td><td>Own status {EV('Verified')}</td><td>{ST('In progress')}</td><td>API and tenant tests before pilot</td></tr>
<tr><td>No user evidence; value and willingness to pay unproven</td><td>Own status {EV('Verified')}</td><td>{ST('Not started')}</td><td>30-day discovery sprint</td></tr>
<tr><td>Text-first is easy to copy; price offers no edge</td><td><a href="/docs/sources.html#c-uph">C-UPH</a>, <a href="/docs/sources.html#c-car">C-CAR</a> {EV('Verified')}</td><td>{EV('Inferred')}</td><td>Differentiate on provenance and privacy architecture</td></tr>
<tr><td>Single-vendor AI dependency (GPT-4o hard-coded); docs describe Claude</td><td>Own status {EV('Verified')}</td><td>{ST('Planned')}</td><td>Decide model route with the BAA decision</td></tr>
</tbody></table></div>
'''
COMP_CHART = f'''<figure class="chart" role="group" aria-labelledby="arr-cap">
<svg viewBox="0 0 640 230" role="img" aria-labelledby="arr-t arr-d"><title id="arr-t">US annual recurring revenue scenarios</title><desc id="arr-d">Conservative $63 thousand with 261 seats, base $348 thousand with 1,160 seats, optimistic $1.61 million with 4,640 seats. Model outputs, not forecasts.</desc>
<g font-family="system-ui,sans-serif" font-size="13" fill="#1F1340">
<text x="0" y="22" font-weight="700">Conservative · 261 seats</text><rect x="0" y="30" width="{max(4,round(63/1615*430))}" height="26" rx="5" fill="#A9A6F5"/><text x="{max(4,round(63/1615*430))+8}" y="49">$63k</text>
<text x="0" y="90" font-weight="700">Base · 1,160 seats</text><rect x="0" y="98" width="{round(348/1615*430)}" height="26" rx="5" fill="#5B4BE0"/><text x="{round(348/1615*430)+8}" y="117">$348k</text>
<text x="0" y="158" font-weight="700">Optimistic · 4,640 seats</text><rect x="0" y="166" width="430" height="26" rx="5" fill="#070C56"/><text x="438" y="185">$1.61M</text>
</g></svg>
<figcaption id="arr-cap">US ARR scenarios from the formula above ({EV('Hypothesis')}). Linear scale. These are model outputs from assumed inputs, not forecasts; the table above is the text alternative.</figcaption></figure>
'''
COMP_FLOW = '''<h3 id="decision-flow">Decision flow</h3>
<div class="flow">
<div class="card"><h4>Continue</h4><ul><li>≥8 of 15 therapists show pain unprompted</li><li>≥6 of 10 pilot clinicians weekly-active</li><li>≥5 of 15 commit at ≥$25</li><li>Users cite memory or privacy, not price</li></ul></div>
<div class="card pivot"><h4>Pivot</h4><ul><li>Use is notes-only: become a niche export or scribe tool</li><li>Pay only at ≤$19: rework unit economics</li><li>Clinicians want assignments but not patient replies: drop reflections</li></ul></div>
<div class="card stop"><h4>Stop or defer</h4><ul><li>Most say existing tools are enough</li><li>Fewer than 3 weekly users</li><li>Nobody commits at ≥$15</li><li>Compliance cost exceeds plausible ARR</li></ul></div>
</div>
<p class="axis-note">Thresholds are proposed hypotheses; full table above. Reviewed at the end of the 30-day sprint.</p>
<h3 id="bets">Strategic bets: evidence to outcome</h3>
<!--gen:bets--><!--/gen:bets-->
'''
CS_DEC = '''<h3 id="decision-timeline">Decision timeline</h3>
<p>Chronological. Full rationale and evidence: <a href="/docs/plan.html#decision-log">Decision log</a>.</p>
<!--gen:timeline--><!--/gen:timeline-->
'''
CS_SEC = f'''<h2 id="security">Security and compliance status</h2>
<p>As of 26 October 2026. TherapOS makes no HIPAA, DPDP, SOC 2 or clinical-validation claim.</p>
<div class="table-wrap" role="region" tabindex="0" aria-label="Table: Security and compliance status"><table><thead><tr><th scope="col">Control</th><th scope="col">Status</th><th scope="col">Evidence</th></tr></thead><tbody>
<tr><td>Email and password authentication with JWT</td><td>{ST('In progress')}</td><td>API implemented; web app lacks a login page</td></tr>
<tr><td>Per-clinician data isolation</td><td>{ST('Built')}</td><td>Enforced in the service layer; no automated test yet</td></tr>
<tr><td>Audit log</td><td>{ST('Planned')}</td><td>Table exists; nothing writes to it</td></tr>
<tr><td>Field-level encryption, MFA, rate limits</td><td>{ST('Planned')}</td><td>Not implemented</td></tr>
<tr><td>CORS and secrets configured from environment</td><td>{ST('Planned')}</td><td>Open item from the <a href="/docs/review.html">product review</a></td></tr>
<tr><td>Pseudonymise client names before AI calls</td><td>{ST('Planned')}</td><td>Not implemented; names currently reach the model</td></tr>
<tr><td>Business associate agreements</td><td>{ST('Planned')}</td><td>None executed (<a href="/docs/sources.html#r-baa">R-BAA</a>)</td></tr>
<tr><td>SOC 2, HIPAA or DPDP compliance</td><td>{ST('Planned')}</td><td>Not started and not claimed</td></tr>
</tbody></table></div>
<h2 id="testing">Testing and validation evidence</h2>
<div class="table-wrap" role="region" tabindex="0" aria-label="Table: Testing evidence"><table><thead><tr><th scope="col">Check</th><th scope="col">Result</th><th scope="col">Evidence label</th></tr></thead><tbody>
<tr><td>Draft parser unit tests (<code>npm test</code> in <code>apps/web</code>)</td><td>7 tests pass: JSON, fenced JSON, DAP and BIRP mapping, partial streams, prose fallback, free text, stream preview</td><td>{EV('Verified')}</td></tr>
<tr><td>Type check and production build (25 Oct 2026)</td><td><code>tsc</code> clean; <code>next build</code> passes</td><td>{EV('Verified')}</td></tr>
<tr><td>Live model output through the parser</td><td>One manual run parsed four SOAP fields; not automated</td><td>{EV('Verified')}</td></tr>
<tr><td>Text contrast (WCAG AA 4.5:1)</td><td>Body text minimum 5.03:1 on the shared palette; computed, not screen-reader tested</td><td>{EV('Verified')}</td></tr>
<tr><td>Docs link, anchor and heading checks (<code>tools/check.py</code>)</td><td>Run on every build of these docs</td><td>{EV('Verified')}</td></tr>
<tr><td>API tests, tenant isolation, note locking</td><td>None written</td><td>{ST('Planned')}</td></tr>
<tr><td>User testing with clinicians or patients</td><td>None done</td><td>{ST('Not started')}</td></tr>
</tbody></table></div>
<h2 id="beta-template">Beta evidence template</h2>
<p>Empty until a pilot runs. When it does, report the number of participants beside every figure, and never show a percentage without its denominator.</p>
<div class="table-wrap" role="region" tabindex="0" aria-label="Table: Beta evidence template"><table><thead><tr><th scope="col">Field</th><th scope="col">Value</th></tr></thead><tbody>
<tr><td>Cohort and recruitment method</td><td>{ST('Not started')}</td></tr>
<tr><td>Participants (n) and dates</td><td>—</td></tr>
<tr><td>Method (observed sessions, diary, interviews)</td><td>—</td></tr>
<tr><td>Observed behaviour (unprompted weekly use, edits to drafts, source-link opens)</td><td>—</td></tr>
<tr><td>Measured outcomes (time per note, with the measurement method)</td><td>—</td></tr>
<tr><td>Willingness to pay (commitments, not stated intent)</td><td>—</td></tr>
<tr><td>Limitations and bias</td><td>—</td></tr>
</tbody></table></div>
<h2 id="update-log">Update log</h2>
<div class="table-wrap" role="region" tabindex="0" aria-label="Table: Update log"><table><thead><tr><th scope="col">Date</th><th scope="col">Change</th></tr></thead><tbody>
<tr><td>2026-10-26</td><td>Added decision log, shared evidence and status labels, source register, founder dashboard and navigation search.</td></tr>
<tr><td>2026-10-25</td><td>Corrected unsupported claims; draft-parser fix; app restyle; pricing decisions applied.</td></tr>
</tbody></table></div>
'''
INDEX_DASH = '<!--gen:dashboard--><!--/gen:dashboard-->\n'

SEEDS = [
 ('plan', 'plan-top', r'<h2 id="1-product-vision">', 'before', PLAN_TOP),
 ('plan', 'plan-log', r'<div class="doc-nav">', 'before', PLAN_LOG),
 ('research', 'research-exec', r'<h2 id="summary">', 'before', RESEARCH_EXEC),
 ('research', 'research-req', r'<h2 id="regulation">.*?</h2>', 'after', RESEARCH_REQ),
 ('competitors', 'comp-fresh', r'<h2 id="s3">.*?</h2>', 'after', COMP_FRESH),
 ('competitors', 'comp-quad', r'<h2 id="s7">', 'before', COMP_QUAD),
 ('competitors', 'comp-vuln', r'<h2 id="s8">', 'before', COMP_VULN),
 ('competitors', 'comp-chart', r'<h3 id="reconciling-with-the-existing-plan">', 'before', COMP_CHART),
 ('competitors', 'comp-flow', r'<h2 id="s15">', 'before', COMP_FLOW),
 ('case-study', 'cs-dec', r'<h2 id="status">', 'before', CS_DEC),
 ('case-study', 'cs-sec', r'<h2 id="risks">', 'before', CS_SEC),
 ('index', 'index-dash', r'<p class="page-desc">.*?</p>', 'after', INDEX_DASH),
]
TOC = {
 'plan': [('strategy', 'Strategy at a glance', None), ('bets', 'Strategic bets', 'strategy'), ('decision-log', 'Decision log', '40-five-year-vision')],
 'research': [('exec', 'Executive summary', None)],
 'competitors': [('vulnerabilities', 'TherapOS weaknesses', 's7'), ('bets', 'Strategic bets', 's14')],
 'case-study': [('security', 'Security status', 'status'), ('testing', 'Testing evidence', 'security'), ('beta-template', 'Beta template', 'testing'), ('update-log', 'Update log', 'lessons')],
 'index': [('dash-h', 'Founder dashboard', None)],
}
