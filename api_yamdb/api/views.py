from rest_framework import viewsets, mixins, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from smtplib import SMTPException

from reviews.models import Category, Title, Genre
from api.exceptions import APIConfirmationEmailSendError
from api.permissions import IsAdmin, IsReadOnly
from api.serializers import GetTokenSerializer, SignupSerializer, UserSerializer, UserPatchMeSerializer, CategorySerializer, TitleSerializer, GenreSerializer
from users.models import User


class GetTokenView(TokenViewBase):
    serializer_class = GetTokenSerializer


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdmin | IsReadOnly]
    authentication_classes = ()


class TitleViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = (permissions.AllowAny,)
    pagination_class = PageNumberPagination
    authentication_classes = ()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (permissions.AllowAny,)
    authentication_classes = ()


class SignupView(CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        try:
            user.email_user(
                subject='Код подтверждения',
                message=str(user.confirmation_code),
                from_email='registration@example.com',
                fail_silently=False,
            )
        except SMTPException:
            raise APIConfirmationEmailSendError('Не удалось отправить email с кодом подтверждения', 503)
        return Response(serializer.validated_data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
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
            serializer = UserPatchMeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = self.get_serializer(user)
        return Response(serializer.data)
