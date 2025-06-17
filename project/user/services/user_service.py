from flask import abort
from flask_login import current_user

from .. import User
from ..repositories import UserRepository


class UserService:

    def __init__(self):
        self.user_repository = UserRepository()

    def find_by_id(self, user_id: int):
        user = self.user_repository.find_by_id(user_id)
        if not user:
            abort(404)
        return user

    def find_by_email(self, email: str):
        return self.user_repository.find_by_email(email)

    def update_email(self, user: User, email: str):
        return self.user_repository.update_email(user, email)

    def delete(self, user: User):
        if user.profile.role == 'admin' and current_user.role != 'god':
            raise Exception('Você não pode excluir admins, quem você pensa que é?')
        elif user.profile.id != current_user.id and current_user.role == 'user':
                raise Exception('Você não pode excluir contas alheias')
        else:
            self.user_repository.delete(user)
