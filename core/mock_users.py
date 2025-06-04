import uuid

from faker import Faker
from werkzeug.security import generate_password_hash
from core import db
from project.user import User, UserProfile

fake = Faker('pt_BR')
Faker.seed(0)

def mock_100_users(app):
    with app.app_context():
        used_emails = set()
        used_usernames = set()

        for _ in range(100):
            name = fake.first_name()
            surname = fake.last_name()

            # Clean up names for email/username
            name_ascii = ''.join(c for c in name.lower() if c.isalnum())
            surname_ascii = ''.join(c for c in surname.lower() if c.isalnum())

            # Ensure unique email
            base_email = f"{name_ascii}.{surname_ascii}@example.com"
            email = base_email
            i = 1
            while (
                email in used_emails or
                db.session.query(User).filter_by(email=email).first()
            ):
                email = f"{name_ascii}.{surname_ascii}{i}@example.com"
                i += 1
            used_emails.add(email)

            # Ensure unique username
            base_username = f"{name_ascii}_{surname_ascii}"
            username = base_username
            j = 1
            while (
                username in used_usernames or
                db.session.query(UserProfile).filter_by(username=username).first()
            ):
                username = f"{base_username}_{j}"
                j += 1
            used_usernames.add(username)

            user = User(name=name, surname=surname, email=email)
            db.session.add(user)
            db.session.flush()

            profile = UserProfile(
                id=str(uuid.uuid4()),
                alt_id=str(uuid.uuid4()),
                user_id=user.id,
                username=username,
                pwd=generate_password_hash("senha"),
                visibility="public",
                profile_pic="/static/img/user.png",
            )
            db.session.add(profile)

        db.session.commit()
        print("✅ Mocked 100 users and profiles with unique emails and usernames.")
