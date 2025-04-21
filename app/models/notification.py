import uuid
from datetime import datetime

from core import Base

from sqlalchemy import Integer, String, ForeignKey, DateTime, UUID, Boolean
from sqlalchemy.orm import Mapped, mapped_column


class Notification(Base):
    __tablename__ = 'notifications'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('profiles.id'))
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    message: Mapped[str] = mapped_column(String(500), nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now())