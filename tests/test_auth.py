from json import dumps
from night_owl import create_app, db
from unittest import TestCase


class AuthTest(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.from_mapping(DEBUG=True, TESTING=True)
        self.test_client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()

    def test_bad_register(self):
        payload = dumps({
            "email": "example@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe1",
            "password": "a"
        })
        response = self.test_client.post(
            "/api/register",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        self.assertEqual(False, response.json["success"])
        self.assertEqual(400, response.status_code)
        payload = dumps({
            "email": "example@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/register",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        self.assertEqual(
            "Missing data for required field.",
            response.json["message"]["username"][0],
        )
        self.assertEqual(False, response.json["success"])
        self.assertEqual(400, response.status_code)
        self.test_register()
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
        self.assertEqual("Internal server error.", response.json["message"])
        self.assertEqual(500, response.status_code)

    def test_register(self):
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
        self.assertEqual("User created.", response.json["message"])
        self.assertEqual(201, response.status_code)

    def test_bad_login(self):
        self.test_register()
        payload = dumps({
            "username": "johndoe1",
            "password": "asdaf3fasfjoiqhasfgaqa"
        })
        response = self.test_client.post(
            "/api/login",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        self.assertEqual(
            "Requested resource not found.",
            response.json["message"],
        )
        self.assertEqual(404, response.status_code)
        payload = dumps({"username": "johndoe1", "password": "a"})
        response = self.test_client.post(
            "/api/login",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        self.assertEqual(
            "Length must be between 12 and 64.",
            response.json["message"]["password"][0],
        )
        self.assertEqual(400, response.status_code)
        payload = dumps({"username": "johndoe1"})
        response = self.test_client.post(
            "/api/login",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        self.assertEqual(
            "Missing data for required field.",
            response.json["message"]["password"][0],
        )
        self.assertEqual(400, response.status_code)

    def test_login(self):
        self.test_register()
        payload = dumps({
            "username": "johndoe1",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/login",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        self.assertEqual(str, type(response.json["data"]["session_token"]))
        self.assertEqual(str, type(response.json["data"]["refresh_token"]))
        self.assertEqual("johndoe1", response.json["data"]["username"])
        self.assertEqual(201, response.status_code)

    def test_bad_refresh(self):
        self.test_register()
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
        response = self.test_client.patch(
            "/api/refresh",
            headers={"Authorization": session_token},
        )
        self.assertEqual(
            "Requested resource not found.",
            response.json["message"],
        )
        self.assertEqual(404, response.status_code)

    def test_refresh(self):
        self.test_register()
        payload = dumps({
            "username": "johndoe1",
            "password": "thisisasecurepassword"
        })
        response = self.test_client.post(
            "/api/login",
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        refresh_token = response.json["data"]["refresh_token"]
        response = self.test_client.patch(
            "/api/refresh",
            headers={"Authorization": refresh_token},
        )
        self.assertEqual(str, type(response.json["data"]["session_token"]))
        self.assertEqual(str, type(response.json["data"]["refresh_token"]))
        self.assertEqual(201, response.status_code)

    def test_bad_logout(self):
        self.test_register()
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
        response = self.test_client.patch(
            "/api/refresh",
            headers={"Authorization": session_token},
        )
        self.assertEqual(
            "Requested resource not found.",
            response.json["message"],
        )
        self.assertEqual(404, response.status_code)

    def test_logout(self):
        self.test_register()
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
        response = self.test_client.delete(
            "/api/logout",
            headers={"Authorization": session_token},
        )
        self.assertEqual("User logged out.", response.json["message"])
        self.assertEqual(201, response.status_code)
    
    def test_login_logout(self):
        self.test_register()
        for i in range(0, 10):
            payload = dumps({
                "username": "johndoe1",
                "password": "thisisasecurepassword"
            })
            response = self.test_client.post(
                "/api/login",
                headers={"Content-Type": "application/json"},
                data=payload,
            )
            self.assertEqual(str, type(response.json["data"]["session_token"]))
            self.assertEqual(str, type(response.json["data"]["refresh_token"]))
            self.assertEqual("johndoe1", response.json["data"]["username"])
            self.assertEqual(201, response.status_code)
            session_token = response.json["data"]["session_token"]
            response = self.test_client.delete(
                "/api/logout",
                headers={"Authorization": session_token},
            )
            self.assertEqual("User logged out.", response.json["message"])
            self.assertEqual(201, response.status_code)