from faker import Faker
from server.models import db, User, Patent
from server.app import create_app

app = create_app()
fake = Faker()

def seed_users(n):
    for _ in range(n):
        user = User(
            username=fake.user_name(),
            password=fake.password()
        )
        db.session.add(user)
    db.session.commit()

def seed_patents(n):
    users = User.query.all()
    for _ in range(n):
        patent = Patent(
            title=fake.catch_phrase(),
            description=fake.text(),
            user_id=fake.random_element(users).id
        )
        db.session.add(patent)
    db.session.commit()

with app.app_context():
    db.drop_all()
    db.create_all()
    seed_users(10)  # Seed 10 users
    seed_patents(50)  # Seed 50 patents
