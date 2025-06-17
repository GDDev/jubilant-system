from flask import flash, render_template, request, jsonify, redirect, url_for
from flask_login import login_required

from .. import major_bp
from ..forms import NewMajorForm
from ..services import MajorService
from ..exceptions import MajorException


major_service = MajorService()


@major_bp.route('/listar', methods=['GET'])
@login_required
def list_all():
    """
    Renders the majors' list page.
    """
    return render_template('majors_list.html')


@major_bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
def add():
    """
    Either gets an existing major with matching content or adds a new one on a temp table for admin approval.
    Returns:
        If 'GET' request, renders the form page.
        If 'POST' request, redirects to the 'add_user_major' page.
    """
    form = NewMajorForm()
    form.area_tag.choices = [('', 'Selecionar')]+[(tag, tag) for tag in major_service.get_area_choices()]
    form.level.choices = [('', '-----Selecionar-----')]+[(level, level) for level in major_service.get_level_choices()]
    form.name.choices = [('', '-----Selecionar-----')]+[(name, name) for name in major_service.get_names_choices()]
    try:
        if form.validate_on_submit():
            form.process(request.form)
            uni = form.university.data
            acronym = form.uni_acronym.data.upper()
            level = form.level.data.capitalize()
            name = form.name.data.capitalize()
            shift = form.shift.data
            # Check if exists
            major = major_service.exists(uni, acronym, level, name, shift)
            if not major:
                raise MajorException(f'Formação não encontrada para o turno {shift}')
            return redirect(url_for('major.add_user_major', major_id=major.id))

    except MajorException as e:
        flash(str(e))
    return render_template('new_major.html', form=form)


@major_bp.route('/atualizar', methods=['POST'])
@login_required
def update():
    pass


@major_bp.route('/remover', methods=['POST'])
@login_required
def remove():
    pass

@major_bp.route('/api/universidades', methods=['GET'])
@login_required
def autocomplete_university():
    """
    Searches the database for universities that match the query.
    Returns:
        JSON with the found universities' info.
    """
    try:
        query = request.args.get('busca')
        majors = major_service.find_by_ilike_university(query)

        if majors:
            result = [
                {
                    'uni':major.university,
                    'acronym':major.uni_acronym,
                    'levels': [
                        {
                            'level': level,
                            'majors': [
                                {
                                    'name': major.name,
                                    'area_tag': major.area_tag,
                                    'major_shift': major.shift,
                                    'min_semesters': major.min_semesters,
                                    'max_semesters': major.max_semesters,
                                }
                                for major in major_service.get_majors_by_uni_and_level(
                                    major.university,
                                    major.uni_acronym,
                                    level
                                )
                            ]
                        }
                        for level in major_service.get_levels_by_uni(major.university, major.uni_acronym)
                    ]
                } for major in majors
            ]

            return jsonify(result)
    except MajorException as e:
        flash(str(e))
    return []
