"""Tests for caselaw_module case-like filter."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from war_room.caselaw_module import _is_case_like


def test_case_with_citation_passes():
    assert _is_case_like({"name": "Some Title", "citation": "123 So. 3d 456"})


def test_case_with_v_dot_passes():
    assert _is_case_like({"name": "Smith v. Jones Insurance Co"})


def test_case_with_vs_dot_passes():
    assert _is_case_like({"name": "Smith vs. Jones"})


def test_case_with_in_re_passes():
    assert _is_case_like({"name": "In re Citizens Property Insurance"})


def test_case_with_ex_rel_passes():
    assert _is_case_like({"name": "State ex rel. Smith v. Dept of Insurance"})


def test_non_case_article_excluded():
    """A blog/article title with no citation should be excluded."""
    assert not _is_case_like({
        "name": "What is an anti-concurrent causation clause?",
        "citation": "",
    })


def test_non_case_explainer_excluded():
    assert not _is_case_like({
        "name": "Understanding Hurricane Insurance Coverage in Florida",
        "citation": "",
    })


def test_non_case_news_excluded():
    assert not _is_case_like({
        "name": "Citizens Property Insurance faces record claims after Milton",
        "citation": "",
    })


def test_empty_result_excluded():
    assert not _is_case_like({"name": "", "citation": ""})


def test_none_fields_excluded():
    assert not _is_case_like({})
