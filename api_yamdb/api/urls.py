"""API URLs."""
from django.urls import include, path

from .routers import router_v1
from .views import APISignUpView, TokenObtainView

auth_patterns = [
    path('auth/signup/', APISignUpView.as_view(), name='signup'),
    path('auth/token/', TokenObtainView.as_view(), name='token_obtain_pair'),
]
urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include(auth_patterns))
]
