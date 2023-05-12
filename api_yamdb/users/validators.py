from django.core.validators import RegexValidator


class UsernameValidator(RegexValidator):
    regex = r'^(?!me$|ME$)[\w.@+-]+\Z'
    message = "can't be equal to 'me' or contain special symbols!"
    code = 'invalid'
