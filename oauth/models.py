import uuid

from django.db import models

class TokenManager(models.Manager):
    pass

class Token(models.Model):
    token = models.CharField(max_length=255)
    user = models.ForeignKey('accounts.User')

    objects = TokenManager()

    class Meta:
        db_table = 'oauth_tokens'

    @staticmethod
    def create_token():
        new_uuid = str(uuid.uuid1())
        token = Token(token=new_uuid)
        return token
