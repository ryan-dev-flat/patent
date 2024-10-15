from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models import User, Patent

class RemoveUserFromPatentResource(Resource):
    @jwt_required()
    def post(self, patent_id):
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Check if the patent exists and belongs to the current user
        patent = Patent.query.filter_by(id=patent_id, user_id=user_id).first()
        if not patent:
            return {'message': 'Patent not found or you do not have permission to modify it'}, 404

        # Find the user to remove by ID or username
        user_to_remove = None
        if 'user_id' in data:
            user_to_remove = User.query.filter_by(id=data['user_id']).first()
        elif 'username' in data:
            user_to_remove = User.query.filter_by(username=data['username']).first()

        if not user_to_remove:
            return {'message': 'User not found'}, 404

        # Remove the user from the patent
        if user_to_remove in patent.user:
            patent.user.remove(user_to_remove)
            db.session.commit()
            return {'message': 'User removed from patent successfully'}, 200
        else:
            return {'message': 'User not associated with this patent'}, 400
