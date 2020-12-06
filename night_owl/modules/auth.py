from flask import Blueprint
from night_owl.models import db
from night_owl.utils import success_response, failure_response

auth = Blueprint("auth", __name__, url_prefix="/api")


@auth.route("/register", methods=["POST"])
def register():
    return success_response()


@auth.route("/login", methods=["POST"])
def login():
    return success_response({"token": "testing"})


@auth.route("/logout", methods=["POST"])
def logout():
    return success_response()