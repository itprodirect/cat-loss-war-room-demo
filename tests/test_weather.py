"""Tests for weather_module — no network calls, uses mock/cache."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from war_room.weather_module import _extract_metrics, _assemble_brief
from war_room.query_plan import CaseIntake


def _sample_intake():
    return CaseIntake(
        event_name="Hurricane Milton",
        event_date="2024-10-09",
        state="FL",
        county="Pinellas",
        carrier="Citizens Property Insurance",
        policy_type="HO-3 Dwelling",
    )


def test_extract_metrics_wind():
    text = "Maximum sustained winds of 120 mph were recorded near landfall."
    m = _extract_metrics(text)
    assert m["max_wind_mph"] == 120


def test_extract_metrics_surge():
    text = "Storm surge of 8.5 feet was observed along the coast."
    m = _extract_metrics(text)
    assert m["storm_surge_ft"] == 8.5


def test_extract_metrics_rain():
    text = "The area received 12.3 inches of rainfall over 24 hours."
    m = _extract_metrics(text)
    assert m["rain_in"] == 12.3


def test_extract_metrics_none():
    text = "The storm caused significant damage to the region."
    m = _extract_metrics(text)
    assert m["max_wind_mph"] is None
    assert m["storm_surge_ft"] is None
    assert m["rain_in"] is None


def test_assemble_brief_structure():
    results = [
        {
            "url": "https://weather.gov/report",
            "title": "NWS Report",
            "snippet": "Winds reached 110 mph in Pinellas County",
            "text": "Winds reached 110 mph in Pinellas County during Milton.",
            "category": "wind_data",
        },
        {
            "url": "https://fema.gov/disaster",
            "title": "FEMA Declaration",
            "snippet": "Major disaster declared for FL",
            "text": "FEMA major disaster declaration for Hurricane Milton FL.",
            "category": "fema_declaration",
        },
    ]
    brief = _assemble_brief(_sample_intake(), results)
    assert brief["module"] == "weather"
    assert "event_summary" in brief
    assert isinstance(brief["key_observations"], list)
    assert isinstance(brief["metrics"], dict)
    assert isinstance(brief["sources"], list)
    assert len(brief["sources"]) == 2
