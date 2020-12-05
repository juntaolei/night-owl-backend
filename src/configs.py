from os import getenv


class Config:
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = 5000
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        if not self.DEBUG:
            return ""


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    pass
