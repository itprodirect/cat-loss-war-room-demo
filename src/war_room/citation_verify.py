"""Citation spot-check module.

TODO (Phase 2): Implement Exa-based citation verification.
- One Exa search per citation
- Check if citation appears on court/legal site
- Report: ✅ found on official site, ⚠️ found but unverified, ❌ not found
- Mandatory disclaimer: "KeyCite/Shepardize before reliance"
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CitationCheck:
    """Result of a citation spot-check."""

    citation: str
    status: str       # "verified" | "uncertain" | "not_found"
    badge: str        # "✅" | "⚠️" | "❌"
    source_url: str | None = None
    note: str = ""


def verify_citation(citation: str, *, use_cache: bool = True) -> CitationCheck:
    """Spot-check a single citation via Exa search.

    TODO: Wire to Exa search in Phase 2.
    """
    raise NotImplementedError("Citation verification not yet implemented — coming in Phase 2")


def verify_batch(citations: list[str], *, use_cache: bool = True) -> list[CitationCheck]:
    """Spot-check a batch of citations.

    TODO: Implement in Phase 2.
    """
    raise NotImplementedError("Batch citation verification not yet implemented — coming in Phase 2")
