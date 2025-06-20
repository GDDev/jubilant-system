from functools import wraps

from flask import abort, redirect, url_for
from flask_login import current_user


def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or getattr(current_user, 'role') not in ['admin', 'god']:
            abort(403)
        return func(*args, **kwargs)
    return decorated_function


def god_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or getattr(current_user, 'role') not in ['god']:
            abort(403)
        return func(*args, **kwargs)
    return decorated_function

def nutri_professor_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_professor:
            abort(403)
        if not current_user.teaches('Nutrição'):
            abort(403)
        return func(*args, **kwargs)
    return decorated_function


def pe_professor_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_professor:
            abort(403)
        if not current_user.teaches('Educação física'):
            abort(403)
        return func(*args, **kwargs)
    return decorated_function

