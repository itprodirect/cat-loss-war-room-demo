# CAT-Loss War Room — Decision Log

Track key architecture and design decisions so future sessions (human or AI) understand *why*.

---

## D001: CLAUDE.md instead of AGENTS.md
**Date:** 2026-02-24  
**Decision:** Use CLAUDE.md as the project conventions file, not AGENTS.md.  
**Reason:** Claude Code automatically reads CLAUDE.md on session start. AGENTS.md is a ChatGPT/Codex convention that Claude Code ignores. Using CLAUDE.md means every Claude Code session inherits project rules automatically.  
**Impact:** If using Codex for some prompts, you may want to also create an AGENTS.md that mirrors CLAUDE.md, or symlink them.

## D002: Posture as list[str], not nested dict
**Date:** 2026-02-24  
**Decision:** `posture: list[str]` (e.g., `["denial", "bad_faith"]`) instead of `posture: dict[str, bool]`.  
**Reason:** Simpler to iterate (`if "bad_faith" in case.posture`), fewer bugs, easier for AI agents to work with. The nested dict added no value — you never need `posture["bad_faith"] = False`.

## D003: Markdown export only in MVP (no PDF)
**Date:** 2026-02-24  
**Decision:** Cell 6 exports markdown. No PDF generation in Phase 1–2.  
**Reason:** PDF generation (weasyprint, wkhtmltopdf, fpdf2) adds dependency complexity and 3+ hours of debugging. Markdown is readable, editable, and converts to PDF in any tool. Ship markdown first, add PDF in Phase 3+.

## D004: Cache-first architecture with committed samples
**Date:** 2026-02-24  
**Decision:** Two cache layers: `cache_samples/` (committed, demo fixtures) and `cache/` (gitignored, runtime).  
**Reason:** The notebook must run without an API key on first clone. Committed sample data guarantees a working demo. Runtime cache avoids re-hitting the API during development. The USE_CACHE toggle lets you switch between cached and live mode.

## D005: Citation spot-check, not full verification
**Date:** 2026-02-24  
**Decision:** Run one Exa search per citation to check if it exists on a court/legal site. Report ✅/⚠️/❌. Do not claim "verified."  
**Reason:** Full citation verification requires Westlaw/Lexis (paywalled). A spot-check gives attorneys confidence the citation is real without overclaiming. The mandatory disclaimer ("KeyCite before reliance") handles the gap.  
**Cost:** ~$0.01 per citation, ~$0.10 per case run. Worth it for trust.

## D006: 7 cells, not 10
**Date:** 2026-02-24  
**Decision:** MVP is 7 cells (setup, intake, query plan, weather, carrier, caselaw, export). Expert finder, depo questions, demand outline, and policy checklist are Phase 2+.  
**Reason:** The 4 cells that actually impress attorneys are weather, carrier, caselaw, and export. The others are useful but don't create "wow" moments. Tight scope = faster ship = earlier feedback.

## D007: Firm Memory is a JSON file, not a database
**Date:** 2026-02-24  
**Decision:** Firm memory is a single JSON file (firm_memory.json) with load/save functions.  
**Reason:** No database, no server, no auth. ~30 lines of code. Creates the "platform" narrative in the demo ("it learns over time") without scope creep. Can migrate to SQLite or a real DB later if needed.

## D008: Source scoring via domain classification, not ML
**Date:** 2026-02-24  
**Decision:** Hardcoded domain dicts (GOV_COURT → 🟢, LEGAL_COMMENTARY → 🟡, everything else → 🔴).  
**Reason:** Deterministic, debuggable, explainable to attorneys. An ML classifier would be overkill for a demo and adds a "why did it rate this yellow?" trust problem. The hardcoded dict can be extended in 30 seconds.

## D009: Three demo fact patterns, one primary
**Date:** 2026-02-24  
**Decision:** Primary: Hurricane Milton / Citizens / Pinellas FL. Backup: TX Hail / Allstate / Tarrant. Stretch: Hurricane Ida / Lloyd's / Orleans Parish LA.  
**Reason:** Milton is Merlin's backyard — every attorney there has active Milton files. Citizens is their #1 opponent. The backup patterns prove jurisdiction flexibility. Cache all three, demo with Milton.

## D010: exa_py in requirements from day 1
**Date:** 2026-02-24  
**Decision:** Include `exa_py` in requirements.txt even though Prompt #1 doesn't make API calls.  
**Reason:** Stub modules import Exa types for type hints. Having it installed prevents import errors during development. Costs nothing, prevents a "why is this broken" moment between Prompt #1 and Prompt #2.
