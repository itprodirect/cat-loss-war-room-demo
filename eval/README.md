# eval/ — Live Eval Intakes & Results

## Rules for intake files

All intake JSONs in `eval/intakes/` **must** be sourced from public
information or be fully redacted/fictional. They are committed to the repo.

### Do NOT include

- Real policyholder names or insured names
- Claim numbers or policy numbers
- Street addresses or GPS coordinates
- Phone numbers or email addresses
- Adjuster or examiner names
- Any information obtained under attorney-client privilege

### Acceptable sources

- NOAA / NWS storm reports (public record)
- Published court opinions (case law databases)
- News articles about declared disaster events
- Fictional / composite scenarios clearly labeled as such

## Intake JSON schema

Each file in `eval/intakes/` should be a JSON object matching the
`CaseIntake` dataclass in `src/war_room/query_plan.py`:

```json
{
  "event_name": "Hurricane Milton",
  "event_date": "2024-10-09",
  "state": "FL",
  "county": "Pinellas",
  "carrier": "Citizens Property Insurance",
  "policy_type": "HO-3 Dwelling",
  "posture": ["denial"],
  "key_facts": [
    "Category 4 at FL landfall",
    "Roof damage from wind-driven rain"
  ],
  "coverage_issues": [
    "Wind vs. flood causation",
    "Anti-concurrent-cause clause"
  ],
  "public_links": [
    "https://www.nhc.noaa.gov/data/tcr/AL142024_Milton.pdf"
  ]
}
```

The `public_links` field is optional and not consumed by the pipeline
today, but useful for traceability.

## Where results go

| Folder | Committed? | Purpose |
|---|---|---|
| `eval/intakes/` | Yes | Public/redacted intake JSONs |
| `eval/results/` | **No** (gitignored) | Per-run metric snapshots |
| `runs/` | **No** (gitignored) | Timestamped full exports |
| `output/live/` | **No** (gitignored) | Markdown memos |

See [`docs/LIVE_EVAL.md`](../docs/LIVE_EVAL.md) for the full workflow and
metrics rubric.
