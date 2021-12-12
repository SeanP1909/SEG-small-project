"""Cofiguration of the admin interface for microblogs."""
from django.contrib import admin
from .models import User, Club, ClubMember, ClubOfficer, Tournament, TournamentOfficer, TournamentParticipant, Match
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""
    list_display = [
        'username', 'first_name', 'last_name', 'email', 'is_active',
    ]

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""
    list_display = [
        'name', 'location', 'description',
    ]

@admin.register(ClubMember)
class ClubMemberAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""
    list_display = [
        'user', 'club', 'role'
    ]

@admin.register(ClubOfficer)
class ClubOfficerAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""
    list_display = [
        'user', 'club',
    ]

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for tournaments."""
    list_display = [
        'name', 'capacity', 'description', 'deadline', 'start'
    ]

@admin.register(TournamentOfficer)
class TournamentOfficerAdmin(admin.ModelAdmin):
    """Configuration of admin interface for tournament officers."""
    list_display = [
        'tournament', 'officer'
    ]

@admin.register(TournamentParticipant)
class TournamentParticipantAdmin(admin.ModelAdmin):
    """Configuration of admin interface for tournament participants."""
    list_display = [
        'tournament', 'participant'
    ]

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    """Configuration of admin interface for tournament matches."""
    list_display = [
        'tournament', 'participant_first', 'participant_second', 'result'
    ]