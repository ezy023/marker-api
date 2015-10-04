import logging

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponseForbidden

from accounts.models import User

class UserAuthMiddleware(object):
    def process_request(self, request):
        try:
            request_dict = self._merge_get_post_dicts(request.GET, request.POST)
            access_token = request_dict.get('access_token')
            if access_token:
                valid_user = self._auth_user_with_access_token(request, access_token)
                if not valid_user:
                    return HttpResponseForbidden()

                request.user = valid_user
            else:
                return HttpResponseForbidden()

        except Exception as e:
            return HttpResponseForbidden()

        return None


    def _auth_user_with_access_token(self, request, access_token):
        user = User.objects.filter(token__token=access_token).first()
        auth_user = authenticate(username=user.username)
        return auth_user

    def _merge_get_post_dicts(self, get_dict, post_dict):
        get_dict_copy = get_dict.copy()
        get_dict_copy.update(post_dict)
        return get_dict_copy
