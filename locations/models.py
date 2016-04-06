from django.db import models

class LocationManager(models.Manager):
    pass

class Location(models.Model):
    # Plan on storing 5 decimal places for now, with 8 total digits
    # I want to add an index on latitude and longitude
    # The index should use a BTREE https://dev.mysql.com/doc/refman/5.5/en/index-btree-hash.html
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    image_url = models.CharField(max_length=1024)
    user = models.ForeignKey('accounts.User')
    # tags = models.ManyToManyField('tagging.Tag',
    #                               through='LocationTags',
    #                               through_fields=('location_id', 'tag_id'),
    #                               related_name='tags')

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
