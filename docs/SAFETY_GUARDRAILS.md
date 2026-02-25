# Safety Guardrails

## Core Principles

1. **Not legal advice.** Every output includes "DEMO RESEARCH MEMO / NOT LEGAL ADVICE."
2. **Verify all citations.** Citation spot-checks are confidence signals, not verification. Always KeyCite/Shepardize before reliance.
3. **Source transparency.** Every source gets a confidence badge:
   - 🟢 Official (.gov, court sites, NOAA, NWS)
   - 🟡 Professional (law firms, legal publishers, news orgs)
   - 🔴 Unvetted (blogs, forums, unknown domains)
4. **Paywalled source flagging.** Westlaw, LexisNexis, and similar sources are flagged as paywalled — content cannot be verified without subscription access.
5. **No hallucinated citations.** The system searches for real sources, not generating case names. But search results can still be wrong — hence the verify mandate.

## Data Handling

- No client data is transmitted to third-party APIs (Exa searches use public legal terms, not case-specific PII)
- `.env` files with API keys are gitignored and never committed
- Cache files may contain search results — treat `cache/` as sensitive
- `cache_samples/` contains only public information suitable for demo

## Export Watermarks

All exported documents include:
- "DRAFT — ATTORNEY WORK PRODUCT" header
- "DEMO RESEARCH MEMO" designation
- Methodology and limitations section
- Source appendix with confidence ratings

## Boundaries

This tool does NOT:
- Provide legal advice or recommendations
- Replace attorney judgment or analysis
- Guarantee the accuracy of any citation or source
- Access privileged or confidential databases
- Store or transmit client PII
