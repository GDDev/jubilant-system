from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from core import db
from ..exceptions import AuthException
from project.user import UserRepository, UserProfileRepository, User, UserProfile
from werkzeug.security import generate_password_hash, check_password_hash


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
            # Calls a method to insert a user object into the db
            self.user_repository.insert_with_no_commit(user)
            # Calls a method to hash the password
            hashed_pwd = self.hash_password(profile_data['password'])
            # Instantiate UserProfileObject
            user_profile = UserProfile(
                user_id=user.id,
                username=profile_data['username'],
                pwd=hashed_pwd
            )
            # Calls a method to insert a user's profile into the db
            self.user_profile_repository.insert_with_no_commit(user_profile)

            db.session.commit()
            return user_profile

        except IntegrityError as e:
            db.session.rollback()
            raise AuthException('Erro interno ao cadastrar usuário, por favor tente novamente.') from e
        except SQLAlchemyError as e:
            db.session.rollback()
            raise AuthException('Falha ao cadastrar usuário.') from e

    def sign_in_user(self, credential: str, pwd: str) -> UserProfile | None:
        try:
            user = self.user_profile_repository.find_by_username(credential)
            if not user:
                user = self.user_repository.find_by_email(credential)
                if user:
                    user = self.user_profile_repository.find_by_user_id(user.id)
                else:
                    raise AuthException('Usuário não encontrado.')

            if user and check_password_hash(user.pwd, pwd): return user
            return None
        except (SQLAlchemyError, AuthException) as e:
            raise e


    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def validate_sign_up_data(self, form):
        if self.user_repository.find_by_email(form.email.data) is not None:
            raise AuthException('E-mail já cadastrado.')
        elif self.user_profile_repository.find_by_username(form.username.data) is not None:
            raise AuthException(f'Nome de usuário "{form.username.data}" já está em uso.')
