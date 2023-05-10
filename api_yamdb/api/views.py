from rest_framework import viewsets, mixins, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenViewBase

from api.serializers import GetTokenSerializer
from reviews.models import Category, Title, Genre
from .serializers import CategorySerializer, TitleSerializer, GenreSerializer
# from .permission import IsAdmin, IsReadOnly


class AUTHGetTokenView(TokenViewBase):
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
    # permission_classes = [IsAdmin | IsReadOnly]
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
