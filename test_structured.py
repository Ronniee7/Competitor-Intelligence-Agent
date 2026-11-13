
import asyncio
import time

from app.llm.ollama_client import OllamaClient
from app.models.intelligence import CompetitorIntelligence


async def main():

    client = OllamaClient()

    prompt = """
    Analyse this fictional example company.

    Company: GreenTech Uganda
    Industry: Renewable Energy

    It sells solar panels and solar irrigation pumps
    to farmers and small businesses in Uganda.

    Produce a concise analysis.
    Only use the information supplied.
    Use empty lists where information is unavailable.
    """

    start = time.time()

    try:

        result = await client.generate_structured(
            prompt=prompt,
            output_schema=CompetitorIntelligence,
        )

        print("\nSTRUCTURED OUTPUT:")
        print(result.model_dump_json(indent=2))

        print(
            f"\nGeneration time: {time.time() - start:.2f} seconds"
        )

    except Exception as exc:

        print("\nGENERATION FAILED:")
        print(repr(exc))


asyncio.run(main())
