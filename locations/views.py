import json
import logging

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render


def create_location(request):
    data = json.dumps({"first": "response"})
    return HttpResponse(data)
