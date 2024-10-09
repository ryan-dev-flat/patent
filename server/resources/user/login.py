from flask import request, jsonify
from flask_restful import Resource

from server.models import db, User, Patent, Novelty, Utility, Obviousness, PriorArt
from server.utils import fetch_patent_grants

from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies, set_access_cookies
from flask_cors import cross_origin
from sqlalchemy.exc import IntegrityError

import requests
import os
import spacy

class LoginResource(Resource):
    @cross_origin()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username cannot be blank!")
        parser.add_argument('password', required=True, help="Password cannot be blank!")
        args = parser.parse_args()

        user = User.query.filter_by(username=args['username']).first()
        if user and user.password == args['password']:
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

    @cross_origin()
    def options(self):
        return '', 200