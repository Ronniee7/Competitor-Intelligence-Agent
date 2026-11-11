from sqlalchemy.orm import Session

from app.database.models import Competitor, ResearchPage
from app.models.research import CompetitorProfile


class StorageService:

    def save_research(
        self,
        db: Session,
        profile: CompetitorProfile,
    ):

        competitor = (
            db.query(Competitor)
            .filter_by(website=profile.website)
            .first()
        )

        if competitor is None:

            competitor = Competitor(
                name=profile.name,
                website=profile.website,
            )

            db.add(competitor)
            db.flush()

        else:
            competitor.name = profile.name

        for page in profile.pages:

            previous = (
                db.query(ResearchPage)
                .filter_by(
                    competitor_id=competitor.id,
                    url=page.url,
                )
                .order_by(ResearchPage.fetched_at.desc())
                .first()
            )

            if (
                previous
                and previous.content_hash == page.content_hash
            ):
                continue

            research_page = ResearchPage(
                competitor_id=competitor.id,
                url=page.url,
                title=page.title,
                content=page.content,
                content_hash=page.content_hash,
            )

            db.add(research_page)

        db.commit()

        db.refresh(competitor)

        return competitor