from flask import app
from src import create_flask_app

# For local development only when executing the file directly.
if __name__ == "__main__":
    app = create_flask_app(True)
    app.run()
# For production only through import.
else:
    app = create_flask_app()
