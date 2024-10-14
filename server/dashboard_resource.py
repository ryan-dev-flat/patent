from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db
from .models import User, Patent

class DashboardResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        # Count the number of patents for the current user
        patent_count = Patent.query.filter_by(user_id=user_id).count()
        
        # Count the number of users
        user_count = User.query.count()
        
        # Count patents by status
        pending_patents_count = Patent.query.filter_by(user_id=user_id, status='Pending').count()
        approved_patents_count = Patent.query.filter_by(user_id=user_id, status='Approved').count()
        rejected_patents_count = Patent.query.filter_by(user_id=user_id, status='Rejected').count()
        abandoned_patents_count = Patent.query.filter_by(user_id=user_id, status='Abandoned').count()
        expired_patents_count = Patent.query.filter_by(user_id=user_id, status='Expired').count()
        invalidated_patents_count = Patent.query.filter_by(user_id=user_id, status='Invalidated').count()

        return {
            'patent_count': patent_count,
            'user_count': user_count,
            'pending_patents_count': pending_patents_count,
            'approved_patents_count': approved_patents_count,
            'rejected_patents_count': rejected_patents_count,
            'abandoned_patents_count': abandoned_patents_count,
            'expired_patents_count': expired_patents_count,
            'invalidated_patents_count': invalidated_patents_count
        }, 200
