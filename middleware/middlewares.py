import logging

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponseForbidden

from accounts.models import User

class UserAuthMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if not getattr(view_func, 'noauth', False):
            try:
                self.authenticate_token_request(request)
            except Exception as e:
                return HttpResponseForbidden()

        return None


    def authenticate_token_request(self, request):
        auth = self.get_authorization_header(request).split()

        if not auth or auth[0].lower() != 'token':
            return HttpResponseForbidden()

        access_token = auth[1]

        valid_user = self._auth_user_with_access_token(request, access_token)
        if not valid_user:
            return HttpResponseForbidden()

    def _auth_user_with_access_token(self, request, access_token):
        auth_user = authenticate(access_token=access_token)
        login(request, auth_user)
        return auth_user


    def get_authorization_header(self, request):
        return request.META.get('HTTP_AUTHORIZATION')
