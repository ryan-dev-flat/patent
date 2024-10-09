from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from flask import jsonify

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        response = jsonify({"message": "Successfully logged out"})
        unset_jwt_cookies(response)
        return response, 200
