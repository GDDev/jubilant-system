import uuid

from sqlalchemy import or_, func
from sqlalchemy.orm import joinedload

from project.user import UserProfile, User
from core import db

class UserProfileRepository:

    @staticmethod
    def insert(profile: UserProfile) -> None:
        db.session.add(profile)
        db.session.commit()

    def insert_with_no_commit(self, session, profile: UserProfile) -> None:
        # session.add(self.assure_uuid_uniqueness(profile))
        session.add(profile)

    @staticmethod
    def find_by_id(user_profile_id: str) -> UserProfile | None:
        return db.session.get(UserProfile, user_profile_id)

    @staticmethod
    def find_by_username(username: str) -> UserProfile | None:
        return db.session.query(UserProfile).filter_by(username=username).first()

    @staticmethod
    def find_by_ilike_username(username: str) -> list[UserProfile]:
        return db.session.query(UserProfile).filter(UserProfile.username.ilike(f'%{username}%')).all()

    @staticmethod
    def find_by_user_id(user_id: int) -> UserProfile | None:
        return db.session.query(UserProfile).filter_by(user_id=user_id).first()

    @staticmethod
    def new_alt_id(profile: UserProfile) -> UserProfile | None:
        profile.alt_id = str(uuid.uuid4())
        db.session.commit()
        return profile

    @staticmethod
    def find_by_code(code):
        return db.session.query(UserProfile).filter_by(code=code).first()

    @staticmethod
    def find_profiles_by_search(search):
        if not search: return []
        search = f'%{search.lower()}%'
        return  (
            db.session.query(UserProfile)
            .join(UserProfile.user)
            .options(joinedload(UserProfile.user))
            .filter(
                or_(
                    func.lower(UserProfile.username).ilike(search),
                    func.lower(UserProfile.code).ilike(search),
                    func.lower(User.name).ilike(search),
                    func.lower(User.surname).ilike(search)
                )
            )
            .all()
        )

    @staticmethod
    def assure_uuid_uniqueness(profile):
        while True:
            if db.session.query(UserProfile).get(profile.id) is not None:
                profile.id = str(uuid.uuid4())
            if db.session.query(UserProfile).filter_by(alt_id = profile.alt_id).first() is not None:
                profile.alt_id = str(uuid.uuid4())
            else:
                break
        return profile
