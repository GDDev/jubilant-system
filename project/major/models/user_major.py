from enum import Enum

from datetime import date

from core import Base

from sqlalchemy import Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MajorEnum(str, Enum):
    STUDENT = 'estudante'
    PROFESSOR = 'professor'


class UserMajor(Base):
    __tablename__ = 'user_majors'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey('profiles.id'), nullable=False)
    major_id: Mapped[int] = mapped_column(Integer, ForeignKey('majors.id'), unique=True, nullable=True)
    temp_major_id: Mapped[int] = mapped_column(Integer, ForeignKey('temp_majors.id'), unique=True, nullable=True)
    college_code: Mapped[str] = mapped_column(String(50), nullable=False)
    institutional_email: Mapped[str] = mapped_column(String(100), nullable=False)
    user_is: Mapped[MajorEnum] = mapped_column('training', nullable=False, default=MajorEnum.STUDENT)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    approved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    major: Mapped['Major'] = relationship('Major', foreign_keys=[major_id])
    temp_major: Mapped['TempMajor'] = relationship('TempMajor', foreign_keys=[temp_major_id])
    profile: Mapped['UserProfile'] = relationship('UserProfile', back_populates='majors', foreign_keys=[profile_id])
