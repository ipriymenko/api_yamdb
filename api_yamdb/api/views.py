from smtplib import SMTPException
from rest_framework import status

from django.conf import settings
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import TitleFilter
from api.exceptions import APIConfirmationEmailSendError
from api.generics import CreateListDestroyGeneric
from api.serializers import (
    GetTokenSerializer,
    SignupSerializer,
    UserSerializer,
    UserPatchMeSerializer,
    CategorySerializer,
    TitleGetSerializer,
    TitlePatchSerializer,
    GenreSerializer,
    ReviewSerializer, CommentSerializer
)
from api.permissions import IsAdmin, IsReadOnly, IsStaffOrAuthorOrReadOnly
from reviews.models import Category, Review, Title, Genre
from users.models import User


class GetTokenView(TokenViewBase):
    serializer_class = GetTokenSerializer


class CategoryViewSet(CreateListDestroyGeneric):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin | IsReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdmin | IsReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitlePatchSerializer


class GenreViewSet(CreateListDestroyGeneric):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdmin | IsReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class SignupView(CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        try:
            user.email_user(
                subject='Код подтверждения',
                message=f'Ваш секретный код: {user.confirmation_code}',
                from_email=settings.EMAIL_SENDER.get('signup'),
                fail_silently=False,
            )
        except SMTPException:
            raise APIConfirmationEmailSendError(
                'Не удалось отправить email с кодом подтверждения',
                status.HTTP_503_SERVICE_UNAVAILABLE
            )
        return Response(serializer.validated_data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    http_method_names = ['get', 'delete', 'patch', 'post']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = self.request.user
        if request.method == 'PATCH':
            serializer = UserPatchMeSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = self.get_serializer(user)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsStaffOrAuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsStaffOrAuthorOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
