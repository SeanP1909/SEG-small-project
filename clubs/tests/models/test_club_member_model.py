from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import User, Club, ClubMember

# Create your tests here.
class ClubMemberModelTestCase(TestCase):
    """Unit tests of the club member model."""

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_clubmember.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_clubs.json',
                'clubs/tests/fixtures/other_clubmembers.json']

    def setUp(self):
        self.user = User.objects.get(username = 'johndoe')
        self.club = Club.objects.get(name = 'ChessHub')
        self.clubmember = ClubMember.objects.get(
            username = 'johndoe',
            name = 'ChessHub'
        )

# Test club member must be a unique entry.
    def test_club_member_must_be_unique(self):
        second_club_member = ClubMember.objects.get(
            username='janedoe',
            name='Chessy')
        self.clubmember = second_club_member
        self._assert_club_member_is_invalid()

# Test 
    def test_club_member_Table_is_deleted_upon_deleting_the_club_model(self):
        self.club.delete()
        with self.assertRaises(ClubMember.DoesNotExist):
            ClubMember.objects.get(pk = self.clubmember.pk)
        self._assert_club_member_is_invalid()

    def test_club_member_table_is_deleted_upon_deleting_the_user_model(self):
        self.user.delete()
        with self.assertRaises(ClubMember.DoesNotExist):
            ClubMember.objects.get(pk = self.clubmember.pk)
        self._assert_club_member_is_invalid()

# Test case assertions
    def _assert_club_member_is_valid(self):
        try:
            self.clubmember.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_club_member_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.clubmember.full_clean()