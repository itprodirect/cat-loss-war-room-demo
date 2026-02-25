"""Tests for cache_io module."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from war_room.cache_io import normalize_key, cache_get, cache_set, cached_call


def test_normalize_key_basic():
    assert normalize_key("Hello World!") == "hello_world"


def test_normalize_key_special_chars():
    assert normalize_key("  NWS Milton FL 2024  ") == "nws_milton_fl_2024"


def test_normalize_key_already_clean():
    assert normalize_key("clean_key") == "clean_key"


def test_cache_roundtrip():
    with tempfile.TemporaryDirectory() as tmpdir:
        data = {"results": [1, 2, 3], "query": "test"}
        cache_set("test_key", data, tmpdir)
        result = cache_get("test_key", tmpdir)
        assert result == data


def test_cache_get_missing():
    with tempfile.TemporaryDirectory() as tmpdir:
        result = cache_get("nonexistent", tmpdir)
        assert result is None


def test_cached_call_uses_cache():
    with tempfile.TemporaryDirectory() as tmpdir:
        call_count = 0

        def expensive_fn():
            nonlocal call_count
            call_count += 1
            return {"value": 42}

        # First call: hits fn
        result1 = cached_call("my_key", expensive_fn, cache_dir=tmpdir, cache_samples_dir=tmpdir)
        assert result1 == {"value": 42}
        assert call_count == 1

        # Second call: hits cache
        result2 = cached_call("my_key", expensive_fn, cache_dir=tmpdir, cache_samples_dir=tmpdir)
        assert result2 == {"value": 42}
        assert call_count == 1  # fn not called again


def test_cached_call_bypass_cache():
    with tempfile.TemporaryDirectory() as tmpdir:
        call_count = 0

        def fn():
            nonlocal call_count
            call_count += 1
            return {"v": call_count}

        result = cached_call("k", fn, cache_dir=tmpdir, cache_samples_dir=tmpdir, use_cache=False)
        assert result == {"v": 1}

        # Even with use_cache=False, the result was saved to cache
        result2 = cached_call("k", fn, cache_dir=tmpdir, cache_samples_dir=tmpdir, use_cache=True)
        assert result2 == {"v": 1}  # from cache, fn not called again


def test_cached_call_prefers_samples():
    with tempfile.TemporaryDirectory() as samples_dir, tempfile.TemporaryDirectory() as cache_dir:
        # Pre-seed samples
        cache_set("shared_key", {"source": "samples"}, samples_dir)
        cache_set("shared_key", {"source": "cache"}, cache_dir)

        result = cached_call(
            "shared_key",
            lambda: {"source": "live"},
            cache_samples_dir=samples_dir,
            cache_dir=cache_dir,
        )
        assert result["source"] == "samples"
