from datetime import datetime, timezone
from pydantic import BaseModel, Field, HttpUrl


class CompetitorCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    website: HttpUrl


class ExtractedPage(BaseModel):
    url: str
    title: str | None = None
    description: str | None = None

    headings: list[str] = Field(default_factory=list)
    paragraphs: list[str] = Field(default_factory=list)
    links: list[str] = Field(default_factory=list)

    content: str = ""

    status_code: int
    content_hash: str

    fetched_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class CompetitorProfile(BaseModel):
    name: str
    website: str
    pages: list[ExtractedPage] = Field(default_factory=list)