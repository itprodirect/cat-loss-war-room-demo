# CAT-Loss War Room — Demo Script (Cells 0–2)

**Duration:** ~3 minutes (Phase 1 scope)
**Setup:** Notebook open, USE_CACHE=true, all cells pre-run

---

## Opening (30 sec)

> "This is a research war room for catastrophic loss litigation. You give it a case,
> it builds a structured research package — weather data, carrier intel, case law —
> in under a minute. Everything is source-scored and citation-checked."

## Cell 0 — Title + Disclaimer (show, don't run)

> "First thing you see: disclaimers. This is a research accelerator, not legal advice.
> Every output says 'verify all citations.' We take that seriously."

## Cell 1 — Config (run)

> "Configuration loads from environment. USE_CACHE=true means we're running from
> pre-cached results — no API calls, no billing surprises. In production mode you'd
> flip this to false for live search."

**Show:** Config printout with directories and cache status.

## Cell 2 — Case Intake (run)

> "Here's our sample case: Hurricane Milton, Citizens Property Insurance, Pinellas County.
> Dwelling policy, denial posture. This is the kind of case Merlin handles every week."

**Show:** Formatted intake card with all case parameters.

## Cell 3 — Query Plan (run)

> "From that intake, the system generates 12–18 targeted research queries — organized
> by module: weather, carrier docs, case law. These aren't generic Google searches.
> They're crafted for legal research: specific jurisdictions, date ranges, legal terms."

**Show:** Query plan grouped by module with query text and date filters.

## What's Next (verbal)

> "In the full version, each of those queries feeds into Exa search. Weather data
> comes back with .gov source preference. Carrier intel finds denial patterns and
> regulatory actions. Case law is organized by legal issue with citation spot-checks.
> The whole package exports to a markdown brief with source confidence badges."

---

## Tips
- Keep USE_CACHE=true for reliable demo
- If asked about cost: "About $0.30 per case run with live search"
- If asked about accuracy: "Every source gets a confidence badge. We flag paywalled
  sources. The disclaimer says verify — and we mean it."
