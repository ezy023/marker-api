import logging
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from oauth.decorators import noauth

# TODO Remove This, just for Vagrant
@noauth
@csrf_exempt
def api_status(request):
    data = json.dumps({"status": "success"})
    return HttpResponse(data)
