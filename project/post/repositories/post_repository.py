from utils import db
from project.post import Post


class PostRepository:

    @staticmethod
    def get_posts_by_user_id(profile_id: str) -> list[Post] | None:
        return db.session.query(Post).filter_by(profile_id=profile_id).all()

    @staticmethod
    def insert(post):
        db.session.add(post)
        db.session.commit()

    @staticmethod
    def find_by_id(post_id) -> Post | None:
        return db.session.get(Post, post_id)

    @staticmethod
    def update(post) -> None:
        post.last_updated_at = db.func.now()
        db.session.commit()

    @staticmethod
    def delete(post) -> None:
        db.session.delete(post)
        db.session.commit()
