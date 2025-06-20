from flask import abort
from numpy.random import choice
from sqlalchemy.exc import SQLAlchemyError

from utils.regex import re_search
from utils.normalize import strip_lower
from .. import UserProfile
from ..repositories import UserProfileRepository
from ...friendship import FriendshipRepository
from ..exceptions import UserProfileException
from re import match


class UserProfileService:

    def __init__(self):
        self.user_profile_repository = UserProfileRepository()
        self.friendship_repository = FriendshipRepository()

    def update(self, profile, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(profile, key, value)
        self.user_profile_repository.update(profile)

    def find_by_id(self, user_profile_id: str):
        return self.user_profile_repository.find_by_id(user_profile_id)

    def find_by_user_id(self, user_id: int):
        return self.user_profile_repository.find_by_user_id(user_id)

    def find_by_username(self, username: str):
        return self.user_profile_repository.find_by_username(username)

    def new_alt_id(self, profile: UserProfile):
        return self.user_profile_repository.new_alt_id(profile)

    def find_by_code(self, code):
        profile = self.user_profile_repository.find_by_code(code)
        if not profile or not self.check_profile_visibility(profile):
            abort(404)
        return profile

    @staticmethod
    def check_profile_visibility(profile: UserProfile):
        if profile.visibility == 'public':
            return True
        return False

    def find_profiles_by_search(self, search):
        if not search or search.strip() == '':
            users = self.user_profile_repository.find_all()
            return users if len(users) <= 10 else choice(users, 10, False).tolist()
        search = strip_lower(search)
        if not match(re_search, search):
            raise UserProfileException('Termo de busca não permitido')
        return self.user_profile_repository.find_profiles_by_search(search)

    def friendship_request(self, current_user, user_profile):
        friendship = (self.friendship_repository.find_by_sender_id_receiver_id(current_user.id, user_profile.id) or
                      self.friendship_repository.find_by_sender_id_receiver_id(user_profile.id, current_user.id))
        if friendship:
            return friendship, friendship.sender
        return None, None

    def get_admins(self):
        return self.user_profile_repository.get_admins()

    def get_all_pagination(self, page: int, per_page: int, role: str = 'user'):
        try:
            return self.user_profile_repository.get_all_pagination(page, per_page, role)
        except SQLAlchemyError as e:
            raise UserProfileException('Erro ao buscar todos os usuários.') from e
