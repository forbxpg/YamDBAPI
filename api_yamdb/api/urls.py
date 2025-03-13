"""API URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


router_v1 = DefaultRouter()

router_v1.register('users', views.UsersViewSet, basename='users')
router_v1.register('categories', views.CategoryViewSet, basename='categories')
router_v1.register('genres', views.GenreViewSet, basename='genres')
router_v1.register('titles', views.TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

auth_urls = [
    path('signup/', views.APISignUpView.as_view(), name='signup'),
    path('token/', views.TokenObtainView.as_view(), name='token_obtain_pair'),
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/users/me/', views.APIMeView.as_view(), name='me'),
    path('v1/', include(router_v1.urls)),
]
