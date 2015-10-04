from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class MyAuthBackend(object):
    def authenticate(self, username=None):
        user = User.objects.get(username=username)
        if user:
            return user
        else:
            user = User.objects.create(username=username)
            return user

    def get_user(self, user_id):
        user = User.objects.get(id=user_id)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'users'

    def to_dict(self):
        dict = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }

        return dict
