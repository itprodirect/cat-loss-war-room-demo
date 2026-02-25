"""Tests for export_md module — no network calls."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from war_room.export_md import render_markdown_memo, write_markdown
from war_room.query_plan import CaseIntake, QuerySpec


def _sample_data():
    intake = CaseIntake(
        event_name="Hurricane Milton",
        event_date="2024-10-09",
        state="FL",
        county="Pinellas",
        carrier="Citizens Property Insurance",
        policy_type="HO-3 Dwelling",
        posture=["denial"],
    )
    weather = {
        "module": "weather",
        "event_summary": "Hurricane Milton — Pinellas County, FL",
        "key_observations": ["Winds of 120 mph"],
        "metrics": {"max_wind_mph": 120, "storm_surge_ft": None, "rain_in": None},
        "sources": [{"title": "NWS Report", "url": "https://weather.gov/r", "badge": "🟢", "reason": "Official"}],
    }
    carrier = {
        "module": "carrier",
        "carrier_snapshot": {"name": "Citizens", "state": "FL", "event": "Milton", "policy_type": "HO-3"},
        "document_pack": [{"doc_type": "Denial", "title": "Doc", "url": "https://example.com", "badge": "🟡", "why_it_matters": "Relevant"}],
        "common_defenses": ["Pre-existing damage"],
        "rebuttal_angles": ["Timeline contradicts carrier position"],
        "sources": [{"title": "Article", "url": "https://example.com", "badge": "🟡", "reason": "Professional"}],
    }
    caselaw = {
        "module": "caselaw",
        "issues": [{"issue": "Coverage", "cases": [{"name": "Doe v. Ins", "citation": "123 So.3d 456", "court": "Fla. App.", "year": "2023", "one_liner": "Coverage upheld", "url": "https://example.com", "badge": "🟡"}], "notes": ["Relevant"]}],
        "sources": [{"title": "Case", "url": "https://example.com/c", "badge": "🟡", "reason": "Professional"}],
    }
    citecheck = {
        "module": "citation_verify",
        "disclaimer": "SPOT-CHECK ONLY",
        "checks": [{"badge": "✅", "case_name": "Doe v. Ins", "citation": "123 So.3d 456", "status": "verified", "note": "Found on official source"}],
        "summary": {"total": 1, "verified": 1, "uncertain": 0, "not_found": 0},
    }
    queries = [QuerySpec(module="weather", query="test query", category="test")]
    return intake, weather, carrier, caselaw, citecheck, queries


def test_render_contains_all_sections():
    md = render_markdown_memo(*_sample_data())
    assert "DRAFT" in md
    assert "ATTORNEY WORK PRODUCT" in md
    assert "DEMO RESEARCH MEMO" in md
    assert "Case Intake" in md
    assert "Weather Corroboration" in md
    assert "Carrier Document Pack" in md
    assert "Case Law" in md
    assert "Citation Spot-Check" in md
    assert "Query Plan" in md
    assert "All Sources" in md
    assert "Methodology" in md


def test_render_contains_case_details():
    md = render_markdown_memo(*_sample_data())
    assert "Hurricane Milton" in md
    assert "Citizens" in md
    assert "Pinellas" in md


def test_write_markdown_creates_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = write_markdown(tmpdir, "test_case", "# Test Memo\nContent here")
        assert path.exists()
        assert path.read_text(encoding="utf-8").startswith("# Test Memo")
        assert "test_case" in path.name
