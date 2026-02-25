"""Case law search module.

TODO (Phase 2): Implement Exa search for case law.
- Run case law queries from query plan
- Organize results by legal issue, not by source
- Pass citations through citation_verify for spot-check
"""

from __future__ import annotations

from typing import Any

from war_room.query_plan import CaseIntake, QuerySpec


def fetch_caselaw(
    intake: CaseIntake,
    queries: list[QuerySpec],
    *,
    use_cache: bool = True,
) -> dict[str, Any]:
    """Fetch case law results. Returns results organized by legal issue.

    TODO: Wire to Exa search in Phase 2.
    """
    raise NotImplementedError("Case law module not yet implemented — coming in Phase 2")


def format_caselaw_summary(data: dict[str, Any]) -> str:
    """Format case law results with citation badges.

    TODO: Implement in Phase 2.
    """
    raise NotImplementedError("Case law formatting not yet implemented — coming in Phase 2")
