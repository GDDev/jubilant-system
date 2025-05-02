from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from core import Base


class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey('profiles.id'), nullable=False)

    profile: Mapped['UserProfile'] = relationship('UserProfile', back_populates='roles', foreign_keys=[profile_id])

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'none'
    }
