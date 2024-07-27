from django import forms


class SiteInfoForm(forms.Form):
    """A form for requesting site data by bts id."""

    max_length = 25
    bts_id = forms.CharField(
        label='',
        min_length=5,
        max_length=max_length,
        widget=forms.TextInput(
            attrs={
                'id': 'input-field',
                'placeholder': 'Enter site id',
                'class': 'form-control',
            },
        ),
    )
    source = forms.ChoiceField(
        label='',
        choices=(
            ('atoll', 'Atoll'),
            ('network', 'Network'),
        ),
    )
