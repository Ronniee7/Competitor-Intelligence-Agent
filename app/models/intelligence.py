from pydantic import BaseModel, Field


class Finding(BaseModel):

    claim: str

    evidence: str

    source_url: str | None = None

    verified: bool = False

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )


class CompetitorIntelligence(BaseModel):

    company_name: str

    industry: str

    company_description: str

    products_and_services: list[Finding]

    target_customers: list[Finding]

    value_propositions: list[Finding]

    geographic_markets: list[Finding]

    potential_competitive_advantages: list[Finding]

    information_gaps: list[str]