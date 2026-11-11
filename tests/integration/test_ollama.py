import pytest

from app.llm.ollama_client import OllamaClient
from app.models.intelligence import CompetitorIntelligence


@pytest.mark.asyncio
@pytest.mark.integration
async def test_ollama_structured_generation():

    client = OllamaClient()

    result = await client.generate_structured(
        prompt=(
            "Analyse a fictional company called TestPay. "
            "It provides digital payment processing."
        ),
        output_schema=CompetitorIntelligence,
    )

    assert isinstance(result, CompetitorIntelligence)

    assert result.company_name

    assert isinstance(result.products_and_services, list)