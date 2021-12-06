from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from clubs.forms import UpdateForm
from clubs.models import User
from clubs.tests.helpers import LogInTester

class UpdateViewTestCase(TestCase, LogInTester):

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.url = reverse('profile')
        self.form_input = {
            'first_name': 'john',
            'last_name': 'doe',
            'username': 'johndoe',
            'email': 'johndoe@example.org',
            'experience': 'beginner',
            'bio': 'Just a bio',

        }

    def test_profile_view_url(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertEqual(self.url, '/profile/')

    def test_get_profile_view(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UpdateForm))
        self.assertFalse(form.is_bound)


    def test_unsuccessful_update_profile(self):
        self.client.login(username=self.user.username, password='Password123')
        temp = self.user.username
        self.form_input ['username'] = 'us'
        self.assertFalse(temp == 'us')
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UpdateForm))
        self.assertTrue(form.is_bound)


    def test_successful_update_profile(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input ['username'] = 'user1'
        response = self.client.post(self.url, self.form_input, follow = True)
        self.assertTemplateUsed(response, 'profile.html')
        user = User.objects.get(username = 'user1')
        self.assertEqual(user.first_name, 'john')
        self.assertEqual(user.last_name, 'doe')
        self.assertEqual(user.email, 'johndoe@example.org')
        self.assertEqual(user.experience, 'beginner')
        self.assertEqual(user.bio, 'Just a bio')
        self.assertTrue(self.is_logged_in())
