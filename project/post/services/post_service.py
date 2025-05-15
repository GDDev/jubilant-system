from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from ..exceptions import PostException
from ..repositories import PostRepository
from ..models import Post


class PostService:

    def __init__(self):
        self.post_repo = PostRepository()

    def get_friends_posts(self, friends) -> list[Post] | None:
        posts = list()
        try:
            for friend in friends:
                posts.extend(self.post_repo.get_posts_by_user_id(friend.id))
        except SQLAlchemyError as e:
            raise PostException('Erro ao recuperar posts.') from e
        return posts

    def new_post(self, profile_id: str, title: str, content: str) -> None:
        try:
            self.post_repo.insert(Post(profile_id=profile_id, title=title, content=content))
        except SQLAlchemyError as e:
            raise PostException('Erro ao criar post.') from e
