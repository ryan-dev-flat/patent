from flask import Blueprint
from flask_restful import Api
from resources import UserResource, LoginResource, PatentResource, PatentabilityAnalysisResource, ChatResource

main = Blueprint('main', __name__)
api = Api(main)

# Add resources to the API
api.add_resource(UserResource, '/register')
api.add_resource(LoginResource, '/login')
api.add_resource(PatentResource, '/patents', '/patents/<int:patent_id>')
api.add_resource(PatentabilityAnalysisResource, '/patentability_analysis')
api.add_resource(ChatResource, '/chat')

