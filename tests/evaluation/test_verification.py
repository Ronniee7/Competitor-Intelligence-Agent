from app.agents.verifier import verify_finding
from app.models.intelligence import Finding
from app.models.research import (
    CompetitorProfile,
    ExtractedPage,
)

def test_supported_finding():

    page = ExtractedPage(
        url="https://example.com/products",
        title="Products",
        content=(
            "The company provides digital payment "
            "processing for businesses."
        ),
        content_hash="a" * 64,
        status_code=200,
    )

    profile = CompetitorProfile(
        name="TestPay",
        website="https://example.com",
        pages=[page],
    )

    finding = Finding(
        claim="Provides payment processing.",
        evidence="digital payment processing",
        source_url="https://example.com/products",
        confidence=0.95,
    )

    assert verify_finding(
        finding,
        profile,
    ) is True

def test_unsupported_finding():

    page = ExtractedPage(
        url="https://example.com",
        content="The company provides business software.",
        content_hash="b" * 64,
        status_code=200,
    )

    profile = CompetitorProfile(
        name="TestPay",
        website="https://example.com",
        pages=[page],
    )

    finding = Finding(
        claim="The company has 10 million customers.",
        evidence="10 million customers",
        source_url="https://example.com",
        confidence=0.99,
    )

    assert verify_finding(
        finding,
        profile,
    ) is False