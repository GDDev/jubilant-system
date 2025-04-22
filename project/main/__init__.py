from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates')

from .controllers import main_controller