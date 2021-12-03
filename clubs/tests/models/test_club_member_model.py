from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club

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
        self.clubmember = ClubMember.objects.get(
            username = 'johndoe',
            name = 'ChessHub'
        )

# Test
    def test_club_member_must_be_unique(self):
        second_club_member = ClubMember.objects.get(
            username='janedoe',
            name='Chessy')
        if self.clubmember.username = second_club_member.username && self.clubmember.name = second_club_member.name:
            self._assert_club_member_is_invalid()

# Test 
        

# Test case assertions
    def _assert_club_member_is_valid(self):
        try:
            self.clubmember.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_club_member_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.clubmember.full_clean()