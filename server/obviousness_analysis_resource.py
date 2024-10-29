from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Obviousness, Patent

class ObviousnessAnalysisResource(Resource):

    @jwt_required()
    def get(self, patent_id):
        """
        Fetch obviousness analysis for the given patent_id.
        """
        # Retrieve the obviousness analysis for the patent
        obviousness = Obviousness.query.filter_by(patent_id=patent_id).first()
        if not obviousness:
            return {'message': 'Obviousness analysis not found'}, 404

        # Return the obviousness analysis data
        return jsonify({
            'id': obviousness.id,
            'scope_of_prior_art': obviousness.scope_of_prior_art,
            'differences_from_prior_art': obviousness.differences_from_prior_art,
            'level_of_ordinary_skill': obviousness.level_of_ordinary_skill,
            'secondary_considerations': obviousness.secondary_considerations,
            'obviousness_score': obviousness.obviousness_score,
            'patent_id': obviousness.patent_id
        })

    @jwt_required()
    def post(self, patent_id):
        """
        Create an obviousness analysis for the given patent_id.
        """
        # Check if the patent exists
        patent = Patent.query.filter_by(id=patent_id).first()
        if not patent:
            return {'message': 'Patent not found'}, 404

        # Parse the request data
        data = request.get_json()

        # Check if obviousness analysis already exists for the patent
        obviousness = Obviousness.query.filter_by(patent_id=patent_id).first()
        if obviousness:
            return {'message': 'Obviousness analysis already exists for this patent'}, 400

        # Create a new Obviousness analysis
        obviousness = Obviousness(
            scope_of_prior_art=data.get('scope_of_prior_art', 'Different field'),
            differences_from_prior_art=data.get('differences_from_prior_art', 'Significant'),
            level_of_ordinary_skill=data.get('level_of_ordinary_skill', 'Medium'),
            secondary_considerations=data.get('secondary_considerations', ''),
            patent_id=patent_id
        )

        # Calculate and set the obviousness score
        obviousness.calculate_obviousness_score()
        db.session.add(obviousness)
        db.session.commit()

        return jsonify({
            'message': 'Obviousness analysis created successfully',
            'obviousness_score': obviousness.obviousness_score,
            'obviousness_id': obviousness.id
        }), 201

    @jwt_required()
    def patch(self, patent_id):
        """
        Update an existing obviousness analysis for the given patent_id.
        """
        # Retrieve the existing obviousness analysis
        obviousness = Obviousness.query.filter_by(patent_id=patent_id).first()
        if not obviousness:
            return {'message': 'Obviousness analysis not found'}, 404

        # Parse the request data
        data = request.get_json()

        # Update obviousness analysis attributes based on request data
        if 'scope_of_prior_art' in data:
            obviousness.scope_of_prior_art = data['scope_of_prior_art']
        if 'differences_from_prior_art' in data:
            obviousness.differences_from_prior_art = data['differences_from_prior_art']
        if 'level_of_ordinary_skill' in data:
            obviousness.level_of_ordinary_skill = data['level_of_ordinary_skill']
        if 'secondary_considerations' in data:
            obviousness.secondary_considerations = data['secondary_considerations']

        # Recalculate the obviousness score after updating
        obviousness.calculate_obviousness_score()
        db.session.commit()

        return jsonify({
            'message': 'Obviousness analysis updated successfully',
            'obviousness_score': obviousness.obviousness_score
        })
