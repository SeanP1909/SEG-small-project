from django.core.management.base import BaseCommand, CommandError
from clubs.models import User, Club

class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.exclude(username__icontains="admin")
        for user in users:
            user.delete()

        clubs = Club.objects.all()
        for club in clubs:
            club.delete()
