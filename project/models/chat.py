from datetime import datetime

from core import Base

from sqlalchemy import Integer, ForeignKey, UUID, DateTime
from sqlalchemy.orm import Mapped, mapped_column
import uuid

class Chat(Base):
    __tablename__ = 'chats'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('profiles.id'))
    chatting_with: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())

