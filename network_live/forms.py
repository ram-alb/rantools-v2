from django import forms


class SelectTables(forms.Form):
    """A form to check Technologies."""

    choices = (
        ('lte', 'LTE Cells'),
        ('wcdma', 'WCDMA Cells'),
        ('gsm', 'GSM Cells'),
        ('nr', 'NR Cells'),
    )

    technologies = forms.MultipleChoiceField(
        choices=choices,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
