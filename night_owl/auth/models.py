from flask import current_app
from itsdangerous import (BadSignature, SignatureExpired,
                          TimedJSONWebSignatureSerializer as TJWSS)
from night_owl import db
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    _password = db.Column(db.String(256), nullable=False)
    session = db.relationship("Session", cascade="delete", uselist=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, given_password):
        self._password = generate_password_hash(given_password)

    def check_password(self, given_password):
        return check_password_hash(self._password, given_password)

    def get_tokens(self):
        return self.session.serialize()

    def refresh_tokens(self):
        self.session.new_tokens()
        return self.get_tokens()

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username
        }

    @staticmethod
    def verify_user(username, given_password):
        user = User.query.filter_by(username=username).first()
        if user.check_password(given_password):
            return user
        return None


class Session(db.Model):
    __tablename__ = "session"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    session_token = db.Column(db.String(512))
    refresh_token = db.Column(db.String(512))

    def __generate_token(self, token_type, expiration):
        secret_key = current_app.config.get("SECRET_KEY")
        tjwss = TJWSS(secret_key, expires_in=expiration)
        token = tjwss.dumps({"id": self.user_id, "type": token_type})
        return token.decode("ascii")

    def new_tokens(self):
        self.session_token = self.__generate_token("session", 1200)
        self.refresh_token = self.__generate_token("refresh", 604800)
        db.session.commit()

    def serialize(self):
        return {
            "session_token": self.session_token,
            "refresh_token": self.refresh_token
        }

    @staticmethod
    def extract_user_id(token):
        secret_key = current_app.config.get("SECRET_KEY")
        tjwss = TJWSS(secret_key)
        try:
            return tjwss.loads(token).get("id")
        except:
            return None

    @staticmethod
    def verify_token(token):
        secret_key = current_app.config.get("SECRET_KEY")
        tjwss = TJWSS(secret_key)
        try:
            tjwss.loads(token)
            return None
        except SignatureExpired:
            return "Token expired."
        except BadSignature:
            return "Bad token."
        except:
            return "Invalid token."

    @staticmethod
    def verify_session(token):
        res = Session.verify_token(token)
        if res is not None:
            return res
        session = Session.query.filter_by(session_token=token).first()
        if session is None:
            return "Invalid session."
        return None