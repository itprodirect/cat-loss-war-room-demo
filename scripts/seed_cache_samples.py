"""Seed cache_samples with live Exa results for offline demo.

Usage:
    # Set your API key first
    export EXA_API_KEY=your_key_here

    # Run from repo root
    python scripts/seed_cache_samples.py

This makes LIVE Exa API calls (costs ~$0.30-0.50).
Results are saved to cache_samples/<case_key>/ for offline demo.

Do NOT run this in CI — it's a manual, one-time step.
"""

import json
import shutil
import sys
from pathlib import Path

# Add src to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from war_room.exa_client import ExaClient
from war_room.query_plan import CaseIntake, generate_query_plan
from war_room.weather_module import build_weather_brief
from war_room.carrier_module import build_carrier_doc_pack
from war_room.caselaw_module import build_caselaw_pack
from war_room.citation_verify import spot_check_citations


def default_intake() -> CaseIntake:
    """The primary demo case: Milton / Citizens / Pinellas."""
    return CaseIntake(
        event_name="Hurricane Milton",
        event_date="2024-10-09",
        state="FL",
        county="Pinellas",
        carrier="Citizens Property Insurance",
        policy_type="HO-3 Dwelling",
        posture=["denial", "bad_faith"],
        key_facts=[
            "Category 3 at landfall near Siesta Key",
            "Roof damage + water intrusion reported within 48 hours",
            "Claim denied citing pre-existing conditions",
        ],
        coverage_issues=[
            "wind vs water causation",
            "anti-concurrent causation clause",
            "duty to investigate",
        ],
    )


def main():
    intake = default_intake()
    case_key = "milton_citizens_pinellas"
    cache_dir = ROOT / "cache"
    samples_dir = ROOT / "cache_samples"

    print(f"Seeding cache_samples for: {intake.summary()}")
    print(f"Output dir: {samples_dir}")
    print()

    client = ExaClient(max_search_calls=40)
    print(f"Exa client initialized. Budget: {client.max_search_calls} calls")
    print()

    # --- Weather ---
    print("[1/4] Fetching weather data...")
    weather = build_weather_brief(
        intake, client, use_cache=False,
        cache_dir=str(cache_dir), cache_samples_dir=str(samples_dir),
    )
    print(f"  -> {len(weather.get('sources', []))} sources, "
          f"{len(weather.get('key_observations', []))} observations")

    # --- Carrier ---
    print("[2/4] Fetching carrier data...")
    carrier = build_carrier_doc_pack(
        intake, client, use_cache=False,
        cache_dir=str(cache_dir), cache_samples_dir=str(samples_dir),
    )
    print(f"  -> {len(carrier.get('document_pack', []))} documents, "
          f"{len(carrier.get('rebuttal_angles', []))} rebuttals")

    # --- Case Law ---
    print("[3/4] Fetching case law...")
    caselaw = build_caselaw_pack(
        intake, client, use_cache=False,
        cache_dir=str(cache_dir), cache_samples_dir=str(samples_dir),
    )
    total_cases = sum(len(i.get("cases", [])) for i in caselaw.get("issues", []))
    print(f"  -> {len(caselaw.get('issues', []))} issues, {total_cases} cases")

    # --- Citation verify ---
    print("[4/4] Running citation spot-checks...")
    citecheck = spot_check_citations(
        caselaw, client, use_cache=False,
        cache_dir=str(cache_dir), cache_samples_dir=str(samples_dir),
    )
    summary = citecheck.get("summary", {})
    print(f"  -> {summary.get('total', 0)} checked: "
          f"{summary.get('verified', 0)} verified, "
          f"{summary.get('uncertain', 0)} uncertain, "
          f"{summary.get('not_found', 0)} not found")

    print(f"\nTotal Exa calls used: {client.search_count}/{client.max_search_calls}")

    # Now copy the relevant cache files into cache_samples under the case key
    out_dir = samples_dir / case_key
    out_dir.mkdir(parents=True, exist_ok=True)

    # Save structured outputs directly as named JSON files
    for name, data in [
        ("weather", weather),
        ("carrier", carrier),
        ("caselaw", caselaw),
        ("citation_verify", citecheck),
    ]:
        path = out_dir / f"{name}.json"
        path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
        print(f"  Saved: {path}")

    # Copy relevant raw cache files so cached_call finds them on next run.
    # Only copy weather/carrier/caselaw/citecheck keys, not unrelated noise.
    RELEVANT_PREFIXES = ("weather_", "carrier_", "caselaw_", "citecheck_")
    cache_dir_path = Path(cache_dir)
    if cache_dir_path.exists():
        for f in cache_dir_path.glob("*.json"):
            if not any(f.name.startswith(p) for p in RELEVANT_PREFIXES):
                continue
            dest = samples_dir / f.name
            shutil.copy2(f, dest)  # overwrite stale fixtures
            print(f"  Copied cache -> samples: {f.name}")

    print(f"\nDone! Cache samples seeded in {out_dir}")
    print("Commit cache_samples/ to make offline demo work on clone.")


if __name__ == "__main__":
    main()
