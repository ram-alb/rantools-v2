from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(UserCreationForm):
    """User registration form."""

    username = forms.CharField(
        label='Username',
        required=True,
        help_text='Use your kcell username without @kcell.kz',
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        help_text='Use your kcell email address',
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        help_text='Use your kcell password',
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(),
        help_text='To confirm, please enter your password again.',
    )

    def clean_username(self):
        """Ensure the username does not contain an email address."""
        username = self.cleaned_data.get('username')
        if '@' in username:
            raise ValidationError('Username should not contain an email address.')
        return username

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
