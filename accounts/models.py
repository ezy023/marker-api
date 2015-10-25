from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class MyAuthBackend(object):
    def authenticate(self, **kwargs):
        if 'access_token' in kwargs:
            user = User.objects.filter(token__token=kwargs.get('access_token')).first()
            if user:
                return user

        elif 'email' in kwargs and 'password' in kwargs:
            email = kwargs.get('email')
            password = kwargs.get('password')
            user = User.objects.get(email=email)
            if user and user.check_password(password):
                return user

        return None

    def get_user(self, user_id):
        user = User.objects.get(id=user_id)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    USERNAME_FIELD = "email"

    class Meta:
        db_table = 'users'

    def to_dict(self):
        dict = {
            'id': self.id,
            'email': self.email,
        }

        return dict
