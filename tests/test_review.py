from json import dumps
from night_owl import create_app, db
from unittest import TestCase


class ReviewTest(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.from_mapping(DEBUG=True, TESTING=True)
        self.test_client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()

    def test_bad_get_all_reviews(self):
        response = self.test_client.get("/api/party/2/review/all")
        self.assertEqual(
            "Requested resource not found.",
            response.json["message"],
        )
        self.assertEqual(404, response.status_code)

    def test_get_all_reviews(self):
        payload = dumps({
            "email": "example@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe1",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/register",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        payload = dumps({
            "username": "johndoe1",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/login",
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
            "images": []
        })
        response = self.test_client.post(
            "/api/party/add",
            headers={
                "Content-Type": "application/json",
                "Authorization": session_token
            },
            data=payload,
        )
        response = self.test_client.get("/api/party/1/review/all")
        self.assertEqual([], response.json["data"])
        self.assertEqual(200, response.status_code)

    def test_bad_add_review(self):
        payload = dumps({
            "email": "example@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe1",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/register",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        payload = dumps({
            "username": "johndoe1",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/login",
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
            "images": []
        })
        response = self.test_client.post(
            "/api/party/add",
            headers={
                "Content-Type": "application/json",
                "Authorization": session_token
            },
            data=payload,
        )
        payload = dumps({})
        response = self.test_client.post(
            "/api/party/1/review/add",
            headers={
                "Content-Type": "application/json",
                "Authorization": session_token
            },
            data=payload,
        )
        self.assertEqual(
            "Missing data for required field.",
            response.json["message"]["rating"][0],
        )
        self.assertEqual(400, response.status_code)

    def test_add_review(self):
        payload = dumps({
            "email": "example@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe1",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/register",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        payload = dumps({
            "username": "johndoe1",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/login",
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
            "images": []
        })
        response = self.test_client.post(
            "/api/party/add",
            headers={
                "Content-Type": "application/json",
                "Authorization": session_token
            },
            data=payload,
        )
        payload = dumps({"rating": 4.5})
        response = self.test_client.post(
            "/api/party/1/review/add",
            headers={
                "Content-Type": "application/json",
                "Authorization": session_token
            },
            data=payload,
        )
        self.assertEqual(4.5, response.json["data"]["rating"])
        self.assertEqual(201, response.status_code)
        payload = dumps({"rating": 4.5, "comment": "Very fun!"})
        response = self.test_client.post(
            "/api/party/1/review/add",
            headers={
                "Content-Type": "application/json",
                "Authorization": session_token
            },
            data=payload,
        )
        self.assertEqual("Very fun!", response.json["data"]["comment"])
        self.assertEqual(201, response.status_code)
        payload = dumps({"rating": 4.5, "comment": "Very fun!", "images": []})
        response = self.test_client.post(
            "/api/party/1/review/add",
            headers={
                "Content-Type": "application/json",
                "Authorization": session_token
            },
            data=payload,
        )
        self.assertEqual("Very fun!", response.json["data"]["comment"])
        self.assertEqual(201, response.status_code)

    def test_bad_delete_review(self):
        payload = dumps({
            "email": "example@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe1",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/register",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        payload = dumps({
            "username": "johndoe1",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/login",
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
            "images": []
        })
        response = self.test_client.post(
            "/api/party/add",
            headers={
                "Content-Type": "application/json",
                "Authorization": session_token
            },
            data=payload,
        )
        payload = dumps({"rating": 4.5})
        response = self.test_client.post(
            "/api/party/1/review/add",
            headers={
                "Content-Type": "application/json",
                "Authorization": session_token
            },
            data=payload,
        )
        response = self.test_client.delete(
            "/api/party/1/review/2/delete",
            headers={
                "Content-Type": "application/json",
                "Authorization": session_token
            },
        )
        self.assertEqual(
            "Requested resource not found.",
            response.json["message"],
        )
        self.assertEqual(404, response.status_code)
        response = self.test_client.delete(
            "/api/party/2/review/2/delete",
            headers={
                "Content-Type": "application/json",
                "Authorization": session_token
            },
        )
        self.assertEqual(
            "Requested resource not found.",
            response.json["message"],
        )
        self.assertEqual(404, response.status_code)
        payload = dumps({
            "email": "jane@example.com",
            "first_name": "Jane",
            "last_name": "Doe",
            "username": "janedoe1",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/register",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        payload = dumps({
            "username": "janedoe1",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/login",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        session_token = response.json["data"]["session_token"]
        response = self.test_client.delete(
            "/api/party/1/review/1/delete",
            headers={
                "Content-Type": "application/json",
                "Authorization": session_token
            },
        )
        self.assertEqual(
            "Unauthorized request.",
            response.json["message"],
        )
        self.assertEqual(401, response.status_code)\

    def test_delete_review(self):
        payload = dumps({
            "email": "example@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe1",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/register",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        payload = dumps({
            "username": "johndoe1",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/login",
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
            "images": []
        })
        response = self.test_client.post(
            "/api/party/add",
            headers={
                "Content-Type": "application/json",
                "Authorization": session_token
            },
            data=payload,
        )
        payload = dumps({"rating": 4.5})
        response = self.test_client.post(
            "/api/party/1/review/add",
            headers={
                "Content-Type": "application/json",
                "Authorization": session_token
            },
            data=payload,
        )
        response = self.test_client.delete(
            "/api/party/1/review/1/delete",
            headers={
                "Content-Type": "application/json",
                "Authorization": session_token
            },
        )
        self.assertEqual(4.5, response.json["data"]["rating"])
        self.assertEqual(201, response.status_code)