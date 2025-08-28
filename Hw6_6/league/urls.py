from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, PlayerProfileViewSet, LeagueViewSet,
    TeamViewSet, PlayerViewSet, MatchViewSet
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', PlayerProfileViewSet)
router.register(r'leagues', LeagueViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'matches', MatchViewSet)


urlpatterns = [
    path('', include(router.urls)),
    
    
    path('auth/jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
]