# CAT-Loss War Room — Prompt Sequence

Status of each Claude Code / Codex prompt in the build pipeline.

---

## Prompt #1: Foundation (Cells 0–2)
**File:** `prompts/PROMPT_1_FINAL.md`  
**Status:** 🔲 Ready to run  
**Agent:** Claude Code  
**Branch:** `chore/foundation-cells-0-2`  
**Estimated time:** 15–25 min agent execution  
**What it builds:**
- CLAUDE.md + README + docs (demo script, guardrails, method)
- src/war_room/ modules: config, cache_io, source_scoring, intake, query_plan
- Stub modules for weather, carrier, caselaw, citation, export, memory
- Notebook: Cells 0–3 (title, config, intake, query plan)
- Tests: 4 test files, all passing
**What it does NOT build:** No Exa calls, no search modules, no export

### After Prompt #1 completes:
1. Run `pytest -q` — confirm all tests pass
2. Open notebook — Run All — confirm no errors
3. Review the query plan output — are the queries sensible?
4. Commit + push branch
5. Paste Claude Code's summary into SESSION_LOG.md
6. Get Prompt #2 from ChatGPT (or draft it yourself)

---

## Prompt #2: Exa Integration (Cells 3–6)
**File:** `prompts/PROMPT_2_EXA.md` (to be created)  
**Status:** 🔲 Waiting for Prompt #1  
**Agent:** Claude Code  
**Branch:** `feat/exa-search-modules`  
**What it builds:**
- Exa search wrapper (retry, budget guard, cache integration)
- Weather module (Cell 3): gov-source-first, structured output
- Carrier playbook (Cell 4): denial patterns, rebuttal angles, carrier docs
- Case law + citation verifier (Cell 5): issue-organized, ✅/⚠️/❌ check
- Markdown export (Cell 6): full bundle with source appendix
- Tests for each module

### After Prompt #2 completes:
1. Set EXA_API_KEY in .env
2. Run notebook with USE_CACHE=false to generate live results
3. Copy results to cache_samples/ for the Milton fact pattern
4. Switch back to USE_CACHE=true
5. Verify notebook runs clean from cache
6. Time each cell — target <10s cached

---

## Prompt #3: Memory + Demo Polish
**File:** `prompts/PROMPT_3_POLISH.md` (to be created)  
**Status:** 🔲 Waiting for Prompt #2  
**Agent:** Claude Code  
**Branch:** `feat/firm-memory-polish`  
**What it builds:**
- Firm Memory Lite (Cell 7): JSON load/save, pre-seeded demo data
- Cache seeding for backup fact patterns (TX hail, LA commercial)
- Demo hardening: graceful degradation in every cell
- Final README update

---

## Prompt #4: Demo Dry-Run (optional)
**Status:** 🔲 Stretch  
**What it does:**
- Full 5-minute timed run
- Screenshot/record outputs for each cell
- Generate sample export for offline demo backup
- Final PR to main

---

## Tips for Running Prompts

1. **Always start Claude Code in the repo root** — it reads CLAUDE.md automatically
2. **One prompt per session** — don't chain prompts in one session, the context gets long
3. **Review before committing** — check that tests pass and notebook runs clean
4. **Log everything** — paste Claude Code's summary into SESSION_LOG.md after each run
5. **If something breaks** — fix it manually, log the fix in SESSION_LOG.md, then continue
