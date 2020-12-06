from os import getenv


class Config:
    DB_HOST = None
    DB_PASSWORD = None
    DB_USER = None
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = getenv("PORT", 5000)
    SECRET_KEY = getenv("SECRET_KEY", "dev")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        if not self.DEBUG and None in (self.DB_HOST, self.DB_PASSWORD,
                                       self.DB_USER):
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/database"
        return "sqlite:///local.db"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DB_HOST = getenv("POSTGRES_HOST", None)
    DB_PASSWORD = getenv("POSTGRES_PASSWORD", None)
    DB_USER = getenv("POSTGRES_USER", None)
