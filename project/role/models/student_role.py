from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base
from . import Role


class StudentRole(Role, Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(Integer, ForeignKey('roles.id'), primary_key=True)
    supervisor_id: Mapped[int] = mapped_column(Integer, ForeignKey('professors.id'), nullable=True)

    #TODO: Add list of majors
    supervisor: Mapped['ProfessorRole'] = relationship('ProfessorRole', back_populates='supervised_students', foreign_keys=[supervisor_id])

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }
