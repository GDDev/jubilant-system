from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from .. import Friendship
from ..repositories import FriendshipRepository
from ..exceptions import FriendshipException


class FriendshipService:
    def __init__(self):
        self.friendship_repo = FriendshipRepository()

    def send_request(self, friend_id: str) -> Friendship | None:
        if not self.friendship_repo.find_by_sender_id_receiver_id(current_user.id, friend_id):
            friendship = Friendship(sender_id=current_user.id, receiver_id=friend_id)
            try:
                return self.friendship_repo.insert(friendship)
            except SQLAlchemyError as e:
                raise FriendshipException('Erro ao adicionar amigo: ' + str(e._message()))
        else:
            raise FriendshipException('Solicitação de amizade já enviada.')

    def accept_request(self, request_id: int) -> None:
        friendship = self.friendship_repo.find_by_id(request_id)
        if friendship:
            if friendship.status == 'accepted':
                raise FriendshipException('Solicitação de amizade já aceita.')
            try:
                self.friendship_repo.accept_request(friendship)
            except SQLAlchemyError as e:
                raise FriendshipException('Erro ao aceitar solicitação de amizade: ')

    def decline_request(self, request_id: int) -> None:
        try:
            friendship = self.friendship_repo.find_by_id(request_id)
            self.friendship_repo.decline_request(friendship)
        except SQLAlchemyError as e:
            raise FriendshipException('Erro ao recusar solicitação de amizade: ' + str(e._message()))

    def get_open_requests(self, user_id) -> list[Friendship] | None:
        try:
            return self.friendship_repo.find_pending_by_receiver_id(user_id)
        except:
            raise FriendshipException('Erro ao buscar solicitações de amizade.')