from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import HTTPException

from utils import admin_required
from .. import admin_bp
from ..forms import NewNameForm, NewUsernameForm, NewEmailForm
from ..services import AdminService


admin_service = AdminService()


@admin_bp.route('/', methods=['GET'])
@login_required
@admin_required
def panel():
    overall = admin_service.get_overall_stats()
    return render_template('panel.html', overall=overall)


@admin_bp.route('/usuario', methods=['GET'])
@login_required
@admin_required
def control_user():
    p_id = request.args.get('p_id')
    try:
        profile = admin_service.test_method_executable(p_id)
        return render_template('control_user.html', profile=profile)
    except (HTTPException, Exception) as e:
        flash(str(e))
        return redirect(url_for('admin.panel'))


@admin_bp.route('/alterar_nome', methods=['GET', 'POST'])
@login_required
@admin_required
def change_name():
    # Get the ID
    p_id = request.args.get('p_id')
    form = NewNameForm()
    try:
        profile = admin_service.test_method_executable(p_id)
        if form.validate_on_submit():
            admin_service.change_name(profile, name=form.name.data, username=form.surname.data)
            return redirect(url_for('admin.control_user', p_id=profile.id))
        # Render the form
        return render_template('user_opts/name.html', form=form, profile=profile)
    except (HTTPException, Exception) as e:
        if hasattr(e, 'message'):
            flash(e.message)
        else:
            flash('Ocorreu um erro desconhecido.')
    return redirect(url_for('admin.control_user', p_id=p_id))


@admin_bp.route('/novo_codigo', methods=['GET'])
@login_required
@admin_required
def new_code():
    p_id = request.args.get('p_id')
    try:
        profile = admin_service.test_method_executable(p_id)
        admin_service.new_code(profile)
    except (HTTPException, Exception) as e:
        if hasattr(e, 'message'):
            flash(e.message)
        else:
            flash('Ocorreu um erro desconhecido.')
    return redirect(url_for('admin.control_user', p_id=p_id))


@admin_bp.route('/alterar_usuario', methods=['GET', 'POST'])
@login_required
@admin_required
def change_username():
    p_id = request.args.get('p_id')
    form = NewUsernameForm()
    try:
        profile = admin_service.test_method_executable(p_id)
        if form.validate_on_submit():
            admin_service.change_username(profile, username=form.username.data)
            return redirect(url_for('admin.control_user', p_id=profile.id))
        return render_template('user_opts/username.html', form=form, profile=profile)
    except (HTTPException, Exception) as e:
        if hasattr(e, 'message'):
            flash(e.message)
        else:
            flash('Ocorreu um erro desconhecido.')
    return redirect(url_for('admin.control_user', p_id=p_id))


@admin_bp.route('/alterar_email', methods=['GET', 'POST'])
@login_required
@admin_required
def change_email():
    p_id = request.args.get('p_id')
    form = NewEmailForm()
    try:
        profile = admin_service.test_method_executable(p_id)
        if form.validate_on_submit():
            admin_service.change_email(profile, email=form.email.data)
            return redirect(url_for('admin.control_user', p_id=profile.id))
        return render_template('user_opts/email.html', form=form, profile=profile)
    except (HTTPException, Exception) as e:
        if hasattr(e, 'message'):
            flash(e.message)
        else:
            flash('Ocorreu um erro desconhecido.')
    return redirect(url_for('admin.control_user', p_id=p_id))


@admin_bp.route('/nova_senha', methods=['GET'])
@login_required
@admin_required
def new_password():
    p_id = request.args.get('p_id')
    try:
        profile = admin_service.test_method_executable(p_id)
        admin_service.new_password(profile)
        flash(f'Nova senha enviada por email para o usuário {profile.username}')
    except (HTTPException, Exception) as e:
        if hasattr(e, 'message'):
            flash(e.message)
        else:
            flash('Ocorreu um erro desconhecido.')
    return redirect(url_for('admin.control_user', p_id=p_id))


@admin_bp.route('/promover_usuario', methods=['GET'])
@login_required
@admin_required
def promote_or_demote():
    p_id = request.args.get('p_id')
    try:
        profile = admin_service.test_method_executable(p_id)
        admin_service.promote_or_demote(profile)
    except (HTTPException, Exception) as e:
        if hasattr(e, 'message'):
            flash(e.message)
        else:
            flash('Ocorreu um erro desconhecido.')
    return redirect(url_for('admin.control_user', p_id=p_id))


@admin_bp.route('/deletar', methods=['GET'])
@login_required
@admin_required
def delete():
    p_id = request.args.get('p_id')
    try:
        profile = admin_service.test_method_executable(p_id)
        if current_user.role == 'god':
            admin_service.delete(profile)
            flash('Usuário deletado com sucesso.')
    except (HTTPException, Exception) as e:
        if hasattr(e, 'message'):
            flash(e.message)
        else:
            flash('Ocorreu um erro desconhecido.')
    return redirect(url_for('admin.panel'))
