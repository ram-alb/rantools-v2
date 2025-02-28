from django import forms
from django.core.validators import RegexValidator


class SearchForm(forms.Form):
    """Form to handle search queries."""

    min_length = 5
    max_length = 50

    query = forms.CharField(
        label='',
        min_length=min_length,
        max_length=max_length,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9_]+$',
                message="Only letters, numbers, and underscore (_) are allowed.",
                code='invalid_query',
            ),
        ],
        widget=forms.TextInput(attrs={
            'id': 'hw-search',
            'class': 'form-control',
            'placeholder': 'Enter site id or sitename',
        }),
    )
