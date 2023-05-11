from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import UsernameValidator


class User(AbstractUser):
    class UserRoles(models.TextChoices):
        USER = 'user', 'пользователь'
        ADMIN = 'admin', 'администратор'
        MODERATOR = 'moderator', 'модератор'

    username_validator = UsernameValidator
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )
    email = models.EmailField(blank=False, null=False, unique=True, max_length=254)
    role = models.CharField(max_length=10, choices=UserRoles.choices, default=UserRoles.USER)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
