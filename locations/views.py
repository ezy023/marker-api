import json
import logging

from django.http import HttpResponse
from django.http import HttpResponseBadRequest

from locations.forms import LocationForm
from locations.models import Location


def create_location(request):
    form = LocationForm(request.POST, request.FILES)
    if form.is_valid():
        new_location = Location()
        new_location.latitude = form.cleaned_data['latitude']
        new_location.longitude = form.cleaned_data['longitude']
        image_file = form.cleaned_data['image']
        new_location.image_url = _handle_image_upload(image_file)
        request.user.location_set.add(new_location) # going to need some error handling here
        data = json.dumps(new_location.to_dict())

        return HttpResponse(data)
    else:
        error_data = json.dumps(form.errors)
        return HttpResponseBadRequest(error_data)


def delete_location(request):
    location_id = request.POST.get('location_id')
    if not location_id:
        errors = {"error": "Need location_id to delete location"}
        error_data = json.dumps(errors)
        return HttpResponseBadRequest(error_data)

    location = Location.objects.get(pk=location_id)
    location.delete()

    resp_data = {
        "status": "deleted",
        "id": location_id,
    }

    return HttpResponse(json.dumps(resp_data))



def _handle_image_upload(image_file):
    pass
