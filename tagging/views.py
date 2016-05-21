import json
import logging

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from accounts.models import User
from tagging.forms import TagForm
from tagging.models import Tag

logger = logging.getLogger(__name__)

@csrf_exempt
def create_tag(request, user_id):
    if request.method != 'POST':
        error_dict = {"message": "Method not allowed"}
        error_data = json.dumps(error_dict)
        return HttpResponseNotAllowed(error_data, content_type="application/json")

    received_json_data = json.loads(request.body)
    form = TagForm(received_json_data)
    if form.is_valid():
        new_tag = Tag(tag_name=form.cleaned_data['tag_name'])
        new_tag.user = request.user
        new_tag.save()
        data = json.dumps(new_tag.to_dict())
        return HttpResponse(data)
    else:
        logger.error("Invalid Tag Form. %s", form.errors)
        error_data = json.dumps(form.errors)
        return HttpResponseBadRequest(error_data)

def delete_tag(request, user_id, tag_id):
    if request.method != 'POST':
        error_dict = {"message": "Method not allowed"}
        error_data = json.dumps(error_dict)
        return HttpResponseNotAllowed(error_data, content_type="application/json")

    tag = Tag.objects.get(id=tag_id)
    if tag.user != request.user:
        error_dict = {"message": "Tag not found"}
        error_data = json.dumps(error_dict)
        return HttpResponseNotFound(error_data, content_type="application/json")

    tag.delete()
    resp_dict = {
        "status": "success",
        "tag_id": tag_id,
    }
    data = json.dumps(resp_dict)
    return HttpResponse(data)

def list_tags(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:
        error_dict = {"message": "Endpoint not found"}
        error_data = json.dumps(error_dict)
        return HttpResponseNotFound(error_data, content_type="application/json")

    tags = map(lambda x: x.to_dict(), Tag.objects.filter(user=request.user))
    resp_dict = {
        "tags": tags,
    }
    data = json.dumps(resp_dict)
    return HttpResponse(data, content_type='application/json')
