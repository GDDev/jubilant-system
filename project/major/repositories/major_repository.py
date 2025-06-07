from core import db
from ..models import Major, TempMajor


class MajorRepository:
    @staticmethod
    def insert(major: Major | TempMajor) -> Major | TempMajor | None:
        db.session.add(major)
        db.session.commit()
        return major

    @staticmethod
    def update(major: Major | TempMajor):
        db.session.commit()

    @staticmethod
    def delete(major: Major | TempMajor):
        db.session.delete(major)
        db.session.commit()

    @staticmethod
    def find_by_id(major_id: int) -> Major | None:
        return db.session.get(Major, major_id)

    @staticmethod
    def find_temp_by_id(major_id: int) -> TempMajor | None:
        return db.session.get(TempMajor, major_id)

    @staticmethod
    def find_by_ilike_uni(uni_name: str) -> list[Major] | None:
        return (db.session.query(Major.university, Major.uni_acronym)
                .filter(Major.university.ilike(f'%{uni_name}%'))
                .distinct()
                .order_by(Major.university)
                .limit(10)
                .all())

    @staticmethod
    def get_levels_by_uni(university: str, acronym: str) -> list[str] | None:
        rows = (db.session.query(Major.level)
                .filter(Major.university == university, Major.uni_acronym == acronym)
                .distinct()
                .order_by(Major.level)
                .all())
        return [row[0] for row in rows]

    @staticmethod
    def get_majors_by_uni_and_level(university: str, uni_acronym: str, level: str) -> list[Major] | None:
        return (db.session.query(Major)
                .filter(Major.university == university, Major.uni_acronym == uni_acronym, Major.level == level)
                .order_by(Major.name)
                .all())

    @staticmethod
    def exists(uni, acronym, level, name, shift):
        return db.session.query(Major).filter_by(university=uni, uni_acronym=acronym, level=level, name=name, shift=shift).first()

    @staticmethod
    def temp_exists(uni, acronym, level, name, shift):
        return db.session.query(TempMajor).filter_by(university=uni, uni_acronym=acronym, level=level, name=name, shift=shift).first()

    @staticmethod
    def get_available_tags():
        return [
            tag for (tag,) in db.session.query(Major.area_tag).distinct().order_by(Major.area_tag).all()
        ]

    def get_available_levels(self):
        return [tag for (tag,) in db.session.query(Major.level).distinct().order_by(Major.level).all()]

    def get_available_names(self):
        return [name for (name,) in db.session.query(Major.name).distinct().order_by(Major.name).all()]
