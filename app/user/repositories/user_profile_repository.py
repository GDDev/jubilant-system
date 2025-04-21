from app.user import UserProfile
from app import db

class UserProfileRepository:

    @staticmethod
    def insert(profile: UserProfile) -> None:
        db.session.add(profile)
        db.session.commit()

    @staticmethod
    def find_by_username(username: str) -> UserProfile | None:
        return db.session.query(UserProfile).filter_by(username=username).first()
