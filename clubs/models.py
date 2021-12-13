from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from libgravatar import Gravatar
from .helpers import experienceChoices, match_result_choices

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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(
        max_length = 50,
        unique = True,
        validators=[
            RegexValidator(
                regex = r'^.{3,}$',
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
    role = models.CharField(max_length = 3, choices = [('MEM','Member'),('OFF','Officer'),('OWN','Owner')], default = 'MEM')
    class Meta():
        unique_together = ('user', 'club',)

# Create the Club officer model.
class ClubOfficer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    class Meta():
        unique_together = ('user', 'club',)

class Tournament(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 520, blank = True)
    capacity = models.IntegerField(validators = [MinValueValidator(2), MaxValueValidator(96)], blank = False)
    deadline = models.DateField(blank = False)
    start = models.DateField(blank = False)
    finished = models.BooleanField(default = False)
    
    def __str__(self):
        return f"{self.name}, Start Date: {self.start}"

class TournamentOfficer(models.Model):
    officer = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    class Meta():
        unique_together = ('officer', 'tournament',)

class TournamentParticipant(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    class Meta():
        unique_together = ('participant', 'tournament',)

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    participant_first = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participant_first_match')
    participant_second = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participant_second_match')
    start = models.DateField(blank = False)
    #TODO: Make result as emun with values (first/second/draw)
    result = models.CharField(max_length = 10, choices=match_result_choices(), blank = False)