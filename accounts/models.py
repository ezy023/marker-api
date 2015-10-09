from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class MyAuthBackend(object):
    def authenticate(self, **kwargs):
        if 'access_token' in kwargs:
            user = User.objects.filter(token__token=kwargs.get('access_token')).first()
            if user:
                return user

        elif 'username' in kwargs and 'password' in kwargs:
            username = kwargs.get('username')
            password = kwargs.get('password')
            user = User.objects.get(username=username)
            if user and user.check_password(password):
                return user

        return None

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
