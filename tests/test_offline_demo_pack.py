"""Offline demo pack validation.

Loads cache_samples/<case_key>/*.json and validates
required keys exist and lists are non-empty.

No network calls — tests the committed fixture data.
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

ROOT = Path(__file__).resolve().parent.parent
SAMPLES_DIR = ROOT / "cache_samples" / "milton_citizens_pinellas"


def _load(name: str) -> dict:
    path = SAMPLES_DIR / f"{name}.json"
    if not path.exists():
        pytest.skip(f"Cache sample not seeded yet: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


class TestWeatherSample:
    def test_has_required_keys(self):
        data = _load("weather")
        assert data["module"] == "weather"
        assert "event_summary" in data
        assert "key_observations" in data
        assert "metrics" in data
        assert "sources" in data

    def test_has_observations(self):
        data = _load("weather")
        assert len(data["key_observations"]) > 0

    def test_has_sources(self):
        data = _load("weather")
        assert len(data["sources"]) > 0
        for s in data["sources"]:
            assert "url" in s
            assert "badge" in s


class TestCarrierSample:
    def test_has_required_keys(self):
        data = _load("carrier")
        assert data["module"] == "carrier"
        assert "carrier_snapshot" in data
        assert "document_pack" in data
        assert "common_defenses" in data
        assert "rebuttal_angles" in data
        assert "sources" in data

    def test_has_documents(self):
        data = _load("carrier")
        assert len(data["document_pack"]) > 0

    def test_has_rebuttals(self):
        data = _load("carrier")
        assert len(data["rebuttal_angles"]) > 0


class TestCaselawSample:
    def test_has_required_keys(self):
        data = _load("caselaw")
        assert data["module"] == "caselaw"
        assert "issues" in data
        assert "sources" in data

    def test_has_issues(self):
        data = _load("caselaw")
        assert len(data["issues"]) > 0

    def test_issues_have_cases(self):
        data = _load("caselaw")
        total_cases = sum(len(i["cases"]) for i in data["issues"])
        assert total_cases >= 1


class TestCitationVerifySample:
    def test_has_required_keys(self):
        data = _load("citation_verify")
        assert data["module"] == "citation_verify"
        assert "disclaimer" in data
        assert "checks" in data
        assert "summary" in data

    def test_has_checks(self):
        data = _load("citation_verify")
        assert len(data["checks"]) > 0

    def test_summary_totals(self):
        data = _load("citation_verify")
        s = data["summary"]
        assert s["total"] == len(data["checks"])
        assert s["total"] == s["verified"] + s["uncertain"] + s["not_found"]
