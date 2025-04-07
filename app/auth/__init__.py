from flask import Blueprint

auth = Blueprint('auth', __name__)

from .controllers import AuthController
from .services import AuthService
from .forms import SignUpForm, SignInForm
