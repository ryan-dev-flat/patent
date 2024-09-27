from app import create_app  # Import your Flask app factory function
from models import db, Patent, Novelty, Utility, Obviousness

def calculate_and_populate_scores():
    # Fetch the first 20 patents
    patents = Patent.query.limit(20).all()

    for patent in patents:
        # Ensure novelty, utility, and obviousness instances exist
        if not patent.novelty:
            patent.novelty = Novelty(patent_id=patent.id)
        if not patent.utility:
            patent.utility = Utility(patent_id=patent.id)
        if not patent.obviousness:
            patent.obviousness = Obviousness(
                prior_art_scope="Some scope",
                differences="Some differences",
                skill_level="Some skill level",
                secondary_considerations="Some considerations",
                patent_id=patent.id
            )
        db.session.commit()

        # Perform the analysis
        novelty_score = patent.novelty.calculate_novelty_score()
        utility_score = patent.utility.calculate_utility_score()
        obviousness_score = patent.obviousness.calculate_obviousness_score()
        patentability_score = patent.calculate_patentability_score()

        # Save the scores to the database
        patent.novelty.novelty_score = novelty_score
        patent.utility.utility_score = utility_score
        patent.obviousness.obviousness_score = obviousness_score
        patent.patentability_score = patentability_score
        db.session.commit()

    print("Patentability scores and related scores have been calculated and populated successfully.")

if __name__ == "__main__":
    app = create_app()  # Create an instance of your Flask app
    with app.app_context():
        calculate_and_populate_scores()
