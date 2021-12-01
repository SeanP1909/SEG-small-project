from django import forms
from django.core.validators import RegexValidator
from .models import User

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "experience", "bio"]
        widgets = { "bio": forms.Textarea() }

    new_password = forms.CharField(
        label="Password", 
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
                message = 'The password must contain an uppercase, lowercase and numeric characters!'
                )
        ]
    )
    password_confirmation = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'The confirmation does not match the original password.')