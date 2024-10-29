from flask import request, jsonify
from flask_restful import Resource, reqparse
import os
import requests
from models import db, User, Patent, Novelty, Utility, Obviousness, PriorArt
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, set_refresh_cookies, unset_jwt_cookies
from utils import fetch_patent_grants, extract_keywords, generate_mock_patents
from flask_cors import cross_origin
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
import logging
import random


# Resources
class UserResource(Resource):
    @cross_origin()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username cannot be blank!")
        parser.add_argument('password', required=True, help="Password cannot be blank!")
        args = parser.parse_args()

        # Check if the username already exists
        existing_user = User.query.filter_by(username=args['username']).first()
        if existing_user:
            print(f"Username {args['username']} already exists.")
            return {'error': 'Username already exists'}, 400

        new_user = User(username=args['username'], password=args['password'])
        db.session.add(new_user)
        try:
            db.session.commit()
            # Generate access token
            access_token = create_access_token(identity=args['username'])
            print(f"User {args['username']} registered successfully.")
            return jsonify({"message": "User registered successfully", "access_token": access_token}), 201
        except IntegrityError as e:
            db.session.rollback()
            print(f"IntegrityError: {e}")
            return {'error': 'Username already exists'}, 400
        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error: {e}")
            return {'error': 'An unexpected error occurred'}, 500


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
    @cross_origin()
    def options(self):
        return '', 200
    
class UserByUsernameResource(Resource):
    @jwt_required()
    def get(self):
        username = request.args.get('username', '').strip()
        logging.info(f"Searching for username: {username}")
        if not username:
            return {'message': 'Username is required'}, 400

        user = User.query.filter_by(username=username).first()

        if not user:
            logging.info(f"User {username} not found in the database.")
            return {'message': 'User not found'}, 404

        return {'id': user.id, 'username': user.username}, 200



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
            response = jsonify(access_token=access_token)
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
        new_access_token = create_access_token(identity=current_user, expires_delta=timedelta(minutes=120))
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
    

# Utility functions for generating random values and calculating scores
def generate_random_utility(patent_id):
    utility = Utility(
        operable=random.choice([True, False]),
        useful=random.choice([True, False]),
        practical=random.choice([True, False]),
        patent_id=patent_id
    )
    utility.calculate_utility_score()
    db.session.add(utility)
    return utility

def generate_random_novelty(patent_id):
    novelty = Novelty(
        new_invention=random.choice([True, False]),
        not_publicly_disclosed=random.choice([True, False]),
        not_described_in_printed_publication=random.choice([True, False]),
        not_in_public_use=random.choice([True, False]),
        not_on_sale=random.choice([True, False]),
        patent_id=patent_id
    )
    novelty.calculate_novelty_score()
    db.session.add(novelty)
    return novelty

def generate_random_obviousness(patent_id):
    obviousness = Obviousness(
        scope_of_prior_art=random.choice(["Very similar", "Somewhat similar", "Different field"]),
        differences_from_prior_art=random.choice(["Minor", "Moderate", "Significant"]),
        level_of_ordinary_skill=random.choice(["High", "Medium", "Low"]),
        secondary_considerations=random.choice([None, "Some considerations"]),
        patent_id=patent_id
    )
    obviousness.calculate_obviousness_score()
    db.session.add(obviousness)
    return obviousness

def calculate_patentability_score(novelty_score, utility_score, obviousness_score):
    return (novelty_score * 0.4) + (utility_score * 0.3) + (obviousness_score * 0.3)

def handle_patent_creation_or_update(patent_id, force_update=False):
    # Remove old analysis data before creating new analysis
    old_utility = Utility.query.filter_by(patent_id=patent_id).first()
    old_novelty = Novelty.query.filter_by(patent_id=patent_id).first()
    old_obviousness = Obviousness.query.filter_by(patent_id=patent_id).first()
    
    # Delete old entries if they exist
    if old_utility:
        db.session.delete(old_utility)
    if old_novelty:
        db.session.delete(old_novelty)
    if old_obviousness:
        db.session.delete(old_obviousness)

    # Create new analysis objects
    utility = generate_random_utility(patent_id)
    novelty = generate_random_novelty(patent_id)
    obviousness = generate_random_obviousness(patent_id)

    # Calculate patentability score
    patentability_score = calculate_patentability_score(
        novelty.novelty_score, utility.utility_score, obviousness.obviousness_score
    )

    # Update the patent's patentability score
    patent = Patent.query.get(patent_id)
    patent.patentability_score = patentability_score
    db.session.commit()

    return {
        'novelty_score': novelty.novelty_score,
        'utility_score': utility.utility_score,
        'obviousness_score': obviousness.obviousness_score,
        'patentability_score': patentability_score
    }



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
                print(f"User not found: {username}")
        
        db.session.commit()  # Commit the added users

        # Generate random values and calculate scores for utility, novelty, obviousness, and patentability
        analysis_result = handle_patent_creation_or_update(new_patent.id)
        
        # Trigger prior art search
        keywords = extract_keywords(f"{new_patent.title} {new_patent.description}")
        prior_art_data = fetch_patent_grants(keywords)

        # Store the fetched prior art
        for data in prior_art_data:
            prior_art = PriorArt(
                patent_number=data['patent_number'],
                title=data['title'],
                abstract=data['abstract'],
                url=data['url'],
                patent_id=new_patent.id
            )
            db.session.add(prior_art)

        db.session.commit()

        # Return the response, including patent ID, added users, prior art, and analysis results
        return {
            'message': 'Patent created successfully',
            'patent_id': new_patent.id,
            'created_by': User.query.get(user_id).username,
            'users': added_users,
            'prior_art': prior_art_data,
            'analysis': analysis_result  # Include the calculated scores
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
        parser.add_argument('status', required=False)
        parser.add_argument('user_ids', type=list, location='json', required=False)
        args = parser.parse_args()

        user_id = get_jwt_identity()
        patent = Patent.query.filter_by(id=patent_id, user_id=user_id).first()
        print(f"Updating patent {patent_id}")
        
        if patent:
            # Track whether title or description changed
            force_update = False
            if args['title'] and args['title'] != patent.title:
                patent.title = args['title']
                force_update = True
            if args['description'] and args['description'] != patent.description:
                patent.description = args['description']
                force_update = True
            if args['status']:
                patent.status = args['status']
            if args['user_ids']:
                # Update users
                patent.users = User.query.filter(User.id.in_(args['user_ids'])).all()
            
            db.session.commit()
            print(f"Updated patent data: {patent.title}, {patent.description}, {patent.status}")


            # Trigger new prior art search
            keywords = extract_keywords(f"{patent.title} {patent.description}")
            prior_art_data = fetch_patent_grants(keywords)

            # Clear existing prior art and store new results
            PriorArt.query.filter_by(patent_id=patent_id).delete()
            for data in prior_art_data:
                prior_art = PriorArt(
                    patent_number=data['patent_number'],
                    title=data['title'],
                    abstract=data['abstract'],
                    url=data['url'],
                    patent_id=patent_id
                )
                db.session.add(prior_art)

            # Handle patent creation or update scores (only regenerate if necessary)
            analysis_result = handle_patent_creation_or_update(patent.id, force_update)
            print(f"Analysis result: {analysis_result}")

            db.session.commit()
            
            print(f"Returning updated patent with id {patent.id} and scores: {analysis_result}")

            return {
                'message': 'Patent updated successfully',
                'patent': {
                    'id': patent.id,
                    'title': patent.title,
                    'description': patent.description,
                    'status': patent.status,
                    'users': [{'id': user.id, 'username': user.username} for user in patent.users],
                    'prior_art': prior_art_data,
                    'analysis': analysis_result  # Include the calculated scores
                }
            }, 200
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
    @cross_origin()
    def post(self, patent_id):
        current_user = get_jwt_identity()

        # Retrieve the patent belonging to the current user
        patent = Patent.query.filter_by(id=patent_id, user_id=current_user).first()
        if not patent:
            return {'message': 'Patent not found or does not belong to the user'}, 404

        # Extract keywords from patent title and description
        keywords = extract_keywords(f"{patent.title} {patent.description}")

        # Fetch prior art data
        prior_art_data = fetch_patent_grants(keywords)

        if not prior_art_data:
    # Optionally generate mock patents here if needed
            prior_art_data = generate_mock_patents(3)
            return {'message': 'No prior art found, returning mock patents.', 'mock_patents': prior_art_data}, 200
        
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

        # Return the fetched and stored prior art
        stored_prior_art = PriorArt.query.filter_by(patent_id=patent_id).all()
        prior_art_list = [{'patent_number': art.patent_number, 'title': art.title, 'abstract': art.abstract, 'url': art.url} for art in stored_prior_art]

        return jsonify({
            'message': 'Prior art fetched and stored successfully',
            'keywords_used': keywords,
            'prior_art': prior_art_list
        })
    
    @jwt_required()
    @cross_origin()
    def get(self, patent_id):
        current_user = get_jwt_identity()
        
        # Retrieve the patent belonging to the current user
        patent = Patent.query.filter_by(id=patent_id, user_id=current_user).first()
        
        if not patent:
            return {'message': 'Patent not found or does not belong to the user'}, 404
        
        # Retrieve the stored prior art
        prior_art = PriorArt.query.filter_by(patent_id=patent_id).all()
        
        if not prior_art:
            return jsonify({'message': 'No prior art found for this patent'}), 200  # Changed to 200 OK
        
        prior_art_list = [
            {
                'patent_number': art.patent_number,
                'title': art.title,
                'abstract': art.abstract,
                'url': art.url
            }
            for art in prior_art
        ]
        
        return jsonify({'prior_art': prior_art_list}), 200  # Added status code for clarity

    @cross_origin()
    def options(self):
        return '', 200