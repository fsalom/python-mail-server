from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class UserDBO(AbstractUser):
    objects = UserManager()

