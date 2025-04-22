import uuid
from datetime import datetime

from core import Base

from sqlalchemy import Integer, String, ForeignKey, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column


class Comment(Base):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('profiles.id'))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'))
    comment: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    last_updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now())
