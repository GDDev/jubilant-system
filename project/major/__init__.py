from flask import Blueprint


major_bp = Blueprint('major', __name__, template_folder='templates')


from .models import Major, TempMajor, MajorEnum, AreaTags, Shift, UserMajor
from .controllers import major_controller, user_major_controller
from .services import MajorService, UserMajorService

from .exceptions import MajorException
