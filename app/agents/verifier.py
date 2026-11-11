import re

from app.models.intelligence import (
    CompetitorIntelligence,
    Finding,
)
from app.models.research import CompetitorProfile

def normalize_text(text: str) -> str:

    return re.sub(
        r"\s+",
        " ",
        text.lower(),
    ).strip()

def verify_finding(
    finding: Finding,
    profile: CompetitorProfile,
) -> bool:

    for page in profile.pages:

        if page.url != finding.source_url:
            continue

        source = normalize_text(page.content)
        evidence = normalize_text(finding.evidence)

        if evidence and evidence in source:
            return True

    return False

def verify_intelligence(
    intelligence: CompetitorIntelligence,
    profile: CompetitorProfile,
):

    categories = [
        "products_and_services",
        "target_customers",
        "value_propositions",
        "geographic_markets",
        "potential_competitive_advantages",
    ]

    verified_count = 0
    rejected_count = 0

    updates = {}

    for category in categories:

        findings = getattr(intelligence, category)

        updated_findings = []

        for finding in findings:

            is_verified = verify_finding(
                finding,
                profile,
            )

            updated = finding.model_copy(
                update={"verified": is_verified}
            )

            updated_findings.append(updated)

            if is_verified:
                verified_count += 1
            else:
                rejected_count += 1

        updates[category] = updated_findings

    updated_intelligence = intelligence.model_copy(
        update=updates
    )

    return updated_intelligence, {
        "verified": verified_count,
        "rejected": rejected_count,
        "total": verified_count + rejected_count,
    }