# CAT-Loss War Room V2 Blueprint

## 1) Deep-Dive Assessment (Current Repo)

### What Works Well

- Cache-first demo architecture is pragmatic and reliable for offline demos.
  - `cached_call()` uses `cache_samples -> cache -> live` in one place: `src/war_room/cache_io.py`.
- Clear legal-safety posture is consistently documented and exported.
  - Disclaimers appear in docs and memo renderer: `docs/SAFETY_GUARDRAILS.md`, `src/war_room/export_md.py`.
- Module separation is understandable.
  - Query planning, weather, carrier, caselaw, citation checks are split into focused files under `src/war_room/`.
- Test intent is good for a prototype.
  - Tests target core behavior and avoid network calls by default.

### What Is OK (But Limits Scale)

- Notebook-first UX is acceptable for internal demos but weak for broad attorney adoption.
  - Flow is linear and reproducible, but not guided for non-technical users.
- Deterministic source scoring improves explainability.
  - Useful baseline, but domain dictionaries will age and drift without governance.
- Query generation is fast and simple.
  - Good for startup velocity, but lacks jurisdiction-aware precision, quality scoring, and explainability logs.

### What Is Bad / High Risk

- Dependency compatibility was a high risk and is now mitigated.
  - Exa compatibility hardening shipped in PR #20 (issue #4 closed).
  - Version-safe contents options + pinned dependencies + CI matrix are now in place.
- Live-eval intake schema is inconsistent.
  - `eval/README.md` says intake JSON should match `CaseIntake`.
  - `eval/intakes/_template_public_intake.json` does not match `CaseIntake` fields.
- Caselaw quality still allows non-case content into issue packs.
  - Citation-like text in commentary pages can pass current filter logic.
- Notebook runtime can degrade badly outside happy path.
  - `client = None` fallback is set in notebook cells, but module functions still call `client.search(...)` when cache misses.
- Extraction quality is brittle.
  - Metrics and case metadata are regex-first and not confidence-scored.
  - Can output noisy artifacts from scraped content.

### Unknowns (Need Measured Validation)

- Real quality across multiple jurisdictions and perils.
- True precision/recall for caselaw relevance.
- Citation verification reliability against official court sources at scale.
- End-user usability for attorneys/paralegals without technical support.
- Live performance and API cost under repeated real-world use.

## 2) V2 Product Vision

### Product Goal

Deliver a dependable legal research workbench for catastrophic-loss litigation that is:

- trusted by attorneys,
- fast enough for live strategy sessions,
- auditable for every claim and citation,
- and simple for non-technical legal teams.

### User Outcomes

- Partner can trust the output structure and source traceability in minutes.
- Paralegal can produce first-pass research packages in less than 15 minutes.
- Litigation team can compare multiple strategy angles with explicit evidence confidence.

## 3) UX / UI Direction (From Notebook to Product)

### Current UX Verdict

- Helpful for technical demos.
- Not sufficient for daily legal operations.
- Discoverability is low, error handling is implicit, and outputs are noisy.

### V2 UX Model

- Web app with guided, step-based workflow:
  1. Intake wizard (jurisdiction, peril, carrier, posture, facts).
  2. Research plan preview and editable scope.
  3. Live progress with module status and budget/time indicators.
  4. Evidence board with source badges, excerpt quality, and exclusions.
  5. Case law workspace with issue clusters and citation confidence.
  6. Memo builder with edit/approve/export.

### UX Principles

- Make trust visible: every assertion linked to evidence.
- Make uncertainty explicit: confidence + why + next action.
- Make failure graceful: partial output is better than crash.
- Make legal review easy: copyable citations, clear provenance, clean summaries.

## 4) V2 Architecture (Ground-Up Rebuild)

### 4.1 High-Level Architecture

- `apps/web`: user-facing UI.
- `apps/api`: orchestration API and session state.
- `services/retrieval`: provider adapters (Exa now, pluggable later).
- `services/enrichment`: extraction, normalization, dedupe, scoring.
- `services/reasoning`: issue clustering, argument synthesis, rebuttal scaffolds.
- `services/export`: markdown/docx/pdf generation.
- `services/memory`: firm memory store (versioned, auditable).
- `shared/domain`: typed domain models and validation rules.

### 4.2 Domain-First Data Model

Use strongly typed models (Pydantic) for:

- `CaseIntake`
- `QueryPlan`
- `EvidenceItem`
- `LegalIssue`
- `CaseCitation`
- `CitationCheck`
- `CarrierSignal`
- `WeatherFact`
- `ResearchMemo`
- `RunAuditLog`

All module boundaries consume/return typed objects, not free-form dicts.

### 4.3 Pipeline Design

1. Intake validation + normalization.
2. Query planning with explicit rationale per query.
3. Retrieval with retry, throttling, budget tracking, and provider contracts.
4. Evidence normalization and deduplication.
5. Module analysis (weather/carrier/caselaw).
6. Citation verification + conflict detection.
7. Memo assembly with provenance map.
8. Export + immutable run snapshot.

### 4.4 AI Integration (Only Where It Adds Real Value)

Use AI for:

- extracting structured facts from noisy text,
- summarizing long evidence into clean legal notes,
- drafting argument variants from verified evidence.

Do not use AI for:

- source credibility tiering (keep deterministic policy + rules),
- citation truth decisions without source evidence,
- legal conclusions presented as advice.

Guardrails:

- Evidence-linked generation only.
- No final statement without at least one citation anchor.
- Confidence score and rationale for every generated section.

### 4.5 Security / Compliance Baseline

- Strict PII redaction layer before external retrieval.
- Secret handling via environment + vault (no plain-text repo secrets).
- Immutable audit log for query and citation actions.
- Role-based access for memo edits and approvals.
- Data retention policy per environment (demo vs production).

### 4.6 Reliability and Observability

- Structured logs for each pipeline stage.
- Run-level trace IDs.
- Metrics: latency, failure rates, source-tier distribution, citation-check outcomes, cost/run.
- Alerting on provider outages and quality regression thresholds.

## 5) Refactor Strategy from V0 to V2

### Keep as Learning Assets

- Query decomposition concept.
- Cache-first design intent.
- Source tiering policy concept.
- Memo export structure and legal disclaimers.

### Replace / Rebuild

- Rebuild Exa adapter with version-safe client abstraction.
- Replace dict-based module contracts with typed models.
- Replace notebook orchestration with API-driven workflow.
- Replace heuristic-only extraction with hybrid extractor (rules + AI with guardrails).
- Replace ad hoc docs with architecture decision records tied to release milestones.

### Migration Path

- Phase A: Introduce typed models and compatibility adapters around existing modules.
- Phase B: Move orchestration into API service while notebook calls API endpoints.
- Phase C: Ship web intake and evidence board.
- Phase D: Retire notebook as primary interface, keep as diagnostic tool only.

## 6) Testing and Edge-Case Strategy (First-Class Workstream)

### 6.1 Testing Pyramid

- Unit tests:
  - Pure functions, model validation, scoring, parsing, query planning.
- Component tests:
  - Retrieval adapter contracts, enrichment pipeline, citation verifier.
- Integration tests:
  - End-to-end pipeline against fixture bundles across multiple fact patterns.
- End-to-end UI tests:
  - Intake-to-export critical flow, error states, retry flows.
- Non-functional tests:
  - Performance, load, resilience, and cost-budget tests.

### 6.2 Quality Gates

- Gate 1: deterministic unit tests must pass.
- Gate 2: contract tests for external provider adapter must pass.
- Gate 3: regression snapshot tests for memo sections must pass.
- Gate 4: scenario suite across 3+ jurisdictions must pass minimum quality thresholds.
- Gate 5: security checks (secret scanning, dependency checks) must pass.

### 6.3 Critical Edge-Case Matrix

- Input edge cases:
  - Missing county/state/date.
  - Non-hurricane peril types.
  - Multi-state events.
  - Invalid posture combinations.
- Retrieval edge cases:
  - API timeout, rate limit, partial outage, malformed results.
  - Empty result set for one module.
  - Provider schema changes.
- Evidence edge cases:
  - Duplicated URLs with conflicting metadata.
  - Non-English pages.
  - Paywalled citation leakage.
  - HTML-heavy noisy text blocks.
- Citation edge cases:
  - Missing citation in relevant case.
  - Citation appears only in commentary page.
  - Conflicting case years/courts across sources.
- Export edge cases:
  - Missing module outputs.
  - Overlong memo sections.
  - Broken links and unsupported characters.

### 6.4 Reliability Targets

- Cached run p95 latency: < 10 seconds.
- Live run p95 latency: < 75 seconds.
- Pipeline success rate: >= 99 percent (cached), >= 95 percent (live).
- Citation check actionable rate (verified or clearly uncertain with reason): >= 95 percent.

## 7) 30/60/90 Day Roadmap

### Days 0-30: Foundations

- Stabilize dependencies and provider adapters.
- Introduce domain models and validation.
- Add robust test harness and scenario fixtures.
- Define quality scorecard and acceptance thresholds.

### Days 31-60: Product Core

- Build API orchestrator.
- Ship web intake wizard + run status UI.
- Implement evidence normalization and improved case filtering.
- Add structured run audit logs and observability dashboards.

### Days 61-90: Trust and Adoption

- Memo workspace and export improvements.
- Firm memory v1 with governance.
- Multi-fact-pattern evaluation suite and benchmark reporting.
- Hardening pass for reliability, usability, and legal workflow fit.

## 8) Success Metrics for V2

- Research package quality:
  - Attorney-rated usefulness >= 8/10 on pilot matters.
- Trust:
  - Citation confidence and provenance accepted in partner review.
- Usability:
  - New user can complete intake and generate memo in < 10 minutes.
- Reliability:
  - Zero hard crashes in guided flow during pilot demos.
- Engineering health:
  - CI green with full quality gates and reproducible builds.

## 9) Immediate Next Actions

1. Align live-eval intake schema with canonical `CaseIntake` (issue #5).
2. Introduce typed contracts across modules (issue #6).
3. Finalize retrieval contract boundary and tests (issue #7).
4. Build multi-jurisdiction fixture + snapshot quality lane (issue #8).
5. Expand CI quality gates and release criteria (issue #9).
