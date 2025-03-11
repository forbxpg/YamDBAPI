"""API URLs."""
from django.urls import include, path

from .routers import router_v1

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
