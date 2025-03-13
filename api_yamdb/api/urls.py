"""API URLs."""
from django.urls import include, path

from .routers import router_v1
from .views import APIMeView, APISignUpView, TokenObtainView


auth_urls = [
    path('signup/', APISignUpView.as_view(), name='signup'),
    path('token/', TokenObtainView.as_view(), name='token_obtain_pair'),
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/users/me/', APIMeView.as_view(), name='me'),
    path('v1/', include(router_v1.urls)),
]
