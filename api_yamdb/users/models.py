from django.contrib.auth.models import AbstractUser
from django.db import models


#  Модель пользователя пока "заглушка"
class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )
    confirmation_code = models.CharField(max_length=200, null=True)
