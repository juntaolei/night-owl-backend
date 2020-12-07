from flask import Blueprint, request
from night_owl.models import db, Party

party = Blueprint("party", __name__, url_prefix="/api")


@party.route("/party/all", methods=["GET"])
def get_all_parties():
    pass


@party.route("/party/<int:party_id>", methods=["GET"])
def get_a_party(id):
    pass


@party.route("/party/add", methods=["POST"])
def create_party():
    pass


@party.route("/party/<int:party_id>/delete", methods=["DELETE"])
def delete_party():
    pass
