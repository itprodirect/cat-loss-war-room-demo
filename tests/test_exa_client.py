"""Tests for exa_client module — no network calls."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from war_room.exa_client import ExaClient, BudgetExhausted
import pytest


def _mock_result(url="https://example.com", title="Test", text="body"):
    r = MagicMock()
    r.url = url
    r.title = title
    r.text = text
    r.published_date = "2024-01-01"
    r.score = 0.9
    r.summary = None
    r.highlights = None
    return r


def _mock_search_response(results):
    resp = MagicMock()
    resp.results = results
    return resp


@patch("war_room.exa_client.Exa")
def test_search_normalizes_results(MockExa):
    instance = MockExa.return_value
    instance.search.return_value = _mock_search_response([
        _mock_result("https://noaa.gov/report", "NOAA Report", "wind 120 mph"),
    ])

    client = ExaClient(api_key="test-key")
    results = client.search("test query")

    assert len(results) == 1
    assert results[0]["url"] == "https://noaa.gov/report"
    assert results[0]["title"] == "NOAA Report"
    assert "text" in results[0]
    assert "snippet" in results[0]


@patch("war_room.exa_client.Exa")
def test_budget_guard(MockExa):
    instance = MockExa.return_value
    instance.search.return_value = _mock_search_response([])

    client = ExaClient(api_key="test-key", max_search_calls=2)

    client.search("q1")
    client.search("q2")

    with pytest.raises(BudgetExhausted):
        client.search("q3")


@patch("war_room.exa_client.Exa")
def test_budget_remaining(MockExa):
    instance = MockExa.return_value
    instance.search.return_value = _mock_search_response([])

    client = ExaClient(api_key="test-key", max_search_calls=5)
    assert client.budget_remaining == 5

    client.search("q1")
    assert client.budget_remaining == 4


@patch("war_room.exa_client.Exa")
def test_retry_on_failure(MockExa):
    instance = MockExa.return_value
    # Fail twice, succeed on third
    instance.search.side_effect = [
        Exception("rate limit"),
        Exception("rate limit"),
        _mock_search_response([_mock_result()]),
    ]

    client = ExaClient(api_key="test-key")
    results = client.search("test")
    assert len(results) == 1
    assert instance.search.call_count == 3
