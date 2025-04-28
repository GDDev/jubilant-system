from core import db
from ..models import Notification


class NotificationRepository:

    @staticmethod
    def insert(notification) -> None:
        db.session.add(notification)
        db.session.commit()

    @staticmethod
    def find_by_id(notification_id) -> Notification | None:
        return db.session.get(Notification, notification_id)

    @staticmethod
    def open_notification(notification: Notification):
        notification.seen = True
        db.session.commit()

    @staticmethod
    def find_by_receiver_id(receiver_id):
        return db.session.query(Notification).filter_by(receiver_id=receiver_id).all()

    @staticmethod
    def delete(notification):
        db.session.delete(notification)
        db.session.commit()
