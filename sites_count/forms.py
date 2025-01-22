from datetime import date

from django import forms


class SiteCountForm(forms.Form):
    """A form to request site count data."""

    date = forms.DateField(
        label='',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            },
            format='%Y-%m-%d',  # noqa: WPS323 - False positive
        ),
        initial=date.today(),
        required=True,
    )
    table_type = forms.ChoiceField(
        choices=[
            ('operator', 'operator'),
            ('vendor', 'vendor'),
            ('region', 'region'),
        ],
        initial='operators',
        label='',
    )
