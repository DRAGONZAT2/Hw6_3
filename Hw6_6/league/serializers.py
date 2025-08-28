from rest_framework import serializers
from .models import CustomUser, PlayerProfile, League, Team, Player, Match
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'role', 'date_joined']

class PlayerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    manager_email = serializers.CharField(source='manager.email', read_only=True)
    league_name = serializers.CharField(source='league.name', read_only=True)

    class Meta:
        model = PlayerProfile
        fields = ['id', 'user', 'manager', 'manager_email', 'league', 'league_name', 'position', 'number']

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    league_name = serializers.CharField(source='league.name', read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'league', 'league_name', 'created_at', 'updated_at']


class PlayerSerializer(serializers.ModelSerializer):
    profile_email = serializers.CharField(source='profile.user.email', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = Player
        fields = ['id', 'profile', 'profile_email', 'team', 'team_name', 'goals', 'assists', 'yellow_cards', 'red_cards', 'created_at', 'updated_at']


class MatchSerializer(serializers.ModelSerializer):
    home_team_name = serializers.CharField(source='home_team.name', read_only=True)
    away_team_name = serializers.CharField(source='away_team.name', read_only=True)

    class Meta:
        model = Match
        fields = ['id', 'home_team', 'home_team_name', 'away_team', 'away_team_name', 'home_score', 'away_score', 'date', 'created_at', 'updated_at']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['id'] = user.id
        token['role'] = user.role
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators = [validate_password])
    new_password2 = serializers.CharField(required = True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Passwords are not matched."})
        return attrs
