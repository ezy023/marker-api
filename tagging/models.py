from django.db import models

class TagManager(models.Manager):
    pass

class Tag(models.Model):
    tag_name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('accounts.User')
    locations = models.ManyToManyField('locations.Location',
                                       through="LocationTags",
                                       related_name='tags')

    class Meta:
        managed = False
        db_table = 'tags'

    objects = TagManager()

    def to_dict(self):
        dict = {
            "id": self.id,
            "tag_name": self.tag_name,
            "active": self.active,
            "user_id": self.user.id,
        }
        return dict

class LocationTagsManager(models.Manager):
    pass

class LocationTags(models.Model):
    """
    This class represents the join table between Locaations and Tags
    """
    tag = models.ForeignKey(Tag, related_name='tags')
    location = models.ForeignKey('locations.Location', related_name='locations')

    class Meta:
        managed = False
        db_table = "location_tags"

    objects = LocationTagsManager()
