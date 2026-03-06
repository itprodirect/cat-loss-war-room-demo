"""Tests for carrier_module - no network calls."""

import tempfile
from pathlib import Path

from war_room.carrier_module import (
    _assemble_pack,
    _build_rebuttals,
    _extract_defenses,
    build_carrier_doc_pack,
)
from war_room.query_plan import CaseIntake


def _sample_intake() -> CaseIntake:
    return CaseIntake(
        event_name="Hurricane Milton",
        event_date="2024-10-09",
        state="FL",
        county="Pinellas",
        carrier="Citizens Property Insurance",
        policy_type="HO-3 Dwelling",
        posture=["denial", "bad_faith"],
        key_facts=["Roof damage reported within 48 hours"],
    )


def test_assemble_pack_structure() -> None:
    results = [
        {
            "url": "https://floir.com/complaint/123",
            "title": "DOI Complaint",
            "snippet": "Citizens Property Insurance complaint filed",
            "text": "Complaint regarding pre-existing damage denial",
            "category": "doi_complaints",
        },
        {
            "url": "https://insurancejournal.com/article",
            "title": "Citizens Denial Patterns",
            "snippet": "Pattern of claim denials after Milton",
            "text": "Citizens has denied claims citing pre-existing conditions and wear and tear",
            "category": "denial_patterns",
        },
    ]
    pack = _assemble_pack(_sample_intake(), results)
    assert pack["module"] == "carrier"
    assert "carrier_snapshot" in pack
    assert isinstance(pack["document_pack"], list)
    assert isinstance(pack["common_defenses"], list)
    assert isinstance(pack["rebuttal_angles"], list)
    assert isinstance(pack["sources"], list)


def test_extract_defenses() -> None:
    intake = _sample_intake()
    results = [
        {"text": "The carrier argued pre-existing damage and wear and tear exclusion"},
    ]
    defenses = _extract_defenses(results, intake)
    assert any("pre-existing" in defense.lower() for defense in defenses)
    assert any("wear and tear" in defense.lower() for defense in defenses)


def test_build_rebuttals_includes_key_facts() -> None:
    intake = _sample_intake()
    rebuttals = _build_rebuttals(intake, [], [])
    assert any("Roof damage" in rebuttal for rebuttal in rebuttals)


def test_build_rebuttals_bad_faith() -> None:
    intake = _sample_intake()
    rebuttals = _build_rebuttals(intake, [], [])
    assert any("bad-faith" in rebuttal.lower() for rebuttal in rebuttals)


def test_build_carrier_pack_without_client_returns_structured_fallback() -> None:
    intake = _sample_intake()
    with tempfile.TemporaryDirectory() as cache_dir, tempfile.TemporaryDirectory() as samples_dir:
        pack = build_carrier_doc_pack(
            intake,
            client=None,
            use_cache=False,
            cache_dir=cache_dir,
            cache_samples_dir=samples_dir,
        )

    assert pack["module"] == "carrier"
    assert pack["document_pack"] == []
    assert pack["common_defenses"] == []
    assert pack["rebuttal_angles"] == []
    assert "warnings" in pack
    assert any("No Exa client available" in warning for warning in pack["warnings"])
