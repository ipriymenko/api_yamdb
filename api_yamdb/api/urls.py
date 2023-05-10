from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    GetTokenView,
    SignupView,
    UserViewSet,
    ReviewViewSet,
)

app_name = 'api'
API_VER = 'v1'

router = DefaultRouter()
router.register('users', UserViewSet, 'user')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

urlpatterns = [
    path(f'{API_VER}/', include(router.urls)),
    path(f'{API_VER}/auth/token/', GetTokenView.as_view(), name='get_token'),
    path(f'{API_VER}/auth/signup/', SignupView.as_view(), name='signup'),
]
