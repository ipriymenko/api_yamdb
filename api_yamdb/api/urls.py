from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (GetTokenView,
                       SignupView,
                       UserViewSet,
                       TitleViewSet,
                       CategoryViewSet,
                       GenreViewSet)


app_name = 'api'
API_VER = 'v1'

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('users', UserViewSet, 'user')

urlpatterns = [
    path(f'{API_VER}/', include(router.urls)),
    path(f'{API_VER}/auth/token/', GetTokenView.as_view(), name='get_token'),
    path(f'{API_VER}/auth/signup/', SignupView.as_view(), name='signup'),
]
