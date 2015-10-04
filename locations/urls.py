from django.conf.urls import url

from locations.views import create_location

urlpatterns = [
    url(r'^create/', create_location),
]
