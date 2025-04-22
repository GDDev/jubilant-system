from project.user import UserProfile
from core import db

class UserProfileRepository:

    @staticmethod
    def insert(profile: UserProfile) -> None:
        db.session.add(profile)
        db.session.commit()

    @staticmethod
    def find_by_username(username: str) -> UserProfile | None:
        return db.session.query(UserProfile).filter_by(username=username).first()

    @staticmethod
    def find_by_user_id(user_id: int) -> UserProfile | None:
        return db.session.query(UserProfile).filter_by(user_id=user_id).first()
