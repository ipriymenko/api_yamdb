from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenViewBase

from api.serializers import GetTokenSerializer


class AUTHGetTokenView(TokenViewBase):
    serializer_class = GetTokenSerializer
