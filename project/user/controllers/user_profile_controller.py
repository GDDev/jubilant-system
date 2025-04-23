from flask import render_template, abort, redirect, url_for, session
from flask_login import login_required, current_user

from project.user import profile
from ..services import UserService, UserProfileService

user_service = UserService()
user_profile_service = UserProfileService()


@profile.route('/<string:username>', methods=['GET', 'POST'])
@login_required
def detail_profile(username: str):
    if username == current_user.username:
        user = user_service.find_by_id(current_user.user_id)
        if not user:
            abort(404)

        session['profile_id'] = current_user.id
        session['user_id'] = user.id
        return render_template('profile/owner_view.html', profile=current_user, user=user)

    user_profile = user_profile_service.find_by_username(username)
    if not user_profile:
        abort(404)

    if user_profile.visibility == 'public':
        return render_template('profile/visitor_view.html', user=user_profile)

    return redirect(url_for('main.home'))

@profile.route('/update', methods=['POST'])
def update_profile():
    pass

# Maybe?
@profile.route('/find', methods=['POST'])
def find_profile():
    pass
