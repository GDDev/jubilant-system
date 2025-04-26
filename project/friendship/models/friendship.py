from datetime import datetime
from core import Base

from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Friendship(Base):
    __tablename__ = 'friendships'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sender_id: Mapped[str] = mapped_column(String(36), ForeignKey('profiles.id'), nullable=False)
    receiver_id: Mapped[str] = mapped_column(String(36), ForeignKey('profiles.id'), nullable=False)
    status: Mapped[str] = mapped_column(String(10), nullable=False, default='pending')
    sent_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    accepted_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    sender: Mapped['UserProfile'] = relationship('UserProfile', back_populates='sent_friend_requests', foreign_keys=[sender_id])
    receiver: Mapped['UserProfile'] = relationship('UserProfile', back_populates='received_friend_requests', foreign_keys=[receiver_id])
