from sqlalchemy.exc import SQLAlchemyError

from ..models import UserMajor
from ..repositories import UserMajorRepository, MajorRepository
from ..exceptions import MajorException


class UserMajorService:
    def __init__(self):
        self.repo = UserMajorRepository()
        self.major_repo = MajorRepository()

    def add(self, is_major_temp, major_id, **kwargs):
        try:
            user_major = UserMajor(**kwargs)
            if is_major_temp:
                user_major.temp_major_id = major_id
            else:
                user_major.major_id = major_id

            self.repo.insert(user_major)
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
