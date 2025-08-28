from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('player', 'Player'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='player')
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.role})"
    
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
class League(TimestampedModel):
    name = models.CharField(max_length=100)
    season = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} ({self.season})"


class PlayerProfile(models.Model):
    POSITION_CHOICES = [
        ('DEF', 'Defender'),
        ('MID', 'Midfielder'),
        ('GK', 'Goalkeeper'),
        ('FWD', 'Forward'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="player_profile")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
    limit_choices_to={'role': 'manager'},related_name="players")
    league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True, blank=True, related_name="players")
    position = models.CharField(max_length=3, choices=POSITION_CHOICES, blank=True)
    number = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} (Manager: {self.manager.email if self.manager else 'None'},League: {self.league.name if self.league else 'None'}, Position: {self.get_position_display()})"
    

class Team(TimestampedModel):
    name = models.CharField(max_length=100)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='teams')

    def __str__(self):
        return self.name

class Player(TimestampedModel):
    profile = models.OneToOneField(PlayerProfile, on_delete= models.CASCADE, related_name='stats')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    yellow_cards = models.PositiveIntegerField(default=0)
    red_cards = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Match(TimestampedModel):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    home_score = models.PositiveIntegerField(default=0)
    away_score = models.PositiveIntegerField(default=0)
    date = models.DateField()

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.date})"