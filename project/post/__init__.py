from flask import Blueprint

post_bp = Blueprint('post', __name__, template_folder='templates')

from .models import Post
from .controllers import post_controller
from .services import PostService
from .repositories import PostRepository
from .exceptions import PostException
