"""Tests for carrier_module — no network calls."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from war_room.carrier_module import _assemble_pack, _extract_defenses, _build_rebuttals
from war_room.query_plan import CaseIntake


def _sample_intake():
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


def test_assemble_pack_structure():
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


def test_extract_defenses():
    intake = _sample_intake()
    results = [
        {"text": "The carrier argued pre-existing damage and wear and tear exclusion"},
    ]
    defenses = _extract_defenses(results, intake)
    assert any("pre-existing" in d.lower() for d in defenses)
    assert any("wear and tear" in d.lower() for d in defenses)


def test_build_rebuttals_includes_key_facts():
    intake = _sample_intake()
    rebuttals = _build_rebuttals(intake, [], [])
    assert any("Roof damage" in r for r in rebuttals)


def test_build_rebuttals_bad_faith():
    intake = _sample_intake()
    rebuttals = _build_rebuttals(intake, [], [])
    assert any("bad faith" in r.lower() for r in rebuttals)
