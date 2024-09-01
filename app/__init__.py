from flask import Flask
from .extensions import db, migrate, cors
from .config import config
from .error_handlers import register_error_handlers


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Register blueprints
    from .routes.home_routes import home_bp
    from .routes.user_routes import user_bp

    app.register_blueprint(home_bp, url_prefix="/")
    app.register_blueprint(user_bp, url_prefix="/users")

    # Register error handlers
    register_error_handlers(app)

    return app
