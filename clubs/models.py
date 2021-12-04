from django.core.validators import RegexValidator, MaxValueValidator
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
        unique=True,
        validators=[
            RegexValidator(
                regex = r'^\w{3,}$',
                message = 'The username must contain at least three character of any kind!'
                )
        ]
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

# Create the Club model.
class Club(models.Model):
    name = models.CharField(
        max_length = 50,
        unique = True,
        validators=[
            RegexValidator(
                regex = r'^\w{3,}$',
                message = 'The name of the club must contain at least three character of any kind!'
                )
        ]
    )
    location = models.CharField(max_length = 100)
    description = models.CharField(max_length = 520, blank = True)

# Create the Club member model.
class ClubMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    class Meta():
        unique_together = ('user', 'club',)

# Create the Club officer model.
class ClubOfficer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    class Meta():
        unique_together = ('user', 'club',)

# Create the Club owner model.
class ClubOwner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    class Meta():
        unique_together = ('user', 'club',)