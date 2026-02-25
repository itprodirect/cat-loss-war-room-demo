# Codex Review — Patch Notes

## Addressed in this patch

- **P0 — Caselaw pack includes non-case pages.** Added a conservative `_is_case_like()` guard: keeps results only if citation is non-empty OR title matches case-name pattern (`v.`, `vs.`, `In re`, `Ex rel.`). Non-case pages (e.g. "What is an anti-concurrent causation clause?") are excluded.

- **P1 — Citation verify wastes budget on blank citations.** Skip checks when citation is blank. Increased search to k=5 hits. Score all hits and prefer the best-tier result (official > professional > unvetted). Budget exhaustion / exceptions now return `status="uncertain"` (not `"not_found"`). Added `MAX_CHECKS=6` cap per run.

- **P2 — Hostname normalization bug.** Replaced `lstrip("www.")` with `removeprefix("www.")` in source_scoring. `lstrip("www.")` could strip leading chars from domains like `www.weather.gov` → `eather.gov`. Added `flcourts.gov` (official) and `courtlistener.com` (official/case-repo).

- **P1 — Seeder headroom + overwrite logic.** Increased seeder budget to 40 calls. Cache-to-samples copy now overwrites stale fixtures. Copy filter limited to relevant keys (weather/carrier/caselaw/citecheck patterns only).

## Deferred (why + when)

- **Exa wrapper kwargs forwarding tests.** Low risk — the wrapper is thin and the `include_domains` / `exclude_domains` mutual exclusion is already handled. Add if we extend kwargs surface. *When:* Phase 3 if wrapper grows.

- **Export timestamp determinism.** `render_markdown_memo` includes `datetime.now()` which makes output non-reproducible. Not blocking — the export is a draft artifact. *When:* Phase 3 if we add snapshot tests for export output.

- **Notebook cwd polish.** The `ROOT = Path(".").resolve().parent` pattern is fragile if the notebook is opened from a different directory. Not blocking — works in the demo setup. *When:* Fix if it fails during demo dry-run.
