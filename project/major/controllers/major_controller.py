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
    # try:
    #     pass
    # except MajorException as e:
    #     flash(str(e))
    return render_template('majors_list.html')


@major_bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
def add():
    form = NewMajorForm()
    try:
        if form.validate_on_submit():
            uni = form.university.data
            acronym = form.uni_acronym.data.upper()
            level = form.level.data.capitalize()
            name = form.name.data.capitalize()
            tag = form.area_tag.data
            shift = form.shift.data
            min = form.min_semesters.data
            max = form.max_semesters.data
            # Check if exists
            major = major_service.exists(uni, acronym, level, name, shift)
            if not major:
                # Check if doesn't exist but was suggested
                major = major_service.exists_as_temp(uni, acronym, level, name, shift)
                if major:
                    major_service.update(major, area_tag=tag, min_semesters=min, max_semesters=max)
                else:
                    # Creates new
                    major = major_service.add_temp(university=uni, uni_acronym=acronym, level=level, name=name, area_tag=tag, shift=shift, min_semesters=min, max_semesters=max)

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
def autocomplete_university():
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
