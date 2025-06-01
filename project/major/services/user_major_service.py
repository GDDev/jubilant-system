from sqlalchemy.exc import SQLAlchemyError

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
            if not kwargs['major_id'] and not kwargs['temp_major_id']:
                raise MajorException('Erro ao associar formação ao usuário.')

            self.repo.insert(UserMajor(**kwargs))
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
            if user_major.user_is.lower() == 'student':
                user_major.approved = True
            else:
                user_major.approved = False

            self.repo.update(user_major)
        except SQLAlchemyError as e:
            raise MajorException('Erro ao atualizar formação.') from e
        except Exception as e:
            raise MajorException('Erro desconhecido.') from e
