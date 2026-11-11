import httpx

from app.ingestion.extractor import extract_page
from app.ingestion.url_validator import validate_public_url
from app.models.research import ExtractedPage


class WebsiteCrawler:

    def __init__(self, transport=None):
        self.timeout = httpx.Timeout(20.0)
        self.transport = transport

        self.headers = {
            "User-Agent": (
                "CompetitorIntelligenceResearchBot/0.1"
            )
        }

    async def fetch_page(self, url: str) -> ExtractedPage:

        validate_public_url(url)

        async with httpx.AsyncClient(
            timeout=self.timeout,
            follow_redirects=False,
            headers=self.headers,
            transport=self.transport,
        ) as client:

            current_url = url

            for _ in range(4):

                validate_public_url(current_url)

                response = await client.get(current_url)

                if response.is_redirect:

                    location = response.headers.get("location")

                    if not location:
                        raise ValueError("Redirect has no destination.")

                    from urllib.parse import urljoin

                    current_url = urljoin(
                        str(response.url),
                        location
                    )

                    continue

                response.raise_for_status()

                content_type = response.headers.get(
                    "content-type",
                    ""
                ).lower()

                if "text/html" not in content_type:
                    raise ValueError(
                        "The requested page is not HTML."
                    )

                if len(response.content) > 2_000_000:
                    raise ValueError("Page exceeds the 2 MB limit.")

                return extract_page(
                    html=response.text,
                    url=str(response.url),
                    status_code=response.status_code,
                )

            raise ValueError("Too many redirects.")