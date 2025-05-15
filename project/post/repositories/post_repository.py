from core import db
from project.post import Post


class PostRepository:

    @staticmethod
    def get_posts_by_user_id(profile_id: str) -> list[Post] | None:
        return db.session.query(Post).filter_by(profile_id=profile_id).all()

    @staticmethod
    def insert(post):
        db.session.add(post)
        db.session.commit()
