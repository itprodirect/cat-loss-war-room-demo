# CAT-Loss War Room

AI-powered catastrophic insurance loss litigation research tool.
Built for demo at Merlin Law Group.

> **DEMO RESEARCH MEMO — NOT LEGAL ADVICE**
> All outputs are for demonstration purposes only. Verify all citations
> independently before any legal reliance. See [SAFETY_GUARDRAILS.md](docs/SAFETY_GUARDRAILS.md).

## Quickstart

```bash
# Clone and setup
git clone <repo-url>
cd cat-loss-war-room-demo
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Copy env template
cp .env.example .env
# Edit .env to add your EXA_API_KEY (optional — demo runs from cache)

# Run tests
pytest -q

# Open the notebook
jupyter notebook notebooks/01_case_war_room.ipynb
```

## What it does

Given a catastrophic loss case (hurricane, hail, etc.), the war room notebook:

1. **Intake** — Captures case facts (location, date, carrier, policy type, posture)
2. **Query Plan** — Generates 12–18 targeted research queries across three modules
3. **Weather Intel** — Gathers official weather data (.gov sources preferred)
4. **Carrier Playbook** — Finds carrier denial patterns, regulatory actions, rebuttal angles
5. **Case Law** — Searches relevant precedent organized by legal issue
6. **Export** — Produces a structured research memo with source confidence badges

## Jupyter Kernel (required)

The notebook must run against the project venv. Register it once:

```bash
source .venv/bin/activate
python -m pip install ipykernel
python -m ipykernel install --user --name cat-loss-war-room-demo --display-name "cat-loss-war-room-demo (.venv)"
```

Then in JupyterLab select **Kernel → Change Kernel → cat-loss-war-room-demo (.venv)**.

## Offline Demo

No API key needed — cached results are committed in `cache_samples/`.

```bash
# Ensure USE_CACHE=true in .env (the default)
source .venv/bin/activate
jupyter notebook notebooks/01_case_war_room.ipynb
# Run All — should complete in < 10 seconds
```

## Current Status

**Phase 2 complete:** Cells 0–7 fully wired — weather, carrier, caselaw, citation spot-check, and markdown export all functional. Offline demo runs from committed cache samples. 75 tests passing.

## Project Structure

See [CLAUDE.md](CLAUDE.md) for full repo layout and conventions.

## Disclaimer

This tool is a research accelerator, not a legal oracle. All outputs carry:
- Source confidence badges (🟢 official / 🟡 professional / 🔴 unvetted)
- Mandatory "VERIFY ALL CITATIONS" disclaimers
- "DRAFT — ATTORNEY WORK PRODUCT" watermarks on exports

No output should be used without independent verification by a licensed attorney.
