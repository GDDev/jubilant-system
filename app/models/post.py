import uuid
from datetime import datetime

from app.utils import Base

from sqlalchemy import Integer, String, ForeignKey, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('profiles.id'))
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    last_updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now())
