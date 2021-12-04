from django.test import TestCase
from django.urls import reverse
from clubs.models import Club, User
from clubs.tests.helpers import reverse_with_next

class ShowClubTest(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/other_clubs.json',
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.target_club = Club.objects.get(name='ChessHub')
        self.url = reverse('show_club', kwargs={'club_id': self.target_club.id})

    def test_show_club_url(self):
        self.assertEqual(self.url,f'/club/{self.target_club.id}')

    def test_get_show_club_with_valid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_club.html')
        self.assertContains(response, "ChessHub")

    def test_get_show_club_with_invalid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('show_club', kwargs={'club_id': self.user.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
