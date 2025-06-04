from flask import Blueprint


admin_ds_bp = Blueprint('admin', __name__, template_folder='templates')
professor_ds_bp = Blueprint('professor', __name__, template_folder='templates')


from .controllers import admin_dashboard
from .controllers import professor_dashboard
