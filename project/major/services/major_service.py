from secrets import choice

from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from ..models import Major
from ..repositories import MajorRepository
from ..exceptions import MajorException


def choose_admin():
    """
    Randomly chooses an admin from the database.
    Returns:
        The chosen admin.
    """
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

    def update(self, major: Major, **kwargs):
        """
        Updates Major.

        Args:
            major: Major to be updated.
            **kwargs: Named fields to be updated.

        Returns:
            None
        """
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
        """
        Deletes a major from the database.

        Args:
            major: Major to be deleted.

        Returns:
            None
        """
        try:
            self.major_repo.delete(major)
        except SQLAlchemyError as e:
            raise MajorException('Erro ao remover formação.') from e

    def find_by_id(self, major_id: int) -> Major | None:
        """
        Finds a major by its ID.

        Args:
            major_id: int of the major's ID.

        Returns:
            The found Major or None.
        """
        try:
            return self.major_repo.find_by_id(major_id)
        except SQLAlchemyError as e:
            raise MajorException('Erro ao buscar formação.') from e

    def find_by_ilike_university(self, university: str) -> list[Major] | None:
        """
        Returns a list of majors that match the given university.

        Args:
            university: str of the university to match.

        Returns:
            List of Majors that match the given university.
        """
        try:
            return self.major_repo.find_by_ilike_uni(university)
        except SQLAlchemyError as e:
            raise MajorException(f'Erro ao buscar formações por universidade {university}.') from e

    def get_levels_by_uni(self, university: str, acronym: str) -> list[str] | None:
        """
        Finds all levels of a specific university defined by its name and acronym.

        Args:
            university: str of the University's name.
            acronym: str of the University's acronym.

        Returns:
            A list with the levels of the University.
        """
        try:
            return self.major_repo.get_levels_by_uni(university, acronym)
        except SQLAlchemyError as e:
            raise MajorException(f'Erro ao buscar níveis de formação para a universidade {university} - {acronym}.') from e

    def get_majors_by_uni_and_level(self, university, uni_acronym, level) -> list[Major] | None:
        """
        Finds all majors of a specific university matching name, acronym and level.

        Args:
            university: str of the University's name.
            uni_acronym: str of the University's acronym.
            level: str of the level of the majors to be retrieved.

        Returns:
            A list with the majors of the University for the level informed.
        """
        try:
            return self.major_repo.get_majors_by_uni_and_level(university, uni_acronym, level)
        except SQLAlchemyError as e:
            raise MajorException(f'Erro ao buscar formações de nível {level} para a universidade {university} - {uni_acronym}.') from e

    def exists(self, uni, acronym, level, name, shift) -> Major | None:
        """
        Tries to find an existing Major by its fields.

        Args:
            uni: str of the University's name.
            acronym: str of the University's acronym.
            level: str of the Major's level.
            name: str of the Major's name.
            shift: str of the Major's shift.

        Returns:
            The found Major or None.
        """
        try:
            return self.major_repo.exists(uni, acronym, level, name, shift)
        except SQLAlchemyError as e:
            raise MajorException('Erro ao checar existência da formação.') from e

    def get_area_choices(self):
        return self.major_repo.get_available_tags()

    def get_level_choices(self):
        return self.major_repo.get_available_levels()

    def get_names_choices(self):
        return self.major_repo.get_available_names()
