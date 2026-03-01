import datetime
from enum import StrEnum

from sqlalchemy import TEXT, DateTime, Enum, Column, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ArticleStatus(StrEnum):
    PUBLISHED = "published"
    DELETED = "deleted"
    ARCHIVED = "archived"
    DRAFT = "draft"


class Article(Base):
    __tablename__ = "article"

    __table_args__ = (
        Index(
            "article_org_slug_slug_unique",
            "org_slug",
            "slug",
            unique=True,
            postgresql_where=Column("status") != "deleted",  # правильное условие
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    org_slug: Mapped[str]
    slug: Mapped[str]
    title: Mapped[str]
    content: Mapped[str] = mapped_column(TEXT)
    owner: Mapped[str]
    status: Mapped[ArticleStatus] = mapped_column(Enum(ArticleStatus, native_enum=False))
    create_ts: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, nullable=False)