import json

from django.test import RequestFactory
from django.test import TestCase

from accounts.models import User
from accounts.views import create_user


class UserCreateTests(TestCase):
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
