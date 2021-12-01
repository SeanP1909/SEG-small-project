from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from libgravatar import Gravatar
from .helpers import experienceChoices

# Create your models here.

# Create the User model
class User(AbstractUser):
    #User model atributes.
    username = models.CharField(
        max_length = 30,
        unique=True
    )
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField(unique = True, blank = False)
    experience = models.CharField(max_length=12, choices=experienceChoices())
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
