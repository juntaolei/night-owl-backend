# Night Owl Backend

![unittest](https://github.com/juntaolei/night-owl-backend/workflows/Flask%20Unit%20Test%20CI/badge.svg)
![heroku](https://github.com/juntaolei/night-owl-backend/workflows/Heroku%20CI/badge.svg)

Night Owl allows users to check where parties are as well as how fun those parties are,
saving you from a potentially disappointing event. With this app, you can browse all available
parties created by other users. You can read the reviews for a party and rate the party
yourself.

**Requirements**

**Backend**

* Created a Swagger API documentation.
* Added a relational database schema with SQLAlchemy.
* Added application endpoints with at least one GET, POST, and DELETE requests that interface with the database.
* Deployed to Heroku.

This app's iOS frontend is available on this [GitHub repository](https://github.com/juntaolei/night-owl-ios).

## Documentation

The backend API documentation is available on [SwaggerHub](https://app.swaggerhub.com/apis-docs/juntaolei/night-owl/1.0.0).

## Development

Create a virtual environment and run locally on Linux and MacOS:

```bash
python3 -m venv venv
FLASK_ENV=development FLASK_APP=night_owl venv/bin/flask run
```

## Unit Testing

Run all provided test cases on Linux and MacOS:

```bash
python3 -m venv venv
venv/bin/python -m unittest tests/test_all.py
```

Run a specific set of test cases on Linux and MacOS:

```bash
python3 -m venv venv
venv/bin/python -m unittest tests/test_auth.py
venv/bin/python -m unittest tests/test_image.py
venv/bin/python -m unittest tests/test_party.py
venv/bin/python -m unittest tests/test_review.py
```

## Deploy to Heroku

Creating a release on GitHub will automatically create an image and deploy it to Heroku.
Add the following configuration variables on Heroku:

* SECRET_KEY
* DATABASE_URL (Heroku PostgreSQL)
* GCS_BUCKET
* GCS_CREDENTIALS (Google Service Account)
