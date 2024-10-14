# seed.py
from faker import Faker
from .models import db, User, Patent, Utility, Novelty, Obviousness, PriorArt
from .app import create_app
from .utils import fetch_patent_grants

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
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error creating users: {e}")
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

        # Many-to-Many Relationship: Assign patent to 1-3 random users
        num_users_for_patent = fake.random_int(min=1, max=3)
        for _ in range(num_users_for_patent):
            patent.users.append(fake.random_element(users))

        patents.append(patent)
        db.session.add(patent)

        # Prior Art: Fetch and store prior art
        try:
            prior_art_data = fetch_patent_grants(patent.description)
            if prior_art_data:
                for data in prior_art_data:
                    prior_art = PriorArt(
                        patent_number=data['patent_number'],
                        title=data['title'],
                        abstract=data['abstract'],
                        url=data['url'],
                        patent_id=patent.id
                    )
                    db.session.add(prior_art)
        except Exception as e:
            print(f"Error fetching/storing prior art: {e}")

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error creating patents: {e}")
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
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error creating utilities: {e}")

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
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error creating novelties: {e}")

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
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error creating obviousnesses: {e}")

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
