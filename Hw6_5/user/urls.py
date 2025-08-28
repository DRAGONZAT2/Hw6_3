from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, ProfileView, LinkViewSet, redirect_short_link
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('links', LinkViewSet, basename='links')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('auth/', include('social_django.urls', namespace='social')),  
    path('r/<str:short_code>/', redirect_short_link, name='redirect_link'),
    path('', include(router.urls)),
]