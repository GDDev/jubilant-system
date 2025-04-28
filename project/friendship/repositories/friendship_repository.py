from core import db
from project.friendship import Friendship


class FriendshipRepository:
    @staticmethod
    def insert(friendship: Friendship) -> Friendship | None:
        db.session.add(friendship)
        db.session.commit()
        return friendship

    @staticmethod
    def find_by_sender_id_receiver_id(user_id, friend_id) -> Friendship | None:
        return (
            db.session.query(Friendship)
            .filter(Friendship.sender_id == user_id, Friendship.receiver_id == friend_id)
            .first()
        )

    @staticmethod
    def find_by_id(request_id):
        return db.session.get(Friendship, request_id)

    @staticmethod
    def accept_request(friendship):
        friendship.status = 'accepted'
        friendship.accepted_at = db.func.now()
        db.session.commit()

    @staticmethod
    def decline_request(friendship):
        if friendship.status == 'pending':
            db.session.delete(friendship)
            db.session.commit()

    @staticmethod
    def find_by_receiver_id(user_id):
        return db.session.query(Friendship).filter_by(receiver_id=user_id).all()

    @staticmethod
    def find_pending_by_receiver_id(user_id):
        return db.session.query(Friendship).filter_by(receiver_id=user_id, status='pending').all()
