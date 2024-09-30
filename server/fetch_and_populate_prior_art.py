from app import create_app  # Import your Flask app factory function
from models import db, Patent, PriorArt
from utils import fetch_patent_grants

def fetch_and_populate_prior_art():
    # Fetch the first 20 patents
    patents = Patent.query.limit(20).all()

    for patent in patents:
        # Fetch prior art data using the API
        prior_art_data = fetch_patent_grants(patent.description)

        if prior_art_data:
            # Save the prior art data to the PriorArt table
            for art in prior_art_data:
                prior_art = PriorArt(
                    patent_number=art['patent_number'],
                    title=art['title'],
                    abstract=art['abstract'],
                    url=art['url'],
                    patent_id=patent.id
                )
                db.session.add(prior_art)
            db.session.commit()
        else:
            print(f"No patents found for keywords: {patent.description}")

    print("Prior art data has been fetched and populated successfully.")

if __name__ == "__main__":
    app = create_app()  # Create an instance of your Flask app
    with app.app_context():
        fetch_and_populate_prior_art()
