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

## Exa Search Wrapper (exa_client.py)

All network calls go through `ExaClient`, a thin wrapper around `exa-py`.

**Assumptions about exa-py (introspected from exa_py 1.x):**
- `Exa(api_key)` constructor
- `Exa.search(query, num_results=, include_domains=, start_published_date=, contents=)` returns `SearchResponse`
- `contents=ContentsOptions(text={"max_characters": N})` inlines text in results
- Result objects have: `url`, `title`, `score`, `published_date`, `text`, `summary`, `highlights`
- `ContentsOptions` is a TypedDict from `exa_py.api`

**Features:**
- Simple retry with exponential backoff (3 attempts)
- Budget guard: `MAX_SEARCH_CALLS` (default 30), raises `BudgetExhausted` if exceeded
- Normalizes results to plain dicts: `{title, url, published_date, snippet, text, score}`

## Citation Verification (citation_verify.py)

Spot-check only: one Exa search per citation to verify it appears on a court or legal site. Reports ✅ (found on official site), ⚠️ (found but unverified source), or ❌ (not found). Not a substitute for KeyCite/Shepardize.

## Weather Module (weather_module.py)

Runs weather queries with gov-first domain preference (noaa.gov, weather.gov, fema.gov, etc.). Extracts metrics (wind mph, surge ft, rain in) via regex only when present in text — never invents numbers.

## Carrier Module (carrier_module.py)

Runs carrier_docs queries. Categorizes results by type (denial patterns, DOI complaints, regulatory actions, claims manuals). Extracts common defenses from text and generates rebuttal angles from case facts. Avoids overclaiming bad faith — describes "signals" with citations.

## Case Law Module (caselaw_module.py)

Runs caselaw queries, excluding paywalled domains (Westlaw, LexisNexis). Organizes results by legal issue. Extracts case names, citations, court, and year via regex. Limits to 6-12 cases total.

## Export (export_md.py)

Compiles all module outputs into a structured markdown memo with:
- DRAFT / ATTORNEY WORK PRODUCT watermark
- Case intake, weather, carrier, caselaw sections
- Citation spot-check table
- Query plan appendix
- Deduplicated source appendix
- Methodology & limitations section
