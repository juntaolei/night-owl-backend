from night_owl.auth.auth import validate_token
from .models import Party
from .schemas import PartySchema
from flask import abort, Blueprint, request
from marshmallow import ValidationError
from night_owl import db, image
from night_owl.auth import Session, validate_session

party = Blueprint("party", __name__, url_prefix="/api")


@party.route("/party/all/", methods=["GET"])
def get_all_parties():
    return {
        "success": True,
        "data": [p.serialize() for p in Party.query.all()]
    }, 200


@party.route("/party/<int:party_id>/", methods=["GET"])
def get_a_party(party_id):
    return {
        "success": True,
        "data": Party.query.filter_by(id=party_id).first_or_404().serialize()
    }, 200


@party.route("/party/add/", methods=["POST"])
@validate_token
@validate_session
def add_party():
    try:
        data = PartySchema().load(request.get_json())
        new_party = Party(
            name=data.get("name"),
            datetime=data.get("datetime"),
            description=data.get("description"),
            address=data.get("address"),
            admin_id=Session.extract_user_id(
                request.headers.get("Authorization")),
        )
        if len(data.get("images", [])) > 0:
            image.upload(new_party, data.get("images"))
        db.session.add(new_party)
        db.session.commit()
        return {"success": True, "data": new_party.serialize()}, 201
    except ValidationError as err:
        return {"success": False, "message": err.messages}, 400
    except:
        abort(500)


@party.route("/party/<int:party_id>/delete/", methods=["DELETE"])
@validate_token
@validate_session
def delete_party(party_id):
    party = Party.query.filter_by(id=party_id).first_or_404()
    token = request.headers.get("Authorization")
    user_id = Session.extract_user_id(token)
    if party.admin_id != user_id:
        abort(401)
    db.session.delete(party)
    db.session.commit()
    return {"success": True, "data": party.serialize()}, 201