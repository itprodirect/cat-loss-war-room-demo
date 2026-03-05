"""Tests for weather_module - no network calls, uses mock/cache."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from war_room.query_plan import CaseIntake
from war_room.weather_module import _assemble_brief, _extract_metrics, build_weather_brief


def _sample_intake() -> CaseIntake:
    return CaseIntake(
        event_name="Hurricane Milton",
        event_date="2024-10-09",
        state="FL",
        county="Pinellas",
        carrier="Citizens Property Insurance",
        policy_type="HO-3 Dwelling",
    )


def test_extract_metrics_wind() -> None:
    text = "Maximum sustained winds of 120 mph were recorded near landfall."
    metrics = _extract_metrics(text)
    assert metrics["max_wind_mph"] == 120


def test_extract_metrics_surge() -> None:
    text = "Storm surge of 8.5 feet was observed along the coast."
    metrics = _extract_metrics(text)
    assert metrics["storm_surge_ft"] == 8.5


def test_extract_metrics_rain() -> None:
    text = "The area received 12.3 inches of rainfall over 24 hours."
    metrics = _extract_metrics(text)
    assert metrics["rain_in"] == 12.3


def test_extract_metrics_none() -> None:
    text = "The storm caused significant damage to the region."
    metrics = _extract_metrics(text)
    assert metrics["max_wind_mph"] is None
    assert metrics["storm_surge_ft"] is None
    assert metrics["rain_in"] is None


def test_assemble_brief_structure() -> None:
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


def test_build_weather_brief_without_client_returns_structured_fallback() -> None:
    intake = _sample_intake()
    with tempfile.TemporaryDirectory() as cache_dir, tempfile.TemporaryDirectory() as samples_dir:
        brief = build_weather_brief(
            intake,
            client=None,
            use_cache=False,
            cache_dir=cache_dir,
            cache_samples_dir=samples_dir,
        )

    assert brief["module"] == "weather"
    assert brief["sources"] == []
    assert brief["key_observations"] == []
    assert "warnings" in brief
    assert any("No Exa client available" in warning for warning in brief["warnings"])
