"""Carrier playbook intel module.

TODO (Phase 2): Implement Exa search for carrier data.
- Run carrier queries from query plan
- Categorize: regulatory actions, denial patterns, carrier documents
- Generate rebuttal angles from key_facts
- Handle missing NAIC/DOI data gracefully
"""

from __future__ import annotations

from typing import Any

from war_room.query_plan import CaseIntake, QuerySpec


def fetch_carrier_data(
    intake: CaseIntake,
    queries: list[QuerySpec],
    *,
    use_cache: bool = True,
) -> dict[str, Any]:
    """Fetch carrier playbook data. Returns structured carrier intel.

    TODO: Wire to Exa search in Phase 2.
    """
    raise NotImplementedError("Carrier module not yet implemented — coming in Phase 2")


def generate_rebuttal_angles(data: dict[str, Any], intake: CaseIntake) -> list[str]:
    """Generate rebuttal angles from carrier data and case facts.

    TODO: Implement in Phase 2.
    """
    raise NotImplementedError("Rebuttal generation not yet implemented — coming in Phase 2")
