from datetime import datetime

from utils import Base

from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Comment(Base):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey('profiles.id'))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'))
    comment: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    last_updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now())

    post: Mapped['Post'] = relationship('Post', back_populates='comments', foreign_keys=[post_id])
    profile: Mapped['UserProfile'] = relationship('UserProfile', back_populates='comments', foreign_keys=[profile_id])
