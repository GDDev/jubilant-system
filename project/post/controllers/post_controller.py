from http.client import HTTPException

from flask import flash, render_template, request, redirect, url_for, abort
from flask_login import current_user, login_required

from .. import post_bp
from ..services import PostService
from ..exceptions import PostException


post_service = PostService()


@post_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'GET':
        return render_template('new_post.html')
    try:
        post_service.new_post(current_user.id, request.form.get('title'), request.form.get('content'))
        return redirect(url_for('post.feed'))
    except PostException as e:
        flash(e.message)
    except (HTTPException, Exception) as _:
        flash('Erro ao criar o post.')
    return redirect(url_for('post.new'))


@post_bp.route('/editar/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update(post_id: int):
    try:
        post = post_service.find_by_id(post_id)
        if not post:
            raise PostException('Postagem não encontrada.')

        if post.profile_id != current_user.id:
            abort(403)

        if request.method == 'GET':
            return render_template('edit_post.html', post=post)

        post_service.update_post(post, request.form.get('title'), request.form.get('content'))
        return redirect(url_for('post.detail_post', post_id=post_id))
    except PostException as e:
        flash(e.message)
    except (HTTPException, Exception) as _:
        flash('Erro ao atualizar o post.')
    return redirect(url_for('post.feed'))


@post_bp.route('/deletar/<int:post_id>', methods=['GET'])
@login_required
def delete(post_id: int):
    try:
        post = post_service.find_by_id(post_id)
        if post:
            if post.profile_id != current_user.id:
                abort(403)
            post_service.delete(post)
    except PostException as e:
        flash(str(e))
    return redirect(url_for('post.feed'))


@post_bp.route('/<int:post_id>', methods=['GET'])
@login_required
def detail_post(post_id: int):
    try:
        post = post_service.find_by_id(post_id)
        if post:
            return render_template('detail_post.html', post=post)
    except PostException as e:
        flash(str(e))
    return redirect(url_for('post.feed'))


@post_bp.route('/feed', methods=['GET'])
@login_required
def feed():
    try:
        friends_posts = post_service.get_friends_posts(current_user.friends)
        posts = current_user.posts + friends_posts
        posts.sort(key=lambda post: post.created_at, reverse=True)

        return render_template('feed.html', all_posts=posts)
    except PostException as e:
        flash(str(e))
        return redirect(url_for('main.home'))
