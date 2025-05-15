from flask import Blueprint

post_bp = Blueprint('post', __name__, template_folder='templates')
comment_bp = Blueprint('comment', __name__, template_folder='templates')

from .models import Post, Comment
from .controllers import post_controller, comment_controller
from .services import PostService, CommentService
from .repositories import PostRepository, CommentRepository
from .exceptions import PostException, CommentException
