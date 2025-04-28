from flask import Blueprint

friendship = Blueprint('amigo', __name__, template_folder='templates')

from .models import Friendship
from .controllers import friendship_controller
from .services import FriendshipService
from .repositories import FriendshipRepository
from .exceptions import FriendshipException
