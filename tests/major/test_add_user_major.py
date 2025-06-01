from core import db
from project.major import UserMajor


def test_add_user_major(client, user, admin):
    client.post('/auth/entrar', data={
        'user': user.username,
        'pwd': 'senha'
    }, follow_redirects=True)

    response = client.post('/formacao/adicionar', data={
        'university': 'Universidade',
        'uni_acronym': 'UNI',
        'level': 'Técnico',
        'name': 'Formação',
        'area_tag': 'NUTRI',
        'shift': 'MORNING',
        'min_semesters': '8',
        'max_semesters': '12'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert '/formacao/adicionar/institucional/' in response.request.path

    response = client.post(f'/formacao/adicionar/institucional/?major_id={1}&is_major_temp={True}', data={
        'college_code': '123',
        'institutional_email': '123@uni.com',
        'user_is': 'STUDENT',
        'start_date': '2024-01-20',
        'check_ongoing': 'off',
        'end_date': '2030-02-20',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert '/formacao/listar' in response.request.path

    major = db.session.query(UserMajor).filter_by(profile_id=user.id).first()

    assert major
    assert major.temp_major.name == 'Formação'
