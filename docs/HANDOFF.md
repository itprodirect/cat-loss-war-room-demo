# CAT-Loss War Room — Handoff Document

**Start here.** This is the canonical orientation for anyone picking up this repo — whether you're a coding agent, a developer, or a non-technical professional evaluating what this tool does.

---

## 1. What This Repo Is

The CAT-Loss War Room is an AI-powered research accelerator for catastrophic insurance loss litigation. An attorney enters a case (hurricane, carrier, location, posture) and the system produces a structured research package — weather corroboration, carrier denial patterns, relevant case law, citation spot-checks — exported as a markdown memo with source confidence badges. It is **not legal advice**. It is a starting point that saves hours of manual research.

## 2. Demo Promise

Given a case intake (e.g. Hurricane Milton / Citizens Property Insurance / Pinellas County FL):

- In **under 10 seconds** (cached) or **~60 seconds** (live), the notebook produces:
  - Weather corroboration with .gov source preference and extracted metrics
  - Carrier document pack with denial patterns, regulatory signals, and rebuttal angles
  - Case law organized by legal issue with citation spot-checks
  - A full markdown research memo exported to `output/`

- The demo runs **offline** from committed cache samples. No API key required on first clone.

## 3. Current Status

| Item | Status |
|------|--------|
| Cells 0–7 (full pipeline) | Working |
| Offline demo (USE_CACHE=true) | Working |
| Tests | 75 passing, 0 network calls |
| Cache samples (Milton/Citizens/Pinellas) | Committed |
| Codex review patches (P0/P1/P2) | Applied |
| Memo export | Working |
| Tag `v0-demo` | Exists |

## 4. How to Run

### Offline Demo (no API key)

```bash
git clone <repo-url> && cd cat-loss-war-room-demo
python -m venv .venv
source .venv/bin/activate        # Windows Git Bash: source .venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env             # USE_CACHE=true is the default

# Register Jupyter kernel (one-time)
python -m pip install ipykernel
python -m ipykernel install --user --name cat-loss-war-room-demo --display-name "cat-loss-war-room-demo (.venv)"

# Run
jupyter notebook notebooks/01_case_war_room.ipynb
# Select kernel: cat-loss-war-room-demo (.venv)
# Run All — should complete in < 10 seconds
```

### Live Mode (with Exa API key)

```bash
# Edit .env:
#   EXA_API_KEY=your_key_here
#   USE_CACHE=false

# Costs ~$0.30-0.50 per case run (~25-30 Exa API calls)
# Results are cached in cache/ for subsequent runs
```

### Re-seed Cache Samples

```bash
# After running live, capture results for offline demo:
python scripts/seed_cache_samples.py
git add cache_samples/ && git commit -m "chore: reseed cache samples"
```

## 5. Architecture in 60 Seconds

```
CaseIntake → QueryPlan (12-18 queries) → [Weather | Carrier | CaseLaw] → CitationVerify → Export
```

| Component | File | What It Does |
|-----------|------|-------------|
| Cache layer | `cache_io.py` | cache_samples/ → cache/ → live API. Demo never hits network. |
| Exa wrapper | `exa_client.py` | Single entry point for all network calls. Retry + budget guard (40 calls max). |
| Source scoring | `source_scoring.py` | Deterministic domain classification: 🟢 official / 🟡 professional / 🔴 unvetted / 🔒 paywalled |
| Query plan | `query_plan.py` | CaseIntake dataclass + generates targeted queries by module |
| Weather | `weather_module.py` | Gov-first search, regex metric extraction (wind/surge/rain) |
| Carrier | `carrier_module.py` | Denial patterns, DOI complaints, rebuttal angle generation |
| Case law | `caselaw_module.py` | Issue-organized results, case-like filter, paywalled exclusion |
| Citation check | `citation_verify.py` | One search per citation, best-tier selection, MAX_CHECKS=6 cap |
| Export | `export_md.py` | Full markdown memo with watermarks, source appendix, methodology |
| Notebook | `notebooks/01_case_war_room.ipynb` | 8 cells (title → config → intake → query plan → weather → carrier → caselaw+cite → export) |

## 6. What We Fixed (Codex Review)

- **P0 — Non-case pages in caselaw pack.** Added `_is_case_like()` filter. Only actual cases (with citations or case-name patterns) make it through.
- **P1 — Citation verify budget waste.** Skip blank citations, search k=5 (not 3), pick best-tier hit, cap at 6 checks. Errors return "uncertain" not "not found."
- **P2 — Hostname normalization bug.** `lstrip("www.")` mangled domains. Fixed with `removeprefix("www.")`. Added flcourts.gov + courtlistener.com.
- **P1 — Seed script fragility.** Budget headroom 30→40, overwrite stale fixtures, filter copy to relevant prefixes.
- **Kernel mismatch.** Notebook ran against system Python. Fixed with ipykernel registration.

## 7. Known Limitations / Deferred

- **Export timestamps are non-deterministic.** `datetime.now()` in memo header. Not blocking — it's a draft artifact. Fix when we add export snapshot tests.
- **Notebook cwd assumption.** `ROOT = Path(".").resolve().parent` works from `notebooks/` but is fragile. Fix if demo dry-run fails from a different working directory.
- **Citation verification is spot-check only.** One Exa search per citation. Not a substitute for KeyCite/Shepardize. All outputs carry disclaimers.
- **Single fact pattern cached.** Only Milton/Citizens/Pinellas is seeded. Additional patterns (TX Hail, Hurricane Ida) need live Exa runs + reseed.
- **No firm memory yet.** Planned for Phase 3 — JSON-based memory that makes the tool "learn" across cases.
- **No PDF export.** Markdown only. PDF is a Phase 3+ stretch goal.

## 8. Roadmap

### Phase 3 — Firm Memory + Polish
- Firm Memory Lite: JSON load/save, pre-seeded demo entries (Citizens, FL experts)
- Cache all 3 fact patterns (Milton, TX Hail, Ida)
- Demo hardening: graceful degradation, timing targets (<10s cached)
- Final README + DEMO_SCRIPT update with actual outputs

### Phase 4 — Stretch
- Expert Finder module
- Depo/EUO Question Bank
- PDF export (weasyprint)
- Policy Language Checklist
- Timeline Builder

## 9. Live Eval Lane

A separate evaluation workflow lives on branch `feat/live-eval`. It lets us
run the pipeline against public/redacted scenarios and record quality metrics
**without touching the canonical demo notebook**.

- **Docs:** [`docs/LIVE_EVAL.md`](LIVE_EVAL.md)
- **Intake rules:** [`eval/README.md`](../eval/README.md)
- **Notebook:** `notebooks/live_eval.ipynb` (copy of `01_case_war_room.ipynb` with separate cache/output dirs)

All live outputs are gitignored. No client PII is ever committed.

## 10. Doc Map

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Agent conventions (read automatically by Claude Code) |
| `AGENTS.md` | Pointer to CLAUDE.md for other agents |
| `README.md` | Quickstart for humans |
| `docs/HANDOFF.md` | **This file.** Full orientation. |
| `docs/LIVE_EVAL.md` | Live Eval Lane workflow and metrics rubric |
| `docs/DEMO_SCRIPT.md` | Talk track for live demo |
| `docs/METHOD.md` | How cache/scoring/queries/modules work |
| `docs/SAFETY_GUARDRAILS.md` | Disclaimers, data handling, boundaries |
| `docs/CODEX_REVIEW.md` | What was fixed and what was deferred |
| `docs/SESSION_LOG.md` | Build session history |
| `docs/BUILD_CHECKLIST.md` | Phase-by-phase checklist |
| `docs/DECISION_LOG.md` | Architecture decisions with rationale |
| `docs/PROMPT_SEQUENCE.md` | Prompt pipeline status |
