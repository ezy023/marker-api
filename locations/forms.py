import decimal

from django import forms

MIN_LATITUDE = decimal.Decimal('-90.00000')
MAX_LATITUDE = decimal.Decimal('90.00000')
MIN_LONGITUDE = decimal.Decimal('-180.00000')
MAX_LONGITUDE = decimal.Decimal('180.00000')


class IntegerListField(forms.Field):
    """
    This is a django form field class that represents a list of integers
    It expects to be passed in a JSON array of objects that it then maps to
    integer values.
    """
    def __init__(self, required=True, widget=None, label=None,
                 initial=None, help_text='', *args, **kwargs):
        super(IntegerListField, self).__init__(required=required,
                                        widget=widget,
                                        label=label,
                                        initial=initial,
                                        help_text=help_text,
                                        *args, **kwargs)

    def to_python(self, value):
        return map(int, value)


class LocationForm(forms.Form):
    latitude = forms.DecimalField(required=True, max_value=MAX_LATITUDE, min_value=MIN_LATITUDE)
    longitude = forms.DecimalField(required=True, max_value=MAX_LONGITUDE, min_value=MIN_LONGITUDE)
    image_url = forms.CharField(required=True)
    tag_ids = IntegerListField(required=False)
