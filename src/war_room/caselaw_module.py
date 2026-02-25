"""Case law search module.

Runs caselaw queries via Exa. Organizes results by legal issue.
Prefers CourtListener / official courts / scholar.google.com.
Avoids Westlaw/Lexis as primary sources.
"""

from __future__ import annotations

import re
from typing import Any

from war_room.cache_io import cached_call
from war_room.exa_client import ExaClient
from war_room.query_plan import CaseIntake, generate_query_plan
from war_room.source_scoring import score_url, PAYWALLED_DOMAINS

CASELAW_EXCLUDE_DOMAINS = list(PAYWALLED_DOMAINS)

_CASE_NAME_RE = re.compile(r"(?:^|\s)(v\.|vs\.|in re|ex rel\.)(?:\s|$)", re.IGNORECASE)


def _is_case_like(result: dict) -> bool:
    """Conservative guard: keep only results that look like actual cases."""
    # Has a citation extracted → likely a case
    if result.get("citation"):
        return True
    # Title matches a case-name pattern (e.g. "Smith v. Jones")
    name = result.get("name", "") or result.get("title", "") or ""
    return bool(_CASE_NAME_RE.search(name))


def build_caselaw_pack(
    intake: CaseIntake,
    client: ExaClient,
    *,
    use_cache: bool = True,
    cache_dir: str = "cache",
    cache_samples_dir: str = "cache_samples",
) -> dict[str, Any]:
    """Build a case law pack organized by legal issue."""
    case_key = f"caselaw__{intake.event_name}__{intake.carrier}__{intake.state}"

    def _fetch() -> dict[str, Any]:
        queries = [q for q in generate_query_plan(intake) if q.module == "caselaw"]
        all_results: list[dict] = []

        for q in queries:
            hits = client.search(
                q.query,
                k=5,
                include_domains=q.preferred_domains or None,
                exclude_domains=CASELAW_EXCLUDE_DOMAINS,
            )
            for h in hits:
                h["category"] = q.category
            all_results.extend(hits)

        return _assemble_pack(intake, all_results)

    return cached_call(
        case_key, _fetch,
        cache_samples_dir=cache_samples_dir,
        cache_dir=cache_dir,
        use_cache=use_cache,
    )


def _assemble_pack(
    intake: CaseIntake, results: list[dict]
) -> dict[str, Any]:
    """Organize results by legal issue."""
    # Deduplicate
    seen: set[str] = set()
    unique: list[dict] = []
    for r in results:
        if r["url"] and r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    # Score and filter out paywalled
    scored = []
    for r in unique:
        s = score_url(r["url"])
        if s["tier"] != "paywalled":
            scored.append({**r, "_score": s})

    # Map categories to legal issues
    issue_map = {
        "carrier_precedent": f"{intake.carrier} Precedent",
        "coverage_law": "Coverage / Denial Law",
        "concurrent_causation": "Concurrent Causation Doctrine",
        "bad_faith_precedent": "Bad Faith Standards",
        "bad_faith_law": "Bad Faith — Duty to Investigate",
        "underpayment_law": "Underpayment / Appraisal",
        "coverage_issue": "Coverage Issue",
    }

    # Group by issue
    issues_dict: dict[str, list[dict]] = {}
    for r in scored:
        cat = r.get("category", "general")
        issue_label = issue_map.get(cat, cat.replace("_", " ").title())
        issues_dict.setdefault(issue_label, []).append(r)

    # Build issues list, limit to 6-12 cases total
    issues = []
    total_cases = 0
    for issue_label, issue_results in issues_dict.items():
        if total_cases >= 12:
            break
        cases = []
        for r in issue_results[:6]:  # scan up to 6, keep max 3
            if total_cases >= 12 or len(cases) >= 3:
                break
            case_info = _extract_case_info(r)
            if not _is_case_like(case_info):
                continue
            cases.append(case_info)
            total_cases += 1

        if cases:
            issues.append({
                "issue": issue_label,
                "cases": cases,
                "notes": [_issue_note(issue_label, intake)],
            })

    # Sources
    sources = []
    for r in scored[:15]:
        s = r["_score"]
        sources.append({
            "title": r.get("title", ""),
            "url": r["url"],
            "badge": s["badge"],
            "reason": s["label"],
        })

    return {
        "module": "caselaw",
        "issues": issues,
        "sources": sources,
    }


def _extract_case_info(result: dict) -> dict[str, Any]:
    """Extract case name, citation, court, year from a search result."""
    title = result.get("title", "") or ""
    text = result.get("text", "") or ""
    snippet = result.get("snippet", "") or ""
    s = result["_score"]

    # Try to extract case name from title
    case_name = title.strip()

    # Try to find a citation pattern (e.g., "123 So. 3d 456" or "2024 WL 12345")
    citation = ""
    cite_patterns = [
        r'\d+\s+(?:So\.|F\.|S\.W\.|N\.E\.|N\.W\.|P\.|A\.)\s*\d*d?\s+\d+',
        r'\d{4}\s+WL\s+\d+',
        r'\d+\s+F\.\s*(?:Supp|App)\.\s*\d*d?\s+\d+',
    ]
    for pat in cite_patterns:
        m = re.search(pat, text[:1000])
        if m:
            citation = m.group(0)
            break

    # Try to extract court
    court = ""
    court_patterns = [
        r'(?:Supreme Court|Circuit Court|District Court|Court of Appeal)[^.]{0,30}',
        r'(?:Fla\.|Cal\.|Tex\.|N\.Y\.)\s*(?:App\.|Dist\.)?\s*\d{4}',
    ]
    for pat in court_patterns:
        m = re.search(pat, text[:1000], re.IGNORECASE)
        if m:
            court = m.group(0).strip()
            break

    # Year
    year = ""
    year_match = re.search(r'\b(19|20)\d{2}\b', text[:500])
    if year_match:
        year = year_match.group(0)

    # One-liner from snippet
    one_liner = snippet[:200].strip()
    if not one_liner:
        one_liner = text[:200].strip()

    return {
        "name": case_name,
        "citation": citation,
        "court": court,
        "year": year,
        "one_liner": one_liner,
        "url": result["url"],
        "badge": s["badge"],
    }


def _issue_note(issue_label: str, intake: CaseIntake) -> str:
    """Generate a contextual note for a legal issue."""
    notes = {
        "Concurrent Causation Doctrine": (
            f"Key issue in {intake.state} hurricane cases — "
            f"determines whether wind or water exclusion controls"
        ),
        "Bad Faith Standards": (
            f"Review {intake.state} bad faith standards — "
            f"statutory penalties and fee-shifting may apply"
        ),
        "Bad Faith — Duty to Investigate": (
            f"Failure to adequately investigate is a common bad faith theory in {intake.state}"
        ),
    }
    return notes.get(
        issue_label,
        f"Review for applicability to {intake.carrier} / {intake.event_name}"
    )
