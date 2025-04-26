from flask import render_template, abort, redirect, url_for, session, request, flash
from flask_login import login_required, current_user

from project.user import profile
from ..services import UserService, UserProfileService

user_service = UserService()
user_profile_service = UserProfileService()


@profile.route('/<string:code>', methods=['GET', 'POST'])
@login_required
def detail_profile(code: str):
    try:
        if code == current_user.code:
            # session['profile_id'] = current_user.id
            # session['user_id'] = user.id
            return render_template('profile/owner_view.html', profile=current_user)

        user_profile = user_profile_service.find_by_code(code)
        return render_template('profile/visitor_view.html', profile=user_profile)

    except Exception as e:
        flash(str(e))
    return redirect(url_for('main.home'))

@profile.route('/update', methods=['POST'])
def update_profile():
    pass

@profile.route('/encontrar', methods=['GET', 'POST'])
def find():
    search = request.form.get('search')
    profiles = []
    try:
        profiles = user_profile_service.find_profiles_by_search(search)
    except Exception as e:
        flash(str(e))
    return render_template('profile_list.html', profiles=profiles, search=search)
