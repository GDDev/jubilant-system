from flask import Blueprint


professor_bp = Blueprint('professor', __name__, template_folder='templates')

from .controllers import professor_controller
