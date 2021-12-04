from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import User, Club, ClubOwner

# Create your tests here.
class ClubOwnerModelTestCase(TestCase):
    """Unit tests of the club owner model."""

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_club_owner.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_clubs.json',
                'clubs/tests/fixtures/other_club_owners.json']

    def setUp(self):
        self.user = User.objects.get(username = 'johndoe')
        self.club = Club.objects.get(name = 'ChessHub')
        self.clubowner = ClubOwner.objects.get(
            user = 1,
            club = 1
        )

# Test club owner must be a unique entry.
    def test_club_owner_must_be_unique(self):
        second_club_owner = ClubOwner.objects.get(
            user = 4,
            club = 4   
        )
        self.clubowner.user = second_club_owner.user
        self.clubowner.club = second_club_owner.club
        self._assert_club_owner_is_invalid()

# Test database reaction upon deleting the content of a foreign key.
    def test_club_owner_table_is_deleted_upon_deleting_the_club_model(self):
        self.club.delete()
        with self.assertRaises(ClubOwner.DoesNotExist):
            ClubOwner.objects.get(pk = self.clubowner.pk)
        self._assert_club_owner_is_invalid()

    def test_club_owner_table_is_deleted_upon_deleting_the_user_model(self):
        self.user.delete()
        with self.assertRaises(ClubOwner.DoesNotExist):
            ClubOwner.objects.get(pk = self.clubowner.pk)
        self._assert_club_owner_is_invalid()

# Test case assertions
    def _assert_club_owner_is_valid(self):
        try:
            self.clubowner.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_club_owner_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.clubowner.full_clean()