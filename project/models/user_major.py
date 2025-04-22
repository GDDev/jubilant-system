import uuid

from core import Base

from sqlalchemy import Integer, String, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column


class UserMajor(Base):
    __tablename__ = 'user_majors'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('profiles.id'))
    major_id: Mapped[int] = mapped_column(Integer, ForeignKey('majors.id'))
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    university: Mapped[str] = mapped_column(String(50), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False, default='student')
