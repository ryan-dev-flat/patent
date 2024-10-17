from flask import Blueprint
from flask_restful import Api

from novelty_analysis_resource import NoveltyAnalysisResource
from obviousness_analysis_resource import ObviousnessAnalysisResource
from utility_analysis_resource import UtilityAnalysisResource
from add_user_to_patent_resource import AddUserToPatentResource
from patentability_analysis_resource import PatentabilityAnalysisResource
from remove_user_from_patent_resource import RemoveUserFromPatentResource
from dashboard_resource import DashboardResource

from resources import (
    AllUsersResource, 
    LoginResource, 
    LogoutResource,
    PatentResource,
    PriorArtResource,
    TokenRefreshResource,
    UserResource,
    UserByUsernameResource
)

main = Blueprint('main', __name__)
api = Api(main)

# User-related endpoints
api.add_resource(UserResource, '/register', endpoint='user_register')
api.add_resource(LoginResource, '/login', endpoint='user_login')
api.add_resource(LogoutResource, '/logout', endpoint='user_logout')
api.add_resource(UserResource, '/update_user', endpoint='user_update', methods=['PATCH', 'GET', 'OPTIONS'])
api.add_resource(UserResource, '/delete_account', endpoint='user_delete_account')
api.add_resource(UserByUsernameResource, '/users', endpoint='user_by_username')

# Patent-related endpoints
api.add_resource(PatentResource, '/patents', endpoint='patent_create', methods=['POST'])
api.add_resource(PatentResource, '/patents', endpoint='patent_list', methods=['GET'])
api.add_resource(PatentResource, '/patents/<int:patent_id>', methods=['GET', 'PATCH', 'DELETE'])

# User management on patents
api.add_resource(AddUserToPatentResource, '/patents/<int:patent_id>/add_user', endpoint='add_user_to_patent')
api.add_resource(RemoveUserFromPatentResource, '/patents/<int:patent_id>/remove_user', endpoint='remove_user_from_patent')

# Analysis endpoints
api.add_resource(PriorArtResource, '/patents/<int:patent_id>/prior_art', endpoint='prior_art')
api.add_resource(UtilityAnalysisResource, '/patents/<int:patent_id>/analysis/utility', endpoint='utility_analysis')
api.add_resource(NoveltyAnalysisResource, '/patents/<int:patent_id>/analysis/novelty', endpoint='novelty_analysis')
api.add_resource(ObviousnessAnalysisResource, '/patents/<int:patent_id>/analysis/obviousness', endpoint='obviousness_analysis')
api.add_resource(PatentabilityAnalysisResource, '/patents/<int:patent_id>/analysis/patentability_score', endpoint='patentability_score')

# Dashboard
api.add_resource(DashboardResource, '/dashboard', endpoint='dashboard')

# All users
api.add_resource(AllUsersResource, '/users/all')

# Token management
api.add_resource(TokenRefreshResource, '/refresh_token', endpoint='refresh_token')
