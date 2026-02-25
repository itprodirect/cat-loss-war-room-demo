"""Carrier playbook intel module.

Runs carrier_docs queries via Exa. Builds a document pack with
denial patterns, regulatory signals, and rebuttal angles.
"""

from __future__ import annotations

from typing import Any

from war_room.cache_io import cached_call
from war_room.exa_client import ExaClient
from war_room.query_plan import CaseIntake, generate_query_plan
from war_room.source_scoring import score_url


def build_carrier_doc_pack(
    intake: CaseIntake,
    client: ExaClient,
    *,
    use_cache: bool = True,
    cache_dir: str = "cache",
    cache_samples_dir: str = "cache_samples",
) -> dict[str, Any]:
    """Build a carrier document pack for the case."""
    case_key = f"carrier__{intake.carrier}__{intake.event_name}__{intake.state}"

    def _fetch() -> dict[str, Any]:
        queries = [q for q in generate_query_plan(intake) if q.module == "carrier_docs"]
        all_results: list[dict] = []

        for q in queries:
            hits = client.search(
                q.query,
                k=5,
                include_domains=q.preferred_domains or None,
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
    """Assemble carrier doc pack from raw results."""
    # Deduplicate
    seen: set[str] = set()
    unique: list[dict] = []
    for r in results:
        if r["url"] and r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    # Score
    scored = []
    for r in unique:
        s = score_url(r["url"])
        scored.append({**r, "_score": s})

    # Categorize into document types
    doc_type_map = {
        "denial_patterns": "Denial Pattern Analysis",
        "doi_complaints": "DOI/Regulatory Complaint",
        "regulatory_action": "Regulatory Action",
        "claims_manual": "Claims Handling Guideline",
        "bad_faith_history": "Bad Faith Signal",
    }

    document_pack = []
    for r in scored[:15]:
        cat = r.get("category", "general")
        s = r["_score"]
        document_pack.append({
            "doc_type": doc_type_map.get(cat, "General"),
            "title": r.get("title", ""),
            "url": r["url"],
            "badge": s["badge"],
            "why_it_matters": _why_it_matters(cat, r, intake),
        })

    # Build common defenses from denial_patterns results
    common_defenses = _extract_defenses(
        [r for r in scored if r.get("category") == "denial_patterns"],
        intake,
    )

    # Build rebuttal angles
    rebuttal_angles = _build_rebuttals(intake, common_defenses, scored)

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
        "module": "carrier",
        "carrier_snapshot": {
            "name": intake.carrier,
            "state": intake.state,
            "event": intake.event_name,
            "policy_type": intake.policy_type,
        },
        "document_pack": document_pack[:12],
        "common_defenses": common_defenses,
        "rebuttal_angles": rebuttal_angles,
        "sources": sources,
    }


def _why_it_matters(category: str, result: dict, intake: CaseIntake) -> str:
    """Generate a short 'why it matters' note for a document."""
    snippet = (result.get("snippet", "") or "")[:200].strip()
    if category == "denial_patterns":
        return f"Documents {intake.carrier} denial patterns — {snippet[:100]}"
    elif category == "doi_complaints":
        return f"Regulatory complaint record — may signal systemic issues"
    elif category == "regulatory_action":
        return f"Regulatory action against {intake.carrier} — supports bad faith narrative"
    elif category == "claims_manual":
        return f"Internal claims handling standards — compare to actual handling"
    elif category == "bad_faith_history":
        return f"Prior bad faith signals for {intake.carrier} in {intake.state}"
    return snippet[:150] if snippet else "Potentially relevant carrier document"


def _extract_defenses(denial_results: list[dict], intake: CaseIntake) -> list[str]:
    """Extract common carrier defenses from denial pattern results."""
    defenses = []
    all_text = " ".join(r.get("text", "") for r in denial_results).lower()

    defense_patterns = [
        ("pre-existing", f"{intake.carrier} may argue damage was pre-existing"),
        ("wear and tear", "Wear and tear / maintenance exclusion defense"),
        ("flood exclu", "Flood exclusion — wind vs. water causation dispute"),
        ("concurrent caus", "Anti-concurrent causation clause defense"),
        ("late notice", "Late notice / failure to mitigate defense"),
        ("policy exclu", "Policy exclusion defense"),
    ]
    for pattern, defense in defense_patterns:
        if pattern in all_text:
            defenses.append(defense)

    if not defenses:
        defenses.append(f"Standard denial defenses for {intake.policy_type} claims")

    return defenses


def _build_rebuttals(
    intake: CaseIntake,
    defenses: list[str],
    scored_results: list[dict],
) -> list[str]:
    """Generate rebuttal angles from case facts and carrier data."""
    rebuttals = []

    for fact in intake.key_facts:
        rebuttals.append(f"Key fact undermines carrier position: {fact}")

    if any("pre-existing" in d.lower() for d in defenses):
        rebuttals.append(
            "Counter pre-existing defense: damage timeline correlates with event date"
        )
    if any("concurrent" in d.lower() for d in defenses):
        rebuttals.append(
            "Counter ACC clause: efficient proximate cause doctrine may apply in "
            f"{intake.state}"
        )
    if "bad_faith" in intake.posture:
        rebuttals.append(
            f"Bad faith signal: investigate {intake.carrier}'s claims handling "
            f"timeline and investigation adequacy"
        )

    # Add regulatory angle if DOI results found
    doi_results = [r for r in scored_results if r.get("category") == "doi_complaints"]
    if doi_results:
        rebuttals.append(
            f"Regulatory record: {len(doi_results)} DOI/regulatory results found — "
            f"may support pattern-of-conduct argument"
        )

    return rebuttals
