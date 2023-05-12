from django.utils import timezone
from rest_framework.exceptions import ValidationError


def year_validator(value):
    if value > timezone.now().year:
        raise ValidationError(
            f'{value} - неверный формат года!'
        )
