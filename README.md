# Night Owl Backend

---

## [API Documentation](https://app.swaggerhub.com/apis-docs/juntaolei/night-owl/1.0.0)

---

---

## [Night Owl IOS Frontend](https://github.com/juntaolei/night-owl-ios)

---

---

## Development

---

Linux and MacOS

```bash
python3 -m venv venv
FLASK_ENV=development FLASK_APP=night_owl venv/bin/flask run
```

---

## Unit Testing

---

### All Test Cases

Linux and MacOS

```bash
python3 -m venv venv
venv/bin/python -m unittest tests/test_all.py
```

### Specific Test Cases

Linux and MacOS

```bash
python3 -m venv venv
venv/bin/python -m unittest tests/test_{auth/image/review/party}.py
```

---

## Deploy to Heroku

---

Creating a release on GitHub will automatically create an image and deploy it to Heroku.

Add the following configuration variables on Heroku:

* SECRET_KEY
* DATABASE_URL (Heroku PostgreSQL)
* GCS_BUCKET
* GCS_CREDENTIALS (Google Service Account)
