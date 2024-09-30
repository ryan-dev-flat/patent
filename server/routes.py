from flask import Blueprint
from flask_restful import Api
from resources import UserResource, PatentResource, LoginResource, LogoutResource, PatentabilityAnalysisResource, PriorArtResource

main = Blueprint('main', __name__)
api = Api(main)

api.add_resource(UserResource, '/register', endpoint='user_register')
api.add_resource(LoginResource, '/login', endpoint='user_login')
api.add_resource(LogoutResource, '/logout', endpoint='user_logout')
api.add_resource(UserResource, '/delete_account', endpoint='user_delete_account')

api.add_resource(PatentResource, '/patents', endpoint='patent_create')
api.add_resource(PatentResource, '/patents/<int:patent_id>', endpoint='patent_update', methods=['PATCH'])
api.add_resource(PatentResource, '/patents/<int:patent_id>', endpoint='patent_delete', methods=['DELETE'])
api.add_resource(PatentResource, '/patents', endpoint='patent_list', methods=['GET'])
api.add_resource(PatentResource, '/patents/<int:patent_id>/inventors', endpoint='patent_add_inventor')

api.add_resource(PatentabilityAnalysisResource, '/patentability_analysis', endpoint='patentability_analysis')
api.add_resource(PriorArtResource, '/prior_art', endpoint='prior_art')

api.add_resource(UserResource, '/update_user', endpoint='user_update', methods=['PATCH'])
