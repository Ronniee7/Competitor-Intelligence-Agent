from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Competitor(Base):

    __tablename__ = "competitors"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    website: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    pages = relationship(
        "ResearchPage",
        back_populates="competitor",
        cascade="all, delete-orphan",
    )


class ResearchPage(Base):

    __tablename__ = "research_pages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    competitor_id: Mapped[int] = mapped_column(
        ForeignKey("competitors.id"),
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    title: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    content_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    competitor = relationship(
        "Competitor",
        back_populates="pages",
    )