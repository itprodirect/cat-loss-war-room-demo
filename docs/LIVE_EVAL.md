# Live Eval Lane

## What this is

The **Live Eval Lane** lets us run the war-room pipeline against
*public or fully-redacted* catastrophic-loss scenarios and record
structured metrics. It exists so we can:

- Measure pipeline quality (coverage, citation support, source mix)
  across multiple fact patterns before a live demo.
- Catch regressions when modules change.
- Build confidence without risking client data.

## What this is NOT

- **Not real client work.** No actual client PII, claim numbers, or
  privileged facts may appear in any committed file.
- **Not a replacement for the canonical demo notebook.**
  `notebooks/01_case_war_room.ipynb` remains the partner-facing demo
  surface and must not be modified by live-eval work.
- **Not automated CI.** Runs are manual; results are reviewed by a human.

## Folder layout

```
eval/
  intakes/          # Public/redacted intake JSONs (committed)
  results/          # Per-run metric snapshots (gitignored)
runs/               # Timestamped run exports (gitignored)
output/live/        # Markdown memos from live-eval runs (gitignored)
.exa_cache_live/    # Exa response cache for live-eval (gitignored)
```

Only `eval/intakes/` and documentation are committed.
Everything else stays local.

## Run workflow

1. **Pick an intake** from `eval/intakes/` (or create a new one from
   public sources — see `eval/README.md` for rules).
2. **Open `notebooks/live_eval.ipynb`** and paste / load the intake facts.
3. **Run all cells.** The notebook writes its cache to `.exa_cache_live/`
   and exports the memo to `output/live/`.
4. **Review the memo.** Score it against the metrics rubric below.
5. **Record metrics** in `eval/results/` (local only, gitignored).

## Metrics rubric (minimal)

| Metric | What to check | Target |
|---|---|---|
| **Coverage** | All three modules (weather, carrier, caselaw) return results | 3/3 |
| **Citation support** | Spot-check passes for best-tier sources | >= 80 % |
| **Gov sources present** | Weather section includes NOAA / NWS / SPC links | Yes |
| **Runtime** | Wall-clock time for full pipeline | < 90 s |
| **Cost** | Exa search spend per run | < $0.60 |

## Definition of Done for this branch

- [ ] `.gitignore` covers all live-eval artifacts
- [ ] `docs/LIVE_EVAL.md` exists (this file)
- [ ] `eval/README.md` documents intake rules and schema
- [ ] `notebooks/live_eval.ipynb` exists, uses separate cache/output dirs
- [ ] Canonical notebook (`01_case_war_room.ipynb`) unchanged
- [ ] 2-3 public intake JSONs committed in `eval/intakes/`
- [ ] At least one successful end-to-end run recorded in `eval/results/`
- [ ] Session log updated
- [ ] All existing tests still pass
