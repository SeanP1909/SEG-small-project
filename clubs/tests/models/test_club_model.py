from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club

# Create your tests here.
class ClubModelTestCase(TestCase):
    """Unit tests of the club model."""

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(username = 'johndoe')