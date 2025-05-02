from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base
from . import Role


class ProfessorRole(Role, Base):
    __tablename__ = 'professors'
    id: Mapped[int] = mapped_column(Integer, ForeignKey('roles.id'), primary_key=True)

    #TODO: Add list of qualifying majors
    #TODO: Add list of teaching in majors
    supervised_students: Mapped[list['StudentRole']] = relationship('StudentRole', back_populates='supervisor', foreign_keys='StudentRole.supervisor_id')

    __mapper_args__ = {
        'polymorphic_identity': 'professor'
    }
