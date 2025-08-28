from django.urls import path
from .views import (
    RegisterView, ProfileView,
    LogoutView, PostListCreateView, PostDetailView,
    ChangePasswordView, CustomTokenObtainPairView
)
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='user-profile'),

    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/',PostDetailView.as_view(), name = 'post-detail'),
    
]
