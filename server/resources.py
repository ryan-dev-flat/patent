from flask_restful import Resource, reqparse
from models import db, User, Patent
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import requests

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
    novelty = check_novelty(idea)
    non_obviousness = check_non_obviousness(idea)
    utility = check_utility(idea)
    prior_art = get_patent_prior_art(idea)
    return {
        'novelty': novelty,
        'non_obviousness': non_obviousness,
        'utility': utility,
        'prior_art': prior_art
    }

def check_novelty(idea):
    prior_art = search_prior_art(idea)
    if prior_art:
        return "The idea is not novel. Similar inventions exist."
    return "The idea is novel."

def check_non_obviousness(idea):
    prior_art = search_prior_art(idea)
    if prior_art:
        return "The idea is obvious based on existing inventions."
    return "The idea is non-obvious."

def check_utility(idea):
    if "useful" in idea.lower():
        return "The idea has utility."
    return "The idea lacks utility."

def search_prior_art(idea):
    url = f'https://developer.uspto.gov/ibd-api/v1/patent/application?searchText={idea}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

def get_patent_prior_art(idea):
    keywords = extract_keywords(idea)
    prior_art = search_case_law(keywords)
    return prior_art

def extract_keywords(idea):
    return idea.split()

def search_case_law(keywords):
    url = f'https://api.harvard.edu/federal-patent-caselaw?query={" ".join(keywords)}'
    headers = {
        'Authorization': 'Bearer your_harvard_api_key'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

class ChatResource(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('message', required=True, help="Message cannot be blank!")
        args = parser.parse_args()

        user_message = args['message']
        response = get_chatgpt_response(user_message)
        patents = search_prior_art(user_message)
        return {'response': response, 'patents': patents}

def get_chatgpt_response(message):
    api_key = 'your_openai_api_key'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': message}]
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']
