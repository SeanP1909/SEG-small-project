from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club

# Create your tests here.
class ClubModelTestCase(TestCase):
    """Unit tests of the club model."""

    fixtures = ['clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_clubs.json']

    def setUp(self):
        self.club = Club.objects.get(name = 'ChessHub')

# Name tests.
    def test_name_is_not_blank(self):
        self.club.name=''
        self._assert_club_is_invalid()

    def test_name_is_not_unique(self):
        second_club = Club.objects.get(name='Chessy')
        self.club.name = second_club.name
        self._assert_club_is_valid()

    def test_name_can_have_less_than_50_characters(self):
        self.club.name='x' * 50
        self._assert_club_is_valid()

    def test_name_cannot_have_more_than_50_characters(self):
        self.club.name='x' * 51
        self._assert_club_is_invalid()

# Population tests.
    def 