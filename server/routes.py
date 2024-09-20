from flask import Flask
from flask_restful import Api
from resources import UserResource, LoginResource, PatentResource, PatentabilityAnalysisResource, ChatResource

app = Flask(__name__)
api = Api(app)

# Add resources to the API
api.add_resource(UserResource, '/register')
api.add_resource(LoginResource, '/login')
api.add_resource(PatentResource, '/patents', '/patents/<int:patent_id>')
api.add_resource(PatentabilityAnalysisResource, '/patentability_analysis')
api.add_resource(ChatResource, '/chat')

if __name__ == '__main__':
    app.run(debug=True)
