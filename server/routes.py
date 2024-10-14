from .add_user_to_patent_resource import AddUserToPatentResource
from .dashboard_resource import DashboardResource
from flask import Blueprint
from flask_restful import Api
from .novelty_analysis_resource import NoveltyAnalysisResource
from .obviousness_analysis_resource import ObviousnessAnalysisResource
from .patentability_analysis_resource import PatentabilityAnalysisResource
from .remove_user_from_patent_resource import RemoveUserFromPatentResource
from .resources import (AllUsersResource, LoginResource, LogoutResource,
                       PatentabilityAnalysisResource, PatentResource,
                       PriorArtResource, TokenRefreshResource, UserResource)
from .utility_analysis_resource import UtilityAnalysisResource

main = Blueprint('main', __name__)
api = Api(main)

api.add_resource(UserResource, '/register', endpoint='user_register')
api.add_resource(LoginResource, '/login', endpoint='user_login')
api.add_resource(LogoutResource, '/logout', endpoint='user_logout')
api.add_resource(UserResource, '/update_user', endpoint='user_update', methods=['PATCH'])
api.add_resource(UserResource, '/delete_account', endpoint='user_delete_account')

api.add_resource(PatentResource, '/patents', endpoint='patent_create', methods=['POST'])
api.add_resource(PatentResource, '/patents/<int:patent_id>', methods=['GET', 'PATCH', 'DELETE'])
api.add_resource(PatentResource, '/patents', endpoint='patent_list', methods=['GET'])

api.add_resource(AddUserToPatentResource, '/patents/<int:patent_id>/add_user', endpoint='add_user_to_patent')
api.add_resource(RemoveUserFromPatentResource, '/patents/<int:patent_id>/remove_user', endpoint='remove_user_from_patent')

api.add_resource(PriorArtResource, '/patents/<int:patent_id>/prior_art', endpoint='prior_art')
api.add_resource(UtilityAnalysisResource, '/patents/<int:patent_id>/analysis/utility', endpoint='utility_analysis')
api.add_resource(NoveltyAnalysisResource, '/patents/<int:patent_id>/analysis/novelty', endpoint='novelty_analysis')
api.add_resource(ObviousnessAnalysisResource, '/patents/<int:patent_id>/analysis/obviousness', endpoint='obviousness_analysis')
api.add_resource(PatentabilityAnalysisResource, '/patents/<int:patent_id>/analysis/patentability_score', endpoint='patentability_score')

api.add_resource(DashboardResource, '/dashboard', endpoint='dashboard')
api.add_resource(AllUsersResource, '/users/all')
api.add_resource(TokenRefreshResource, '/refresh_token', endpoint='refresh_token')
