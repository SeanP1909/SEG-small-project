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
    def test_population_is_a_positive_integer_number(self):
        self.club.population=2
        self._assert_club_is_valid()

    def test_population_is_not_negative_number(self):
        self.club.population=-2
        self._assert_club_is_invalid()

    def test_population_is_not_empty(self):
        self.club.population=''
        self._assert_club_is_invalid()

    def test_population_is_less_than_100_people(self):
        self.club.population=99
        self._assert_club_is_valid()

    def test_population_is_no_more_than_100_people(self):
        self.club.population=101
        self._assert_club_is_invalid()

# Location tests.
    def test_location_is_not_blank(self):
        self.club.location=''
        self._assert_club_is_invalid()

    def test_location_is_not_unique(self):
        second_club = Club.objects.get(name='Hubby')
        self.club.location = second_club.location
        self._assert_club_is_valid()

    def test_location_can_have_less_than_100_characters(self):
        self.club.location='x' * 100
        self._assert_club_is_valid()

    def test_location_cannot_have_more_than_50_characters(self):
        self.club.location='x' * 101
        self._assert_club_is_invalid()

# Description tests.
    def test_description_can_be_blank(self):
        self.club.description=''
        self._assert_club_is_valid()

    def test_description_may_not_be_unique(self):
        second_club = Club.objects.get(name='Avalon')
        self.club.description = second_club.description
        self._assert_club_is_valid()

    def test_description_may_have_520_chars(self):
        self.club.bio='x' * 520
        self._assert_club_is_valid()

    def test_description_cannot_have_over_520_chars(self):
        self.club.description='x' * 521
        self._assert_club_is_invalid()

# Test case assertions
    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()