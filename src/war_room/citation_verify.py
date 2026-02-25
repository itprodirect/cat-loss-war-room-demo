"""Citation spot-check module.

For each case citation, runs ONE Exa search to check if it appears
on a court/legal site. Reports confidence level, not verification.

Mandatory disclaimer: KeyCite/Shepardize before reliance.
"""

from __future__ import annotations

from typing import Any

from war_room.cache_io import cached_call
from war_room.exa_client import ExaClient
from war_room.source_scoring import score_url


DISCLAIMER = (
    "CITATION SPOT-CHECK ONLY — These are confidence signals, not verification. "
    "KeyCite / Shepardize every citation before reliance."
)


def spot_check_citations(
    caselaw_pack: dict[str, Any],
    client: ExaClient,
    *,
    use_cache: bool = True,
    cache_dir: str = "cache",
    cache_samples_dir: str = "cache_samples",
) -> dict[str, Any]:
    """Spot-check all citations in a caselaw pack.

    Returns dict with: module, disclaimer, checks, summary.
    """
    case_key_base = "citecheck"
    # Gather all cases from the pack
    all_cases = []
    for issue in caselaw_pack.get("issues", []):
        for case in issue.get("cases", []):
            if case.get("name"):
                all_cases.append(case)

    checks = []
    for case in all_cases:
        name = case.get("name", "")
        citation = case.get("citation", "")
        search_term = f"{name} {citation}".strip()
        if not search_term:
            continue

        check_key = f"{case_key_base}__{search_term}"

        def _verify(q=search_term) -> dict[str, Any]:
            return _do_check(q, client)

        result = cached_call(
            check_key, _verify,
            cache_samples_dir=cache_samples_dir,
            cache_dir=cache_dir,
            use_cache=use_cache,
        )
        result["case_name"] = name
        result["citation"] = citation
        checks.append(result)

    # Summary counts
    verified = sum(1 for c in checks if c["status"] == "verified")
    uncertain = sum(1 for c in checks if c["status"] == "uncertain")
    not_found = sum(1 for c in checks if c["status"] == "not_found")

    return {
        "module": "citation_verify",
        "disclaimer": DISCLAIMER,
        "checks": checks,
        "summary": {
            "total": len(checks),
            "verified": verified,
            "uncertain": uncertain,
            "not_found": not_found,
        },
    }


def _do_check(query: str, client: ExaClient) -> dict[str, Any]:
    """Run a single citation spot-check."""
    try:
        hits = client.search(query, k=3)
    except Exception:
        return {
            "status": "not_found",
            "badge": "❌",
            "source_url": None,
            "note": "Search failed",
        }

    if not hits:
        return {
            "status": "not_found",
            "badge": "❌",
            "source_url": None,
            "note": "No results found",
        }

    # Check the best hit
    best = hits[0]
    score = score_url(best["url"])

    if score["tier"] == "official":
        return {
            "status": "verified",
            "badge": "✅",
            "source_url": best["url"],
            "note": f"Found on official source: {score['hostname']}",
        }
    elif score["tier"] == "professional":
        return {
            "status": "uncertain",
            "badge": "⚠️",
            "source_url": best["url"],
            "note": f"Found on professional source: {score['hostname']} — verify independently",
        }
    else:
        return {
            "status": "uncertain",
            "badge": "⚠️",
            "source_url": best["url"],
            "note": f"Found on {score['hostname']} — unvetted source, verify independently",
        }
