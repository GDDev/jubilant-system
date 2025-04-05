import uuid

from app.utils import Base
from flask_login import UserMixin  # type: ignore
from sqlalchemy import Integer, String, ForeignKey, UUID  # type: ignore
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore
from secrets import token_hex


class UserProfile(UserMixin, Base):
    __tablename__ = 'profiles'
    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True, 
        default=uuid.uuid4()
    )
    alt_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        unique=True, 
        default=uuid.uuid4()
    )
    code: Mapped[str] = mapped_column(
        String(12),
        unique=True,
        default=lambda: token_hex(6)
    )
    user_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('users.id'), 
        unique=True
    )
    username: Mapped[str] = mapped_column(
        String(25), 
        unique=True, 
        nullable=False
    )
    pwd: Mapped[str] = mapped_column(
        String(250), 
        nullable=False
    )
    visibility: Mapped[str] = mapped_column(
        String(20), 
        nullable=False,
        default='public'
    )

    user: Mapped['User'] = relationship('User', back_populates='profile')


    def get_id(self):
        return str(self.alt_id)

    # def __init__(self, user_id: int, username: str, pwd: str, id: str = None, alt_id: str = None, visibility: str = 'public'):
    #     self.id = id or str(uuid4())
    #     self.alt_id = alt_id or str(uuid4())
    #     self.user_id = user_id
    #     self.username = username
    #     self.pwd = pwd
    #     self.visibility = visibility
