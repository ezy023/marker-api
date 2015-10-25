import logging
import json

from django.contrib.auth import authenticate
from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from accounts.forms import UserRegistrationForm
from accounts.models import User
from oauth.decorators import noauth
from oauth.models import Token

logger = logging.getLogger(__name__)

@noauth
@csrf_exempt
def create_user(request):
    if request.POST:
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = User()
            user.email = form.cleaned_data.get('email')
            user.set_password(form.cleaned_data.get('password'))
            with transaction.atomic():
                user.save()
                token = Token.create_token()
                user.token_set.add(token)

            logger.info("New user created. Email: %s", user.email)
            user_dict = user.to_dict()
            user_dict['access_token'] = token.token
            data = json.dumps(user_dict)
            return HttpResponse(data)
        else:
            logger.error("Invalid form to create new user. Errors: %s", form.errors)
            data = json.dumps(form.errors)
            return HttpResponseBadRequest(data)
    else:
        return HttpResponseNotAllowed(['POST'])

@noauth
@csrf_exempt
def login_user(request):
    if not request.POST:
        return HttpResponseNotAllowed(['POST'])

    email = request.POST.get('email')
    password = request.POST.get('password')
    user = None
    try:
        user = authenticate(email=email, password=password)
    except User.DoesNotExist as e:
        logger.error("Error logging in user. Email: %s. %s", email, e.message)
        return HttpResponseNotFound("Invalid username and password")

    if not user:
        return HttpResponseNotFound("Invalid username and password")

    user_dict = user.to_dict()
    user_dict['access_token'] = user.token_set.first().token
    data = json.dumps(user_dict)
    return HttpResponse(data)
