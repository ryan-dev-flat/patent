from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import db, User, Patent
import requests

main = Blueprint('main', __name__)

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@main.route('/patents', methods=['POST'])
@jwt_required()
def create_patent():
    data = request.get_json()
    user_id = get_jwt_identity()
    new_patent = Patent(title=data['title'], description=data['description'], user_id=user_id)
    db.session.add(new_patent)
    db.session.commit()
    return jsonify({'message': 'Patent created successfully'}), 201

@main.route('/patents', methods=['GET'])
@jwt_required()
def get_patents():
    user_id = get_jwt_identity()
    patents = Patent.query.filter_by(user_id=user_id).all()
    return jsonify([{'title': patent.title, 'description': patent.description} for patent in patents]), 200

@main.route('/patentability_analysis', methods=['POST'])
@jwt_required()
def patentability_analysis():
    data = request.get_json()
    invention_idea = data['idea']
    analysis = analyze_patentability(invention_idea)
    return jsonify({'analysis': analysis})

def analyze_patentability(idea):
    novelty = check_novelty(idea)
    non_obviousness = check_non_obviousness(idea)
    utility = check_utility(idea)
    prior_art = get_patent_prior_art()(idea)
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
    url = f'https://api.lexisnexis.com/v1/case-law?query={" ".join(keywords)}'
    headers = {
        'Authorization': 'Bearer your_lexisnexis_api_key'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

@main.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    data = request.get_json()
    user_message = data['message']
    response = get_chatgpt_response(user_message)
    patents = search_prior_art(user_message)
    return jsonify({'response': response, 'patents': patents})

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
