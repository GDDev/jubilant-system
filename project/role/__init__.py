from flask import Blueprint

role = Blueprint('funcao', __name__, template_folder='templates')

from .models import Role, AdminRole, StudentRole, ProfessorRole

from .repositories import RoleRepository
