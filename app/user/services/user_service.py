from app.user import UserRepository


class UserService:

    def __init__(self):
        self.user_repository = UserRepository()

    def find_by_id(self, user_id: int):
        return self.user_repository.find_by_id(user_id)

    def find_by_email(self, email: str):
        return self.user_repository.find_by_email(email)
