from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    AUTHGetTokenView,
    AUTHSignupView,
    UserViewSet,
    titles,
    categories,
    genres
)

app_name = 'api'
API_VER = 'v1'

router = DefaultRouter()
router.register('users', UserViewSet, 'user')

urlpatterns = [
    path(f'{API_VER}/', include(router.urls)),
    path(f'{API_VER}/auth/token/', AUTHGetTokenView.as_view(), name='get_token'),
    path(f'{API_VER}/titles/<int:titles_id>/', titles, name='titles'),
    path(f'{API_VER}/categories/<slug:slug>/', categories, name='categories'),
    path(f'{API_VER}/genres/<slug:slug>/', genres, name='genres'),
    path(f'{API_VER}/auth/signup/', AUTHSignupView.as_view(), name='signup'),
]
