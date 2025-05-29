from django import forms


class SearchForm(forms.Form):
    """Form for searching by site name and technology types."""

    site_name = forms.CharField(
        label='Input Sitename',
        required=True,
        min_length=5,
        widget=forms.TextInput(
            attrs={
                'id': 'input-field',
                'placeholder': 'Enter node name',
                'class': 'form-control',
            },
        ),
    )
    technologies = forms.MultipleChoiceField(
        choices=[
            ('5G', '5G'),
            ('4G', '4G'),
            ('3G', '3G'),
            ('2G', '2G'),
        ],
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'id': 'technologies',
                'class': 'checkbox-group',
            },
        ),
        label='Choose Technologies',
        required=True,
    )
