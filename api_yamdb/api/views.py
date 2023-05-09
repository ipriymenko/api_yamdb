from rest_framework import viewsets, mixins
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from smtplib import SMTPException

from api.exceptions import APIConfirmationEmailSendError
from api.serializers import GetTokenSerializer, SignupSerializer


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
