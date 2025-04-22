from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates')

from .controllers import auth_controller
from .services import AuthService
from .forms import SignUpForm, SignInForm
