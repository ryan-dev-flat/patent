from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Utility, Patent

class UtilityAnalysisResource(Resource):
    def get(self, patent_id):
        utility = Utility.query.filter_by(patent_id=patent_id).first_or_404()
        return jsonify({
            'id': utility.id,
            'operability': utility.operability,
            'beneficial': utility.beneficial,
            'practical': utility.practical,
            'utility_score': utility.utility_score,
            'patent_id': utility.patent_id
        })

    def post(self, patent_id):
        data = request.get_json()
        utility = Utility(
            operability=data.get('operability'),
            beneficial=data.get('beneficial'),
            practical=data.get('practical'),
            patent_id=patent_id
        )
        utility_score = utility.calculate_utility_score()
        db.session.add(utility)
        db.session.commit()
        return jsonify({
            'message': 'Utility analysis added successfully',
            'utility_id': utility.id,
            'utility_score': utility_score
        })

    def patch(self, patent_id):
        utility = Utility.query.filter_by(patent_id=patent_id).first_or_404()
        data = request.get_json()
        if 'operability' in data:
            utility.operability = data['operability']
        if 'beneficial' in data:
            utility.beneficial = data['beneficial']
        if 'practical' in data:
            utility.practical = data['practical']
        utility_score = utility.calculate_utility_score()
        db.session.commit()
        return jsonify({
            'message': 'Utility analysis updated successfully',
            'utility_score': utility_score
        })

    def delete(self, patent_id):
        utility = Utility.query.filter_by(patent_id=patent_id).first_or_404()
        db.session.delete(utility)
        db.session.commit()
        return jsonify({'message': 'Utility analysis deleted successfully'})