"""Tests for source_scoring module."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from war_room.source_scoring import score_url, format_badge


def test_gov_is_official():
    result = score_url("https://www.weather.gov/reports/milton")
    assert result["tier"] == "official"
    assert result["badge"] == "🟢"


def test_noaa_is_official():
    result = score_url("https://nws.noaa.gov/data/storm-report")
    assert result["tier"] == "official"
    assert result["badge"] == "🟢"


def test_fema_is_official():
    result = score_url("https://www.fema.gov/disaster/4834")
    assert result["tier"] == "official"
    assert result["badge"] == "🟢"


def test_law_firm_is_professional():
    result = score_url("https://www.merlinlawgroup.com/blog/post")
    assert result["tier"] == "professional"
    assert result["badge"] == "🟡"


def test_insurance_journal_is_professional():
    result = score_url("https://www.insurancejournal.com/article/123")
    assert result["tier"] == "professional"
    assert result["badge"] == "🟡"


def test_random_blog_is_unvetted():
    result = score_url("https://random-insurance-blog.wordpress.com/post")
    assert result["tier"] == "unvetted"
    assert result["badge"] == "🔴"


def test_westlaw_is_paywalled():
    result = score_url("https://next.westlaw.com/Document/I123")
    assert result["tier"] == "paywalled"
    assert result["badge"] == "🔒"


def test_lexis_is_paywalled():
    result = score_url("https://advance.lexis.com/document/123")
    assert result["tier"] == "paywalled"
    assert result["badge"] == "🔒"


def test_format_badge_output():
    result = score_url("https://www.weather.gov/report")
    badge = format_badge(result)
    assert "🟢" in badge
    assert "Official" in badge


def test_malformed_url_returns_unvetted():
    result = score_url("not-a-url")
    assert result["tier"] == "unvetted"
