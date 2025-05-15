from flask import abort
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from ..models import Comment
from ..exceptions import CommentException
from ..repositories import CommentRepository


class CommentService:
    def __init__(self):
        self.comment_repo = CommentRepository()

    def add(self, comment_data: dict) -> None:
        try:
            self.comment_repo.insert(
                Comment(
                    profile_id=comment_data['profile_id'],
                    post_id=comment_data['post_id'],
                    comment=comment_data['comment']
                )
            )
        except SQLAlchemyError as e:
            raise CommentException('Falha ao comentar.') from e

    def update(self, comment_id: int, content: str) -> None:
        try:
            comment = self.comment_repo.find_by_id(comment_id)
            if not comment:
                raise CommentException('Comentário não encontrado.')
            if comment.profile_id != current_user.id:
                abort(403)
            comment.comment = content
            self.comment_repo.update(comment)
        except SQLAlchemyError as e:
            raise CommentException('Falha ao editar comentário.') from e

    def delete(self, comment_id: int) -> None:
        try:
            comment = self.comment_repo.find_by_id(comment_id)
            if comment:
                if comment.profile_id != current_user.id:
                    abort(403)
                self.comment_repo.delete(comment)
        except SQLAlchemyError as e:
            raise CommentException('Falha ao deletar comentário.') from e

    def find_by_id(self, comment_id: int) -> Comment | None:
        try:
            return self.comment_repo.find_by_id(comment_id)
        except SQLAlchemyError as e:
            raise CommentException('Falha ao buscar comentário.') from e
