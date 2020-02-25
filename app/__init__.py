from flask import Flask
from config import Config


def create_app(app_config=Config):
    # Standard initialize
    app = Flask(__name__, static_folder='./public', template_folder='./static')
    app.config.from_object(app_config)

    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
