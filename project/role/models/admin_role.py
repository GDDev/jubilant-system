from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core import Base
from . import Role


class AdminRole(Role, Base):
    __tablename__ = 'admins'
    id: Mapped[int] = mapped_column(ForeignKey('roles.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }
