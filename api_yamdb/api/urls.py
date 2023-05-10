from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (AUTHGetTokenView,
                       TitleViewSet,
                       CategoryViewSet,
                       GenreViewSet)


app_name = 'api'
API_VER = 'v1'

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')

urlpatterns = [
    path(f'{API_VER}/', include(router.urls)),
    path(f'{API_VER}/auth/token/', AUTHGetTokenView.as_view(), name='get_token'),
]
