from flask import app
from night_owl import create_app
from night_owl.configs import DevelopmentConfig

# For local development only when executing the file directly.
if __name__ == "__main__":
    create_app(DevelopmentConfig()).run()
