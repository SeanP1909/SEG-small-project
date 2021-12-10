from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import User, Club

# Create your tests here.
class ClubModelTestCase(TestCase):
    """Unit tests of the club model."""

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_clubs.json',]

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(username='johndoe')
        self.club = Club.objects.get(name="ChessHub")

# Name tests.
    def test_name_is_not_blank(self):
        self.club.name=''
        self._assert_club_is_invalid()

    def test_name_must_be_unique(self):
        second_club=Club.objects.get(name="Chessy")
        self.club.name=second_club.name
        self._assert_club_is_invalid()

    def test_name_contains_whitespace(self):
        self.club.name = "Chess Hub"
        self._assert_club_is_valid()

    def test_name_contains_number(self):
        self.club.name = "Chess4Hub"
        self._assert_club_is_valid()

    def test_name_can_have_less_than_50_characters(self):
        self.club.name='x' * 50
        self._assert_club_is_valid()

    def test_name_cannot_have_more_than_50_characters(self):
        self.club.name='x' * 51
        self._assert_club_is_invalid()

# Location tests.
    def test_location_is_not_blank(self):
        self.club.location=''
        self._assert_club_is_invalid()

    def test_location_is_not_unique(self):
        second_club=Club.objects.get(name="Chessy")
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

    def test_description_does_not_need_to_be_unique(self):
        second_club=Club.objects.get(name="Chessy")
        self.club.description = second_club.description
        self._assert_club_is_valid()

    def test_description_may_have_520_chars(self):
        self.club.bio='x' * 520
        self._assert_club_is_valid()

    def test_description_cannot_have_over_520_chars(self):
        self.club.description='x' * 521
        self._assert_club_is_invalid()

# Test club ownership
    def test_user_can_own_multiple_clubs(self):
        second_club=Club.objects.get(name="Chessy")
        self.club.owner = second_club.owner
        self._assert_club_is_valid()

    def test_club_cannot_have_no_owner(self):
        self.club.owner = None
        self._assert_club_is_invalid()

# Test case assertions
    def _assert_club_is_valid(self):
        try:
            self.club.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.club.full_clean()
