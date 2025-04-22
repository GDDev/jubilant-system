import uuid

from core import Base
from sqlalchemy import Integer, String, Date, UUID
from sqlalchemy.orm import Mapped, mapped_column

class Major(Base):
    __tablename__ = 'majors'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    degree: Mapped[str] = mapped_column(String(50), nullable=False)
    major: Mapped[str] = mapped_column(String(50), nullable=False)
    start: Mapped[Date] = mapped_column(Date, nullable=False)
    end: Mapped[Date] = mapped_column(Date, nullable=False)
