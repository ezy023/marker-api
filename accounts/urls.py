from django.conf.urls import url

from accounts.views import create_user
from accounts.views import login_user

urlpatterns = [
    url(r'^create/', create_user),
    url(r'^login/', login_user),
]
