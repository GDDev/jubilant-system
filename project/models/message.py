import uuid
from datetime import datetime

from core import Base

from sqlalchemy import Integer, String, ForeignKey, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column


class Message(Base):
    __tablename__ = 'messages'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey('chats.id'))
    sender_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('profiles.id'))
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='sent')
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    sent_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    opened_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)