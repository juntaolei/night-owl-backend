from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ, getenv, makedirs

__version__ = (1, 0, 0)

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        DEBUG=False,
        GCS_BUCKET=getenv("GCS_BUCKET", ""),
        GCS_CREDENTIALS=getenv("GCS_CREDENTIALS", ""),
        SECRET_KEY=getenv("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=getenv(
            "DATABASE_URL",
            f"sqlite:///{app.instance_path}/dev.db",
        ),
        SQLALCHEMY_ECHO=False,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        TESTING=False,
    )
    gcs_creds_filename = f"{app.instance_path}/creds.json"
    environ.update(GOOGLE_APPLICATION_CREDENTIALS=gcs_creds_filename)

    from night_owl import auth
    from night_owl import image
    from night_owl import party
    from night_owl import review

    app.register_blueprint(auth.auth)
    app.register_blueprint(party.party)
    app.register_blueprint(review.review)

    db.init_app(app)

    try:
        makedirs(app.instance_path)
        with open(gcs_creds_filename, "w") as f:
            f.write(app.config.get("GCS_CREDENTIALS"))
        with app.app_context():
            db.drop_all()
            db.create_all()
    except OSError:
        pass

    @app.errorhandler(401)
    def unauthorized(error):
        return {"success": False, "message": "Unauthorized request."}, 401

    @app.errorhandler(404)
    def not_found_response(error):
        return {
            "success": False,
            "message": "Requested resource not found."
        }, 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {"success": False, "message": "Internal server error."}, 500

    return app