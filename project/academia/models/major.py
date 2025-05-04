from enum import Enum

from core import Base
from sqlalchemy import Integer, String, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class AreaTags(str, Enum):
    OTHER = 'other'
    NUTRI = 'nutrition'
    PE = 'physical_education'


class Major(Base):
    __tablename__ = 'majors'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    level: Mapped[str] = mapped_column(String(50), nullable=False)
    university: Mapped[str] = mapped_column(String(50), nullable=False)
    area_tag: Mapped[AreaTags] = mapped_column('AreaTags', nullable=False, default=AreaTags.OTHER)
