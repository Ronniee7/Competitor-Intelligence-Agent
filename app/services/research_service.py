import asyncio

from app.ingestion.crawler import WebsiteCrawler
from app.ingestion.discovery import discover_relevant_links

from app.models.research import (
    CompetitorCreate,
    CompetitorProfile,
)

class ResearchService:

    def __init__(self):

        self.crawler = WebsiteCrawler()

    async def research_competitor(
        self,
        competitor: CompetitorCreate,
    ) -> CompetitorProfile:

        homepage = await self.crawler.fetch_page(
            str(competitor.website)
        )

        links = discover_relevant_links(
            links=homepage.links,
            base_url=str(competitor.website),
            max_pages=8,
        )

        semaphore = asyncio.Semaphore(2)

        async def fetch_safely(url):

            async with semaphore:

                try:
                    return await self.crawler.fetch_page(url)

                except Exception:
                    return None

        results = await asyncio.gather(
            *[
                fetch_safely(url)
                for url in links
            ]
        )

        pages = [homepage]

        pages.extend(
            page
            for page in results
            if page is not None
        )

        return CompetitorProfile(
            name=competitor.name,
            website=str(competitor.website),
            pages=pages,
        )