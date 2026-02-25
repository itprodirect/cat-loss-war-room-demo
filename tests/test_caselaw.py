"""Tests for caselaw_module — no network calls."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from war_room.caselaw_module import _assemble_pack, _extract_case_info
from war_room.query_plan import CaseIntake


def _sample_intake():
    return CaseIntake(
        event_name="Hurricane Milton",
        event_date="2024-10-09",
        state="FL",
        county="Pinellas",
        carrier="Citizens Property Insurance",
        policy_type="HO-3 Dwelling",
        posture=["denial"],
    )


def test_assemble_pack_structure():
    results = [
        {
            "url": "https://scholar.google.com/case1",
            "title": "Citizens v. Homeowner",
            "snippet": "Coverage dispute involving wind damage",
            "text": "Citizens Property Insurance Corp v. Homeowner, 123 So. 3d 456 (Fla. App. 2023). The court held that...",
            "category": "carrier_precedent",
        },
    ]
    pack = _assemble_pack(_sample_intake(), results)
    assert pack["module"] == "caselaw"
    assert isinstance(pack["issues"], list)
    assert isinstance(pack["sources"], list)


def test_extract_case_info():
    result = {
        "url": "https://scholar.google.com/case",
        "title": "Smith v. Insurance Co",
        "snippet": "Wind damage coverage case",
        "text": "Smith v. Insurance Co, 234 So. 3d 789 (Fla. App. 2022). The court found coverage...",
        "_score": {"tier": "professional", "badge": "🟡"},
    }
    info = _extract_case_info(result)
    assert info["name"] == "Smith v. Insurance Co"
    assert info["url"] == "https://scholar.google.com/case"
    assert info["badge"] == "🟡"
    assert "citation" in info
    assert "year" in info


def test_pack_limits_cases():
    """Pack should return at most 12 cases total."""
    results = [
        {
            "url": f"https://example.com/case{i}",
            "title": f"Case {i}",
            "snippet": f"Case {i} snippet",
            "text": f"Case {i} text about insurance in 2024",
            "category": "coverage_law",
        }
        for i in range(30)
    ]
    pack = _assemble_pack(_sample_intake(), results)
    total = sum(len(issue["cases"]) for issue in pack["issues"])
    assert total <= 12
