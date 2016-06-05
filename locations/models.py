from django.contrib.gis.db import models

class LocationManager(models.Manager):
    pass

class Location(models.Model):
    # I want to add an index on latitude and longitude
    coordinates = models.PointField(srid=4326, null=True)
    image_url = models.CharField(max_length=1024) # this may become longer?
    # visited = models.BooleanField(default=False)
    user = models.ForeignKey('accounts.User')
    tags = models.ManyToManyField('tagging.Tag',
                                  through='tagging.LocationTags',
                                  through_fields=('location_id', 'tag_id'),
                                  related_name='tags')

    class Meta:
        db_table = 'locations'

    objects = LocationManager()

    def to_dict(self):
        dict = {
            "id": self.id,
            "user": self.user.id,
            "lat": str(self.coordinates.x),
            "lng": str(self.coordinates.y),
            "image_url": self.image_url,
        }

        return dict
