#routes.py
from flask import Blueprint
from flask_restful import Api
from resources import UserResource, LoginResource, PatentResource, PatentabilityAnalysisResource, ChatResource, PriorArtResource, Dashboard

main = Blueprint('main', __name__)
api = Api(main)

# Add resources to the API
api.add_resource(UserResource, '/register', '/user')
api.add_resource(LoginResource, '/login')
api.add_resource(PatentResource, '/patents', '/patents/<int:patent_id>')
api.add_resource(PatentabilityAnalysisResource, '/patentability_analysis')
api.add_resource(ChatResource, '/chat')
api.add_resource(PriorArtResource, '/patents/<int:patent_id>/prior-art')
api.add_resource(Dashboard, '/api/dashboard')
