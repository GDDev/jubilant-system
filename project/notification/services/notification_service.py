from abc import abstractmethod

from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from ..models import Notification, NotificationType
from ..models.notification_friend_request import NotificationFriendRequest
from ..repositories import NotificationRepository
from ..exceptions import NotificationException


class NotificationService:

    def __init__(self):
        self.noti_repo = NotificationRepository()

    def get_all_by_receiver_id(self, receiver_id: str) -> list[Notification] | None:
        try:
            return self.noti_repo.find_by_receiver_id(receiver_id)
        except SQLAlchemyError as e:
            raise NotificationException('Erro ao recuperar notificações.') from e

    @staticmethod
    def instantiate_notification(**kwargs) -> Notification:
        if kwargs.get('type') == NotificationType.FRIEND_REQUEST:
            return NotificationFriendRequest(**kwargs)
        return Notification(**kwargs)

    def send_notification(self, **kwargs) -> None:
        try:
            self.noti_repo.insert(self.instantiate_notification(**kwargs))
        except SQLAlchemyError as e:
            raise NotificationException('Erro ao enviar notificação.') from e

    def open_notification(self, notification_id: int) -> None:
        try:
            self.noti_repo.open_notification(self.noti_repo.find_by_id(notification_id))
        except SQLAlchemyError as e:
            raise NotificationException('Erro ao marcar notificação como lida.') from e

    def get_by_id(self, notification_id):
        pass

    def delete(self, notification):
        try:
            self.noti_repo.delete(notification)
        except SQLAlchemyError as e:
            raise NotificationException('Erro ao excluir notificação.') from e
