
import httpx

from urllib.parse import urljoin, urlsplit
from urllib.robotparser import RobotFileParser

from app.ingestion.extractor import extract_page
from app.ingestion.url_validator import validate_public_url
from app.models.research import ExtractedPage


class WebsiteCrawler:

    def __init__(self, transport=None):
        self.timeout = httpx.Timeout(20.0)
        self.transport = transport

        self.headers = {
            "User-Agent": "CompetitorIntelligenceResearchBot/0.1"
        }

    async def can_fetch(self, client, url: str) -> bool:

        parsed = urlsplit(url)

        robots_url = (
            f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        )

        validate_public_url(robots_url)

        try:
            response = await client.get(robots_url)

        except httpx.HTTPError:
            # Fail closed if robots.txt cannot be checked.
            return False

        if response.status_code in (404, 410):
            return True

        if response.status_code != 200:
            return False

        parser = RobotFileParser()

        parser.set_url(robots_url)
        parser.parse(response.text.splitlines())

        return parser.can_fetch(
            "CompetitorIntelligenceResearchBot",
            url,
        )

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

                # Check robots.txt before fetching each destination.
                if not await self.can_fetch(client, current_url):
                    raise ValueError(
                        "Website crawling is disallowed by robots.txt "
                        "or its policy could not be checked."
                    )

                response = await client.get(current_url)

                if response.is_redirect:

                    location = response.headers.get("location")

                    if not location:
                        raise ValueError(
                            "Redirect has no destination."
                        )

                    current_url = urljoin(
                        str(response.url),
                        location,
                    )

                    continue

                response.raise_for_status()

                content_type = response.headers.get(
                    "content-type",
                    "",
                ).lower()

                if "text/html" not in content_type:
                    raise ValueError(
                        "The requested page is not HTML."
                    )

                if len(response.content) > 2_000_000:
                    raise ValueError(
                        "Page exceeds the 2 MB limit."
                    )

                return extract_page(
                    html=response.text,
                    url=str(response.url),
                    status_code=response.status_code,
                )

            raise ValueError("Too many redirects.")
