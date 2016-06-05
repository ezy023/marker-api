import json
import logging

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from locations.forms import LocationForm
from locations.models import Location
from aws.s3 import gen_signed_s3_image_post
from tagging.models import LocationTags
from tagging.models import Tag

from oauth.decorators import noauth

logger = logging.getLogger(__name__)

@csrf_exempt
def create_location(request, user_id):
    received_json_data = json.loads(request.body)
    form = LocationForm(received_json_data)
    if form.is_valid():
        new_location = Location()
        coordinates_point_string = "POINT(%s %s)" % (form.cleaned_data['latitude'], form.cleaned_data['longitude'])
        new_location.coordinates = coordinates_point_string
        new_location.image_url = form.cleaned_data['image_url']
        try:
            request.user.location_set.add(new_location)
        except Exception as e:
            logger.error("Error associating location to user. User %s Location %s. %s", request.user, new_location, e.message)
            return HttpResponseBadRequest(e.message)

        # Add tags to the location if any were passed
        tag_ids = form.cleaned_data['tag_ids']
        if tag_ids:
            tags = Tag.objects.filter(id__in=tag_ids)
            for tag in tags:
                LocationTags.objects.create(tag=tag, location=new_location)

        data = json.dumps(new_location.to_dict())
        return HttpResponse(data)
    else:
        logger.error("Form invalid. %s", form.errors)
        error_data = json.dumps(form.errors)
        return HttpResponseBadRequest(error_data)


# require post request
def delete_location(request, location_id):
    if not location_id:
        errors = {"error": "Need location_id to delete location"}
        error_data = json.dumps(errors)
        return HttpResponseBadRequest(error_data)

    location = Location.objects.get(pk=location_id)
    location.delete()
    logger.info("Location %s deleted by user %s", location_id, request.user)

    resp_data = {
        "status": "deleted",
        "id": location_id,
    }

    return HttpResponse(json.dumps(resp_data))


def all_locations(request, user_id):
    user = request.user
    locations = user.location_set.all()
    location_dicts = map(lambda l: l.to_dict(), locations)
    data = {
        "data": location_dicts,
    }

    return HttpResponse(json.dumps(data))

@noauth
@csrf_exempt
def generate_signed_post_request(request, user_id):
    data = gen_signed_s3_image_post()
    return HttpResponse(json.dumps(data), content_type='application/json')
