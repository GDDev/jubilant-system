from flask import Blueprint

profile = Blueprint('perfil', __name__, template_folder='templates')
user = Blueprint('usuario', __name__, template_folder='templates')

from .models import User, UserProfile
from .controllers import user_controller, user_profile_controller
from .services import UserService, UserProfileService
from .repositories import UserRepository, UserProfileRepository
