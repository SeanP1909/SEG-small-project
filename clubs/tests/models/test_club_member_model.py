from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import User, Club, ClubMember

# Create your tests here.
class ClubMemberModelTestCase(TestCase):
    """Unit tests of the club member model."""

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_club_member.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_clubs.json',
                'clubs/tests/fixtures/other_club_members.json']

    def setUp(self):
        self.user = User.objects.get(username = 'johndoe')
        self.club = Club.objects.get(name = 'ChessHub')
        self.clubmember = ClubMember.objects.get(
            user = 1,
            club = 1
        )

# Test club member must be a unique entry.
    def test_club_member_must_be_unique(self):
        second_club_member = ClubMember.objects.get(
            user = 3,
            club = 3
        )
        self.clubmember.user = second_club_member.user
        self.clubmember.club = second_club_member.club
        self._assert_club_member_is_invalid()

# Test database reaction upon deleting the content of a foreign key.
    def test_club_member_table_is_deleted_upon_deleting_the_club_model(self):
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
