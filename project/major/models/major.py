from datetime import datetime
from enum import Enum

from utils import Base
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


class AreaTags(str, Enum):
    OTHER = 'outro'
    NUTRI = 'nutrição'
    PE = 'educação física'


class Shift(str, Enum):
    MORNING = 'manhã'
    AFTERNOON = 'tarde'
    NIGHT = 'noite'
    FULL_DAY = 'integral'


class MajorMixin:
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    level: Mapped[str] = mapped_column(String(50), nullable=False)
    university: Mapped[str] = mapped_column(String(50), nullable=False)
    uni_acronym: Mapped[str] = mapped_column(String(5), nullable=True)
    area_tag: Mapped[str] = mapped_column(String(50), nullable=False)
    shift: Mapped[Shift] = mapped_column('shift', nullable=True, default=Shift.MORNING)
    min_semesters: Mapped[int] = mapped_column(Integer, nullable=True, default=3)
    max_semesters: Mapped[int] = mapped_column(Integer, nullable=True, default=16)


class Major(Base, MajorMixin):
    __tablename__ = 'majors'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
