import json

from django.test import RequestFactory
from django.test import TestCase

from accounts.models import User
from oauth.models import Token
from tagging.models import Tag

class TaggingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@email.com",
                                        password="password",
                                        first_name="Erik",
                                        last_name="Test")

        self.user_token = Token.objects.create(token="test_token",
                                               user=self.user)

        pass

    def test_create_tag(self):
        url = '/users/{user_id}/tags/create/?access_token={access_token}'
        post_data = {
            "tag_name": "test tag 1"
        }
        response = self.client.post(url.format(user_id=self.user.id, access_token=self.user_token.token),
                                    data=json.dumps(post_data),
                                    content_type='application/json')
        resp_content = json.loads(response.content)
        created_tag = Tag.objects.get(id=resp_content.get('id'))

        self.assertEqual(200, response.status_code)
        self.assertEqual(created_tag.tag_name, "test tag 1")
        self.assertTrue(created_tag.active)

    def test_delete_tag(self):
        tag = Tag.objects.create(tag_name="test tag deletion",
                                 user=self.user)

        url = '/users/{user_id}/tags/{tag_id}/delete/?access_token={access_token}'
        response = self.client.post(url.format(user_id=self.user.id,
                                               tag_id=tag.id,
                                               access_token=self.user_token.token),
                                    content_type='application/json')
        resp_content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual("success", resp_content.get('status'))
        self.assertEqual(tag.id, int(resp_content.get('tag_id')))
        with self.assertRaises(Tag.DoesNotExist):
            Tag.objects.get(id=tag.id)

    def test_list_all_tags(self):
        tag1 = Tag.objects.create(tag_name="tag1",
                                 user=self.user)
        tag2 = Tag.objects.create(tag_name="tag2",
                                 user=self.user)
        tag3 = Tag.objects.create(tag_name="tag3",
                                 user=self.user)

        url = '/users/{user_id}/tags/?access_token={access_token}'

        response = self.client.post(url.format(user_id=self.user.id,
                                               access_token=self.user_token.token))
        resp_content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(resp_content.get('tags')))
