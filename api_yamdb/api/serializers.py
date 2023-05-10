from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken

from api.utils import confirmation_code_make, confirmation_code_check
from users.models import User
from users.validators import UsernameValidator


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(min_length=1)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
            raise ValidationError('Invalid user or confirmation_code!')
        if user.confirmation_code is None:
            raise ValidationError('Confirmation code not requested. Use auth/signup first!')
        if not confirmation_code_check(user, user.confirmation_code):
            raise ValidationError('Confirmation need to be refreshed. Use auth/signup!')
        return {'token': str(AccessToken.for_user(user))}


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150, validators=[UsernameValidator()])

    def create(self, validated):
        user = User.objects.filter(**validated)
        if not user.exists():
            try:
                user = User.objects.create_user(**validated)
            except IntegrityError:
                raise ValidationError("username or email already used!")
        else:
            user = user.first()
        user.confirmation_code = confirmation_code_make(user)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'username')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class UserPatchMeSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)
