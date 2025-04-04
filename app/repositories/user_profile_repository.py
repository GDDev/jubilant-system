from app.models import UserProfile
from app.utils import db

class UserProfileRepository:
    
    def insert(profile: UserProfile) -> None:
        db.session.add(profile)
        db.session.commit()
