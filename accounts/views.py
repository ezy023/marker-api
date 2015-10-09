import logging
import json

from django.contrib.auth import authenticate
from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseNotFound

from accounts.forms import UserRegistrationForm
from accounts.models import User
from oauth.decorators import noauth
from oauth.models import Token


def create_user(request):
    # Need to add the retrieval of the oauth token
    if request.POST:
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = User()
            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('email')
            user.set_password(form.cleaned_data.get('password'))
            with transaction.atomic():
                user.save()
                token = Token.create_token()
                user.token_set.add(token)
            user_dict = user.to_dict()
            user_dict['access_token'] = token.token
            data = json.dumps(user_dict)
            return HttpResponse(data)
        else:
            data = json.dumps(form.errors)
            return HttpResponseBadRequest(data)
    else:
        return HttpResponseNotAllowed(['POST'])

@noauth
def login_user(request):
    if not request.POST:
        return HttpResponseNotAllowed(['POST'])

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = None
    try:
        user = authenticate(username=username, password=password)
    except User.DoesNotExist as e:
        return HttpResponseNotFound("Invalid username and password")

    if not user:
        return HttpResponseNotFound("Invalid username and password")

    user_dict = user.to_dict()
    user_dict['access_token'] = user.token_set.first().token
    data = json.dumps(user_dict)
    return HttpResponse(data)
