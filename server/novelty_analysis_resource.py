from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Patent, Novelty 
from flask_cors import cross_origin


class NoveltyAnalysisResource(Resource):
    @jwt_required()
    @cross_origin()
    def post(self, patent_id):
        current_user = get_jwt_identity()
        
        # Retrieve the patent belonging to the current user
        patent = Patent.query.filter_by(id=patent_id, user_id=current_user).first()
        
        if not patent:
            return {'message': 'Patent not found or does not belong to the user'}, 404
        
        # Retrieve or create a Novelty instance for the patent
        novelty = Novelty.query.filter_by(patent_id=patent_id).first()
        if not novelty:
            novelty = Novelty(patent_id=patent_id)
            db.session.add(novelty)
            db.session.commit()
        
        # Update novelty attributes based on the request data
        data = request.get_json()
        novelty.patented = data.get('patented', novelty.patented)
        novelty.printed_pub = data.get('printed_pub', novelty.printed_pub)
        novelty.public_use = data.get('public_use', novelty.public_use)
        novelty.on_sale = data.get('on_sale', novelty.on_sale)
        novelty.publicly_available = data.get('publicly_available', novelty.publicly_available)
        novelty.patent_app = data.get('patent_app', novelty.patent_app)
        novelty.inventor_underoneyear = data.get('inventor_underoneyear', novelty.inventor_underoneyear)
        
        # Calculate the novelty score
        novelty_score = novelty.calculate_novelty_score()
        db.session.commit()
        
        return jsonify({'novelty_score': novelty_score})

    @cross_origin()
    def options(self):
        return '', 200
