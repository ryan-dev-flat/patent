from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Novelty, Patent

class NoveltyAnalysisResource(Resource):
    
    @jwt_required()
    def get(self, patent_id):
        """
        Fetch novelty analysis for the given patent_id.
        """
        # Retrieve the novelty analysis for the patent
        novelty = Novelty.query.filter_by(patent_id=patent_id).first()
        if not novelty:
            return {'message': 'Novelty analysis not found'}, 404
        
        # Return the novelty analysis data
        return jsonify({
            'id': novelty.id,
            'new_invention': novelty.new_invention,
            'not_publicly_disclosed': novelty.not_publicly_disclosed,
            'not_described_in_printed_publication': novelty.not_described_in_printed_publication,
            'not_in_public_use': novelty.not_in_public_use,
            'not_on_sale': novelty.not_on_sale,
            'novelty_score': novelty.novelty_score,
            'patent_id': novelty.patent_id
        })

    @jwt_required()
    def post(self, patent_id):
        """
        Create a novelty analysis for the given patent_id.
        """
        # Check if the patent exists
        patent = Patent.query.filter_by(id=patent_id).first()
        if not patent:
            return {'message': 'Patent not found'}, 404

        # Parse the request data
        data = request.get_json()

        # Check if novelty already exists for the patent
        novelty = Novelty.query.filter_by(patent_id=patent_id).first()
        if novelty:
            return {'message': 'Novelty analysis already exists for this patent'}, 400

        # Create a new Novelty analysis
        novelty = Novelty(
            new_invention=data.get('new_invention', True),
            not_publicly_disclosed=data.get('not_publicly_disclosed', True),
            not_described_in_printed_publication=data.get('not_described_in_printed_publication', True),
            not_in_public_use=data.get('not_in_public_use', True),
            not_on_sale=data.get('not_on_sale', True),
            patent_id=patent_id
        )
        
        # Calculate and set the novelty score
        novelty.calculate_novelty_score()
        db.session.add(novelty)
        db.session.commit()

        return jsonify({
            'message': 'Novelty analysis created successfully',
            'novelty_score': novelty.novelty_score,
            'novelty_id': novelty.id
        }), 201

    @jwt_required()
    def patch(self, patent_id):
        """
        Update an existing novelty analysis for the given patent_id.
        """
        # Retrieve the existing novelty analysis
        novelty = Novelty.query.filter_by(patent_id=patent_id).first()
        if not novelty:
            return {'message': 'Novelty analysis not found'}, 404

        # Parse the request data
        data = request.get_json()

        # Update novelty analysis attributes based on request data
        if 'new_invention' in data:
            novelty.new_invention = data['new_invention']
        if 'not_publicly_disclosed' in data:
            novelty.not_publicly_disclosed = data['not_publicly_disclosed']
        if 'not_described_in_printed_publication' in data:
            novelty.not_described_in_printed_publication = data['not_described_in_printed_publication']
        if 'not_in_public_use' in data:
            novelty.not_in_public_use = data['not_in_public_use']
        if 'not_on_sale' in data:
            novelty.not_on_sale = data['not_on_sale']

        # Recalculate the novelty score after updating
        novelty.calculate_novelty_score()
        db.session.commit()

        return jsonify({
            'message': 'Novelty analysis updated successfully',
            'novelty_score': novelty.novelty_score
        })
