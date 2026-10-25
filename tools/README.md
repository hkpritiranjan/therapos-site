# Docs maintenance

The site is static HTML with no build framework. Three small scripts keep it consistent.

| File | Role |
|---|---|
| `data/sources.json` | One record per market, competitor or legal claim (URL, dates, evidence label, limitations, cadence). Edit prices and legal facts **here**. |
| `data/status.json` | Product status items, decisions (D01…), strategic bets, milestones, open decisions, risks. |
| `data/pages.json` | Navigation, page roles and the reading journey. |
| `tools/enhance.py` | Idempotent page chrome: heading ids, sidebar, breadcrumbs, search button, legends, table regions. |
| `tools/build.py` | Renders `<!--gen:NAME-->` blocks and `docs/sources.html` from the data files and rebuilds `search-index.json`. |
| `tools/check.py` | Fails on broken links or anchors, duplicate ids, heading jumps, legacy labels, unknown source ids. |

Run after any change:

    python3 tools/enhance.py && python3 tools/build.py && python3 tools/enhance.py && python3 tools/check.py

## Routine
- **Every 30 days:** open each `C-*` record URL, confirm or correct price and features, set `verified` to today.
- **Every 90 days:** the same for `R-*` (legal) records; legal items need counsel review before patient-facing use.
- **Every 180 days:** `M-*` market statistics.
- Nothing monitors sources automatically. A "Review due" flag shows in the browser once a next-check date passes.
- `seed:` blocks are inserted once and then hand-edited in the page; `gen:` blocks are overwritten on every build.
- Add a decision to `data/status.json` when strategy changes; it appears in the plan's decision log, the case-study timeline and the dashboard.
