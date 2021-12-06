from django.test import TestCase
from django import forms
from django.contrib.auth.hashers import check_password
from clubs.forms import UpdateForm
from clubs.models import User

class UpdateFormTestCase(TestCase):
    """Unit tests of the sign up form."""

    def setUp(self):
        self.form_input = {
            'first_name': 'leopold',
            'last_name': 'patrice',
            'username': 'leopo',
            'email': 'leopo@example.com',
            'experience': 'beginner',
            'bio': 'Hi, my name is Leo.',
        }

    def test_valid_update_form(self):
        form = UpdateForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = UpdateForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('experience', form.fields)
        self.assertIn('bio', form.fields)


    def test_form_uses_model_validation(self):
        self.form_input['username'] = 'us'
        form = UpdateForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = UpdateForm(data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        user = User.objects.get(username = 'leopo')
        self.assertEqual(user.first_name, 'leopold')
        self.assertEqual(user.last_name, 'patrice')
        self.assertEqual(user.email, 'leopo@example.com')
        self.assertEqual(user.email, 'leopo@example.com')
        self.assertEqual(user.experience, 'beginner')
