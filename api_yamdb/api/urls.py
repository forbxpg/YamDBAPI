from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet

router_v1 = DefaultRouter()

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


api_patterns = [
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(api_patterns))
]
