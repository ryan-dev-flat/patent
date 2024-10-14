from .app import create_app  # Import your Flask app factory function
from .models import db, User, Patent

def populate_user_patent():
    # Assuming you have the first 10 users and 20 patents already in the database
    users = User.query.limit(10).all()
    patents = Patent.query.limit(20).all()

    # Assign patents to users
    for i, patent in enumerate(patents):
        user = users[i % len(users)]  # Distribute patents among the first 10 users
        user.patents.append(patent)

    db.session.commit()
    print("User-patent relationships have been populated successfully.")

if __name__ == "__main__":
    app = create_app()  # Create an instance of your Flask app
    with app.app_context():
        populate_user_patent()
