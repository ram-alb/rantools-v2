from django import forms


class SearchForm(forms.Form):
    """Form to handle search queries."""

    min_length = 5
    max_length = 5

    query = forms.CharField(
        label="",
        min_length=min_length,
        max_length=max_length,
        widget=forms.TextInput(
            attrs={
                "id": "ret-search",
                "class": "form-control",
                "placeholder": "Enter 5-digit site ID",
            },
        ),
    )

    def clean_query(self):
        """Validate the query field."""
        query_value = self.cleaned_data["query"]
        if not query_value.isdigit():
            raise forms.ValidationError("Enter exactly 5 digits.")
        return query_value
