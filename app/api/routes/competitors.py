from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Competitor, ResearchPage


router = APIRouter(prefix="/competitors", tags=["Competitors"])


@router.get("/")
def list_competitors(
    db: Session = Depends(get_db),
):

    competitors = db.query(Competitor).all()

    return [
        {
            "id": competitor.id,
            "name": competitor.name,
            "website": competitor.website,
            "pages_researched": len(competitor.pages),
        }
        for competitor in competitors
    ]


@router.get("/{competitor_id}")
def get_competitor(
    competitor_id: int,
    db: Session = Depends(get_db),
):

    competitor = db.get(Competitor, competitor_id)

    if competitor is None:
        raise HTTPException(
            status_code=404,
            detail="Competitor not found.",
        )

    return {
        "id": competitor.id,
        "name": competitor.name,
        "website": competitor.website,
        "research_pages": [
            {
                "url": page.url,
                "title": page.title,
                "content_hash": page.content_hash,
                "fetched_at": page.fetched_at,
            }
            for page in competitor.pages
        ],
    }