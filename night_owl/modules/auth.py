from flask import Blueprint, request
from functools import wraps
from marshmallow import Schema, fields, validate, ValidationError
from night_owl.models import db, User, Session
from night_owl.utils import success_response, failure_response
from sqlalchemy.exc import IntegrityError

auth = Blueprint("auth", __name__, url_prefix="/api")


class UserSchema(Schema):
    email = fields.Email()
    username = fields.Str(validate=validate.Length(min=1, max=32))
    first_name = fields.Str(validate=validate.Length(min=1, max=32))
    last_name = fields.Str(validate=validate.Length(min=1, max=32))
    password = fields.Str(validate=validate.Length(min=12, max=64))


class LoginSchema(Schema):
    username = fields.Str(validate=validate.Length(min=1, max=32))
    password = fields.Str(validate=validate.Length(min=12, max=64))


class SessionTokenSchema(Schema):
    session_token = fields.Str(validate=validate.Length(min=32, max=64))


def session_token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            request_body = SessionTokenSchema().load(request.get_json())
        except ValidationError as err:
            return failure_response(message=err.messages, code=400)

        current_session = Session.query.filter_by(
            session_token=request_body.get("session_token")).first()

        if current_session is None:
            return failure_response("Invalid session token.")

        return f(*args, **kwargs)

    return decorator


@auth.route("/register", methods=["POST"])
def register():
    try:
        request_body = UserSchema().load(request.get_json())
    except ValidationError as err:
        return failure_response(message=err.messages, code=400)

    try:
        new_user = User(email=request_body.get("email"),
                        username=request_body.get("username"),
                        first_name=request_body.get("first_name"),
                        last_name=request_body.get("last_name"),
                        password=request_body.get("password"))

        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        return failure_response(message="User already exist.", code=500)

    return success_response(code=201)


@auth.route("/login", methods=["POST"])
def login():
    try:
        request_body = LoginSchema().load(request.get_json())
    except ValidationError as err:
        return failure_response(message=err.messages, code=400)

    user = User.query.filter_by(username=request_body.get("username")).first()

    if user is None or not user.check_password(request_body.get("password")):
        return failure_response("User not found or invalid credentials.")

    # Session Token To Be Implemented
    return success_response({"token": "testing"})


@auth.route("/logout", methods=["POST"])
@session_token_required
def logout():
    # Logout To Be Implemented
    return success_response()