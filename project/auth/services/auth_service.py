from flask import render_template
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from core import db, send_mail
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

            if profile_data.get('google_id'): user_profile.google_id = profile_data['google_id']
            if profile_data.get('profile_pic'): user_profile.profile_pic = profile_data['profile_pic']

            # Calls a method to insert a user's profile into the db
            self.user_profile_repository.insert_with_no_commit(user_profile)

            db.session.commit()
            return user_profile

        except IntegrityError as e:
            db.session.rollback()
            raise AuthException('Erro interno ao cadastrar usuário, por favor tente novamente.' + e._message()) from e
        except SQLAlchemyError as e:
            db.session.rollback()
            raise AuthException('Falha ao cadastrar usuário.' + e._message()) from e

    def sign_in_user(self, credential: str, pwd: str) -> UserProfile | None:
        try:
            user = self.user_profile_repository.find_by_username(credential)
            if not user:
                user = self.user_repository.find_by_email(credential)
                if not user:
                    raise AuthException('Usuário ou senha incorretos.')
                user = self.user_profile_repository.find_by_user_id(user.id)

            if user and check_password_hash(user.pwd, pwd): return user
            raise AuthException('Usuário ou senha incorretos.')
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

    def find_user_by_email(self, email):
        try:
            return self.user_repository.find_by_email(email)
        except SQLAlchemyError as e:
            raise AuthException('Erro ao buscar usuário por e-mail.') from e

    def forgot_password(self, email):
        from secrets import token_urlsafe
        try:
            user = self.user_repository.find_by_email(email)
            if not user:
                raise AuthException('Erro ao redefinir senha: usuário não encontrado.')

            new_pwd = token_urlsafe(18)
            user.profile.pwd = self.hash_password(new_pwd)
            self.user_profile_repository.update(user.profile)

            html_body = render_template(
                'new_pwd.html',
                new_password=new_pwd,
                user_name=user.name+" "+user.surname
            )
            text_body = f"Olá {user.name},\n\nAqui está sua nova senha: {new_pwd}\n\nPor favor, troque-a assim que possível."
            send_mail(
                subject='Redefinição de senha - Jubilant System',
                body=text_body,
                to=email,
                html=html_body,
            )
            return True
        except (SQLAlchemyError, AuthException) as e:
            raise AuthException('Erro ao redefinir senha.') from e
        except Exception as e:
            raise AuthException(f'Ocorreu um erro desconhecido. {str(e)}') from e
