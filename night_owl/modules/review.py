from flask import Blueprint, request
from night_owl.models import db, Review

review = Blueprint("review", __name__, url_prefix="/api")


@review.route("/party/<int:party_id>/review/add", methods=["POST"])
def add_review(party_id):
    pass


@review.route("/party/<int:party_id>/review/<int:review_id>/delete",
              methods=["DELETE"])
def delete_review(party_id, review_id):
    pass


@review.route("/party/<int:party_id>/review/all", methods=["GET"])
def get_reviews(party_id):
    pass
