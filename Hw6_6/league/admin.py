from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, PlayerProfile, League, Team,
    Player, Match
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'role', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )

@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'manager', 'league', 'position', 'number')
    list_filter = ('league', 'position')
    search_fields = ('user__email', 'manager__email')


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'season', 'country')
    search_fields = ('name',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league')
    list_filter = ('league',)
    search_fields = ('name',)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'goals', 'assists', 'yellow_cards', 'red_cards')
    list_filter = ('team',)
    search_fields = ('name',)

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'home_score', 'away_score', 'date')
    list_filter = ('date', 'home_team', 'away_team')
    search_fields = ('home_team__name', 'away_team__name')