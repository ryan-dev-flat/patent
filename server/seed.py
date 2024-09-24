from faker import Faker
from models import db, User, Patent, Utility, Novelty, Obviousness
from app import create_app

fake = Faker()

def create_users(num_users=10):
    users = []
    for _ in range(num_users):
        user = User(
            username=fake.user_name(),
            password=fake.password(length=10)
        )
        users.append(user)
        db.session.add(user)
    db.session.commit()
    return users

def create_patents(users, num_patents=20):
    patents = []
    for _ in range(num_patents):
        user = fake.random_element(users)
        patent = Patent(
            title=fake.sentence(nb_words=6),
            description=fake.text(max_nb_chars=200),
            user_id=user.id
        )
        patents.append(patent)
        db.session.add(patent)
    db.session.commit()
    return patents

def create_utilities(patents):
    for patent in patents:
        utility = Utility(
            operability=fake.boolean(),
            beneficial=fake.boolean(),
            practical=fake.boolean(),
            patent_id=patent.id
        )
        db.session.add(utility)
    db.session.commit()

def create_novelties(patents):
    for patent in patents:
        novelty = Novelty(
            patented=fake.boolean(),
            printed_pub=fake.boolean(),
            public_use=fake.boolean(),
            on_sale=fake.boolean(),
            publicly_available=fake.boolean(),
            patent_app=fake.boolean(),
            inventor_underoneyear=fake.boolean(),
            patent_id=patent.id
        )
        db.session.add(novelty)
    db.session.commit()

def create_obviousnesses(patents):
    for patent in patents:
        obviousness = Obviousness(
            prior_art_scope=fake.sentence(nb_words=4),
            differences=fake.sentence(nb_words=4),
            skill_level=fake.sentence(nb_words=4),
            secondary_considerations=fake.sentence(nb_words=4),
            patent_id=patent.id
        )
        db.session.add(obviousness)
    db.session.commit()

def seed_database():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        users = create_users()
        patents = create_patents(users)
        create_utilities(patents)
        create_novelties(patents)
        create_obviousnesses(patents)

if __name__ == '__main__':
    seed_database()
