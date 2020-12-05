from flask import Blueprint
from src.models import db
from src.utils import success_response, failure_response

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