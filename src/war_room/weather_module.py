"""Weather data gathering module.

TODO (Phase 2): Implement Exa search for weather data.
- Run weather queries from query plan
- Filter for .gov sources first
- Output structured weather summary with source badges
- Templated "litigation relevance" paragraph
"""

from __future__ import annotations

from typing import Any

from war_room.query_plan import CaseIntake, QuerySpec


def fetch_weather_data(
    intake: CaseIntake,
    queries: list[QuerySpec],
    *,
    use_cache: bool = True,
) -> dict[str, Any]:
    """Fetch weather data for a case. Returns structured weather summary.

    TODO: Wire to Exa search in Phase 2.
    """
    raise NotImplementedError("Weather module not yet implemented — coming in Phase 2")


def format_weather_summary(data: dict[str, Any]) -> str:
    """Format weather data as a display summary with source badges.

    TODO: Implement in Phase 2.
    """
    raise NotImplementedError("Weather formatting not yet implemented — coming in Phase 2")
