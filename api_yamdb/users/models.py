from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import UsernameValidator


class User(AbstractUser):
    USERNAME_MAX_LENGTH = 150
    EMAIL_MAX_LENGTH = 254
    CONFIRMATION_CODE_MAX_LENGTH = 200
    ROLE_MAX_LENGTH = 10

    class UserRoles(models.TextChoices):
        USER = 'user', 'пользователь'
        ADMIN = 'admin', 'администратор'
        MODERATOR = 'moderator', 'модератор'

    username_validator = UsernameValidator
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография',
    )
    confirmation_code = models.CharField(
        max_length=CONFIRMATION_CODE_MAX_LENGTH,
        null=True,
        verbose_name='Код подтверждения',
    )
    email = models.EmailField(
        blank=False,
        null=False,
        unique=True,
        verbose_name='Емейл',
    )
    role = models.CharField(
        max_length=ROLE_MAX_LENGTH,
        choices=UserRoles.choices,
        default=UserRoles.USER,
        verbose_name='Роль'
    )

    @property
    def is_admin(self):
        return self.is_superuser or self.role == User.UserRoles.ADMIN

    @property
    def is_moderator(self):
        return self.role == User.UserRoles.MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.get_username()
