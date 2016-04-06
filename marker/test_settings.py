import sys

from marker.settings import *
from django.test.runner import DiscoverRunner


class UnManagedModelTestRunner(DiscoverRunner):
    '''
    Test runner that automatically makes all unmanaged models in your Django
    project managed for the duration of the test run.
    Many thanks to the Caktus Group: http://bit.ly/1N8TcHW
    '''

    def setup_test_environment(self, *args, **kwargs):
        from django.db.models.loading import get_models
        self.unmanaged_models = [m for m in get_models() if not m._meta.managed]
        for m in self.unmanaged_models:
            m._meta.managed = True
        super(UnManagedModelTestRunner, self).setup_test_environment(*args, **kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        super(UnManagedModelTestRunner, self).teardown_test_environment(*args, **kwargs)
        # reset unmanaged models
        for m in self.unmanaged_models:
            m._meta.managed = False


if 'test' in sys.argv or 'test_coverage' in sys.argv:  # Covers regular testing and django-coverage

    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
    DATABASES['default']['HOST'] = '127.0.0.1'
    DATABASES['default']['USER'] = 'username'
    DATABASES['default']['PASSWORD'] = 'secret'

# Set Django's test runner to the custom class defined above
TEST_RUNNER = 'marker.test_settings.UnManagedModelTestRunner'
