from django.conf.urls import url

from tagging.views import create_tag
from tagging.views import delete_tag
from tagging.views import list_tags

urlpatterns = [
    url(r'^tags/$', list_tags),
    url(r'^tags/create/$', create_tag),
    url(r'^tags/(?P<tag_id>\d+)/delete/$', delete_tag),
]
