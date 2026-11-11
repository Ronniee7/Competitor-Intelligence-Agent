from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.agents.intelligence_graph import intelligence_graph

from app.database.connection import get_db
from app.database.models import (
    Competitor,
    IntelligenceReport,
    ResearchPage,
)

from app.models.research import (
    CompetitorProfile,
    ExtractedPage,
)

from app.intelligence.report_generator import generate_markdown_report

router = APIRouter(prefix="/analysis", tags=["Intelligence"])

@router.post("/{competitor_id}")
async def analyse_competitor(
    competitor_id: int,
    db: Session = Depends(get_db),
):

    competitor = db.get(Competitor, competitor_id)

    if competitor is None:

        raise HTTPException(
            status_code=404,
            detail="Competitor not found.",
        )

    pages = (
        db.query(ResearchPage)
        .filter_by(competitor_id=competitor_id)
        .order_by(ResearchPage.fetched_at.desc())
        .all()
    )

    # Keep only the latest snapshot of each URL.
    latest_pages = {}

    for page in pages:
        if page.url not in latest_pages:
            latest_pages[page.url] = page

    if not latest_pages:

        raise HTTPException(
            status_code=400,
            detail="No research data available.",
        )

    extracted_pages = [
        ExtractedPage(
            url=page.url,
            title=page.title,
            content=page.content,
            content_hash=page.content_hash,
            status_code=200,
            fetched_at=page.fetched_at,
        )
        for page in latest_pages.values()
    ]

    profile = CompetitorProfile(
        name=competitor.name,
        website=competitor.website,
        pages=extracted_pages,
    )

    result = await intelligence_graph.ainvoke({
        "profile": profile,
        "errors": [],
    })

    if result.get("errors") or not result.get("intelligence"):

        raise HTTPException(
            status_code=502,
            detail={
                "message": "Intelligence analysis failed.",
                "errors": result.get("errors", []),
            },
        )

    intelligence = result["intelligence"]

    report = generate_markdown_report(intelligence)

    saved_report = IntelligenceReport(
        competitor_id=competitor.id,
        report_json=intelligence.model_dump(mode="json"),
    )

    db.add(saved_report)
    db.commit()
    db.refresh(saved_report)

    return {
        "report_id": saved_report.id,
        "competitor": competitor.name,
        "verification": result.get("verification_summary"),
        "intelligence": intelligence.model_dump(mode="json"),
        "markdown_report": report,
    }