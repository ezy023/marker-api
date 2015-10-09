import json

from django.test import RequestFactory
from django.test import TestCase
from mock import patch

from accounts.models import User
from accounts.views import create_user
from accounts.views import login_user
from oauth.models import Token


class UserCreationTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_user_creation(self):
        test_username = 'testuser'
        test_email = 'test@example.com'
        post_data = {
            'username': test_username,
            'email': test_email,
            'password': 'password'
        }
        req = self.factory.post('/create', data=post_data)
        resp = create_user(req)
        resp_content = json.loads(resp.content)
        created_user = User.objects.get(id=resp_content.get('id'))

        self.assertEqual(200, resp.status_code)
        self.assertEqual(created_user.username, test_username)
        self.assertEqual(created_user.email, test_email)
        self.assertTrue(created_user.token_set.first())

    def test_user_creation_no_email(self):
        test_username = 'testuser'
        post_data = {
            'username': test_username,
            'password': 'password'
        }
        req = self.factory.post('/create', data=post_data)
        resp = create_user(req)

        self.assertEqual(400, resp.status_code)

    def test_user_creation_no_password(self):
        test_username = 'testuser'
        test_email = 'test@example.com'
        post_data = {
            'username': test_username,
            'email': test_email,
        }
        req = self.factory.post('/create', data=post_data)
        resp = create_user(req)

        self.assertEqual(400, resp.status_code)

    def test_user_creation_get_request(self):
        req = self.factory.get('/create')
        resp = create_user(req)

        self.assertEqual(405, resp.status_code)


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.test_user_password = "password"
        self.test_user = User(username="testuser",
                              email="test@example.com")
        self.test_user.set_password(self.test_user_password)
        self.test_user.save()
        self.access_token = Token(token="test_access_token")
        self.test_user.token_set.add(self.access_token)


    def test_user_login_with_valid_credentials(self):
        post_data = {
            'username': "testuser",
            'password': "password",
        }
        req = self.factory.post('/login', post_data)
        resp = login_user(req)
        resp_data = json.loads(resp.content)

        self.assertEqual(200, resp.status_code)
        self.assertEqual("test_access_token", resp_data['access_token'])

    def test_user_login_with_bad_password(self):
        post_data = {
            'username': "wrong",
            'password': "password",
        }
        req = self.factory.post('/login', post_data)
        resp = login_user(req)

        self.assertEqual(404, resp.status_code)

    def test_user_login_with_valid_credentials(self):
        post_data = {
            'username': "testuser",
            'password': "wrong",
        }
        req = self.factory.post('/login', post_data)
        resp = login_user(req)

        self.assertEqual(404, resp.status_code)
