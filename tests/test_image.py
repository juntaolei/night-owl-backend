from json import dumps
from night_owl import create_app, db
from unittest import TestCase

jpeg_image = "data:image/jpeg;base64,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"


class ImageTest(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.from_mapping(DEBUG=True, TESTING=True)
        self.test_client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()

    def test_create_party_with_image(self):
        payload = dumps({
            "email": "example@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe1",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/register/",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        payload = dumps({
            "username": "johndoe1",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/login/",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        session_token = response.json["data"]["session_token"]
        payload = dumps({
            "name": "Christmas Party",
            "datetime": "2020-12-13T14:54:58.921515",
            "address": "1234 Main St. New York, NY 10282",
            "description": "Happy Christmas!",
            "admin_id": 1,
            "images": [jpeg_image]
        })
        response = self.test_client.post(
            "/api/party/add/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {session_token}"
            },
            data=payload,
        )
        self.assertEqual(str, type(response.json["data"]["images"][0]["url"]))
        self.assertEqual(201, response.status_code)

    def test_create_review_with_image(self):
        payload = dumps({
            "email": "example@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe1",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/register/",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        payload = dumps({
            "username": "johndoe1",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/login/",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        session_token = response.json["data"]["session_token"]
        payload = dumps({
            "name": "Christmas Party",
            "datetime": "2020-12-13T14:54:58.921515",
            "address": "1234 Main St. New York, NY 10282",
            "description": "Happy Christmas!",
            "admin_id": 1
        })
        response = self.test_client.post(
            "/api/party/add/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {session_token}"
            },
            data=payload,
        )
        payload = dumps({"rating": 4.5, "images": [jpeg_image]})
        response = self.test_client.post(
            "/api/party/1/review/add/",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {session_token}"
            },
            data=payload,
        )
        self.assertEqual(str, type(response.json["data"]["images"][0]["url"]))
        self.assertEqual(201, response.status_code)