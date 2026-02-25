# CAT-Loss War Room — Demo Script

**Duration:** 5 minutes
**Setup:** Notebook open in JupyterLab, kernel set to `cat-loss-war-room-demo (.venv)`, USE_CACHE=true, all cells pre-run once.

---

## Demo Modes

| Mode | When to use | Setup |
|------|-------------|-------|
| **Offline (recommended)** | Partner meetings, conferences, any environment | USE_CACHE=true in .env. No API key needed. |
| **Live** | Showing real-time capability | USE_CACHE=false, EXA_API_KEY set. ~60 seconds, ~$0.30. |

**Always use offline mode for the first demo.** Switch to live only if explicitly asked "can it run in real time?"

---

## Opening (30 sec)

> "This is a research war room for catastrophic loss litigation. You give it a case — a hurricane, a carrier, a county — and it builds a structured research package in under a minute. Weather data, carrier intel, case law, all source-scored and citation-checked."

## Cell 0 — Title + Disclaimer (show, don't run)

> "First thing you see: disclaimers. This is a research accelerator, not legal advice. Every output says 'verify all citations.' That's not a checkbox — it's how the tool is designed."

## Cell 1 — Config (run)

> "Configuration loads automatically. We're running from pre-cached results today — no API calls, no billing. In production you'd flip one switch for live search."

**Show:** Config printout. Point out USE_CACHE=true.

## Cell 2 — Case Intake (run)

> "Here's our sample case: Hurricane Milton, Citizens Property Insurance, Pinellas County. Dwelling policy, denial posture with bad faith. This is a case your attorneys would recognize."

**Show:** Formatted intake card.

## Cell 3 — Query Plan (run)

> "From that intake, the system generates targeted research queries — not generic Google searches. These are jurisdiction-specific, date-filtered, and organized by research module."

**Show:** Query plan grouped by weather / carrier docs / case law. Point out the domain preferences and date filters.

## Cell 4 — Weather Corroboration (run)

> "Weather corroboration pulls from official sources — NOAA, NWS, FEMA. It extracts wind speeds, storm surge, rainfall when the data is there. Every source gets a confidence badge."

**Show:** Metrics, key observations, top sources with badges. Point out 🟢 badges on .gov sources.

## Cell 5 — Carrier Document Pack (run)

> "The carrier pack finds denial patterns, DOI complaints, regulatory actions. It generates rebuttal angles from the case facts. This is the kind of intelligence that takes a paralegal days to compile."

**Show:** Document list with badges, common defenses, rebuttal angles.

## Cell 6 — Case Law + Citation Check (run)

> "Case law is organized by legal issue — concurrent causation, bad faith standards, carrier precedent. Each citation gets a spot-check: can we find it on an official court site? Green check means yes, yellow means we found it but on a secondary source, red means verify manually."

**Show:** Issues with cases, citation spot-check table with badges.

## Cell 7 — Export (run)

> "Everything compiles into a single markdown memo — watermarked as draft, with a full source appendix and methodology section. An attorney can open this, verify the citations, and start building their brief."

**Show:** File path, character count, first 40 lines of the memo.

---

## What to Say (confidence + guardrails)

- "Every source gets a confidence badge — green for official, yellow for professional, red for unvetted."
- "We exclude paywalled sources like Westlaw from primary results — we can't verify what we can't read."
- "Citation spot-checks are confidence signals, not verification. The tool says KeyCite before reliance and means it."
- "This runs on about $0.30 of API calls per case. The cached version is free."
- "The export is a starting point. An attorney still needs to verify and analyze."

## What NOT to Say

- Don't say "hallucination" — say "we verify against real sources" or "we flag what we can't confirm."
- Don't get into AI model internals, training data, or architecture details.
- Don't promise accuracy percentages or claim the tool replaces attorney judgment.
- Don't mention specific model names (Claude, GPT) unless asked directly.
- Don't demo live mode unless you've tested it in the last 24 hours.

## If Asked...

- **"Is this accurate?"** — "Every source is real and linked. The confidence badges tell you how much to trust each one. We always recommend independent verification."
- **"Can it handle my case type?"** — "It's built for catastrophic loss — hurricanes, hail, flood. The query plan adapts to jurisdiction, carrier, and coverage type."
- **"How much does it cost?"** — "About 30 cents per case in API calls. The demo runs for free from cached results."
- **"Can we use this tomorrow?"** — "This is a demo prototype. The architecture is solid but it needs firm-specific customization before production use."
