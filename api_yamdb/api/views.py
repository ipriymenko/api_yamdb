from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from smtplib import SMTPException
from django.http import HttpResponse

from api.exceptions import APIConfirmationEmailSendError
from api.permissions import IsOwnerOrHasAdminRole
from api.serializers import GetTokenSerializer, SignupSerializer, UserSerializer, UserPatchMeSerializer
from users.models import User


class AUTHGetTokenView(TokenViewBase):
    serializer_class = GetTokenSerializer


class AUTHSignupView(CreateAPIView):
    serializer_class = SignupSerializer
    authentication_classes = ()
    permission_classes = ()

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

    permission_classes = (IsOwnerOrHasAdminRole,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    # def update(self, request, *args, **kwargs):
    #     raise MethodNotAllowed(request.method)

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
