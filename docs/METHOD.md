# Methodology

## Architecture

The war room follows a **cache-first, source-scored** pipeline:

```
CaseIntake → QueryPlan → [Weather | Carrier | CaseLaw] → CitationVerify → Export
```

## Cache System (cache_io.py)

Two-layer cache:
1. **cache_samples/** — Committed to repo. Contains pre-cached demo results. Guarantees the notebook runs without an API key on first clone.
2. **cache/** — Gitignored. Runtime cache populated by live API calls. Avoids re-hitting Exa during development.

Lookup order: `cache_samples/` → `cache/` → live API call → save to `cache/`.

Cache keys are normalized: lowercased, stripped, with spaces replaced by underscores. Files are stored as JSON.

## Source Scoring (source_scoring.py)

Deterministic domain-based classification:

| Tier | Badge | Examples |
|------|-------|----------|
| Official | 🟢 | .gov, courts.*, NOAA, NWS, state DOI |
| Professional | 🟡 | law firms, legal publishers, Reuters, AM Best |
| Unvetted | 🔴 | blogs, forums, unknown domains |
| Paywalled | 🔒 | Westlaw, LexisNexis, HeinOnline |

No ML — fully deterministic and debuggable.

## Query Plan (query_plan.py)

Given a `CaseIntake`, generates 12–18 search queries organized by module:

- **weather** — NOAA storm reports, NWS advisories, damage surveys for the specific event/location
- **carrier_docs** — Carrier denial patterns, DOI complaints, regulatory actions, claims manuals
- **caselaw** — Jurisdiction-specific precedent for the coverage type and litigation posture

Queries include date ranges, domain preferences, and category tags.

## Citation Verification (citation_verify.py) — Phase 2

Spot-check only: one Exa search per citation to verify it appears on a court or legal site. Reports ✅ (found on official site), ⚠️ (found but unverified source), or ❌ (not found). Not a substitute for KeyCite/Shepardize.
