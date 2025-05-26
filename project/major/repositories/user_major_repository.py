from core import db
from ..models import UserMajor


class UserMajorRepository:
    @staticmethod
    def insert(user_major: UserMajor):
        db.session.add(user_major)
        db.session.commit()

    @staticmethod
    def update(user_major):
        db.session.commit()

    @staticmethod
    def delete(user_major):
        db.session.delete(user_major)
        db.session.commit()

    @staticmethod
    def find_by_id(user_major_id):
        return db.session.get(UserMajor, user_major_id)
