class UserProfileService:
    def create_id(self, userId: int) -> str:
        return '1223' + str(userId)

    def get_id(self) -> str:
        return self._alternative_id

    def get_real_id(self) -> str:
        return self._id

    def create_alternative_id(self) -> str:
        return self._id + '123'