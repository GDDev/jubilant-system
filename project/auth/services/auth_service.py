from sqlalchemy.exc import SQLAlchemyError

from ..exceptions import AuthException
from core import db
from project.user import UserRepository, UserProfileRepository, User, UserProfile
from werkzeug.security import generate_password_hash


class AuthService:

    def __init__(self):
        self.user_repository = UserRepository()
        self.user_profile_repository = UserProfileRepository()

    def sign_up_user(self, user_data: dict, profile_data: dict) -> UserProfile | None:
        # Instantiate User object
        user = User(
            name=user_data['name'],
            surname=user_data['surname'],
            email=user_data['email']
        )
        try:
            print("Begin")
            # Calls a method to insert a user object into the db
            user = self.user_repository.insert(user)

            # Calls a method to hash the password
            pwd = self.hash_password(profile_data['password'])

            # Instantiate UserProfileObject
            user_profile = UserProfile(
                user_id=user.id,
                username=profile_data['username'],
                pwd=pwd,
                role=user_data.get('role')
            )

            # Calls a method to insert a user's profile into the db
            self.user_profile_repository.insert(user_profile)

            return user_profile

        except SQLAlchemyError as e:
            raise AuthException('Falha ao cadastrar usuário.') from e

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def validate_sign_up_data(self, form):
        if self.user_repository.find_by_email(form.email.data) is not None:
            raise AuthException('E-mail já cadastrado.')
        elif self.user_profile_repository.find_by_username(form.username.data) is not None:
            raise AuthException(f'Nome de usuário "{form.username.data}" já está em uso.')
