from django.core.management.base import BaseCommand, CommandError
from clubs.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.exclude(username__icontains="admin")
        for user in users:
            user.delete()
