from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import AUTHGetTokenView

app_name = 'api'
API_VER = 'v1'

router = DefaultRouter()

urlpatterns = [
    path(f'{API_VER}/', include(router.urls)),
    path(f'{API_VER}/auth/token/', AUTHGetTokenView.as_view(), name='get_token'),
]