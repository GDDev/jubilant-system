from project.user import User
from core import db

class UserRepository:
    @staticmethod
    def insert(user: User) -> User | None:
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def insert_with_no_commit(session, user: User) -> User | None:
        session.add(user)
        session.flush()

    @staticmethod
    def delete(user: User) -> None:
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def find_by_id(user_id: int) -> User | None:
        return db.session.get(User, user_id)

    @staticmethod
    def find_by_email(email: str) -> User | None:
        return db.session.query(User).filter_by(email=email).first()

    @staticmethod
    def update_email(user: User, email: str) -> User | None:
        user.email = email
        db.session.commit()
        return user
