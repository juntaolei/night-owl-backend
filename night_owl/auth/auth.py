from .models import Session, User
from .schemas import LoginSchema, RegistrationSchema
from flask import abort, Blueprint, request
from functools import wraps
from marshmallow import ValidationError
from night_owl import db

auth = Blueprint("auth", __name__, url_prefix="/api")


def validate_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        res = Session.verify_token(token)
        if res is not None:
            return {"success": False, "message": res}, 400
        return f(*args, **kwargs)

    return decorated_function


def validate_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        Session.query.filter_by(session_token=token).first_or_404()
        return f(*args, **kwargs)

    return decorated_function


@auth.route("/register/", methods=["POST"])
def register_user():
    try:
        data = RegistrationSchema().load(request.get_json())
        user = User(email=data.get("email"),
                    username=data.get("username"),
                    first_name=data.get("first_name"),
                    last_name=data.get("last_name"),
                    password=data.get("password"))
        db.session.add(user)
        db.session.commit()
        db.session.add(Session(user_id=user.id))
        db.session.commit()
        return {"success": True, "message": "User created."}, 201
    except ValidationError as err:
        return {"success": False, "message": err.messages}, 400
    except:
        abort(500)


@auth.route("/login/", methods=["POST"])
def login_user():
    try:
        data = LoginSchema().load(request.get_json())
        user = User.verify_user(data.get("username"), data.get("password"))
        auth_tokens = user.refresh_tokens()
        db.session.commit()
        response = {**auth_tokens, **user.serialize()}
        return {"success": True, "data": response}, 201
    except ValidationError as err:
        return {"success": False, "message": err.messages}, 400
    except AttributeError:
        abort(404)
    except:
        abort(500)


@auth.route("/refresh/", methods=["PATCH"])
@validate_token
def refresh_session():
    token = request.headers.get("Authorization")
    session = Session.query.filter_by(refresh_token=token).first_or_404()
    session.new_tokens()
    db.session.commit()
    return {"success": True, "data": session.serialize()}, 201


@auth.route("/logout/", methods=["DELETE"])
@validate_token
@validate_session
def logout():
    token = request.headers.get("Authorization")
    session = Session.query.filter_by(session_token=token).first_or_404()
    session.session_token = None
    session.refresh_token = None
    db.session.commit()
    return {"success": True, "message": "User logged out."}, 201