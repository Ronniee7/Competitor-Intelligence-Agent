from app.ingestion.crawler import WebsiteCrawler
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

        page = await self.crawler.fetch_page(
            str(competitor.website)
        )

        return CompetitorProfile(
            name=competitor.name,
            website=str(competitor.website),
            pages=[page],
        )