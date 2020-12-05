from os import getenv


class Config:
    DB_URL = None
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = getenv("PORT", 5000)
    SECRET_KEY = getenv("SECRET_KEY", "dev")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        if not self.DEBUG and self.DB_URL is not None:
            return self.DB_URL
        return "sqlite:///local.db"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DB_URL = getenv("DATABASE_URL", None)
