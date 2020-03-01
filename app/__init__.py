from flask import Flask, g
from flask_cors import CORS
from config import Config
from app.db import db
from flask_jwt_extended import JWTManager
from flask_restful import Api
from marshmallow import Schema, fields
from bson import ObjectId


def create_app(config_class=Config):

    app = Flask(__name__, static_folder='./public', template_folder='./static')
    app.config.from_object(Config)

    # Schema.TYPE_MAPPING[ObjectId] = fields.String

    # Extension stuff
    # Because we want JS, handles CORS.
    CORS(app)
    # JWT for auth.
    jwt = JWTManager(app)
    # REST API extension
    api = Api(app)

    @app.teardown_appcontext
    def teardown_db(self):
        db = g.pop('db', None)

        if db is not None:
            print('closing db')
            db.client.close()

    import app.main.resources as resources

    api.add_resource(resources.Register, '/register')
    api.add_resource(resources.AllUsers, '/users')
    api.add_resource(resources.UserLogin, '/login')
    api.add_resource(resources.TokenRefresh, '/token/refresh')
    api.add_resource(resources.TestResource, '/test')

    return app
