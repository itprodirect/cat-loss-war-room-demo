"""Source credibility scoring — deterministic, domain-based."""

from __future__ import annotations

from urllib.parse import urlparse

# --- Domain classification dictionaries ---

OFFICIAL_DOMAINS: set[str] = {
    ".gov",
    "courts.state",
    "uscourts.gov",
    "noaa.gov",
    "weather.gov",
    "nws.noaa.gov",
    "scc.virginia.gov",
    "floir.com",           # FL Office of Insurance Regulation
    "tdi.texas.gov",       # TX Dept of Insurance
    "doi.sc.gov",
    "insurance.ca.gov",
    "dfs.ny.gov",
}

PROFESSIONAL_DOMAINS: set[str] = {
    "law.com",
    "reuters.com",
    "bloomberglaw.com",
    "insurancejournal.com",
    "ambest.com",
    "naic.org",
    "propertyinsurancecoveragelaw.com",
    "merlinlawgroup.com",
    "law.cornell.edu",
    "scholar.google.com",
    "casetext.com",
}

PAYWALLED_DOMAINS: set[str] = {
    "westlaw.com",
    "thomsonreuters.com",
    "lexisnexis.com",
    "heinonline.org",
    "next.westlaw.com",
    "advance.lexis.com",
}


def _classify_domain(hostname: str) -> str:
    """Classify a hostname into a scoring tier."""
    hostname = hostname.lower().lstrip("www.")

    # Check paywalled first (takes priority)
    for domain in PAYWALLED_DOMAINS:
        if hostname == domain or hostname.endswith("." + domain):
            return "paywalled"

    # Check official
    for domain in OFFICIAL_DOMAINS:
        if hostname.endswith(domain):
            return "official"

    # Check professional
    for domain in PROFESSIONAL_DOMAINS:
        if hostname == domain or hostname.endswith("." + domain):
            return "professional"

    return "unvetted"


def score_url(url: str) -> dict:
    """Score a URL for source credibility.

    Returns:
        dict with keys: url, hostname, tier, badge, label
    """
    try:
        parsed = urlparse(url)
        hostname = (parsed.hostname or "").lower()
    except Exception:
        hostname = ""

    tier = _classify_domain(hostname)

    badges = {
        "official": "🟢",
        "professional": "🟡",
        "unvetted": "🔴",
        "paywalled": "🔒",
    }

    labels = {
        "official": "Official source",
        "professional": "Professional source",
        "unvetted": "Unvetted source",
        "paywalled": "Paywalled — verify with subscription access",
    }

    return {
        "url": url,
        "hostname": hostname,
        "tier": tier,
        "badge": badges[tier],
        "label": labels[tier],
    }


def format_badge(score: dict) -> str:
    """Format a score dict as a display string."""
    return f"{score['badge']} {score['label']} ({score['hostname']})"
