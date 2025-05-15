from flask import flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from .. import post_bp
from ..services import PostService
from ..exceptions import PostException


post_service = PostService()


@post_bp.route('/novo', methods=['GET', 'POST'])
def new():
    if request.method == 'GET':
        return render_template('new_post.html')
    try:
        post_service.new_post(current_user.id, request.form.get('title'), request.form.get('content'))
    except PostException as e:
        flash(str(e))
    return redirect(url_for('post.feed'))


@post_bp.route('/update', methods=['POST'])
def update_post():
    pass


@post_bp.route('/delete', methods=['POST'])
def delete_post():
    pass


@post_bp.route('/detail_post/<int:post_id>', methods=['GET'])
def detail_post(post_id: int):
    return redirect(url_for('post.feed'))


@post_bp.route('/feed', methods=['GET'])
@login_required
def feed():
    try:
        friends_posts = post_service.get_friends_posts(current_user.friends)
        posts = current_user.posts + friends_posts
        posts.sort(key=lambda post: post.created_at, reverse=True)

        return render_template('feed.html', all_posts=posts)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('main.home'))
