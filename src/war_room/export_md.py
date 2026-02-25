"""Markdown export module.

TODO (Phase 2): Implement full export.
- Compile all module outputs to single markdown
- Source appendix table (URL, confidence, module, date)
- DRAFT — ATTORNEY WORK PRODUCT watermark
- Methodology & limitations section
- Save to output/ directory
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from war_room.query_plan import CaseIntake


def export_memo(
    intake: CaseIntake,
    *,
    weather_data: dict[str, Any] | None = None,
    carrier_data: dict[str, Any] | None = None,
    caselaw_data: dict[str, Any] | None = None,
    output_dir: str | Path = "output",
) -> Path:
    """Export a structured research memo as markdown.

    TODO: Wire to module outputs in Phase 2.
    """
    raise NotImplementedError("Export not yet implemented — coming in Phase 2")
