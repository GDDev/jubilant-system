import uuid
from datetime import datetime

from core import Base

from sqlalchemy import Integer, String, ForeignKey, UUID, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class Friendship(Base):
    __tablename__ = 'friendships'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('profiles.id'))
    friend_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('profiles.id'))
    status: Mapped[str] = mapped_column(String(10), nullable=False, default='pending')
    sent_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    accepted_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
