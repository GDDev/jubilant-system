from flask import flash, request, abort, redirect, url_for
from flask_login import login_required, current_user

from .. import comment_bp
from ..exceptions import CommentException
from ..services import PostService, CommentService


post_service = PostService()
comment_service = CommentService()


@comment_bp.route('/novo/<int:post_id>', methods=['POST'])
@login_required
def new(post_id):
    try:
        post = post_service.find_by_id(post_id)
        if not post:
            raise CommentException('Impossível comentar em postagem inexistente.')

        comment_service.add({
            'profile_id': current_user.id,
            'post_id': post.id,
            'comment': request.form.get('content')
        })
    except CommentException as e:
        flash(str(e))
    return redirect(url_for('post.detail_post', post_id=post_id))


@comment_bp.route('/editar/<int:post_id>/<int:comment_id>', methods=['POST'])
@login_required
def update(post_id, comment_id):
    try:
        comment_service.update(comment_id, request.form.get('content'))
    except CommentException as e:
        flash(str(e))
    return redirect(url_for('post.detail_post', post_id=post_id))


@comment_bp.route('/deletar/<int:post_id>/<int:comment_id>', methods=['GET'])
@login_required
def delete(post_id, comment_id):
    try:
        comment_service.delete(comment_id)
    except CommentException as e:
        flash(str(e))
    return redirect(url_for('post.detail_post', post_id=post_id))
