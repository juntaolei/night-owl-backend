from .auth import session_token_validation
from flask import Blueprint, request
from marshmallow import Schema, fields, validate, ValidationError
from night_owl.models import db, Party, Session
from night_owl.utils import success_response, failure_response

party = Blueprint("party", __name__, url_prefix="/api")


class PartySchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=64))
    datetime = fields.DateTime()
    address = fields.Str(validate=validate.Length(min=1, max=256))
    description = fields.Str(validate=validate.Length(min=1, max=280))


@party.route("/party/all", methods=["GET"])
def get_all_parties():
    return success_response([p.serialize() for p in Party.query.all()])


@party.route("/party/<int:party_id>", methods=["GET"])
def get_a_party(party_id):
    party = Party.query.filter_by(id=party_id).first()

    if party is None:
        return failure_response(f"Party with ID of {party_id} not found.")

    return success_response(party.serialize())


@party.route("/party/add", methods=["POST"])
@session_token_validation
def create_party():
    try:
        request_body = PartySchema().load(request.get_json())
    except ValidationError as err:
        return failure_response(err.messages, 400)

    valid, data = Session.verify_token(request_body.get("session_token"))

    if not valid:
        return failure_response(data, 400)

    new_party = Party(name=request_body.get("name"),
                      datetime=request_body.get("date"),
                      description=request_body.get("description"),
                      address=request_body.get("address"),
                      admin_id=data.id)

    db.session.add(new_party)
    db.session.commit()

    return success_response()


@party.route("/party/<int:party_id>/delete", methods=["DELETE"])
@session_token_validation
def delete_party(party_id):
    party = Party.query.filter_by(id=party_id).first()

    if party is None:
        return failure_response(f"Party with ID of {party_id} not found.")

    valid, data = Session.verify_token(request.get_json().get("session_token"))

    if not valid:
        return failure_response(data, 400)

    if data.id != party.admin_id:
        return failure_response("User does not have permission to delete.",
                                500)

    db.session.delete(party)
    db.session.commit()

    return success_response()
