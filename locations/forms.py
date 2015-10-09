import decimal

from django import forms

MIN_LAT_LNG = decimal.Decimal('0.00000')
MAX_LATITUDE = decimal.Decimal('90.00000')
MAX_LONGITUDE = decimal.Decimal('180.00000')

class LocationForm(forms.Form):
    latitude = forms.DecimalField(required=True, max_value=MAX_LATITUDE, min_value=MIN_LAT_LNG)
    longitude = forms.DecimalField(required=True, max_value=MAX_LONGITUDE, min_value=MIN_LAT_LNG)
    image = forms.ImageField()
