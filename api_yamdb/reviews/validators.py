from django.utils import timezone
from rest_framework.exceptions import ValidationError


def year_validator(value):
    if 0 < value <= timezone.now().year:
        raise ValidationError(
            f'{value} - неверный формат года!'
        )
