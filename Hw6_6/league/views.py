from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import CustomUser, PlayerProfile, League, Team, Player, Match
from .serializers import (
    UserSerializer, PlayerProfileSerializer, LeagueSerializer, 
    TeamSerializer, PlayerSerializer, MatchSerializer
)
from .permissions import IsAdmin, IsManagerOrAdmin


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    pagination_class = StandardPagination


class PlayerProfileViewSet(viewsets.ModelViewSet):
    queryset = PlayerProfile.objects.select_related('user', 'manager', 'league').all()
    serializer_class = PlayerProfileSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['league', 'manager']
    search_fields = ['user__email']
    ordering_fields = ['number']
    pagination_class = StandardPagination



class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    permission_classes = [IsAdmin]
    pagination_class = StandardPagination


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['league']
    search_fields = ['name']
    ordering_fields = ['name']
    pagination_class = StandardPagination


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.select_related('profile', 'team').all()
    serializer_class = PlayerSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['team', 'profile']
    search_fields = ['profile__user__email']
    ordering_fields = ['goals', 'assists']
    pagination_class = StandardPagination


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.select_related('home_team', 'away_team').all()
    serializer_class = MatchSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['home_team', 'away_team', 'date']
    ordering_fields = ['date']
    pagination_class = StandardPagination