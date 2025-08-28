
from django.shortcuts import render
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, CustomTokenObtainPairView, ProfileView,
    ChangePasswordView, LogoutView, NoteViewSet
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register('notes', NoteViewSet, basename='notes')

def login_view(request):
    return render(request, "login.html")

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name= 'refresh_token'),
    path('profile/', ProfileView.as_view(), name= 'profile'),
    path('change-password/', ChangePasswordView.as_view(),name ='change_password'),
    path('logout/', LogoutView.as_view(), name= 'logout'),
    path('', include(router.urls)), 
    path("auth/", include("social_django.urls"), name="social"),
    path("login/", login_view, name='login'),
]