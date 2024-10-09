from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse
import os
import requests
from server.models import db, User, Patent, Novelty, Utility, Obviousness, PriorArt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies, set_access_cookies
from utils import fetch_patent_grants
from flask_cors import cross_origin
from sqlalchemy.exc import IntegrityError

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

