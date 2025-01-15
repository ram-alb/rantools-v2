from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(UserCreationForm):
    """User registration form."""

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

    def clean_email(self):
        """Ensure the email is valid and generate a username from it."""
        email = self.cleaned_data.get('email').lower()
        if '@kcell.kz' not in email:
            raise ValidationError('Please use a Kcell email address.')

        self.cleaned_data['username'] = email.split('@')[0]
        return email

    def save(self, commit=True):
        """Save the user with the generated username in lowercase."""
        user = super().save(commit=False)
        user.username = self.cleaned_data['username'].lower()
        user.email = self.cleaned_data['email'].lower()
        if commit:
            user.save()
        return user

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'email',
            'password1',
            'password2',
        ]
