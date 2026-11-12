
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.research import CompetitorCreate
from app.services.research_service import ResearchService
from app.services.storage_service import StorageService


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/research", tags=["Research"])

research_service = ResearchService()
storage_service = StorageService()


@router.post("/competitor")
async def research_competitor(
    competitor: CompetitorCreate,
    db: Session = Depends(get_db),
):
    try:
        result = await research_service.research_competitor(
            competitor
        )

        saved = storage_service.save_research(
            db=db,
            profile=result,
        )

        return {
            "message": "Research completed and saved.",
            "competitor_id": saved.id,
            "name": saved.name,
            "website": saved.website,
            "pages_researched": len(result.pages),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        db.rollback()

        logger.exception("COMPETITOR RESEARCH FAILED")

        raise HTTPException(
            status_code=502,
            detail=f"Research operation failed: {str(exc)}",
        ) from exc
