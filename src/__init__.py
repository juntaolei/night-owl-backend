from flask import Flask
from src.configs import DevelopmentConfig, ProductionConfig
from src.models import db
from src.modules import auth, doc


def create_flask_app(is_development=False):
    app = Flask(__name__)

    if is_development:
        app.config.from_object(DevelopmentConfig())
    else:
        app.config.from_object(ProductionConfig())

    app.register_blueprint(auth)
    app.register_blueprint(doc)
    db.init_app(app)

    try:
        with app.app_context():
            db.create_all()
    except Exception:
        pass

    return app
