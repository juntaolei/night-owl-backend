from flask import Flask
from night_owl.configs import ProductionConfig
from night_owl.models import db
from night_owl.modules import auth


def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        app.config.from_object(ProductionConfig())
    else:
        app.config.from_object(config)

    app.register_blueprint(auth)
    db.init_app(app)

    try:
        with app.app_context():
            db.create_all()
    except Exception:
        pass

    return app
