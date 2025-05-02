from core import db

class RoleRepository:
    @staticmethod
    def insert(role) -> None:
        db.session.add(role)
        db.session.commit()
