"""Tests for caselaw_module - no network calls."""

import tempfile
from pathlib import Path

from war_room.caselaw_module import _assemble_pack, _extract_case_info, build_caselaw_pack
from war_room.query_plan import CaseIntake


def _sample_intake() -> CaseIntake:
    return CaseIntake(
        event_name="Hurricane Milton",
        event_date="2024-10-09",
        state="FL",
        county="Pinellas",
        carrier="Citizens Property Insurance",
        policy_type="HO-3 Dwelling",
        posture=["denial"],
    )


def test_assemble_pack_structure() -> None:
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


def test_extract_case_info() -> None:
    result = {
        "url": "https://scholar.google.com/case",
        "title": "Smith v. Insurance Co",
        "snippet": "Wind damage coverage case",
        "text": "Smith v. Insurance Co, 234 So. 3d 789 (Fla. App. 2022). The court found coverage...",
        "_score": {"tier": "professional", "badge": "X"},
    }
    info = _extract_case_info(result)
    assert info["name"] == "Smith v. Insurance Co"
    assert info["url"] == "https://scholar.google.com/case"
    assert info["badge"] == "X"
    assert "citation" in info
    assert "year" in info


def test_pack_limits_cases() -> None:
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


def test_build_caselaw_pack_without_client_returns_structured_fallback() -> None:
    intake = _sample_intake()
    with tempfile.TemporaryDirectory() as cache_dir, tempfile.TemporaryDirectory() as samples_dir:
        pack = build_caselaw_pack(
            intake,
            client=None,
            use_cache=False,
            cache_dir=cache_dir,
            cache_samples_dir=samples_dir,
        )

    assert pack["module"] == "caselaw"
    assert pack["issues"] == []
    assert pack["sources"] == []
    assert "warnings" in pack
    assert any("No Exa client available" in warning for warning in pack["warnings"])
