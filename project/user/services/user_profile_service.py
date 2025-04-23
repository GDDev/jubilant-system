from .. import UserProfile
from ..repositories import UserProfileRepository


class UserProfileService:

    def __init__(self):
        self.user_profile_repository = UserProfileRepository()

    def find_by_id(self, user_profile_id: str):
        return self.user_profile_repository.find_by_id(user_profile_id)

    def find_by_user_id(self, user_id: int):
        return self.user_profile_repository.find_by_user_id(user_id)

    def find_by_username(self, username: str):
        return self.user_profile_repository.find_by_username(username)

    def new_alt_id(self, profile: UserProfile):
        return self.user_profile_repository.new_alt_id(profile)
