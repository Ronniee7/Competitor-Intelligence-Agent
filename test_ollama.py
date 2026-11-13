
import asyncio
import httpx
import time


async def main():

    url = "http://localhost:11434/api/chat"

    payload = {
        "model": "qwen3:4b",
        "messages": [
            {
                "role": "user",
                "content": "Explain a buck converter in three sentences."
            }
        ],
        "stream": False,
        "options": {
            "num_predict": 150,
            "temperature": 0.1
        }
    }

    start = time.time()

    try:
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(600.0)
        ) as client:

            response = await client.post(
                url,
                json=payload
            )

            response.raise_for_status()

            result = response.json()

            print("RESPONSE:")
            print(result["message"]["content"])

            print(
                f"\nDuration: {time.time() - start:.2f} seconds"
            )

    except Exception as exc:
        print("ERROR:", repr(exc))


asyncio.run(main())
