from app.models import User
from app.utils import db

class UserRepository:
    def insert(user: User) -> User | None:
        db.session.add(user)
        db.session.commit()
        return user

    def delete(user: User) -> None:
        db.session.delete(user)
        db.session.commit()

    def find_by_id(user_id: User) -> User | None:
        return db.session.get(User, user_id)

    def find_by_email(email: str) -> User | None:
        # return db.session.get(User, email)
        return db.session.query(User).filter_by(email=email).first()