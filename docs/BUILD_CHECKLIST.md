# CAT-Loss War Room — Build Checklist

## Phase 1: Foundation (Prompt #1) — Target: 3–4 hours

### Repo Structure
- [ ] .gitignore updated
- [ ] .env.example created
- [ ] Directory tree: src/war_room/, cache_samples/, output/, docs/, tests/, notebooks/
- [ ] .gitkeep files in empty tracked dirs

### Documentation
- [ ] CLAUDE.md (project conventions for Claude Code)
- [ ] README.md (quickstart + disclaimer)
- [ ] docs/DEMO_SCRIPT.md (5-min talk track)
- [ ] docs/GUARDRAILS.md (safety rules)
- [ ] docs/METHOD.md (how cache/scoring/queries work)

### Python Modules (src/war_room/)
- [ ] __init__.py (clean exports)
- [ ] config.py (env loading, defaults)
- [ ] cache_io.py (normalize_key, cached_call, cache_get/set)
- [ ] source_scoring.py (score_url, domain dicts, format helper)
- [ ] intake.py (CaseIntake dataclass, validate, format_card)
- [ ] query_plan.py (QuerySpec, generate_query_plan, format table)
- [ ] Stub modules: weather, carrier, caselaw, citation_verify, export_md, firm_memory

### Notebook (notebooks/01_case_war_room.ipynb)
- [ ] Cell 0: Title + disclaimer (markdown)
- [ ] Cell 1: Imports + config (code)
- [ ] Cell 2: Sample intake + formatted card (code)
- [ ] Cell 3: Query plan generator + formatted output (code)
- [ ] Cell 4: "Coming next" placeholder (markdown)

### Tests
- [ ] test_query_plan.py — plan returns queries for all 3 modules
- [ ] test_source_scoring.py — .gov=🟢, blog=🔴, merlin=🟡, westlaw=paywalled
- [ ] test_cache_io.py — roundtrip + normalize_key
- [ ] test_intake.py — validation + format card
- [ ] All tests pass: `pytest -q`

### Verification
- [ ] Notebook runs all cells without errors (no API key needed)
- [ ] Branch pushed: chore/foundation-cells-0-2

---

## Phase 2: Exa Integration (Prompt #2) — Target: 5–6 hours

### Exa Wrapper
- [ ] src/war_room/exa_client.py — search wrapper with retry, rate limit, budget tracking
- [ ] Integrates with cached_call (cache-first, live-fallback)
- [ ] Budget guard: warn at 80%, halt at session cap

### Weather Module (Cell 3)
- [ ] Runs weather queries from query plan
- [ ] Filters for .gov sources first
- [ ] Outputs structured weather summary with source badges
- [ ] Templated "litigation relevance" paragraph
- [ ] Graceful degradation if no .gov results found

### Carrier Playbook (Cell 4)
- [ ] Runs carrier queries
- [ ] Categorizes: regulatory actions, denial patterns, carrier documents
- [ ] Generates rebuttal angles from key_facts
- [ ] Handles missing NAIC/DOI data gracefully
- [ ] Carrier Document Pack (claims manuals, bulletins)

### Case Law + Citation Verifier (Cell 5)
- [ ] Runs case law queries (dynamic by posture)
- [ ] Organizes by legal issue, not by source
- [ ] Citation spot-check: ✅ / ⚠️ / ❌ per citation
- [ ] Mandatory verification disclaimer
- [ ] Paywalled source flagging

### Export (Cell 6)
- [ ] Compiles all module outputs to single markdown
- [ ] Source appendix table (URL, confidence, module, date)
- [ ] DRAFT — ATTORNEY WORK PRODUCT watermark
- [ ] Methodology & limitations section
- [ ] Saves to output/ directory

### Tests
- [ ] test_exa_client.py — mock search, budget tracking
- [ ] test_weather.py — output structure validation
- [ ] test_carrier.py — rebuttal angle generation
- [ ] test_caselaw.py — citation verifier logic
- [ ] test_export.py — markdown output contains all sections

### Cache Seeding
- [ ] Run live queries for Milton/Citizens/Pinellas
- [ ] Save results to cache_samples/ (committed to repo)
- [ ] Verify notebook runs end-to-end with USE_CACHE=true

---

## Phase 3: Memory + Polish (Prompt #3) — Target: 2–3 hours

### Firm Memory Lite (Cell 7)
- [ ] JSON load/save from firm_memory.json
- [ ] Pre-seeded with 5–8 demo entries (Citizens, FL experts)
- [ ] Display as "📋 FIRM NOTES" — visually distinct from Exa results
- [ ] Add to relevant cells: carrier playbook gets carrier_notes, etc.

### Demo Hardening
- [ ] Cache all 3 fact patterns (Milton, TX Hail, Ida)
- [ ] USE_CACHE=true is default and demo-stable
- [ ] Every cell handles API failures gracefully
- [ ] Dry-run 5-minute demo script end-to-end
- [ ] Time each cell execution (target: <10 sec cached, <30 sec live)

### Final Polish
- [ ] README updated with full quickstart
- [ ] DEMO_SCRIPT.md updated with actual outputs
- [ ] Sample export PDF generated and committed
- [ ] PR merged to main

---

## Phase 4: Stretch Goals (if time permits)

- [ ] Expert Finder module
- [ ] Depo/EUO Question Bank
- [ ] Demand Brief Outline
- [ ] PDF export (weasyprint)
- [ ] Policy Language Checklist
- [ ] Timeline Builder
- [ ] Second/third fact pattern fully cached + tested
