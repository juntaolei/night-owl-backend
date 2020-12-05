from os import getenv


class Config:
    DB_HOST = None
    DB_PASSWORD = None
    DB_USER = None
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = 5000
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        if not self.DEBUG and None not in (self.DB_HOST, self.DB_PASSWORD,
                                           self.DB_USER):
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/database"
        return "sqlite:///local.db"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DB_HOST = getenv("POSTGRES_HOST", None)
    DB_PASSWORD = getenv("POSTGRES_PASSWORD", None)
    DB_USER = getenv("POSTGRES_USER", None)
