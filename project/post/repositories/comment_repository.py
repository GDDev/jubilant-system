from utils import db
from ..models import Comment


class CommentRepository:

    @staticmethod
    def insert(comment):
        db.session.add(comment)
        db.session.commit()

    @staticmethod
    def update(comment):
        comment.last_updated_at = db.func.now()
        db.session.commit()

    @staticmethod
    def delete(comment):
        db.session.delete(comment)
        db.session.commit()

    @staticmethod
    def find_by_id(comment_id):
        return db.session.get(Comment, comment_id)

    @staticmethod
    def find_by_post_id(post_id):
        return db.session.query(Comment).filter_by(post_id=post_id).all()

    @staticmethod
    def find_by_profile_id(profile_id):
        return db.session.query(Comment).filter_by(profile_id=profile_id).all()
