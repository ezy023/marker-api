from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from marker import urls

class Command(BaseCommand):
    def handle(self, *args, **options):
        self._show_urls(urls.urlpatterns)

    def _show_urls(self, urllist, depth=0):
        for entry in urllist:
            print "  " * depth, entry.regex.pattern
            if hasattr(entry, 'url_patterns'):
                self._show_urls(entry.url_patterns, depth + 1)
