from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
            raise ValidationError('Invalid user or confirmation_code!')
        return {'token': str(RefreshToken.for_user(user))}
