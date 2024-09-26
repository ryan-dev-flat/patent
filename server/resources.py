from flask_restful import Resource, reqparse
import os
import requests
from models import db, User, Patent, Novelty, Utility, Obviousness, PriorArt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils import fetch_patent_grants
from flask_cors import cross_origin

import spacy

# Initialize NLP model
nlp = spacy.load("en_core_web_sm")

# Helper functions
def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    return " ".join(keywords)

def search_prior_art(idea):
    keywords = extract_keywords(idea)
    return fetch_patent_grants(keywords)

# Resources
class UserResource(Resource):
    @cross_origin()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username cannot be blank!")
        parser.add_argument('password', required=True, help="Password cannot be blank!")
        args = parser.parse_args()

        new_user = User(username=args['username'], password=args['password'])
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201

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

class PatentResource(Resource):
    @jwt_required()
    @cross_origin()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, help="Title cannot be blank!")
        parser.add_argument('description', required=True, help="Description cannot be blank!")
        args = parser.parse_args()

        user_id = get_jwt_identity()
        new_patent = Patent(title=args['title'], description=args['description'], user_id=user_id)
        db.session.add(new_patent)
        db.session.commit()

        # Create and associate Novelty, Utility, and Obviousness instances
        novelty = Novelty(patent_id=new_patent.id)
        utility = Utility(patent_id=new_patent.id)
        obviousness = Obviousness(patent_id=new_patent.id)
        db.session.add(novelty)
        db.session.add(utility)
        db.session.add(obviousness)
        db.session.commit()

        # Populate the user_patent table
        user = User.query.get(user_id)
        user.patents.append(new_patent)
        db.session.commit()

        return {'message': 'Patent created successfully'}, 201

    @jwt_required()
    @cross_origin()
    def get(self, patent_id=None):
        user_id = get_jwt_identity()
        if patent_id:
            patent = Patent.query.filter_by(id=patent_id, user_id=user_id).first()
            if patent:
                return {'id': patent.id, 'title': patent.title, 'description': patent.description}, 200
            return {'message': 'Patent not found'}, 404
        else:
            patents = Patent.query.filter_by(user_id=user_id).all()
            return [{'id': patent.id, 'title': patent.title, 'description': patent.description} for patent in patents], 200

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

        # Perform the analysis
        prior_art_data = fetch_patent_grants(patent.description)
        novelty_score = patent.novelty.calculate_novelty_score()
        utility_score = patent.utility.calculate_utility_score()
        obviousness_score = patent.obviousness.calculate_obviousness_score()
        patentability_score = patent.calculate_patentability_score()

        # Save the scores to the database
        patent.novelty.novelty_score = novelty_score
        patent.utility.utility_score = utility_score
        patent.obviousness.obviousness_score = obviousness_score
        patent.patentability_score = patentability_score
        db.session.commit()

        # Save prior art data to the PriorArt table
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

        return {
            'novelty_score': novelty_score,
            'utility_score': utility_score,
            'obviousness_score': obviousness_score,
            'patentability_score': patentability_score,
            'prior_art': prior_art_data
        }

    @cross_origin()
    def options(self):
        return '', 200






def analyze_patentability(idea):
    prior_art_data = fetch_patent_grants(idea)
    novelty = check_novelty(prior_art_data)
    non_obviousness = check_non_obviousness(prior_art_data)
    utility = check_utility(prior_art_data)

    # Example values for required fields
    prior_art_scope = "Some scope"
    differences = "Some differences"
    skill_level = "Some skill level"
    secondary_considerations = "Some considerations"

    return {
        'novelty': novelty,
        'non_obviousness': non_obviousness,
        'utility': utility,
        'prior_art': prior_art_data,
        'prior_art_scope': prior_art_scope,
        'differences': differences,
        'skill_level': skill_level,
        'secondary_considerations': secondary_considerations
    }


def check_novelty(prior_art_data):
    if prior_art_data:
        return "The idea is not novel. Similar inventions exist."
    return "The idea is novel."

def check_non_obviousness(prior_art_data):
    if prior_art_data:
        return "The idea is obvious based on existing inventions."
    return "The idea is non-obvious."

def check_utility(prior_art_data):
    if any("useful" in art['abstract'].lower() for art in prior_art_data):
        return "The idea has utility."
    return "The idea lacks utility."

class PriorArtResource(Resource):
    @jwt_required()
    @cross_origin()
    def get(self, patent_id):
        user_id = get_jwt_identity()
        patent = Patent.query.filter_by(id=patent_id, user_id=user_id).first()
        if not patent:
            return {'message': 'Patent not found'}, 404

        prior_art_list = PriorArt.query.filter_by(patent_id=patent.id).all()
        if not prior_art_list:
            return {'message': 'No prior art found for this patent'}, 404

        prior_art_data = [
            {
                'patent_number': art.patent_number,
                'title': art.title,
                'abstract': art.abstract,
                'url': art.url
            }
            for art in prior_art_list
        ]

        return {'prior_art': prior_art_data}, 200

    @cross_origin()
    def options(self):
        return '', 200


class ChatResource(Resource):
    @jwt_required()
    @cross_origin()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('message', required=True, help="Message cannot be blank!")
        args = parser.parse_args()

        user_message = args['message']
        response = get_chatgpt_response(user_message)
        patents = fetch_patent_grants(user_message)
        return {'response': response, 'patents': patents}

    @cross_origin()
    def options(self):
        return '', 200

def get_chatgpt_response(message):
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': message}]
    }
    response = requests.post('https://chatgpt-api.shn.hk/v1/', headers=headers, json=payload)
    response_json = response.json()
    if 'choices' in response_json and len(response_json['choices']) > 0:
        return response_json['choices'][0]['message']['content']
    else:
        return f"Error: {response_json.get('error', 'Unable to retrieve response from ChatGPT API.')}"

