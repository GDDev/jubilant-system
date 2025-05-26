from datetime import datetime
from enum import Enum

from core import Base
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
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    level: Mapped[str] = mapped_column(String(50), nullable=False)
    university: Mapped[str] = mapped_column(String(50), nullable=False)
    uni_acronym: Mapped[str] = mapped_column(String(5), nullable=True)
    area_tag: Mapped[AreaTags] = mapped_column('tag', nullable=False, default=AreaTags.OTHER)
    shift: Mapped[Shift] = mapped_column('shift', nullable=True, default=Shift.MORNING)
    min_semesters: Mapped[int] = mapped_column(Integer, nullable=True, default=3)
    max_semesters: Mapped[int] = mapped_column(Integer, nullable=True, default=16)


class Major(Base, MajorMixin):
    __tablename__ = 'majors'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TempMajor(Base, MajorMixin):
    __tablename__ = 'temp_majors'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    submitted_by: Mapped[str] = mapped_column(String(36), ForeignKey('profiles.id', ondelete='set null'), nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    assigned_to: Mapped[str] = mapped_column(String(36), ForeignKey('profiles.id', ondelete='set null'), nullable=True)

    submitter: Mapped['UserProfile'] = relationship('UserProfile', foreign_keys=[submitted_by], back_populates='submitted_temp_majors')
    assigned_admin: Mapped['UserProfile'] = relationship('UserProfile', foreign_keys=[assigned_to], back_populates='assigned_temp_majors')
