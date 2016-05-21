import json
import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from django.test import TestCase

from accounts.models import User
from locations.models import Location
from locations.views import all_locations
from locations.views import create_location
from locations.views import delete_location
from oauth.models import Token
from tagging.models import Tag

IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mock_data", "mock_image.png")

class LocationsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        img = open(IMAGE_PATH, "r")
        self.image_file = SimpleUploadedFile("image.jpg", img.read(), content_type='image/png')
        self.user = User.objects.create(email="test@mail.com")

    def test_create_location(self):
        post_data = {
            "latitude": "45.12345",
            "longitude": "90.67891",
            "image_url": "fake.picture.url",
        }

        req = self.factory.post('create/', json.dumps(post_data), content_type="application/json")
        req.user = self.user
        resp = create_location(req, self.user.id)
        resp_data = json.loads(resp.content)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(1, resp_data.get('id'))
        self.assertEqual('45.12345', resp_data.get('lat'))
        self.assertEqual('90.67891', resp_data.get('lng'))
        self.assertEqual("fake.picture.url", resp_data.get('image_url'))

    def test_create_location_no_image(self):
        post_data = {
            "latitude": "45.12345",
            "longitude": "90.67891",
        }

        req = self.factory.post('create/', json.dumps(post_data), content_type="application/json")
        resp = create_location(req, self.user.id)

        self.assertEqual(400, resp.status_code)

    def test_create_location_no_latitude(self):
        post_data = {
            "longitude": "90.67891",
            "image_url": "fake.image.url",
        }

        req = self.factory.post('create/', json.dumps(post_data), content_type="application/json")
        resp = create_location(req, self.user.id)

        self.assertEqual(400, resp.status_code)

    def test_create_location_no_longitude(self):
        post_data = {
            "latitude": "45.12345",
            "image_url": "fake.image.url",
        }

        req = self.factory.post('create/', json.dumps(post_data), content_type="application/json")
        resp = create_location(req, self.user.id)

        self.assertEqual(400, resp.status_code)

    def test_delete_location(self):
        location = Location.objects.create(longitude=45.00, latitude=45.00, image_url="fake.url", user=self.user)
        location_id = location.id
        req = self.factory.post('delete/')
        req.user = self.user
        resp = delete_location(req, location_id)
        resp_data = json.loads(resp.content)

        self.assertEqual(location.id, resp_data.get('id'))

    def test_get_all_locations(self):
        Location.objects.create(longitude=45.00, latitude=45.00, image_url="fake.url", user=self.user)
        Location.objects.create(longitude=45.00, latitude=45.00, image_url="fake.url2", user=self.user)
        req = self.factory.get('locations/')
        req.user = self.user
        resp = all_locations(req, self.user.id)
        resp_data = json.loads(resp.content)

        self.assertEqual(2, len(resp_data.get('data')))

class LocationsWithTagsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@email.com",
                                        password="password",
                                        first_name="Erik",
                                        last_name="Test")

        self.user_token = Token.objects.create(token="test_token",
                                               user=self.user)

        self.tag1 = Tag.objects.create(tag_name="tag1", user=self.user)
        self.tag2 = Tag.objects.create(tag_name="tag2", user=self.user)

    def test_create_location_with_tag(self):
        url = '/users/{user_id}/locations/create/'
        formatted_url = url.format(user_id=self.user.id)
        post_data = {
            "latitude": "45.12345",
            "longitude": "90.67891",
            "image_url": "fake.picture.url",
            "tag_ids": [self.tag1.id, self.tag2.id],
        }
        auth_header = "Token %s" % self.user_token.token

        response = self.client.post(formatted_url,
                                    data=json.dumps(post_data),
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=auth_header)
        new_location = Location.objects.first()

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(new_location.tags.all()))
