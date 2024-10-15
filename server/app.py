#app.py
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.migrate = Migrate(app, db)
    app.jwt = JWTManager(app)
    CORS(app, resources={r"/*": {"origins": "http://172.19.87.107:3000"}}, supports_credentials=True)

    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api')

    # Handle OPTIONS requests
    @app.after_request
    def after_request(response):
        response.headers['Access-Control-Allow-Origin'] = 'http://172.19.87.107:3000'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,PATCH,POST,DELETE,OPTIONS'
        return response

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


