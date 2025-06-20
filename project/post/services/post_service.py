from sqlalchemy.exc import SQLAlchemyError

from ..exceptions import PostException
from ..repositories import PostRepository
from ..models import Post

from utils.validators import validate_post


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
            validate_post(title, content)
            self.post_repo.insert(Post(profile_id=profile_id, title=title, content=content))
        except (SQLAlchemyError, PostException, Exception) as e:
            raise e

    def find_by_id(self, post_id: int) -> Post | None:
        try:
            return self.post_repo.find_by_id(post_id)
        except SQLAlchemyError as e:
            raise PostException('Erro ao recuperar post.') from e

    def update_post(self, post: Post, title: str, content: str) -> None:
        try:
            validate_post(title, content)
            post.title = title
            post.content = content
            self.post_repo.update(post)
        except (SQLAlchemyError, PostException, Exception) as e:
            raise PostException('Erro ao atualizar post.') from e

    def delete(self, post):
        try:
            self.post_repo.delete(post)
        except SQLAlchemyError as e:
            raise PostException('Erro ao deletar post.') from e
