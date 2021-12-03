"""Cofiguration of the admin interface for microblogs."""
from django.contrib import admin
from .models import User, Club
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
