from faker import Faker
from models import db, User, Patent, Utility, Novelty, Obviousness, PriorArt
from app import create_app
from utils import extract_keywords, fetch_patent_grants
import random

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
        print(f"Data committed successfully.")
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
            user_id=user.id,
            status=fake.random_element(['Pending', 'Granted', 'Rejected', 'Expired', 'Invalidated']),
            created_date=fake.date_time_this_decade(before_now=True, after_now=False)
        )
        
        # Assign patent to random users without duplicates
        num_users_for_patent = fake.random_int(min=1, max=3)
        assigned_users = set()
        while len(assigned_users) < num_users_for_patent:
            random_user = fake.random_element(users)
            if random_user not in assigned_users:
                assigned_users.add(random_user)
                patent.users.append(random_user)

        patents.append(patent)
        db.session.add(patent)

    try:
        db.session.commit()  # Commit patents first
        print(f"Data committed successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating patents: {e}")
    
    return patents


def create_utilities(patents):
    for patent in patents:
        utility = Utility(
            useful=random.choice([True, False]),
            operable=random.choice([True, False]),
            practical=random.choice([True, False]),
            patent_id=patent.id
        )
        utility.calculate_utility_score()
        db.session.add(utility)
    try:
        db.session.commit()
        print(f"Data committed successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating utilities: {e}")


def create_novelties(patents):
    for patent in patents:
        novelty = Novelty(
            new_invention=random.choice([True, False]),
            not_publicly_disclosed=random.choice([True, False]),
            not_described_in_printed_publication=random.choice([True, False]),
            not_in_public_use=random.choice([True, False]),
            not_on_sale=random.choice([True, False]),
            patent_id=patent.id
        )
        novelty.calculate_novelty_score()
        db.session.add(novelty)
    try:
        db.session.commit()
        print(f"Data committed successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating novelties: {e}")


def create_obviousnesses(patents):
    for patent in patents:
        obviousness = Obviousness(
            scope_of_prior_art=random.choice(["Very similar", "Somewhat similar", "Different field"]),
            differences_from_prior_art=random.choice(["Minor", "Moderate", "Significant"]),
            level_of_ordinary_skill=random.choice(["High", "Medium", "Low"]),
            secondary_considerations=random.choice([None, "Commercial success", "Long-felt need", "Failure of others"]),
            patent_id=patent.id
        )
        obviousness.calculate_obviousness_score()
        db.session.add(obviousness)
    try:
        db.session.commit()
        print(f"Data committed successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating obviousnesses: {e}")


def recalculate_patentability_scores(patents):
    for patent in patents:
        patentability_score = patent.calculate_patentability_score()
        print(f"Patent {patent.id} recalculated patentability score: {patentability_score}")
        db.session.add(patent)  # Re-save the patent with the new score
    try:
        db.session.commit()
        print(f"Data committed successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error recalculating patentability scores: {e}")


def seed_database():
    app = create_app()
    with app.app_context():
        #db.drop_all()
        #db.create_all()
        users = create_users()
        print("Users created successfully and committed.")
        patents = create_patents(users)
        print("Patents created successfully and committed.")
        create_utilities(patents)
        print("Utilities created successfully and committed.")
        create_novelties(patents)
        print("Novelties created successfully and committed.")
        create_obviousnesses(patents)
        print("Obviousnesses created successfully and committed.")
        recalculate_patentability_scores(patents)  # Recalculate after utilities, novelty, and obviousness are created
        print("Patentability scores recalculated successfully.")

if __name__ == '__main__':
    seed_database()
    print("Database seeded successfully.")