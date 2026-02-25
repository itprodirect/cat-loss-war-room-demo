# CAT-Loss War Room — Session Log

Track every build session here. Paste summaries from Claude Code / Codex after each prompt.

---

## Session 1 — Foundation (Prompt #1)
**Date:** 2026-02-25
**Agent:** Claude Code (Opus 4.6)
**Branch:** `chore/foundation-cells-0-2`
**Status:** ✅ Complete

### Goal
Stand up repo structure, Cells 0–2 (config/intake/query plan), caching system, source scoring, docs, tests.

### Results
```
Files created: 28
Tests passed: 24
Notes: All source stubs, docs, notebook (4 cells), cache/scoring/query plan modules.
```

---

## Session 2 — Exa Integration (Prompt #2)
**Date:** 2026-02-25
**Agent:** Claude Code (Opus 4.6)
**Branch:** `feat/cells-3-6-exa-modules`
**Status:** ✅ Complete

### Goal
Wire in Exa search wrapper, weather module (Cell 3), carrier playbook (Cell 4), case law + citation verifier (Cell 5), markdown export (Cell 6). Seed cache_samples for offline demo.

### Results
```
Files created: 35 changed
Tests passed: 55 (43 unit + 12 offline fixture validation)
Notes: Exa include/exclude domains are mutually exclusive — fixed in wrapper (include takes priority).
       Cache seeded with 30 Exa calls for Milton/Citizens/Pinellas.
       All 12 citation checks returned "uncertain" (professional sources, not court sites).
```

---

## Session 3 — Codex Review Patches
**Date:** 2026-02-25
**Agent:** Claude Code (Opus 4.6)
**Branch:** `feat/cells-3-6-exa-modules`
**Status:** ✅ Complete

### Goal
Apply P0 + key P1/P2 fixes from Codex review. No network calls — code + docs + tests only.

### Codex Review Findings
- **P0:** Caselaw pack included non-case pages (blog articles, explainers) alongside actual cases.
- **P1:** Citation verify wasted budget on blank citations, used only k=3 hits, treated budget exhaustion as "not found."
- **P2:** `lstrip("www.")` in hostname normalization could mangle domains (e.g. `weather.gov` → `eather.gov`). Missing court domains (flcourts.gov, courtlistener.com).
- **P1:** Seed script had no headroom (budget=30, used=30), and skipped overwriting stale fixtures.

### Patches Applied
- `caselaw_module.py`: Added `_is_case_like()` guard — keeps results only if citation is non-empty OR title matches case-name pattern (`v.`, `vs.`, `In re`, `ex rel.`).
- `citation_verify.py`: Skip blank citations; k=5 hits; score all hits and pick best tier; `BudgetExhausted` → `uncertain` (not `not_found`); `MAX_CHECKS=6` cap.
- `source_scoring.py`: `lstrip("www.")` → `removeprefix("www.")`; added `flcourts.gov` + `courtlistener.com` to official.
- `seed_cache_samples.py`: Budget 30→40; overwrite stale fixtures; copy filter limited to relevant prefixes.
- `docs/CODEX_REVIEW.md`: Addressed/deferred lists.

### Test Expansion
```
Tests: 55 → 75 (all passing)
New test files:
  - test_caselaw_filter.py (10 tests)
  - test_citation_verify.py (7 tests)
  - test_source_scoring.py (+3 regression tests)
```

### Kernel Mismatch Root Cause
Notebook was running against the system Python, not the project venv. Fix: register a named ipykernel from `.venv` and select it in JupyterLab. Added instructions to README.md.

### Reseed Results (after patches)
After reseeding with the patched code (user ran manually):
- Citation checks reduced from 12 → 6 (MAX_CHECKS cap)
- 1 verified (courtlistener.com hit), 5 uncertain
- Non-case pages filtered from caselaw pack

### Current Status
- Notebook Run All works with USE_CACHE=true
- Memo export to output/ works
- 75 tests passing, 0 network calls in tests

### Deferred
- Export timestamp determinism (Phase 3 if snapshot tests needed)
- Notebook cwd fragility (fix if demo dry-run fails)
- Exa wrapper kwargs forwarding tests (Phase 3 if wrapper grows)

---

## Stop Point — v0-demo shipped
**Date:** 2026-02-25
**Status:** Stable MVP

### What was shipped
- v0-demo tagged and released on GitHub
- PR merged to main with all Phase 1 + Phase 2 + Codex review patches
- Full pipeline working: intake → query plan → weather → carrier → caselaw → citation check → export
- Offline demo runs from committed cache_samples in <10 seconds
- 75 tests passing, 0 network calls in test suite
- Documentation: HANDOFF.md, DEMO_SCRIPT.md, CLAUDE.md, README.md, METHOD.md, SAFETY_GUARDRAILS.md, CODEX_REVIEW.md

### Why we stopped
MVP is stable. The offline demo works end-to-end. Tests pass. Docs exist for both agents and humans. Further work (firm memory, additional fact patterns, PDF export) is additive, not corrective. The right next step is a partner demo, not more code.

### Next session focus
- Approachability for non-technical professionals (docs/HANDOFF.md is the canonical entry point)
- Firm Memory Lite if Phase 3 proceeds
- Demo hardening for additional fact patterns (TX Hail, Hurricane Ida) if live demo is scheduled

---

## Session 4 — Firm Memory + Demo Polish (Prompt #3)
**Date:**
**Agent:**
**Branch:** `feat/firm-memory-polish`
**Status:** 🔲 Not started

### Goal
Firm Memory Lite (Cell 7), pre-seed demo cache with real Exa results for Milton/Citizens/Pinellas, polish export, test full demo run.

---

## Session 5 — Demo Hardening
**Date:**
**Agent:**
**Branch:**
**Status:** 🔲 Not started

### Goal
Cache all 3 fact patterns, test graceful degradation, dry-run the 5-minute script, generate sample PDF export.

---
