from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import User, Club, ClubOfficer

# Create your tests here.
class ClubOfficerModelTestCase(TestCase):
    """Unit tests of the club officer model."""

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_club_officer.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_clubs.json',
                'clubs/tests/fixtures/other_club_officers.json']

    def setUp(self):
        self.user = User.objects.get(username = 'johndoe')
        self.club = Club.objects.get(name = 'ChessHub')
        self.clubofficer = ClubOfficer.objects.get(
            user = 1,
            club = 1
        )

# Test club officer must be a unique entry.
    def test_club_officer_must_be_unique(self):
        second_club_officer = ClubOfficer.objects.get(
            user = 2,
            club = 2
        )
        self.clubofficer.user = second_club_officer.user
        self.clubofficer.club = second_club_officer.club
        self._assert_club_officer_is_invalid()

# Test database reaction upon deleting the content of a foreign key.
    def test_club_officer_table_is_deleted_upon_deleting_the_club_model(self):
        self.club.delete()
        with self.assertRaises(ClubOfficer.DoesNotExist):
            ClubOfficer.objects.get(pk = self.clubofficer.pk)
        self._assert_club_officer_is_invalid()

    def test_club_officer_table_is_deleted_upon_deleting_the_user_model(self):
        self.user.delete()
        with self.assertRaises(ClubOfficer.DoesNotExist):
            ClubOfficer.objects.get(pk = self.clubofficer.pk)
        self._assert_club_officer_is_invalid()

# Test case assertions
    def _assert_club_officer_is_valid(self):
        try:
            self.clubofficer.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_club_officer_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.clubofficer.full_clean()
