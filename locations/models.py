from django.db import models

class LocationManager(models.Manager):
    pass

class Location(models.Model):
    # Plan on storing 5 decimal places for now, with 8 total digits
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    image_url = models.CharField(max_length=1024) # this may become longer?
    # visited = models.BooleanField(default=False)
    user = models.ForeignKey('accounts.User')

    class Meta:
        db_table = 'locations'

    objects = LocationManager()

    def to_dict(self):
        dict = {
            "id": self.id,
            "user": self.user.id,
            "lat": str(self.latitude),
            "lng": str(self.longitude),
            "image_url": self.image_url,
        }

        return dict
