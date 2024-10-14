from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db
from .models import User, Patent

class AddUserToPatentResource(Resource):
    @jwt_required()
    def post(self, patent_id):
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Check if the patent exists and belongs to the current user
        patent = Patent.query.filter_by(id=patent_id, user_id=user_id).first()
        if not patent:
            return {'message': 'Patent not found or you do not have permission to modify it'}, 404

        # Find the user to add by ID or username
        user_to_add = None
        if 'user_id' in data:
            user_to_add = User.query.filter_by(id=data['user_id']).first()
        elif 'username' in data:
            user_to_add = User.query.filter_by(username=data['username']).first()

        if not user_to_add:
            return {'message': 'User not found'}, 404

        # Add the user to the patent
        if user_to_add not in patent.user:
            patent.user.append(user_to_add)
            db.session.commit()
            return {'message': 'User added to patent successfully'}, 200
        else:
            return {'message': 'User already associated with this patent'}, 400
