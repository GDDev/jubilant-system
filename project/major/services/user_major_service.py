from sqlalchemy.exc import SQLAlchemyError

from ..models import UserMajor
from ..repositories import UserMajorRepository
from ..exceptions import MajorException


class UserMajorService:
    def __init__(self):
        self.repo = UserMajorRepository()

    def add(self, **kwargs):
        try:
            self.repo.insert(UserMajor(**kwargs))
        except SQLAlchemyError as e:
            raise MajorException('Erro ao adicionar formação ao usuário.') from e
