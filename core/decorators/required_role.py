from functools import wraps

from flask import abort, redirect, url_for
from flask_login import current_user

from project.user.models.user_profile import RoleEnum


def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or getattr(current_user, 'role') not in ['admin', 'god']:
            abort(403)
        return func(*args, **kwargs)
    return decorated_function
