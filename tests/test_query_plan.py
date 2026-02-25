"""Tests for query_plan module."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from war_room.query_plan import CaseIntake, QuerySpec, generate_query_plan, format_query_plan


def _sample_intake() -> CaseIntake:
    return CaseIntake(
        event_name="Hurricane Milton",
        event_date="2024-10-09",
        state="FL",
        county="Pinellas",
        carrier="Citizens Property Insurance",
        policy_type="HO-3 Dwelling",
        posture=["denial", "bad_faith"],
        key_facts=["Roof damage reported"],
        coverage_issues=["wind vs water causation"],
    )


def test_generate_returns_queries():
    queries = generate_query_plan(_sample_intake())
    assert len(queries) >= 12
    assert len(queries) <= 25


def test_all_three_modules_present():
    queries = generate_query_plan(_sample_intake())
    modules = {q.module for q in queries}
    assert "weather" in modules
    assert "carrier_docs" in modules
    assert "caselaw" in modules


def test_each_module_has_multiple_queries():
    queries = generate_query_plan(_sample_intake())
    for mod in ["weather", "carrier_docs", "caselaw"]:
        mod_queries = [q for q in queries if q.module == mod]
        assert len(mod_queries) >= 3, f"Module {mod} has too few queries: {len(mod_queries)}"


def test_queries_contain_case_details():
    queries = generate_query_plan(_sample_intake())
    all_text = " ".join(q.query for q in queries)
    assert "Milton" in all_text
    assert "Citizens" in all_text
    assert "FL" in all_text


def test_format_query_plan_output():
    queries = generate_query_plan(_sample_intake())
    output = format_query_plan(queries)
    assert "QUERY PLAN" in output
    assert "WEATHER DATA" in output
    assert "CARRIER DOCUMENTS" in output
    assert "CASE LAW" in output


def test_bad_faith_posture_adds_query():
    intake_with = _sample_intake()  # has bad_faith
    intake_without = CaseIntake(
        event_name="Hurricane Milton",
        event_date="2024-10-09",
        state="FL",
        county="Pinellas",
        carrier="Citizens Property Insurance",
        policy_type="HO-3 Dwelling",
        posture=["denial"],
    )
    queries_with = generate_query_plan(intake_with)
    queries_without = generate_query_plan(intake_without)
    assert len(queries_with) > len(queries_without)
