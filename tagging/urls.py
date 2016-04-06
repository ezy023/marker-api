from django.conf.urls import url

from tagging.views import all_tags_for_user

urlpatterns = [
    url(r'^tags/$', all_tags_for_user),
]
