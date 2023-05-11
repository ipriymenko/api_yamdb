from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (GetTokenView,
                       SignupView,
                       UserViewSet,
                       ReviewViewSet,
                       TitleViewSet,
                       CategoryViewSet,
                       CommentViewSet,
                       GenreViewSet)


app_name = 'api'
API_VER = 'v1'

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('users', UserViewSet, 'user')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path(f'{API_VER}/', include(router.urls)),
    path(f'{API_VER}/auth/token/', GetTokenView.as_view(), name='get_token'),
    path(f'{API_VER}/auth/signup/', SignupView.as_view(), name='signup'),
]
