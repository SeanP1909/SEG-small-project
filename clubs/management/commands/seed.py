from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from faker import Faker
from clubs.models import User, Club, ClubMember, ClubOfficer

class Command(BaseCommand):
    """The database seeder."""
    PASSWORD = make_password("Password123", hasher='default')

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.clubs = []

        User.objects.create(
            username = "clubber",
            first_name = "Clubber",
            last_name = "McClubberson",
            email = "clubber@example.com",
            password = Command.PASSWORD,
            experience = 'professional',
            bio = "I am Clubber, the CEO of McClubberson & Son."
        )


        for i in range(10):
            fakeName = self.faker.company()
            fakeLocation = self.faker.address()
            fakeDescription = self.faker.text(max_nb_chars = 520)

            self.club = Club.objects.create(
                owner = User.objects.get(username = "clubber"),
                name = fakeName,
                location = fakeLocation,
                description = fakeDescription,
            )

            self.clubs.append(self.club)

        n = 0

        for i in range(1, 101):
            fakeUsername = self.faker.user_name()
            fakeName = self.faker.first_name()
            fakeLastName = self.faker.last_name()
            fakeEmail = self.faker.ascii_email()
            fakeBio = self.faker.text(max_nb_chars = 520)

            self.user = User.objects.create(
                username = fakeUsername,
                first_name = fakeName,
                last_name = fakeLastName,
                email = fakeEmail,
                password = Command.PASSWORD,
                experience = 'beginner',
                bio = fakeBio
            )

            if(i % 10 == 0):
                ClubOfficer.objects.create(
                    user = self.user,
                    club = self.clubs[n]
                )
                n+=1
            else:
                ClubMember.objects.create(
                    user = self.user,
                    club = self.clubs[n]
                )
