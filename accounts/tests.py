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
        test_email = "test@example.com"
        post_data = {
            "email": test_email,
            "password": "password"
        }
        resp = self.client.post('/users/create/', data=json.dumps(post_data), content_type="application/json")
        resp_content = json.loads(resp.content)
        created_user = User.objects.get(id=resp_content.get('id'))

        self.assertEqual(200, resp.status_code)
        self.assertEqual(created_user.email, test_email)
        self.assertTrue(created_user.token_set.first())

    def test_user_creation_no_email(self):
        post_data = {
            'password': 'password'
        }
        resp = self.client.post('/users/create/',
                               data=json.dumps(post_data),
                               content_type='application/json')

        self.assertEqual(400, resp.status_code)

    def test_user_creation_no_password(self):
        test_email = 'test@example.com'
        post_data = {
            'email': test_email,
        }
        resp = self.client.post('/users/create/',
                               data=json.dumps(post_data),
                               content_type='application/json')

        self.assertEqual(400, resp.status_code)

    def test_user_creation_get_request(self):
        req = self.factory.get('/create')
        resp = create_user(req)

        self.assertEqual(405, resp.status_code)


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.test_user_password = "password"
        self.test_user = User(email="test@example.com")
        self.test_user.set_password(self.test_user_password)
        self.test_user.save()
        self.access_token = Token(token="test_access_token")
        self.test_user.token_set.add(self.access_token)


    def test_user_login_with_valid_credentials(self):
        post_data = {
            'email': "test@example.com",
            'password': "password",
        }
        resp = self.client.post('/users/login/',
                                data=json.dumps(post_data),
                                content_type='application/json')
        resp_data = json.loads(resp.content)

        self.assertEqual(200, resp.status_code)
        self.assertEqual("test_access_token", resp_data['access_token'])

    def test_user_login_with_bad_password(self):
        post_data = {
            'email': "test@example.com",
            'password': "badpassword",
        }
        resp = self.client.post('/users/login/',
                                data=json.dumps(post_data),
                                content_type='application/json')

        self.assertEqual(404, resp.status_code)
