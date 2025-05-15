import uuid
from datetime import datetime

from core import Base

from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey('profiles.id'))
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    last_updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now())

    profile: Mapped['UserProfile'] = relationship('UserProfile', back_populates='posts', foreign_keys=[profile_id])
