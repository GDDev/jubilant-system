from flask import abort, url_for, render_template, flash
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from utils import generate_verification_token, send_mail
from ..models import UserMajor
from ..repositories import UserMajorRepository, MajorRepository
from ..exceptions import MajorException


class UserMajorService:
    def __init__(self):
        self.repo = UserMajorRepository()
        self.major_repo = MajorRepository()

    def add(self, **kwargs):
        """
        Adds a UserMajor to the database.

        Args:
            **kwargs: dict of the fields to fill in the UserMajor.

        Returns:
            None
        """
        try:
            if not kwargs['major_id']:
                raise MajorException('Erro ao associar formação ao usuário.')

            return self.repo.insert(UserMajor(**kwargs))
        except SQLAlchemyError as e:
            raise MajorException('Erro ao adicionar formação ao usuário.') from e

    def remove(self, user_major_id):
        """
        Removes a UserMajor from the database.

        Args:
            user_major_id: int of the UserMajor's ID.

        Returns:
            None
        """
        try:
            user_major = self.repo.find_by_id(user_major_id)
            if not user_major:
                raise MajorException('Erro ao deletar formação: Formação não encontrada.')
            self.repo.delete(user_major)
        except MajorException as e:
            raise e
        except SQLAlchemyError as e:
            raise MajorException('Erro ao deletar formação.') from e

    def find_by_id(self, user_major_id: int) -> UserMajor | None:
        """
        Tries to find a UserMajor by its ID.

        Args:
            user_major_id: into of the UserMajor's ID.

        Returns:
            Found UserMajor or None.
        """
        try:
            return self.repo.find_by_id(user_major_id)
        except SQLAlchemyError as e:
            raise MajorException(f'Erro ao buscar formação por ID {user_major_id}.') from e
        except Exception as e:
            raise MajorException('Erro desconhecido.') from e

    def update(self, user_major, **kwargs):
        """
        Updates a UserMajor.

        Args:
            user_major: the UserMajor to be updated.
            **kwargs: dict of the fields to be updated.

        Returns:
            None
        """
        try:
            for arg in kwargs:
                setattr(user_major, arg, kwargs[arg])

            self.repo.update(user_major)
        except SQLAlchemyError as e:
            raise MajorException('Erro ao atualizar formação.') from e
        except Exception as e:
            raise MajorException('Erro desconhecido.') from e

    def approve_major(self, user_major):
        try:
            if user_major.profile_id != current_user.id:
                abort(403)
            user_major.approved = True
            self.repo.update(user_major)
        except (SQLAlchemyError, MajorException) as e:
            raise e

    @staticmethod
    def send_institutional_email_verification(email, user_major_id):
        try:
            token = generate_verification_token(email)
            verify_url = url_for('auth.verify_institutional_email',
                                 token=token,
                                 user_major_id=user_major_id,
                                 _external=True)
            html_body = render_template(
                'verification.html',
                user_name=current_user.user.name + " " + current_user.user.surname,
                verify_url=verify_url
            )
            send_mail(
                subject='Verificação de e-mail institucional',
                body=None,
                to=email,
                html=html_body
            )
            flash('E-mail de verificação enviado, confira sua caixa de entrada.')
        except (MajorException, Exception) as e:
            raise e
