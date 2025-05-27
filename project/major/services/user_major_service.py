from sqlalchemy.exc import SQLAlchemyError

from ..models import UserMajor
from ..repositories import UserMajorRepository, MajorRepository
from ..exceptions import MajorException


class UserMajorService:
    def __init__(self):
        self.repo = UserMajorRepository()
        self.major_repo = MajorRepository()

    def add(self, **kwargs):
        try:
            if not kwargs['major_id'] and not kwargs['temp_major_id']:
                raise MajorException('Erro ao associar formação ao usuário.')

            self.repo.insert(UserMajor(**kwargs))
        except SQLAlchemyError as e:
            raise MajorException('Erro ao adicionar formação ao usuário.') from e

    def remove(self, user_major_id):
        try:
            user_major = self.repo.find_by_id(user_major_id)
            if not user_major:
                raise MajorException('Erro ao deletar formação: Formação não encontrada.')
            self.repo.delete(user_major)
        except MajorException as e:
            raise e
        except SQLAlchemyError as e:
            raise MajorException('Erro ao deletar formação.') from e
