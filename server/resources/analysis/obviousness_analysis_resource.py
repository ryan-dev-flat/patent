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

class ObviousnessAnalysisResource(Resource):
    def get(self, patent_id):
        obviousness = Obviousness.query.filter_by(patent_id=patent_id).first_or_404()
        return jsonify({
            'id': obviousness.id,
            'prior_art_scope': obviousness.prior_art_scope,
            'differences': obviousness.differences,
            'skill_level': obviousness.skill_level,
            'secondary_considerations': obviousness.secondary_considerations,
            'obviousness_score': obviousness.obviousness_score,
            'patent_id': obviousness.patent_id
        })

    def post(self, patent_id):
        data = request.get_json()
        obviousness = Obviousness(
            prior_art_scope=data.get('prior_art_scope'),
            differences=data.get('differences'),
            skill_level=data.get('skill_level'),
            secondary_considerations=data.get('secondary_considerations'),
            patent_id=patent_id
        )
        obviousness_score = obviousness.calculate_obviousness_score()
        db.session.add(obviousness)
        db.session.commit()
        return jsonify({
            'message': 'Obviousness analysis added successfully',
            'obviousness_id': obviousness.id,
            'obviousness_score': obviousness_score
        })

    def patch(self, patent_id):
        obviousness = Obviousness.query.filter_by(patent_id=patent_id).first_or_404()
        data = request.get_json()
        if 'prior_art_scope' in data:
            obviousness.prior_art_scope = data['prior_art_scope']
        if 'differences' in data:
            obviousness.differences = data['differences']
        if 'skill_level' in data:
            obviousness.skill_level = data['skill_level']
        if 'secondary_considerations' in data:
            obviousness.secondary_considerations = data['secondary_considerations']
        obviousness_score = obviousness.calculate_obviousness_score()
        db.session.commit()
        return jsonify({
            'message': 'Obviousness analysis updated successfully',
            'obviousness_score': obviousness_score
        })

    def delete(self, patent_id):
        obviousness = Obviousness.query.filter_by(patent_id=patent_id).first_or_404()
        db.session.delete(obviousness)
        db.session.commit()
        return jsonify({'message': 'Obviousness analysis deleted successfully'})
