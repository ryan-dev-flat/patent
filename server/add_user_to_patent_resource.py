from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from models import db
from models import User, Patent
import logging

class AddUserToPatentResource(Resource):
    @jwt_required()
    @cross_origin()
    def post(self, patent_id):
        current_user = get_jwt_identity()
        patent = Patent.query.filter_by(id=patent_id, user_id=current_user).first()
        
        if not patent:
            logging.warning(f"Patent not found or permission denied for user {current_user}")
            return {'message': 'Patent not found or you do not have permission'}, 404

        data = request.get_json()
        print('Received data:', request.get_json())
        username = data.get('username')
        
        if not username:
            logging.warning("Username not provided in request")
            return {'message': 'Username is required'}, 400

        user_to_add = User.query.filter_by(username=username).first()
        
        if not user_to_add:
            logging.warning(f"User not found: {username}")
            return {'message': 'User not found'}, 404

        if user_to_add in patent.users:
            logging.info(f"User {username} is already associated with patent {patent_id}")
            return {'message': 'User is already associated with this patent'}, 400

        patent.users.append(user_to_add)
        db.session.commit()

        logging.info(f"User {username} added to patent {patent_id}")
        return {'message': 'User added to patent successfully'}, 200
    
    @cross_origin()
    def options(self):
        return '', 200
    
