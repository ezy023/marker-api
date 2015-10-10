from django.conf.urls import url

from locations.views import all_locations
from locations.views import create_location
from locations.views import delete_location

urlpatterns = [
    url(r'^locations/', all_locations),
    url(r'^locations/create/', create_location),
    url(r'^locations/(?P<location_id>\d+)/delete/', delete_location),
]
