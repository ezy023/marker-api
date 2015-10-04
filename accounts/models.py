from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class MyAuthBackend(object):
    def authenticate(self, access_token=None):
        user = User.objects.filter(token__token=access_token).first()
        if user:
            return user
        else:
            raise User.DoesNotExist

    def get_user(self, user_id):
        user = User.objects.get(id=user_id)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = 'username' # consider changing this to the email field

    class Meta:
        db_table = 'users'

    def to_dict(self):
        dict = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }

        return dict
