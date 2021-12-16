from django.http import response
from django.test import TestCase
from django.urls import reverse
from clubs.forms import PassOwnershipForm
from clubs.models import Club, User, ClubMember
from clubs.tests.helpers import reverse_with_next

class MakeOwnerTestCase(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_club_member.json',
                'clubs/tests/fixtures/other_users.json']
                

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.target_user = User.objects.get(username = 'janedoe')
        self.club = Club.objects.get(name='ChessHub')
        self.url = reverse('make_owner', kwargs={'club_id': self.club.id, 'user_id': self.target_user.id})
        ClubMember.objects.create(
            user = self.target_user,
            club = self.club,
            role = 'OFF'
        )
        self.form_input = {
            'password' : 'Password123', 
            'password_confirmation' : 'Password123', 
        }

    def test_make_owner_url(self):
        self.assertEqual(self.url,f'/{self.club.id}/pass_ownership/{self.target_user.id}/')

    def test_invalid_input_in_PassOwnership_form(self):
        self.client.login(username=self.user.username, password = 'Password123')
        self.form_input['password'] = 'WrongPassword123'
        response = self.client.post(self.url, self.form_input, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'make_owner.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PassOwnershipForm))
        self.assertEqual(self.club.owner, self.user)


    def test_valid_pass_ownership(self):
        self.client.login(username=self.user.username, password = 'Password123')
        response=self.client.post(self.url, self.form_input, follow=True)
        redirect_url = reverse('show_club',kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'show_club.html')
        self.club.refresh_from_db()
        self.assertEqual(self.club.owner, self.target_user)
    
    


        
   

        







