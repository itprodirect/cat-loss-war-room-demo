# CAT-Loss War Room — Claude Code Project Conventions

## What this project is
A Jupyter-notebook-based "war room" tool for catastrophic insurance loss litigation.
It uses Exa search to gather weather data, carrier playbook intel, and case law,
then exports a structured research memo. Built for demo at Merlin Law Group.

## Quick setup
```bash
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# source .venv/Scripts/activate  # Windows Git Bash
pip install -r requirements.txt
pytest -q
```

## Repo layout
```
src/war_room/       # All Python logic lives here
  cache_io.py       # Cache-first data access (cache_samples → cache → live)
  source_scoring.py # 🟢🟡🔴 URL credibility scoring
  query_plan.py     # CaseIntake + QuerySpec + generate_query_plan()
  weather_module.py # (stub) Weather data gathering
  carrier_module.py # (stub) Carrier playbook intel
  caselaw_module.py # (stub) Case law search
  citation_verify.py# (stub) Citation spot-check
  export_md.py      # (stub) Markdown export
notebooks/          # Jupyter notebooks (the demo surface)
cache_samples/      # Committed demo fixtures (run without API key)
cache/              # Runtime cache (gitignored)
output/             # Generated reports (gitignored)
tests/              # pytest test suite
docs/               # Project documentation
```

## Conventions
- **Keep notebooks thin.** Business logic goes in `src/war_room/`, notebooks just call it.
- **Cache-first.** Every external call goes through `cached_call()`. Demo must work offline.
- **No secrets in code.** `.env` is gitignored. Use `.env.example` for the template.
- **Source scoring is deterministic.** Hardcoded domain dicts, not ML.
- **Always include disclaimers.** Every output must say "DEMO RESEARCH MEMO / NOT LEGAL ADVICE / VERIFY ALL CITATIONS."
- **Tests must pass.** Run `pytest -q` before committing.

## Boundaries — what Claude Code should NOT do
- Never commit `.env` or any file containing API keys
- Never make live Exa API calls in tests (use mocks/cache)
- Never claim outputs are verified legal advice
- Never remove safety disclaimers from notebooks or exports
- Never install packages not in requirements.txt without asking

## Branch naming
- `chore/` — repo setup, docs, config
- `feat/` — new functionality
- `fix/` — bug fixes

## Current phase
Phase 1 (Prompt #1): Foundation — Cells 0–2 + docs + tests.
No Exa API calls yet. Cache system and query plan only.
