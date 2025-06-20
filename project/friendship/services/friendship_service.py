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
                raise FriendshipException('Erro ao adicionar amigo') from e
        else:
            raise FriendshipException('Solicitação de amizade já enviada.')

    def accept_request(self, friendship) -> None:
        if friendship.status == 'accepted':
            raise FriendshipException('Solicitação de amizade já aceita.')
        try:
            self.friendship_repo.accept_request(friendship)
        except (FriendshipException, SQLAlchemyError, Exception) as e:
            raise FriendshipException('Erro ao aceitar solicitação de amizade: ') from e

    def decline_request(self, request_id: int) -> None:
        try:
            friendship = self.friendship_repo.find_by_id(request_id)
            if friendship:
                self.friendship_repo.delete(friendship)
        except SQLAlchemyError as e:
            raise FriendshipException('Erro ao recusar solicitação de amizade') from e

    def get_open_requests(self, user_id) -> list[Friendship] | None:
        try:
            return self.friendship_repo.find_pending_by_receiver_id(user_id)
        except:
            raise FriendshipException('Erro ao buscar solicitações de amizade.')

    def remove_friendship(self, friendship):
        try:
            self.friendship_repo.delete(friendship)
        except (SQLAlchemyError, Exception) as e:
            raise FriendshipException('Erro ao remover solicitação de amizade')

    def find_by_id(self, friendship_id: int) -> Friendship | None:
        try:
            return self.friendship_repo.find_by_id(friendship_id)
        except (SQLAlchemyError, Exception) as e:
            raise FriendshipException('Erro ao buscar amizade/solicitação.') from e

    @staticmethod
    def get_friend_suggestions():
        from project.user import UserProfileRepository
        from random import choices
        profile_repo = UserProfileRepository()
        try:
            not_friends = [p for p in profile_repo.find_all() if p not in current_user.friends]
            return choices(not_friends, k=5)
        except (SQLAlchemyError, Exception) as e:
            raise FriendshipException('Erro ao gerar sugestão de amigos.') from e
