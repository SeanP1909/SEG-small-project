from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from libgravatar import Gravatar

# Create your models here.

# Create the User model
class User(AbstractUser):
    EXPERIENCE_LEVELS = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("master", "Master"),
        ("professional", "Professional")
    )

    username = models.CharField(
        max_length = 30,
        unique=True
    )
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField(unique = True, blank = False)
    experience = models.CharField(max_length=12, choices=EXPERIENCE_LEVELS, default='beginner')
    bio = models.CharField(max_length = 520, blank = True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar"""
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to the user's miniature gravatar."""
        return self.gravatar(size=60)

# Create the Club model.
class Club():
    name = models.CharField(
        max_length = 50,
        unique = True
        validators=[
            RegexValidator(
                regex = r'^\w{3,}$',
                message = 'The name of the club must contain at least three character of any kind!'
                )
        ]
    )
    population = models.IntegerField()
    location = models.CharField(max_length = 50)
    description = models.CharField(max_length = 520, blank = True)
    mission_statement = models.CharField(max_length = 520, blank = True)

    def get_name(self):
        return self.name

    def get_population(self):
        return self.population
    
    def get_location(self):
        return self.location

    def get_description(self):
        return self.description

    def get_mission_statement(self):
        return self.mission_statement
