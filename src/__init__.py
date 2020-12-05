from flask import Flask
from os import makedirs
from os.path import join
from src.configs import DevelopmentConfig, ProductionConfig
from src.models import db
from src.modules import auth, doc


def create_flask_app(is_development=False):
    app = Flask(__name__)

    if is_development:
        app.config.from_object(DevelopmentConfig())
        app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI=
            f"sqlite:///{join(app.instance_path, 'development.db')}")
    else:
        app.config.from_object(ProductionConfig())

    app.register_blueprint(auth)
    app.register_blueprint(doc)
    db.init_app(app)

    try:
        makedirs(app.instance_path)
        with app.app_context():
            db.create_all()
    except Exception:
        pass

    return app
