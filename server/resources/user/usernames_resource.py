from flask_restful import Resource
from models import User  # Assuming you have a User model

class UsernamesResource(Resource):
    def get(self):
        try:
            users = User.query.with_entities(User.username).all()
            usernames = [user.username for user in users]
            return {'usernames': usernames}, 200
        except Exception as e:
            return {'message': str(e)}, 500
