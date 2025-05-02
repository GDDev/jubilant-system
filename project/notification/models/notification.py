from datetime import datetime
from enum import Enum
from typing import Optional

from core import Base

from sqlalchemy import Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


class NotificationType(str, Enum):
    MESSAGE = 'message'
    FRIEND_REQUEST = 'friend_request'
    FRIEND_ACCEPT = 'friend_accept'
    SYSTEM = 'system'

class Notification(Base):
    """
    A class representing a notification.

    Attributes:
        id (int): Primary key of the notification.
        receiver_id (str): ID of the user profile receiving the notification.
        sender_id (str): ID of the user profile sending the notification. Can be null for system-generated notifications.
        type (NotificationType): Type of the notification, defaulting to SYSTEM.
        content (str): The content of the notification message. Can be null.
        created_at (datetime): Datetime of when the notification was created. Defaults to the current timestamp.
        seen (bool): Indicates whether the receiver has seen the notification. Defaults to False.
        url (str): URL to redirect when the notification is clicked. Can be null.

    Relationships:
        receiver (UserProfile): User receiving the notification.
        sender (UserProfile): User sending the notification. Null for system-generated notifications.
    """
    __tablename__ = 'notifications'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='Primary key')
    receiver_id: Mapped[str] = mapped_column(String(36), ForeignKey('profiles.id'), nullable=False, comment='ID of the user profile receiving the notification')
    type: Mapped[NotificationType] = mapped_column(String(50), nullable=False, default=NotificationType.SYSTEM, comment='Type of the notification')
    content: Mapped[str] = mapped_column(String(100), nullable=True, comment='Content of the notification message')
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now(), comment='Timestamp of the notification creation')
    seen: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment='Whether the receiver has seen the notification')

    __mapper_args__ = {
        'polymorphic_identity': 'system',
        'polymorphic_on': type
    }

    receiver: Mapped['UserProfile'] = relationship('UserProfile', back_populates='notifications', foreign_keys=[receiver_id])

