from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GetTokenView,
    GenreViewSet,
    ReviewViewSet,
    SignupView,
    TitleViewSet,
    UserViewSet,
)

app_name = 'api'

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

auth_urls = [
    path('token/', GetTokenView.as_view(), name='get_token'),
    path('signup/', SignupView.as_view(), name='signup'),
]

api_v1 = [
    path('', include(router.urls)),
    path('auth/', include(auth_urls)),
]

urlpatterns = [
    path('v1/', include(api_v1)),
]
