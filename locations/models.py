from django.db import models

class LocationManager(models.Manager):
    pass

class Location(models.Model):
    class Meta:
        db_table = 'locations'

    objects = LocationManager()
