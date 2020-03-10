from flask import Flask, g
from flask_cors import CORS
from config import Config
from app.db import db
from flask_jwt_extended import JWTManager
from flask_restful import Api
from marshmallow import Schema, fields
from bson import ObjectId

cors = CORS()


def create_app(config_class=Config):

    app = Flask(__name__, static_folder='./public', template_folder='./static')
    app.config.from_object(Config)

    # Schema.TYPE_MAPPING[ObjectId] = fields.String

    # Extension stuff
    # Because we want JS, handles CORS.
    # CORS(app)
    cors.init_app(app)
    # JWT for auth.
    jwt = JWTManager(app)
    # REST API extension
    api = Api(app)

    import app.main.resources as resources
    from app.main import models

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return models.BlacklistToken.is_jti_blacklisted(jti)

    @app.teardown_appcontext
    def teardown_db(self):
        db = g.pop('db', None)

        if db is not None:
            print('closing db')
            db.client.close()

    api.add_resource(resources.Register, '/register')
    api.add_resource(resources.AllUsers, '/users')
    api.add_resource(resources.Login, '/login')
    api.add_resource(resources.Logout, '/logout')
    # api.add_resource(resources.UserLogoutAccess, '/logout/access')
    # api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
    api.add_resource(resources.TokenRefresh, '/token/refresh')
    api.add_resource(resources.TestResource, '/test')

    return app
