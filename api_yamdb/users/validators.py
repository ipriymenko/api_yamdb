from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.exceptions import ValidationError


class UsernameValidator:
    message = "can't be equal to 'me' or contain special symbols!"
    code = 'invalid'
    unicode_validator = UnicodeUsernameValidator()

    def __call__(self, value):
        if str(value).strip().lower() == 'me':
            raise ValidationError(self.message, code=self.code)
        else:
            self.unicode_validator(value)
