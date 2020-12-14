from night_owl.auth.auth import validate_token
from .models import Review
from .schemas import ReviewSchema
from flask import abort, Blueprint, request
from marshmallow import ValidationError
from night_owl import db, image
from night_owl.auth import validate_session, validate_token, Session
from night_owl.party import Party

review = Blueprint("review", __name__, url_prefix="/api")


@review.route("/party/<int:party_id>/review/all/", methods=["GET"])
def get_reviews(party_id):
    party = Party.query.filter_by(id=party_id).first_or_404()
    return {
        "success": True,
        "data": [r.serialize() for r in party.reviews]
    }, 200


@review.route("/party/<int:party_id>/review/add/", methods=["POST"])
@validate_token
@validate_session
def add_review(party_id):
    try:
        data = ReviewSchema().load(request.get_json())
        party = Party.query.filter_by(id=party_id).first_or_404()
        token = request.headers.get("Authorization", "")
        if len(token) > 0:
            token = token.split(" ")[1]
        user_id = Session.extract_user_id(token)
        new_review = Review(
            user_id=user_id,
            party_id=party.id,
            rating=data.get("rating"),
            comment=data.get("comment"),
        )
        if len(data.get("images", [])) > 0:
            image.upload(new_review, data.get("images"))
        db.session.add(new_review)
        db.session.commit()
        return {"success": True, "data": new_review.serialize()}, 201
    except ValidationError as err:
        return {"success": False, "message": err.messages}, 400
    except:
        abort(500)


@review.route("/party/<int:party_id>/review/<int:review_id>/delete/",
              methods=["DELETE"])
@validate_token
@validate_session
def delete_party(party_id, review_id):
    Party.query.filter_by(id=party_id).first_or_404()
    review = Review.query.filter_by(id=review_id).first_or_404()
    token = request.headers.get("Authorization", "")
    if len(token) > 0:
        token = token.split(" ")[1]
    user_id = Session.extract_user_id(token)
    if review.user_id != user_id:
        abort(401)
    db.session.delete(review)
    db.session.commit()
    return {"success": True, "data": review.serialize()}, 201