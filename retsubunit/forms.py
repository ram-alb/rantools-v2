from django import forms
from django.core.validators import RegexValidator


class SearchForm(forms.Form):
    """Form to handle search queries."""

    min_length = 5
    max_length = 5

    query = forms.CharField(
        label="",
        min_length=min_length,
        max_length=max_length,
        validators=[
            RegexValidator(
                regex=r"^\d{5}$",
                message="Enter exactly 5 digits.",
                code="invalid_query",
            ),
        ],
        widget=forms.TextInput(
            attrs={
                "id": "ret-search",
                "class": "form-control",
                "placeholder": "Enter 5-digit site ID",
            },
        ),
    )
