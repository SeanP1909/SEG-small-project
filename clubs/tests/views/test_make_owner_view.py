from django.test import TestCase
from django.urls import reverse
from clubs.models import Club, User, ClubMember
from clubs.tests.helpers import reverse_with_next

class MakeOwnerTestCase(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_clubs.json',]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.target_user = User.objects.get(username = 'janedoe')
        self.club = Club.objects.get(name='Chessy')
        self.url = reverse('make_owner', kwargs={'club_id': self.club.id, 'user_id': self.target_user.id})

    def test_make_owner_url(self):
        self.assertEqual(self.url,f'/{self.club.id}/pass_ownership/{self.target_user.id}/')
