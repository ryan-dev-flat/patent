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
    print("Connecting to database:", app.config['SQLALCHEMY_DATABASE_URI'])

    db.init_app(app)

    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api')

    

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


