from .auth import session_token_validation
from flask import Blueprint, request
from marshmallow import Schema, fields, validate, ValidationError
from night_owl.models import db, Party, Review
from night_owl.utils import success_response, failure_response

review = Blueprint("review", __name__, url_prefix="/api")


class ReviewSchema(Schema):
    rating = fields.Float()
    comment = fields.Str(validate=validate.Length(min=1, max=280),
                         allow_none=True)


@review.route("/party/<int:party_id>/review/add", methods=["POST"])
@session_token_validation
def add_review(party_id):
    # TODO
    party = Party.query.filter_by(id=party_id).first()

    if party is None:
        return failure_response(f"Party with ID of {party_id} not found.")

    try:
        request_body = ReviewSchema().load(request.get_json())
    except ValidationError as err:
        return failure_response(err.messages, 400)

    new_review = Review()


@review.route("/party/<int:party_id>/review/<int:review_id>/delete",
              methods=["DELETE"])
@session_token_validation
def delete_review(party_id, review_id):
    # TODO
    pass


@review.route("/party/<int:party_id>/review/all", methods=["GET"])
def get_reviews(party_id):
    # TODO
    pass
