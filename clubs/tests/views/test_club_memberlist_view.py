from django.test import TestCase
from django.urls import reverse
from clubs.models import Club, User
from clubs.tests.helpers import reverse_with_next

class ShowClubMemberListTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_clubs.json',]

    def setUp(self):
        self.user = User.objects.get(username='janedoe')
        self.target_club = Club.objects.get(name='Chessy')
        self.url = reverse('club_member_list', kwargs={'club_id': self.target_club.id})

    def test_show_club_url(self):
        self.assertEqual(self.url,f'/club/{self.target_club.id}/memberlist')

    def test_get_show_club_with_invalid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('club_member_list', kwargs={'club_id': self.user.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
