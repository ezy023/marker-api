import decimal

from django import forms

MIN_LATITUDE = decimal.Decimal('-90.00000')
MAX_LATITUDE = decimal.Decimal('90.00000')
MIN_LONGITUDE = decimal.Decimal('-180.00000')
MAX_LONGITUDE = decimal.Decimal('180.00000')


class LocationForm(forms.Form):
    latitude = forms.DecimalField(required=True, max_value=MAX_LATITUDE, min_value=MIN_LATITUDE)
    longitude = forms.DecimalField(required=True, max_value=MAX_LONGITUDE, min_value=MIN_LONGITUDE)
    image_url = forms.CharField(required=True)
