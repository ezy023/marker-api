import json
import logging

from django.http import HttpResponse
from django.http import HttpResponseBadRequest

from locations.forms import LocationForm
from locations.models import Location

logger = logging.getLogger(__name__)

def create_location(request):
    form = LocationForm(request.POST, request.FILES)
    if form.is_valid():
        new_location = Location()
        new_location.latitude = form.cleaned_data['latitude']
        new_location.longitude = form.cleaned_data['longitude']
        image_file = form.cleaned_data['image']
        new_location.image_url = _handle_image_upload(image_file)
        try:
            request.user.location_set.add(new_location)
        except Exception as e:
            logger.error("Error associating location to user. User %s Location %s. %s", request.user, new_location, e.message)
            return HttpResponseBadRequest(e.message)

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


def all_locations(request):
    user = request.user
    locations = user.location_set.all()
    location_dicts = map(lambda l: l.to_dict(), locations)
    data = {
        "data": location_dicts,
    }

    return HttpResponse(json.dumps(data))


def _handle_image_upload(image_file):
    pass
