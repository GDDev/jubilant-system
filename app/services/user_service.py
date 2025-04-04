from app.models import User, UserProfile
from app.repositories import ur, pr

class UserService:

    def create_user(name: str, surname: str, email: str, username: str, pwd: str, pwd2: str, accept_terms: bool) -> User | None:
        if accept_terms:
            if not ur.find_by_email(email):
                if pwd == pwd2:
                    user = User(name=name, surname=surname, email=email)
                    hashed_pwd = pwd #TODO: actually hash it
                    
                    try:
                        user = ur.insert(user)
                    except:
                        return None
                    try:
                        profile = UserProfile(
                            user_id=user.id,
                            username=username,
                            pwd=hashed_pwd
                        )

                        pr.insert(profile)
                    except:
                        ur.delete(user)
                    return profile
        return None
