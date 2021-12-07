from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from clubs.forms import SignUpForm, ClubCreationForm
from clubs.models import User, Club
from clubs.tests.helpers import LogInTester

class ClubCreatorTestCase(TestCase, LogInTester):
    """Tests the Sign Up View"""

    fixtures = ['clubs/tests/fixtures/default_user.json',]

    def setUp(self):
        self.url = reverse('club_creator')
        self.user = User.objects.get(username='johndoe')
        self.form_input = {
            'name': 'Chesser',
            'location': 'London',
            'description': 'This is a chess club.',
        }

    def test_club_creator_url(self):
        self.assertEqual(self.url, '/club_creator/')

    def test_get_club_creator(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_creator.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ClubCreationForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_club_creation(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = Club.objects.count()
        self.form_input ['name'] = 'na'
        response = self.client.post(self.url, self.form_input)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_creator.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ClubCreationForm))
        self.assertTrue(form.is_bound)

    def test_successful_club_creation(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = Club.objects.count()
        response = self.client.post(self.url, self.form_input, follow = True)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count + 1)
        club = Club.objects.get(name = 'Chesser')
        response_url = reverse('show_club', kwargs={'club_id': club.id})
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'show_club.html')
        self.assertEqual(club.location, 'London')
        self.assertEqual(club.description, 'This is a chess club.')
