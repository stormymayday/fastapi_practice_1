from __future__ import annotations

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from database import Base

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, default=False)