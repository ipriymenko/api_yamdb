from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

from api.utils import confirmation_code_make, confirmation_code_check
from users.models import User


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(min_length=1)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
            raise ValidationError('Invalid user or confirmation_code!')
        if user.confirmation_code is None or confirmation_code_check(user, user.confirmation_code):
            raise ValidationError('Confirmation code not requested. Use auth/signup first!')
        return {'token': str(RefreshToken.for_user(user))}


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=254)
    username = serializers.CharField(max_length=150)

    def create(self, validated):
        user = User.objects.filter(**validated)
        if not user.exists():
            try:
                user = User.objects.create_user(**validated)
            except IntegrityError:
                raise ValidationError("Can't signup: username or email already used!")
        else:
            user = user.first()
        user.confirmation_code = confirmation_code_make(user)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'username')
