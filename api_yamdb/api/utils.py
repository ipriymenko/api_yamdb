from django.contrib.auth.tokens import default_token_generator

from users.models import User


def confirmation_code_make(user: User) -> str:
    return default_token_generator.make_token(user)


def confirmation_code_check(user: User, confirmation_code: str) -> bool:
    return default_token_generator.chek_token(user, confirmation_code)
