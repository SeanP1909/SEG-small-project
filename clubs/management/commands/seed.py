from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from clubs.models import User

class Command(BaseCommand):
    """The database seeder."""
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')
        self.user = User()

    def handle(self, *args, **options):

        for i in range(100):
            fakeUsername = self.faker.user_name()
            fakeName = self.faker.first_name()
            fakeLastName = self.faker.last_name()
            fakeEmail = self.faker.ascii_email()
            fakeBio = self.faker.text(max_nb_chars = 520)

            User.objects.create(
                username = fakeUsername,
                first_name = fakeName,
                last_name = fakeLastName,
                email = fakeEmail,
                password = 'Password123',
                experience = 'beginner',
                bio = fakeBio
            )
