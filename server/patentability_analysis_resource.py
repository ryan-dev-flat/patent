from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models import Patent, Novelty, Obviousness, Utility

class PatentabilityAnalysisResource(Resource):
    @jwt_required()
    def get(self, patent_id):
        user_id = get_jwt_identity()
        patent = Patent.query.filter_by(id=patent_id, user_id=user_id).first()
        if not patent:
            return {'message': 'Patent not found'}, 404

        if not patent.novelty:
            return {'message': 'Novelty analysis not found'}, 404
        if not patent.utility:
            return {'message': 'Utility analysis not found'}, 404
        if not patent.obviousness:
            return {'message': 'Obviousness analysis not found'}, 404

        novelty_score = patent.novelty.calculate_novelty_score()
        utility_score = patent.utility.calculate_utility_score()
        obviousness_score = patent.obviousness.calculate_obviousness_score()
        patentability_score = (novelty_score * 0.4) + (utility_score * 0.3) + (obviousness_score * 0.3)
        patent.patentability_score = patentability_score

        db.session.commit()

        print({
            'novelty_score': novelty_score,
            'utility_score': utility_score,
            'obviousness_score': obviousness_score,
            'patentability_score': patentability_score
        })

        return jsonify({
            'novelty_score': novelty_score,
            'utility_score': utility_score,
            'obviousness_score': obviousness_score,
            'patentability_score': patentability_score
        })

