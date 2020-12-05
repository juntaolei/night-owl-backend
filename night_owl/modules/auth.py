from flask import Blueprint, request
from functools import wraps
from marshmallow import Schema, fields, validate, ValidationError
from night_owl.models import db, User, Session
from night_owl.utils import success_response, failure_response
from sqlalchemy.exc import IntegrityError

auth = Blueprint("auth", __name__, url_prefix="/api")


class RegistrationSchema(Schema):
    email = fields.Email()
    username = fields.Str(validate=validate.Length(min=1, max=32))
    first_name = fields.Str(validate=validate.Length(min=1, max=32))
    last_name = fields.Str(validate=validate.Length(min=1, max=32))
    password = fields.Str(validate=validate.Length(min=12, max=64))


class LoginSchema(Schema):
    username = fields.Str(validate=validate.Length(min=1, max=32))
    password = fields.Str(validate=validate.Length(min=12, max=64))


class SessionTokenSchema(Schema):
    session_token = fields.Str(validate=validate.Length(min=32, max=256))


class RefreshTokenSchema(Schema):
    refresh_token = fields.Str(validate=validate.Length(min=32, max=256))


def session_token_validation(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            request_body = SessionTokenSchema().load(request.get_json())
        except ValidationError as err:
            return failure_response(err.messages, 400)

        valid, data = Session.verify_token(request_body.get("session_token"))

        if not valid:
            return failure_response(data)

        return f(*args, **kwargs)

    return decorator


@auth.route("/register", methods=["POST"])
def register():
    try:
        request_body = RegistrationSchema().load(request.get_json())
    except ValidationError as err:
        return failure_response(err.messages, 400)

    try:
        new_user = User(email=request_body.get("email"),
                        username=request_body.get("username"),
                        first_name=request_body.get("first_name"),
                        last_name=request_body.get("last_name"),
                        password=request_body.get("password"))

        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        return failure_response("User already exist.", 500)

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

    session = Session.query.filter_by(user_id=user.id).first()
    session_token = user.generate_session_token().decode("ascii")
    refresh_token = user.generate_refresh_token().decode("ascii")

    if session is None:
        new_session = Session(session_token=session_token,
                              refresh_token=refresh_token,
                              user_id=user.id)

        db.session.add(new_session)
        db.session.commit()
    else:
        session.session_token = session_token
        session.refresh_token = refresh_token

        db.session.commit()

    return success_response(
        {
            "session_token": session_token,
            "refresh_token": refresh_token
        }, 201)


@auth.route("/refresh", methods=["POST"])
def refresh():
    try:
        request_body = RefreshTokenSchema().load(request.get_json())
    except ValidationError as err:
        return failure_response(err.messages, 400)

    valid, data = Session.verify_token(request_body.get("session_token"))

    if not valid:
        return failure_response(data)
    else:
        session = Session.query.filter_by(user_id=data.id).first()
        session_token = data.generate_session_token().decode("ascii")
        refresh_token = data.generate_refresh_token().decode("ascii")
        session.session_token = session_token
        session.refresh_token = refresh_token

        db.session.commit()

        return success_response(
            {
                "session_token": session_token,
                "refresh_token": refresh_token
            }, 201)


@auth.route("/logout", methods=["POST"])
@session_token_validation
def logout():
    try:
        request_body = SessionTokenSchema().load(request.get_json())
    except ValidationError as err:
        return failure_response(err.messages, 400)

    session = Session.query.filter_by(
        session_token=request_body.get("session_token")).first()

    db.session.delete(session)
    db.session.commit()

    return success_response()
