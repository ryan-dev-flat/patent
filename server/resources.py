from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
import os
import requests
from models import db, User, Patent, Novelty, Utility, Obviousness, PriorArt
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, set_refresh_cookies, unset_jwt_cookies
from utils import fetch_patent_grants
from flask_cors import cross_origin
from sqlalchemy.exc import IntegrityError
from datetime import timedelta


import spacy

# Initialize NLP model
nlp = spacy.load("en_core_web_sm")

# Helper functions
def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    return " ".join(keywords)

# Helper function to search for prior art using the extracted keywords
def search_prior_art(description):
    keywords = extract_keywords(description)
    return fetch_patent_grants(keywords)

# Resources
class UserResource(Resource):
    @cross_origin()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username cannot be blank!")
        parser.add_argument('password', required=True, help="Password cannot be blank!")
        args = parser.parse_args()

        # Check if the username already exists
        if User.query.filter_by(username=args['username']).first():
            return {'error': 'Username already exists'}, 400

        new_user = User(username=args['username'], password=args['password'])
        db.session.add(new_user)
        try:
            db.session.commit()
            # Generate access token
            access_token = create_access_token(identity=args['username'])
            return jsonify({"message": "User registered successfully", "access_token": access_token}), 201
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Username already exists'}, 400

    @jwt_required()
    @cross_origin()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user:
            return {'username': user.username}, 200
        return {'message': 'User not found'}, 404

    @jwt_required()
    @cross_origin()
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=False)
        parser.add_argument('password', required=False)
        args = parser.parse_args()

        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user:
            if args['username']:
                user.username = args['username']
            if args['password']:
                user.password = args['password']
            db.session.commit()
            return {'message': 'User updated successfully'}, 200
        return {'message': 'User not found'}, 404

    @jwt_required()
    @cross_origin()
    def delete(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}, 200
        return {'message': 'User not found'}, 404

    @cross_origin()
    def options(self):
        return '', 200
    
class AllUsersResource(Resource):
    @jwt_required()
    @cross_origin()
    def get(self):
        users = User.query.all()
        if users:
            usernames = [user.username for user in users]
            return {'usernames': usernames}, 200
        return {'message': 'No users found'}, 404



class LoginResource(Resource):
    @cross_origin()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username cannot be blank!")
        parser.add_argument('password', required=True, help="Password cannot be blank!")
        args = parser.parse_args()

        user = User.query.filter_by(username=args['username']).first()
        if user and user.password == args['password']:
            access_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=120))  # Short-lived access token
            refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(days=90))  # Long-lived refresh token
            response = jsonify(access_token=access_token, refresh_token=refresh_token)
            set_refresh_cookies(response, refresh_token)  # Set refresh token as cookie
            return response, 200
        return {'message': 'Invalid credentials'}, 401

    @cross_origin()
    def options(self):
        return '', 200

class TokenRefreshResource(Resource):
    @jwt_required(refresh=True)
    @cross_origin()
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user, expires_delta=timedelta(minutes=60))
        response = jsonify(access_token=new_access_token)
        return response, 200

    @cross_origin()
    def options(self):
        return '', 200


class LogoutResource(Resource):
    @jwt_required()
    @cross_origin()
    def post(self):
        response = jsonify({"msg": "Logout successful"})
        unset_jwt_cookies(response)
        return response, 200
    
    @cross_origin()
    def options(self):
        return '', 200


class PatentResource(Resource):
    
    @jwt_required()
    @cross_origin()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, help="Title cannot be blank!")
        parser.add_argument('description', required=True, help="Description cannot be blank!")
        parser.add_argument('users', type=list, location='json', required=False, default=[])
        args = parser.parse_args()

        user_id = get_jwt_identity()
        new_patent = Patent(
            title=args['title'],
            description=args['description'],
            status='Pending',
            user_id=user_id
        )
        db.session.add(new_patent)
        db.session.commit()

        # Add users to the patent
        added_users = []
        for username in args['users']:
            user = User.query.filter_by(username=username).first()
            if user:
                new_patent.users.append(user)
                added_users.append(user.username)  # Track successfully added users
            else:
                # You can log or handle this case if necessary
                print(f"User not found: {username}")
        
        db.session.commit()  # Commit the added users

        # Return the response, including patent ID and added users
        return {
            'message': 'Patent created successfully',
            'patent_id': new_patent.id,
            'created_by': User.query.get(user_id).username,  # Fetch the creator's username
            'users': added_users  # Users successfully added
        }, 201

    @jwt_required()
    @cross_origin()
    def get(self, patent_id=None):
        user_id = get_jwt_identity()
        
        if patent_id:
            patent = Patent.query.filter_by(id=patent_id, user_id=user_id).first()
            if patent:
                # Fetch the creator's username
                creator = User.query.get(patent.user_id)
                # Prepare the response
                return {
                    'id': patent.id,
                    'title': patent.title,
                    'description': patent.description,
                    'status': patent.status,
                    'created_by': creator.username if creator else 'Unknown',
                    'users': [user.username for user in patent.users]
                }, 200
            return {'message': 'Patent not found'}, 404
        else:
            patents = Patent.query.filter_by(user_id=user_id).all()
            return [{
                'id': patent.id,
                'title': patent.title,
                'description': patent.description,
                'status': patent.status,
                'created_by': User.query.get(patent.user_id).username if User.query.get(patent.user_id) else 'Unknown',
                'users': [user.username for user in patent.users]
            } for patent in patents], 200

    
    @jwt_required()
    @cross_origin()
    def patch(self, patent_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=False)
        parser.add_argument('description', required=False)
        args = parser.parse_args()

        user_id = get_jwt_identity()
        patent = Patent.query.filter_by(id=patent_id, user_id=user_id).first()
        if patent:
            if args['title']:
                patent.title = args['title']
            if args['description']:
                patent.description = args['description']
            db.session.commit()
            return {'message': 'Patent updated successfully'}, 200
        return {'message': 'Patent not found'}, 404

    @jwt_required()
    @cross_origin()
    def delete(self, patent_id):
        user_id = get_jwt_identity()
        patent = Patent.query.filter_by(id=patent_id, user_id=user_id).first()
        if patent:
            db.session.delete(patent)
            db.session.commit()
            return {'message': 'Patent deleted successfully'}, 200
        return {'message': 'Patent not found'}, 404

    @jwt_required()
    @cross_origin()
    def add_inventor(self, patent_id):
        user_id = get_jwt_identity()
        patent = Patent.query.filter_by(id=patent_id, user_id=user_id).first()
        if not patent:
            return jsonify({"error": "Patent not found"}), 404

        data = request.get_json()
        inventor_name = data.get('name')

        inventor = User.query.filter_by(username=inventor_name).first()
        if not inventor:
            return jsonify({"error": "Inventor not found"}), 404

        patent.user.append(inventor)
        db.session.commit()

        return jsonify({"message": "Inventor added successfully"}), 200

    @cross_origin()
    def options(self):
        return '', 200

class PatentabilityAnalysisResource(Resource):
    @jwt_required()
    @cross_origin()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('patent_id', required=True, help="Patent ID cannot be blank!")
        args = parser.parse_args()

        user_id = get_jwt_identity()
        patent = Patent.query.filter_by(id=args['patent_id'], user_id=user_id).first()
        if not patent:
            return {'message': 'Patent not found'}, 404

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

        # Calculate scores
        novelty_score = patent.novelty.calculate_novelty_score()
        utility_score = patent.utility.calculate_utility_score()
        obviousness_score = patent.obviousness.calculate_obviousness_score()
        patentability_score = (novelty_score * 0.4) + (utility_score * 0.3) + (obviousness_score * 0.3)
        patent.patentability_score = patentability_score

        db.session.commit()

        return jsonify({
            'novelty_score': novelty_score,
            'utility_score': utility_score,
            'obviousness_score': obviousness_score,
            'patentability_score': patentability_score
        }), 200

    @cross_origin()
    def options(self):
        return '', 200

    
class PriorArtResource(Resource):
    @jwt_required()
    def post(self, patent_id):
        current_user = get_jwt_identity()
        
        # Retrieve the patent belonging to the current user
        patent = Patent.query.filter_by(id=patent_id, user_id=current_user).first()
        
        if not patent:
            return {'message': 'Patent not found or does not belong to the user'}, 404
        
        # Extract keywords from the patent description using spaCy
        doc = nlp(patent.description)
        keywords = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha and len(token.text) > 2]
        
        # Use the most frequent keywords (adjust the number as needed)
        top_keywords = " ".join(sorted(set(keywords), key=keywords.count, reverse=True)[:10])
        
        # Fetch and store prior art using the extracted keywords
        prior_art_data = fetch_patent_grants(top_keywords)
        
        if not prior_art_data:
            return {'message': 'No prior art found for this patent'}, 404
        
        # Store the fetched prior art
        for data in prior_art_data:
            prior_art = PriorArt(
                patent_number=data['patent_number'],
                title=data['title'],
                abstract=data['abstract'],
                url=data['url'],
                patent_id=patent_id
            )
            db.session.add(prior_art)
        
        db.session.commit()
        
        # Retrieve the stored prior art
        stored_prior_art = PriorArt.query.filter_by(patent_id=patent_id).all()
        prior_art_list = [{'patent_number': art.patent_number, 'title': art.title, 'abstract': art.abstract, 'url': art.url} for art in stored_prior_art]
        
        return jsonify({
            'message': 'Prior art fetched and stored successfully',
            'keywords_used': top_keywords,
            'prior_art': prior_art_list
        })
    
    @jwt_required()
    def get(self, patent_id):
        current_user = get_jwt_identity()
        
        # Retrieve the patent belonging to the current user
        patent = Patent.query.filter_by(id=patent_id, user_id=current_user).first()
        
        if not patent:
            return {'message': 'Patent not found or does not belong to the user'}, 404
        
        # Retrieve the stored prior art
        prior_art = PriorArt.query.filter_by(patent_id=patent_id).all()
        
        if not prior_art:
            return {'message': 'No prior art found for this patent'}, 404
        
        prior_art_list = [{'patent_number': art.patent_number, 'title': art.title, 'abstract': art.abstract, 'url': art.url} for art in prior_art]
        
        return jsonify({'prior_art': prior_art_list})

    @cross_origin()
    def options(self):
        return '', 200


