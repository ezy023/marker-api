import json
import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from django.test import TestCase
from mock import patch

from accounts.models import User
from locations.models import Location
from locations.views import create_location
from locations.views import delete_location

IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mock_data", "mock_image.png")

class LocationsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        img = open(IMAGE_PATH, "r")
        self.image_file = SimpleUploadedFile("image.jpg", img.read(), content_type='image/png')
        self.user = User.objects.create(username="test_user", email="test@mail.com")

    @patch('locations.views._handle_image_upload')
    def test_create_location(self, image_upload_func):
        image_upload_func.return_value = "fake.picture.url"
        post_data = {
            "latitude": "45.12345",
            "longitude": "90.67891",
            "image": self.image_file,
        }

        req = self.factory.post('create/', post_data)
        req.user = self.user
        resp = create_location(req)
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

        req = self.factory.post('create/', post_data)
        resp = create_location(req)

        self.assertEqual(400, resp.status_code)

    def test_create_location_no_latitude(self):
        post_data = {
            "longitude": "90.67891",
            "image": self.image_file,
        }

        req = self.factory.post('create/', post_data)
        resp = create_location(req)

        self.assertEqual(400, resp.status_code)

    def test_create_location_no_longitude(self):
        post_data = {
            "latitude": "45.12345",
            "image": self.image_file,
        }

        req = self.factory.post('create/', post_data)
        resp = create_location(req)

        self.assertEqual(400, resp.status_code)

    def test_delete_location(self):
        Location.objects.create(longitude=45.00, latitude=45.00, image_url="fake.url", user=self.user)
        post_data = {
            "location_id": 2,
        }
        req = self.factory.post('delete/', post_data)
        resp = delete_location(req)
        resp_data = json.loads(resp.content)

        self.assertEqual('2', resp_data.get('id'))
