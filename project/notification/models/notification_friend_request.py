from typing import Optional

from flask_login import current_user
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .notification import Notification


class NotificationFriendRequest(Notification):
    __tablename__ = 'friend_request_notifications'
    __mapper_args__ = {
        'polymorphic_identity': 'friend_request',
    }

    id: Mapped[int] = mapped_column(ForeignKey('notifications.id'), primary_key=True)
    sender_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('profiles.id'),
        nullable=True,
        comment='ID of the user profile sending the notification'
    )
    friendship_id: Mapped[int] = mapped_column(Integer, ForeignKey('friendships.id'), nullable=False, comment='ID of the friendship')
    url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment='URL to redirect when the notification is clicked')

    sender: Mapped[Optional['UserProfile']] = relationship('UserProfile', back_populates='sent_friend_notifications', foreign_keys=[sender_id])
    friendship: Mapped['Friendship'] = relationship('Friendship')
