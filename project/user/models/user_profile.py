import uuid

from core import Base
from flask_login import UserMixin  # type: ignore
from sqlalchemy import Integer, String, ForeignKey, UUID  # type: ignore
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore
from secrets import token_hex


class UserProfile(UserMixin, Base):
    __tablename__ = 'profiles'
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True, 
        default=str(uuid.uuid4())
    )
    alt_id: Mapped[str] = mapped_column(
        String(36),
        unique=True, 
        default=str(uuid.uuid4())
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
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default='none'
    )
    visibility: Mapped[str] = mapped_column(
        String(20), 
        nullable=False,
        default='public'
    )

    profile_pic: Mapped[str] = mapped_column(
        String(250),
        nullable=False,
        default='/static/img/user.png'
    )

    user: Mapped['User'] = relationship('User', back_populates='profile')

    sent_friend_requests: Mapped[list['Friendship']] = relationship(
        'Friendship',
        back_populates='sender',
        foreign_keys='[Friendship.sender_id]',
        cascade='all, delete-orphan'
    )
    received_friend_requests: Mapped[list['Friendship']] = relationship(
        'Friendship',
        back_populates='receiver',
        foreign_keys='[Friendship.receiver_id]',
        cascade='all, delete-orphan'
    )

    def get_id(self):
        return self.alt_id

    @property
    def friends(self) -> list['UserProfile']:
        return [f.receiver for f in self.sent_friend_requests if f.status == 'accepted'] + \
            [f.sender for f in self.received_friend_requests if f.status == 'accepted']

    @property
    def pending_friend_requests(self) -> list['UserProfile']:
        return [f.sender for f in self.received_friend_requests if f.status == 'pending']
