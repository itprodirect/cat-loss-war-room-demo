"""Case intake and query plan generation.

Generates 12-18 targeted research queries from a CaseIntake,
organized by module: weather, carrier_docs, caselaw.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CaseIntake:
    """Structured case intake for a CAT loss matter."""

    event_name: str               # e.g. "Hurricane Milton"
    event_date: str               # e.g. "2024-10-09"
    state: str                    # e.g. "FL"
    county: str                   # e.g. "Pinellas"
    carrier: str                  # e.g. "Citizens Property Insurance"
    policy_type: str              # e.g. "HO-3 Dwelling"
    posture: list[str] = field(default_factory=lambda: ["denial"])
    key_facts: list[str] = field(default_factory=list)
    coverage_issues: list[str] = field(default_factory=list)

    def summary(self) -> str:
        """One-line case summary."""
        return (
            f"{self.event_name} | {self.carrier} | "
            f"{self.county} County, {self.state} | "
            f"{self.policy_type} | Posture: {', '.join(self.posture)}"
        )

    def format_card(self) -> str:
        """Multi-line formatted intake card for display."""
        lines = [
            "=" * 60,
            "CASE INTAKE",
            "=" * 60,
            f"  Event:       {self.event_name} ({self.event_date})",
            f"  Location:    {self.county} County, {self.state}",
            f"  Carrier:     {self.carrier}",
            f"  Policy:      {self.policy_type}",
            f"  Posture:     {', '.join(self.posture)}",
        ]
        if self.key_facts:
            lines.append(f"  Key Facts:   {'; '.join(self.key_facts)}")
        if self.coverage_issues:
            lines.append(f"  Issues:      {'; '.join(self.coverage_issues)}")
        lines.append("=" * 60)
        return "\n".join(lines)


@dataclass
class QuerySpec:
    """A single search query specification."""

    module: str                   # "weather" | "carrier_docs" | "caselaw"
    query: str                    # The search query text
    category: str                 # Sub-category within the module
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    preferred_domains: list[str] = field(default_factory=list)

    def format_row(self) -> str:
        """Format as a display row."""
        date_range = ""
        if self.date_start and self.date_end:
            date_range = f" [{self.date_start} → {self.date_end}]"
        elif self.date_start:
            date_range = f" [from {self.date_start}]"
        domains = ""
        if self.preferred_domains:
            domains = f" (prefer: {', '.join(self.preferred_domains)})"
        return f"  [{self.category}] {self.query}{date_range}{domains}"


def generate_query_plan(intake: CaseIntake) -> list[QuerySpec]:
    """Generate 12-18 targeted research queries from a case intake.

    Queries are organized by module: weather, carrier_docs, caselaw.
    """
    queries: list[QuerySpec] = []

    # --- WEATHER MODULE (4-6 queries) ---
    queries.append(QuerySpec(
        module="weather",
        query=f"{intake.event_name} {intake.county} County {intake.state} damage report",
        category="damage_report",
        date_start=intake.event_date,
        preferred_domains=["noaa.gov", "weather.gov"],
    ))
    queries.append(QuerySpec(
        module="weather",
        query=f"NWS {intake.event_name} wind speed {intake.county} {intake.state}",
        category="wind_data",
        date_start=intake.event_date,
        preferred_domains=["weather.gov", "nhc.noaa.gov"],
    ))
    queries.append(QuerySpec(
        module="weather",
        query=f"{intake.event_name} storm surge flood {intake.county} County {intake.state}",
        category="flood_surge",
        date_start=intake.event_date,
        preferred_domains=["noaa.gov", "usgs.gov"],
    ))
    queries.append(QuerySpec(
        module="weather",
        query=f"FEMA disaster declaration {intake.event_name} {intake.state}",
        category="fema_declaration",
        date_start=intake.event_date,
        preferred_domains=["fema.gov", "disasterassistance.gov"],
    ))
    queries.append(QuerySpec(
        module="weather",
        query=f"{intake.event_name} damage assessment {intake.county} County insured losses",
        category="loss_estimate",
        date_start=intake.event_date,
    ))

    # --- CARRIER DOCS MODULE (4-6 queries) ---
    queries.append(QuerySpec(
        module="carrier_docs",
        query=f"{intake.carrier} {intake.event_name} claim denial {intake.state}",
        category="denial_patterns",
        date_start=intake.event_date,
    ))
    queries.append(QuerySpec(
        module="carrier_docs",
        query=f"{intake.carrier} department of insurance complaints {intake.state}",
        category="doi_complaints",
        preferred_domains=["floir.com", "tdi.texas.gov", "naic.org"],
    ))
    queries.append(QuerySpec(
        module="carrier_docs",
        query=f"{intake.carrier} {intake.event_name} regulatory action {intake.state}",
        category="regulatory_action",
        date_start=intake.event_date,
    ))
    queries.append(QuerySpec(
        module="carrier_docs",
        query=f"{intake.carrier} claims handling guidelines {intake.policy_type}",
        category="claims_manual",
    ))
    queries.append(QuerySpec(
        module="carrier_docs",
        query=f"{intake.carrier} bad faith insurance {intake.state} settlement practices",
        category="bad_faith_history",
    ))

    # --- CASELAW MODULE (4-6 queries) ---
    _posture_str = " ".join(intake.posture)
    queries.append(QuerySpec(
        module="caselaw",
        query=f"{intake.carrier} {intake.policy_type} {_posture_str} {intake.state}",
        category="carrier_precedent",
        preferred_domains=["scholar.google.com", "law.cornell.edu", "casetext.com"],
    ))
    queries.append(QuerySpec(
        module="caselaw",
        query=f"hurricane wind damage insurance coverage {_posture_str} {intake.state}",
        category="coverage_law",
        preferred_domains=["scholar.google.com", "casetext.com"],
    ))
    queries.append(QuerySpec(
        module="caselaw",
        query=f"concurrent causation wind water damage insurance {intake.state}",
        category="concurrent_causation",
    ))
    queries.append(QuerySpec(
        module="caselaw",
        query=f"insurance bad faith {intake.state} {intake.carrier} penalty damages",
        category="bad_faith_precedent",
    ))

    # Dynamic: add coverage-issue-specific queries
    for issue in intake.coverage_issues:
        queries.append(QuerySpec(
            module="caselaw",
            query=f"{issue} insurance coverage {intake.state} {intake.policy_type}",
            category="coverage_issue",
        ))

    # Dynamic: add posture-specific queries
    if "bad_faith" in intake.posture:
        queries.append(QuerySpec(
            module="caselaw",
            query=f"bad faith failure to investigate insurance claim {intake.state}",
            category="bad_faith_law",
        ))
    if "underpayment" in intake.posture:
        queries.append(QuerySpec(
            module="caselaw",
            query=f"insurance underpayment {intake.event_name} appraisal {intake.state}",
            category="underpayment_law",
        ))

    return queries


def format_query_plan(queries: list[QuerySpec]) -> str:
    """Format the query plan grouped by module for display."""
    lines = [
        "=" * 60,
        f"QUERY PLAN — {len(queries)} queries",
        "=" * 60,
    ]

    modules = ["weather", "carrier_docs", "caselaw"]
    module_labels = {
        "weather": "WEATHER DATA",
        "carrier_docs": "CARRIER DOCUMENTS",
        "caselaw": "CASE LAW",
    }

    for mod in modules:
        mod_queries = [q for q in queries if q.module == mod]
        if mod_queries:
            lines.append(f"\n  [{module_labels.get(mod, mod)}] ({len(mod_queries)} queries)")
            lines.append("  " + "-" * 40)
            for q in mod_queries:
                lines.append(q.format_row())

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)
