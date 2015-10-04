import logging
import json

from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from django.shortcuts import render

from accounts.forms import UserRegistrationForm
from accounts.models import User
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
        return HttpResponseNotAllowed('POST')
