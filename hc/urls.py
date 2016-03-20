from django.conf.urls import url

from hc.views import api_status

urlpatterns = [
    url(r'^status/', api_status),
]
