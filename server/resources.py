from flask_restful import Resource, reqparse
from models import db, User, Patent
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils import fetch_patent_grants, requests, os
from flask_jwt_extended import jwt_required, get_jwt_identity


# Updated import

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
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username cannot be blank!")
        parser.add_argument('password', required=True, help="Password cannot be blank!")
        args = parser.parse_args()

        new_user = User(username=args['username'], password=args['password'])
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201

class LoginResource(Resource):
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

class PatentResource(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, help="Title cannot be blank!")
        parser.add_argument('description', required=True, help="Description cannot be blank!")
        args = parser.parse_args()

        user_id = get_jwt_identity()
        new_patent = Patent(title=args['title'], description=args['description'], user_id=user_id)
        db.session.add(new_patent)
        db.session.commit()
        return {'message': 'Patent created successfully'}, 201

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        patents = Patent.query.filter_by(user_id=user_id).all()
        return [{'title': patent.title, 'description': patent.description} for patent in patents], 200

class PatentabilityAnalysisResource(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('idea', required=True, help="Idea cannot be blank!")
        args = parser.parse_args()

        analysis = analyze_patentability(args['idea'])
        return {'analysis': analysis}

def analyze_patentability(idea):
    prior_art_data = fetch_patent_grants(idea)
    novelty = check_novelty(prior_art_data)
    non_obviousness = check_non_obviousness(prior_art_data)
    utility = check_utility(prior_art_data)
    return {
        'novelty': novelty,
        'non_obviousness': non_obviousness,
        'utility': utility,
        'prior_art': prior_art_data
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

claude_api_key = os.getenv('CLAUDE_API_KEY')

def get_claude_response(message):
    headers = {
        'Authorization': f'Bearer {claude_api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'prompt': message,
        'model': 'claude-v1',
        'max_tokens': 150
    }
    response = requests.post('https://api.anthropic.com/v1/complete', headers=headers, json=payload)
    response_json = response.json()
    if 'completion' in response_json:
        return response_json['completion']
    else:
        return "Error: Unable to retrieve response from Claude AI API."

class ChatResource(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('message', required=True, help="Message cannot be blank!")
        args = parser.parse_args()

        user_message = args['message']
        response = get_claude_response(user_message)
        patents = fetch_patent_grants(user_message)
        return {'response': response, 'patents': patents}





