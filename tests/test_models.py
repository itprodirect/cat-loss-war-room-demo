"""Tests for Pydantic domain models introduced in issue #6."""

import pytest
from pydantic import ValidationError

from war_room.models import (
    CaseIntake,
    QuerySpec,
    adapt_query_plan,
    case_intake_to_payload,
    query_plan_to_payloads,
    query_spec_to_payload,
)


def test_case_intake_round_trip_dump_and_validate():
    intake = CaseIntake(
        event_name="Hurricane Milton",
        event_date="2024-10-09",
        state="FL",
        county="Pinellas",
        carrier="Citizens Property Insurance",
        policy_type="HO-3 Dwelling",
        posture=["denial", "bad_faith"],
        key_facts=["Roof damage"],
        coverage_issues=["wind_vs_water_causation"],
    )

    payload = intake.model_dump()
    reloaded = CaseIntake.model_validate(payload)

    assert reloaded == intake


def test_case_intake_payload_helper_normalizes_model():
    intake = CaseIntake(
        event_name="Hurricane Milton",
        event_date="2024-10-09",
        state="FL",
        county="Pinellas",
        carrier="Citizens Property Insurance",
        policy_type="HO-3 Dwelling",
    )

    payload = case_intake_to_payload(intake)

    assert payload["event_name"] == "Hurricane Milton"
    assert payload["posture"] == ["denial"]


def test_case_intake_rejects_invalid_date():
    with pytest.raises(ValidationError, match="YYYY-MM-DD"):
        CaseIntake(
            event_name="Hurricane Milton",
            event_date="10/09/2024",
            state="FL",
            county="Pinellas",
            carrier="Citizens Property Insurance",
            policy_type="HO-3 Dwelling",
        )


def test_case_intake_rejects_unknown_field():
    with pytest.raises(ValidationError):
        CaseIntake.model_validate(
            {
                "event_name": "Hurricane Milton",
                "event_date": "2024-10-09",
                "state": "FL",
                "county": "Pinellas",
                "carrier": "Citizens Property Insurance",
                "policy_type": "HO-3 Dwelling",
                "unknown_field": "x",
            }
        )


def test_query_spec_format_row_includes_dates_and_domains():
    spec = QuerySpec(
        module="weather",
        query="milton pinellas weather",
        category="damage_report",
        date_start="2024-10-09",
        date_end="2024-10-10",
        preferred_domains=["weather.gov"],
    )

    row = spec.format_row()
    assert "[damage_report]" in row
    assert "2024-10-09" in row and "2024-10-10" in row
    assert "weather.gov" in row


def test_query_plan_adapters_accept_mixed_shapes():
    spec = QuerySpec(module="weather", query="storm report", category="damage_report")

    typed = adapt_query_plan([spec.model_dump(), spec])
    payloads = query_plan_to_payloads(typed)

    assert [item.module for item in typed] == ["weather", "weather"]
    assert payloads[0]["query"] == "storm report"


def test_query_spec_payload_helper_normalizes_model():
    spec = QuerySpec(module="weather", query="storm report", category="damage_report")

    payload = query_spec_to_payload(spec)

    assert payload["module"] == "weather"
    assert payload["query"] == "storm report"
