# Roadmap (Simple, Current)

Last updated: March 4, 2026

This is the short version. Clean, practical, no drama.

## Where we are now

- Demo pipeline is stable.
- 81 tests are passing.
- CI has a fresh-environment gate plus `exa-py` compatibility matrix.
- Issue [#4](https://github.com/itprodirect/cat-loss-war-room-demo/issues/4) is done.

## Now (next 2-3 weeks)

Goal: remove schema ambiguity, strengthen contracts, and harden test quality.

- [#5](https://github.com/itprodirect/cat-loss-war-room-demo/issues/5) Align eval intake schema with `CaseIntake`
- [#6](https://github.com/itprodirect/cat-loss-war-room-demo/issues/6) Introduce typed domain contracts
- [#7](https://github.com/itprodirect/cat-loss-war-room-demo/issues/7) Retrieval provider abstraction + contract tests
- [#8](https://github.com/itprodirect/cat-loss-war-room-demo/issues/8) Multi-jurisdiction fixture suite + snapshots
- [#9](https://github.com/itprodirect/cat-loss-war-room-demo/issues/9) Expand CI quality gates

## Next (30-60 days)

Goal: move from notebook orchestration to product-grade flow.

- [#10](https://github.com/itprodirect/cat-loss-war-room-demo/issues/10) API orchestrator with graceful degradation
- [#11](https://github.com/itprodirect/cat-loss-war-room-demo/issues/11) Guided web intake + run status UX
- [#12](https://github.com/itprodirect/cat-loss-war-room-demo/issues/12) Evidence normalization + provenance
- [#13](https://github.com/itprodirect/cat-loss-war-room-demo/issues/13) Caselaw quality v2

## Then (60-90 days)

Goal: trust, polish, and real-world adoption readiness.

- [#14](https://github.com/itprodirect/cat-loss-war-room-demo/issues/14) Citation verification hardening
- [#15](https://github.com/itprodirect/cat-loss-war-room-demo/issues/15) Memo workspace v2
- [#16](https://github.com/itprodirect/cat-loss-war-room-demo/issues/16) Firm memory v1
- [#17](https://github.com/itprodirect/cat-loss-war-room-demo/issues/17) Observability + cost controls
- [#18](https://github.com/itprodirect/cat-loss-war-room-demo/issues/18) Security baseline
- [#19](https://github.com/itprodirect/cat-loss-war-room-demo/issues/19) Attorney pilot validation

## Success checks we care about

- Reliability: tests and CI stay green on every PR.
- Trust: every key statement in output can be traced to sources.
- Usability: non-technical users can run intake-to-memo with minimal guidance.
- Quality: fewer noisy results, better case law precision, clearer citation confidence.

## Notes

- Detailed architecture plan: [V2_BLUEPRINT.md](V2_BLUEPRINT.md)
- Issue-by-issue map: [V2_ISSUE_MAP.md](V2_ISSUE_MAP.md)
