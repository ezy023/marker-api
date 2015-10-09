from django.conf.urls import url

from locations.views import create_location
from locations.views import delete_location

urlpatterns = [
    url(r'^create/', create_location),
    url(r'^delete/', delete_location),
]
