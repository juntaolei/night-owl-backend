from flask_sqlalchemy import SQLAlchemy
from itsdangerous import (TimedJSONWebSignatureSerializer as JWS, BadSignature,
                          SignatureExpired)
from os import getenv
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    _password = db.Column("password", db.String(128), nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, given_password):
        self._password = generate_password_hash(given_password)

    def check_password(self, given_password):
        return check_password_hash(self.password, given_password)

    def __generate_token(self, expiration):
        jws = JWS(getenv("SECRET_KEY", "dev"), expires_in=expiration)

        return jws.dumps({"id": self.id})

    def generate_session_token(self):
        return self.__generate_token(1200)

    def generate_refresh_token(self):
        return self.__generate_token(604800)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name
        }


class Session(db.Model):
    __tablename__ = "session"

    id = db.Column(db.Integer, primary_key=True)
    session_token = db.Column(db.String(512), nullable=False)
    refresh_token = db.Column(db.String(512), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    @staticmethod
    def verify_token(token):
        jws = JWS(getenv("SECRET_KEY", "dev"))

        try:
            data = jws.loads(token)
        except SignatureExpired:
            return (False, "Token expired.")
        except BadSignature:
            return (False, "Bad token.")

        user = User.query.filter_by(id=data["id"]).first()

        return (True, user)
