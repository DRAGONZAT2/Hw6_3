from rest_framework import generics, viewsets, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser, Link
from .serializers import RegisterSerializer, UserSerializer, LinkSerializer
from .permissions import IsOwnerOrAdmin
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404, redirect

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user

class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Link.objects.all()
        return Link.objects.filter(is_public=True) | Link.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

@api_view(['GET'])
def redirect_short_link(request, short_code):
    link = get_object_or_404(Link, short_code=short_code, is_public=True)
    return redirect(link.target_url)