from secrets import choice

from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from ..models import Major, TempMajor
from ..repositories import MajorRepository
from ..exceptions import MajorException


def choose_admin():
    from ...user import UserProfileService
    user_profile_service = UserProfileService()
    admins = user_profile_service.get_admins()
    if admins:
        return choice(admins)
    else:
        return None


class MajorService:
    def __init__(self):
        self.major_repo = MajorRepository()

    def add_temp(self, **kwargs) -> TempMajor | None:
        try:
            admin = choose_admin()
            return self.major_repo.insert(TempMajor(submitted_by=current_user.id, assigned_to=admin.id ,**kwargs))
        except SQLAlchemyError as e:
            raise MajorException('Erro ao cadastrar formação.') from e

    def update(self, major: Major | TempMajor, **kwargs):
        try:
            if not self.major_repo.find_by_id(major.id) and not self.major_repo.find_temp_by_id(major.id):
                raise MajorException('Formção não encontrada.')

            for arg in kwargs:
                if arg in major.__dict__:
                    setattr(major, arg, kwargs[arg])

            self.major_repo.update(major)
        except SQLAlchemyError as e:
            raise MajorException('Erro ao atualizar formação.') from e

    def delete(self, major):
        try:
            self.major_repo.delete(major)
        except SQLAlchemyError as e:
            raise MajorException('Erro ao remover formação.') from e

    def find_by_id(self, major_id: int) -> Major | None:
        try:
            return self.major_repo.find_by_id(major_id)
        except SQLAlchemyError as e:
            raise MajorException('Erro ao buscar formação.') from e

    def find_temp_by_id(self, major_id: int) -> TempMajor | None:
        try:
            return self.major_repo.find_temp_by_id(major_id)
        except SQLAlchemyError as e:
            raise MajorException('Erro ao buscar formação.') from e

    def find_by_ilike_university(self, university: str) -> list[Major | TempMajor] | None:
        try:
            return self.major_repo.find_by_ilike_uni(university)
        except SQLAlchemyError as e:
            raise MajorException(f'Erro ao buscar formações por universidade {university}.') from e

    def get_levels_by_uni(self, university: str, acronym: str) -> list[str] | None:
        try:
            return self.major_repo.get_levels_by_uni(university, acronym)
        except SQLAlchemyError as e:
            raise MajorException(f'Erro ao buscar níveis de formação para a universidade {university} - {acronym}.') from e

    def get_majors_by_uni_and_level(self, university, uni_acronym, level) -> list[Major] | None:
        try:
            return self.major_repo.get_majors_by_uni_and_level(university, uni_acronym, level)
        except SQLAlchemyError as e:
            raise MajorException(f'Erro ao buscar formações de nível {level} para a universidade {university} - {uni_acronym}.') from e

    def exists(self, uni, acronym, level, name, shift) -> Major | None:
        try:
            return self.major_repo.exists(uni, acronym, level, name, shift)
        except SQLAlchemyError as e:
            raise MajorException('Erro ao checar existência da formação.') from e

    def exists_as_temp(self, uni, acronym, level, name, shift) -> TempMajor | None:
        try:
            return self.major_repo.temp_exists(uni, acronym, level, name, shift)
        except SQLAlchemyError as e:
            raise MajorException('Erro ao checar existência da formação.') from e
