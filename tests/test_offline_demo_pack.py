"""Offline demo pack validation.

Loads cache_samples/<case_key>/*.json and validates
required keys exist and lists are non-empty.

No network calls - tests the committed fixture data.
"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SAMPLES_DIR = ROOT / "cache_samples" / "milton_citizens_pinellas"

_GENERIC_CARRIER_TITLES = {
    "consumers - floir",
    "contact us - floir",
    "organization and operation - floir",
}

_GENERIC_WEATHER_TITLES = {
    "hurricane costs",
    "news and media: disaster 4834 - fema",
    "dr-4834 public notice 001 - fema.gov",
}

_CASE_COMMENTARY_MARKERS = (
    "jd supra",
    "what homeowners must know",
    "in the wake of hurricane",
)


def _load(name: str) -> dict:
    path = SAMPLES_DIR / f"{name}.json"
    if not path.exists():
        pytest.skip(f"Cache sample not seeded yet: {path}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


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

    def test_excludes_generic_weather_reference_pages(self):
        data = _load("weather")
        titles = {source["title"].strip().lower() for source in data["sources"]}
        assert not titles.intersection(_GENERIC_WEATHER_TITLES)


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

    def test_excludes_generic_regulator_navigation_pages(self):
        data = _load("carrier")
        titles = {document["title"].strip().lower() for document in data["document_pack"]}
        assert not titles.intersection(_GENERIC_CARRIER_TITLES)


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

    def test_excludes_commentary_titles_from_case_entries(self):
        data = _load("caselaw")
        case_titles = [case["name"].lower() for issue in data["issues"] for case in issue["cases"]]
        for marker in _CASE_COMMENTARY_MARKERS:
            assert all(marker not in title for title in case_titles)


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

    def test_checks_reference_case_titles_not_commentary(self):
        data = _load("citation_verify")
        case_titles = [check["case_name"].lower() for check in data["checks"]]
        for marker in _CASE_COMMENTARY_MARKERS:
            assert all(marker not in title for title in case_titles)
