from wtforms import StringField, DateField
from app.auth import SignUpForm


# def validate_major_end(form, field):
    #     start = form.major_start.data
    #     end = field.data
    #     if end < start:
    #         raise ValidationError(
    #             'Data de conclusão do curso deve ser após a data de início.'
    #         )
    #     diff = trunc((end - start).days / 365.25)
    #     if not (2 < diff <= 10):
    #         raise ValidationError(
    #             'Duração de curso deve ser entre 2 e 10 anos.'
    #         )


class SignUpStudentForm(SignUpForm):
    # If student
    major = StringField('Curso:')
    major_start = DateField(
        'Data de início:'   
    )
    major_end = DateField(
        'Data de conclusão (ou prevista):'
    )

class SignUpProfessorForm(SignUpForm):
    # If professor
    degree = StringField('Nível da formação:')
    area = StringField('Área de formação:')


