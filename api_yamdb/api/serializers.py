from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken

from api.utils import confirmation_code_check, confirmation_code_make
from users.models import User
from reviews.models import Category, Comment, Review, Title, Genre
from users.validators import UsernameValidator


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=User.USERNAME_MAX_LENGTH)
    confirmation_code = serializers.CharField(allow_blank=False)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
            raise ValidationError(
                'Invalid user or confirmation_code!'
            )
        if user.confirmation_code is None:
            raise ValidationError(
                'Confirmation code not requested. Use auth/signup first!'
            )
        if not confirmation_code_check(user, user.confirmation_code):
            raise ValidationError(
                'Confirmation need to be refreshed. Use auth/signup!'
            )
        return {'token': str(AccessToken.for_user(user))}


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=User.EMAIL_MAX_LENGTH)
    username = serializers.CharField(
        max_length=User.USERNAME_MAX_LENGTH,
        validators=[UsernameValidator()]
    )

    def create(self, validated):
        try:
            user = User.objects.get_or_create(**validated)[0]
        except IntegrityError:
            raise ValidationError("username or email already used!")
        user.confirmation_code = confirmation_code_make(user)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'username')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserPatchMeSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        fields = '__all__'
        model = Title


class TitlePatchSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id', 'pub_date', 'title')

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            title_id = self.context.get('view').kwargs.get('title_id')
            if request.user.reviews.filter(title_id=title_id).exists():
                raise ValidationError('Нельзя оставить больше одного отзыва.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review', 'pub_date',)
