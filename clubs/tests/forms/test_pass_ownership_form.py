from django import forms
from django.test import TestCase
from clubs.forms import PassOwnershipForm

class PassOwnershipFormTestCase(TestCase):
    """Unit tests of the log in form."""

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.form_input = {'password': 'Password123', 'password_confirmation': 'Password123'}

    def test_form_contains_required_fields(self):
        form = PassOwnershipForm()
        self.assertIn('password', form.fields)
        self.assertIn('password_confirmation', form.fields)
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget,forms.PasswordInput))
        password_confirmation_field = form.fields['password_confirmation']
        self.assertTrue(isinstance(password_confirmation_field.widget,forms.PasswordInput))

    def test_valid_form(self):
        form = PassOwnershipForm(data=self.form_input)
        self.assertTrue(form.is_valid()) 

    def test_valid_form(self):
        self.form_input['new_password'] = 'Wrongpassword123'
        self.form_input['password_confirmation'] = 'Wrongpassword123'
        form = PassOwnershipForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        

    
    
